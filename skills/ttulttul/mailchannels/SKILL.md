---
name: mailchannels-email-api
description: 通过 MailChannels 的 Email API 发送电子邮件，并将已签名的交付事件（delivery-event）Webhook 数据导入 Clawdbot（Moltbot）。
homepage: https://docs.mailchannels.net/email-api/
metadata: {"moltbot":{"emoji":"📨","requires":{"env":["MAILCHANNELS_API_KEY","MAILCHANNELS_ACCOUNT_ID"],"bins":["curl"]},"primaryEnv":"MAILCHANNELS_API_KEY"}}
---

# MailChannels 邮件 API（发送邮件 + 通知事件）

## 环境要求

**必填项：**
- `MAILCHANNELS_API_KEY`（在请求头中设置为 `X-Api-Key`）
- `MAILCHANNELS_ACCOUNT_ID`（也称为 `customer_handle`）

**可选项：**
- `MAILCHANNELS_BASE_URL`（默认值：`https://api.mailchannels.net/tx/v1`）
- `MAILCHANNELS_WEBHOOK_ENDPOINT_URL`

## 域名配置（DNS）

为每个发件人域名创建一个 TXT 记录：
- 主机：`_mailchannels.<your-domain>`
- 值：`v=mc1; auid=<YOUR_ACCOUNT_ID>`

## API 快速参考

**基础 URL：** `${MAILCHANNELS_BASE_URL}-https://api.mailchannels.net/tx/v1`
- **发送邮件：** `POST /send`
- **异步发送：** `POST /send-async`
- **Webhook：** `POST /webhook?endpoint=<url>`, `GET /webhook`, `DELETE /webhook`, `POST /webhook/validate`
- **公钥：** `GET /webhook/public-key?id=<keyid>`

## 发送邮件

**最低要求的数据字段：** `personalizations`, `from`, `subject`, `content`。
- 使用 `/send` 发送普通邮件；使用 `/send-async` 发送队列中的邮件或低延迟邮件。这两种方式都会触发 Webhook。
- 确保保存 MailChannels 的关联 ID（例如 `request_id`）。

## 通知事件（Webhook）

MailChannels 会发送一个 JSON 数组作为通知。常见字段包括：`email`, `customer_handle`, `timestamp`, `event`, `request_id`。
**退信相关字段：** `recipients`, `status`, `reason`, `smtp_id`。

## Moltbot 的 Hook 路由配置

1. 在 `~/.clawdbot/moltbot.json` 中启用 Hook 功能。
2. 通过 `hooks.mappings` 将 `/hooks/<path>` 映射到相应的代理操作，并可选地添加转换逻辑。
3. 将公共 Webhook 端点注册到 MailChannels：`/webhook?endpoint=...`

## Webhook 签名验证

**所需请求头：** `Content-Digest`, `Signature-Input`, `Signature`。

**验证步骤：**
1. 解析 `Signature-Input`（包含签名名称、创建时间、算法和密钥 ID）。
2. 拒绝过时的创建时间值。
3. 根据 `keyid` 获取公钥。
4. 根据 RFC 9421 规范重新生成签名。
5. 验证 ed25519 签名（避免手动计算签名）。
6. 确保 JSON 正文是一个数组，并且每个事件中的 `customer_handle` 与 `MAILCHANNELS_ACCOUNT_ID` 一致。

## 关联信息与状态更新

存储内部消息 ID 和 MailChannels 的 ID（例如 `request_id`, `smtp_id`）。
根据事件更新邮件状态：`processed`, `delivered`, `soft-bounced`, `hard-bounced`, `dropped`。

**运营建议：**
- 快速返回 2xx 状态码以表示请求成功。
- 异步处理请求。
- 存储原始事件数据。
- 避免重复发送请求。