---
name: mailgun
description: 通过 Mailgun API 发送电子邮件。适用于需要以编程方式发送电子邮件的场景，例如发送新闻通讯、通知、警报或自动化报告等。使用此功能前，必须配置 `MAILGUN_API_KEY` 和 `MAILGUN_DOMAIN` 环境变量。
---

# Mailgun 邮件发送工具

使用 Mailgun 的 HTTP API 以编程方式发送电子邮件。

## 前提条件

在 `~/.zshrc` 或 `~/.bash_profile` 中配置以下环境变量：

```bash
export MAILGUN_API_KEY="key-xxxxx"      # Your Mailgun private API key
export MAILGUN_DOMAIN="mg.yourdomain.com"  # Your Mailgun domain
export MAILGUN_FROM="Sender <noreply@mg.yourdomain.com>"  # Default sender
export MAILGUN_DEFAULT_TO="you@email.com"  # Default recipient (optional)
```

然后重新加载 shell 配置：
```bash
source ~/.zshrc
```

## 使用方法

### 发送简单邮件

```bash
mailgun/scripts/send_email.sh "Subject" "Email body text"
```

### 发送给特定收件人

```bash
mailgun/scripts/send_email.sh "Newsletter" "Content here" "recipient@email.com"
```

### 使用自定义发件人发送邮件

```bash
mailgun/scripts/send_email.sh "Alert" "System down" "admin@company.com" "alerts@company.com"
```

## 特点

- 简单的命令行界面
- 通过环境变量进行配置
- 支持自定义发件人和收件人
- 返回成功/错误状态码
- 支持 HTML 内容（将 HTML 传递给 `body` 参数）

## 常见使用场景

- 日/周新闻通讯
- 系统警报和通知
- 自动化报告
- 确认邮件
- 定时提醒

## 故障排除

**错误：MAILGUN_API_KEY 和 MAILGUN_DOMAIN 必须设置**
→ 按照前提条件中的说明配置环境变量

**错误：401 未授权**
→ 确认您的 API 密钥是否正确且有效

**错误：404 未找到**
→ 验证您的 `MAILGUN_DOMAIN` 是否正确

## 参考资料

- Mailgun 文档：https://documentation.mailgun.com/
- API 参考：请参阅 [references/api.md](references/api.md)