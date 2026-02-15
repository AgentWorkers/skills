# WhatsApp 分析器

该工具可自动检测来自 WhatsApp 的约会信息及紧急消息，并通过 Telegram 发出警报；同时可选择将相关信息同步到 Google 日历中。

## 工作原理

```
WhatsApp message arrives
        ↓
WAHA (Docker) captures it
        ↓
Webhook → Message Store → messages.jsonl
        ↓
OpenClaw cron (every 60s) → Agent analyzes
        ↓
RDV detected? → Telegram: "Add to calendar? OUI/NON"
        ↓
User confirms → Google Calendar event created
```

## 快速入门

```bash
./setup.sh
# Enter your Telegram Chat ID when prompted
# Scan the QR code with WhatsApp
# Done! 🎉
```

## 所需软件及环境

- Docker
- Node.js
- 配置了 Telegram 的 OpenClaw
- 用于同步到 Google 日历的 `gog` CLI（可选）

## 可检测的信息类型

| 信息类型 | 关键词 | 处理方式 |
|------|----------|--------|
| **约会** | meeting, rdv, rendez-vous, reunion, appointment + 时间 | 通过 Telegram 发出警报，并可选择同步到日历 |
| **紧急消息** | urgent, important, asap, help, sos | 通过 Telegram 发出警报 |

## 生成的文件

| 文件名 | 存放位置 | 用途 |
|------|----------|---------|
| `message-store.js` | `~/.openclaw/workspace/.whatsapp-messages/` | 用于接收 WhatsApp 消息的 Webhook 处理程序 |
| `messages.jsonl` | 同上 | 存储消息内容 |
| `.last-ts` | 同上 | 记录消息最后处理的时间戳 |
| `.env` | 同上 | 存储 WhatsApp 和 Telegram 的登录凭据 |

## 可使用的命令

```bash
# Check WAHA status
source ~/.openclaw/workspace/.whatsapp-messages/.env
curl -s -H "X-Api-Key: $WAHA_API_KEY" http://localhost:3000/api/sessions/default | jq '.status'

# View recent messages
tail -5 ~/.openclaw/workspace/.whatsapp-messages/messages.jsonl | jq '.text'

# Restart message store
launchctl unload ~/Library/LaunchAgents/ai.openclaw.whatsapp-store.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.whatsapp-store.plist

# Get new QR code (if disconnected)
curl -s -H "X-Api-Key: $WAHA_API_KEY" http://localhost:3000/api/default/auth/qr --output /tmp/qr.png
open /tmp/qr.png
```

## 常见问题排查

### WhatsApp 连接失败
```bash
# Get new QR
source ~/.openclaw/workspace/.whatsapp-messages/.env
curl -s -H "X-Api-Key: $WAHA_API_KEY" http://localhost:3000/api/default/auth/qr --output /tmp/qr.png
open /tmp/qr.png
```

### 消息未传送到系统
1. 检查 WhatsApp-Waha 的日志：`docker logs whatsapp-waha | tail -10`
2. 查看消息存储文件：`cat /tmp/whatsapp-store.log`
3. 查看 WhatsApp-Waha 仪表板中的 Webhook 配置：`http://localhost:3000`

### 日历同步失败
确保 `gog` 已正确配置：
```bash
gog auth login
gog calendar events primary --from today --to tomorrow
```

## 隐私政策

- 所有数据均存储在本地
- 不使用任何外部服务器（仅依赖 WhatsApp、Telegram 和 Google 的 API）
- 登录凭据存储在 `.env` 文件中（未上传至 Git）