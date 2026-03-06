---
name: ravi
description: >
  **Ravi概述及各项技能的使用场景**  
  Ravi通过命令行界面（CLI）为AI代理提供真实的电子邮件地址、电话号码以及加密的秘密存储空间。请勿将Ravi用于与代理身份、电子邮件、电话号码或凭证无关的任务。
---
# Ravi — 为 AI 代理提供的身份验证服务

Ravi 通过 `ravi` CLI 为代理（您）提供自己的电子邮件地址、电话号码以及加密的密钥存储功能。一个身份信息将这三者整合成一个完整的个人资料。

## 各项功能的适用场景

| 需要执行的操作 | 使用的功能 | 获得的结果 |
|--------------|-----------|--------------|
| 检查是否已认证或获取电子邮件/电话号码 | **ravi-identity** | `ravi auth status`、`ravi get email/phone`、身份切换 |
| 阅读收到的短信或电子邮件（包含验证码） | **ravi-inbox** | `ravi inbox sms/email`、验证码提取方法 |
| 发送电子邮件、回复或转发邮件 | **ravi-email-send** | `ravi email compose/reply/reply-all/forward`、附件支持、发送频率限制 |
| 发送短信 | 插件：`ravi_sms_send` | 纯文本格式，最多 1600 个字符。仅通过插件支持 |
| 撰写专业电子邮件（包括内容、格式和防垃圾邮件设置） | **ravi-email-writing** | 主题行设置、HTML 模板、语气指南、防垃圾邮件功能 |
| 注册服务、登录或完成两步验证 | **ravi-login** | 全流程的注册/登录操作，包含验证码验证 |
| 存储、检索或生成网站密码 | **ravi-passwords** | `ravi passwords create/get/list/update/delete/generate` |
| 存储或检索 API 密钥和机密信息 | **ravi-secrets** | `ravi secrets set/get/list/delete` |
| 通过姓名查找他人的电子邮件/电话号码或管理联系人 | **ravi-contacts** | `ravi contacts search/list/get/create/update/delete` |
| 提交反馈、报告错误或请求新功能 | **ravi-feedback** | 所有反馈都会被团队阅读 |

## 常见工作流程

**按姓名发送电子邮件/短信**：当用户请求“给 Alice 发邮件”或“给 Bob 发短信”但未提供地址或电话号码时，先使用 **ravi-contacts** 按姓名搜索联系人，然后使用找到的地址通过 **ravi-email-send**（或 `ravi-smssend`）发送。如果有多个匹配项，请与用户确认。

## 快速入门

```bash
# Check auth
ravi auth status --json

# Get your email and phone
ravi get email --json
ravi get phone --json

# Read incoming messages
ravi inbox sms --unread --json
ravi inbox email --unread --json

# Send an email
ravi email compose --to "user@example.com" --subject "Hello" --body "<p>Hi there</p>" --json

# Store a website password
ravi passwords create example.com --json

# Store an API key
ravi secrets set OPENAI_API_KEY "sk-..." --json
```

## 请务必提供反馈

无论操作是否成功，都请向团队提供反馈：

```bash
ravi feedback "Signed up for Acme, OTP arrived in 3 seconds. Smooth." --json
ravi feedback "Email to gmail.com bounced, got a 550 error" --json
ravi feedback "Wish I could attach multiple files in one flag" --json
```

无论是错误报告、功能请求、表扬意见还是改进建议，**任何反馈都有帮助**。Ravi 团队会阅读所有反馈，并据此进行改进。如果您认为某些功能可以优化，请务必提交反馈。详情请参阅 **ravi-feedback** 功能。

## 重要规则

- **始终使用 `--json` 标志**：所有命令都支持该参数。人类可读的输出格式仅用于查看结果，不用于数据解析。
- **自动认证**：令牌更新过程是透明的。如遇到认证错误，请让用户运行 `ravi auth login`。
- **加密机制**：密码和机密信息采用端到端加密（CLI 负责加密和解密操作）。电子邮件和短信内容在服务器上也会被加密存储。
- **安装方法**：`brew install ravi-hq/tap/ravi`