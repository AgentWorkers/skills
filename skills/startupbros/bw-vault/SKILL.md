---
name: bitwarden
description: **设置并使用 Bitwarden CLI (bw)**  
Bitwarden CLI 是用于管理 Bitwarden 数据库的命令行工具，可用于安装 Bitwarden、进行身份验证（登录/解锁）以及从数据库中读取敏感信息。它支持多种身份验证方式，包括电子邮件/密码、API 密钥以及单点登录（SSO）。  

**使用方法：**  
1. **安装 Bitwarden CLI**：根据您的操作系统，从 Bitwarden 官网下载并安装相应的 CLI 工具。  
2. **身份验证**：使用 CLI 进行登录或解锁操作时，需要提供正确的用户名、密码（如果使用电子邮件/密码或 API 密钥进行身份验证）以及 SSO 凭据。  
3. **读取数据**：通过 CLI 可以方便地从 Bitwarden 数据库中检索或导出敏感信息（如密码、密钥等）。  

**示例命令：**  
- **安装 Bitwarden CLI（Linux/macOS）：**  
  ```bash
  sudo curl -o bitwarden-cli.sh https://github.com/Bitwarden/Bitwarden-CLI/releases/download/v2.1.1/bin/bitwarden-cli.sh
  chmod +x bitwarden-cli.sh
  ```

- **使用 CLI 登录 Bitwarden：**  
  ```bash
  bitwarden-cli login --username "your_username" --password "your_password"
  ```

- **使用 CLI 读取密码：**  
  ```bash
  bitwarden-cli secret list
  ```

- **使用 SSO 登录：**  
  （具体命令可能因 SSO 方案而异，通常需要提供相应的访问令牌或认证信息。）

**注意：**  
- 请确保您的 Bitwarden 数据库已正确配置，并且已启用 CLI 访问权限。  
- 在使用 CLI 时，请注意保护您的密码和敏感信息，避免在公共网络或不受信任的环境中执行敏感操作。
homepage: https://bitwarden.com/help/cli/
metadata: {"clawdbot":{"emoji":"🔒","requires":{"bins":["bw"]},"install":[{"id":"npm","kind":"npm","package":"@bitwarden/cli","bins":["bw"],"label":"Install Bitwarden CLI (npm)"},{"id":"brew","kind":"brew","formula":"bitwarden-cli","bins":["bw"],"label":"Install Bitwarden CLI (brew)"},{"id":"choco","kind":"choco","package":"bitwarden-cli","bins":["bw"],"label":"Install Bitwarden CLI (choco)"}]}}
---

# Bitwarden 命令行接口（CLI）技能

Bitwarden 的命令行接口（CLI）允许您通过编程方式完全访问您的 Bitwarden 保管库，以检索密码、安全笔记和其他机密信息。

## 工作流程要求

**重要提示：** 请始终在专用的 tmux 会话中运行 `bw` 命令。在身份验证后，所有保管库操作都需要使用会话密钥（`BW_SESSION`）。tmux 会话可以跨命令保持此环境变量的有效性。

### 必要的工作流程

1. **验证 CLI 是否已安装**：运行 `bw --version` 以确认 CLI 是否可用。
2. **创建专用 tmux 会话**：`tmux new-session -d -s bw-session`
3. **连接并登录**：在会话中运行 `bw login` 或 `bw unlock`。
4. **导出会话密钥**：解锁后，按照 CLI 的指示导出 `BW_SESSION`。
5. **执行保管库命令**：在同一会话中使用 `bw get`、`bw list` 等命令。

### 身份验证方法

| 方法 | 命令 | 使用场景 |
|--------|---------|----------|
| 邮箱/密码 | `bw login` | 交互式会话，首次设置 |
| API 密钥 | `bw login --apikey` | 自动化操作、脚本（需要单独解锁） |
| SSO | `bw login --sso` | 企业/组织账户 |

使用邮箱/密码登录 `bw login` 后，您的保管库会自动解锁。对于 API 密钥或 SSO 登录，您需要随后运行 `bw unlock` 来解密保管库。

### 会话密钥管理

`unlock` 命令会输出一个会话密钥。您**必须**将其导出：

```bash
# Bash/Zsh
export BW_SESSION="<session_key_from_unlock>"

# Or capture automatically
export BW_SESSION=$(bw unlock --raw)
```

会话密钥的有效期直到您运行 `bw lock` 或 `bw logout` 为止。它们不会在终端窗口之间持久化——因此需要使用 tmux。

## 读取机密信息

```bash
# Get password by item name
bw get password "GitHub"

# Get username
bw get username "GitHub"

# Get TOTP code
bw get totp "GitHub"

# Get full item as JSON
bw get item "GitHub"

# Get specific field
bw get item "GitHub" | jq -r '.fields[] | select(.name=="api_key") | .value'

# List all items
bw list items

# Search items
bw list items --search "github"
```

## 安全防护措施

- **切勿** 将机密信息暴露在日志、代码或用户可见的命令输出中。
- **除非绝对必要，否则** **切勿** 将机密信息写入磁盘。
- **完成保管库操作后** **务必** 使用 `bw lock` 命令。
- **建议** 直接将机密信息读取到环境变量中或通过管道传递给命令。
- 如果收到“保管库被锁定”的错误，请使用 `bw unlock` 重新登录。
- 如果收到“您未登录”的错误，请先运行 `bw login`。
- 如果系统中无法使用 tmux，请停止操作并寻求帮助。

## 环境变量

| 变量 | 用途 |
|----------|---------|
| `BW_SESSION` | 用于解密保管库的会话密钥（所有保管库命令均需此密钥） |
| `BW_CLIENTID` | API 密钥客户端 ID（用于 `--apikey` 登录） |
| `BW_CLIENTSECRET` | API 密钥客户端密钥（用于 `--apikey` 登录） |
| `BITWARDENCLI_APPDATA_DIR` | 自定义配置目录（支持多账户设置） |

## 自托管服务器

对于自托管的 Bitwarden 服务器：

```bash
bw config server https://your-bitwarden-server.com
```

## 参考文档

- [入门指南](references/get-started.md) - 安装和初始设置
- [CLI 示例](references/cli-examples.md) - 常见使用模式和高级操作