---
name: telegram-context
description: 这是一个启用了切换功能的技能，它在会话开始时获取 Telegram 的消息历史记录，以确保对话的连贯性。该功能能够在不同会话之间保持上下文信息，而无需完全依赖内存文件。
homepage: https://github.com/openclaw/skills
metadata:
  openclaw:
    emoji: "💬"
    requires:
      bins: []
      env: []
    permissions:
      - message:read
---
# Telegram上下文管理

该功能通过在会话开始时获取最近的Telegram消息来保持对话的连贯性。启用该功能后，代理会自动检索消息历史记录，以便在会话中断后仍能保持对话的上下文。

## 致谢

由@fourthdensity创建

## 命令

- `/telegram-context on` — 启用自动消息历史记录检索
- `/telegram-context off` — 禁用自动检索
- `/telegram-context status` — 显示当前设置
- `/telegram-context fetch [n]` — 手动获取最后n条消息（默认值：20）

## 设置

1. 该技能会自动检测您使用的Telegram频道，无需额外配置
2. 设置信息存储在`memory/telegram-context.json`文件中
3. 仅当当前使用的频道为Telegram时，该功能才会激活

## 工作原理

当在Telegram中开始一个新的会话时：

1. 检查`memory/telegram-context.json`文件中的启用状态
2. 如果已启用，则通过`message`工具获取最近的消息
3. 将这些消息作为对话的上下文提供给用户
4. 更新`lastFetch`时间戳

## 状态文件

`memory/telegram-context.json`:
```json
{
  "enabled": true,
  "fetchCount": 20,
  "lastFetch": "2025-01-15T10:30:00Z"
}
```

## 实现细节

### 命令处理

**启用/禁用自动消息历史记录检索：**
```javascript
// Read current state
read: memory/telegram-context.json

// Update state
write: memory/telegram-context.json
{
  "enabled": true/false,
  "fetchCount": 20,
  "lastFetch": "2025-01-15T10:30:00Z"
}
```

**手动获取消息：**
```javascript
message: {
  action: "list",
  limit: 20  // or user-specified count
}
// Provide results as context summary
```

### 会话启动时的行为

在每次开始Telegram会话时：

1. 检查`memory/telegram-context.json`文件是否存在
2. 如果已启用，则使用`message`工具执行`action: "list"`操作
3. 将最近的消息汇总并显示在对话窗口中
4. （可选）向用户确认对话的连贯性已恢复

### 实现范围

该技能使用了OpenClaw内置的`message`工具：
- `action: "list"`—— 仅限于当前使用的Telegram聊天频道
- 无法访问其他聊天频道或外部Telegram账户
- 需要确保OpenClaw网关已配置正确的权限以访问Telegram频道

### 隐私与安全

**数据管理：**
- 仅从当前使用的聊天频道中获取消息（不会跨频道或与其他Telegram对话共享数据）
- 消息内容会显示在代理的对话窗口中，并会被发送到您配置的LLM（大型语言模型）提供商
- `memory/telegram-context.json`文件中不存储消息内容，仅保存设置和时间戳
- 消息内容可能会被记录在OpenClaw的会话日志中（具体取决于您的日志配置）

**对于敏感对话的建议：**
- 对于敏感对话，建议使用`/telegram-context fetch`命令手动获取消息
- 将`fetchCount`设置为较低的值（如5-10条消息），以减少上下文信息的泄露风险
- 在讨论敏感话题时，建议完全禁用该功能：`/telegram-context off`
- 请注意，获取到的消息会成为发送给AI模型的对话历史记录的一部分

**用户控制：**
- 可随时完全启用或禁用该功能（数据不会被持久化保存）
- 无需使用任何外部凭证或API密钥
- 该技能为纯指令驱动型，无需安装任何二进制文件

## 限制

- 仅支持Telegram聊天（不支持其他类型的频道）
- 需要通过OpenClaw网关获取相应的消息访问权限
- 如果消息历史记录过长，可能需要对其进行压缩以便显示在对话窗口中
- 获取到的消息会被发送到您配置的LLM提供商——请确保您的AI模型能够妥善处理这些数据

## 使用提示：

- 对于大多数场景，建议将`fetchCount`设置为10-30条消息，以在保持对话上下文和节省资源之间取得平衡
- 如果需要为特定任务获取更详细的上下文信息，可以使用`/telegram-context fetch 50`
- 该功能与`MEMORY.md`文件配合使用，可以更好地实现长期数据持久化