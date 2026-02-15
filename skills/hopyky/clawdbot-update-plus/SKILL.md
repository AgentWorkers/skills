---
name: clawdbot-update-plus
description: Clawdbot的全备份、更新及恢复功能：包括配置文件、工作区数据以及各项技能设置，并支持自动回滚功能。
version: 2.1.1
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":["git","jq","rsync"],"commands":["clawdbot"]}}}
---

# 🔄 Clawdbot Update Plus

这是一个全面的备份、更新和恢复工具，适用于您的整个Clawdbot环境。通过自动回滚、加密备份和云同步功能，保护您的配置文件、工作区和技能设置。

## 快速入门

```bash
# Check for available updates
clawdbot-update-plus check

# Create a full backup
clawdbot-update-plus backup

# Update everything (creates backup first)
clawdbot-update-plus update

# Preview changes (no modifications)
clawdbot-update-plus update --dry-run

# Restore from backup
clawdbot-update-plus restore clawdbot-update-2026-01-25-12:00:00.tar.gz
```

## 主要功能

| 功能 | 描述 |
|---------|-------------|
| **完整备份** | 备份整个环境（配置文件、工作区和技能设置） |
| **自动备份** | 每次更新前自动创建备份 |
| **自动回滚** | 如果更新失败，可恢复到之前的版本 |
| **智能恢复** | 恢复全部或部分数据（配置文件、工作区） |
| **多目录支持** | 支持针对生产环境（prod）和开发环境（dev）分别设置备份策略 |
| **加密备份** | 可选GPG加密 |
| **云同步** | 通过rclone将备份文件上传到Google Drive、S3或Dropbox |
| **通知机制** | 通过WhatsApp、Telegram或Discord接收通知 |
| **模块化架构** | 代码结构清晰，易于维护 |

## 安装

```bash
# Via ClawdHub
clawdhub install clawdbot-update-plus --dir ~/.clawdbot/skills

# Or clone manually
git clone https://github.com/hopyky/clawdbot-update-plus.git ~/.clawdbot/skills/clawdbot-update-plus
```

### 将工具添加到系统路径

创建一个符号链接，以便全局使用该工具：

```bash
mkdir -p ~/bin
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc  # or ~/.bashrc
source ~/.zshrc
ln -sf ~/.clawdbot/skills/clawdbot-update-plus/bin/clawdbot-update-plus ~/bin/clawdbot-update-plus
```

### 所需依赖项

| 依赖项 | 是否必需 | 用途 |
|------------|----------|---------|
| `git` | 是 | 用于从仓库拉取技能更新 |
| `jq` | 是 | 用于解析JSON配置文件 |
| `rsync` | 是 | 用于高效文件复制 |
| `rclone` | 可选 | 用于云存储同步 |
| `gpg` | 可选 | 用于备份文件加密 |

## 配置

创建`~/.clawdbot/clawdbot-update.json`配置文件：

```json
{
  "backup_dir": "~/.clawdbot/backups",
  "backup_before_update": true,
  "backup_count": 5,
  "backup_paths": [
    {"path": "~/.clawdbot", "label": "config", "exclude": ["backups", "logs", "media", "*.lock"]},
    {"path": "~/clawd", "label": "workspace", "exclude": ["node_modules", ".venv"]}
  ],
  "skills_dirs": [
    {"path": "~/.clawdbot/skills", "label": "prod", "update": true},
    {"path": "~/clawd/skills", "label": "dev", "update": false}
  ],
  "remote_storage": {
    "enabled": false,
    "rclone_remote": "gdrive:",
    "path": "clawdbot-backups"
  },
  "encryption": {
    "enabled": false,
    "gpg_recipient": "your-email@example.com"
  },
  "notifications": {
    "enabled": false,
    "target": "+1234567890",
    "on_success": true,
    "on_error": true
  }
}
```

## 备份路径配置

使用`backup_paths`参数配置备份内容：

| 参数 | 描述 |
|--------|-------------|
| `path` | 备份目录（支持使用`~`符号） |
| `label` | 备份文件在日志中的标签 |
| `exclude` | 需要排除的文件或文件夹 |

### 推荐配置方案

```json
"backup_paths": [
  {"path": "~/.clawdbot", "label": "config", "exclude": ["backups", "logs", "media"]},
  {"path": "~/clawd", "label": "workspace", "exclude": ["node_modules", ".venv"]}
]
```

## 技能更新

使用`skills_dirs`参数配置需要更新的技能：

| 参数 | 描述 |
|--------|-------------|
| `path` | 技能目录路径 |
| `label` | 备份文件在日志中的标签 |
| `update` | 是否执行`git pull`操作（true/false） |

### 推荐配置方案

