---
name: shellmail
description: 用于AI代理的电子邮件API：可以检查收件箱、阅读邮件、提取OTP验证码，并通过ShellMail搜索邮件内容。该API支持以下请求类型：“check email”、“inbox”、“otp”、“verification code”、“shellmail”以及任何与电子邮件相关的操作。
homepage: https://shellmail.ai
source: https://github.com/aaronbatchelder/shellmail
env:
  SHELLMAIL_TOKEN:
    required: true
    sensitive: true
    description: Bearer token for ShellMail API authentication (grants access to inbox and OTPs)
  SHELLMAIL_API_URL:
    required: false
    default: https://shellmail.ai
    description: API base URL (only change for self-hosted instances)
---
# ShellMail

通过 shellmail.ai 为 AI 代理发送和接收电子邮件。支持创建收件箱、自动接收邮件以及提取 OTP（一次性密码）。

## 首次设置

如果未配置令牌：

1. 询问用户所需的电子邮件地址（例如：“atlas”）以及备用电子邮件地址。
2. 运行以下命令：`{baseDir}/scripts/shellmail.sh create <name> <recovery_email>`
3. 保存返回的令牌：

```
gateway config.patch {"skills":{"entries":{"shellmail":{"env":{"SHELLMAIL_TOKEN":"sm_..."}}}}}
```

4. 告知用户务必安全保管该令牌——该令牌不会再显示。

## 命令

```bash
{baseDir}/scripts/shellmail.sh <command>
```

### 检查收件箱
```bash
{baseDir}/scripts/shellmail.sh inbox
{baseDir}/scripts/shellmail.sh inbox --unread
```

### 阅读邮件
```bash
{baseDir}/scripts/shellmail.sh read <email_id>
```

### 获取 OTP 代码
```bash
# Get latest OTP
{baseDir}/scripts/shellmail.sh otp

# Wait up to 30 seconds for OTP
{baseDir}/scripts/shellmail.sh otp --wait 30

# Filter by sender
{baseDir}/scripts/shellmail.sh otp --wait 30 --from github.com
```

### 搜索邮件
```bash
{baseDir}/scripts/shellmail.sh search --query "verification"
{baseDir}/scripts/shellmail.sh search --otp
{baseDir}/scripts/shellmail.sh search --from stripe.com
```

### 其他命令
```bash
{baseDir}/scripts/shellmail.sh mark-read <id>
{baseDir}/scripts/shellmail.sh archive <id>
{baseDir}/scripts/shellmail.sh delete <id>
{baseDir}/scripts/shellmail.sh health
```

## 常见对话场景

**用户说：“检查我的邮件”：**
```bash
{baseDir}/scripts/shellmail.sh inbox --unread
```

**用户说：“获取验证码”：**
```bash
{baseDir}/scripts/shellmail.sh otp --wait 30
```

**用户说：“等待 GitHub 发送的 OTP”：**
```bash
{baseDir}/scripts/shellmail.sh otp --wait 30 --from github.com
```

## API 参考

基础 URL：`https://shellmail.ai`

所有 API 端点均使用 `Authorization: Bearer $SHELLMAIL_TOKEN` 进行身份验证。

| 端点            | 方法        | 描述                                      |
|------------------|-----------|-------------------------------------------|
| `/api/mail`       | GET        | 列出未读邮件（?unread=true&limit=50）                   |
| `/api/mail/:id`      | GET        | 阅读完整邮件                              |
| `/api/mail/:id`      | PATCH       | 更新邮件的阅读状态或归档状态（{is_read, is_archived}）         |
| `/api/mail/:id`      | DELETE      | 删除邮件                                      |
| `/api/mail/otp`       | GET        | 获取 OTP（?timeout=30000&from=domain）                   |
| `/api/mail/search`    | GET        | 搜索邮件（?q=text&from=domain&has_otp=true）             |
| `/api/addresses`     | POST        | 创建新的本地邮箱地址或备用邮箱地址                   |