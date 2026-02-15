---
name: zoom-unofficial-community-skill
description: Zoom API集成支持会议、日历、聊天和用户管理功能。当用户需要安排会议、查看Zoom日历、列出会议录像、发送Zoom聊天消息、管理联系人或使用Zoom Workplace的任何功能时，均可使用该API。该API支持服务器到服务器（Server-to-Server）的OAuth认证机制，同时也兼容OAuth应用程序（OAuth apps）。
---

# Zoom

使用 `scripts/zoom.py` 脚本与 Zoom 的 REST API 进行交互。

## 先决条件

```bash
pip3 install requests PyJWT --break-system-packages
```

## 认证

请在技能的 `.env` 文件中设置以下参数（复制自 `.env.example`）：

- `ZOOM_ACCOUNT_ID` — Zoom 帐户 ID（来自 Zoom Marketplace 应用）
- `ZOOM_CLIENT_ID` — OAuth 客户端 ID
- `ZOOM_CLIENT_SECRET` — OAuth 客户端密钥
- `ZOOM_USER_EMAIL` — 用于身份验证的 Zoom 用户邮箱（对于 S2S 应用是必需的；如果未设置，默认为 `me`）
- `ZOOM_RTMS_CLIENT_ID` — RTMS Marketplace 应用的客户端 ID（用于 `rtms-start`/`rtms-stop` 操作；此应用与 S2S OAuth 应用是分开的）

请在 https://marketplace.zoom.us/ 上创建一个 **服务器到服务器的 OAuth** 应用以获得完整的 API 访问权限。
有关详细设置指南，请参阅 [references/AUTH.md](references/AUTH.md)。

## 命令

### 会议
```bash
# List upcoming meetings
python3 scripts/zoom.py meetings list

# List live/in-progress meetings (requires Business+ plan with Dashboard)
python3 scripts/zoom.py meetings live

# Start RTMS for a live meeting (requires ZOOM_RTMS_CLIENT_ID)
python3 scripts/zoom.py meetings rtms-start <meeting_id>

# Stop RTMS for a live meeting
python3 scripts/zoom.py meetings rtms-stop <meeting_id>

# Get meeting details
python3 scripts/zoom.py meetings get <meeting_id>

# Schedule a new meeting
python3 scripts/zoom.py meetings create --topic "Standup" --start "2026-01-28T10:00:00" --duration 30

# Schedule with options
python3 scripts/zoom.py meetings create --topic "Review" --start "2026-01-28T14:00:00" --duration 60 --agenda "Sprint review" --password "abc123"

# Delete a meeting
python3 scripts/zoom.py meetings delete <meeting_id>

# Update a meeting
python3 scripts/zoom.py meetings update <meeting_id> --topic "New Title" --start "2026-01-29T10:00:00"
```

### 日历（即将举行的会议）
```bash
# Today's meetings
python3 scripts/zoom.py meetings list --from today --to today

# This week's meetings
python3 scripts/zoom.py meetings list --from today --days 7
```

### 录制
```bash
# List cloud recordings
python3 scripts/zoom.py recordings list

# List recordings for date range
python3 scripts/zoom.py recordings list --from "2026-01-01" --to "2026-01-31"

# Get recording details
python3 scripts/zoom.py recordings get <meeting_id>

# Download recording files (video/audio)
python3 scripts/zoom.py recordings download <meeting_id>
python3 scripts/zoom.py recordings download <meeting_id> --output ~/Downloads

# Download transcript files only
python3 scripts/zoom.py recordings download-transcript <meeting_id>
python3 scripts/zoom.py recordings download-transcript <meeting_id> --output ~/Downloads

# Download AI Companion summary as markdown
python3 scripts/zoom.py recordings download-summary <meeting_uuid>
python3 scripts/zoom.py recordings download-summary <meeting_uuid> --output ~/Downloads

# Delete a recording
python3 scripts/zoom.py recordings delete <meeting_id>
```

### AI 会议总结（AI 功能）
```bash
# List meeting summaries
python3 scripts/zoom.py summary list
python3 scripts/zoom.py summary list --from "2026-01-01" --to "2026-01-31"

# Get AI summary for a specific meeting
python3 scripts/zoom.py summary get <meeting_id>
```

### 用户
```bash
# Get my profile
python3 scripts/zoom.py users me

# List users (admin)
python3 scripts/zoom.py users list
```

### 团队聊天
```bash
# List chat channels
python3 scripts/zoom.py chat channels

# List messages in a channel
python3 scripts/zoom.py chat messages <channel_id>

# Send a message to a channel
python3 scripts/zoom.py chat send <channel_id> "Hello team!"

# Send a direct message
python3 scripts/zoom.py chat dm <email> "Hey, are you free?"

# List contacts
python3 scripts/zoom.py chat contacts
```

### 电话（Zoom Phone）
```bash
# List call logs
python3 scripts/zoom.py phone calls --from "2026-01-01" --to "2026-01-31"
```

## 所需的权限范围

对于服务器到服务器的 OAuth 认证，需要在您的 Zoom Marketplace 应用中启用以下权限范围：
请仅添加所需的权限范围——每个命令组都需要特定的权限范围：

| 命令组 | 所需权限范围 |
|---|---|
| `users me` / `users list` | `user:read:admin` |
| `meetings list/get/create/update/delete` | `meeting:read:admin`, `meeting:write:admin` |
| `recordings list/get/delete` | `recording:read:admin`, `recording:write:admin` |
| `chat channels/messages/send/dm` | `chat_channel:read:admin`, `chat_message:read:admin`, `chat_message:write:admin` |
| `chat contacts` | `contact:read:admin` |
| `summary list/get` | `meeting_summary:read:admin` |
| `phone calls` | `phone:read:admin`（需要您的账户启用了 Zoom Phone 功能）

**如果您收到权限范围错误**，请访问 https://marketplace.zoom.us/ → 您的应用 → 权限范围（Scopes），然后添加错误消息中列出的缺失权限范围。

## 速率限制

Zoom API 有速率限制（因端点而异，通常为每秒 30-100 次请求）。该脚本会自动重试处理 429 错误（表示请求次数超过限制）。