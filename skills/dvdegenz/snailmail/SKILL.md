---
name: snail-mail
description: 这是一个用于向操作员发送重要消息的“慢通道”收件箱功能。当发生需要引起注意的事件、异常情况或需要做出决策的情况时，可以使用该功能来通知操作员——但这些情况并不紧急到需要立即中断操作员的当前工作。此外，当操作员要求查看自己的收件箱、标记消息为已读或归档某些邮件时，也可以使用该功能。
---

# 操作员收件箱

这是一个连接您和操作员的“慢通道”（即信息传递的缓冲区）。并非所有事件都值得立即通知操作员；收件箱只会记录重要的信息，并在操作员有空查看时以清晰的方式呈现这些内容。

## 设置

首次使用时，收件箱文件会自动创建在 `{workspace}/inbox/messages.json` 中。

## 何时向收件箱写入信息

当有以下情况时，向收件箱写入信息：
- 事件足够重要，操作员需要知道，但又不紧急到需要打扰他们。
- 出现异常情况（如错误、故障、异常行为或安全事件）。
- 有值得关注的事件发生（如用户互动、媒体提及、重要里程碑或机会）。
- 提供一些背景信息，虽然目前不需要采取行动，但未来可能有用。

## 何时不要写入信息：
- 常规操作成功（例如“定时任务正常运行”、“心跳检测通过”）。
- 已经在聊天中告知操作员的内容。
- 无关紧要的琐碎事件。
- 收件箱中已有的重复信息。

## 优先级级别：
- **紧急**：需在几小时内得到处理（标题前加 `[URGENT]`）。
- **重要**：应当天处理（标题前加 `[IMPORTANT]`）。
- **普通**：操作员随时可以查看（无需加前缀）。

## 如何撰写有效的信息：
- **标题**：简短且易于阅读，明确说明事件的相关方或内容（例如：“@bigaccount (500K) 提到了我们”，而不是“社交媒体事件”）。
- **正文**：1-3句话，说明发生了什么、为什么重要以及需要采取什么措施（如有的话）。相关链接或处理方式也请一并提供。

## 命令行工具使用

```bash
# Add entry
node {skill}/scripts/inbox.js add "Title" "Description of what happened"

# Add with priority
node {skill}/scripts/inbox.js add "[URGENT] Server disk 95%" "Only 2GB remaining on /dev/sda1"

# List unread
node {skill}/scripts/inbox.js list

# List all (including read)
node {skill}/scripts/inbox.js list all

# List archived
node {skill}/scripts/inbox.js list archived

# Mark one read
node {skill}/scripts/inbox.js read <id>

# Mark all read
node {skill}/scripts/inbox.js read-all

# Archive one
node {skill}/scripts/inbox.js archive <id>

# Archive all read
node {skill}/scripts/inbox.js archive-read

# Render for chat (auto-detects channel)
node {skill}/scripts/inbox.js render [unread|all|archived]

# Render as HTML (force)
node {skill}/scripts/inbox.js render --html

# Render as markdown (force)
node {skill}/scripts/inbox.js render --md

# Render as plain text (force)
node {skill}/scripts/inbox.js render --text
```

## 查看收件箱内容

当操作员要求查看收件箱内容时（或输入 “inbox”、“messages”、“check inbox”），运行以下命令：

```bash
node {skill}/scripts/inbox.js render [unread|all|archived] [--html|--md|--text]
```

根据通信渠道选择合适的显示格式：
- **Telegram、Webchat**：`--html`
- **Discord、Slack**：`--md`
- **SMS、纯文本**：`--text`

将结果显示为回复内容。除非操作员另有要求，否则不要添加额外的说明。

## 心跳检测集成

在心跳检测过程中，检查是否有未读的紧急或重要信息：

```bash
node {skill}/scripts/inbox.js list unread --json
```

如果发现紧急信息，应主动提醒操作员；否则保持静默。

## 存储方式

所有信息都存储在 `{workspace}/inbox/messages.json` 文件中。该文件由单一用户（即代理）写入，因此无需锁定机制。写入操作采用原子性重命名方式（先创建临时文件 `.tmp`，再重命名原文件），以防止数据损坏。