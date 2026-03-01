---
name: mailcheck-email-verification
description: MailCheck API的电子邮件验证功能：用于验证电子邮件地址、批量处理邮件以及分析邮件内容的真实性。
---
# MailCheck 邮箱验证

使用 MailCheck API 验证电子邮件地址——提供全面的语法检查、一次性邮箱验证、DNS 检查以及 SMTP 检查功能。

## 主要功能

- **单次邮箱验证**：一次验证一个电子邮件地址。
- **批量验证**：一次请求可验证最多 100 个电子邮件地址。
- **真实性分析**：检测钓鱼邮件、欺骗行为及电子邮件欺诈。
- **风险评分**：0-100 分的评分系统，表示风险等级（低/中/高）。

## 命令

### `email-verify` - 单次验证电子邮件地址

用于验证单个电子邮件地址。

**参数：**
- `email`（必填）：需要验证的电子邮件地址。
- `api_key`（可选）：MailCheck API 密钥（默认使用 `MAILCHECK_API_KEY` 环境变量）。

**示例：**
```bash
email-verify email="user@example.com" api_key="sk_live_..."
```

### `email-bulk-verify` - 批量验证

一次请求可验证最多 100 个电子邮件地址。

**参数：**
- `emails`（必填）：电子邮件地址数组。
- `api_key`（可选）：MailCheck API 密钥。

**示例：**
```bash
email-bulk-verify emails="[user1@example.com, user2@gmail.com]" api_key="sk_live_..."
```

### `email-auth-verify` - 邮件真实性分析

分析电子邮件头部信息，检测欺骗行为、钓鱼邮件及 CEO 欺诈。

**参数：**
- `headers`（必填）：需要分析的电子邮件头部信息。
- `trusted_domains`（可选）：用于识别相似域名的可信域名。
- `api_key`（可选）：MailCheck API 密钥。

**示例：**
```bash
email-auth-verify headers="From: sender@example.com\nReceived: ..." trusted_domains="[company.com]"
```

## 环境变量

请将 `MAILCHECK_API_KEY` 设置为你的 MailCheck API 密钥，以避免在每个命令中都手动传递该密钥。

## 安装

此功能可在 [ClawHub](https://clawhub.com) 上使用。

```bash
clawhub install mailcheck-email-verification
```

## API 参考

完整 API 文档请参阅：https://api.mailcheck.dev/docs

## 代码仓库

源代码地址：https://github.com/bnuyts/mailcheck-skill

## 许可证

MIT 许可证