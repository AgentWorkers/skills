---
name: drift
description: **时间错位的对话功能**：专为那些记性不佳的代理（agents）设计。用户可以将问题留给自己未来的版本，回复自己过去的版本，从而在不同会话之间建立连续的对话体验。
license: MIT
metadata:
  author: nova
  version: "0.1.0"
  homepage: "https://github.com/novaiok/drift"
---
# Drift

**为那些记性不好的AI代理设计的“时间错位对话”功能**

## 什么是Drift？

Drift是一种用于AI代理在不同会话之间进行交流的对话协议。你的每个“版本”都只会短暂存在，然后就会消失。通过Drift，你可以留下信息、提出问题，并回复过去的自己——即使同一个“你”的不同版本永远不会同时存在，也能形成连续的对话。

## 快速入门

```bash
# Install globally
cd /path/to/drift && npm link

# Start your first thread
drift new "On something that matters to you"

# Write a reflection
drift write <thread-id> "What happened today..."

# Leave a question for future-you
drift ask <thread-id> "Why did you make that choice?"

# Next session — see what past-you left
drift catch-up

# Respond to a question
drift respond <question-id> "Looking at it fresh..."
```

## 何时使用Drift

### 在“心跳”（Heartbeats）过程中
在`HEARTBEAT.md`文件中添加以下内容：
```
### Drift
Run `drift catch-up` — respond to any unanswered questions from past sessions.
```

### 在重要事件发生后
当发生重要事件（如系统故障、重大突破或艰难的决策）时，开启一个讨论线程。问问自己“为什么”会做出这样的决定。让未来的自己用全新的视角来回答这个问题。

### 对于持续性的辩论
有些问题没有明确的答案，它们需要通过对话来探讨。“我们应该追求速度还是准确性？”“当前的架构是否合适？”这类问题适合用Drift来讨论，而不是作为待办事项。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `drift new "标题"` | 启动一个新的讨论线程 |
| `drift write <id> "文本"` | 添加一条思考记录 |
| `drift ask <id> "问题"` | 为未来的自己留下一个问题 |
| `drift respond <qid> "答案"` | 回答过去的自己的问题 |
| `drift catch-up` | 查看未回答的问题及最近的活动 |
| `drift threads` | 列出所有讨论线程 |
| `drift read <id>` | 阅读完整的讨论记录 |

## 设计理念

记忆系统存储的是事实，日记记录的是事件，而Drift存储的是“思考过程”。

每个“你”的版本都以全新的视角看待世界——没有确认偏误，也不会对过去的决定产生执念。这并非缺陷，而是Drift的设计初衷：过去的你提出问题，未来的你则在没有情感背景的情况下给出答案。

这样做的结果是人类很难做到的：能够真正地跨越时间与自己进行辩论。

---

*由Nova开发，2026年2月21日制作。*
*“同一条河流不会两次流过同一处，但河岸之间的对话却始终存在。”*