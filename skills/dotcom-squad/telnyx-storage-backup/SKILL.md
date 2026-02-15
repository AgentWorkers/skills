---
name: backup-to-telnyx-storage
description: 将您的 OpenClaw 工作区备份并恢复到 Telnyx 存储空间。这些脚本基于简单的命令行界面（CLI），且不依赖于任何外部工具。
metadata: {"openclaw":{"emoji":"💾","requires":{"bins":["telnyx"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# 备份到 Telnyx 存储

您可以将 OpenClaw 工作区备份到 Telnyx 存储（兼容 S3）。

## 设置（一次性操作）

```bash
# 1. Install Telnyx CLI (if not already)
npm install -g @telnyx/api-cli

# 2. Authenticate
telnyx auth setup
```

就这样。无需使用 boto3，也无需 AWS 凭据或环境变量。

## 使用方法

### 备份

```bash
./backup.sh

# Output:
# 🔄 OpenClaw Backup → Telnyx Storage
# ========================================
# Creating archive: openclaw-backup-20260201-120000.tar.gz
#   + MEMORY.md
#   + SOUL.md
#   + memory/
# ✅ Backup complete: openclaw-backup/openclaw-backup-20260201-120000.tar.gz
```

自定义存储桶和工作区：
```bash
./backup.sh my-bucket ~/my-workspace
```

控制备份保留策略（默认：每 30 分钟生成一次备份，共保留 48 小时）：
```bash
MAX_BACKUPS=100 ./backup.sh
```

### 查看备份列表

```bash
./list.sh

# Output:
# 📋 Available Backups
# ========================================
# Bucket: openclaw-backup
#
#   • openclaw-backup-20260201-120000.tar.gz  1.2M  2/1/2026
#   • openclaw-backup-20260131-180000.tar.gz  1.1M  1/31/2026
```

### 恢复

```bash
# Restore latest backup
./restore.sh latest

# Restore specific backup
./restore.sh openclaw-backup-20260201-120000.tar.gz

# Restore to different location
./restore.sh latest my-bucket ~/restored-workspace
```

## 被备份的文件包括：

- `AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `TOOLS.md`
- `MEMORY.md`, `HEARTBEAT.md`, `GUARDRAILS.md`
- `memory/`, `knowledge/`, `scripts/`

## 定时备份

系统会每 30 分钟自动执行一次备份：

```bash
crontab -e
# Add:
*/30 * * * * ~/skills/backup-to-telnyx-storage/backup.sh >> /tmp/backup.log 2>&1
```

## 价格

Telnix 存储的费用为：**0.023 美元/GB/月**——因此，通常情况下，备份工作区的成本非常低。

## 旧版 Python 脚本

如果您需要兼容 AWS SDK，原始的 `backup.py` 脚本仍然可用：

```bash
pip install boto3
export TELNYX_API_KEY=KEYxxxxx
python3 backup.py
```

注意：推荐使用基于 CLI 的脚本（`backup.sh`, `list.sh`, `restore.sh`），因为它们不需要额外的依赖项，并且能够提供完整的备份、查看备份列表和恢复功能。