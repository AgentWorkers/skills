---
name: email
description: >
  **按需电子邮件检查功能，配备AI摘要功能**  
  支持Gmail、Outlook/M365、Google Workspace以及自定义的IMAP账户。
homepage: https://clawhub.ai/skills/email
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["node"]}}}
---
# email

根据需求检查电子邮件，获取人工智能生成的摘要，并生成邮件摘要。支持通过 IMAP 和 OAuth2 连接多个账户。

## 快速入门

```bash
# 1. Configure AI (for email summaries)
node .../cli.js config ai_api_key <YOUR_DEEPSEEK_OR_OPENAI_KEY>

# 2. Add an email account
node .../cli.js setup user@gmail.com --password <APP_PASSWORD>

# 3. Check emails
node .../cli.js check --summarize
```

## 命令行接口（CLI）路径

```
node /Users/jundong/.openclaw/workspace/skills/email/cli.js <command> [options]
```

## 命令

### config — 配置 API 密钥

```bash
# Show all config
node .../cli.js config

# Set AI API key (DeepSeek, OpenAI, or any compatible API)
node .../cli.js config ai_api_key sk-xxx

# Set API base URL (default: https://api.deepseek.com)
node .../cli.js config ai_api_base https://api.openai.com/v1

# Set AI model (default: deepseek-chat)
node .../cli.js config ai_model gpt-4o-mini

# Set Microsoft OAuth2 Client ID (for Outlook/M365)
node .../cli.js config ms_client_id <CLIENT_ID>
node .../cli.js config ms_tenant_id <TENANT_ID>
```

您也可以通过带有 `EMAIL_SKILL_` 前缀的环境变量来设置配置：
- `EMAIL_SKILL.AI_API_KEY`
- `EMAIL_SKILL.AI_API_BASE`
- `EMAIL_SKILL_MS_CLIENT_ID`

### check — 检查新邮件

```bash
# Check all accounts, last 60 minutes
node .../cli.js check

# With AI summaries
node .../cli.js check --summarize

# Specific account, last 4 hours, max 5
node .../cli.js check --account user@example.com --since 240 --max 5
```

选项：
- `--max N` — 返回的最大邮件数量（默认：10）
- `--since M` — 回溯 M 分钟内的邮件（默认：60）
- `--summarize` — 为每封邮件生成人工智能摘要
- `--account EMAIL` — 筛选特定账户的邮件

### read — 读取特定邮件

```bash
node .../cli.js read <uid> [--account EMAIL]
```

返回邮件的完整内容及人工智能生成的摘要。

### digest — 生成邮件摘要

```bash
# Last 24 hours
node .../cli.js digest

# Last 8 hours
node .../cli.js digest --since 480

# Specific account
node .../cli.js digest --account user@example.com
```

返回按重要性分类的邮件摘要（紧急/重要/可忽略）。

### accounts — 列出已配置的账户

```bash
node .../cli.js accounts
```

### setup — 添加电子邮件账户

```bash
# Gmail / Google Workspace (needs App Password)
node .../cli.js setup user@gmail.com --password <APP_PASSWORD>

# Outlook / M365 with OAuth2 (interactive)
node .../cli.js setup user@outlook.com --auth oauth

# Outlook / M365 with App Password
node .../cli.js setup user@company.com --auth password --password <APP_PASSWORD>
```

### remove — 删除电子邮件账户

```bash
node .../cli.js remove user@gmail.com
```

## 输出

所有命令的输出均为 JSON 格式，便于解析。

## 设置指南

**Gmail 应用密码：**
进入 Google 账户 → 安全设置 → 两步验证 → 应用密码

**Outlook OAuth2：**
需要使用具有 `Mail.Read` 权限的 Azure AD 应用，并启用设备代码验证流程。通过配置文件设置 `ms_client_id` 和 `ms_tenant_id`。

**Outlook 应用密码：**
访问 `mysignins.microsoft.com` → 安全信息 → 添加登录方式 → 应用密码

## 数据存储

- 凭据：`skills/email/data/email.db`（SQLite 数据库）
- 配置：`skills/email/data/config.json`