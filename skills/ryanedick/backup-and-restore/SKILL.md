---
name: backup
description: OpenClaw 的备份、恢复、灾难恢复及迁移功能：支持将数据加密后存储在本地（`~/.openclaw/` 目录）或云存储服务（如 S3、R2、B2、GCS、Google Drive）中。当用户需要了解备份、快照、灾难恢复或从备份中恢复 OpenClaw 的相关操作时，可使用此功能。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["gpg", "tar"], "optionalBins": ["jq", "aws", "gsutil", "gcloud", "b2", "rclone", "rsync"] },
        "env": ["BACKUP_PASSPHRASE", "BACKUP_ENCRYPT", "BACKUP_RETAIN_DAYS", "BACKUP_STOP_GATEWAY", "BACKUP_DIR"],
        "credentials": ["~/.openclaw/credentials/backup/backup-passphrase"],
        "optionalCredentials": ["~/.openclaw/credentials/backup/aws-credentials", "~/.openclaw/credentials/backup/r2-credentials", "~/.openclaw/credentials/backup/b2-credentials", "~/.openclaw/credentials/backup/gcs-key.json", "~/.openclaw/credentials/backup/rclone.conf"],
      },
  }
---

# 备份功能

您可以备份并恢复整个 OpenClaw 安装环境，包括配置文件、凭据、工作区数据、内存内容以及所有技能相关的数据。

## 所需工具

**必备工具：** `gpg`、`tar`（通常在 Linux 系统中已预安装）

**可选工具（用于上传到云端）：** `jq`、`aws`（用于 AWS S3/R2）、`gsutil`/`gcloud`（用于 Google Cloud Storage）、`b2`（用于 Backblaze）、`rclone`（用于 Google Drive）、`rsync`

**环境变量：**  
`BACKUP_PASSPHRASE`、`BACKUP_ENCRYPT`、`BACKUP_RETAIN DAYS`、`BACKUP_STOP/GateWAY`、`BACKUP_DIR`

**凭据文件**（在安装过程中生成，存储在 `~/.openclaw/credentials/backup/` 目录下）：  
- `backup-passphrase`：用于加密备份  
- `aws-credentials`、`r2-credentials`、`b2-credentials`、`gcs-key.json`、`rclone.conf`：根据所使用的云服务提供商选择性地配置

## 快速入门

```bash
# Run a backup now — creates TWO files: full (encrypted) + workspace-only
~/.openclaw/workspace/skills/backup/scripts/backup.sh

# Upload both backups to configured cloud destinations
~/.openclaw/workspace/skills/backup/scripts/upload.sh

# Full restore (same environment / disaster recovery)
~/.openclaw/workspace/skills/backup/scripts/restore.sh ~/backups/openclaw/openclaw-myhost-20260215-full.tar.gz.gpg

# Workspace-only restore (any environment — just the agent's brain)
~/.openclaw/workspace/skills/backup/scripts/restore.sh ~/backups/openclaw/openclaw-myhost-20260215-workspace.tar.gz
```

## 交互式设置

如需进行引导式设置，请阅读 `references/setup-guide.md` 并按照其中的步骤操作。该文档会指导您完成加密设置、备份模式选择、备份计划配置以及云存储目标的设置。

## 手动使用方法

### `backup.sh` — 创建本地备份

每次运行该脚本会生成两个文件：  
1. **完整备份文件`*-full.tar.gz.gpg`**：包含所有数据（包括凭据），经过加密处理，适用于在同一或类似环境中进行灾难恢复。  
2. **工作区备份文件`*-workspace.tar.gz.gpg`**：仅包含 `~/.openclaw/workspace/` 目录下的数据（内存内容、技能相关数据及文件），同样经过加密处理，可以在任何环境中安全恢复，且不会影响网关配置。该文件相当于代理程序的核心数据。

```bash
# Default: creates both files
./scripts/backup.sh

# Skip gateway stop/restart (for testing)
BACKUP_STOP_GATEWAY=false ./scripts/backup.sh
```

备份文件会被保存到 `~/backups/openclaw/` 目录下。

### `upload.sh` — 上传备份到云端

```bash
# Upload latest local backup to all configured destinations
./scripts/upload.sh

# Upload a specific file
./scripts/upload.sh /path/to/backup.tar.gz.gpg
```

### `restore.sh` — 从备份中恢复数据

```bash
# Full restore (disaster recovery — replaces entire ~/.openclaw/)
./scripts/restore.sh openclaw-myhost-20260215-full.tar.gz.gpg

# Workspace-only restore (just the agent brain — keeps your config/credentials)
./scripts/restore.sh openclaw-myhost-20260215-workspace.tar.gz

# Extract only workspace from a full backup
./scripts/restore.sh --workspace-only openclaw-myhost-20260215-full.tar.gz.gpg

# From cloud
./scripts/restore.sh s3://mybucket/openclaw/openclaw-myhost-20260215-workspace.tar.gz
```

该脚本会自动识别工作区备份文件，并在恢复前创建一个备份副本。  

**注意：** 仅恢复工作区数据的操作无需重启网关；代理程序会在下次启动时自动加载新文件。而完整备份会替换整个 `~/.openclaw/` 目录的内容，因此恢复后需要重启网关。

### `test-backup.sh` — 验证备份设置

```bash
./scripts/test-backup.sh
```

该脚本会创建一个小型测试文件，对其进行加密处理后上传到所有指定的云存储目标，然后验证备份是否成功。如果执行成功，脚本会输出 0。

## 配置参考

配置文件位于 `~/.openclaw/workspace/skills/backup/config.json`：  
| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `encrypt` | bool | `true` | 是否使用 AES-256 GPG 对数据进行加密（仅针对完整备份） |
| `retainDays` | 数字 | `30` | 保留本地备份文件的时长（天） |
| `schedule` | 字符串 | `"daily"` | 备份频率（每日、每周或手动） |
| `destinations` | 数组 | `[]` | 云存储目标地址（详见 `destinations.md`） |

## 环境变量

所有配置项均可通过环境变量进行修改：  
| 变量 | 说明 |