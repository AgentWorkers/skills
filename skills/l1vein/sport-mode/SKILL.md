---
name: sport-mode
description: 激活“运动模式”（Sport Mode）以实现高频监控（默认心跳间隔为3分钟）和自动清理功能。在监督高强度任务（如代码编译、系统构建、数据迁移等）时使用该模式。
metadata:
  {
    "openclaw": { "emoji": "🏎️" }
  }
---

# 运动模式（Sport Mode）

该模式会临时提高心跳频率（默认为3分钟一次），并将相关监控任务添加到 `HEARTBEAT.md` 文件中。非常适合用于监控后台代理程序（如 Codex）、长时间运行的构建过程或交互式游戏。

## 使用方法

```bash
# Turn ON: Set heartbeat to 3m and set monitoring task
sport-mode on --task "Check Codex progress. If done, run sport-mode off."

# Custom Interval: Set to 1 minute
sport-mode on --task "Game tick" --every "1m"

# Turn OFF: Reset heartbeat to 30m and clear HEARTBEAT.md
sport-mode off
```

## 工作原理

1. **开启模式**：
   - 通过修改 `~/.openclaw/openclaw.json` 文件（实现热重载）来设置 `heartbeat.every` 的值。
   - 将当前任务信息写入 `HEARTBEAT.md` 文件，并在文件开头添加 “Sport Mode Active” 的标记。

2. **关闭模式**：
   - 将心跳频率恢复到默认的30分钟。
   - 清除 `HEARTBEAT.md` 文件中的所有相关内容。

## 最佳实践

### 1. 设定终止条件
除非你希望任务无限期地运行下去，否则务必为任务设置一个明确的终止条件。
- ✅ 正确的做法：**“监控构建过程。无论成功还是失败，都应关闭运动模式”。**
- ❌ 错误的做法：**“仅监控构建过程”。**（代理程序可能会无限循环地报告 “已完成”，直到你手动停止它。）

### 2. 使用状态机管理任务流程
对于多步骤的任务（如游戏或分阶段部署），让代理程序自行更新 `HEARTBEAT.md` 文件中的状态。
- 工作流程：读取当前状态 → 执行相应步骤 → 更新状态 → 进入等待状态。
- 这种方式可以使代理程序保持 “无状态”（不依赖于之前的交互记录），但任务本身仍具有状态信息。

### 3. 使用 tmux 提高可见性
如果监控任务需要输出终端信息（例如代码编写、编译过程），建议在 tmux 会话中运行该任务。
- 代理程序可以在不干扰任务运行的情况下查看终端输出。
- 用户也可以通过 `tmux attach` 命令实时查看任务进度。

### 4. 避免频繁发送无关信息
在高频运行的模式下（例如每分钟一次），应避免频繁发送 “没有发生任何变化” 的通知。
- 配置代理程序在状态没有变化时返回 `HEARTBEAT_OK`（表示一切正常）。
- 仅在任务完成、出现错误或最终成功时才通知用户。

## 实现说明
该功能通过 `openclaw config set` 在运行时安全地修改配置文件，从而实现无缝的 Gateway 重载。