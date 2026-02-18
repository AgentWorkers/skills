---
name: telegram-history
description: >
  **通过 MTProto 用户 API（Telethon）获取 Telegram 聊天记录**  
  当需要读取机器人 API 无法访问的任何 Telegram 聊天、群组或论坛主题中的旧消息时，可以使用此方法。支持按聊天 ID、论坛主题/帖子、消息数量进行查询，并支持分页显示结果，输出格式为 JSON。使用前需用户使用手机号码进行一次性登录，并启用双重身份验证（2FA）。
---
# Telegram 历史记录

使用 MTProto（Telethon）从任意 Telegram 聊天中获取消息历史记录。Bot API 无法读取聊天历史记录，因此该功能会使用用户 API 来实现这一操作。

## 设置

### 1. 安装 Telethon
```bash
pip3 install telethon
```

### 2. 获取 API 凭据
访问 https://my.telegram.org/apps 并创建一个应用。保存凭据：
```bash
cat > skills/telegram-history/api_credentials.json << 'EOF'
{"api_id": YOUR_API_ID, "api_hash": "YOUR_API_HASH"}
EOF
```

### 3. 登录（一次性登录）
```bash
python3 scripts/login.py send
# Telegram sends a code to your phone
# Write code to a file (don't send via Telegram — it blocks shared codes):
echo YOUR_CODE > /tmp/tgcode.txt
# Then verify:
python3 scripts/login.py verify <CODE> <HASH>
# If 2FA enabled:
python3 scripts/login.py verify <CODE> <HASH> <2FA_PASSWORD>
```

登录信息会保存在 `session/` 文件夹中，无需重新登录。

## 使用方法
```bash
# Fetch last 50 messages from a chat
python3 scripts/tg_history.py history <chat_id> --limit 50

# Fetch from a forum topic
python3 scripts/tg_history.py history <chat_id> --topic <topic_id> --limit 30

# JSON output
python3 scripts/tg_history.py history <chat_id> --json

# Paginate (messages before a specific ID)
python3 scripts/tg_history.py history <chat_id> --offset-id <msg_id> --limit 50
```

## 注意事项

- 群组聊天 ID 以 `-100` 为前缀（例如：`-1001234567890`）
- 论坛主题 ID 即为帖子/主题的消息 ID
- 发件人名称会自动显示
- **请勿通过 Telegram 发送登录验证码**—— Telegram 会检测到这种行为并阻止登录。请使用文件或其他渠道来传递验证码。