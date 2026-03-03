---
name: qq-email
description: "通过 QQ Mail 的 SMTP/IMAP 协议发送和接收电子邮件。适用场景：用户需要发送/接收电子邮件、查看收件箱、阅读邮件内容或通过电子邮件共享文档。使用前需在 `TOOLS.md` 文件中配置 QQ 邮箱的授权码。"
homepage: https://mail.qq.com
metadata: { "openclaw": { "emoji": "📧", "requires": { "bins": ["python3"], "files": ["~/.openclaw/workspace/skills/qq-email/qq_email.py", "~/.openclaw/workspace/TOOLS.md"] } } }
---
# QQ 邮件功能

通过 QQ Mail 的 SMTP/IMAP 服务器发送和接收电子邮件。

## 使用场景

✅ **适用于以下情况：**
- “给……发送电子邮件”
- “查看我的邮件”
- “阅读未读邮件”
- “将此文件通过电子邮件发送给[某人]”
- “通过电子邮件通知[某人]”
- “通过电子邮件分享此文档”
- “我的收件箱里有什么？”

## 不适用场景

❌ **请勿在以下情况下使用此功能：**
- 发送短信/WhatsApp → 使用相应的消息工具
- 记录内部信息 → 使用内存文件
- 发布公开内容 → 使用社交媒体工具

## 配置要求

在使用前，请在 `TOOLS.md` 文件中进行配置：

```markdown
### QQ Email

- Email: your_qq_number@qq.com
- Auth Code: your_16_char_auth_code
- Sender Name: Your Name
```

**获取 QQ 认证码：**
1. 登录到 mail.qq.com
2. 进入“设置” → “账户”
3. 启用 POP3/SMTP 服务
4. 生成认证码（16 个字符）

## 命令

### 发送电子邮件

```bash
python3 ~/.openclaw/workspace/skills/qq-email/qq_email.py send \
  --to "recipient@example.com" \
  --subject "Email Subject" \
  --content "Email content here"
```

### 接收/列出邮件

```bash
# List 10 recent emails
python3 ~/.openclaw/workspace/skills/qq-email/qq_email.py receive

# List 20 emails
python3 ~/.openclaw/workspace/skills/qq-email/qq_email.py receive --count 20

# Unread emails only
python3 ~/.openclaw/workspace/skills/qq-email/qq_email.py receive --unread
```

### 阅读特定邮件

```bash
# Read email by UID
python3 ~/.openclaw/workspace/skills/qq-email/qq_email.py read --uid 123

# Read and save attachments
python3 ~/.openclaw/workspace/skills/qq-email/qq_email.py read --uid 123 --save
```

### 将邮件标记为已读

```bash
python3 ~/.openclaw/workspace/skills/qq-email/qq_email.py mark-read --uid 123
```

### 发送 HTML 格式的电子邮件

```bash
python3 ~/.openclaw/workspace/skills/qq-email/qq_email.py send \
  --to "recipient@example.com" \
  --subject "HTML Email" \
  --content "<h1>Hello</h1><p>HTML content</p>" \
  --html
```

### 发送带附件的电子邮件

```bash
python3 ~/.openclaw/workspace/skills/qq-email/qq_email.py send \
  --to "recipient@example.com" \
  --subject "Document Attached" \
  --content "Please find attached." \
  --attachment "/path/to/file.pdf"
```

## 快速操作示例

**“给 test@example.com 发送电子邮件”**
→ 提示输入邮件主题和内容，然后执行相应操作：
```bash
python3 ~/.openclaw/workspace/skills/qq-email/qq_email.py --to "test@example.com" --subject "[subject]" --content "[content]"
```

**“将此文件通过电子邮件发送给某人”**
→ 提示输入收件人地址并添加附件：
```bash
python3 ~/.openclaw/workspace/skills/qq-email/qq_email.py --to "[email]" --subject "[subject]" --content "[content]" --attachment "[file]"
```

## 注意事项：
- 认证码不同于 QQ 密码（请从 mail.qq.com 的设置中获取）
- SMTP 服务器：smtp.qq.com:465（支持 SSL）
- 免费账户的发送频率限制为每小时约 50 封邮件
- 每封邮件的附件大小不得超过 50MB
- 所有发送的邮件都会保存在 QQ Mail 的“已发送”文件夹中