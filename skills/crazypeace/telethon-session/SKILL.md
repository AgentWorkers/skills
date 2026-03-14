---
name: telethon-session
description: Generate Telethon .session files for user-account login to Telegram. Use when: (1) user wants to test a Telegram bot as a real user, (2) user needs to interact with Telegram via user identity, (3) creating a Telegram session for Telethon-based automation, (4) mentions telethon, telegram session, or user-account login. NOT for: bot-token-based bots (no session needed).
---

# Telethon 会话生成器

该工具用于生成一个 `.session` 文件，以便通过 Telethon 对 Telegram 用户账户进行身份验证。

## 先决条件

- **`telethon`**：使用 `pip install telethon` 进行安装（如有需要，可以使用虚拟环境 `venv`）  
- 来自 <https://my.telegram.org> 的 API 凭据（`api_id` 和 `api_hash`）

## 快速入门

在交互式（PTY）模式下运行捆绑的脚本——Telegram 会发送登录代码，并可能要求输入二次验证（2FA）：

```bash
python3 scripts/login.py --api-id YOUR_ID --api-hash YOUR_HASH --phone "+86..."
```

脚本会提示用户输入：
1. **登录代码**：从 Telegram 应用程序或短信中获取
2. **二次验证密码**：仅在账户启用了该功能时需要输入

成功后，`<session_name>.session` 文件会生成在当前工作目录中。

## 重要说明

- **会话文件可重复使用**：除非 Telegram 使会话失效，否则无需重新登录。
- **请勿将 `.session` 文件提交到版本控制系统中**（应将其视为机密信息）。
- **机器人令牌（Bot Token）与会话文件不同**：机器人使用 `bot_token=` 进行身份验证，因此不需要会话文件。
- 如果在由外部管理的 Python 环境中安装 `telethon` 失败，请使用虚拟环境 `venv`：

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install telethon
  ```

## 使用会话文件

```python
from telethon import TelegramClient

client = TelegramClient('telegram_session', api_id, api_hash)
await client.start()  # auto-loads session, no prompt needed
```