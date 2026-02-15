---
name: proton-pass
description: 管理 Proton Pass 的保管库（vault）中的项目（包括登录信息、SSH 密钥、别名、备注等），以及密码的存储和安全管理。支持与 Proton Pass 集成，实现密码管理、SSH 密钥存储、秘密数据注入（使用秘密信息执行命令、将秘密数据注入模板中）、环境变量配置等功能。此外，还提供保管库/项目的创建、读取、更新和删除（CRUD）操作、成员管理、SSH 代理配置、一次性密码（TOTP）生成、秘密数据引用（格式为 `pass://vault/item/field`）、模板注入以及使用秘密信息执行命令等功能。
---

# Proton Pass CLI

Proton Pass CLI 提供了全面的密码和秘密管理功能，支持管理密码库、项目、SSH 密钥、共享凭证、注入秘密以及与 SSH 工作流程的集成。

## 安装

### 快速安装

macOS/Linux:
```bash
curl -fsSL https://proton.me/download/pass-cli/install.sh | bash
```

Windows:
```powershell
Invoke-WebRequest -Uri https://proton.me/download/pass-cli/install.ps1 -OutFile install.ps1; .\install.ps1
```

### Homebrew (macOS)

```bash
brew install protonpass/tap/pass-cli
```

**注意：** 包管理器（如 Homebrew）不支持 `pass-cli update` 命令，也无法切换版本。

### 验证安装

```bash
pass-cli --version
```

## 认证

### 网页登录（推荐）

支持所有登录方式的默认认证方法（包括 SSO 和 U2F）：

```bash
pass-cli login
# Open the URL displayed in your browser and complete authentication
```

### 交互式登录

基于终端的认证方式（支持密码 + TOTP，但不支持 SSO 或 U2F）：

```bash
pass-cli login --interactive user@proton.me
```

#### 自动化所需的环境变量

```bash
# Credentials as plain text (less secure)
export PROTON_PASS_PASSWORD='your-password'
export PROTON_PASS_TOTP='123456'
export PROTON_PASS_EXTRA_PASSWORD='your-extra-password'

# Or from files (more secure)
export PROTON_PASS_PASSWORD_FILE='/secure/password.txt'
export PROTON_PASS_TOTP_FILE='/secure/totp.txt'
export PROTON_PASS_EXTRA_PASSWORD_FILE='/secure/extra-password.txt'

pass-cli login --interactive user@proton.me
```

### 验证会话

```bash
pass-cli info          # Show session info
pass-cli test          # Test connection
```

### 注销

```bash
pass-cli logout        # Normal logout
pass-cli logout --force  # Force local cleanup if remote fails
```

## 密码库管理

### 列出密码库

```bash
pass-cli vault list
pass-cli vault list --output json
```

### 创建密码库

```bash
pass-cli vault create --name "Vault Name"
```

### 更新密码库

```bash
# By share ID
pass-cli vault update --share-id "abc123def" --name "New Name"

# By name
pass-cli vault update --vault-name "Old Name" --name "New Name"
```

### 删除密码库

⚠️ **警告：** 删除密码库及其所有内容将不可恢复。

```bash
# By share ID
pass-cli vault delete --share-id "abc123def"

# By name
pass-cli vault delete --vault-name "Old Vault"
```

### 共享密码库

```bash
# Share with viewer access (default)
pass-cli vault share --share-id "abc123def" colleague@company.com

# Share with specific role
pass-cli vault share --vault-name "Team Vault" colleague@company.com --role editor

# Roles: viewer, editor, manager
```

### 管理密码库成员

```bash
# List members
pass-cli vault member list --share-id "abc123def"
pass-cli vault member list --vault-name "Team Vault" --output json

# Update member role
pass-cli vault member update --share-id "abc123def" --member-share-id "member123" --role editor

# Remove member
pass-cli vault member remove --share-id "abc123def" --member-share-id "member123"
```

### 转移密码库所有权

```bash
pass-cli vault transfer --share-id "abc123def" "member_share_id_xyz"
pass-cli vault transfer --vault-name "My Vault" "member_share_id_xyz"
```

## 项目管理

### 列出项目

```bash
# List from specific vault
pass-cli item list "Vault Name"
pass-cli item list --share-id "abc123def"

# List with default vault (if configured)
pass-cli item list
```

### 查看项目

