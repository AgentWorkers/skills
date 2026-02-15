---
name: claw-sync
description: OpenClaw 提供了安全的数据同步功能，用于管理内存和工作区的数据。您可以使用 `/sync` 命令进行数据推送，`/restore` 命令进行数据拉取，以及 `/sync-status` 命令来检查同步状态。该系统支持版本化的数据备份，并具备灾难恢复能力。
commands:
  - name: sync
    description: Push memory and skills to remote repository
    usage: /sync [--dry-run]
    run: node skills/claw-sync/index.js sync
  - name: restore
    description: Restore memory and skills from remote
    usage: /restore [latest|<version>] [--force]
    run: node skills/claw-sync/index.js restore
  - name: sync-status
    description: Show sync configuration and local backups
    usage: /sync-status
    run: node skills/claw-sync/index.js status
  - name: sync-list
    description: List all available backup versions
    usage: /sync-list
    run: node skills/claw-sync/index.js list
---

# Claw Sync

为 OpenClaw 提供的安全、版本控制的同步功能，用于管理内存和工作区数据。

## 命令

### /sync
将您的内存数据和技能信息推送到远程仓库。
```
/sync              → Push and create versioned backup
/sync --dry-run    → Preview what would be synced
```

### /restore
从远程仓库恢复内存数据和技能信息。
```
/restore                        → Restore latest version
/restore latest                 → Same as above
/restore backup-20260202-1430   → Restore specific version
/restore latest --force         → Skip confirmation
```

### /sync-status
显示同步配置和本地备份信息。
```
/sync-status
```

### /sync-list
列出所有可用的备份版本。
```
/sync-list
```

---

## 同步的内容

| 文件 | 说明 |
|------|-------------|
| `MEMORY.md` | 长期存储的内存数据 |
| `USER.md` | 用户配置文件 |
| `SOUL.md` | 代理角色信息 |
| `IDENTITY.md` | 代理身份信息 |
| `TOOLS.md` | 工具配置文件 |
| `AGENTS.md` | 工作区规则 |
| `memory/*.md` | 每日日志 |
| `skills/*` | 自定义技能信息 |

## 不会同步的内容（出于安全考虑）

- `openclaw.json` - 包含 API 密钥 |
- `.env` - 包含敏感信息 |

## 必需的设置

创建 `~/.openclaw/.backup.env` 文件：
```
BACKUP_REPO=https://github.com/username/your-repo
BACKUP_TOKEN=ghp_your_token
```

## 功能特点

- 🏷️ **版本控制**：每次同步都会生成一个可恢复的版本 |
- 💾 **灾难恢复**：每次恢复前都会进行本地备份 |
- 🔒 **安全性**：不会同步配置文件，并对敏感数据进行加密处理 |
- 🖥️ **跨平台支持**：支持 Windows、Mac 和 Linux 系统