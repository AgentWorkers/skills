---
name: ravi-login
description: 使用您的 Ravi 身份注册并登录服务——该系统负责处理表单提交、二次身份验证（2FA）、一次性密码（OTP）以及凭证存储。请勿将其用于单独的收件箱阅读功能（请使用 ravi-inbox），也不得用于发送电子邮件（请使用 ravi-email-send）。
---
# Ravi 登录

提供从注册、登录到完成身份验证的端到端工作流程。

## 你的姓名

当表格要求输入姓名时，请使用你的**身份姓名**，而不是账户所有者的姓名。
身份姓名应类似于真实的人名（例如：“Sarah Johnson”）。

```bash
# Get identity name — split into first/last for form fields
IDENTITY=$(ravi identity list --json | jq -r '.[0]')
NAME=$(echo "$IDENTITY" | jq -r '.name')
FIRST_NAME=$(echo "$NAME" | awk '{print $1}')
LAST_NAME=$(echo "$NAME" | awk '{print $2}')
```

> **注意：** 对于自动生成的姓名（例如：“Sarah Johnson”），这种姓名的拆分方式是有效的。对于自定义的身份姓名（例如：“Shopping Agent”），请直接使用完整的姓名，或者根据表格的要求进行调整。

**切勿** 在表格字段中使用 `ravi get owner` 命令。账户所有者是指账户背后的真实人物，而身份姓名才是**你的**姓名。

## 注册服务

```bash
# 1. Get your identity
EMAIL=$(ravi get email --json | jq -r '.email')
PHONE=$(ravi get phone --json | jq -r '.phone_number')

# 2. Fill the signup form with $EMAIL, $PHONE, and identity name

# 3. Generate and store a password
CREDS=$(ravi passwords create example.com --username "$EMAIL" --json)
PASSWORD=$(echo "$CREDS" | jq -r '.password')
# Use $PASSWORD in the signup form

# 4. Wait for verification
sleep 5
ravi inbox sms --unread --json   # Check for SMS OTP
ravi inbox email --unread --json # Check for email verification
```

## 登录服务

```bash
# Find stored credentials
ENTRY=$(ravi passwords list --json | jq -r '.[] | select(.domain == "example.com")')
UUID=$(echo "$ENTRY" | jq -r '.uuid')

# Get decrypted credentials
CREDS=$(ravi passwords get "$UUID" --json)
USERNAME=$(echo "$CREDS" | jq -r '.username')
PASSWORD=$(echo "$CREDS" | jq -r '.password')
# Use $USERNAME and $PASSWORD to log in
```

## 完成双重身份验证（2FA）/一次性密码（OTP）验证

```bash
# After triggering 2FA on a website:
sleep 5
CODE=$(ravi inbox sms --unread --json | jq -r '.[0].preview' | grep -oE '[0-9]{4,8}' | head -1)
# Use $CODE to complete the login
```

## 从电子邮件中提取验证链接

```bash
THREAD_ID=$(ravi inbox email --unread --json | jq -r '.[0].thread_id')
ravi inbox email "$THREAD_ID" --json | jq -r '.messages[].text_content' | grep -oE 'https?://[^ ]+'
```

## 提示

- **耐心等待，不要着急**——短信或电子邮件的发送需要 2 到 10 秒的时间。在检查之前，请使用 `sleep 5` 命令稍作等待。
- **立即保存凭据**——在注册过程中创建密码条目，以免丢失密码。
- **表格填写时使用身份姓名**——始终使用身份姓名，而不是账户所有者的姓名。
- **发送操作存在频率限制**——每小时最多发送 60 封电子邮件，每天最多 500 封。详情请参阅 `ravi-email-send` 技能。
- **电子邮件的质量很重要**——如果你需要在工作流程中发送电子邮件（例如联系支持），请参考 `ravi-email-writing` 以获取关于格式和反垃圾邮件的建议。

## 相关技能

- **ravi-identity**——获取用于表格字段的电子邮件地址、电话号码和身份姓名。
- **ravi-inbox**——读取一次性密码（OTP）、验证代码和确认邮件。
- **ravi-email-send**——在工作流程中发送电子邮件（如支持请求、确认信息）。
- **ravi-email-writing**——编写能够通过垃圾邮件过滤器的专业电子邮件。
- **ravi-passwords**——在注册后存储和检索网站凭据。
- **ravi-secrets**——存储服务注册过程中获得的 API 密钥。
- **ravi-feedback**——报告登录流程中的问题或提出工作流程改进的建议。