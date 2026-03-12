---
name: telegram-autopilot
description: 管理一个 Telegram 用户机器人（userbot），使其能够使用人工智能（AI）来回复用户的私信。该工具适用于用户希望为个人 Telegram 账户设置自动回复规则、管理允许接收私信的联系人、配置 AI 回复样式，或以用户自己的身份发送消息/媒体文件的情况。触发关键词包括：“telegram autopilot”、“auto reply telegram”、“manage my telegram”、“respond for me”、“telegram userbot”、“paid media telegram”。
---
# Telegram 自动驾驶功能

这是一个基于人工智能的自动化工具，专为个人 Telegram 账户设计。当用户无法即时响应私信时，该工具会代为回复。

## 先决条件

- Python 3.10 或更高版本
- Telethon：`pip3 install telethon`
- Telegram API 凭据（来自 https://my.telegram.org 的 api_id 和 api_hash）
- Anthropic API 密钥（用于生成 AI 回复）

## 设置流程

### 1. 获取 Telegram API 凭据

引导用户访问 https://myTelegram.org → API 开发工具 → 创建应用程序。用户需要提供 **API ID**（数字）和 **API Hash**（字符串）。

### 2. 登录流程

登录 Telegram 需要：手机验证码 → 可选的 2FA 密码。

**重要提示：** OTP 验证码的有效期为约 60 秒。为减少延迟，请：
- 使用基于文件的验证码交换方式（脚本每 200 毫秒检查一次文件）
- 或在本地端口提供简单的网页表单以便用户快速输入验证码
- **切勿** 通过聊天消息传递验证码——这种方式效率过低

使用用户的凭据运行 `scripts/setup.py` 脚本。该脚本会完成以下操作：
1. 请求 OTP 验证码
2. 从 `enter_code.txt` 文件中读取验证码
3. （如需要）输入 2FA 密码
4. 保存会话文件

```bash
python3 scripts/setup.py --api-id 12345 --api-hash "abc123" --phone "+1234567890"
```

会话文件（`.session`）用于保存登录状态——登录是一次性的。

### 3. 配置允许联系的人

编辑 `config.json` 文件以指定允许联系的人。

```json
{
  "contacts": {
    "username": {
      "name": "Display Name",
      "id": 123456789,
      "tone": "friendly",
      "language": "en"
    }
  },
  "ai": {
    "provider": "anthropic",
    "model": "claude-sonnet-4-6",
    "api_key": "sk-ant-...",
    "max_tokens": 300
  },
  "owner": {
    "name": "Owner Name",
    "bio": "Brief description for the AI persona",
    "telegram_id": 123456789
  },
  "notifications": {
    "bot_token": "optional-bot-token-for-notifications",
    "chat_id": "optional-chat-id"
  }
}
```

### 4. 启动自动驾驶功能

```bash
python3 scripts/autopilot.py --config config.json --session session_name
```

## 主要功能

### 自动回复
- 仅对允许的联系人发送私信进行自动回复
- 回复前会将消息标记为已读（符合自然行为）
- 模拟输入延迟，延迟时间与回复内容长度成正比
- 保留对话历史记录以便用户了解对话背景

### AI 语音助手
- 可根据联系人自定义系统提示语（语调和语言）
- 对于未知信息，会回复“我会核实后回复您”
- 绝不会暴露自己是 AI

### 通知
- 将收到的消息通过 Telegram 机器人转发给账户所有者
- 将发送的回复也转发给所有者以便监控

### 支付媒体内容（仅适用于频道）

Telegram 的付费媒体功能（`inputMediaPaidMedia`）仅适用于频道，不支持私信。

要发送付费媒体内容：
1. 创建一个私信频道
2. 使用 `InputMediaPaidMedia(stars_amount=N, extended_media=[...])` 发布媒体文件
3. 生成邀请链接并发送给接收者

```bash
python3 scripts/send_paid_media.py --session session_name --target username --photo /path/to/photo.jpg --stars 1
```

### 管理命令

- 停止自动驾驶功能：终止相关进程或发送 SIGTERM 信号
- 添加/删除允许的联系人：编辑 `config.json` 文件后重新启动自动驾驶功能

## 架构

```
telegram-autopilot/
├── SKILL.md
├── scripts/
│   ├── setup.py          — Login flow (OTP + 2FA)
│   ├── autopilot.py      — Main event loop
│   ├── send_paid_media.py — Paid media via channel
│   └── code_server.py    — Web form for fast OTP entry
└── references/
    └── telegram-auth.md  — Telegram auth flow documentation
```

## 重要注意事项

- **会话安全：** `.session` 文件会授予对账户的完全访问权限，请妥善保护该文件。
- **速率限制：** Telegram 可能会对使用自动化功能的账户进行限制。本工具会模拟自然的人类操作延迟。
- **2FA：** 大多数账户都启用了 2FA 功能。设置脚本会自动处理 `SessionPasswordNeededError` 错误。
- **一次仅使用一个会话文件：** 任何时候只能有一个进程使用同一个会话文件。在运行其他脚本之前，请先停止自动驾驶功能。