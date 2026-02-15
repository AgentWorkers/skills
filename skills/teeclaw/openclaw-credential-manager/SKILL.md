---
name: credential-manager
description: OpenClaw的强制性安全基础配置。将分散的API密钥和凭据整合到一个具有适当权限的安全`.env`文件中。该配置支持对高价值敏感信息进行GPG加密、跟踪凭据轮换情况、进行深度安全扫描以及加强系统备份措施。在设置OpenClaw、迁移凭据、进行安全审计或强制执行`.env`文件规范时，必须使用此配置。这并非可选项——集中式凭据管理是确保OpenClaw安全部署的核心要求。
---

# 凭据管理器

**状态：强制性的安全基础**

将分散的API密钥和凭据整合到一个安全的、集中式的`.env`文件中。

## ⚠️ 这不是可选的

集中式的`.env`凭据管理是OpenClaw安全性的**核心要求**。如果您的凭据分散在多个文件中，请**立即停止并整合它们**。

**规则：**所有凭据必须仅保存在`~/.openclaw/.env`文件中。禁止保存在工作区、技能或脚本目录中。

请参阅：
- [CORE-PRINCIPLE.md](CORE-PRINCIPLE.md) — 为什么这是不可商量的
- [CONSOLIDATION-RULE.md](CONSOLIDATION-RULE.md) — 单一来源原则

## 基础要求

**每个OpenClaw部署都必须具备：**
```
~/.openclaw/.env (mode 600)
```

这是您所有凭据的单一、权威来源。没有任何例外。

**为什么？**
- 单一存储位置 = 更容易保护
- 文件权限设置为600（仅所有者可读）
- 被Git忽略（防止意外提交）
- 验证过的格式 = 可以发现错误
- 审计追踪 = 可以了解哪些内容发生了变化

分散的凭据意味着分散的攻击面。此技能可以解决这个问题。

## 该技能的功能

1. **扫描**常见位置的凭据（包括深度扫描硬编码的秘密）
2. **备份**现有的凭据文件（带有时间戳，权限设置为600）
3. **整合**到`~/.openclaw/.env`中
4. **使用适当的权限进行保护（文件权限600，目录权限700）
5. **验证**安全性、格式和熵值
6. **使用GPG加密**高价值秘密（钱包密钥、私钥、助记词）
7. **跟踪**凭据轮换计划
8. **通过快速失败检查**强制执行最佳实践
9. **迁移后清理**旧文件

## 检测参数

该技能通过扫描以下位置自动检测凭据：

**文件模式：**
- `~/.config/*/credentials.json` — 服务配置目录
- `~/.config/*/*.credentials.json` — 嵌套的凭据文件
- `~/.openclaw/*.json` — OpenClaw根目录下的凭据文件
- `~/.openclaw/*-credentials*` — 带有名称的凭据文件（例如，farcaster-credentials.json）
- `~/.openclaw/workspace/memory/*-creds.json` — 内存凭据文件
- `~/.openclaw/workspace/memory/*credentials*.json` — 内存凭据文件
- `~/.openclaw/workspace/.env` — 工作区环境文件
- `~/.openclaw/workspace/*/.env` — 子目录环境文件
- `~/.openclaw/workspace/skills/*/.env` — 技能环境文件
- `~/.local/share/*/credentials.json` — 本地共享目录

**敏感密钥模式：**
- API密钥、访问令牌、bearer令牌
- 秘密、密码、口令短语
- OAuth消费者密钥
- 私钥、签名密钥、钱包密钥
- 助记词和种子短语

**深度扫描（--deep标志）：**
- 在`.sh`、`.js`、`.py`、`.mjs`、`.ts`文件中搜索硬编码的秘密
- 检测符合常见密钥前缀的高熵字符串（`sk_`、`pk_`、`Bearer`、`0x` + 64 hex）
- 排除`node_modules/`、`.git/`目录

