---
name: agent-autonomy-kit
version: 1.0.0
description: 不要再等待提示了，继续工作吧。
homepage: https://github.com/itskai-dev/agent-autonomy-kit
metadata:
  openclaw:
    emoji: "🚀"
    category: productivity
---

# 代理自主性套件（Agent Autonomy Kit）

将您的代理从被动响应式转变为主动式（proactive）。

## 快速入门

1. 创建 `tasks/QUEUE.md` 文件，其中包含 “Ready”（就绪）、”In Progress”（进行中）、”Blocked”（阻塞） 和 “Done”（已完成） 状态。
2. 更新 `HEARTBEAT.md` 文件，使其能够从任务队列中获取任务并执行相应操作。
3. 设置定时任务（cron jobs），以便在夜间执行任务并生成每日报告。
4. 在无需人工提示的情况下监控任务的执行过程。

## 关键概念

- **任务队列（Task Queue）**：确保始终有任务可供执行。
- **主动式心跳机制（Proactive Heartbeat）**：主动执行任务，而不仅仅是定期检查状态。
- **持续运行（Continuous Operation）**：持续运行任务，直到达到系统限制。

详细文档请参阅 `README.md`。