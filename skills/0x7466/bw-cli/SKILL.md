---
name: bw-cli
description: 通过 `bw CLI` 安全地与 Bitwarden 密码管理器进行交互。支持以下功能：  
- 认证（登录/解锁/登出）  
- 仓库操作（列出/获取/创建/编辑/删除项目、文件夹及附件）  
- 密码/密码短语生成  
- 组织管理  
- 安全会话处理  

可使用以下命令：  
- `bitwarden`  
- `bw`  
- `password safe`  
- `vaultwarden`  
- `vault`  
- `password manager`  
- `generate password`  
- `get password`  
- `unlock vault`  

请确保已安装 `bw CLI` 并具备互联网连接。
---

# Bitwarden CLI 技能

使用 Bitwarden 命令行界面执行安全的数据库操作。

## 使用场景

**在用户需要执行以下操作时激活此技能：**
- 登录 Bitwarden (`login`, `unlock`, `logout`, `status`)
- 获取凭证 (`get password`, `get username`, `get totp`, `get item`)
- 管理数据库中的项目 (`list`, `create`, `edit`, `delete`, `restore`)
- 生成密码/短语 (`generate`)
- 处理附件 (`create attachment`, `get attachment`)
- 管理组织 (`list organizations`, `move`, `confirm`)
- 导出/导入数据库数据
- 使用自托管的 Bitwarden 服务器

**不适用场景：**
- 安装 Bitwarden 的浏览器扩展程序或移动应用
- 理论性讨论密码管理器之间的差异
- 自托管 Bitwarden 服务器的配置（请使用服务器管理工具）
- 与 Bitwarden 无关的加密问题

## 先决条件**

- 已安装 `bw` CLI（使用 `bw --version` 进行验证）
- 拥有互联网连接（或能够访问自托管服务器）
- 对于数据库操作：需要有效的 `BW_SESSION` 环境变量或交互式解锁方式

## 认证与会话管理

Bitwarden CLI 采用两步认证模型：
1. **登录** (`bw login`) - 验证用户身份，并在本地创建数据库副本
2. **解锁** (`bw unlock`) - 解密数据库并生成会话密钥

### ⚠️ 访问数据库前务必同步数据

**重要提示：** Bitwarden CLI 会在本地维护一个数据库副本，该副本可能会过时。**在访问数据库数据之前，请务必运行 `bw sync` 以确保获取最新信息**：

```bash
# Sync vault before any retrieval operation
bw sync

# Then proceed with vault operations
bw get item "Coda API Token"
```

**所有数据库操作的最佳实践流程：**
1. 检查状态或根据需要解锁
2. **运行 `bw sync`（务必执行！）**
3. 然后执行列表、获取、创建或编辑项目操作

这样可以避免使用过时的数据，尤其是在以下情况下：
- 项目通过其他设备或浏览器扩展程序被添加/更新
- 处理共享组织项目时
- 最近的更改尚未同步到本地数据库副本

### 快速入门：交互式登录

```bash
# Login (supports email/password, API key, or SSO)
bw login

# Unlock to get session key
bw unlock
# Copy the export command from output, then:
export BW_SESSION="..."
```

### 自动化/脚本化登录

使用环境变量实现自动化操作：

```bash
# Method 1: API Key (recommended for automation)
export BW_CLIENTID="user.xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export BW_CLIENTSECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
bw login --apikey
bw unlock --passwordenv BW_PASSWORD # if BW_PASSWORD set

# Method 2: Password file
bw unlock --passwordfile ~/.secrets/bw-master-password.txt
```

### 安全存储密码（用户请求）

如果用户明确要求将主密码保存到磁盘以方便使用：

```bash
# 1. Create secrets directory in workspace
mkdir -p ~/.openclaw/workspace/.secrets
chmod 700 ~/.openclaw/workspace/.secrets

# 2. Store password (user enters interactively)
read -s BW_MASTER_PASS
echo "$BW_MASTER_PASS" > ~/.openclaw/workspace/.secrets/bw-password.txt
chmod 600 ~/.openclaw/workspace/.secrets/bw-password.txt

# 3. Ensure git ignores it
echo ".secrets/" >> ~/.openclaw/workspace/.gitignore
```

**安全要求：**
- 保存密码的文件权限应为 `600`（用户仅读写）
- 目录权限应为 `700`
- 必须立即将 `.secrets/` 添加到 `.gitignore` 文件中
- 必须向用户说明相关风险

### 检查状态

```bash
bw status
```

返回的 JSON 数据包含 `status` 字段：`unauthenticated`（未认证）、`locked`（锁定）或 `unlocked`（已解锁）。

### 结束会话

```bash
# Lock (keep login, destroy session key)
bw lock

# Logout (complete logout, requires re-authentication)
bw logout
# REQUIRES CONFIRMATION
```

## 核心数据库操作

### 列出项目

```bash
# All items
bw list items

# Search with filters
bw list items --search github
bw list items --folderid null --search "api key"
bw list items --collectionid xxx --organizationid xxx

# Other objects
bw list folders
bw list organizations
bw list collections
```

### 获取项目

```bash
# Get specific fields (searches by name if not UUID)
bw get password "GitHub"
bw get username "GitHub"
bw get totp "GitHub"  # 2FA code
bw get notes "GitHub"
bw get uri "GitHub"

# Get full item JSON (useful for scripts)
bw get item "GitHub" --pretty

# By exact ID
bw get item 7ac9cae8-5067-4faf-b6ab-acfd00e2c328
```