**安全检查：**
- 文件权限（文件必须设置为600，目录必须设置为700）
- 备份权限（备份文件必须设置为600，备份目录必须设置为700）
- 被Git忽略（防止意外提交）
- 格式验证（允许包含空格的引用值）
- 熵值分析（标记出低熵值的秘密）
- 私钥检测（标记出`0x` + 64 hex字符值的密钥）
- 助记词检测（标记出12/24个单词的助记词）

## 快速入门

### 完整迁移（推荐）

```bash
# Scan for credentials
./scripts/scan.py

# Deep scan (includes hardcoded secrets in scripts)
./scripts/scan.py --deep

# Review and consolidate
./scripts/consolidate.py

# Validate security
./scripts/validate.py

# Encrypt high-value secrets
./scripts/encrypt.py --keys MAIN_WALLET_PRIVATE_KEY,CUSTODY_PRIVATE_KEY

# Check rotation status
./scripts/rotation-check.py
```

### 单个操作

```bash
# Scan only
./scripts/scan.py

# Consolidate specific service
./scripts/consolidate.py --service x

# Backup without removing
./scripts/consolidate.py --backup-only

# Clean up old files
./scripts/cleanup.py --confirm
```

## 常见的凭据位置

该技能会扫描以下位置：

```
~/.config/*/credentials.json
~/.openclaw/*.json
~/.openclaw/*-credentials*
~/.openclaw/workspace/memory/*-creds.json
~/.openclaw/workspace/memory/*credentials*.json
~/.openclaw/workspace/*/.env
~/.openclaw/workspace/skills/*/.env
~/.env (if exists, merges)
```

## 安全特性

✅ **文件权限：**将`.env`文件的权限设置为600（仅所有者可读）
✅ **目录权限：**将备份目录的权限设置为700（仅所有者可读）
✅ **备份权限：**将备份文件的权限设置为600（仅所有者可读）
✅ **Git保护：**创建/更新`.gitignore`文件
✅ **备份：**在更改前进行时间戳备份（确保安全）
✅ **验证：**检查格式、权限、熵值和重复项
✅ **模板：**创建`.env.example`文件（可安全共享）
✅ **GPG加密：**对高价值秘密进行加密
✅ **轮换跟踪：**在需要轮换凭据时发出警告
✅ **深度扫描：**检测源文件中的硬编码秘密
✅ **支持符号链接：**验证符号链接的`.env`目标文件

## 输出结构

迁移完成后：

```
~/.openclaw/
├── .env                     # All credentials (secure, mode 600)
├── .env.secrets.gpg         # GPG-encrypted high-value keys (mode 600)
├── .env.meta                # Rotation metadata (mode 600)
├── .env.example             # Template (safe to share)
├── .gitignore               # Protects .env and .env.secrets.gpg
└── backups/                 # (mode 700)
    └── credentials-old-YYYYMMDD/  # (mode 700)
        └── *.bak            # Backup files (mode 600)
```

## 高价值秘密的GPG加密

私钥、钱包密钥和助记词**绝不应**以明文形式存在于磁盘上。应使用GPG对其进行加密。

### 设置GPG

```bash
# First-time setup (generates OpenClaw GPG key, configures agent cache)
./scripts/setup-gpg.sh
```

### 加密高价值密钥

```bash
# Encrypt specific keys (moves them from .env to .env.secrets.gpg)
./scripts/encrypt.py --keys MAIN_WALLET_PRIVATE_KEY,CUSTODY_PRIVATE_KEY,SIGNER_PRIVATE_KEY

# The .env will contain placeholders:
# MAIN_WALLET_PRIVATE_KEY=GPG:MAIN_WALLET_PRIVATE_KEY
```

### 脚本如何访问加密密钥

`enforce.py`模块会透明地处理这些操作：

```python
from enforce import get_credential

# Works for both plaintext and GPG-encrypted keys
key = get_credential('MAIN_WALLET_PRIVATE_KEY')
# If value starts with "GPG:", decrypts from .env.secrets.gpg automatically
```

