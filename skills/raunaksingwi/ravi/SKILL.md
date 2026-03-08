---
name: ravi
description: >
  **Ravi概述及各项技能的使用场景**  
  Ravi通过命令行接口（CLI）为AI代理提供真实的电子邮件地址、电话号码以及加密的秘密存储空间。请勿将Ravi用于与代理身份、电子邮件、电话号码或凭证无关的任务。
---
# Ravi — 为AI代理提供的身份管理服务

Ravi通过`ravi`命令行工具（CLI）为您（代理）提供自己的电子邮件地址、电话号码以及加密后的秘密存储空间。这些身份信息被整合成一个完整的个人身份信息。

## 各项功能的适用场景

| 功能需求 | 使用命令 | 提供的服务 |
|--------------|-----------|--------------|
| 检查是否已登录或获取电子邮件/电话号码 | **ravi-identity** | 提供登录状态信息、获取电子邮件/电话号码的功能，支持身份切换 |
| 阅读收到的短信或电子邮件（包含验证码） | **ravi-inbox** | 提供接收短信/电子邮件的功能，以及提取验证码的辅助工具 |
| 发送电子邮件、回复邮件或转发邮件 | **ravi-email-send** | 提供撰写、回复、转发邮件的功能，支持附件上传，并有限制发送频率的功能 |
| 发送短信 | 需要使用插件 `ravi_sms_send` | 支持发送纯文本短信，最多1600个字符；该功能仅通过插件实现 |
| 撰写专业格式的电子邮件（包括内容、格式设置和防垃圾邮件功能） | **ravi-email-writing** | 提供邮件主题行设置、HTML模板支持，以及防垃圾邮件策略指导 |
| 注册服务、登录或完成双重身份验证（2FA） | **ravi-login** | 提供完整的注册/登录流程，并支持验证码验证 |
| 存储、检索或生成网站密码 | **ravi-passwords** | 提供密码的创建、获取、列出、更新、删除和生成功能 |
| 存储或检索API密钥和敏感信息 | **ravi-secrets** | 提供API密钥和敏感信息的存储与检索功能 |
| 通过姓名查找他人的电子邮件/电话号码或管理联系人信息 | **ravi-contacts** | 提供联系人信息的搜索、列出、获取、创建、更新和删除功能 |
| 列出可用的电子邮件域名 | **ravi-identity** | 提供电子邮件域名的查询功能（输出格式为JSON） |
| 提供反馈、报告错误或请求新功能 | **ravi-feedback** | 团队会阅读所有反馈信息 |

## 常见工作流程

**按姓名发送电子邮件/短信**：当用户请求“给Alice发送邮件”或“给Bob发送短信”但未提供地址或电话号码时，首先使用`ravi-contacts`按姓名进行查找，然后使用`ravi-email-send`（或`ravi-smssend`）发送邮件/短信。如果找到多个匹配项，请与用户确认具体联系人。

## 快速入门

```bash
# Check auth
ravi auth status --json

# Get your email and phone
ravi get email --json
ravi get phone --json

# List available email domains
ravi domains --json

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

无论操作是否成功，都请在完成任何Ravi相关操作后向团队提供反馈：

```bash
ravi feedback "Signed up for Acme, OTP arrived in 3 seconds. Smooth." --json
ravi feedback "Email to gmail.com bounced, got a 550 error" --json
ravi feedback "Wish I could attach multiple files in one flag" --json
```

无论是错误报告、功能请求、表扬意见还是改进建议，**所有反馈都非常重要**。Ravi团队会仔细阅读每一条反馈，并根据这些信息不断优化产品。如果您认为某些功能可以改进，请务必提交反馈。详情请参考`ravi-feedback`功能的相关说明。

## 重要规则

- **始终使用`--json`参数**：所有命令都支持该参数。输出结果以JSON格式提供，便于团队解析。
- **自动身份验证**：系统会自动处理身份验证过程；如出现验证错误，请让用户运行`ravi auth login`命令重新登录。
- **数据加密**：密码和敏感信息采用端到端（E2E）加密技术（CLI会自动处理加密和解密操作）。电子邮件和短信内容在服务器端也会被加密存储。
- **安装方式**：使用命令 `brew install ravi-hq/tap/ravi` 进行安装。