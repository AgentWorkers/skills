---
name: gamma
description: 使用 Gamma.app API 生成由 AI 支持的演示文稿、文档和社交媒体帖子。当用户请求创建演示文稿、提案资料、幻灯片集、文档或社交媒体轮播图时，可调用此 API。触发条件包括：“创建关于 X 的演示文稿”、“制作提案资料”、“生成幻灯片”或“创建关于 X 的社交媒体内容”。
metadata: {"clawdbot":{"requires":{"env":["GAMMA_API_KEY"]}}}
---

# Gamma.app API

使用人工智能生成精美的演示文稿、文档和社交媒体帖子。

## 设置

```bash
export GAMMA_API_KEY="sk-gamma-xxxxx"
```

## 快速命令

```bash
# Generate a presentation
{baseDir}/scripts/gamma.sh generate "Your content or topic here"

# Generate with options
{baseDir}/scripts/gamma.sh generate "Content" --format presentation --cards 12

# Check generation status
{baseDir}/scripts/gamma.sh status <generationId>

# List recent generations (if supported)
{baseDir}/scripts/gamma.sh list
```

## 脚本使用方法

### 生成内容

```bash
{baseDir}/scripts/gamma.sh generate "<content>" [options]

Options:
  --format       presentation|document|social (default: presentation)
  --cards        Number of cards/slides (default: 10)
  --instructions Additional instructions for styling/tone
  --amount       concise|detailed (default: detailed)
  --tone         e.g., "professional", "casual", "technical"
  --audience     e.g., "investors", "developers", "general"
  --image-source aiGenerated|web|none (default: aiGenerated)
  --image-style  illustration|photo|mixed (default: illustration)
  --wait         Wait for completion and return URL
```

### 示例

```bash
# Simple presentation
{baseDir}/scripts/gamma.sh generate "The future of AI automation" --wait

# Pitch deck with specific styling
{baseDir}/scripts/gamma.sh generate "$(cat pitch.md)" \
  --format presentation \
  --cards 15 \
  --instructions "Make it a professional pitch deck for investors" \
  --tone "professional" \
  --audience "investors" \
  --wait

# Social carousel
{baseDir}/scripts/gamma.sh generate "5 tips for productivity" \
  --format social \
  --cards 5 \
  --wait

# Document/report
{baseDir}/scripts/gamma.sh generate "Q4 2025 Performance Report" \
  --format document \
  --amount detailed \
  --wait
```

## API 参考

### 端点
```
POST https://public-api.gamma.app/v1.0/generations
```

### 请求头
```
X-API-KEY: <your-api-key>
Content-Type: application/json
```

### 请求体
```json
{
  "inputText": "Your content (1-750,000 chars)",
  "textMode": "generate",
  "format": "presentation|document|social",
  "numCards": 10,
  "additionalInstructions": "Styling instructions",
  "textOptions": {
    "amount": "concise|detailed",
    "tone": "professional",
    "audience": "target audience"
  },
  "imageOptions": {
    "source": "aiGenerated|web|none",
    "model": "flux-kontext-pro",
    "style": "illustration|photo"
  },
  "cardOptions": {
    "dimensions": "fluid|16x9|4x3|1x1|4x5|9x16"
  }
}
```

### 响应

- 初始响应：
```json
{"generationId": "abc123"}
```

- 检查任务状态：
```
GET https://public-api.gamma.app/v1.0/generations/<generationId>
```

- 任务完成后的响应：
```json
{
  "generationId": "abc123",
  "status": "completed",
  "gammaUrl": "https://gamma.app/docs/xxxxx",
  "credits": {"deducted": 150, "remaining": 7500}
}
```

## 格式选项

| 格式 | 尺寸 | 用途 |
|--------|------------|----------|
| 演示文稿 | fluid, 16x9, 4x3 | 用于 pitching 或幻灯片展示 |
| 文档 | fluid, pageless, letter, a4 | 用于报告或文档编写 |
| 社交媒体帖子 | 1x1, 4x5, 9x16 | 适用于 Instagram 或 LinkedIn 的轮播图 |

## 注意事项

- 生成内容通常需要 1-3 分钟的时间。
- 每生成一份内容会扣除一定的费用（每份演示文稿约 150-300 单位费用）。
- 输入文本可以使用 Markdown 格式。
- 可以使用 `--wait` 标志来等待生成完成，并直接获取生成的 URL。