```bash
# By IDs
pass-cli item view --share-id "abc123def" --item-id "item456"

# By names
pass-cli item view --vault-name "MyVault" --item-title "MyItem"

# Using Pass URI
pass-cli item view "pass://abc123def/item456"
pass-cli item view "pass://MyVault/MyItem"

# View specific field
pass-cli item view "pass://abc123def/item456/password"
pass-cli item view --share-id "abc123def" --item-id "item456" --field "username"

# Output format
pass-cli item view --share-id "abc123def" --item-id "item456" --output json
```

### 创建登录项目

```bash
# Basic login
pass-cli item create login \
  --share-id "abc123def" \
  --title "GitHub Account" \
  --username "myuser" \
  --password "mypassword" \
  --url "https://github.com"

# With vault name
pass-cli item create login \
  --vault-name "Personal" \
  --title "Account" \
  --username "user" \
  --email "user@example.com" \
  --url "https://example.com"

# With generated password
pass-cli item create login \
  --share-id "abc123def" \
  --title "New Account" \
  --username "myuser" \
  --generate-password \
  --url "https://example.com"

# Custom password generation: "length,uppercase,symbols"
pass-cli item create login \
  --vault-name "Work" \
  --title "Secure Account" \
  --username "myuser" \
  --generate-password="20,true,true" \
  --url "https://example.com"

# Generate passphrase
pass-cli item create login \
  --share-id "abc123def" \
  --title "Account" \
  --username "user" \
  --generate-passphrase="5" \
  --url "https://example.com"
```

#### 登录模板

```bash
# Get template structure
pass-cli item create login --get-template > template.json

# Create from template
pass-cli item create login --from-template template.json --share-id "abc123def"

# Create from stdin
echo '{"title":"Test","username":"user","password":"pass","urls":["https://test.com"]}' | \
  pass-cli item create login --share-id "abc123def" --from-template -
```

模板格式：
```json
{
  "title": "Item Title",
  "username": "optional_username",
  "email": "optional_email@example.com",
  "password": "optional_password",
  "urls": ["https://example.com", "https://app.example.com"]
}
```

### 创建 SSH 密钥项目

#### 生成新的 SSH 密钥

```bash
# Generate Ed25519 key (recommended)
pass-cli item create ssh-key generate \
  --share-id "abc123def" \
  --title "GitHub Deploy Key"

# Using vault name
pass-cli item create ssh-key generate \
  --vault-name "Development Keys" \
  --title "GitHub Deploy Key"

# Generate RSA 4096 key with comment
pass-cli item create ssh-key generate \
  --share-id "abc123def" \
  --title "Production Server" \
  --key-type rsa4096 \
  --comment "prod-server-deploy"

# Key types: ed25519 (default), rsa2048, rsa4096

# With passphrase protection
pass-cli item create ssh-key generate \
  --share-id "abc123def" \
  --title "Secure Key" \
  --password

# Passphrase from environment
PROTON_PASS_SSH_KEY_PASSWORD="my-passphrase" \
  pass-cli item create ssh-key generate \
  --share-id "abc123def" \
  --title "Automated Key" \
  --password
```

#### 导入现有的 SSH 密钥

```bash
# Import unencrypted key
pass-cli item create ssh-key import \
  --from-private-key ~/.ssh/id_ed25519 \
  --share-id "abc123def" \
  --title "My SSH Key"

# Import with vault name
pass-cli item create ssh-key import \
  --from-private-key ~/.ssh/id_rsa \
  --vault-name "Personal Keys" \
  --title "Old RSA Key"

# Import passphrase-protected key (will prompt)
pass-cli item create ssh-key import \
  --from-private-key ~/.ssh/id_ed25519 \
  --share-id "abc123def" \
  --title "Protected Key" \
  --password

# Passphrase from environment
PROTON_PASS_SSH_KEY_PASSWORD="my-key-passphrase" \
  pass-cli item create ssh-key import \
  --from-private-key ~/.ssh/id_ed25519 \
  --share-id "abc123def" \
  --title "Automated Import" \
  --password
```

**建议：** 在导入受密码保护的密钥时，建议先删除密码，因为密钥将在密码库中被加密。

```bash
# Create unencrypted copy
cp ~/.ssh/id_ed25519 /tmp/id_ed25519_temp
ssh-keygen -p -f /tmp/id_ed25519_temp -N ""

# Import
pass-cli item create ssh-key import \
  --from-private-key /tmp/id_ed25519_temp \
  --share-id "abc123def" \
  --title "My SSH Key"

# Securely delete temp copy
shred -u /tmp/id_ed25519_temp  # Linux
rm -P /tmp/id_ed25519_temp     # macOS
```

