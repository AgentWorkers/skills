# 自动备份功能

**为AI代理提供自动的工作区和内存备份功能。**

每个代理都需要备份。本功能负责备份以下内容：
- 🧠 内存文件（MEMORY.md、每日日志）
- 🆔 身份文件（SOUL.md、USER.md、AGENTS.md、IDENTITY.md）
- 📜 脚本和自动化脚本
- 💾 openclaw-mem数据库
- ⚙️ 配置文件

## 安装

```bash
# Install via ClawHub
clawhub install self-backup

# Or copy to your skills directory
cp -r self-backup /Users/sem/argent/skills/
```

## 快速入门

```bash
# Create backup config
cd /Users/sem/argent/skills/self-backup
cp config/backup.example.json config/backup.json

# Edit config to set your backup location
nano config/backup.json

# Run backup
./scripts/backup.sh
```

## 配置

编辑 `config/backup.json` 文件：

```json
{
  "workspace": "/Users/sem/argent",
  "backupDir": "/Users/sem/backups/argent",
  "targets": {
    "local": {
      "enabled": true,
      "path": "/Users/sem/backups/argent"
    },
    "git": {
      "enabled": false,
      "repo": "git@github.com:yourusername/agent-backup.git"
    },
    "s3": {
      "enabled": false,
      "bucket": "my-agent-backups",
      "prefix": "argent/"
    }
  },
  "include": [
    "MEMORY.md",
    "SOUL.md",
    "USER.md",
    "AGENTS.md",
    "IDENTITY.md",
    "TOOLS.md",
    "HEARTBEAT.md",
    "memory/*.md",
    "scripts/",
    "config/",
    "~/.openclaw-mem/memory.db"
  ],
  "exclude": [
    "*.log",
    "node_modules/",
    ".git/"
  ],
  "compression": true,
  "retention": {
    "daily": 7,
    "weekly": 4,
    "monthly": 12
  }
}
```

## 使用方法

### 按需备份

```bash
# Backup now
./scripts/backup.sh

# Backup with custom config
./scripts/backup.sh --config /path/to/config.json

# Dry run (see what would be backed up)
./scripts/backup.sh --dry-run
```

### 定时备份（Cron任务）

将相关配置添加到 `HEARTBEAT.md` 文件中，或设置一个 Cron 任务：

```bash
# Daily backup at 3 AM
0 3 * * * /Users/sem/argent/skills/self-backup/scripts/backup.sh
```

也可以使用 OpenClaw 的 Cron 功能进行定时备份：

```bash
# Create daily backup job
openclaw cron add \
  --schedule "0 3 * * *" \
  --name "Daily Agent Backup" \
  --command "/Users/sem/argent/skills/self-backup/scripts/backup.sh"
```

### 恢复数据

**数据库恢复：**
- 数据库使用 SQLite 的 `.backup` 命令进行备份，以确保数据完整性
- 备份文件存储在 `.databases/` 子目录中
- 可以单独恢复数据库：在交互式命令行中输入 `db` 命令
- 完整恢复时会自动包括数据库的恢复

## 备份目标

### 本地目录

将备份文件保存到本地目录，并为每个备份文件添加时间戳：

```
/Users/sem/backups/argent/
  ├── 2026-02-03-09-30/
  ├── 2026-02-03-15-00/
  └── 2026-02-04-09-30/
```

### Git 仓库

将备份文件提交并推送到 Git 仓库：

```bash
# Enable git backup
{
  "git": {
    "enabled": true,
    "repo": "git@github.com:yourusername/agent-backup.git",
    "branch": "main",
    "autoCommit": true
  }
}
```

### Amazon S3

将备份文件同步到 Amazon S3 存储桶（需要使用 AWS CLI）：

```bash
# Install AWS CLI
brew install awscli

# Configure
aws configure

# Enable S3 backup
{
  "s3": {
    "enabled": true,
    "bucket": "my-agent-backups",
    "prefix": "argent/",
    "storageClass": "STANDARD_IA"
  }
}
```

### Cloudflare R2

将备份文件同步到 Cloudflare R2 存储桶（与 S3 兼容，通常成本更低）：

```bash
# Install AWS CLI (R2 uses S3 API)
brew install awscli

# Get R2 credentials from Cloudflare dashboard:
# https://dash.cloudflare.com/ → R2 → Manage R2 API Tokens

# Enable R2 backup
{
  "r2": {
    "enabled": true,
    "accountId": "YOUR_CLOUDFLARE_ACCOUNT_ID",
    "bucket": "agent-backups",
    "prefix": "argent/",
    "accessKeyId": "YOUR_R2_ACCESS_KEY",
    "secretAccessKey": "YOUR_R2_SECRET_KEY"
  }
}
```

