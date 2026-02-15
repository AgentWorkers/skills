---
name: email-send
description: "使用 `msmtp` 通过 SMTP 快速发送一封电子邮件，而无需打开完整的邮件客户端。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "bins": ["msmtp"] },
        "install":
          [
            {
              "id": "dnf",
              "kind": "dnf",
              "package": "msmtp",
              "bins": ["msmtp"],
              "label": "Install msmtp (dnf)",
            },
          ],
      },
  }
---

# 发送电子邮件功能

无需打开完整的Himalaya客户端，即可通过SMTP快速发送电子邮件。该功能需要`SMTP_HOST`、`SMTP_PORT`、`SMTP_USER`、`SMTP_PASS`这些环境变量。

## 发送电子邮件

发送一条简单的电子邮件：

```bash
echo "Meeting at 3pm tomorrow." | msmtp recipient@example.com
```

发送带有主题和头部的电子邮件：

```bash
printf "To: recipient@example.com\nSubject: Quick update\n\nHey, the deploy is done." | msmtp recipient@example.com
```

## 选项

- `--cc`：抄送收件人
- `--bcc`：密件抄送收件人
- `--attach <file>`：附加文件

## 安装

```bash
sudo dnf install msmtp
```