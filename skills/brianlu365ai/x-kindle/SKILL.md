---
name: x-to-kindle
description: 将 X/Twitter 上的帖子发送到 Kindle，以实现无干扰的阅读体验。适用于用户分享 X/Twitter 链接后希望在 Kindle 上阅读，或请求将推文/帖子发送到 Kindle 设备的情况。
---

# 将 X/Twitter 帖子转换为 Kindle 可读格式的文档

通过电子邮件将 X/Twitter 帖子转换为 Kindle 可读的文档。

## 必备条件

- 拥有带应用密码的 Gmail 账户（或支持 SMTP 的其他邮件服务）
- Kindle 的电子邮件地址（可在亚马逊账户设置中找到）

## 工作流程

当用户分享一个 X 链接时：

1. **通过 fxtwitter API 提取内容**：
   ```
   https://api.fxtwitter.com/status/<tweet_id>
   ```
   从 URL 中提取内容：`twitter.com/*/status/<id>` 或 `x.com/*/status/<id>`

2. **将内容格式化为 HTML 邮件**：
   ```html
   <html>
   <body>
     <h1>@{author_handle}</h1>
     <p>{tweet_text}</p>
     <p><em>{timestamp}</em></p>
     <p><a href="{original_url}">View on X</a></p>
   </body>
   </html>
   ```

3. **通过 SMTP 将邮件发送到用户的 Kindle 地址**，邮件主题行设置为帖子的预览内容。

## 配置信息

配置信息存储在 `TOOLS.md` 文件中：
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

用户发送链接：`https://x.com/elonmusk/status/1234567890`

1. 从 `https://api.fxtwitter.com/status/1234567890` 获取内容
2. 提取作者、正文和时间戳
3. 将格式化后的 HTML 邮件发送到用户的 Kindle 地址
4. 确认邮件已成功发送至 Kindle："邮件已发送至 Kindle 📚"