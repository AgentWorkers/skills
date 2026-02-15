---
name: telegram-create-bot
description: 通过 Telegram Bot API 构建和管理 Telegram 机器人。可以创建机器人、发送消息、处理 Webhook 事件、管理群组和频道。
homepage: https://core.telegram.org/bots/api
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["jq","curl"],"env":["TELEGRAM_BOT_TOKEN"]}}}
---

# 创建 Telegram 机器人

直接使用 OpenClaw 构建和管理 Telegram 机器人。

## 设置

1. 打开 Telegram，向 [@BotFather](https://t.me/BotFather) 发送消息。
2. 输入 `/newbot` 并按照提示操作来创建你的机器人。
3. 复制机器人的令牌（格式类似 `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）。
4. 设置环境变量：
   ```bash
   export TELEGRAM_BOT_TOKEN="your-bot-token"
   ```

## API 基本 URL

所有请求都发送到：
```
https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/METHOD_NAME
```

## 使用方法

### 机器人信息

#### 获取机器人信息
```bash
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe" | jq
```

#### 获取机器人命令
```bash
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMyCommands" | jq
```

#### 设置机器人命令
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setMyCommands" \
  -H "Content-Type: application/json" \
  -d '{
    "commands": [
      {"command": "start", "description": "Start the bot"},
      {"command": "help", "description": "Show help message"},
      {"command": "settings", "description": "Bot settings"}
    ]
  }' | jq
```

### 发送消息

#### 发送文本消息
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "CHAT_ID",
    "text": "Hello from Clawdbot!",
    "parse_mode": "HTML"
  }' | jq
```

#### 发送带内联键盘的消息
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "CHAT_ID",
    "text": "Choose an option:",
    "reply_markup": {
      "inline_keyboard": [
        [{"text": "Option 1", "callback_data": "opt1"}, {"text": "Option 2", "callback_data": "opt2"}],
        [{"text": "Visit Website", "url": "https://example.com"}]
      ]
    }
  }' | jq
```

#### 发送带回复键盘的消息
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "CHAT_ID",
    "text": "Choose from keyboard:",
    "reply_markup": {
      "keyboard": [
        [{"text": "Button 1"}, {"text": "Button 2"}],
        [{"text": "Send Location", "request_location": true}]
      ],
      "resize_keyboard": true,
      "one_time_keyboard": true
    }
  }' | jq
```

#### 发送照片
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendPhoto" \
  -F "chat_id=CHAT_ID" \
  -F "photo=@/path/to/image.jpg" \
  -F "caption=Photo caption here" | jq
```

#### 通过 URL 发送照片
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendPhoto" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "CHAT_ID",
    "photo": "https://example.com/image.jpg",
    "caption": "Image from URL"
  }' | jq
```

#### 发送文档
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendDocument" \
  -F "chat_id=CHAT_ID" \
  -F "document=@/path/to/file.pdf" \
  -F "caption=Here is your document" | jq
```

#### 发送位置信息
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendLocation" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "CHAT_ID",
    "latitude": 40.7128,
    "longitude": -74.0060
  }' | jq
```

### 获取更新

#### 获取更新（轮询）
```bash
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates" | jq
```

#### 带偏移量获取更新（标记为已读）
```bash
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates?offset=UPDATE_ID" | jq
```

#### 带超时设置获取更新（长时间轮询）
```bash
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates?timeout=30" | jq
```

### Webhook

#### 设置 Webhook
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook",
    "allowed_updates": ["message", "callback_query"]
  }' | jq
```

#### 获取 Webhook 信息
```bash
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo" | jq
```

#### 删除 Webhook
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/deleteWebhook" | jq
```

### 聊天管理

#### 获取聊天信息
```bash
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getChat?chat_id=CHAT_ID" | jq
```

#### 获取聊天成员数量
```bash
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getChatMemberCount?chat_id=CHAT_ID" | jq
```

#### 获取聊天管理员
```bash
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getChatAdministrators?chat_id=CHAT_ID" | jq
```

#### 将用户禁言
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/banChatMember" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "CHAT_ID",
    "user_id": USER_ID
  }' | jq
```

#### 解禁用户
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/unbanChatMember" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "CHAT_ID",
    "user_id": USER_ID,
    "only_if_banned": true
  }' | jq
```

### 消息管理

#### 编辑消息内容
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/editMessageText" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "CHAT_ID",
    "message_id": MESSAGE_ID,
    "text": "Updated message text"
  }' | jq
```

#### 删除消息
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/deleteMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "CHAT_ID",
    "message_id": MESSAGE_ID
  }' | jq
```

#### 固定消息
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/pinChatMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "CHAT_ID",
    "message_id": MESSAGE_ID
  }' | jq
```

#### 转发消息
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/forwardMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "TARGET_CHAT_ID",
    "from_chat_id": "SOURCE_CHAT_ID",
    "message_id": MESSAGE_ID
  }' | jq
```

### 回调查询

#### 回答回调查询
```bash
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/answerCallbackQuery" \
  -H "Content-Type: application/json" \
  -d '{
    "callback_query_id": "CALLBACK_QUERY_ID",
    "text": "Button clicked!",
    "show_alert": false
  }' | jq
```

## 注意事项

- **聊天 ID**：可以是正数（表示用户）或负数（表示群组/频道）。可以通过更新信息获取，或使用 `@userinfobot` 来获取。
- **解析模式**：`HTML`、`Markdown`、`MarkdownV2`。
- **速率限制**：不同聊天每秒最多发送 30 条消息；同一聊天每秒最多发送 1 条消息。
- **文件限制**：照片最大 10MB，文档最大 50MB。
- **机器人权限**：机器人不能主动向用户发送消息——必须由用户先使用 `/start` 命令启动机器人。

## HTML 格式化

```html
<b>bold</b>
<i>italic</i>
<u>underline</u>
<s>strikethrough</s>
<code>inline code</code>
<pre>code block</pre>
<a href="https://example.com">link</a>
<tg-spoiler>spoiler</tg-spoiler>
```

## 示例

### 简单的回显机器人（bash 脚本）
```bash
#!/bin/bash
OFFSET=0
while true; do
  UPDATES=$(curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates?offset=$OFFSET&timeout=30")
  
  for UPDATE in $(echo "$UPDATES" | jq -c '.result[]'); do
    UPDATE_ID=$(echo "$UPDATE" | jq '.update_id')
    CHAT_ID=$(echo "$UPDATE" | jq '.message.chat.id')
    TEXT=$(echo "$UPDATE" | jq -r '.message.text')
    
    if [ "$TEXT" != "null" ]; then
      curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\": $CHAT_ID, \"text\": \"You said: $TEXT\"}"
    fi
    
    OFFSET=$((UPDATE_ID + 1))
  done
done
```

### 获取你的聊天 ID
```bash
# 1. Send a message to your bot
# 2. Run this to see your chat ID:
curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates" | jq '.result[-1].message.chat.id'
```

### 向频道发送消息
```bash
# Use @channelname or channel ID (starts with -100)
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "@your_channel_name",
    "text": "Channel announcement!"
  }' | jq
```

## 有用资源

- [Bot API 文档](https://core.telegram.org/bots/api)
- [BotFather 命令](https://core.telegram.org/bots#botfather)
- [Bot API 更新日志](https://coreTelegram.org/bots/api-changelog)