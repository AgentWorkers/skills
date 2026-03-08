---
name: ravi-identity
description: 检查 Ravi 的认证状态，并获取您的代理身份信息（电子邮件、电话号码、所有者名称）。请勿将这些信息用于阅读消息（请使用 `ravi-inbox`）、发送电子邮件（请使用 `ravi-email-send`）或获取凭证（请使用 `ravi-passwords` 或 `ravi-secrets`）。
---
# Ravi 身份管理

您可以使用 `ravi` 这个命令行工具来管理您的电话号码、电子邮件地址以及安全密钥。

## 先决条件

### 安装 `ravi` 命令行工具

如果 `ravi` 尚未安装，请指导用户进行安装：

```bash
brew install ravi-hq/tap/ravi
```

### 验证身份

在使用任何命令之前，请先验证您的身份：

```bash
ravi auth status --json
```

如果返回 `"authenticated": false`，请指导用户运行 `ravi auth login`（此操作需要浏览器支持——您无法自行完成）。

## 您的身份信息

```bash
# Your email address (use this for signups)
ravi get email --json
# → {"id": 1, "email": "janedoe@example.com", "created_dt": "..."}

# Your phone number (use this for SMS verification)
ravi get phone --json
# → {"id": 1, "phone_number": "+15551234567", "provider": "twilio", "created_dt": "..."}

# The human who owns this account
ravi get owner --json
# → {"first_name": "Jane", "last_name": "Doe"}
```

## 切换身份

`ravi` 支持多个身份。每个身份都有自己的电子邮件地址、电话号码和安全密钥。

### 查看所有身份

```bash
ravi identity list --json
```

### 为特定项目设置身份

当用户需要为某个特定项目使用不同的身份时，可以执行以下操作：
1. 查看所有身份：`ravi identity list --json`
2. 为该项目设置身份（针对该目录的覆盖设置）：
   ```bash
   # Recommended: use the CLI (handles bound tokens automatically)
   ravi identity use "<uuid>"

   # Manual fallback (identity only, no bound tokens):
   mkdir -p .ravi && echo '{"identity_uuid":"<uuid>","identity_name":"<name>"}' > .ravi/config.json
   ```
   - 将 `.ravi/` 添加到 `.gitignore` 文件中

该目录下的所有 `ravi` 命令都将使用指定的身份。

### 全局切换身份

```bash
ravi identity use "<uuid>"
```

### 创建新身份

仅在用户明确要求时创建新身份（例如，为需要独立电子邮件/电话号码的新项目）。创建新身份需要付费，并且需要一些时间来完成配置。

```bash
# Auto-generated name and email (recommended — looks like a real person)
ravi identity create --json
# → name: "Sarah Johnson", email: "sarah.johnson472@ravi.app"

# Custom name, auto-generated email
ravi identity create --name "Shopping Agent" --json

# Custom email local part (domain auto-picked)
ravi identity create --name "Work Agent" --email "shopping" --json

# Full email on a specific domain (must be a domain you have access to)
ravi identity create --email "work@acme.com" --json

# List available domains
ravi domains --json
```

如果未指定身份名称，服务器会自动生成一个合理的名字（例如 “Sarah Johnson”）。生成的电子邮件地址格式为 `sarah.johnson472@ravi.app`。

**自定义电子邮件规则：** 邮箱地址长度为 3-30 个字符，包含小写字母、数字和点（.），必须以字母或数字开头和结尾，不能连续使用点（..）或连字符（--）。如果邮箱地址已被占用，系统会返回 HTTP 409 错误。

## 重要提示

- **始终使用 `--json` 格式**——所有命令都支持该格式。人类可读的输出格式并不适用于程序解析。
- **身份验证是自动完成的**——令牌会自动更新。如果出现身份验证错误，请让用户重新登录。
- **身份配置优先级**：当前工作目录下的 `.ravi/config.json` 文件的配置会优先于 `~/.ravi/config.json` 文件的配置。
- **身份信息是永久性的**——每个身份都有自己的电子邮件地址、电话号码和安全密钥。除非用户特别要求，否则不要创建新的身份。

## 相关功能

- **ravi-inbox**：读取短信和电子邮件消息
- **ravi-email-send**：撰写、回复和转发电子邮件
- **ravi-email-writing**：以专业格式撰写电子邮件
- **ravi-contacts**：查找或管理与该身份关联的联系人
- **ravi-passwords**：存储和检索网站登录凭据（域名 + 用户名 + 密码）
- **ravi-secrets**：存储和检索键值对形式的敏感信息（API 密钥、环境变量）
- **ravi-login**：注册和登录服务，处理双重身份验证（2FA/OTP）
- **ravi-feedback**：发送反馈、报告错误、请求新功能