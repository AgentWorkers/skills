---
name: nest-devices
description: 通过设备访问 API（Device Access API）来控制 Nest 智能家居设备（如恒温器、摄像头、门铃）。当需要查看或调节室内温度、查看摄像头画面、确认门口有人、监控房间状况或设置温度调节计划时，可以使用该 API。
metadata:
  clawdbot:
    emoji: "🏠"
---

# 访问Nest设备

通过Google的智能设备管理API来控制Nest设备。

## 设置

### 1. Google Cloud与设备访问

1. 在[console.cloud.google.com](https://console.cloud.google.com)创建一个Google Cloud项目。
2. 支付5美元的费用，并在[console.nest.google.com/device-access](https://console.nest.google.com/device-access)创建一个设备访问项目。
3. 创建OAuth 2.0凭据（Web应用程序类型）。
4. 将`https://www.google.com`添加为授权重定向URI。
5. 将您的Nest账户与设备访问项目关联起来。

### 2. 获取刷新令牌

运行OAuth流程以获取刷新令牌：

```bash
# 1. Open this URL in browser (replace CLIENT_ID and PROJECT_ID):
https://nestservices.google.com/partnerconnections/PROJECT_ID/auth?redirect_uri=https://www.google.com&access_type=offline&prompt=consent&client_id=CLIENT_ID&response_type=code&scope=https://www.googleapis.com/auth/sdm.service

# 2. Authorize and copy the 'code' parameter from the redirect URL

# 3. Exchange code for tokens:
curl -X POST https://oauth2.googleapis.com/token \
  -d "client_id=CLIENT_ID" \
  -d "client_secret=CLIENT_SECRET" \
  -d "code=AUTH_CODE" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=https://www.google.com"
```

### 3. 存储凭据

将凭据存储在1Password或环境变量中：

**1Password**（推荐）：
创建一个条目，包含以下字段：`project_id`、`client_id`、`client_secret`、`refresh_token`。

**环境变量：**
```bash
export NEST_PROJECT_ID="your-project-id"
export NEST_CLIENT_ID="your-client-id"
export NEST_CLIENT_SECRET="your-client-secret"
export NEST_REFRESH_TOKEN="your-refresh-token"
```

## 使用方法

### 列出设备
```bash
python3 scripts/nest.py list
```

### 温控器
```bash
# Get status
python3 scripts/nest.py get <device_id>

# Set temperature (Celsius)
python3 scripts/nest.py set-temp <device_id> 21 --unit c --type heat

# Set temperature (Fahrenheit)
python3 scripts/nest.py set-temp <device_id> 70 --unit f --type heat

# Change mode (HEAT, COOL, HEATCOOL, OFF)
python3 scripts/nest.py set-mode <device_id> HEAT

# Eco mode
python3 scripts/nest.py set-eco <device_id> MANUAL_ECO
```

### 摄像头
```bash
# Generate live stream URL (RTSP, valid ~5 min)
python3 scripts/nest.py stream <device_id>
```

## Python API
```python
from nest import NestClient

client = NestClient()

# List devices
devices = client.list_devices()

# Thermostat control
client.set_heat_temperature(device_id, 21.0)  # Celsius
client.set_thermostat_mode(device_id, 'HEAT')
client.set_eco_mode(device_id, 'MANUAL_ECO')

# Camera stream
result = client.generate_stream(device_id)
rtsp_url = result['results']['streamUrls']['rtspUrl']
```

## 配置

脚本按以下顺序检查凭据：

1. **1Password**：设置`NEST_OP_VAULT`和`NEST_OP_ITEM`（或使用默认值：vault "Alfred"，item "Nest Device Access API"）。
2. **环境变量**：`NEST_PROJECT_ID`、`NEST_CLIENT_ID`、`NEST_CLIENT_SECRET`、`NEST_REFRESH_TOKEN`。

## 温度参考

| 设置 | 摄氏度 | 华氏度 |
|---------|---------|------------|
| 节能模式（离开） | 15-17°C | 59-63°F |
| 舒适模式 | 19-21°C | 66-70°F |
| 温暖模式 | 22-23°C | 72-73°F |
| 夜间模式 | 17-18°C | 63-65°F |

---

## 实时事件（门铃、运动等）

当有人按门铃或检测到运动时，您需要设置Google Cloud Pub/Sub并配置Webhook以接收即时警报。

### 先决条件

- 安装并登录Google Cloud CLI（`gcloud`）。
- 拥有Cloudflare账户（免费 tier即可）用于建立隧道。
- 在配置中启用Clawdbot的钩子功能。

### 1. 启用Clawdbot钩子

在`clawdbot.json`中添加以下配置：
```json
{
  "hooks": {
    "enabled": true,
    "token": "your-secret-token-here"
  }
}
```

生成令牌：`openssl rand -hex 24`

### 2. 创建Pub/Sub主题

```bash
gcloud config set project YOUR_GCP_PROJECT_ID

# Create topic
gcloud pubsub topics create nest-events

# Grant SDM permission to publish (both the service account and publisher group)
gcloud pubsub topics add-iam-policy-binding nest-events \
  --member="serviceAccount:sdm-prod@sdm-prod.iam.gserviceaccount.com" \
  --role="roles/pubsub.publisher"

gcloud pubsub topics add-iam-policy-binding nest-events \
  --member="group:sdm-publisher@googlegroups.com" \
  --role="roles/pubsub.publisher"
```

### 3. 将主题与设备访问关联

访问[console.nest.google.com/device-access](https://console.nest.google.com/device-access) → 选择您的项目 → 编辑 → 将Pub/Sub主题设置为：
```
projects/YOUR_GCP_PROJECT_ID/topics/nest-events
```

### 4. 设置Cloudflare隧道

```bash
# Install cloudflared
curl -L -o ~/.local/bin/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x ~/.local/bin/cloudflared

# Authenticate (opens browser)
~/.local/bin/cloudflared tunnel login

# Create named tunnel
~/.local/bin/cloudflared tunnel create nest-webhook

# Note the Tunnel ID (UUID) from output
```

创建`~/.cloudflared/config.yml`文件：
```yaml
tunnel: nest-webhook
credentials-file: /home/YOUR_USER/.cloudflared/TUNNEL_ID.json

ingress:
  - hostname: nest.yourdomain.com
    service: http://localhost:8420
  - service: http_status:404
```

创建DNS路由：
```bash
~/.local/bin/cloudflared tunnel route dns nest-webhook nest.yourdomain.com
```

### 5. 创建Systemd服务

**Webhook服务器**（`/etc/systemd/system/nest-webhook.service`）：
```ini
[Unit]
Description=Nest Pub/Sub Webhook Server
After=network.target

[Service]
Type=simple
User=YOUR_USER
Environment=CLAWDBOT_GATEWAY_URL=http://localhost:18789
Environment=CLAWDBOT_HOOKS_TOKEN=your-hooks-token-here
ExecStart=/usr/bin/python3 /path/to/skills/nest-devices/scripts/nest-webhook.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Cloudflare隧道**（`/etc/systemd/system/cloudflared-nest.service`）：
```ini
[Unit]
Description=Cloudflare Tunnel for Nest Webhook
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=YOUR_USER
ExecStart=/home/YOUR_USER/.local/bin/cloudflared tunnel run nest-webhook
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启用并启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now nest-webhook cloudflared-nest
```

### 6. 创建Pub/Sub推送订阅

```bash
gcloud pubsub subscriptions create nest-events-sub \
  --topic=nest-events \
  --push-endpoint="https://nest.yourdomain.com/nest/events" \
  --ack-deadline=30
```

### 7. 测试

```bash
# Test webhook endpoint
curl https://nest.yourdomain.com/health

# Simulate doorbell event
curl -X POST http://localhost:8420/nest/events \
  -H "Content-Type: application/json" \
  -d '{"message":{"data":"eyJyZXNvdXJjZVVwZGF0ZSI6eyJuYW1lIjoiZW50ZXJwcmlzZXMvdGVzdC9kZXZpY2VzL0RPT1JCRUxMLTAxIiwiZXZlbnRzIjp7InNkbS5kZXZpY2VzLmV2ZW50cy5Eb29yYmVsbENoaW1lLkNoaW1lIjp7ImV2ZW50SWQiOiJ0ZXN0In19fX0="}}'
```

### 支持的事件

| 事件 | 行为 |
|-------|-----------|
| `DoorbellChime.Chime` | 🔔 **警报** — 向Telegram发送照片 |
| `CameraPerson.Person` | 🚶 **警报** — 向Telegram发送照片 |
| `CameraMotion.Motion` | 📹 仅记录日志（无警报） |
| `CameraSound.Sound` | 🔊 仅记录日志（无警报） |
| `CameraClipPreview.ClipPreview` | 🎬 仅记录日志（无警报） |

> **过期过滤**：超过5分钟的事件会被记录在日志中，但不会触发警报。这样可以防止因Pub/Sub消息延迟发送而导致大量通知。

### 图像捕获

当门铃或人员事件触发警报时：

1. **主要方式**：使用SDM的`GenerateImage` API生成快速、针对特定事件的快照。
2. **备用方式**：通过`ffmpeg`捕获RTSP实时流帧（需要安装`ffmpeg`）。

### 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `CLAWDBOT_GATEWAY_URL` | 否 | 网关URL（默认：`http://localhost:18789`） |
| `CLAWDBOTHOOKS_TOKEN` | 是 | 用于通知的网关钩子令牌 |
| `OP_SVC_ACCT_TOKEN` | 是 | 用于Nest API凭据的1Password服务账户令牌 |
| `TELEGRAM_BOT_TOKEN` | 是 | 用于发送警报的Telegram机器人令牌 |
| `TELEGRAM_chat_ID` | 是 | 用于接收警报的Telegram聊天ID |
| `PORT` | 否 | Webhook服务器端口（默认：`8420`） |

### 重要设置说明

- **请确保设备访问控制台中的Pub/Sub主题路径与您的GCP项目完全匹配**：`projects/YOUR_GCP PROJECT_ID/topics/nest-events`。
- **使用推送订阅**，而不是拉取方式——Webhook期望接收HTTP POST请求。
- **设置完成后进行端到端测试**：按门铃确认照片是否成功发送到Telegram。
- **不要仅依赖模拟的POST请求**。

---

## 限制

- 摄像头事件产生的图片会在大约5分钟后过期（RTSP备用方式会捕获当前帧）。
- 实时事件需要设置Pub/Sub（详见上文）。
- 使用非Cloudflare账户的临时隧道可能无法保证持续运行。
- 一些较旧的Nest设备可能不支持所有功能。
- 为了减少通知负担，运动和声音事件不会触发警报。