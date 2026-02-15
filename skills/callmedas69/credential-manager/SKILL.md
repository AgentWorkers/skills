---
name: credential-manager
description: OpenClaw的强制性安全基础要求：将分散的API密钥和凭据整合到一个具有适当权限的安全`.env`文件中。在设置OpenClaw、迁移凭据、进行安全审计或实施`.env`文件标准时，必须使用该文件。这并非可选功能——集中式凭据管理是确保OpenClaw安全部署的核心要求。系统会扫描常见位置中的凭据文件，备份现有文件，创建一个权限设置为600的统一`.env`文件，验证其安全性，并遵循最佳实践。
---

# 凭据管理器

**状态：强制性的安全基础**

将分散的 API 密钥和凭证整合到一个安全的、集中式的 `.env` 文件中。

## ⚠️ 这不是可选的

集中式的 `.env` 凭据管理是 OpenClaw 安全性的**核心要求**。如果您的凭证分散在多个文件中，请**立即停止并整合它们**。

**规则：** 所有凭证必须仅保存在 `~/.openclaw/.env` 文件中，不允许保存在工作区、技能文件或脚本目录中。

请参阅：
- [CORE-PRINCIPLE.md](CORE-PRINCIPLE.md) – 为什么这是不可协商的
- [CONSOLIDATION-RULE.md](CONSOLIDATION-RULE.md) – 单一来源原则

## 基础要求

**每个 OpenClaw 部署都必须具备：**
```
~/.openclaw/.env (mode 600)
```

这是您所有凭证的唯一来源，没有任何例外。

**为什么？**
- 单一存储位置 = 更容易保护
- 文件权限设置为 600（仅所有者可读）
- 被 Git 忽略（防止意外提交）
- 格式经过验证（可检测错误）
- 有审计跟踪（便于了解更改内容）

凭证分散意味着攻击面也会分散。此功能可以解决这个问题。

## 该功能的用途

1. **扫描** 常见位置中的凭证
2. **备份** 现有的凭证文件（并添加时间戳）
3. **整合** 到 `~/.openclaw/.env` 文件中
4. **设置适当权限（600）以保护文件**
5. **验证** 凭据的安全性和格式
6. **遵循最佳实践**
7. **迁移后清理** 旧文件

## 检测参数

该功能通过扫描以下内容自动检测凭证：

**文件模式：**
- 配置目录中的 `credentials.json` 文件
- `.env` 文件
- 名称中包含 `-creds` 或 `credentials` 的内存文件

**敏感密钥模式：**
- API 密钥、访问令牌、承载令牌
- 秘密信息、密码、短语
- OAuth 消费者密钥
- 私钥、签名密钥、钱包密钥
- 备忘词和种子短语

**安全检查：**
- 文件权限（必须设置为 600）
- 被 Git 忽略（防止意外提交）
- 格式验证

## 快速入门

### 完整迁移（推荐）

```bash
# Scan for credentials
./scripts/scan.py

# Review and consolidate
./scripts/consolidate.py

# Validate security
./scripts/validate.py
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

## 常见凭证存储位置

该功能会扫描以下位置：

```
~/.config/*/credentials.json
~/.openclaw/workspace/memory/*-creds.json
~/.openclaw/workspace/memory/*credentials*.json
~/.env (if exists, merges)
```

## 安全特性

✅ **文件权限：** 将 `.env` 文件的权限设置为 600（仅所有者可读）
✅ **Git 保护：** 创建/更新 `.gitignore` 文件
✅ **备份：** 在更改前进行时间戳备份
✅ **验证：** 检查格式、权限和重复项
✅ **模板：** 创建 `.env.example` 文件（可安全共享）

## 迁移后的文件结构

```
~/.openclaw/
├── .env                     # All credentials (secure)
├── .env.example             # Template (safe)
├── .gitignore               # Protects .env
├── CREDENTIALS.md           # Documentation
└── backups/
    └── credentials-old-YYYYMMDD/  # Backup of old files
```

## 支持的服务

系统会自动检测以下服务：
- **X (Twitter)：** OAuth 1.0a 凭据
- **Molten：** 代理意图匹配
- **Moltbook：** 代理社交网络
- **Botchan/4claw：** 网络协议
- **OpenAI, Anthropic, Google：** 人工智能服务提供商
- **GitHub, GitLab：** 代码托管平台
- **通用：** `API_KEY`, `*_TOKEN`, `*_SECRET` 等模式

完整服务列表请参阅 [references/supported-services.md](references/supported-services.md)。

## 安全最佳实践

详细的安全指南请参阅 [references/security.md](references/security.md)。

**快速检查清单：**
- ✅ `.env` 文件的权限设置为 600
- ✅ `.env` 文件被 Git 忽略
- ✅ 代码和日志中不含凭证
- ✅ 定期轮换密钥
- ✅ 每个环境使用独立的密钥

## 脚本

所有脚本都支持使用 `--help` 参数查看详细用法。

### scan.py
```bash
# Scan and report
./scripts/scan.py

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
# Full validation
./scripts/validate.py

# Check permissions only
./scripts/validate.py --check permissions

# Fix issues automatically
./scripts/validate.py --fix
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

**步骤 1：发现**
```bash
./scripts/scan.py
```
查看输出，了解哪些凭证需要迁移。

**步骤 2：备份与整合**
```bash
./scripts/consolidate.py
```
创建备份文件，生成新的 `.env` 文件，并设置文件权限。

**步骤 3：验证**
```bash
./scripts/validate.py
```
确保所有内容都安全且正确。

**步骤 4：测试**
使用新的 `.env` 文件测试您的应用程序/技能。

**步骤 5：清理**
```bash
./scripts/cleanup.py --confirm
```
删除旧凭证文件（备份文件保留）。

## 对于技能开发者：强制执行此标准

其他 OpenClaw 技能在使用凭证之前必须验证其安全性：

### Python 技能
```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add credential-manager scripts to path
sys.path.insert(0, str(Path.home() / '.openclaw/skills/credential-manager/scripts'))

# Enforce secure .env (exits if not compliant)
from enforce import require_secure_env, get_credential

require_secure_env()

# Now safe to load credentials
api_key = get_credential('SERVICE_API_KEY')
```

### Bash 技能
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

**这会创建一个“快速失败”的系统**：如果凭证未得到妥善保护，相关技能将拒绝运行，迫使用户进行修复。

## 加载凭证

迁移完成后，从 `.env` 文件中加载凭证：

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
如果您使用 OpenClaw 脚本进行了迁移：
```python
from load_credentials import get_credentials
creds = get_credentials('x')
```

## 添加新凭证

编辑 `~/.openclaw/.env` 文件：
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

## 回滚

如果出现问题：
```bash
# Find your backup
ls -la ~/.openclaw/backups/

# Restore specific file
cp ~/.openclaw/backups/credentials-old-YYYYMMDD/x-credentials.json.bak \
   ~/.config/x/credentials.json
```

## 注意事项

- **默认情况下是非破坏性的：** 删除前会备份原始文件
- **幂等操作：** 可多次安全运行
- **可扩展性：** 可在脚本中添加自定义的凭证检测规则
- **安全性：** 仅记录凭证的元数据，不记录完整内容