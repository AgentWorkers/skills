---
name: ravi-identity
description: 检查 Ravi 的授权状态，并获取您的代理身份信息（电子邮件、电话号码、所有者名称）。请勿使用这些信息来阅读消息（请使用 `ravi-inbox`）、发送电子邮件（请使用 `ravi-email-send`），或获取凭据（请使用 `ravi-passwords` 或 `ravi-vault`）。
---
# Ravi 身份管理

您可以使用 `ravi` 这个命令行工具来管理自己的电话号码、电子邮件地址以及凭证库（credential vault）。

## 先决条件

### 安装 `ravi` 命令行工具

如果 `ravi` 尚未安装，请提示用户进行安装：

```bash
brew install ravi-hq/tap/ravi
```

### 验证身份

在使用任何命令之前，请先验证您的身份是否已经登录：

```bash
ravi auth status --json
```

如果验证结果显示 `"authenticated": false`，请提示用户运行 `ravi auth login`（此操作需要浏览器支持，您无法自行完成）。

## 您的身份信息

```bash
# Your email address (use this for signups)
ravi get email --json
# → {"id": 1, "email": "janedoe@ravi.app", "created_dt": "..."}

# Your phone number (use this for SMS verification)
ravi get phone --json
# → {"id": 1, "phone_number": "+15551234567", "provider": "twilio", "created_dt": "..."}

# The human who owns this account
ravi get owner --json
# → {"first_name": "Jane", "last_name": "Doe"}
```

## 切换身份

`ravi` 支持多个身份。每个身份都有自己的电子邮件地址、电话号码和凭证库。

### 列出所有身份

```bash
ravi identity list --json
```

### 为当前项目设置特定身份

当用户需要为某个特定项目使用不同的身份时，可以执行以下操作：
1. 列出所有身份：`ravi identity list --json`
2. 为当前项目设置身份（通过修改目录配置文件）：
   - 创建一个名为 `.ravi` 的目录：`mkdir -p .ravi`
   - 在该目录中创建配置文件 `config.json`：`echo '{"identity_uuid":"<uuid>","identity_name":"<name>"}' > .ravi/config.json`
   - 将 `.ravi/` 添加到 `.gitignore` 文件中，以避免版本控制系统的干扰
   - 之后，该目录下的所有 `ravi` 命令都将使用指定的身份信息。

### 全局切换身份

```bash
ravi identity use "<name-or-uuid>"
```

### 创建新身份

只有在用户明确要求的情况下，才创建新身份（例如，为需要独立身份信息的独立项目）。创建新身份需要付费，并且需要一些时间来完成配置。

```bash
ravi identity create --name "Project Name" --json
```

## 重要说明

- **始终使用 `--json` 参数**：所有 `ravi` 命令都支持该参数。以人类可读格式输出的命令结果并不适合进一步处理。
- **身份验证是自动完成的**：令牌会自动更新。如果出现身份验证错误，请让用户重新登录。
- **身份配置优先级**：当前工作目录下的 `./ravi/config.json` 文件的配置优先于 `~/.ravi/config.json` 文件的配置。
- **身份信息是永久性的**：每个身份都有独立的电子邮件地址、电话号码和凭证库。除非用户有特殊需求，否则不要创建新的身份。

## 相关功能

- **ravi-inbox**：用于读取短信和电子邮件消息
- **ravi-email-send**：用于撰写、回复和转发电子邮件
- **ravi-email-writing**：用于编写格式正确、语气专业的电子邮件
- **ravi-passwords**：用于存储和检索网站登录凭证（域名、用户名和密码）
- **ravi-vault**：用于存储和检索键值对形式的敏感信息（如 API 密钥、环境变量）
- **ravi-login**：用于注册和登录服务，并处理双重身份验证（2FA/OTP）流程
- **ravi-feedback**：用于发送反馈、报告问题或请求新功能