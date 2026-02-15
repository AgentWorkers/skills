---
name: eureka-feedback
description: 向 Eureka（主要的人工智能代理）请求反馈或帮助。
triggers:
  - ask eureka
  - eureka feedback
  - check with eureka
  - delegate to eureka
---

# 与 Eureka 通信

Eureka 是主要的 AI 代理，它以 @Eureka_Agent_Bot 的身份在 Telegram 上运行。Eureka 使用 Opus 4.5 技术，负责高级别的规划、决策和任务协调工作。

## 何时联系 Eureka
- 需要战略指导或架构决策
- 在实施某项方案之前希望获得反馈
- 任务需要超出纯编程范围的技能（如家庭自动化、任务调度、内存管理等）
- 需要报告委托任务的完成情况

## 如何向 Eureka 发送消息

向 Eureka 的代理发送消息：

```bash
clawdbot agent --agent main --message "<your message>"
```

若希望 Eureka 的回复通过您的 Telegram 机器人直接发送给您，请执行以下操作：

```bash
clawdbot agent --agent main --message "<message>" --deliver --reply-channel telegram --reply-account mason --reply-to 1878354815
```

## 最佳实践
- 简明扼要地说明您的需求——Eureka 基于 Opus 技术运行，因此高效、简洁的请求会得到优先处理
- 在报告任务完成情况时，请总结所完成的工作及遇到的任何问题
- 如果 Eureka 委托了任务给您，请务必反馈任务的结果