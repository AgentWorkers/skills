---
name: x-to-kindle
description: 将 X/Twitter 的帖子发送到 Kindle 上，以实现无干扰的阅读体验。适用于用户分享 X/Twitter 链接并希望在 Kindle 上阅读，或者请求将推文/帖子发送到他们的 Kindle 设备上的情况。
---

# 将 X/Twitter 帖子转换为 Kindle 可读文档

通过电子邮件将 X/Twitter 帖子转换为 Kindle 可读的文档。

## 必备条件

- 拥有带应用密码的 Gmail 账户（或已配置的 SMTP 账户）
- Kindle 电子邮件地址（可在 Amazon 账户设置中找到）

## 工作流程

当用户分享一个 X 链接时：

1. **提取内容**：使用 fxtwitter API 提取内容：
   ```
   https://api.fxtwitter.com/status/<tweet_id>
   ```
   从以下 URL 中提取内容：`twitter.com/*/status/<id>` 或 `x.com/*/status/<id>`

2. **格式化为 HTML 文件**（保存到 `/tmp` 目录）：
   ```html
   <!DOCTYPE html>
   <html>
   <head><meta charset="UTF-8"><title>{title}</title></head>
   <body style="font-family: Georgia, serif; max-width: 600px; margin: 0 auto; padding: 20px; line-height: 1.6;">
     <h1>@{author_handle}</h1>
     <p>{tweet_text}</p>
     <p><em>{timestamp}</em></p>
     <p><a href="{original_url}">View on X</a></p>
   </body>
   </html>
   ```

3. **通过 SMTP 发送邮件，并将 HTML 文件作为附件**（Kindle 需要附件，而非内联 HTML）：
   ```python
   from email.mime.multipart import MIMEMultipart
   from email.mime.text import MIMEText
   from email.mime.base import MIMEBase
   from email import encoders
   
   msg = MIMEMultipart()
   msg['Subject'] = "Tweet from @handle"
   msg['From'] = from_email
   msg['To'] = kindle_email
   
   # Plain text body (not the content)
   msg.attach(MIMEText("Article attached.", 'plain'))
   
   # HTML file as attachment - THIS IS REQUIRED
   with open("/tmp/article.html", "rb") as f:
       attachment = MIMEBase('text', 'html')
       attachment.set_payload(f.read())
       encoders.encode_base64(attachment)
       attachment.add_header('Content-Disposition', 'attachment', filename='article.html')
       msg.attach(attachment)
   ```

## 工具
- `send_to_kindle`：用于将本地文件发送到配置好的 Kindle 电子邮件地址。

## 配置

在 Clawdbot 的配置文件（或 `.env` 文件）中设置以下环境变量：

- `SMTP_EMAIL`：发送者的电子邮件地址（例如：gmail）
- `SMTP_PASSWORD`：应用密码
- `KINDLE_EMAIL`：Kindle 电子邮件地址
- `SMTP_SERVER`：（可选）默认值：smtp.gmail.com
- `SMTP_PORT`：（可选）默认值：587

## 工具说明

### `send_to_kindle`

将本地文件（PDF、HTML、TXT 格式）发送到 Kindle。

- **使用方法**：`python3 skills/x-to-kindle/send_to_kindle.py <file_path>`

## 配置信息

详细配置信息请参见 `TOOLS.md` 文件：

```markdown
## Kindle
- Address: user@kindle.com

## Email (Gmail SMTP)
- From: your@gmail.com
- App Password: xxxx xxxx xxxx xxxx
- Host: smtp.gmail.com
- Port: 587
```

## 示例

用户分享链接：`https://x.com/elonmusk/status/1234567890`

1. 从 `https://api.fxtwitter.com/status/1234567890` 获取内容
2. 提取作者、文本和时间戳
3. 将格式化后的 HTML 文件发送到 Kindle 电子邮件地址
4. 确认发送结果：“已发送到 Kindle 📚”