---
name: ai-automation-workflows
description: "构建结合多种模型和服务的自动化 AI 工作流程。常见模式包括：批量处理、定时任务、事件驱动的管道系统以及代理循环（agent loops）。可使用的工具包括：inference.sh 命令行工具（CLI）、Bash 脚本、Python SDK 以及 Webhook 集成。这些工作流程适用于内容自动化、数据处理、监控以及定期内容生成等场景。触发机制包括：AI 自动化、工作流程自动化、批量处理、AI 管道系统、自动化内容生成等。"
allowed-tools: Bash(infsh *)
---
# AI自动化工作流

通过 [inference.sh](https://inference.sh) 命令行工具（CLI）构建自动化AI工作流。

![AI自动化工作流](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg0v0nz7wv0qwqjtq1cam52z.jpeg)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Simple automation: Generate daily image
infsh app run falai/flux-dev --input '{
  "prompt": "Inspirational quote background, minimalist design, date: '"$(date +%Y-%m-%d)"'"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其SHA-256校验和。无需提升权限或启动后台进程。也可选择[手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## 自动化模式

### 模式1：批量处理

使用相同的工作流处理多个项目。

```bash
#!/bin/bash
# batch_images.sh - Generate images for multiple prompts

PROMPTS=(
  "Mountain landscape at sunrise"
  "Ocean waves at sunset"
  "Forest path in autumn"
  "Desert dunes at night"
)

for prompt in "${PROMPTS[@]}"; do
  echo "Generating: $prompt"
  infsh app run falai/flux-dev --input "{
    \"prompt\": \"$prompt, professional photography, 4K\"
  }" > "output_${prompt// /_}.json"
  sleep 2  # Rate limiting
done
```

### 模式2：顺序流程

将多个AI操作串联起来执行。

```bash
#!/bin/bash
# content_pipeline.sh - Full content creation pipeline

TOPIC="AI in healthcare"

# Step 1: Research
echo "Researching..."
RESEARCH=$(infsh app run tavily/search-assistant --input "{
  \"query\": \"$TOPIC latest developments\"
}")

# Step 2: Write article
echo "Writing article..."
ARTICLE=$(infsh app run openrouter/claude-sonnet-45 --input "{
  \"prompt\": \"Write a 500-word blog post about $TOPIC based on: $RESEARCH\"
}")

# Step 3: Generate image
echo "Generating image..."
IMAGE=$(infsh app run falai/flux-dev --input "{
  \"prompt\": \"Blog header image for article about $TOPIC, modern, professional\"
}")

# Step 4: Generate social post
echo "Creating social post..."
SOCIAL=$(infsh app run openrouter/claude-haiku-45 --input "{
  \"prompt\": \"Write a Twitter thread (5 tweets) summarizing: $ARTICLE\"
}")

echo "Pipeline complete!"
```

### 模式3：并行处理

同时运行多个操作。

```bash
#!/bin/bash
# parallel_generation.sh - Generate multiple assets in parallel

# Start all jobs in background
infsh app run falai/flux-dev --input '{"prompt": "Hero image..."}' > hero.json &
PID1=$!

infsh app run falai/flux-dev --input '{"prompt": "Feature image 1..."}' > feature1.json &
PID2=$!

infsh app run falai/flux-dev --input '{"prompt": "Feature image 2..."}' > feature2.json &
PID3=$!

# Wait for all to complete
wait $PID1 $PID2 $PID3
echo "All images generated!"
```

### 模式4：条件分支

根据结果选择不同的处理路径。

```bash
#!/bin/bash
# conditional_workflow.sh - Process based on content analysis

INPUT_TEXT="$1"

# Analyze content
ANALYSIS=$(infsh app run openrouter/claude-haiku-45 --input "{
  \"prompt\": \"Classify this text as: positive, negative, or neutral. Return only the classification.\n\n$INPUT_TEXT\"
}")

# Branch based on result
case "$ANALYSIS" in
  *positive*)
    echo "Generating celebration image..."
    infsh app run falai/flux-dev --input '{"prompt": "Celebration, success, happy"}'
    ;;
  *negative*)
    echo "Generating supportive message..."
    infsh app run openrouter/claude-sonnet-45 --input "{
      \"prompt\": \"Write a supportive, encouraging response to: $INPUT_TEXT\"
    }"
    ;;
  *)
    echo "Generating neutral acknowledgment..."
    ;;
esac
```

### 模式5：重试与回退

优雅地处理失败情况。

```bash
#!/bin/bash
# retry_workflow.sh - Retry failed operations

generate_with_retry() {
  local prompt="$1"
  local max_attempts=3
  local attempt=1

  while [ $attempt -le $max_attempts ]; do
    echo "Attempt $attempt..."

    result=$(infsh app run falai/flux-dev --input "{\"prompt\": \"$prompt\"}" 2>&1)

    if [ $? -eq 0 ]; then
      echo "$result"
      return 0
    fi

    echo "Failed, retrying..."
    ((attempt++))
    sleep $((attempt * 2))  # Exponential backoff
  done

  # Fallback to different model
  echo "Falling back to alternative model..."
  infsh app run google/imagen-3 --input "{\"prompt\": \"$prompt\"}"
}

generate_with_retry "A beautiful sunset over mountains"
```

## 定时自动化

### Cron作业设置

```bash
# Edit crontab
crontab -e

# Daily content generation at 9 AM
0 9 * * * /path/to/daily_content.sh >> /var/log/ai-automation.log 2>&1

# Weekly report every Monday at 8 AM
0 8 * * 1 /path/to/weekly_report.sh >> /var/log/ai-automation.log 2>&1

# Every 6 hours: social media content
0 */6 * * * /path/to/social_content.sh >> /var/log/ai-automation.log 2>&1
```

### 每日内容脚本

```bash
#!/bin/bash
# daily_content.sh - Run daily at 9 AM

DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="/output/$DATE"
mkdir -p "$OUTPUT_DIR"

# Generate daily quote image
infsh app run falai/flux-dev --input '{
  "prompt": "Motivational quote background, minimalist, morning vibes"
}' > "$OUTPUT_DIR/quote_image.json"

# Generate daily tip
infsh app run openrouter/claude-haiku-45 --input '{
  "prompt": "Give me one actionable productivity tip for today. Be concise."
}' > "$OUTPUT_DIR/daily_tip.json"

# Post to social (optional)
# infsh app run twitter/post-tweet --input "{...}"

echo "Daily content generated: $DATE"
```

## 监控与日志记录

### 日志记录框架

```bash
#!/bin/bash
# logged_workflow.sh - With comprehensive logging

LOG_FILE="/var/log/ai-workflow-$(date +%Y%m%d).log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting workflow"

# Track execution time
START_TIME=$(date +%s)

# Run workflow
log "Generating image..."
RESULT=$(infsh app run falai/flux-dev --input '{"prompt": "test"}' 2>&1)
STATUS=$?

if [ $STATUS -eq 0 ]; then
  log "Success: Image generated"
else
  log "Error: $RESULT"
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
log "Completed in ${DURATION}s"
```

### 错误警报

```bash
#!/bin/bash
# monitored_workflow.sh - With error alerts

run_with_alert() {
  local result
  result=$("$@" 2>&1)
  local status=$?

  if [ $status -ne 0 ]; then
    # Send alert (webhook, email, etc.)
    curl -X POST "https://your-webhook.com/alert" \
      -H "Content-Type: application/json" \
      -d "{\"error\": \"$result\", \"command\": \"$*\"}"
  fi

  echo "$result"
  return $status
}

run_with_alert infsh app run falai/flux-dev --input '{"prompt": "test"}'
```

## Python SDK自动化

```python
#!/usr/bin/env python3
# automation.py - Python-based workflow

import subprocess
import json
from datetime import datetime
from pathlib import Path

def run_infsh(app_id: str, input_data: dict) -> dict:
    """Run inference.sh app and return result."""
    result = subprocess.run(
        ["infsh", "app", "run", app_id, "--input", json.dumps(input_data)],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout) if result.returncode == 0 else None

def daily_content_pipeline():
    """Generate daily content."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(f"output/{date_str}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate image
    image = run_infsh("falai/flux-dev", {
        "prompt": f"Daily inspiration for {date_str}, beautiful, uplifting"
    })
    (output_dir / "image.json").write_text(json.dumps(image))

    # Generate caption
    caption = run_infsh("openrouter/claude-haiku-45", {
        "prompt": "Write an inspiring caption for a daily motivation post. 2-3 sentences."
    })
    (output_dir / "caption.json").write_text(json.dumps(caption))

    print(f"Generated content for {date_str}")

if __name__ == "__main__":
    daily_content_pipeline()
```

## 工作流模板

### 内容日历自动化

```bash
#!/bin/bash
# content_calendar.sh - Generate week of content

TOPICS=("productivity" "wellness" "technology" "creativity" "leadership")
DAYS=("Monday" "Tuesday" "Wednesday" "Thursday" "Friday")

for i in "${!DAYS[@]}"; do
  DAY=${DAYS[$i]}
  TOPIC=${TOPICS[$i]}

  echo "Generating $DAY content about $TOPIC..."

  # Image
  infsh app run falai/flux-dev --input "{
    \"prompt\": \"$TOPIC theme, $DAY motivation, social media style\"
  }" > "content/${DAY}_image.json"

  # Caption
  infsh app run openrouter/claude-haiku-45 --input "{
    \"prompt\": \"Write a $DAY motivation post about $TOPIC. Include hashtags.\"
  }" > "content/${DAY}_caption.json"
done
```

### 数据处理流程

```bash
#!/bin/bash
# data_processing.sh - Process and analyze data files

INPUT_DIR="./data/raw"
OUTPUT_DIR="./data/processed"

for file in "$INPUT_DIR"/*.txt; do
  filename=$(basename "$file" .txt)

  # Analyze content
  infsh app run openrouter/claude-haiku-45 --input "{
    \"prompt\": \"Analyze this data and provide key insights in JSON format: $(cat $file)\"
  }" > "$OUTPUT_DIR/${filename}_analysis.json"

done
```

## 最佳实践

1. **速率限制** - 在API调用之间设置延迟
2. **错误处理** - 始终检查返回代码
3. **日志记录** - 记录所有操作
4. **幂等性** - 设计可安全重运行的流程
5. **监控** - 在发生故障时发出警报
6. **备份** - 保存中间结果
7. **超时设置** - 设置合理的超时限制

## 相关技能

```bash
# Content pipelines
npx skills add inference-sh/skills@ai-content-pipeline

# RAG pipelines
npx skills add inference-sh/skills@ai-rag-pipeline

# Social media automation
npx skills add inference-sh/skills@ai-social-media-content

# Full platform skill
npx skills add inference-sh/skills@inference-sh
```

浏览所有应用程序：`infsh app list`