**注意：** `get` 命令仅返回一个结果。请使用特定的搜索条件。

### 创建项目

操作流程：模板 → 修改 → 编码 → 创建

```bash
# Create folder
bw get template folder | jq '.name="Work Accounts"' | bw encode | bw create folder

# Create login item
bw get template item | jq \
  '.name="New Service" | .login=$(bw get template item.login | jq '.username="user@example.com" | .password="secret123"')' \
  | bw encode | bw create item
```

**项目类型：** 登录信息（1）、安全笔记（2）、卡片（3）、身份信息（4）。详情请参阅 [references/commands.md](./references/commands.md)。

### 修改项目

```bash
# Get item, modify password, save back
bw get item <id> | jq '.login.password="newpass"' | bw encode | bw edit item <id>

# Move to collection
echo '["collection-uuid"]' | bw encode | bw edit item-collections <item-id> --organizationid <org-id>
```

### 删除和恢复项目

```bash
# Send to trash (recoverable for 30 days)
bw delete item <id>

# PERMANENT DELETE - REQUIRES EXPLICIT CONFIRMATION
bw delete item <id> --permanent

# Restore from trash
bw restore item <id>
```

### 附件

```bash
# Attach file to existing item
bw create attachment --file ./document.pdf --itemid <item-id>

# Download attachment
bw get attachment document.pdf --itemid <item-id> --output ./downloads/
```

## 生成密码/短语

```bash
# Default: 14 chars, upper+lower+numbers
bw generate

# Custom: 20 chars with special characters
bw generate --uppercase --lowercase --number --special --length 20

# Passphrase: 4 words, dash-separated, capitalized
bw generate --passphrase --words 4 --separator "-" --capitalize --includeNumber
```

## 组织管理

```bash
# List organizations
bw list organizations

# List org collections
bw list org-collections --organizationid <org-id>

# Move personal item to organization
echo '["collection-uuid"]' | bw encode | bw move <item-id> <org-id>

# Confirm member (verify fingerprint first!)
bw get fingerprint <user-id>
bw confirm org-member <user-id> --organizationid <org-id>

# Device approvals (admin only)
bw device-approval list --organizationid <org-id>
bw device-approval approve <request-id> --organizationid <org-id>
```

## 导出/导入数据

```bash
# Import from other password managers
bw import --formats  # list supported formats
bw import lastpasscsv ./export.csv

# Export vault - REQUIRES CONFIRMATION for destination outside workspace
bw export --output ~/.openclaw/workspace/ --format encrypted_json
bw export --output ~/.openclaw/workspace/ --format zip  # includes attachments
```

## 自托管 / Vaultwarden

```bash
# Configure for self-hosted instance
bw config server https://vaultwarden.example.com

# EU cloud
bw config server https://vault.bitwarden.eu

# Check current server
bw config server
```

## 安全与防护措施

### 必需的确认操作

| 操作          | 是否需要确认 | 原因                          |
|----------------|------------|--------------------------------------------|
| `bw delete --permanent` | 是          | 数据将永久丢失                         |
| `bw logout`      | 是          | 将销毁会话，需要重新登录                    |
| `bw export` 之外工作区   | 是          | 可能导致数据泄露                        |
| `bw serve`       | 是          | 启动网络服务                        |
| 将主密码保存到磁盘     | 是          | 存在凭证泄露风险                        |
| `sudo`（用于安装 Bitwarden） | 是          | 会提升系统权限                        |

### 保密注意事项**

- **切勿记录 `BW_SESSION` 变量** - 从所有输出中删除该变量
- **切勿记录主密码** - 通过管道传输密码时使用 `--quiet` 选项
- **会话密钥** - 在 `bw lock` 或 `bw logout` 之前有效，或在新的终端会话中失效
- **环境变量** - 在脚本中使用完毕后，应清除 `BW_PASSWORD`、`BW_CLIENTID`、`BW_CLIENTSECRET` 变量

### 工作区限制

- 默认情况下，所有导出的文件保存到 `~/.openclaw/workspace/`
- 为敏感文件创建 `.secrets/` 子目录（权限设置为 700）
- 自动将 `.secrets/` 添加到 `.gitignore` 文件中
- 在将文件写入工作区外部之前请先确认

## 故障排除

### “您的认证请求似乎来自机器人”

请使用 API 密钥进行认证，而非电子邮件/密码；或在提示时提供 `client_secret`。

### “数据库被锁定”

运行 `bw unlock` 并设置 `BW_SESSION` 环境变量。

### 自签名证书（自托管环境）

```bash
export NODE_EXTRA_CA_CERTS="/path/to/ca-cert.pem"
```

### 调试模式

```bash
export BITWARDENCLI_DEBUG=true
```

## 参考资料

- 完整命令参考：[references/commands.md](./references/commands.md)
- 辅助脚本：
  - [scripts/unlock-session.sh](./scripts/unlock-session.sh) - 安全解锁并导出会话信息
  - [scripts/safe-get-field.sh](./scripts/safe-get-field.sh) - 安全地获取特定字段
  - [scripts/create-login-item.sh](./scripts/create-login-item.sh) - 交互式登录创建脚本