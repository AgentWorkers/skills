---
name: aliyun-mail
description: 一种通过阿里云企业邮箱服务发送电子邮件的技能，支持使用 Markdown 格式、HTML 文本、附件，以及对代码块进行语法高亮显示的功能。
---

# 阿里云邮件技能（Aliyun Mail Skill）

该技能支持通过阿里云企业邮件服务发送电子邮件，具备多种高级功能，包括Markdown格式转换、HTML样式渲染、文件附件支持以及对代码块的语法高亮显示。

## 主要功能
- **阿里云企业邮件服务支持**：专为阿里云的SMTP服务（smtp.mxhichina.com）优化设计
- **多种内容类型**：支持发送纯文本邮件、Markdown格式邮件或HTML格式邮件
- **带语法高亮的Markdown邮件**：能够自动对Markdown中的代码块进行语法高亮显示
- **文件附件**：可以附加一个或多个文件
- **基于配置文件的安全认证**：使用加密的配置文件来存储SMTP凭据
- **错误处理**：具备重试机制和详细的错误报告功能

## 使用前提
- **需要创建SMTP配置文件**：在OpenClaw的配置目录（`/root/.openclaw/`）下创建`aliyun-mail-config.json`文件

**配置文件示例：**
```json
{
  "server": "smtp.mxhichina.com",
  "port": 465,
  "username": "your-email@yourdomain.com",
  "password": "your-app-password",
  "emailFrom": "your-email@yourdomain.com",
  "useTLS": true
}
```

**配置文件的安全性注意事项：**
确保配置文件具有适当的权限设置，以防止未经授权的访问。

## 使用方法

### 发送纯文本邮件
```bash
aliyun-mail send --to "recipient@example.com" --subject "Hello" --body "This is a plain text email"
```

### 发送带语法高亮的Markdown邮件
```bash
aliyun-mail send \
  --to "recipient@example.com" \
  --subject "Code Report" \
  --body "**Check out this Python code:**\n\n```
python
print('Hello World')
```
```
--markdown
```

```

### HTML Email with Attachment
```
bash
aliyun-mail send \
  --to "recipient@example.com" \
  --subject "每周报告" \
  --body "<h1>每周报告</h1><p>请查看附件。</p>" \
  --html \
  --attachments "/path/to/report.pdf"
```

```

### Using Body from File
```
bash
aliyun-mail send \
  --to "recipient@example.com" \
  --subject "来自文件的报告" \
  --body-file "/path/to/report.md" \
  --markdown \
  --attachments "/path/to/data.csv"
```

## 命令行参数
- `--to`：收件人电子邮件地址（必填）
- `--subject`：邮件主题（必填）
- `--body`：邮件正文内容（如果未指定`--body-file`参数，则必须提供）
- `--body-file`：包含邮件正文的文件路径
- `--html`：以HTML格式发送邮件（默认为纯文本）
- `--markdown`：以Markdown格式发送邮件，并对代码块进行语法高亮显示
- `--attachments`：以空格分隔的文件路径列表，用于附加文件

## 错误处理
该工具具备强大的错误处理机制，失败时会尝试最多3次重试。对于网络问题、认证错误或无效的电子邮件地址，系统会生成详细的错误报告。

## 安全提示
- 请使用专门为该工具设置的密码，而非您的个人邮箱密码
- 确保配置文件的安全性，设置适当的文件权限
- 绝不要将配置文件提交到版本控制系统中

## 未来改进计划
- 支持抄送/密送（CC/BCC）功能
- 邮件模板系统
- 定时发送邮件功能
- 集成丰富的文本编辑器功能