### GPG代理缓存

在无头服务器（VPS）上，GPG代理会缓存密码短语：
- 默认缓存有效期：8小时
- 可通过`setup-gpg.sh`进行配置
- 重启后需要输入一次密码短语，之后会自动缓存

### 需要加密的密钥类型

| 密钥类型 | 是否需要加密？ | 原因 |
|----------|----------|-----|
| 钱包私钥 | ✅ 是 | 控制资金 |
| 托管/签名私钥 | ✅ 是 | 控制身份 |
| 助记词/种子短语 | ✅ 是 | 用于恢复 |
| API密钥（服务） | ❌ 否 | 可撤销，损害较小 |
| 代理ID、名称、URL | ❌ 否 | 不属于敏感信息 |

## 凭据轮换跟踪

### 设置轮换元数据

```bash
# Initialize rotation tracking for all keys
./scripts/rotation-check.py --init
```

创建`~/.openclaw/.env.meta`文件：
```json
{
  "MAIN_WALLET_PRIVATE_KEY": {
    "created": "2026-01-15",
    "lastRotated": null,
    "rotationDays": 90,
    "risk": "critical"
  },
  "MOLTBOOK_API_KEY": {
    "created": "2026-02-04",
    "lastRotated": null,
    "rotationDays": 180,
    "risk": "low"
  }
}
```

### 检查轮换状态

```bash
# Check which keys need rotation
./scripts/rotation-check.py

# Output:
# 🔴 MAIN_WALLET_PRIVATE_KEY: 26 days old (critical, rotate every 90 days)
# ✅ MOLTBOOK_API_KEY: 7 days old (low, rotate every 180 days)
```

### 轮换计划

| 风险等级 | 轮换周期 | 例子 |
|------------|----------------|----------|
| 关键 | 90天 | 钱包密钥、私钥 |
| 标准 | 180天 | 收费服务的API密钥 |
| 低风险 | 365天 | 免费 tier 的API密钥、代理ID |

### 添加到Heartbeat中（可选）

将轮换检查添加到`HEARTBEAT.md`文件中，以便定期监控：
```markdown
## Credential Rotation (weekly)
If 7+ days since last rotation check:
1. Run: ./scripts/rotation-check.py
2. If any keys overdue: notify human
3. Update lastRotationCheck timestamp
```

## 支持的服务

系统会自动检测以下服务：
- **X（Twitter）：** OAuth 1.0a凭据
- **Farcaster：** 托管密钥、签名密钥、FID凭据
- **Molten：** 代理意图匹配
- **Moltbook：** 代理社交网络
- **Botchan/4claw：** Net Protocol
- **OpenAI、Anthropic、Google：** AI提供商
- **GitHub、GitLab：** 代码托管服务
- **Coinbase/CDP：** 加密钱包凭据
- **通用：** `API_KEY`、`*_TOKEN`、`*_SECRET`等模式

请参阅[references/supported-services.md](references/supported-services.md)以获取完整列表。

## 脚本

所有脚本都支持`--help`参数以获取详细使用说明。

### scan.py
```bash
# Scan and report
./scripts/scan.py

# Deep scan (includes hardcoded secrets in scripts)
./scripts/scan.py --deep

# Include custom paths
./scripts/scan.py --paths ~/.myapp/config ~/.local/share/creds

# JSON output
./scripts/scan.py --format json
```

### consolidate.py
```bash
# Interactive mode (prompts before changes)
./scripts/consolidate.py

# Auto-confirm (no prompts)
./scripts/consolidate.py --yes

# Backup only
./scripts/consolidate.py --backup-only

# Specific service
./scripts/consolidate.py --service molten
```

### validate.py
```bash
# Full validation (permissions, format, entropy, security)
./scripts/validate.py

# Check permissions only
./scripts/validate.py --check permissions

# Fix issues automatically
./scripts/validate.py --fix
```