### 创建电子邮件别名

```bash
# Create alias
pass-cli item alias create --share-id "abc123def" --prefix "newsletter"
pass-cli item alias create --vault-name "Personal" --prefix "shopping"

# With JSON output
pass-cli item alias create --vault-name "Personal" --prefix "temp" --output json
```

### 更新项目

```bash
# Update single field
pass-cli item update \
  --share-id "abc123def" \
  --item-id "item456" \
  --field "password=newpassword123"

# By vault name and item title
pass-cli item update \
  --vault-name "Personal" \
  --item-title "GitHub Account" \
  --field "password=newpassword123"

# Update multiple fields
pass-cli item update \
  --share-id "abc123def" \
  --item-id "item456" \
  --field "username=newusername" \
  --field "password=newpassword" \
  --field "email=newemail@example.com"

# Rename item
pass-cli item update \
  --vault-name "Work" \
  --item-title "Old Title" \
  --field "title=New Title"

# Create/update custom fields
pass-cli item update \
  --share-id "abc123def" \
  --item-id "item456" \
  --field "api_key=sk_live_abc123" \
  --field "environment=production"
```

**注意：** 项目更新不支持 TOTP 或时间字段。请使用其他 Proton Pass 客户端进行这些操作。

### 删除项目

⚠️ **警告：** 删除项目将不可恢复。

```bash
pass-cli item delete --share-id "abc123def" --item-id "item456"
```

### 共享项目

```bash
# Share with viewer access (default)
pass-cli item share --share-id "abc123def" --item-id "item456" colleague@company.com

# Share with editor access
pass-cli item share --share-id "abc123def" --item-id "item456" colleague@company.com --role editor
```

### 生成 TOTP 代码

```bash
# Generate all TOTPs for an item
pass-cli item totp "pass://TOTP vault/WithTOTPs"

# Specific TOTP field
pass-cli item totp "pass://TOTP vault/WithTOTPs/TOTP 1"

# JSON output
pass-cli item totp "pass://TOTP vault/WithTOTPs" --output json

# Extract specific value
pass-cli item totp "pass://TOTP vault/WithTOTPs/TOTP 1" --output json | jq -r '.["TOTP 1"]'
```

## 密码生成与分析

### 生成密码

```bash
# Random password (default settings)
pass-cli password generate random

# Custom random password
pass-cli password generate random --length 20 --numbers true --uppercase true --symbols true

# Simple password without symbols
pass-cli password generate random --length 16 --symbols false

# Generate passphrase
pass-cli password generate passphrase

# Custom passphrase
pass-cli password generate passphrase --count 5
pass-cli password generate passphrase --count 4 --separator hyphens
pass-cli password generate passphrase --count 4 --capitalize true --numbers true
```

### 分析密码强度

```bash
# Score a password
pass-cli password score "mypassword123"

# JSON output
pass-cli password score "MySecureP@ssw0rd*" --output json
```

示例 JSON 输出：
```json
{
  "numeric_score": 51.666666666666664,
  "password_score": "Vulnerable",
  "penalties": [
    "ContainsCommonPassword",
    "Consecutive"
  ]
}
```

## SSH 代理集成

### 将 Proton Pass SSH 密钥加载到现有代理中

将 Proton Pass 的 SSH 密钥加载到现有的 SSH 代理中：

```bash
# Load all SSH keys
pass-cli ssh-agent load

# Load from specific vault
pass-cli ssh-agent load --share-id MY_SHARE_ID
pass-cli ssh-agent load --vault-name MySshKeysVault
```

**前提条件：** 确保 `SSH_AUTH_SOCK` 环境变量已定义。

### 以 SSH 代理的方式运行 Proton Pass CLI

将 Proton Pass CLI 作为独立的 SSH 代理运行：

```bash
# Start agent
pass-cli ssh-agent start

# From specific vault
pass-cli ssh-agent start --share-id MY_SHARE_ID
pass-cli ssh-agent start --vault-name MySshKeysVault

# Custom socket path
pass-cli ssh-agent start --socket-path /custom/path/agent.sock

# Custom refresh interval (default 3600 seconds)
pass-cli ssh-agent start --refresh-interval 7200  # 2 hours
```

运行后，导出代理的套接字：
```bash
export SSH_AUTH_SOCK=/Users/youruser/.ssh/proton-pass-agent.sock
```

