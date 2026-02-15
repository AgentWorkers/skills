---
name: fieldy
description: 将 Fieldy 的 Webhook 转换为 Moltbot 的钩子（hooks）。
---

## 这些设置的作用

您需要配置 Moltbot Gateway 的 Webhook，使得发送到 `POST /hooks/fieldy` 的请求在触发代理执行之前，会先经过一个 **转换模块**（`fieldy-webhook.js`）的处理。

**`fieldy-webhook.js` 中的默认行为说明：**
- 如果发送 “Hey, Fieldy”（或仅发送 “Fieldy”），系统会使用该文本来触发代理执行。
- 不包含唤醒词（wake word）的转录内容不会触发代理执行；这些内容只会被 `fieldy-webhook.js` 记录到 JSONL 文件中（路径为 `<workspace>/fieldy/transcripts/`）。
- 您可以通过编辑 `fieldy-webhook.js` 来调整唤醒词、解析规则以及日志记录行为。

## 1) 将转换脚本放入配置好的 `transforms` 目录中

您的 `hookstransformsDir` 是：

`/root/clawd/skills/fieldy/scripts`

请将以下脚本从当前仓库复制到目标目录：

- 从：`src/fieldy-webhook.js`
- 到：`/root/clawd/skills/fieldy/scripts/fieldy-webhook.js`

**注意：** 确保目标文件的名称为 `fieldy-webhook.js`，以匹配配置文件中的指定名称。

## 2) 将 Webhook 映射添加到 `~/.clawdbot/moltbot.json` 中**

在 `~/.clawdbot/moltbot.json` 文件中添加以下配置：

```json
"hooks": {
  "token": "insert-your-token",
  "transformsDir": "/root/clawd/skills/fieldy/scripts",
  "mappings": [
    {
      "match": {
        "path": "fieldy"
      },
      "action": "agent",
      "name": "Fieldy",
      "messageTemplate": "{{message}}",
      "deliver": true,
      "transform": {
        "module": "fieldy-webhook.js"
      }
    }
  ]
}
```

**重要提示：**
- 当启用 Webhook 功能时，`hooks.token` 是必需的（详见 [Webhook 文档](https://docs.molt.bot/automation/webhook.md)）。
- 请确保配置文件中存在 `hooks.enabled: true`（可选地，还需要配置 `hooks.path`，默认值为 `/hooks`）。

## 3) 重启 Gateway

通常情况下，修改插件配置后需要重启 Gateway。重启后，Webhook 端点才能生效。

## 4) 在 Fieldy 应用中配置 Webhook URL

- 登录到您的 Fieldy 应用
- 进入 **设置** → **开发者设置**
- 将 **Webhook 端点 URL** 设置为：

`https://your-url.com/hooks/fieldy?token=insert-your-token`

**注意：** Moltbot 支持通过请求头传递 token，但许多 Webhook 提供商仅支持通过查询参数传递。Moltbot 仍然支持使用 `?token=` 的方式（详见 [Webhook 文档](https://docs.molt.bot/automation/webhook.md)）。

## 5) 测试

**示例请求（请根据实际情况调整主机、端口和 token）：**

```bash
curl -X POST "http://127.0.0.1:18789/hooks/fieldy" \
  -H "Authorization: Bearer insert-your-token" \
  -H "Content-Type: application/json" \
  -d '{"transcript":"Hey Fieldy summarize this: hello world"}'
```