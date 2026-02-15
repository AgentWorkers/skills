# Slack Hub 技能

OpenClaw 的专业 Slack 集成功能，支持消息发送、主题讨论（线程）以及工作区搜索。

## 配置
需要在您的 `.env` 文件中设置 Slack 机器人令牌（`xoxb-...`），并将其命名为 `SLACK_BOT_TOKEN`。

## 工具

### `slack_send`
向指定频道或用户发送消息。
- `target`：频道 ID 或名称（例如：“#general”）。
- `message`：消息内容。
- `thread_ts`：（可选）用于回复主题讨论的时间戳。

### `slack_search`
在工作区内搜索消息或文件。
- `query`：搜索关键词。

### `slack_list_channels`
列出工作区中的所有公共频道。

## 实现说明
- 使用 `https://slack.com/api/chat.postMessage` 进行消息发送。
- 使用 `https://slack.com/api/search.messages` 进行消息搜索。
- 为高流量工作区实现了速率限制机制（防止频繁请求）。