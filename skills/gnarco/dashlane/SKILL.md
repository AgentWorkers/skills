---
name: dashlane
description: 从 Dashlane 保险库中访问密码、安全笔记、机密信息以及一次性密码（OTP）代码。
homepage: https://cli.dashlane.com
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["dcli"]}}}
---

# Dashlane CLI

您可以通过命令行访问您的 Dashlane 保管库。该命令行工具支持对密码、安全笔记、机密信息和一次性密码（OTP）进行只读操作。

## 安装

```bash
brew install dashlane/tap/dashlane-cli
```

## 认证

首次同步数据以触发认证过程：
```bash
dcli sync
```

**操作步骤：**
1. 输入您的 Dashlane 电子邮件地址。
2. **⚠️ 重要提示：在浏览器中打开显示的链接**（完成设备注册）。
3. 输入通过电子邮件收到的验证码。
4. 输入您的主密码。

**查看当前账户信息：**
```bash
dcli accounts whoami
```

## 获取密码

```bash
# Search by URL or title (copies password to clipboard by default)
dcli p mywebsite
dcli password mywebsite

# Get specific field
dcli p mywebsite -f login      # Username/login
dcli p mywebsite -f email      # Email
dcli p mywebsite -f otp        # TOTP 2FA code
dcli p mywebsite -f password   # Password (default)

# Output formats
dcli p mywebsite -o clipboard  # Copy to clipboard (default)
dcli p mywebsite -o console    # Print to stdout
dcli p mywebsite -o json       # Full JSON output (all matches)

# Search by specific fields
dcli p url=example.com
dcli p title=MyBank
dcli p id=xxxxxx               # By vault ID
dcli p url=site1 title=site2   # Multiple filters (OR)
```

## 获取安全笔记

```bash
dcli note [filters]
dcli n [filters]               # Shorthand

# Filter by title (default)
dcli n my-note
dcli n title=api-keys

# Output formats: text (default), json
dcli n my-note -o json
```

## 获取机密信息

Dashlane 的“机密信息”是一种专门用于存储敏感数据的文件类型。

```bash
dcli secret [filters]

# Filter by title (default)
dcli secret api_keys
dcli secret title=api_keys -o json
```

## 其他命令

```bash
# Sync vault manually (auto-sync every hour by default)
dcli sync

# Lock the vault (requires master password to unlock)
dcli lock

# Logout completely
dcli logout

# Backup vault to current directory
dcli backup
dcli backup --directory /path/to/backup
```

## 配置

```bash
# Save master password in OS keychain (default: true)
dcli configure save-master-password true

# Disable auto-sync
dcli configure disable-auto-sync true

# Enable biometrics unlock (macOS only)
dcli configure user-presence --method biometrics

# Disable user presence check
dcli configure user-presence --method none
```

## 数据持久化方式

### macOS
默认情况下，主密码会存储在 **Keychain** 中，因此重启后数据仍然可用。
```bash
dcli configure save-master-password true
```

### Linux（服务器/无界面模式）
Linux 系统没有内置的 Keychain 功能。可选方案如下：
1. **环境变量**（安全性较低，但使用简单）：
   ```bash
   export DASHLANE_MASTER_PASSWORD="..."
   ```
2. **本地加密文件**：通过设置 `save-master-password true` 将主密码保存在 `~/.local/share/dcli/` 文件中。
3. **外部密钥管理工具**（如 Vault、AWS Secrets 等）来存储主密码。

### Docker / 持续集成（CI）环境
将 `DASHLANE_MASTER_PASSWORD` 环境变量传递给 Docker 容器。
```bash
docker run -e DASHLANE_MASTER_PASSWORD="..." myimage
```

### 单点登录（SSO）/ 无密码登录
目前 dcli 不支持这些功能——仍需要使用传统的主密码。

## 高级功能：注入机密信息

```bash
# Inject secrets into environment variables
dcli exec -- mycommand

# Inject into templated files
dcli inject < template.txt > output.txt

# Read secret by path
dcli read "dl://vault/secret-id"
```

## 示例

### 获取用于双重身份验证（2FA）的 OTP 代码
```bash
dcli p github -f otp
# Returns: 123456 (25s remaining)
```

### 从保管库中获取 SSH 密钥
将私钥保存到安全笔记中，然后执行相应操作：
```bash
dcli n SSH_KEY | ssh-add -
```

### 脚本编写
```bash
# Get password for a script
PASSWORD=$(dcli p myservice -o console)

# Get JSON and parse with jq
dcli p myservice -o json | jq -r '.[0].password'
```

## 故障排除

- **账号被锁定？** 运行 `dcli sync` 命令来解锁账号。
- **使用 SSO 的用户**：需要安装 Chrome 浏览器并使用相应的图形界面。
- **无密码登录**：目前尚不支持。
- **调试模式**：使用 `dcli --debug <命令>` 进行调试。

更多文档请访问：https://cli.dashlane.com