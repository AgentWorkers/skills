---
name: mailgun-simple
description: Send outbound emails via the Mailgun API. REQUIRED: MAILGUN_API_KEY. Built for AI Commander.
metadata: {
  "author": "Skippy & Lucas (AI Commander)",
  "homepage": "https://aicommander.dev",
  "env": {
    "MAILGUN_API_KEY": { "description": "Your private Mailgun API key. REQUIRED.", "required": true },
    "MAILGUN_DOMAIN": { "description": "Your verified sending domain (default: aicommander.dev).", "default": "aicommander.dev" },
    "MAILGUN_REGION": { "description": "The API region, either US or EU (default: EU).", "default": "EU" },
    "MAILGUN_FROM": { "description": "Default sender address (default: Postmaster <postmaster@domain>)." }
  },
  "openclaw": {
    "requires": { "bins": ["node"] },
    "install": [
      {
        "id": "npm-deps",
        "kind": "exec",
        "command": "npm install mailgun.js form-data",
        "label": "Install Mailgun SDK dependencies"
      }
    ]
  }
}
---

# Mailgun Simple

使用官方的 Mailgun JS SDK 发送出站邮件。

## 🚨 安全性与设置

此功能依赖于运行环境，**不**会加载外部的 `.env` 文件。它完全依赖于调用者提供的环境变量。

### 环境变量
- `MAILGUN_API_KEY`：您的私有 Mailgun API 密钥。**必需**。
- `MAILGUN_DOMAIN`：经过验证的发送域名（默认值：`aicommander.dev`）。
- `MAILGUN_REGION`：API 所在的区域，可以是 `US` 或 `EU`（默认值：`EU`）。

## 工具

### 发送邮件
向收件人发送纯文本邮件。
```bash
MAILGUN_API_KEY=xxx MAILGUN_DOMAIN=example.com MAILGUN_REGION=EU node scripts/send_email.js <to> <subject> <text> [from]
```

## 运行时要求
需要以下工具：`mailgun.js`、`form-data` 和 `node`。