---
name: shellmail
version: 1.2.2
description: 用于AI代理的电子邮件API：可以检查收件箱、阅读邮件、提取OTP验证码，并通过ShellMail搜索邮件内容。该API支持响应与电子邮件相关的请求，如“check email”、“inbox”、“otp”、“verification code”、“shellmail”等。
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
metadata:
  openclaw:
    requires:
      env:
        - SHELLMAIL_TOKEN
      bins:
        - curl
        - python3
      primaryEnv: SHELLMAIL_TOKEN
---
# ShellMail

通过 shellmail.ai 为 AI 代理发送和接收电子邮件，自动提取验证码（OTP）。

## ⚠️ 安全与隐私声明

**此功能需要一个敏感的 `SHELLMAIL_TOKEN`，该令牌可授予代理对您的收件箱和验证码的完全访问权限。**

首次设置此功能时，系统会提示您使用 `gateway config.patch` 命令将令牌保存到代理配置中。这意味着：
- 代理将永久拥有对您 ShellMail 收件箱的访问权限；
- 该令牌会一直有效，直到您明确撤销或从配置中删除它；
- 仅当您完全信任 shellmail.ai 并了解相关的隐私影响时，才应继续操作。

**最佳实践：**
- 仅将 ShellMail 用于与代理相关的活动，而非个人邮件；
- 尽可能使用一次性或独立的恢复邮箱；
- 在确认之前，请仔细检查 `gateway config.patch` 命令的输出；
- 当不再需要此功能时，请撤销代理的访问权限。

## 首次设置

如果尚未配置令牌：
1. 询问用户所需的邮箱地址（例如：“atlas”）以及恢复邮箱地址；
   - 或者使用 `auto` 生成一个随机地址（例如：“swift-reef-4821”）；
2. 运行命令：`{baseDir}/scripts/shellmail.sh create <name> <recovery_email>`；
3. 如果地址已被占用：
   - 如果用户表示这是他们的旧地址：尝试使用相同的恢复邮箱重新创建账户（被删除的地址会保留 14 天，之后可以重新申请）；
   - 否则：建议用户选择其他地址或使用 `auto` 生成新地址；
   - 除非用户确认这是他们的旧收件箱，否则不要建议使用恢复邮箱；
4. 保存返回的令牌：

```
gateway config.patch {"skills":{"entries":{"shellmail":{"env":{"SHELLMAIL_TOKEN":"sm_..."}}}}}
```

**⚠️ 重要提示：** 在运行此命令之前，请向用户说明：
   - 该令牌将被保存到代理配置中，以实现永久访问；
   - 代理将一直拥有对用户收件箱和验证码的访问权限，直到令牌被删除或撤销；
   - 仅当用户信任 shellmail.ai 并了解相关隐私影响时，才应继续操作；
   - 在执行命令前，请向用户展示具体的命令内容并获取他们的确认；
5. 告诉用户务必妥善保管令牌（令牌不会再次显示）；
6. 建议用户向新邮箱发送测试邮件以验证其是否正常工作；
7. 用户确认后，运行 `inbox` 命令查看测试邮件是否已成功送达。

## 令牌恢复

仅当用户明确表示无法访问自己拥有的现有收件箱时，才使用恢复功能：

```bash
{baseDir}/scripts/shellmail.sh recover <address@shellmail.ai> <recovery_email>
```

此命令会将新的令牌发送到用户提供的恢复邮箱地址。对于“地址已被占用”的错误情况，请不要建议使用此功能。

## 命令列表

```bash
{baseDir}/scripts/shellmail.sh <command>
```

### 查看收件箱
```bash
{baseDir}/scripts/shellmail.sh inbox
{baseDir}/scripts/shellmail.sh inbox --unread
```

### 阅读邮件
```bash
{baseDir}/scripts/shellmail.sh read <email_id>
```

### 获取验证码
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

## 常见操作场景

**用户请求“查看我的邮件”：**
```bash
{baseDir}/scripts/shellmail.sh inbox --unread
```

**用户请求“获取验证码”：**
```bash
{baseDir}/scripts/shellmail.sh otp --wait 30
```

**用户请求“等待 GitHub 验证码”：**
```bash
{baseDir}/scripts/shellmail.sh otp --wait 30 --from github.com
```

## 撤销访问权限

如果用户希望撤销代理对 ShellMail 收件箱的访问权限：
### 从配置中删除令牌
```bash
gateway config.patch '{"skills":{"entries":{"shellmail":{"env":{"SHELLMAIL_TOKEN":""}}}}}'
```

### 完全删除账户
```bash
{baseDir}/scripts/shellmail.sh delete-account
```

**注意：** 被删除的邮箱地址会保留 14 天，原账户所有者只能通过恢复邮箱重新申请访问权限。

## API 参考

基础 URL：`https://shellmail.ai`

所有 API 端点均使用 `Authorization: Bearer $SHELLMAIL_TOKEN` 进行身份验证。

| 端点            | 方法            | 描述                                      |
|-----------------|------------------|-------------------------------------------|
| `/api/mail`         | GET            | 列出未读邮件（?unread=true&limit=50）                     |
| `/api/mail/:id`       | GET            | 阅读完整邮件                               |
| `/api/mail/:id`       | PATCH            | 更新邮件状态（is_read, is_archived）                     |
| `/api/mail/:id`       | DELETE            | 删除邮件                                   |
| `/api/mail/otp`        | GET            | 获取验证码（?timeout=30000&from=domain）                   |
| `/api/mail/search`      | GET            | 搜索邮件（?q=text&from=domain&has_otp=true）                |
| `/api/addresses`      | POST            | 创建新邮箱地址（local, recovery_email）                   |