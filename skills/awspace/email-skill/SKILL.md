---
name: email
description: 电子邮件管理和自动化：支持跨多个邮件服务提供商发送、接收、搜索和整理电子邮件。
metadata: {"clawdbot":{"emoji":"📧","always":true,"requires":{"bins":["python3"]}}}
---
# 电子邮件 📧

支持附件管理的电子邮件发送与自动化功能。

## 主要功能

- 支持发送带有附件的电子邮件
- 支持多种电子邮件服务提供商（Gmail、Outlook、Yahoo等）
- 支持HTML格式和纯文本格式的电子邮件
- 支持抄送（CC）和密送（BCC）功能
- 可测试电子邮件发送功能
- 使用安全的TLS/SSL连接

## 设置说明

### 1. 配置电子邮件凭据

在工作区中创建一个名为 `email_config.json` 的配置文件：

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "username": "your-email@gmail.com",
  "password": "your-app-password",
  "sender_name": "OpenClaw Assistant",
  "use_tls": true,
  "use_ssl": false
}
```

### 2. （推荐）Gmail用户操作

1. 在您的Google账户中启用两步验证
2. 生成应用密码：
   - 访问 https://myaccount.google.com/security
   - 在“登录到Google”选项下，选择“应用密码”
   - 为“Mail”服务生成一个新的应用密码
   - 在配置文件中使用这个16位的密码

### 3. 替代方案：使用环境变量

您可以不使用配置文件，而是通过设置环境变量来配置这些信息：

```bash
# Windows
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=587
set EMAIL_USERNAME=your-email@gmail.com
set EMAIL_PASSWORD=your-app-password
set EMAIL_SENDER_NAME="OpenClaw Assistant"

# macOS/Linux
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export EMAIL_USERNAME=your-email@gmail.com
export EMAIL_PASSWORD=your-app-password
export EMAIL_SENDER_NAME="OpenClaw Assistant"
```

## 使用示例

### 发送简单邮件
```bash
python email_sender.py --to "recipient@example.com" --subject "Hello" --body "This is a test email"
```

### 发送带有附件的邮件
```bash
python email_sender.py --to "recipient@example.com" --subject "Report" --body "Please find attached" --attachment "report.pdf" --attachment "data.xlsx"
```

### 发送测试邮件
```bash
python email_sender.py --to "your-email@gmail.com" --test
```

### 与OpenClaw命令结合使用
```
"Send email to recipient@example.com with subject Meeting Notes and body Here are the notes from today's meeting"
"Send test email to verify configuration"
"Email the report.pdf file to team@company.com"
```

## 支持的电子邮件服务提供商

| 服务提供商 | SMTP服务器 | 端口 | 是否支持TLS |
|----------|-------------|------|---------|
| Gmail | smtp.gmail.com | 587 | 支持 |
| Outlook/Office365 | smtp.office365.com | 587 | 支持 |
| Yahoo | smtp.mail.yahoo.com | 587 | 支持 |
| QQ Mail | smtp.qq.com | 587 | 支持 |
| 自定义SMTP服务器 | yoursmtp.server.com | 587/465 | 根据实际情况配置 |

## Python API使用方法
```python
from email_sender import EmailSender

# Initialize with config file
sender = EmailSender("email_config.json")

# Send email with attachment
result = sender.send_email(
    to_email="recipient@example.com",
    subject="Important Document",
    body="Please review the attached document.",
    attachments=["document.pdf", "data.csv"]
)

if result["success"]:
    print(f"Email sent with {result['attachments']} attachments")
else:
    print(f"Error: {result['error']}")
```

## 故障排除

### 常见问题

1. **身份验证失败**
   - 确认您的用户名和密码是否正确
   - 对于Gmail，请使用应用密码而非普通密码
   - 检查是否已启用两步验证

2. **连接被拒绝**
   - 确认SMTP服务器和端口的设置是否正确
   - 检查防火墙设置
   - 尝试使用其他端口（SSL连接通常使用465端口）

3. **附件过大**
   - 大多数服务提供商对附件大小有限制（通常为25MB）
   - 考虑压缩文件或使用云存储链接

## 安全注意事项

- 切勿将电子邮件凭据提交到版本控制系统中
- 在生产环境中使用环境变量进行配置
- 定期更换应用密码
- 建议为自动化任务使用专用的电子邮件账户