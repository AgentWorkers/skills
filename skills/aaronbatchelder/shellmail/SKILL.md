---
name: shellmail
description: >
  **AI代理的电子邮件API**  
  该API用于处理与电子邮件相关的操作，具体功能包括：  
  1. 检查收件箱；  
  2. 读取电子邮件内容；  
  3. 提取一次性密码（OTP）代码；  
  4. 通过ShellMail搜索邮件信息。  
  API支持以下请求参数：  
  - `check_email`：检查收件箱中的所有邮件；  
  - `inbox`：仅读取收件箱中的邮件；  
  - `otp`：提取当前邮件中的OTP代码；  
  - `verification_code`：获取与验证相关的代码；  
  - `shellmail`：通过ShellMail查询邮件信息；  
  - 以及其他与电子邮件相关的请求。  
  通过调用这些API，您可以轻松实现AI代理与电子邮件系统的交互，从而提升系统的自动化处理能力。
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

如果尚未配置令牌：

1. 询问用户所需的电子邮件地址（例如：“atlas”）以及用于恢复访问权限的备用电子邮件地址。
   - 或者使用 `auto` 生成一个随机地址（例如：“swift-reef-4821”）。
2. 运行命令：`{baseDir}/scripts/shellmail.sh create <name> <recovery_email>`
3. 如果该地址已被占用：
   - 建议用户选择其他地址，或者继续使用 `auto` 生成新地址。
   - 除非用户确认这是他们之前的收件箱地址，否则不要建议使用备用电子邮件地址进行恢复。
4. 保存返回的令牌：

```
gateway config.patch {"skills":{"entries":{"shellmail":{"env":{"SHELLMAIL_TOKEN":"sm_..."}}}}}
```

5. 告知用户务必妥善保管令牌——该令牌不会再显示给用户。

6. 建议用户向新地址发送一封测试邮件以验证功能是否正常。

7. 用户确认无误后，运行 `inbox` 命令查看测试邮件是否已成功送达。

## 令牌恢复

仅当用户明确表示无法访问自己拥有的现有收件箱时，才使用备用电子邮件地址进行令牌恢复：

```bash
{baseDir}/scripts/shellmail.sh recover <address@shellmail.ai> <recovery_email>
```

此操作会将新的令牌发送到用户指定的备用电子邮件地址。对于“地址已被占用”的错误情况，切勿建议用户使用此方法恢复令牌。

## 命令列表

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

**用户请求：“检查我的邮件”：**
```bash
{baseDir}/scripts/shellmail.sh inbox --unread
```

**用户请求：“获取验证码”：**
```bash
{baseDir}/scripts/shellmail.sh otp --wait 30
```

**用户请求：“等待 GitHub 发送的 OTP”：**
```bash
{baseDir}/scripts/shellmail.sh otp --wait 30 --from github.com
```

## API 参考

基础 URL：`https://shellmail.ai`

所有 API 端点均使用以下授权方式：`Authorization: Bearer $SHELLMAIL_TOKEN`

| 端点          | 方法          | 描述                                      |
|------------------|--------------|-----------------------------------------|
| `/api/mail`       | GET           | 列出未读邮件（可选参数：?unread=true&limit=50）           |
| `/api/mail/:id`     | GET           | 读取完整邮件内容                         |
| `/api/mail/:id`     | PATCH          | 更新邮件的阅读状态（is_read, is_archived）             |
| `/api/mail/:id`     | DELETE         | 删除邮件                                   |
| `/api/mail/otp`      | GET           | 获取 OTP（可选参数：?timeout=30000&from=domain）         |
| `/api/mail/search`    | GET           | 搜索邮件（可选参数：?q=text&from=domain&has_otp=true）       |
| `/api/addresses`    | POST           | 创建新的电子邮件地址（local, recovery_email）           |