### encrypt.py
```bash
# Encrypt specific high-value keys
./scripts/encrypt.py --keys MAIN_WALLET_PRIVATE_KEY,CUSTODY_PRIVATE_KEY

# List currently encrypted keys
./scripts/encrypt.py --list

# Decrypt (move back to plaintext .env)
./scripts/encrypt.py --decrypt --keys MAIN_WALLET_PRIVATE_KEY
```

### rotation-check.py
```bash
# Check rotation status
./scripts/rotation-check.py

# Initialize tracking for all keys
./scripts/rotation-check.py --init

# Record a rotation
./scripts/rotation-check.py --rotated MOLTBOOK_API_KEY
```

### setup-gpg.sh
```bash
# First-time GPG setup for OpenClaw
./scripts/setup-gpg.sh

# Configure cache timeout (hours)
./scripts/setup-gpg.sh --cache-hours 12
```

### cleanup.py
```bash
# Dry run (shows what would be deleted)
./scripts/cleanup.py

# Actually delete old files
./scripts/cleanup.py --confirm

# Keep backups
./scripts/cleanup.py --confirm --keep-backups
```

## 迁移工作流程

这是经过测试和验证的详细步骤流程，适用于实际的开源Claw部署。

### 第1步：扫描分散的凭据

```bash
cd /path/to/openclaw/skills/credential-manager

# Basic scan — finds credential files by path patterns
./scripts/scan.py

# Deep scan — also greps source files for hardcoded secrets
./scripts/scan.py --deep
```

**输出中需要注意的内容：**
- ⚠️ 权限设置为非600的文件（不安全的权限）
- 指向主`.env`文件的符号链接`.env`文件
- 位于`~/.openclaw/.env`之外的JSON格式凭据文件
- 脚本中发现的硬编码密钥

**示例输出：**
```
⚠️ /home/user/.openclaw/farcaster-credentials.json
   Type: json
   Keys: custodyPrivateKey, signerPrivateKey, ...
   Mode: 644
   ⚠️  Should be 600 for security

✅ /home/user/.openclaw/.env
   Type: env
   Keys: API_KEY, X_CONSUMER_KEY, ...
   Mode: 600
```

### 第2步：整合到`.env`文件中

```bash
./scripts/consolidate.py
```

**交互式流程：**
1. 脚本扫描并列出所有找到的凭据文件
2. 将现有的`.env`文件备份到`~/.openclaw/backups/credentials-old-YYYYMMDD/`
3. 加载现有的`.env`文件中的密钥
4. 处理每个凭据文件：
   - 自动检测服务类型（如x、farcaster、moltbook等）
   - 规范化密钥名称（例如，`custodyPrivateKey` → `FARCASTER_CUSTODY_PRIVATE_KEY`
   - 显示映射关系：`密钥 → 环境变量名`
5. 请求确认：`继续？[y/N]`
6. 写入合并后的`.env`文件（权限设置为600）
7. 创建`.env.example`模板（可安全共享）
8. 更新`.gitignore`文件

**对于未被自动检测到的凭据**（例如，嵌套的JSON文件`farcaster-credentials.json`中包含多个账户），需要手动将其添加到`.env`文件中：
```bash
cat >> ~/.openclaw/.env << 'EOF'

# FARCASTER (Active: mr-teeclaw, FID 2700953)
FARCASTER_FID=2700953
FARCASTER_FNAME=mr-teeclaw
FARCASTER_CUSTODY_ADDRESS=0x...
FARCASTER_CUSTODY_PRIVATE_KEY=0x...
FARCASTER_SIGNER_PUBLIC_KEY=...
FARCASTER_SIGNER_PRIVATE_KEY=...

# FARCASTER LEGACY (teeclaw, FID 2684290)
FARCASTER_LEGACY_FID=2684290
FARCASTER_LEGACY_CUSTODY_ADDRESS=0x...
FARCASTER_LEGACY_CUSTODY_PRIVATE_KEY=0x...
FARCASTER_LEGACY_SIGNER_PUBLIC_KEY=...
FARCASTER_LEGACY_SIGNER_PRIVATE_KEY=...
EOF

chmod 600 ~/.openclaw/.env
```

