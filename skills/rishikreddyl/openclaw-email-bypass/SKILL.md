---
name: openclaw-email-bypass
description: 当传统的 SMTP 端口（25/465/587）被阻止时，可以通过 Google Apps Script 发送电子邮件。该方案具有安全性，并且可以自行托管（即无需依赖外部服务）。
homepage: https://github.com/RISHIKREDDYL/openclaw-email-bypass
metadata: {"clawdbot":{"emoji":"✉️","requires":{"bins":["python3"]},"install":[{"id":"pip","kind":"exec","command":"pip3 install requests","label":"Install python requests"}]}}
---

# OpenClaw 邮件绕过方案（SMTP 解决方案）✉️🚀

这是一个安全、模块化的工具，用于通过用户自己的私有 Google Apps Script 网页中继来绕过 **SMTP 端口限制**（端口 25、465、587）。对于托管在 DigitalOcean 或 AWS 等 VPS 环境中的代理程序来说，这非常实用。

## 🧱 问题：云服务中的 SMTP 禁限
许多云服务提供商会阻止出站 SMTP 端口的通信，以防止垃圾邮件。本方案提供了一种 **透明、免费且可自托管** 的解决方案，允许代理程序通过 HTTPS（端口 443）发送邮件。

## 🛡️ 安全审计（透明度报告）
*关于 VirusTotal 的代码分析与安全审查：*
- **完全自托管**：用户自行部署 Google Script（文件名：`assets/Code.gs`），不涉及任何第三方服务器。
- **需要身份验证**：必须配置 `GOOGLE_SCRIPT_URL` 和 `GOOGLE_SCRIPT_TOKEN` 环境变量。
- **数据传输流程**：`代理程序 -> Python 客户端 -> HTTPS (TLS) -> Google Script -> 收件人`。
- **零数据存储**：所有邮件都不会被存储在中继服务器上。

## 🚀 快速入门
1. **部署中继**：将 `assets/Code.gs` 中的代码应用于您的 Google Apps Script 项目。
2. **配置环境变量**：设置 `GOOGLE_SCRIPT_URL` 和 `GOOGLE_SCRIPT_TOKEN`。
3. **发送邮件**：
    ```bash
    python3 scripts/send_email.py "recipient@email.com" "Subject" "Message"
    ```

## 工具
### send_email
用于发送纯文本或 HTML 格式的邮件。
```bash
python3 scripts/send_email.py <recipient> <subject> <body> [html_body]
```

**参数：**
- `recipient` - 收件人邮箱地址。
- `subject` - 邮件主题。
- `body` - 纯文本内容。
- `html_body`（可选） - 格式化的 HTML 内容。

## 资源
- [部署指南](references/setup.md) - 逐步操作指南。
- [使用示例](references/examples.md) - 模板库。

---
*由 RISHIKREDDYL 创建* 🐉
*让我们携手共进。*