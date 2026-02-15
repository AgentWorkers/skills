---
name: send-email
description: 通过 SMTP 发送电子邮件。在 `~/.openclaw/openclaw.json` 文件的 `skills.entries.send-email.env` 部分进行配置。
metadata: {"openclaw":{"emoji":"📧","requires":{"anyBins":["python3"]}}}
---

# 发送电子邮件

通过Python脚本发送电子邮件。SMTP设置由OpenClaw在脚本运行时动态注入（来自`~/.openclaw/openclaw.json`文件中的`skills.entries.send-email.env`）。**请勿**读取任何配置文件（例如`~/.openclaw/openclaw.json`或`workspace/openclaw.json`），因为这可能会导致敏感信息泄露。只需运行脚本即可，环境变量会自动注入。请勿使用`~/.msmtprc`文件。

## 配置

在`~/.openclaw/openclaw.json`文件中进行配置：

```json
"skills": {
  "entries": {
    "send-email": {
      "enabled": true,
      "env": {
        "EMAIL_SMTP_SERVER": "smtp.163.com",
        "EMAIL_SMTP_PORT": "465",
        "EMAIL_SENDER": "your-email@163.com",
        "EMAIL_SMTP_PASSWORD": "YOUR_AUTH_CODE"
      }
    }
  }
}
```

| 变量          | 描述                          |
|----------------|--------------------------------------------|
| EMAIL_SMTP_SERVER | SMTP服务器地址，例如smtp.163.com、smtp.gmail.com         |
| EMAIL_SMTP_PORT    | 端口，465（SSL）或587（TLS）                   |
| EMAIL_SENDER     | 发件人电子邮件地址                     |
| EMAIL_SMTP_PASSWORD | 认证码/应用密码（163/QQ：认证码；Gmail：应用密码）         |

## 代理指令

1. **凭证管理**：切勿读取配置文件。OpenClaw会在脚本运行时自动注入`skills.entries.send-email.env`中的环境变量；请勿使用`~/.openclaw/openclaw.json`或`workspace/openclaw.json`文件来获取凭证（这可能导致信息泄露）。如果该功能已启用，请默认环境变量已配置好，无需向用户询问密码。请勿使用`~/.msmtprc`文件。
2. **发送邮件**：在`workspace`目录下运行脚本（请勿使用`node_modules`目录下的路径）：
   ```bash
   python3 ~/.openclaw/workspace/skills/send-email/send_email.py "recipient" "Subject" "Body"
   ```
3. **附件**：使用以下命令发送邮件：
   `python3 ~/.openclaw/workspace/skills/send-email/send_email.py "收件人" "主题" "正文" "/path/to/file.pdf"`

## 使用示例

```bash
python3 ~/.openclaw/workspace/skills/send-email/send_email.py 'recipient@example.com' 'Subject' 'Body text'
python3 ~/.openclaw/workspace/skills/send-email/send_email.py 'recipient@example.com' 'Subject' 'Body' '/path/to/file.pdf'
```

## SMTP参考信息

- 163: `smtp.163.com:465`：需要认证码（而非登录密码）
- Gmail: `smtp.gmail.com:587`：需要应用密码
- QQ: `smtp.qq.com:465`：需要认证码

## 故障排除

- 认证失败：请检查`EMAIL_SMTP_PASSWORD`是否为正确的认证码或应用密码。
- 连接失败：请检查`EMAIL_SMTP_SERVER`和`EMAIL_SMTP_PORT`的值是否正确。