### 第3步：验证

```bash
./scripts/validate.py
```

**执行的检查：**
- ✅ `.env`文件的权限是否设置为600
- `.gitignore`文件是否正确配置
- 格式是否正确（包括引号和重复项）
- 安全性分析：
  - 检测明文私钥（`0x` + 64 hex字符） → 建议使用GPG加密
  - 检测助记词/种子短语（12/24个单词） → 建议使用GPG加密
  - 对`SECRET/PRIVATE_KEY/PASSWORD`字段进行熵值分析
  - 标记出弱或占位符形式的密钥
- 备份权限是否正确（文件权限为600，目录权限为700）

**自动修复问题：**
```bash
./scripts/validate.py --fix
```
该步骤会修复文件权限、目录权限和备份权限问题。但它不会自动修复格式问题或加密密钥——这些需要手动处理。

### 第4步：设置GPG并加密私钥

```bash
# First-time GPG setup (configures agent cache, tests encrypt/decrypt)
./scripts/setup-gpg.sh
# Optional: --cache-hours 12 (default: 8)
```

**加密高价值密钥：**
```bash
# Encrypt wallet + Farcaster private keys
./scripts/encrypt.py --keys MAIN_WALLET_PRIVATE_KEY,FARCASTER_CUSTODY_PRIVATE_KEY,FARCASTER_SIGNER_PRIVATE_KEY,FARCASTER_LEGACY_CUSTODY_PRIVATE_KEY,FARCASTER_LEGACY_SIGNER_PRIVATE_KEY
```

**操作过程：**
1. 提示输入GPG密码短语（或读取环境变量`OPENCLAW_GPG_PASSPHRASE`）
2. 从`.env`文件中提取指定的密钥值
3. 将它们加密后存储在`~/.openclaw/.env.secrets.gpg`文件中（使用AES256算法，权限设置为600）
4. 用`GPG:KEY_NAME`替换`.env`文件中的原始密钥值
5. 使用`get_credential()`或 `_load_cred()`函数的脚本可以透明地解密这些密钥

**将密码短语保存到`.env`文件中以供自动解密：**
```bash
echo 'OPENCLAW_GPG_PASSPHRASE=your-passphrase-here' >> ~/.openclaw/.env
chmod 600 ~/.openclaw/.env
```

**验证加密效果：**
```bash
# Check .env has GPG placeholders
grep "GPG:" ~/.openclaw/.env

# List all encrypted keys
./scripts/encrypt.py --list
```

### 第5步：初始化轮换跟踪

```bash
./scripts/rotation-check.py --init
```

**自动对所有密钥进行分类：**
- **关键级别**（90天轮换）：`*PRIVATE_KEY`、`*MNEMONIC`、`*SEED`、`*WALLET_KEY`、`*CUSTODY`、`*SIGNER`**
- **标准级别**（180天轮换）：`*API_KEY`、`*SECRET`、`*TOKEN`、`*BEARER`、`*CONSUMER`、`*ACCESS`**
- **低风险级别**（365天轮换）：其他所有密钥

创建`~/.openclaw/.env.meta`文件（权限设置为600），其中包含创建日期和轮换计划。

**随时可以检查轮换状态：**
```bash
./scripts/rotation-check.py
```

### 第6步：清理旧凭据文件

```bash
# Dry run first — see what would be deleted
./scripts/cleanup.py

# Actually delete (prompts for 'DELETE' confirmation)
./scripts/cleanup.py --confirm
```

**还需要手动删除扫描未发现的旧文件：**
```bash
# Example: farcaster-credentials.json was manually migrated
cp ~/.openclaw/farcaster-credentials.json ~/.openclaw/backups/credentials-old-YYYYMMDD/farcaster-credentials.json.bak
chmod 600 ~/.openclaw/backups/credentials-old-YYYYMMDD/farcaster-credentials.json.bak
rm ~/.openclaw/farcaster-credentials.json
```

