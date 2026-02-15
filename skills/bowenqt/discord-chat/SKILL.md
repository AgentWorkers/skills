---
name: discord-chat
description: 使用消息工具在 Discord 频道中发送消息、回复消息以及搜索消息历史记录。当用户需要与 Discord 通信（发送/回复消息或搜索消息）、查看 Discord 活动或与 Discord 频道互动时，可以使用该工具。
---

# Discord 聊天

您可以使用 Clawdbot 的 `message` 工具与 Discord 频道进行交互。

## 核心操作

### 发送消息

向 Discord 频道发送消息：

```bash
message action=send channel=discord target="#channel-name" message="Your message here"
```

或通过频道 ID 发送消息：

```bash
message action=send channel=discord target="1234567890" message="Your message here"
```

**提示：**
- 使用带有 `#` 前缀的频道名称或频道 ID
- 对于多个链接，请使用 `<>` 将其括起来以抑制嵌入内容：`<https://example.com>`
- 不要使用 Markdown 表格！请使用项目符号列表
- 可以使用 `effect=balloons` 或 `effectId=invisible-ink` 来添加效果

### 回复消息

回复特定消息：

```bash
message action=send channel=discord target="#channel-name" message="Reply text" replyTo="message-id"
```

`replyTo` 参数用于创建对指定消息 ID 的回复。

### 搜索消息

在频道中搜索消息：

```bash
message action=search channel=discord channelId="1234567890" query="search terms" limit=50
```

**搜索选项：**
- `query`：搜索关键词
- `authorId`：按作者过滤
- `before`/`after`/`around`：消息 ID 用于分页
- `limit`：最大结果数量（默认为 25）

有关高级搜索模式的详细信息，请参阅 [SEARCH.md](references/SEARCH.md)。

### 其他操作

**读取消息：**
```bash
message action=read channel=discord target="#channel-name" limit=20
```

**响应消息：**
```bash
message action=react channel=discord messageId="1234567890" emoji="👍"
```

**编辑消息：**
```bash
message action=edit channel=discord messageId="1234567890" message="Updated text"
```

**删除消息：**
```bash
message action=delete channel=discord messageId="1234567890"
```

## 快速参考

常用操作模式：
- **向频道发布公告**：`action=send target="#announcements"`
- **在帖子中回复**：`action=send replyTo="msg-id"`
- **查看最近的活动**：`action=read limit=10`
- **查找提及**：`action=search query="@username"`
- **确认收到**：`action=react emoji="✅"`

## 频道管理

**列出频道：**
```bash
message action=channel-list channel=discord guildId="server-id"
```

**获取频道信息：**
```bash
message action=channel-info channel=discord channelId="1234567890"
```

有关创建/编辑频道的详细信息，请参阅 [CHANNELS.md](references/CHANNELS.md)。

## 最佳实践

1. **尽可能使用频道名称** - `target="#general"` 比使用频道 ID 更清晰
2. **批量响应**：每条消息使用一个表情符号，选择最合适的表情
3. **遵循 Discord 的格式规范** - 使用项目符号列表而非表格，使用 `<link>` 来抑制嵌入内容
4. **先搜索再请求** - 在请求信息之前先查看聊天记录
5. **使用反应而不是回复** - 对于简单的确认，使用表情符号

## 配置

您的 Discord 机器人配置应位于网关配置文件中。当指定 `channel=discord` 时，`message` 工具会自动路由到已配置的 Discord 插件。

有关设置帮助，请参阅 [CONFIG.md](references/CONFIG.md)。