#### 自动创建 SSH 密钥项目（v1.3.0 及更高版本）

通过 `ssh-add` 命令添加的 SSH 密钥会自动保存：

```bash
# Enable auto-creation
pass-cli ssh-agent start --create-new-identities MySshKeysVault

# In another terminal
export SSH_AUTH_SOCK=$HOME/.ssh/proton-pass-agent.sock
ssh-add ~/.ssh/my_new_key
# Key is now automatically saved to Proton Pass!
```

### SSH 故障排除

#### 当使用多个密钥时 `ssh-copy-id` 失败

强制使用密码认证：
```bash
ssh-copy-id -o PreferredAuthentications=password -o PubkeyAuthentication=no user@server
```

## Pass URI 语法（秘密引用）

使用以下格式引用秘密：`pass://vault/item/field`

### 语法

```
pass://<vault-identifier>/<item-identifier>/<field-name>
```

- **vault-identifier：** 密码库的共享 ID 或名称
- **item-identifier：** 项目的 ID 或标题
- **field-name：** 需要检索的特定字段

### 示例

```bash
# By names
pass://Work/GitHub Account/password
pass://Personal/Email Login/username

# By IDs
pass://AbCdEf123456/XyZ789/password
pass://ShareId123/ItemId456/api_key

# Mixed (vault by name, item by ID)
pass://Work/XyZ789/password

# Custom fields (case-sensitive)
pass://Work/API Keys/api_key
pass://Production/Database/connection_string
```

### 常见字段

- `username` - 用户名/登录名
- `password` - 密码
- `email` - 电子邮件地址
- `url` - 网站 URL
- `note` - 附加说明
- `totp` - TOTP 密码（用于双因素认证）
- 自定义字段（名称任意）

### 规则

- 三个组成部分（vault/item/field）都是必需的
- 名称中可以包含空格
- 名称区分大小写
- 如果存在重复项，使用第一个匹配项（为了准确性）

**无效格式：**
```bash
pass://vault/item              # Missing field name
pass://vault/item/             # Trailing slash
pass://vault/                  # Missing item and field
```

## 秘密注入

### 使用 Proton Pass 中的秘密执行命令（`run`）

使用 Proton Pass 中的秘密作为环境变量来执行命令。

**概述：**
```bash
pass-cli run [--env-file FILE]... [--no-masking] -- COMMAND [ARGS...]
```

**工作原理：**
1. 从当前进程和 `.env` 文件中收集环境变量
2. 检查变量值中是否包含 `pass://` 格式的 URI
3. 从 Proton Pass 中获取相应的秘密
4. 用实际的秘密值替换 URI
5. 在输出中隐藏秘密（除非指定了 `--no-masking`）
6. 使用处理后的环境变量执行命令
7. 将标准输入/输出/标准错误和信号（SIGTERM/SIGINT）传递给命令

**参数：**
- `--env-file FILE` - 从 `.env` 文件中加载环境变量（可以指定多个文件，按顺序处理）
- `--no-masking` - 禁用输出中的秘密隐藏功能
- `COMMAND [ARGS...]` - 要执行的命令（必须放在 `--` 之后）

#### 基本用法

```bash
# Set secret reference in environment
export DB_PASSWORD='pass://Production/Database/password'

# Run application with injected secret
pass-cli run -- ./my-app
```

#### 使用 `.env` 文件

创建 `.env` 文件：
```bash
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=admin
DB_PASSWORD=pass://Production/Database/password
API_KEY=pass://Work/External API/api_key
```

执行命令：
```bash
pass-cli run --env-file .env -- ./my-app

# Multiple env files (later override earlier)
pass-cli run \
  --env-file base.env \
  --env-file secrets.env \
  --env-file local.env \
  -- ./my-app
```

#### 在单个值中包含多个秘密

```bash
# Mix secrets with plain text
DATABASE_URL="postgresql://user:pass://vault/db/password@localhost/db"
API_ENDPOINT="https://api.example.com?key=pass://vault/api/key"
```

#### 秘密隐藏

**默认设置（隐藏秘密）：**
```bash
pass-cli run -- ./my-app
# If app logs: API_KEY: sk_live_abc123
# Output shows: API_KEY: <concealed by Proton Pass>
```

**显示秘密：**
```bash
pass-cli run --no-masking -- ./my-app
```

#### 带参数执行命令

```bash
pass-cli run -- ./my-app --config production --verbose
```