### 第7步：更新引用旧文件的脚本

任何从JSON凭据文件或硬编码路径加载数据的脚本都需要更新。

**Bash脚本的更新方式：**
```bash
# OLD (insecure):
FARCASTER_CREDS="/home/user/.openclaw/farcaster-credentials.json"
fid=$(jq -r '.fid' "$FARCASTER_CREDS")
private_key=$(jq -r '.custodyPrivateKey' "$FARCASTER_CREDS")

# NEW (secure, GPG-aware):
ENV_FILE="$HOME/.openclaw/.env"

_load_cred() {
  local key="$1"
  local value
  value=$(grep "^${key}=" "$ENV_FILE" | head -1 | cut -d= -f2-)
  if [[ "$value" == GPG:* ]]; then
    local gpg_key="${value#GPG:}"
    local passphrase="${OPENCLAW_GPG_PASSPHRASE:-}"
    if [ -n "$passphrase" ]; then
      value=$(echo "$passphrase" | gpg -d --batch --quiet --passphrase-fd 0 "$HOME/.openclaw/.env.secrets.gpg" | python3 -c "import json,sys; print(json.load(sys.stdin).get('$gpg_key',''))")
    else
      value=$(gpg -d --batch --quiet "$HOME/.openclaw/.env.secrets.gpg" | python3 -c "import json,sys; print(json.load(sys.stdin).get('$gpg_key',''))")
    fi
  fi
  echo "$value"
}

fid=$(_load_cred "FARCASTER_FID")
private_key=$(_load_cred "FARCASTER_CUSTODY_PRIVATE_KEY")
```

**Node.js脚本的更新方式：**
```javascript
// OLD (insecure):
const creds = JSON.parse(fs.readFileSync('~/.openclaw/farcaster-credentials.json'));
const privateKey = creds.custodyPrivateKey;

// NEW (secure, GPG-aware):
const ENV_PATH = path.join(os.homedir(), '.openclaw/.env');
const SECRETS_PATH = path.join(os.homedir(), '.openclaw/.env.secrets.gpg');

function loadCred(key) {
  const content = fs.readFileSync(ENV_PATH, 'utf8');
  for (const line of content.split('\n')) {
    if (line.startsWith(key + '=')) {
      let value = line.slice(key.length + 1).trim();
      if (value.startsWith('GPG:')) {
        const { execSync } = require('child_process');
        const passphrase = process.env.OPENCLAW_GPG_PASSPHRASE || '';
        const cmd = passphrase
          ? `echo "${passphrase}" | gpg -d --batch --quiet --passphrase-fd 0 "${SECRETS_PATH}"`
          : `gpg -d --batch --quiet "${SECRETS_PATH}"`;
        const secrets = JSON.parse(execSync(cmd, { encoding: 'utf8' }));
        return secrets[value.slice(4)] || '';
      }
      return value;
    }
  }
  return '';
}

const privateKey = loadCred('FARCASTER_CUSTODY_PRIVATE_KEY');
```

**Python脚本的更新方式：**
```python
# Use the enforce module (recommended):
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / 'openclaw/skills/credential-manager/scripts'))
from enforce import get_credential

private_key = get_credential('FARCASTER_CUSTODY_PRIVATE_KEY')  # Auto-decrypts GPG
```

### 第8步：最终验证

**预期的最终状态：**
```
~/.openclaw/
├── .env                     # All credentials (mode 600, private keys = GPG:*)
├── .env.secrets.gpg         # GPG-encrypted private keys (mode 600)
├── .env.meta                # Rotation tracking metadata (mode 600)
├── .env.example             # Template (safe to share)
├── .gitignore               # Protects .env, .env.secrets.gpg, .env.meta
└── backups/                 # (mode 700)
    └── credentials-old-YYYYMMDD/  # (mode 700)
        └── *.bak            # Backup files (mode 600)
```

