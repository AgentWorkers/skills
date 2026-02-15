---
name: meta-business
description: "Meta Business CLI 的核心功能是通过 Graph API 完成对 WhatsApp、Instagram、Facebook Pages 以及 Messenger 的自动化操作。该工具支持消息发送、媒体文件上传、模板使用、数据分析、Webhook 配置以及 systemd 服务管理等功能。"
version: 1.2.0
author: adolago
tags:
  - whatsapp
  - instagram
  - facebook
  - messenger
  - meta
  - cli
  - automation
triggers:
  - whatsapp
  - instagram
  - facebook
  - messenger
  - meta
  - send message
metadata:
  openclaw:
    requires:
      bins: [meta]
    install:
      - id: bun
        kind: command
        command: "bun install -g meta-business-cli"
        bins: [meta]
        label: "Install meta CLI (bun)"
      - id: compile
        kind: command
        command: "git clone https://github.com/adolago/meta-cli.git && cd meta-cli && bun install && bun build --compile --outfile ~/.bun/bin/meta src/index.ts"
        bins: [meta]
        label: "Build from source (standalone binary)"
---
# Meta Business CLI

使用 `meta` 命令，可以通过 Graph API 自动化 WhatsApp、Instagram、Facebook Pages 和 Messenger 的操作。

## 设置

```bash
# 1. Configure app credentials
meta config set app.id YOUR_APP_ID
meta config set app.secret YOUR_APP_SECRET

# 2. Authenticate (OAuth PKCE, opens browser)
meta auth login

# 3. Configure WhatsApp (from API Setup page)
meta config set whatsapp.phoneNumberId YOUR_PHONE_NUMBER_ID
meta config set whatsapp.businessAccountId YOUR_WABA_ID

# 4. Verify everything works
meta doctor
```

或者在使用任何命令时加上 `--token YOUR_TOKEN` 以跳过 OAuth 验证（例如，使用系统用户令牌）。

## 认证

```bash
meta auth login                              # OAuth PKCE flow (opens browser)
meta auth login --token YOUR_ACCESS_TOKEN    # Use existing token
meta auth login --scopes "whatsapp_business_messaging,instagram_basic,pages_show_list"
meta auth status                             # Show token validity and scopes
meta auth logout                             # Remove stored credentials
```

## 配置

```bash
meta config set app.id YOUR_APP_ID           # App ID (numeric)
meta config set app.secret YOUR_APP_SECRET   # App secret
meta config set whatsapp.phoneNumberId ID    # WhatsApp phone number ID
meta config set whatsapp.businessAccountId ID  # WhatsApp business account ID
meta config set instagram.accountId ID       # Instagram account ID
meta config set pages.pageId ID              # Facebook Page ID
meta config set webhook.forwardUrl URL       # Forward inbound messages to URL
meta config get <key>                        # Get a config value
meta config list                             # Show all config values
```

配置文件存储在 `~/.meta-cli/config.json` 中。

## WhatsApp

### 发送消息

```bash
# Text
meta wa send "+1234567890" --text "Hello" --json

# Markdown (converts to WhatsApp formatting)
meta wa send "+1234567890" --text "**bold** and _italic_" --markdown --json

# Chunked (splits long text into multiple messages)
meta wa send "+1234567890" --text "very long message..." --chunk --json

# Image
meta wa send "+1234567890" --image "https://example.com/photo.jpg" --caption "Look" --json

# Video
meta wa send "+1234567890" --video "https://example.com/video.mp4" --caption "Watch" --json

# Document
meta wa send "+1234567890" --document "https://example.com/file.pdf" --json

# Local file (auto-uploads)
meta wa send "+1234567890" --document ./report.pdf --caption "Q4 report" --json

# Audio
meta wa send "+1234567890" --audio "https://example.com/note.ogg" --json

# Voice note (renders as playable voice note, requires OGG/Opus)
meta wa send "+1234567890" --audio "./recording.ogg" --voice --json

# Template
meta wa send "+1234567890" --template "hello_world" --template-lang en_US --json

# Mark as read
meta wa read WAMID --json
```

### 媒体文件大小限制

| 类型 | 最大大小 |
|------|----------|
| 图片 | 5 MB |
| 视频 | 16 MB |
| 文档 | 100 MB |

