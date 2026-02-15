---
name: bluebubbles
description: 构建或更新 BlueBubbles 外部通道插件，用于 Clawdbot（扩展包、REST 请求/响应、Webhook 收发功能）。
---

# BlueBubbles 插件

在使用 BlueBubbles 通道插件时，请参考本文档。

## 架构
- 扩展包：`extensions/bluebubbles/`（入口文件：`index.ts`）
- 通道实现：`extensions/bluebubbles/src/channel.ts`
- Webhook 处理：`extensions/bluebubbles/src/monitor.ts`（通过 `api.registerHttpHandler` 注册）
- REST 辅助函数：`extensions/bluebubbles/src/send.ts` + `extensions/bluebubbles/src/probe.ts`
- 运行时桥接：`extensions/bluebubbles/src/runtime.ts`（通过 `api.runtime` 设置）
- 用于插件集成的目录条目：`src/channels/plugins/catalog.ts`

## 内部辅助函数（请使用这些函数，而非直接调用 API）
- `probeBlueBubbles`：位于 `extensions/bluebubbles/src/probe.ts`，用于检查插件运行状态。
- `sendMessageBlueBubbles`：位于 `extensions/bluebubbles/src/send.ts`，用于发送文本消息。
- `resolveChatGuidForTarget`：位于 `extensions/bluebubbles/src/send.ts`，用于查找聊天对象。
- `sendBlueBubblesReaction`：位于 `extensions/bluebubbles/src/reactions.ts`，用于发送回复消息。
- `sendBlueBubblesTyping` + `markBlueBubblesChatRead`：位于 `extensions/bluebubbles/src/chat.ts`，用于处理用户输入和标记聊天状态。
- `downloadBlueBubblesAttachment`：位于 `extensions/bluebubbles/src/attachments.ts`，用于下载传入的媒体文件。
- `buildBlueBubblesApiUrl` + `blueBubblesFetchWithTimeout`：位于 `extensions/bluebubbles/src/types.ts`，用于构建 REST 请求和设置超时。

## Webhook 功能
- BlueBubbles 通过 JSON 格式将消息发送到网关 HTTP 服务器。
- 防范性地对发送者/聊天 ID 进行规范化处理（不同版本的 payload 可能有所不同）。
- 跳过标记为“来自自身”的消息。
- 通过插件运行时 (`api.runtime`) 和 `clawdbot/plugin-sdk` 辅助函数将消息路由到核心回复流程。
- 对于附件/贴纸，当文本为空时使用 `<media:...>` 占位符，并通过 `MediaUrl(s)` 将媒体路径附加到消息中。

## 配置（核心设置）
- `channels.bluebubbles.serverUrl`（基础 URL）
- `channels.bluebubbles.password`
- `channels.bluebubbles.webhookPath`
- 操作权限控制：`channels.bluebubbles.actions.reactions`（默认值为 `true`）

## 消息处理注意事项
- **回复操作（Reactions）**：`react` 操作除了需要 `messageId` 外，还需要提供一个 `target`（电话号码或聊天标识符）。示例：`action=react target=+15551234567 messageId=ABC123 emoji=❤️`