---
name: snail-mail
description: 这是一个用于向操作员发送重要消息的“慢通道”收件箱功能。当发生值得注意的事件、异常情况或需要操作员做出决策的情况时，可以使用该功能——但这些情况并不紧急到需要立即打扰操作员。此外，当操作员要求查看收件箱、标记消息为已读或归档某些信息时，也可以使用该功能。
metadata: {"openclaw": {"requires": {"bins": ["node"], "env": ["OPENCLAW_WORKSPACE", "OPENCLAW_CHANNEL"]}}}
---

# 操作员收件箱

这是一个连接您和操作员的“慢通道”（即信息传递的缓冲区）。并非所有事件都值得立即通知操作员；收件箱仅记录重要的信息，并在操作员有时间查看时以美观的方式呈现这些信息。

## 设置

首次使用时，收件箱文件会自动创建在 `{workspace}/inbox/messages.json` 中。

**所需环境：** Node.js 运行时。

## 何时向收件箱写入信息

当某件事“足够重要，操作员需要知道，但又不是紧急到需要打断他们的工作”时，就将其写入收件箱。

### 适合写入收件箱的情况：
- **需要决策** — 只有人类才能解决的问题（例如付款、审批、政策相关事宜）
- **异常情况** — 错误、故障、异常行为、安全事件
- **值得关注的事件** — 重要的用户互动、媒体提及、重要里程碑、潜在机会
- **供参考** — 可能日后有用但当前无需采取行动的信息

### 不适合写入收件箱的情况：
- 常规性的成功事件（例如“定时任务正常运行”、“心跳检测通过”）
- 已经通过聊天告知操作员的信息
- 没有长期意义的小事
- 收件箱中已有的重复信息

## 优先级等级：
- **紧急** — 需要在几小时内得到处理（标题前加 `[URGENT]`）
- **重要** — 应在今天内查看（标题前加 `[IMPORTANT]`）
- **普通** — 操作员随时可以查看（无需加前缀）

### 编写高质量的信息条目：
- **标题：** 简短易读，包含相关方或事件内容（例如：“@bigaccount (500K) 提到了我们”，而不是“社交媒体事件”）
- **正文：** 1-3句话，说明发生了什么、为什么重要以及需要采取什么措施（如有必要可附上链接或处理方式）。

## 命令行工具使用方法

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

# Render for chat (auto-detects channel via OPENCLAW_CHANNEL)
node {skill}/scripts/inbox.js render [unread|all|archived]

# Render as HTML (force)
node {skill}/scripts/inbox.js render --html

# Render as markdown (force)
node {skill}/scripts/inbox.js render --md

# Render as plain text (force)
node {skill}/scripts/inbox.js render --text
```

## 查看收件箱内容

当操作员要求查看收件箱内容时（或输入“inbox”、“messages”、“check inbox”），运行以下命令：

```bash
node {skill}/scripts/inbox.js render [unread|all|archived] [--html|--md|--text]
```

根据通信渠道选择合适的格式：
- **Telegram、Webchat** → `--html`
- **Discord、Slack** → `--md`
- **SMS、纯文本** → `--text`

将输出结果作为回复发送给操作员。除非操作员询问，否则不要添加额外说明。

## 心跳检测集成

在系统进行心跳检测时，检查是否有未读的紧急或重要信息：

```bash
node {skill}/scripts/inbox.js list unread --json
```

如果存在紧急信息，应主动将其显示给操作员；否则保持静默。

## 存储方式

信息存储在 `{workspace}/inbox/messages.json` 文件中。该文件由单一用户（即代理）写入，因此无需锁定机制。写入操作采用原子性重命名机制（先创建临时文件 `.tmp`，再重命名原文件）以防止数据损坏。

**环境变量：**
- `OPENCLAW_WORKSPACE` — 收件箱存储的根目录（默认为 `$HOME`）
- `OPENCLAW_CHANNEL` — 用于自动识别通信渠道（Telegram/Discord/Slack/Webchat）