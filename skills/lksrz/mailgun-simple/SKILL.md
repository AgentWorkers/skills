---
name: mailgun-simple
description: 通过 Mailgun API 发送出站邮件。需要使用以下参数：MAILGUN_API_KEY、MAILGUN_DOMAIN、MAILGUN_REGION 和 MAILGUN_FROM。
metadata: {"openclaw": {"requires": {"bins": ["node"], "env": ["MAILGUN_API_KEY", "MAILGUN_DOMAIN", "MAILGUN_REGION", "MAILGUN_FROM"]}, "primaryEnv": "MAILGUN_API_KEY", "install": [{"id": "npm-deps", "kind": "node", "package": "mailgun.js@12.7.0 form-data@4.0.1", "label": "Install Mailgun SDK dependencies"}]}}
---
# Mailgun Simple

使用官方的 Mailgun JS SDK 发送出站邮件。

## 环境变量

| 变量 | 是否必需 | 默认值 | 说明 |
|---|---|---|---|
| `MAILGUN_API_KEY` | 是 | — | 你的私有 Mailgun API 密钥。 |
| `MAILGUN_DOMAIN` | 是 | `aicommander.dev` | 你的已验证的发送域名。 |
| `MAILGUN_REGION` | 是 | `EU` | API 区域：`EU` 或 `US`。 |
| `MAILGUN_FROM` | 否 | `Postmaster <postmaster@{domain}>` | 默认的发件人地址。 |

## 设置

```bash
npm install mailgun.js@12.7.0 form-data@4.0.1
```

## 工具

### 发送邮件
```bash
MAILGUN_API_KEY=xxx MAILGUN_DOMAIN=example.com MAILGUN_REGION=EU node scripts/send_email.js <to> <subject> <text> [from]
```