- **生产环境（Prod）**：自动从ClawdHub或GitHub获取更新 |
- **开发环境（Dev）**：仅手动更新（保护开发中的数据）

## 命令行工具

### `backup` — 创建完整备份

```bash
clawdbot-update-plus backup
```

### `list-backups` — 列出所有可用备份

```bash
clawdbot-update-plus list-backups
```

### `update` — 更新所有内容

```bash
# Standard update (with automatic backup)
clawdbot-update-plus update

# Preview changes only
clawdbot-update-plus update --dry-run

# Skip backup
clawdbot-update-plus update --no-backup

# Force continue even if backup fails
clawdbot-update-plus update --force
```

### `restore` — 从备份中恢复数据

```bash
# Restore everything
clawdbot-update-plus restore backup.tar.gz

# Restore only config
clawdbot-update-plus restore backup.tar.gz config

# Restore only workspace
clawdbot-update-plus restore backup.tar.gz workspace

# Force (no confirmation)
clawdbot-update-plus restore backup.tar.gz --force
```

### `check` — 检查是否有更新可用

```bash
clawdbot-update-plus check
```

### `install-cron` — 自动执行更新任务

```bash
# Install daily at 2 AM
clawdbot-update-plus install-cron

# Custom schedule
clawdbot-update-plus install-cron "0 3 * * 0"  # Sundays at 3 AM

# Remove
clawdbot-update-plus uninstall-cron
```

## 通知机制

当更新完成或失败时，系统会发送通知：

```json
"notifications": {
  "enabled": true,
  "target": "+1234567890",
  "on_success": true,
  "on_error": true
}
```

通知渠道的设置方式：
- `+1234567890` → WhatsApp
- `@username` → Telegram
- `channel:123` → Discord

## 云存储设置

### 配置rclone工具

```bash
# Install
brew install rclone  # macOS
curl https://rclone.org/install.sh | sudo bash  # Linux

# Configure
rclone config
```

### 在配置文件中启用云存储功能

```json
"remote_storage": {
  "enabled": true,
  "rclone_remote": "gdrive:",
  "path": "clawdbot-backups"
}
```

## 加密备份

```json
"encryption": {
  "enabled": true,
  "gpg_recipient": "your-email@example.com"
}
```

## 日志记录

所有操作都会被记录到`~/.clawdbot/backups/update.log`文件中：

```
[2026-01-25 20:22:48] === Update started 2026-01-25 20:22:48 ===
[2026-01-25 20:23:39] Creating backup...
[2026-01-25 20:23:39] Backup created: clawdbot-update-2026-01-25-20:22:48.tar.gz (625M)
[2026-01-25 20:23:39] Clawdbot current version: 2026.1.22
[2026-01-25 20:23:41] Starting skills update
[2026-01-25 20:23:41] === Update completed 2026-01-25 20:23:41 ===
[2026-01-25 20:23:43] Notification sent to +1234567890 via whatsapp
```

**日志保留策略**：超过30天的日志会自动删除。

## 数据保留规则

| 数据类型 | 保留策略 | 配置参数 |
|------|-----------|--------|
| 本地备份 | 保留最近N份备份 | `backup_count: 5` |
| 远程备份 | 保留最近N份备份 | 与本地相同 |
| 日志文件 | 保留30天 | 自动删除 |

## 架构（v2.0）

```
bin/
├── clawdbot-update-plus     # Main entry point
└── lib/
    ├── utils.sh             # Logging, helpers
    ├── config.sh            # Configuration
    ├── backup.sh            # Backup functions
    ├── restore.sh           # Restore functions
    ├── update.sh            # Update functions
    ├── notify.sh            # Notifications
    └── cron.sh              # Cron management
```

## 更新日志

### v2.0.0
- 完整重构架构 |
- 模块化设计（分为7个独立模块） |
- 代码更简洁（每个模块约150行，而非之前的1000多行） |
- 改进了错误处理机制 |
- 支持使用标签进行智能恢复 |
- 自动识别通知渠道 |
- 修复了`--no-backup`参数被忽略的问题 |
- 日志记录更加详细，并支持自动清理 |
- 实现了本地和远程备份的保留策略 |

### 其他版本更新记录

### v1.7.0
- 引入了基于标签的智能恢复功能 |
- 自动识别备份文件格式 |

### v1.6.0
- 新增了`backup_paths`参数，支持完整环境备份 |
- 将备份逻辑与更新逻辑分离 |

### v1.5.0
- 支持多目录备份（通过`skills_dirs`参数配置）

### v1.4.0
- 增加了通过Clawdbot发送通知的功能

### v1.3.0
- 新增了`check`、`diff-backups`和`install-cron`命令

## 开发者

由 **hopyky** 创建

## 许可证

MIT许可证