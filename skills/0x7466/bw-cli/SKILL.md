---
name: bw-cli
description: 使用 `bw CLI` 与 Bitwarden 密码管理器进行交互。涵盖以下功能：  
- 认证（登录/解锁/登出/状态查询）  
- 保险库操作（列出/获取/创建/编辑/删除/恢复项目、文件夹、附件、收藏夹）  
- 密码/口令生成  
- 组织管理  
- 发送/接收密码  

相关命令示例：  
- `bitwarden`  
- `bw`  
- `password safe`  
- `vaultwarden`  
- `vault`  
- `password manager`  
- `generate password`  
- `get password`  
- `unlock vault`  
- `share send`
metadata:
  author: tfm
  version: "1.9.0"
  docs: https://bitwarden.com/help/cli/
  docs-md: https://bitwarden.com/help/cli.md
  api-key-docs: https://bitwarden.com/help/personal-api-key/
---

# Bitwarden CLI

本文档提供了通过命令行界面与 Bitwarden 交互的完整参考信息。

**官方文档：** https://bitwarden.com/help/cli/  
**Markdown 版本（适用于代理）：** https://bitwarden.com/help/cli.md

## 快速参考

### 安装

```bash
# Native executable (recommended)
# https://bitwarden.com/download/?app=cli

# npm
npm install -g @bitwarden/cli

# Linux package managers
choco install bitwarden-cli  # Windows via Chocolatey
snap install bw              # Linux via Snap
```

### 认证流程（推荐：先解锁）

**标准工作流程（先解锁）：**
```bash
# 1. Try unlock first (fast, most common case)
export BW_SESSION=$(bw unlock --passwordenv BW_PASSWORD --raw 2>/dev/null)

# 2. Only if unlock fails, fall back to login
if [ -z "$BW_SESSION" ]; then
  bw login "$BW_EMAIL" "$BW_PASSWORD"
  export BW_SESSION=$(bw unlock --passwordenv BW_PASSWORD --raw)
fi

# 3. Sync before any vault operation
bw sync

# 4. End session
bw lock                      # Lock (keep login)
bw logout                    # Complete logout
```

**替代方案：直接登录方法**
```bash
bw login                     # Interactive login (email + password)
bw login --apikey           # API key login (uses BW_CLIENTID/BW_CLIENTSECRET from .secrets)
bw login --sso              # SSO login
bw unlock                    # Interactive unlock
bw unlock --passwordenv BW_PASSWORD     # Auto-available from sourced .secrets
```

## 会话与配置命令

### status

检查认证状态和保管库状态：

```bash
bw status
```

返回值：`unauthenticated`、`locked` 或 `unlocked`。

### config

配置 CLI 设置：

```bash
# Set server (self-hosted or regional)
bw config server https://vault.example.com
bw config server https://vault.bitwarden.eu   # EU cloud
bw config server                              # Check current

# Individual service URLs
bw config server --web-vault <url> --api <url> --identity <url>
```

### sync

将本地保管库与服务器同步（在所有保管库操作前运行）：

```bash
bw sync                     # Full sync
bw sync --last             # Show last sync timestamp
```

### update

检查是否有更新（不会自动安装）：

```bash
bw update
```

### serve

启动 REST API 服务器：

```bash
bw serve --port 8087 --hostname localhost
```

## 保管库对象命令

### list

列出保管库中的对象：

```bash
# Items
bw list items
bw list items --search github
bw list items --folderid <id> --collectionid <id>
bw list items --url https://example.com
bw list items --trash                        # Items in trash

# Folders
bw list folders

# Collections
bw list collections                          # All collections
bw list org-collections --organizationid <id>  # Org collections

# Organizations
bw list organizations
bw list org-members --organizationid <id>
```

### get

检索单个值或对象：

```bash
# Get specific fields (by name or ID)
bw get password "GitHub"
bw get username "GitHub"
bw get totp "GitHub"                         # 2FA code
bw get notes "GitHub"
bw get uri "GitHub"

# Get full item JSON
bw get item "GitHub"
bw get item <uuid> --pretty

# Other objects
bw get folder <id>
bw get collection <id>
bw get organization <id>
bw get org-collection <id> --organizationid <id>

# Templates for create operations
bw get template item
bw get template item.login
bw get template item.card
bw get template item.identity
bw get template item.securenote
bw get template folder
bw get template collection
bw get template item-collections

# Security
bw get fingerprint <user-id>
bw get fingerprint me
bw get exposed <password>                    # Check if password is breached

# Attachments
bw get attachment <filename> --itemid <id> --output /path/
```

### create

创建新对象：

