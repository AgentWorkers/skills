---
name: tmux-agents
description: 在 tmux 会话中管理后台编码代理程序。可以启动 Claude Code 或其他代理程序，查看进度并获取结果。
version: 1.0.0
author: Jose Munoz
homepage: https://clawdhub.com/skills/tmux-agents
triggers:
  - spawn agent
  - coding task
  - background task
  - tmux session
  - run codex
  - run gemini
  - local agent
  - ollama agent
metadata:
  clawdbot:
    emoji: "🖥️"
    requires:
      bins: ["tmux"]
    install:
      - id: brew-tmux
        kind: brew
        formula: tmux
        bins: ["tmux"]
        label: "Install tmux (brew)"
---

# Tmux Agents

在持久的 tmux 会话中运行编程代理。这些代理会在你进行其他操作时在后台运行。

## 可用的代理

### ☁️ 云代理（需要 API 许可）

| 代理 | 命令 | 适用场景 |
|-------|---------|----------|
| **claude** | Claude Code | 复杂的编码任务、代码重构、完整的项目开发 |
| **codex** | OpenAI Codex | 快速编辑、自动审批功能 |
| **gemini** | Google Gemini | 研究、分析、文档编写 |

### 🦙 本地代理（通过 Ollama 免费使用）

| 代理 | 命令 | 适用场景 |
|-------|---------|----------|
| **ollama-claude** | Claude Code + Ollama | 长时间的实验、大规模的代码重构 |
| **ollama-codex** | Codex + Ollama | 扩展的编码会话 |

本地代理会使用你 Mac 的 GPU，无需支付 API 费用，非常适合进行实验！

## 快速命令

### 创建一个新的代理会话
```bash
./skills/tmux-agents/scripts/spawn.sh <name> <task> [agent]

# Cloud (uses API credits)
./skills/tmux-agents/scripts/spawn.sh fix-bug "Fix login validation" claude
./skills/tmux-agents/scripts/spawn.sh refactor "Refactor the auth module" codex
./skills/tmux-agents/scripts/spawn.sh research "Research caching strategies" gemini

# Local (FREE - uses Ollama)
./skills/tmux-agents/scripts/spawn.sh experiment "Rewrite entire test suite" ollama-claude
./skills/tmux-agents/scripts/spawn.sh big-refactor "Refactor all services" ollama-codex
```

### 列出正在运行的会话
```bash
tmux list-sessions
# or
./skills/tmux-agents/scripts/status.sh
```

### 检查某个会话的状态
```bash
./skills/tmux-agents/scripts/check.sh session-name
```

### 远程查看会话的实时输出
```bash
tmux attach -t session-name
# Detach with: Ctrl+B, then D
```

### 向会话发送额外的指令
```bash
tmux send-keys -t session-name "additional instruction here" Enter
```

### 完成后终止会话
```bash
tmux kill-session -t session-name
```

## 何时使用本地代理与云代理

| 使用场景 | 推荐方案 |
|----------|----------------|
| 需要快速处理且时间敏感的任务 | ☁️ 云代理（响应更快） |
| 需要考虑预算的开销较大的任务 | 🦙 本地代理 |
| 需要长时间运行的实验（可能存在失败风险） | 🦙 本地代理 |
| 代码审查（生产环境） | ☁️ 云代理（更智能） |
| 学习或探索新功能 | 🦙 本地代理 |
| 大规模的代码重构 | 🦙 本地代理 |

## 并行运行多个代理

可以同时运行多个代理：
```bash
# Mix and match cloud + local
./scripts/spawn.sh backend "Implement user API" claude           # Cloud
./scripts/spawn.sh frontend "Build login form" ollama-codex      # Local
./scripts/spawn.sh docs "Write API documentation" gemini         # Cloud
./scripts/spawn.sh tests "Write all unit tests" ollama-claude    # Local
```

### 一次性查看所有代理的状态
```bash
./skills/tmux-agents/scripts/status.sh
```

## Ollama 的设置

使用本地代理需要安装 Ollama 并配置相应的编程模型：
```bash
# Pull recommended model
ollama pull glm-4.7-flash

# Configure tools (one-time)
ollama launch claude --model glm-4.7-flash --config
ollama launch codex --model glm-4.7-flash --config
```

## 提示

- 即使 Clawdbot 重启，会话也会保持持续运行状态。
- 对于风险较高或实验性的工作，建议使用本地代理。
- 对于生产环境中的关键任务，建议使用云代理。
- 可以使用 `tmux ls` 命令查看所有正在运行的会话。
- 完成任务后终止会话以释放系统资源。