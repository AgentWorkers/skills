---
name: ngrok-unofficial-webhook-skill
description: 启动一个 ngrok 隧道，用于接收传入的 Webhook 请求并通过大型语言模型（LLM）进行处理。当用户请求监听 Webhook、设置 Webhook 端点、启动 ngrok，或者其他技能（如 Zoom RTMS 会议助手）需要一个公共 Webhook URL 时，可以使用此功能。该功能会接收 Webhook 的数据 payload，并由大型语言模型决定如何处理这些数据。
---

# Ngrok Webhook 监听器

通过 ngrok 启动一个公共 webhook 端点。接收到的 webhook 请求会自动路由到相应的技能，或由用户手动处理。

## 先决条件

```bash
cd skills/ngrok-unofficial-webhook-skill
npm install
```

## 环境变量

在技能的 `.env` 文件中设置这些变量（可参考 `.env.example` 文件）。

**必填变量：**
- `NGROK_AUTHTOKEN` — 从 https://dashboard.ngrok.com 获取的 ngrok 认证令牌

**可选变量：**
- `NGROK_DOMAIN` — 用于生成稳定 URL 的 ngrok 域名
- `WEBHOOK_PORT` — 本地端口号（默认：`4040`）
- `WEBHOOK_PATH` — webhook 路径（默认：`/webhook`）
- `OPENCLAW_BIN` — openclaw 可执行文件的路径（默认：`openclaw`）
- `OPENCLAW_NOTIFY_CHANNEL` — 通知通道（默认：`whatsapp`）
- `OPENCLAW_NOTIFY_TARGET` — 通知接收者（电话号码或目标）

## 使用方法

### 启动 webhook 监听器

以 **后台进程** 的方式运行：

```bash
cd skills/ngrok-unofficial-webhook-skill
node scripts/webhook-server.js
```

服务器会将自身的公共 URL 输出到标准错误流（stderr）中：
```
NGROK_URL=https://xxxx.ngrok-free.app
Webhook endpoint: https://xxxx.ngrok-free.app/webhook
```

若需要长时间运行，可使用 `nohup` 命令启动后台进程：
```bash
nohup node scripts/webhook-server.js >> /tmp/ngrok-webhook.log 2>&1 &
```

### 当 webhook 到达时

1. 服务器会立即向发送者返回 **200 OK** 响应。
2. 服务器会检查已安装的技能中是否包含 `webhookEvents` 字段。
3. **自动路由**（无需用户干预）：
   - 如果有匹配的技能设置了 `forwardPort`，则将请求转发到本地服务。
   - 如果有匹配的技能设置了 `webhookCommands`，则会执行配置好的 shell 命令。
4. **手动路由**（由用户决定）：
   - 如果没有自动路由规则，系统会通过 WhatsApp 发送通知，通知中包含请求内容及匹配技能的列表。
   - 用户可以选择处理方式。

### 技能配置

技能可以通过在 `skill.json` 文件中添加 `webhookEvents` 来启用 webhook 处理功能：

```json
{
  "openclaw": {
    "webhookEvents": ["meeting.rtms_started", "meeting.rtms_stopped"],
    "forwardPort": 4048,
    "forwardPath": "/"
  }
}
```

### 基于命令的自动处理（无需运行额外服务）

```json
{
  "openclaw": {
    "webhookEvents": ["recording.completed"],
    "webhookCommands": {
      "recording.completed": {
        "command": "python3 scripts/download.py {{meeting_id}}",
        "description": "Download cloud recording",
        "meetingIdPath": "payload.object.id"
      }
    }
  }
}
```

- `command` — 需要执行的 shell 命令；`{{meeting_id}}` 会被替换为从 webhook 请求中提取的会议 ID。
- `meetingIdPath` — 用于从 webhook 请求中提取会议 ID 的路径（格式为点分隔符）。
- `description` — 用于通知的用户友好型描述。

ngrok 会扫描所有相关技能文件夹中的 `skill.json` 文件以检测这些配置。

### 标准输出

服务器还会将每个接收到的 webhook 请求以 JSON 格式输出到标准输出（stdout），以便其他进程进行监控：

```json
{
  "id": "uuid",
  "timestamp": "ISO-8601",
  "method": "POST",
  "path": "/webhook",
  "query": {},
  "body": {}
}
```

### 健康检查

```bash
curl http://localhost:4040/health
```

### 停止监听器

完成任务后，需要终止后台进程。

## 与 Zoom 的集成

典型集成流程：
1. 启动此 webhook 监听器并获取 ngrok 提供的公共 URL。
2. 在 Zoom Marketplace 应用的 webhook 设置中配置该 URL。
3. 当 RTMS 启动时，Zoom 会发送 `meeting.rtms_started` 信号，该信号会被自动转发给 RTMS 会议助手。
4. 当 RTMS 停止时，Zoom 会发送 `meeting.rtms_stopped` 信号，系统会自动执行清理操作。