```bash
# Create folder
bw get template folder | jq '.name="Work"' | bw encode | bw create folder

# Create login item
bw get template item | jq \
  '.name="Service" | .login=$(bw get template item.login | jq '.username="user@example.com" | .password="secret"')' \
  | bw encode | bw create item

# Create secure note (type=2)
bw get template item | jq \
  '.type=2 | .secureNote.type=0 | .name="Note" | .notes="Content"' \
  | bw encode | bw create item

# Create card (type=3)
bw get template item | jq \
  '.type=3 | .name="My Card" | .card=$(bw get template item.card | jq '.number="4111..."')' \
  | bw encode | bw create item

# Create identity (type=4)
bw get template item | jq \
  '.type=4 | .name="My Identity" | .identity=$(bw get template item.identity)' \
  | bw encode | bw create item

# Create SSH key (type=5)
bw get template item | jq \
  '.type=5 | .name="My SSH Key"' \
  | bw encode | bw create item

# Attach file to existing item
bw create attachment --file ./doc.pdf --itemid <uuid>
```

对象类型：`1=登录信息`、`2=安全笔记`、`3=卡片`、`4=身份信息`、`5=SSH 密钥`。

### edit

修改现有对象：

```bash
# Edit item
bw get item <id> | jq '.login.password="newpass"' | bw encode | bw edit item <id>

# Edit folder
bw get folder <id> | jq '.name="New Name"' | bw encode | bw edit folder <id>

# Edit item collections
 echo '["collection-uuid"]' | bw encode | bw edit item-collections <item-id> --organizationid <id>

# Edit org collection
bw get org-collection <id> --organizationid <id> | jq '.name="New Name"' | bw encode | bw edit org-collection <id> --organizationid <id>
```

### delete

删除对象：

```bash
# Send to trash (recoverable 30 days)
bw delete item <id>
bw delete folder <id>
bw delete attachment <id> --itemid <id>
bw delete org-collection <id> --organizationid <id>

# Permanent delete (irreversible!)
bw delete item <id> --permanent
```

### restore

从回收站中恢复对象：

```bash
bw restore item <id>
```

## 密码生成

### generate

生成密码或短语：

```bash
# Password (default: 14 chars)
bw generate
bw generate --uppercase --lowercase --number --special --length 20
bw generate -ulns --length 32

# Passphrase
bw generate --passphrase --words 4 --separator "-" --capitalize --includeNumber
```

## 发送命令（安全共享）

### send

创建临时共享链接：

```bash
# Text Send
bw send -n "Secret" -d 7 --hidden "This text vanishes in 7 days"

# File Send
bw send -n "Doc" -d 14 -f /path/to/file.pdf

# Advanced options
bw send --password accesspass -f file.txt
```

### receive

接收收到的共享链接：

```bash
bw receive <url> --password <pass>
```

## 组织命令

### move

将对象共享给组织成员：

```bash
echo '["collection-uuid"]' | bw encode | bw move <item-id> <organization-id>
```

### confirm

确认被邀请的成员：

```bash
bw get fingerprint <user-id>
bw confirm org-member <user-id> --organizationid <id>
```

### device-approval

管理设备授权：

```bash
bw device-approval list --organizationid <id>
bw device-approval approve <request-id> --organizationid <id>
bw device-approval approve-all --organizationid <id>
bw device-approval deny <request-id> --organizationid <id>
bw device-approval deny-all --organizationid <id>
```

## 导入与导出

### import

从其他密码管理器导入数据：

```bash
bw import --formats                          # List supported formats
bw import lastpasscsv ./export.csv
bw import bitwardencsv ./import.csv --organizationid <id>
```

### export

导出保管库数据：

```bash
bw export                                    # CSV format
bw export --format json
bw export --format encrypted_json
bw export --format encrypted_json --password <custom-pass>
bw export --format zip                       # Includes attachments
bw export --output /path/ --raw              # Output to file or stdout
bw export --organizationid <id> --format json
```

## 实用工具

### encode

对 JSON 数据进行 Base64 编码（用于创建/修改操作）：

```bash
bw get template folder | jq '.name="Test"' | bw encode | bw create folder
```

### generate (password)