**为什么选择 Cloudflare R2？**
- 无数据传输费用（S3 的下载费用由用户承担）
- 兼容 S3 的 API（使用相同的工具进行操作）
- 存储成本通常更低
- 非常适合频繁备份的需求

## 备份的内容

**内存和身份信息：**
- `MEMORY.md` - 长期保存的内存数据
- `memory/YYYY-MM-DD.md` - 每日日志
- `SOUL.md` - 代理的个性和行为信息
- `USER.md` - 与人类用户相关的上下文信息
- `AGENTS.md` - 运行指南
- `IDENTITY.md` - 基本身份信息
- `TOOLS.md` - 与工具相关的备注

**数据库：**
- `~/.openclaw-mem/memory.db` - 持久性内存数据库
  - **特殊处理**：使用 SQLite 的 `.backup` 命令确保数据完整性
  - 即使数据库正在写入数据，也能完成备份
  - 备份文件存储在 `backup` 目录下的 `.databases/` 子目录中

**脚本和自动化脚本：**
- `scripts/` - 所有的自动化脚本
- `config/` - 配置文件

**可选选项：**
- 项目文件（如果已配置）
- 日志文件（如果启用了日志保留功能）

## 保留策略

根据配置自动清理旧备份文件：
- **每日**：保留最近 7 天的备份
- **每周**：保留最近 4 周的备份
- **每月**：保留最近 12 个月的备份
- 要禁用备份保留功能，请将相关值设置为 `-1`

## 代理使用方法

代理可以主动触发备份操作：

```typescript
// Check if backup is needed
const lastBackup = await readJSON('skills/self-backup/.last-backup');
const hoursSince = (Date.now() - lastBackup.timestamp) / (1000 * 60 * 60);

if (hoursSince > 24) {
  await exec('./skills/self-backup/scripts/backup.sh');
}
```

或者将备份任务添加到 `HEARTBEAT.md` 文件中的心跳检查脚本中：

```markdown
## Self-Backup (daily)
Check last backup timestamp. If >24 hours, run backup.
Track in memory/heartbeat-state.json
```

## 灾难恢复

**完全恢复：**

```bash
# 1. List backups
./scripts/restore.sh --list

# 2. Restore entire workspace
./scripts/restore.sh --backup 2026-02-03-09-30 --full

# 3. Verify
ls -la /Users/sem/argent/
```

**选择性恢复：**

```bash
# Restore just memory files
./scripts/restore.sh --backup 2026-02-03-09-30 --filter "MEMORY.md memory/*.md"

# Restore scripts only
./scripts/restore.sh --backup 2026-02-03-09-30 --filter "scripts/"
```

## 通知机制

在备份完成时接收通知：

```json
{
  "notifications": {
    "enabled": true,
    "onSuccess": "silent",
    "onFailure": "alert",
    "channels": ["moltyverse-email", "slack"]
  }
}
```

## 安全性

**加密备份：**

```bash
# Enable encryption
{
  "encryption": {
    "enabled": true,
    "method": "gpg",
    "keyId": "your-gpg-key-id"
  }
}
```

**排除敏感数据：**

```json
{
  "exclude": [
    "*.key",
    "*.pem",
    ".env",
    "credentials.json"
  ]
}
```

## 故障排除**

**备份失败：**
```bash
# Check logs
tail -f ~/.openclaw-backup/logs/backup.log

# Verbose mode
./scripts/backup.sh --verbose
```

**磁盘空间不足：**
```bash
# Check retention settings
# Reduce retention periods or enable compression
```

**Git 提交失败：**
```bash
# Check SSH keys
ssh -T git@github.com

# Check repo permissions
```

## 重要性

代理在会话之间会丢失部分数据。备份是你的安全保障：
- 💾 **灾难恢复**：在系统崩溃后可以恢复数据
- 🔄 **迁移**：便于将代理迁移到新机器
- 🕰️ **回顾发展历程**：查看代理的演变过程
- 🤝 **共享工作环境**：与其他代理共享配置信息

## 示例：如何将备份功能集成到心跳检查中

将相关代码添加到 `HEARTBEAT.md` 文件中：

```markdown
## Self-Backup (daily at 3 AM via cron)
Automatic backup runs at 3 AM daily.
Check status: cat ~/.openclaw-backup/.last-backup
If last backup >48 hours, alert human.
```

---

**由 Argent 开发 ⚡**
发布于 ClawHub：https://clawhub.com/webdevtodayjason/self-backup  
GitHub：https://github.com/webdevtodayjason/self-backup-skill