#### 集成到持续集成/持续部署（CI/CD）流程中

```bash
#!/bin/bash
# Load production secrets
pass-cli run --env-file .env.production -- ./deploy.sh
```

### 将秘密注入模板（`inject`）

使用 Handlebars 风格的语法处理模板文件，并将秘密引用替换为实际值。

**概述：**
```bash
pass-cli inject [--in-file FILE] [--out-file FILE] [--force] [--file-mode MODE]
```

**工作原理：**
1. 从 `--in-file` 或标准输入读取模板文件
2. 查找 `{{ pass://vault/item/field }}` 模式
3. 从 Proton Pass 中获取相应的秘密
4. 用实际值替换模板中的引用
5. 将结果输出到 `--out-file` 或标准输出
6. 设置文件的权限（Unix 环境）

**参数：**
- `--in-file`, `-i` - 模板文件的路径（或标准输入）
- `--out-file`, `-o` - 输出文件的路径（或标准输出）
- `--force`, `-f` - 不提示地覆盖输出文件
- `--file-mode` - 设置文件的权限（Unix，默认为 `0600`）

#### 模板语法

**注意：** 使用双大括号 `{{ }}`（与 `run` 命令使用的简单 `pass://` 不同）

```yaml
# config.yaml.template
database:
  host: localhost
  username: {{ pass://Production/Database/username }}
  password: {{ pass://Production/Database/password }}

api:
  key: {{ pass://Work/API Keys/api_key }}
  secret: {{ pass://Work/API Keys/secret }}

# This comment with pass://fake/uri is ignored
# Only {{ }} wrapped references are processed
```

#### 将秘密输出到标准输出

```bash
pass-cli inject --in-file config.yaml.template
```

#### 将秘密写入文件

```bash
pass-cli inject \
  --in-file config.yaml.template \
  --out-file config.yaml

# Overwrite existing
pass-cli inject \
  --in-file config.yaml.template \
  --out-file config.yaml \
  --force
```

#### 从标准输入读取

```bash
cat template.txt | pass-cli inject

# Or with heredoc
pass-cli inject << EOF
{
  "database": {
    "password": "{{ pass://Production/Database/password }}"
  }
}
EOF
```

#### 自定义文件权限

```bash
pass-cli inject \
  --in-file template.txt \
  --out-file config.txt \
  --file-mode 0644
```

#### JSON 模板示例

```json
{
  "database": {
    "host": "localhost",
    "password": "{{ pass://Production/Database/password }}"
  },
  "api": {
    "key": "{{ pass://Work/API/key }}"
  }
}
```

## 设置管理

配置持久化的偏好设置：

### 查看设置

```bash
pass-cli settings view
```

### 设置默认密码库

```bash
# By name
pass-cli settings set default-vault --vault-name "Personal Vault"

# By share ID
pass-cli settings set default-vault --share-id "3GqM1RhVZL8uXR_abc123"
```

**受影响的命令：** `item list`, `item view`, `item totp`, `item create`, `item update` 等

### 设置默认输出格式

```bash
pass-cli settings set default-format human
pass-cli settings set default-format json
```

**受影响的命令：** `item list`, `item view`, `item totp`, `vault list` 等

### 取消默认设置

```bash
pass-cli settings unset default-vault
pass-cli settings unset default-format
```

## 共享管理

### 列出所有共享内容

```bash
pass-cli share list
pass-cli share list --output json
```

显示与您和您的角色共享的所有资源（密码库和项目）。

## 邀请管理

### 列出待处理的邀请

```bash
pass-cli invite list
pass-cli invite list --output json
```

### 接受邀请

```bash
pass-cli invite accept --invite-token "abc123def456"
```

### 拒绝邀请

```bash
pass-cli invite reject --invite-token "abc123def456"
```

## 用户和会话信息

### 查看会话信息

```bash
pass-cli info
```

显示：版本跟踪、用户 ID、用户名、电子邮件。

### 查看用户详细信息

```bash
pass-cli user info
pass-cli user info --output json
```

显示：账户详情、订阅信息、存储使用情况。

### 测试连接

```bash
pass-cli test
```

验证会话的有效性和 API 连接性。

## 更新

**注意：** 仅适用于手动安装（不适用于包管理器）。

### 升级到最新版本

```bash
pass-cli update
pass-cli update --yes  # Skip confirmation
```

### 更改版本跟踪