请参阅 [密码生成](#password-generation)。

### 全局选项

所有命令均支持以下全局选项：

```bash
--pretty                     # Format JSON output with tabs
--raw                        # Return raw output
--response                   # JSON formatted response
--quiet                      # No stdout (use for piping secrets)
--nointeraction             # Don't prompt for input
--session <key>             # Pass session key directly
--version                   # CLI version
--help                      # Command help
```

## 安全性参考

### 安全的密码存储（.secrets 文件）

将主密码存储在工作区的 `.secrets` 文件中，并自动加载：

```bash
# Create .secrets file
mkdir -p ~/.openclaw/workspace
echo "BW_PASSWORD=your_master_password" > ~/.openclaw/workspace/.secrets
chmod 600 ~/.openclaw/workspace/.secrets

# Add to .gitignore
echo ".secrets" >> ~/.openclaw/workspace/.gitignore

# Auto-source in shell config (run once)
echo 'source ~/.openclaw/workspace/.secrets 2>/dev/null' >> ~/.bashrc
# OR for zsh:
echo 'source ~/.openclaw/workspace/.secrets 2>/dev/null' >> ~/.zshrc
```

**现在，BW_PASSWORD 始终可用：**

```bash
bw unlock --passwordenv BW_PASSWORD
```

**安全要求：**
- 文件权限必须设置为 `600`（用户仅读/写）
- 必须将 `.secrets` 文件添加到 `.gitignore` 文件中
- 绝不要提交 `.secrets` 文件
- 新 shell 会话会自动加载密码；当前会话可运行 `source ~/.openclaw/workspace/.secrets`。

### API 密钥认证（.secrets 文件）

对于自动化操作或使用 API 密钥登录，请将凭据存储在同一 `.secrets` 文件中：

```bash
# Add API credentials to .secrets
echo "BW_CLIENTID=user.xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" >> ~/.openclaw/workspace/.secrets
echo "BW_CLIENTSECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" >> ~/.openclaw/workspace/.secrets
chmod 600 ~/.openclaw/workspace/.secrets
```

**使用 API 密钥登录：**

```bash
bw login --apikey
```

**⚠️ 已知问题/解决方法**

在某些自托管的 Vaultwarden 实例中，`bw login --apikey` 可能会失败：
```
User Decryption Options are required for client initialization
```

**解决方法 - 使用电子邮件/密码登录：**

```bash
# Add EMAIL to .secrets
echo "BW_EMAIL=your@email.com" >> ~/.openclaw/workspace/.secrets

# Login with email + password (instead of --apikey)
bw login "$BW_EMAIL" "$BW_PASSWORD"

# Or as one-liner
set -a && source ~/.openclaw/workspace/.secrets && set +a && bw login "$BW_EMAIL" "$BW_PASSWORD"

# Then unlock as usual
bw unlock --passwordenv BW_PASSWORD
```

**完整工作流程（推荐用于自托管环境）：**

```bash
# Source the .secrets file
set -a && source ~/.openclaw/workspace/.secrets && set +a

# Try unlock first (faster, works if already logged in)
export BW_SESSION=$(bw unlock --passwordenv BW_PASSWORD --raw 2>/dev/null)

# Only login if unlock failed (vault not initialized)
if [ -z "$BW_SESSION" ]; then
  bw login "$BW_EMAIL" "$BW_PASSWORD"
  export BW_SESSION=$(bw unlock --passwordenv BW_PASSWORD --raw)
fi

# Ready to use
bw sync
bw list items
```

**获取您的 API 密钥：** https://bitwarden.com/help/personal-api-key/

### 环境变量

```bash
BW_CLIENTID                  # API key client_id
BW_CLIENTSECRET              # API key client_secret
BW_PASSWORD                  # Master password for unlock
BW_SESSION                   # Session key (auto-used by CLI)
BITWARDENCLI_DEBUG=true      # Enable debug output
NODE_EXTRA_CA_CERTS          # Self-signed certs path
BITWARDENCLI_APPDATA_DIR     # Custom config directory
```

### 两步登录方法

方法值：`0=身份验证器`、`1=电子邮件`、`3=YubiKey`。

```bash
bw login user@example.com password --method 0 --code 123456
```

### URI 匹配类型

值：`0=域名`、`1=主机`、`2=以...开头`、`3=完全匹配`、`4=正则表达式`、`5=从不匹配`。

### 字段类型

值：`0=文本`、`1=隐藏`、`2=布尔值`。

### 组织用户类型

`0=所有者`、`1=管理员`、`2=用户`、`3=经理`、`4=自定义`。

### 组织用户状态

`0=被邀请`、`1=已接受`、`2=已确认`、`-1=被撤销`。

## 最佳实践

1. **先解锁，仅在需要时登录**：建议先使用 `bw unlock`，因为它更快；只有在解锁失败（保管库未初始化时）才使用 `bw login`。
2. **始终同步**：在所有保管库操作前运行 `bw sync`。
3. **保护会话**：操作完成后使用 `bw lock` 锁定会话。
4. **保护密码**：切勿记录 `BW_SESSION` 或 `BW_PASSWORD`。
5. **安全存储**：将 `.secrets` 文件的权限设置为 `600`，切勿提交该文件。
6. **自动加载设置**：将相关环境变量添加到 `~/.bashrc` 或 `~/.zshrc` 中以实现持久化。
7. **验证指纹**：在确认组织成员身份之前进行验证。

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| “检测到机器人” | 使用 `--apikey` 或提供 `client_secret` |
| “保管库被锁定” | 运行 `bw unlock` 并导出 `BW_SESSION` |
| 自签名证书错误 | 设置 `NODE_EXTRA_CA_CERTS` |
| 需要调试信息 | 设置 `export BITWARDENCLI_DEBUG=true` |

---

**参考资料：**
- HTML 文档：https://bitwarden.com/help/cli/
- Markdown 文档：https://bitwarden.com/help/cli.md
- 个人 API 密钥：https://bitwarden.com/help/personal-api-key/