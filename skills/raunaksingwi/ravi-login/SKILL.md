---
name: ravi-login
description: 使用您的 Ravi 身份注册并登录相关服务——该系统负责处理表单提交、双因素认证（2FA）、一次性密码（OTP）以及凭证存储功能。请勿将其用于单独的收件箱阅读（请使用 ravi-inbox）或邮件发送（请使用 ravi-email-send）。
---
# Ravi 登录

提供端到端的工作流程，用于使用您的 Ravi 身份进行注册、登录和完成验证。

## 您的姓名

当表格要求您输入姓名时，请使用您的**身份名称**（而非账户所有者的姓名）：

```bash
# Get identity name (use this for "First Name" / "Full Name" fields)
IDENTITY=$(ravi identity list --json | jq -r '.[0]')
NAME=$(echo "$IDENTITY" | jq -r '.name')
```

**切勿**在表单字段中使用 `ravi get owner`。账户所有者是指账户背后的实际使用者，而身份名称是**您的**姓名。

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

## 完成双因素认证（2FA）/一次性密码（OTP）验证

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

- **耐心等待，不要着急**——短信或电子邮件的发送需要 2-10 秒的时间。在检查之前，请使用 `sleep 5` 命令稍作等待。
- **立即保存凭据**——在注册过程中创建密码记录，以免丢失密码。
- **表单填写时使用身份名称**——始终使用您的身份名称，而非账户所有者的姓名。
- **发送操作存在频率限制**——每小时最多发送 60 封电子邮件，每天最多发送 500 封。详情请参阅 `ravi-email-send` 技能。
- **电子邮件质量很重要**——如果您需要在工作流程中发送电子邮件（例如联系支持），请参考 `ravi-email-writing` 以获取关于格式和防垃圾邮件设置的建议。

## 相关技能

- **ravi-identity**——获取您的电子邮件地址、电话号码和身份名称，用于填写表单。
- **ravi-inbox**——读取 OTP（一次性密码）、验证码和确认邮件。
- **ravi-email-send**——在工作流程中发送电子邮件（如支持请求、确认信息）。
- **ravi-email-writing**——撰写专业的电子邮件，避免被垃圾邮件过滤器拦截。
- **ravi-passwords**——在注册后存储和检索网站凭据。
- **ravi-secrets**——存储服务注册过程中获得的 API 密钥。
- **ravi-feedback**——报告登录流程中的问题或提出工作流程改进建议。