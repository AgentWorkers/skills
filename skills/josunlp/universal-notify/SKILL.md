---
name: universal-notify
description: 通过单个脚本通过多个渠道发送通知。支持 ntfy.sh（免费、无需注册）、Gotify（自托管）、通用 Webhook、电子邮件（SMTP/curl）、Telegram Bot API 和 Pushover。适用于发送警报、监控通知、部署通知或任何需要通过用户偏好的渠道传达给用户的事件。提供统一的管理界面，并支持不同的优先级级别（低/普通/高/紧急）。
---

# Universal Notify

通过 `scripts/notify.sh` 发送通知：

```bash
# ntfy.sh (free, no auth needed)
scripts/notify.sh --channel ntfy --topic myalerts --message "Disk 90%!" --priority urgent

# Gotify (self-hosted)
scripts/notify.sh --channel gotify --url https://gotify.local --token TOKEN --message "Deploy done"

# Webhook (generic JSON POST)
scripts/notify.sh --channel webhook --url https://hooks.example.com/abc --message "Event fired"

# Email
scripts/notify.sh --channel email --smtp smtp://mail:587 --from a@x.com --to b@y.com --subject "Alert" --message "Check server"

# Telegram
scripts/notify.sh --channel telegram --bot-token BOT:TOK --chat-id 12345 --message "Hello"

# Pushover
scripts/notify.sh --channel pushover --app-token X --user-key Y --message "Alert" --priority high
```

## 常见选项

所有通知渠道都支持以下选项：
- `--message`（必填）：通知内容
- `--title`（可选）：通知标题
- `--priority`（可选）：通知优先级（默认值：normal）
  - `low`：低优先级
  - `normal`：普通优先级
  - `high`：高优先级
  - `urgent`：紧急优先级

## 系统要求

- 需要安装 `curl`（大多数系统都预装了该工具）

注意：`ntfy.sh` 本身不需要 API 密钥；其他通知渠道则需要使用相应的凭证进行身份验证。