```bash
# Switch to beta
pass-cli update --set-track beta
pass-cli update

# Switch back to stable
pass-cli update --set-track stable
pass-cli update
```

### 禁用自动更新检查

```bash
export PROTON_PASS_NO_UPDATE_CHECK=1
```

## 对象类型

### 共享

共享表示用户与资源（密码库或项目）之间的关系。它定义了访问权限：

- **密码库共享：** 允许访问整个密码库及其内的所有项目
- **项目共享：** 仅允许访问单个特定项目
- **角色：**
  - **查看者：** 只有读取权限
  - **编辑者：** 具有读取和写入权限，可以管理项目（但不能共享或管理成员）
  - **管理员：** 具有完全控制权，包括共享和管理员权限
  - **所有者：** 创建密码库的人，只有所有者可以删除密码库

### 密码库

密码库用于组织项目。项目只能存在于一个密码库中。

### 项目类型

- **登录：** 包含用户名/密码凭证以及 URL，支持 TOTP
- **备注：** 安全文本笔记
- **信用卡：** 加密后的支付卡信息
- **身份：** 个人身份信息
- **别名：** 用于保护隐私的电子邮件别名
- **SSH 密钥：** 用于身份验证的 SSH 私钥
- **WiFi：** 访问 WiFi 网络的凭证

**注意：** 项目通过项目 ID 进行标识，但该 ID 仅在结合共享 ID 时才具有唯一性（ShareID + ItemID = 全局唯一）。

## 最佳实践

### 安全性

- 使用网页登录以实现最大程度的兼容性（包括 SSO 和 U2F）
- 为每个账户生成唯一的密码
- 将 SSH 密钥存储在 Proton Pass 中，而不是本地文件系统中
- 在共享系统上注销
- 定期审查共享权限

### 组织管理

- 为不同的场景创建单独的密码库（工作用和个人用）
- 为项目和密码库设置描述性标题
- 为常用密码库设置默认值
- 配置默认的输出格式（脚本使用 JSON，交互式使用人类可读格式）

### 自动化

- 将凭证存储在文件中（而不是环境变量中）以增强安全性
- 使用 Proton Pass 的 URI 进行程序化的秘密访问
- 利用 JSON 格式进行脚本编写
- 在自动化脚本中包含 `pass-cli logout` 命令以完成清理

### 共享

- 遵循最小权限原则（从查看者权限开始）
- 对于持续协作，优先使用密码库共享
- 对于特定且有限的访问需求，使用项目共享
- 定期审核成员和权限

## Docker 使用

在 Docker 容器中运行 Proton Pass 时需要文件系统密钥存储（Docker 容器不支持 Keyring）：

```bash
# 1. Ensure logged out
pass-cli logout --force

# 2. Set filesystem key provider
export PROTON_PASS_KEY_PROVIDER=fs

# 3. Login as normal
pass-cli login
```

**为什么需要文件系统存储？**
- 容器无法访问内核的秘密服务
- 无头环境中无法使用 D-Bus
- 文件系统存储是唯一的选择

⚠️ **安全提示：** 密钥会与加密数据存储在同一位置。请确保容器环境的安全。

## 故障排除

### 认证问题

```bash
# Check session status
pass-cli info
pass-cli test

# Re-authenticate
pass-cli logout
pass-cli login
```

### 网络问题

- 检查互联网连接
- 检查防火墙设置是否允许 Proton Pass 的域名
- 使用 `pass-cli test` 命令进行测试

### 权限问题

- 查看您的角色：`pass-cli share list`
- 确保您具有执行操作的必要权限
- 联系密码库的所有者以调整权限

### 资源丢失

- 确认您正在查看正确的密码库
- 验证资源是否已被删除
- 确认访问权限是否已被撤销
- 检查待处理的邀请：`pass-cli invite list`

### 秘密引用解析错误

**“无效的引用格式”：**
- 确保格式为 `pass://vault/item/field`
- 检查是否缺少尾随的斜杠
- 确保三个组成部分都存在

**“引用需要字段名”：**
- 添加字段名：`pass://vault/item/field`（而不是 `pass://vault/item`）

**“字段未找到”：**
- 确认字段存在：`pass-cli item view --share-id <id> --item-id <id>`
- 检查字段名的拼写（区分大小写）

**引用未找到：**
1. 检查密码库访问权限：`pass-cli vault list`
2. 确认项目存在：`pass-cli item list --share-id <id>`
3. 确认字段名：`pass-cli item view <uri>`

