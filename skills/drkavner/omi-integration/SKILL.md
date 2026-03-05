---
name: omi
description: 通过 API 和 Webhook 从 Omi AI 可穿戴设备（如 Omi、Limitless 等）同步录音文件。自动同步转录内容，处理录音数据，并按设备或日期进行分类整理。
homepage: https://github.com/BasedHardware/omi
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["curl","jq"]}}}
---
# Omi 集成

同步和管理来自 Omi AI 可穿戴设备（如 Omi、Limitless 系列设备等）的录音数据。

## 主要功能

- 自动从 Omi 后端同步录音数据
- 支持 Webhook 功能以实现实时转录
- 支持多设备同步（可按设备进行分类）
- 录音数据会附带元数据并存储在本地
- 提供录音摘要及后续操作建议

## 设置

1. 从 https://omi.me/developer 获取您的 Omi API 密钥，或使用自托管的后端服务。
2. 安全地存储该 API 密钥：
```bash
mkdir -p ~/.config/omi
echo "YOUR_API_KEY" > ~/.config/omi/api_key
chmod 600 ~/.config/omi/api_key
```

3. 配置后端 URL（默认为 https://api.omi.me）：
```bash
echo "https://api.omi.me" > ~/.config/omi/backend_url
# Or for self-hosted:
echo "https://your-backend.com" > ~/.config/omi/backend_url
```

## 使用方法

### 同步所有录音
```bash
omi-sync
```

### 同步最近 7 天内的录音
```bash
omi-sync --days 7
```

### 列出所有录音
```bash
omi-list
```

### 查看录音详情
```bash
omi-get <recording-id>
```

### 处理 Webhook 数据
```bash
cat webhook-payload.json | omi-webhook-handler
```

## 数据存储

录音数据存储在：
```
~/omi_recordings/
├── YYYY-MM-DD/
│   ├── <recording-id>/
│   │   ├── metadata.json
│   │   ├── transcript.txt
│   │   ├── audio.wav (if available)
│   │   └── summary.md
└── index.json
```

## Webhook 配置

请配置您的 Omi 应用程序，使其能够向您的服务器端点发送 Webhook 请求：
1. 打开 Omi 应用程序 → 设置 → 开发者选项
2. 创建新的 Webhook
3. 输入您的 Webhook URL
4. 选择需要触发 Webhook 的事件：`recording.created`（录音创建时）或 `transcript.updated`（转录更新时）

该功能包含一个名为 `omi-webhook-handler` 的处理程序，用于处理实时发生的事件。

## 多设备支持

系统会自动根据设备类型对录音数据进行分类：
```json
{
  "recording_id": "rec_123",
  "device_id": "limitless-001",
  "device_name": "Limitless Pendant",
  "device_type": "wearable",
  "context": "work",
  "transcript": "Meeting notes...",
  "created_at": "2026-02-02T15:38:00Z"
}
```

## API 端点

基础 URL：`https://api.omi.me/v1`（可配置）

- `GET /recordings` - 列出所有录音
- `GET /recordings/:id` - 查看特定录音的详细信息
- `GET /recordings/:id/transcript` - 获取录音的文字转录内容
- `GET /recordings/:id/summary` - 获取录音的 AI 摘要
- `POST /webhooks/register` - 注册新的 Webhook 端点

## 隐私保护

- 所有数据均存储在本地
- API 密钥在传输过程中会被加密
- 支持自托管的后端服务
- 不会收集任何用户数据或进行跟踪
- Webhook 数据会记录下来以便调试（可选）

## 定时同步

系统会每小时自动同步一次录音数据：
```bash
0 * * * * /path/to/omi-sync --days 1 >> ~/.local/share/omi/sync.log 2>&1
```

或者您也可以使用 Clawdbot 的定时任务功能来集成同步操作。