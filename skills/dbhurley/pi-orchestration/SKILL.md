---
name: pi-orchestration
description: 使用 Pi Coding Agent 将多个 AI 模型（如 GLM、MiniMax 等）作为工作节点进行协调管理，同时由 Claude 负责整体的协调工作。
homepage: https://github.com/mariozechner/pi-coding-agent
metadata: {"clawdis":{"emoji":"🎭","requires":{"bins":["pi"]}}}
---

# Pi编排

使用Claude作为编排器，通过Pi Coding Agent来启动和协调多个AI模型工作者（如GLM、MiniMax等）。

## 支持的提供商

| 提供商 | 模型 | 状态 |
|----------|-------|--------|
| **GLM** | glm-4.7 | ✅ 可用 |
| **MiniMax** | MiniMax-M2.1 | ✅ 可用 |
| OpenAI | gpt-4o等 | ✅ 可用 |
| Anthropic | claude-* | ✅ 可用 |

## 设置

### 1. GLM（Zhipu AI）

从[open.bigmodel.cn](https://open.bigmodel.cn/)获取API密钥

```bash
export GLM_API_KEY="your-glm-api-key"
```

### 2. MiniMax

从[api.minimax.chat](https://api.minimax.chat/)获取API密钥

```bash
export MINIMAX_API_KEY="your-minimax-api-key"
export MINIMAX_GROUP_ID="your-group-id"  # Required for MiniMax
```

## 使用方法

### 直接命令

```bash
# GLM-4.7
pi --provider glm --model glm-4.7 -p "Your task"

# MiniMax M2.1
pi --provider minimax --model MiniMax-M2.1 -p "Your task"

# Test connectivity
pi --provider glm --model glm-4.7 -p "Say hello"
```

### 编排模式

Claude（Opus）可以作为后台工作者来执行以下任务：

#### 后台工作者
```bash
bash workdir:/tmp/task background:true command:"pi --provider glm --model glm-4.7 -p 'Build feature X'"
```

#### 并行处理（tmux）
```bash
# Create worker sessions
tmux new-session -d -s worker-1
tmux new-session -d -s worker-2

# Dispatch tasks
tmux send-keys -t worker-1 "pi --provider glm --model glm-4.7 -p 'Task 1'" Enter
tmux send-keys -t worker-2 "pi --provider minimax --model MiniMax-M2.1 -p 'Task 2'" Enter

# Check progress
tmux capture-pane -t worker-1 -p
tmux capture-pane -t worker-2 -p
```

#### Map-Reduce模式
```bash
# Map: Distribute subtasks to workers
for i in 1 2 3; do
  tmux send-keys -t worker-$i "pi --provider glm --model glm-4.7 -p 'Process chunk $i'" Enter
done

# Reduce: Collect and combine results
for i in 1 2 3; do
  tmux capture-pane -t worker-$i -p >> /tmp/results.txt
done
```

## 编排脚本

```bash
# Quick orchestration helper
uv run {baseDir}/scripts/orchestrate.py spawn --provider glm --model glm-4.7 --task "Build a REST API"
uv run {baseDir}/scripts/orchestrate.py status
uv run {baseDir}/scripts/orchestrate.py collect
```

## 最佳实践

1. **任务分解**：将大型任务拆分为独立的子任务。
2. **模型选择**：使用GLM处理中文内容，使用MiniMax处理创造性任务。
3. **错误处理**：在收集结果之前检查工作者的状态。
4. **资源管理**：任务完成后清理tmux会话。

## 示例：并行代码审查

```bash
# Claude orchestrates 3 workers to review different files
tmux send-keys -t worker-1 "pi --provider glm -p 'Review auth.py for security issues'" Enter
tmux send-keys -t worker-2 "pi --provider minimax -p 'Review api.py for performance'" Enter  
tmux send-keys -t worker-3 "pi --provider glm -p 'Review db.py for SQL injection'" Enter

# Wait and collect
sleep 30
for i in 1 2 3; do
  echo "=== Worker $i ===" >> review.md
  tmux capture-pane -t worker-$i -p >> review.md
done
```

## 注意事项

- 必须安装Pi Coding Agent：`npm install -g @anthropic/pi-coding-agent`
- GLM和MiniMax提供丰富的免费 tier。
- Claude负责协调工作，具体任务由工作者完成。
- 可以结合进程管理工具来更好地管理后台任务。