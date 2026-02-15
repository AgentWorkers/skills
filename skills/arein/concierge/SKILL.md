---
name: concierge
description: 查找住宿的联系方式，并通过人工智能辅助进行预订电话。
version: 1.3.1
triggers:
  - find contact
  - hotel contact
  - accommodation contact
  - property contact
  - airbnb contact
  - booking contact
  - vrbo contact
  - expedia contact
  - direct booking
  - property email
  - property phone
  - call hotel
  - call property
  - direct booking call
---

# 旅行礼宾服务

该服务可查询住宿房源的联系方式（电话、电子邮件、WhatsApp、Instagram等），并自动发起AI预订电话。

## 功能

### 1) 从房源URL中提取联系方式

```bash
concierge find-contact "<url>"
```

### 2) 自动发起电话呼叫

```bash
concierge call "+1-555-123-4567" \
  --goal "Book a room for March 12-14" \
  --name "Derek Rein" \
  --email "alexanderderekrein@gmail.com" \
  --customer-phone "+1-555-000-1111" \
  --context "Prefer direct booking if rate beats Booking.com"
```

`call` 命令现在默认会自动管理相关基础设施：如果本地服务器不可用，它会自动启动 `ngrok` 并连接呼叫服务器；通话结束后，这两个服务也会同时停止。

## 支持的房源预订平台

- **Airbnb**: `airbnb.com/rooms/...`
- **Booking.com**: `booking.com/hotel/...`
- **VRBO**: `vrbo.com/...`
- **Expedia**: `expedia.com/...Hotel...`

## 示例

### 查询Airbnb房源的联系方式
运行命令：
```bash
concierge find-contact "https://www.airbnb.com/rooms/12345"
```

### 手动控制电话呼叫的流程
运行命令：
```bash
concierge call "+1-555-123-4567" \
  --goal "Negotiate a direct booking rate" \
  --name "Derek Rein" \
  --email "alexanderderekrein@gmail.com" \
  --customer-phone "+1-555-000-1111" \
  --interactive
```

### 用于脚本编写的JSON输出（联系方式查询结果）
```bash
concierge find-contact --json "https://..."
```

### 详细输出（包含调试信息）
```bash
concierge --verbose find-contact "https://..."
```

## 配置

该命令行工具（CLI）的配置文件位于：

`~/.config/concierge/config.json5`

### 用于联系方式查询的可选配置项
```bash
concierge config set googlePlacesApiKey "your-key"
```

### 发起AI电话呼叫所必需的配置项
```bash
concierge config set twilioAccountSid "<sid>"
concierge config set twilioAuthToken "<token>"
concierge config set twilioPhoneNumber "+14155551234"
concierge config set deepgramApiKey "<key>"
concierge config set elevenLabsApiKey "<key>"
concierge config set elevenLabsVoiceId "EXAVITQu4vr4xnSDxMaL"
concierge config set anthropicApiKey "<key>"

# Optional for auto ngrok auth
concierge config set ngrokAuthToken "<token>"
```

### 配置值检查
```bash
concierge config show
```

## 注意事项

- 联系方式提取基于公开可获取的信息。
- `call` 命令在拨打电话前会验证所需的本地依赖项（包括支持MP3解码的 `ffmpeg` 以及自动启用基础设施时所需的 `ngrok`）。
- 在拨打电话前，`call` 命令会检查Twilio、Deepgram和ElevenLabs的配额使用情况。
- 当使用自动基础设施时，服务器和 `ngrok` 的日志会保存在 `~/.config/concierge/call-runs/<run-id>/` 目录下。