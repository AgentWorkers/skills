---
name: update-plus
description: OpenClaw 的完整备份、更新及恢复功能：包括配置文件、工作区以及各项技能设置，并支持自动回滚功能。
version: 4.0.3
metadata: {"openclaw":{"emoji":"🔄","requires":{"bins":["git","jq","rsync"]}}}
---

# 🔄 Update Plus

这是一个专为 OpenClaw 环境设计的全面备份、更新和恢复工具。通过自动回滚、加密备份以及云同步功能，保护您的配置文件、工作区和技能设置。

## 快速入门

```bash
# Check for available updates
update-plus check

# Create a full backup
update-plus backup

# Update everything (creates backup first)
update-plus update

# Preview changes (no modifications)
update-plus update --dry-run

# Restore from backup
update-plus restore openclaw-backup-2026-01-25-12:00:00.tar.gz
```

## 主要功能

| 功能 | 说明 |
|---------|-------------|
| **全面备份** | 备份整个环境（配置文件、工作区和技能设置） |
| **自动备份** | 每次更新前自动创建备份 |
| **自动回滚** | 如果更新失败，可恢复到之前的版本 |
| **智能恢复** | 恢复全部或部分内容（配置文件、工作区） |
| **多目录管理** | 支持区分生产环境（prod）和开发环境（dev），并设置不同的更新策略 |
| **加密备份** | 支持 GPG 加密备份 |
| **云同步** | 可通过 rclone 将备份文件上传至 Google Drive、S3 或 Dropbox |
| **通知功能** | 通过 WhatsApp、Telegram 或 Discord 接收更新通知 |
| **网络重试机制** | 在网络故障时自动重试（可配置） |

## 安装

```bash
git clone https://github.com/hopyky/update-plus.git ~/.openclaw/skills/update-plus
```

### 将工具添加到系统路径

```bash
mkdir -p ~/bin
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
ln -sf ~/.openclaw/skills/update-plus/bin/update-plus ~/bin/update-plus
```

## 配置

创建 `~/.openclaw/update-plus.json` 文件：

```json
{
  "backup_dir": "~/.openclaw/backups",
  "backup_before_update": true,
  "backup_count": 5,
  "backup_paths": [
    {"path": "~/.openclaw", "label": "config", "exclude": ["backups", "logs"]},
    {"path": "~/.openclaw/workspace", "label": "workspace", "exclude": ["node_modules"]}
  ],
  "skills_dirs": [
    {"path": "~/.openclaw/skills", "label": "prod", "update": true}
  ],
  "notifications": {
    "enabled": false,
    "target": "+1234567890"
  },
  "connection_retries": 3,
  "connection_retry_delay": 60
}
```

## 命令行工具

| 命令 | 说明 |
|---------|-------------|
| `update-plus check` | 检查是否有可用更新 |
| `update-plus backup` | 创建全面备份 |
| `update-plus update` | 更新 OpenClaw 及所有相关技能 |
| `update-plus update --dry-run` | 预览更新内容 |
| `update-plus restore <file>` | 从备份文件中恢复数据 |
| `update-plus install-cron` | 安装自动更新任务（每天凌晨 2 点执行） |
| `update-plus uninstall-cron` | 卸载自动更新任务 |

## 更新日志

### v4.0.3
- 在备份前先检查是否需要更新（如果已是最新版本，则跳过备份）
- 当无需更新时，避免浪费带宽和存储空间 |
- 使用 curl 替代 ping 进行连接检测（更可靠） |
- 支持通过防火墙以及 Mac 从睡眠状态唤醒后的连接 |

### v4.0.2
- 使用 curl 替代 ping 进行连接检测（更可靠） |
- 可在通过防火墙或 Mac 从睡眠状态唤醒后正常使用 |
- 为 cron 任务添加了 Homebrew 路径检测功能（`/opt/homebrew/bin`） |
- 将 `~/bin` 添加到 cron 的系统路径中，以支持本地符号链接 |
- 更新了示例配置文件，使其更符合实际使用习惯 |

### v4.0.0
- 仅支持 OpenClaw（移除了对 moltbot/clawdbot 的旧版本支持） |
- 简化了配置流程和路径设置 |
- 配置文件位置：`~/.openclaw/update-plus.json`

### v3.x
- 支持多款机器人（OpenClaw、moltbot、clawdbot） |
- 为 cron 任务添加了网络重试机制 |

## 开发者

由 **hopyky** 创建

## 许可证

MIT 许可证