---
name: sending-reactions
description: XMTP代理的emoji反应和思考指示器：用于在消息中添加反应效果，或通过思考表情来显示处理状态。这些功能会在用户发送emoji反应、显示思考指示器或确认收到消息时触发。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP 反应功能

支持发送和接收表情符号（emoji）作为反馈，包括用于表示思考状态的特定表情模式。

## 适用场景

在以下情况下请参考这些指南：
- 用表情符号回复用户消息
- 显示处理或思考中的状态
- 接收并处理用户的反馈
- 实现确认用户反馈的机制

## 规则分类（按优先级）

| 优先级 | 规则类别 | 影响程度 | 前缀 |
|---------|-----------|-----------|---------|
| 1       | 发送       | 高        | `send-`     |
| 2       | 接收       | 高        | `receive-`     |
| 3       | 表情模式     | 中        | `patterns-`   |

## 快速参考

### 发送（高优先级）
- `send-reaction`  - 向消息发送表情符号作为反馈

### 接收（高优先级）
- `receive-reaction` - 处理收到的用户反馈

### 表情模式（中等优先级）
- `patterns-thinking`  - 用于表示思考状态的表情模式

## 快速入门

```typescript
// Send a reaction
await ctx.conversation.sendReaction({
  reference: ctx.message.id,
  action: "added",
  content: "👍",
  schema: "unicode",
});

// Thinking indicator pattern
await ctx.conversation.sendReaction({
  reference: ctx.message.id,
  action: "added",
  content: "⏳",
  schema: "unicode",
});

// Process...

await ctx.conversation.sendReaction({
  reference: ctx.message.id,
  action: "removed",
  content: "⏳",
  schema: "unicode",
});
```

## 使用方法

如需详细说明，请阅读相应的规则文件：

```
rules/send-reaction.md
rules/receive-reaction.md
rules/patterns-thinking.md
```