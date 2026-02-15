---
name: sunday
description: "**代理身份提供者（Agent Identity Provider）**：支持使用代理自身的电子邮件地址以及经过端到端（E2E）加密的凭证库。该功能可用于存储或检索服务所需的密码、使用存储的凭证登录服务、查看电子邮件收件箱、通过电子邮件接收一次性密码（OTP）/验证码、注册服务、获取代理的电子邮件地址，以及任何需要代理拥有独立身份的场景（该身份与用户身份分开）。它将 `1Password` 和 `AgentMail` 的功能整合为一个统一的技能（skill），无需安装任何桌面应用程序或使用 `tmux`，实现完全自主的操作。"
metadata: {"openclaw": {"emoji": "☀️", "requires": {"bins": ["sunday"]}, "install": [{"id": "brew", "kind": "brew", "formula": "ravi-technologies/tap/sunday", "bins": ["sunday"], "label": "Install Sunday CLI via Homebrew"}]}}
---

# Sunday

为您的代理分配一个独立的身份标识——一个专用的电子邮件地址以及一个端到端加密的凭证库。所有这些功能都通过一个命令行界面（CLI）实现，无需安装任何桌面应用程序，也无需使用 `tmux` 会话或生物识别验证。只需完成一次设置后，您的代理即可完全自主运行。

## 设置（仅一次）

1. 在 [sunday.ravi.app](https://sunday.ravi.app) 上创建一个 Sunday 账户。设置您的加密 PIN 码，并创建一个身份标识（这将为您的代理提供一个独立的电子邮件地址）。

2. 安装 CLI：

```bash
brew install ravi-technologies/tap/sunday
```

3. 进行身份验证（在启动 OpenClaw 之前运行此命令）：

```bash
sunday auth login
```

系统会打开一个浏览器窗口用于登录，随后会要求您输入 6 位数的加密 PIN 码。验证通过后，您的凭证和加密密钥将被存储在 `~/.sunday/config.json` 文件中，之后无需再次输入任何信息。此后，所有与 `sunday` 相关的命令都将自动执行。

4. 验证设置是否成功：

```bash
sunday auth status
```

设置完成后，无需保持任何桌面应用程序处于打开状态，也无需使用 `tmux` 会话或环境变量。启动 OpenClaw，您的代理就拥有了独立的身份标识。

## 使用场景

- **注册服务**：在注册表单中使用您的 Sunday 电子邮件地址。
- **接收 OTP 或验证码**：查看收件箱中的邮件。
- **存储凭证**：保存您注册的服务的用户名和密码。
- **检索凭证**：在登录服务时查看已存储的密码。
- **查看邮件**：所有收到的邮件都会发送到您的代理的电子邮件地址。
- **需要使用独立身份标识的任何操作**：请勿使用用户的个人电子邮件地址。

## 您的代理身份标识

获取您的代理的独立电子邮件地址：

```bash
# Get your email address
sunday get email --json
# → {"email": "scout-a1b2c3@sunday.app"}

# Get the account owner's name
sunday get owner --json
```

在填写注册表单时，请使用此地址，而非用户的个人电子邮件地址。

## 收件箱——邮件阅读

### 统一收件箱

```bash
# All messages, newest first
sunday inbox list --json

# Only unread messages
sunday inbox list --unread --json

# Filter to email only
sunday inbox list --type email --json

# Filter by direction
sunday inbox list --direction incoming --json
```

### 邮件主题和正文

```bash
# List all email threads
sunday inbox email --json

# List only threads with unread messages
sunday inbox email --unread --json

# View a specific thread (all messages in conversation)
sunday inbox email <thread_id> --json
```

### 单个邮件

```bash
# List all email messages (flat, not grouped by thread)
sunday message email --json

# View a specific email by ID
sunday message email <message_id> --json
```

## 密码——端到端加密的凭证库

所有密码都经过端到端加密，服务器永远不会看到明文形式的凭证。解密过程在客户端完成，使用的是在首次登录时输入的 PIN 码生成的密钥。

### 注册后存储凭证

```bash
# Auto-generate a secure password and store it
sunday passwords create example.com --json
# → Generates password, stores encrypted entry, returns UUID

# Store with specific credentials
sunday passwords create example.com --username "scout-a1b2c3@sunday.app" --password "my-secret-pass" --json

# Store with notes
sunday passwords create example.com --username "me@email.com" --password "pass123" --notes "Free tier account" --json
```

输入的 URL 会自动被简化为域名格式（例如，`https://mail.google.com/inbox` 会被简化为 `google.com`）。如果未指定用户名，系统会默认使用您的 Sunday 电子邮件地址；如果未提供密码，系统会自动生成一个密码。

### 检索凭证

```bash
# List all stored passwords (shows domain and username, NOT password)
sunday passwords list --json

# Get full entry with decrypted password
sunday passwords get <uuid> --json
```

### 更新和删除凭证

```bash
# Update password
sunday passwords edit <uuid> --password "new-password" --json

# Update username
sunday passwords edit <uuid> --username "new-user@email.com" --json

# Delete entry
sunday passwords delete <uuid>
```

### 生成密码（无需存储）

```bash
# Generate a random password
sunday passwords generate --json

# Custom length
sunday passwords generate --length 24 --json

# No special characters (for sites that restrict them)
sunday passwords generate --no-special --json

# Exclude specific characters
sunday passwords generate --exclude-chars "!@#" --json
```

## 工作流程

### 注册新服务

```bash
# 1. Get your Sunday email
EMAIL=$(sunday get email --json | jq -r '.email')

# 2. Fill out the signup form with $EMAIL

# 3. Generate and store credentials
sunday passwords create theservice.com --json

# 4. Wait for verification email
sleep 10
sunday inbox list --unread --json

# 5. Extract verification link or code from email
sunday inbox email --unread --json
```

### 登录服务

```bash
# 1. Look up credentials
sunday passwords list --json
# Find the entry for the target domain

# 2. Get the full credentials
sunday passwords get <uuid> --json
# Returns decrypted username and password

# 3. If 2FA is required, check inbox for the code
sleep 5
sunday inbox list --type email --unread --json
```

### 检查 OTP 码

```bash
# After triggering a verification, wait then check
sleep 5

# Check email for verification links or codes
sunday inbox email --unread --json

# Unified check
sunday inbox list --unread --json
```

## 重要提示

- 所有命令都应使用 `--json` 选项，以确保输出格式规范且易于解析。
- 这是您的代理身份标识，而非用户的个人身份。请始终使用 `sunday get email` 命令来获取您的代理的电子邮件地址。
- 凭证信息已加密，您无法从磁盘或内存文件中直接读取原始密码。请使用 `sunday passwords get <uuid>` 命令来检索密码。
- 收件箱仅支持读取操作，您无法通过 Sunday 发送邮件。
- 令牌会自动刷新。如果遇到认证错误，请重新尝试命令；如果问题仍然存在，用户需要重新运行 `sunday auth login` 命令。