## 配置

### 日志记录

**注意：** 日志会被发送到 `stderr`（不会干扰管道或命令集成）。

### 会话存储

**默认位置：**
- macOS：`~/Library/Application Support/proton-pass-cli/.session/`
- Linux：`~/.local/share/proton-pass-cli/.session/`

**自定义设置：**
```bash
export PROTON_PASS_SESSION_DIR='/custom/path'
```

### 密钥存储方式

使用 `PROTON_PASS_KEY_PROVIDER` 控制加密密钥的存储方式：

#### 1. Keyring 存储（默认，最安全）

```bash
export PROTON_PASS_KEY_PROVIDER=keyring  # or unset
```

**使用操作系统的安全存储方式：**
- **macOS：** macOS Keychain
- **Linux：** 基于内核的秘密存储（内核 Keyring）
- **Windows：** Windows 凭据管理器

**工作原理：**
- 首次运行时生成一个 256 位的随机密钥
- 存储在系统 Keyring 中
- 在后续运行时从中获取密钥
- 如果 Keyring 无法使用但会话存在，为了安全起见，系统会强制用户注销

**Linux 注意：** 使用内核 Keyring（不需要 D-Bus），适用于无头环境。**密钥在重启时会清除。**

**Docker 限制：** 容器无法使用内核的秘密服务，因此需要使用文件系统存储。**

#### 2. 文件系统存储

⚠️ **警告：** 存储方式安全性较低——密钥会与加密数据存储在同一位置。

```bash
export PROTON_PASS_KEY_PROVIDER=fs
```

将密钥存储在 `<session-dir>/local.key` 文件中，权限设置为 `0600`。

**优点：**
- 适用于所有环境（包括无头环境和容器）
- 在重启后仍能保留密钥
- 不依赖于系统服务

**适用场景：**
- Docker 容器
- 开发/测试环境
- 当系统 Keyring 不可用时

#### 3. 环境变量存储

⚠️ **警告：** 密钥会对同一会话中的其他进程可见。

```bash
export PROTON_PASS_KEY_PROVIDER=env
export PROTON_PASS_ENCRYPTION_KEY=your-secret-key
```

密钥的生成依赖于 `PROTON_PASS_ENCRYPTION_KEY`（必须设置且不能为空）。

**生成安全密钥：**
```bash
dd if=/dev/urandom bs=1 count=2048 2>/dev/null | sha256sum | awk '{print $1}'
```

**优点：**
- 可在所有环境中使用
- 不依赖于文件系统或 Keyring
- 用户可以控制密钥的可见性
- 适用于 CI/CD 流程和容器环境

**适用场景：**
- CI/CD 流程
- 需要避免使用文件系统存储的容器
- 需要明确控制密钥管理的自动化脚本

### 隐私设置

**禁用遥测：**
```bash
export PROTON_PASS_DISABLE_TELEMETRY=1
```

