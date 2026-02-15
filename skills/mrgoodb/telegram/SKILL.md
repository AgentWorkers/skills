---
name: telegram
description: 通过 Telegram Bot API 发送消息、照片和文件。当您需要向 Telegram 聊天、频道或群组发送通知、提醒或内容时，可以使用该功能。支持文本格式化、媒体文件以及内联键盘（inline keyboards）的使用。
---

# Telegram机器人API

使用机器人令牌向Telegram发送消息。

## 设置

1. 通过Telegram上的@BotFather创建机器人。
2. 复制机器人令牌。
3. 存储令牌：
```bash
mkdir -p ~/.config/telegram
echo "YOUR_BOT_TOKEN" > ~/.config/telegram/bot_token
```
4. 获取聊天ID：向您的机器人发送`/start`命令，然后访问：
   `https://api.telegram.org/bot<TOKEN>/getUpdates`

## 发送文本消息

```bash
TOKEN=$(cat ~/.config/telegram/bot_token)
CHAT_ID="123456789"

curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"Hello from Clawdbot!\"}"
```

## 格式化（MarkdownV2）

```bash
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'$CHAT_ID'",
    "text": "*Bold* _italic_ `code` [link](https://example.com)",
    "parse_mode": "MarkdownV2"
  }'
```

在MarkdownV2中转义这些字符：`_*[]()~>#+-=|{}.!`

## 发送图片

```bash
# From URL
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendPhoto" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'$CHAT_ID'",
    "photo": "https://example.com/image.jpg",
    "caption": "Image caption"
  }'

# From file
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendPhoto" \
  -F "chat_id=${CHAT_ID}" \
  -F "photo=@/path/to/image.jpg" \
  -F "caption=Image caption"
```

## 发送文档

```bash
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendDocument" \
  -F "chat_id=${CHAT_ID}" \
  -F "document=@/path/to/file.pdf" \
  -F "caption=File description"
```

## 内联键盘（按钮）

```bash
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'$CHAT_ID'",
    "text": "Choose an option:",
    "reply_markup": {
      "inline_keyboard": [[
        {"text": "Option A", "callback_data": "option_a"},
        {"text": "Option B", "callback_data": "option_b"}
      ]]
    }
  }'
```

## 静默消息

```bash
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'$CHAT_ID'",
    "text": "Silent notification",
    "disable_notification": true
  }'
```

## 获取更新（轮询）

```bash
curl -s "https://api.telegram.org/bot${TOKEN}/getUpdates" | jq
```

## 错误处理

检查响应中的`ok`字段：
```json
{"ok": true, "result": {...}}
{"ok": false, "error_code": 400, "description": "Bad Request: chat not found"}
```

## 常见聊天ID

- 用户聊天：正数（例如：`123456789`）
- 群组：负数（例如：`-123456789`）
- 频道：`@channel_username` 或负数ID

## 速率限制

- 同一聊天每秒最多30条消息
- 同一群组每分钟最多20条消息
- 批量发送：所有聊天每秒最多30条消息