### 模板

```bash
meta wa template list --json                 # List all templates
meta wa template get TEMPLATE_NAME --json    # Get template details
meta wa template delete TEMPLATE_NAME --json # Delete template
```

### 媒体文件上传

```bash
meta wa media upload ./photo.jpg --json      # Upload media
meta wa media url MEDIA_ID --json            # Get media URL
meta wa media download MEDIA_ID ./output.jpg # Download media
```

### 分析数据

```bash
meta wa analytics --days 30 --granularity DAY --json
```

### 手机号码管理

```bash
meta wa phone list --json                    # List numbers
meta wa phone get --json                     # Get active number details
meta wa phone select PHONE_NUMBER_ID         # Select active number
```

### 允许列表（防止恶意信息注入）

```bash
meta wa allowlist list                       # List allowed numbers
meta wa allowlist add "+1234567890"          # Add number
meta wa allowlist remove "+1234567890"       # Remove number
```

当允许列表不为空时，`meta wa send` 命令只会将消息发送到列表中的号码。

## Instagram

```bash
# Publish image
meta ig publish --image "https://example.com/photo.jpg" --caption "My post" --json

# Publish video
meta ig publish --video "https://example.com/video.mp4" --caption "Watch this" --json

# Publish Reel
meta ig publish --video "https://example.com/reel.mp4" --reel --caption "New reel" --json

# Account insights
meta ig insights --period day --days 30 --json

# Media insights
meta ig insights --media-id MEDIA_ID --json

# Comments
meta ig comments list MEDIA_ID --json        # List comments
meta ig comments reply COMMENT_ID "Thanks!" --json  # Reply
meta ig comments hide COMMENT_ID --json      # Hide
meta ig comments delete COMMENT_ID --json    # Delete
```

在 Instagram 上发布图片或视频时，需要使用公共 URL（不能使用本地文件）。

## Facebook Pages

```bash
meta fb post --message "Hello from the CLI" --json           # Create post
meta fb post --message "Check this" --link "https://example.com" --json  # Link post
meta fb list --limit 10 --json                               # List posts
meta fb insights --period day --days 30 --json               # View insights
```

## Messenger

### 注意事项

在 24 小时之外发送 Messenger 消息时，需要使用 `message tag`。

## Webhook

```bash
# Start listener
meta webhook listen --port 3000 --verify-token TOKEN --app-secret SECRET

# Test verification locally
meta webhook verify --verify-token TOKEN --json

# Subscribe to events
meta webhook subscribe \
  --object whatsapp_business_account \
  --fields messages \
  --callback-url "https://example.com/webhook" --json
```

在配置文件中设置 `webhook.forwardUrl`，以便将收到的消息转发到外部服务。
Webhook 会自动发送已读通知并确认用户的反应。

## Webhook 服务（systemd）

```bash
meta service install                         # Install systemd user service
meta service start                           # Start the webhook service
meta service stop                            # Stop the service
meta service restart                         # Restart the service
meta service status                          # Show service status
meta service logs                            # Show service logs
meta service uninstall                       # Remove systemd service
```

## Shell 完成提示（Shell Completion）

```bash
# Bash
meta completion >> ~/.bashrc

# Zsh (add to .zshrc)
meta completion >> ~/.zshrc
```

## 日志诊断

```bash
meta doctor --json
```

检查配置文件、凭证、令牌的有效性、Graph API 的连接状态、权限以及特定平台的资源访问权限。首次使用前请运行此命令。

## 全局参数

| 参数 | 说明 |
|------|-------------|
| `--json` | 为脚本编写或代理程序提供结构化输出 |
| `--verbose` | 将调试日志输出到标准错误流（stderr） |
| `--token TOKEN` | 覆盖已保存的凭证 |
| `--api-version v22.0` | 指定使用的 Graph API 版本 |

## 注意事项：

- 在自动化操作时，始终使用 `--json` 以获得结构化输出。
- 如果所需参数以参数标志的形式提供，所有命令将以非交互式方式运行。
- 语音笔记需要 OGG/Opus 格式才能在 WhatsApp 中正确显示。
- 超过大小限制的文件会被拒绝，并会显示相应的错误信息。
- 对于较大的文件，请将其托管在某个 URL 上，并直接传递该 URL。