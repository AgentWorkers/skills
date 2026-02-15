---
name: near-email-reporter
description: 通过 SMTP 配置、调度功能以及自动报告机制，将 NEAR 报告和警报通过电子邮件发送出去。
---
# NEAR 邮件报告功能

通过电子邮件发送 NEAR 交易报告，并支持定时发送。

## 描述

此功能允许您配置电子邮件设置、发送 NEAR 交易报告、设置警报以及安排定期电子邮件报告。该功能使用标准的 SMTP 协议，并采用安全的配置存储方式。

## 特点

- 配置 SMTP 电子邮件设置
- 通过电子邮件发送交易报告
- 为特定事件设置警报
- 安排定期报告
- 使用安全的配置存储方式

## 命令

### `near-email setup [选项]`
配置电子邮件设置。

**选项:**
- `--host <主机>` - SMTP 服务器主机
- `--port <端口>` - SMTP 服务器端口（默认：587）
- `--user <用户名>` - SMTP 用户名
- `--pass <密码>` - SMTP 密码
- `--from <发件人邮箱>` - 发件人邮箱地址
- `--secure` - 使用 SSL/TLS（默认：不使用）

**示例:**
```bash
near-email setup --host smtp.gmail.com --port 587 --user myemail@gmail.com --pass mypassword --from myemail@gmail.com
```

### `near-email report <账户ID> [收件人]`
为指定账户发送交易报告。

**参数:**
- `account_id` - 需要报告的 NEAR 账户ID
- `recipient` - 收件人邮箱（可选，使用默认值）

### `near-email alert <账户ID> <阈值> [收件人]`
为指定账户设置余额警报。

**参数:**
- `account_id` - 需要监控的 NEAR 账户ID
- `threshold` - 余额阈值（以 NEAR 为单位）
- `recipient` - 收件人邮箱（可选）

### `near-email schedule <账户ID> <cron_expr> [收件人]`
安排定期电子邮件报告。

**参数:**
- `account_id` - 需要报告的 NEAR 账户ID
- `cron_expr` - Cron 表达式（例如：“0 9 * * *”表示每天上午 9 点发送）
- `recipient` - 收件人邮箱（可选）

## 配置

电子邮件设置存储在 `~/.near-email/config.json` 文件中，并具有受限的访问权限。

## 必备条件

- 拥有用于发送电子邮件的 SMTP 账户（如 Gmail、SendGrid 等）
- 需要 Node.js 环境来运行相关脚本

## 注意事项

- 对于 Gmail，请使用应用密码（App Password）：https://myaccount.google.com/apppasswords
- 配置文件采用安全存储方式，仅允许授权用户访问

## 参考资料

- Nodemailer：https://nodemailer.com/
- NEAR RPC API：https://docs.near.org/api/rpc