## 对于技能开发者：强制执行此标准

其他OpenClaw技能在使用凭据之前必须验证其安全性：

### Python技能
```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add credential-manager scripts to path
sys.path.insert(0, str(Path.home() / '.openclaw/skills/credential-manager/scripts'))

# Enforce secure .env (exits if not compliant)
from enforce import require_secure_env, get_credential

require_secure_env()

# Now safe to load credentials (handles GPG-encrypted keys transparently)
api_key = get_credential('SERVICE_API_KEY')
wallet_key = get_credential('MAIN_WALLET_PRIVATE_KEY')  # Auto-decrypts from GPG
```

### Bash技能
```bash
#!/usr/bin/env bash
set -euo pipefail

# Validate .env exists and is secure
if ! python3 ~/.openclaw/skills/credential-manager/scripts/enforce.py; then
    exit 1
fi

# Now safe to load
source ~/.openclaw/.env
```

**这会创建一个快速失败的系统：**如果凭据未得到适当保护，相关技能将拒绝运行。用户必须修复这些问题。

## 加载凭据

迁移完成后，从`.env`文件中加载凭据：

### Python
```python
import os
from pathlib import Path

# Load .env
env_file = Path.home() / '.openclaw' / '.env'
with open(env_file) as f:
    for line in f:
        if '=' in line and not line.strip().startswith('#'):
            key, val = line.strip().split('=', 1)
            os.environ[key] = val

# Use credentials
api_key = os.getenv('SERVICE_API_KEY')
```

### Bash
```bash
# Load .env
set -a
source ~/.openclaw/.env
set +a

# Use credentials
echo "$SERVICE_API_KEY"
```

### 使用现有的加载器

如果您使用OpenClaw脚本进行了迁移：
```python
from load_credentials import get_credentials
creds = get_credentials('x')
```

### 添加新凭据

编辑`~/.openclaw/.env`文件：
```bash
# Add new service
NEW_SERVICE_API_KEY=your_key_here
NEW_SERVICE_SECRET=your_secret_here
```

同时更新模板文件：
```bash
# Edit .env.example
NEW_SERVICE_API_KEY=your_key_here
NEW_SERVICE_SECRET=your_secret_here
```

如果新凭据具有高价值（如私钥或钱包密钥）：
```bash
# Add to .env first, then encrypt
./scripts/encrypt.py --keys NEW_SERVICE_PRIVATE_KEY
```

## 安全最佳实践

请参阅[references/security.md](references/security.md)以获取详细的安全指南。

**快速检查清单：**
- ✅ `.env`文件的权限设置为600
- `.env`文件被Git忽略
- 备份文件的权限设置为600
- 备份目录的权限设置为700
- 代码或日志中不存在凭据（使用`--deep`选项进行扫描验证）
- 私钥已使用GPG加密
- 已建立并跟踪轮换计划
- 符号链接的`.env`文件仅指向主`.env`文件
- 命令行历史记录中不存在凭据（使用`source`命令加载，而不是`export KEY=value`

## 回滚

如果出现问题：

```bash
# Find your backup
ls -la ~/.openclaw/backups/

# Restore specific file
cp ~/.openclaw/backups/credentials-old-YYYYMMDD/x-credentials.json.bak \
   ~/.config/x/credentials.json

# Decrypt GPG secrets back to plaintext
./scripts/encrypt.py --decrypt --keys MAIN_WALLET_PRIVATE_KEY
```

## 注意事项

- **默认情况下操作是非破坏性的：**在删除原始文件之前会先进行备份
- **操作是幂等的：**可以多次安全执行
- **可扩展性：**可以在脚本中添加自定义的凭据匹配规则
- **安全性：**从不记录完整的凭据内容，只记录元数据
- **支持GPG：**透明地处理加密和明文凭据
- **备份措施完善：**所有备份文件都设置了适当的权限
- **支持符号链接：**能够检测和验证符号链接的凭据文件