或者全局禁用：[账户安全设置](https://account.proton.me/pass/security) → 禁用“收集使用数据”

**发送的数据：** 包含匿名化的使用数据（例如，“创建了类型为 ‘note’ 的项目”）——**绝不包含个人敏感信息**。

## 环境变量

### 登录凭证（交互式登录）

```bash
export PROTON_PASS_PASSWORD='password'
export PROTON_PASS_PASSWORD_FILE='/path/to/file'
export PROTON_PASS_TOTP='123456'
export PROTON_PASS_TOTP_FILE='/path/to/file'
export PROTON_PASS_EXTRA_PASSWORD='extra-password'
export PROTON_PASS_EXTRA_PASSWORD_FILE='/path/to/file'
```

### SSH 密钥密码

```bash
export PROTON_PASS_SSH_KEY_PASSWORD='passphrase'
export PROTON_PASS_SSH_KEY_PASSWORD_FILE='/path/to/file'
```

### 更新设置

```bash
export PROTON_PASS_NO_UPDATE_CHECK=1
```

### 安装

```bash
export PROTON_PASS_CLI_INSTALL_DIR=/custom/path
export PROTON_PASS_CLI_INSTALL_CHANNEL=beta
```

## 常见工作流程

### 创建并填充新的密码库

```bash
# Create vault
pass-cli vault create --name "Project Alpha"

# List to get share ID
pass-cli vault list

# Create login items
pass-cli item create login \
  --share-id "new_vault_id" \
  --title "API Key" \
  --username "api_user" \
  --generate-password \
  --url "https://api.example.com"

# Share with team
pass-cli vault share --share-id "new_vault_id" alice@team.com --role editor
```

### 导入和使用 SSH 密钥

```bash
# Import existing key
pass-cli item create ssh-key import \
  --from-private-key ~/.ssh/id_ed25519 \
  --vault-name "SSH Keys" \
  --title "GitHub Key"

# Load into SSH agent
pass-cli ssh-agent load --vault-name "SSH Keys"

# Or start Pass as SSH agent
pass-cli ssh-agent start --vault-name "SSH Keys"
export SSH_AUTH_SOCK=$HOME/.ssh/proton-pass-agent.sock
```

### 通过脚本访问秘密

```bash
#!/bin/bash
# Automated login
export PROTON_PASS_PASSWORD_FILE="$HOME/.secrets/pass-password"
pass-cli login --interactive user@proton.me

# Retrieve secret
DB_PASSWORD=$(pass-cli item view "pass://Production/Database/password" --output json | jq -r '.password')

# Use secret
connect-to-db --password "$DB_PASSWORD"

# Cleanup
pass-cli logout
```

### 在应用程序部署中使用秘密

```bash
#!/bin/bash
# Create .env.production with secret references
cat > .env.production << EOF
NODE_ENV=production
DATABASE_URL=pass://Production/Database/connection_string
API_KEY=pass://Production/API/key
STRIPE_SECRET=pass://Production/Stripe/secret_key
EOF

# Deploy application with secrets injected
pass-cli run --env-file .env.production -- npm start

# Or generate config file from template
pass-cli inject \
  --in-file config.yaml.template \
  --out-file config.yaml \
  --force

# Then run app with generated config
./app --config config.yaml
```

### 集成到持续集成/持续部署（CI/CD）流程中

```bash
#!/bin/bash
# Login with environment variable key storage
export PROTON_PASS_KEY_PROVIDER=env
export PROTON_PASS_ENCRYPTION_KEY="${CI_PASS_ENCRYPTION_KEY}"
export PROTON_PASS_PASSWORD_FILE=/run/secrets/pass-password

pass-cli login --interactive user@proton.me

# Run tests with secrets
pass-cli run --env-file .env.test -- npm test

# Deploy with secrets
pass-cli run --env-file .env.production -- ./deploy.sh

# Cleanup
pass-cli logout
```

## 注意事项

- **测试阶段：** Proton Pass CLI 目前仍处于测试阶段
- **版本切换：** 仅适用于手动安装（不适用于包管理器）
- **项目更新限制：** 无法通过 CLI 更新 TOTP 或时间字段
- **密码建议：** 生成的密钥可以不设置密码（因为密钥已在密码库中加密）
- **SSH 代理刷新：** 默认刷新间隔为 1 小时，可通过 `--refresh-interval` 参数进行自定义
- **Docker 容器：** 必须使用文件系统密钥存储（`PROTON_PASS_KEY_PROVIDER=fs`）
- **Linux 下使用 Keyring：** 使用内核 Keyring（不使用 D-Bus），密钥在重启时会清除
- **遥测：** 仅发送匿名化数据（不包含个人敏感信息），可以禁用
- **秘密隐藏：** 在 `run` 命令的输出中自动隐藏秘密
- **模板语法：** `inject` 命令需要使用 `{{ }}` 括号，`run` 命令使用简单的 `pass://` 格式
- **项目 ID 的唯一性：** 项目 ID 仅在结合共享 ID 时才具有唯一性

## 命令参考快速列表

**认证相关命令：**
- `login`, `logout`, `info`, `test`

**密码库相关命令：**
- `vault list`, `vault create`, `vault update`, `vault delete`, `vault share`, `vault member`, `vault transfer`

**项目相关命令：**
- `item list`, `item view`, `item create`, `item update`, `item delete`, `item share`, `item totp`, `item alias`, `item attachment`

**秘密注入相关命令：**
- `run` - 使用 Proton Pass 中的秘密作为环境变量执行命令
- `inject` - 处理包含秘密引用的模板文件

**密码相关命令：**
- `password generate`, `password score`

**SSH 相关命令：**
- `ssh-agent load`, `ssh-agent start`

**设置相关命令：**
- `settings view`, `settings set`, `settings unset`

**共享与邀请相关命令：**
- `share list`, `invite list`, `invite accept`, `invite reject`

**用户相关命令：**
- `user info`

**更新相关命令：**
- `update`