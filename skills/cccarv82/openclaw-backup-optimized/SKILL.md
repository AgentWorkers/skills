---
name: openclaw-backup-optimized
description: "**优化的 OpenClaw 备份功能**：  
该功能支持创建完整的系统快照，并具备工作区文件归档、变更摘要生成、恢复操作指导以及 Discord 通知等功能。适用于需要设置自动化备份任务、配置定时备份脚本，或记录/恢复 OpenClaw 系统状态的场景。  
**主要特性包括：**  
- **完整系统快照**：能够生成包含所有系统数据的完整快照。  
- **工作区文件归档**：自动将工作区中的文件和目录打包到备份文件中。  
- **变更摘要**：为每次备份生成详细的变更记录，便于快速了解文件内容的更新情况。  
- **恢复操作指导**：提供详细的恢复步骤，确保用户能够轻松恢复系统到备份状态。  
- **Discord 通知**：在备份完成或发生重要变更时，通过 Discord 发送通知，提高用户反馈效率。  
**使用场景：**  
- **自动化备份**：用于配置自动化备份流程，确保数据安全。  
- **备份脚本**：与备份脚本集成，实现批量备份操作。  
- **系统状态记录**：帮助管理员监控和记录系统的备份历史。  

**适用场景：**  
- 当您需要设置或运行自动化备份任务时。  
- 当您需要配置定时备份任务以保障数据安全时。  
- 当您需要记录或恢复 OpenClaw 系统的状态时。  
**触发条件：**  
- 备份自动化流程触发。  
- 备份脚本执行完毕时。  
- 快照或恢复操作完成时。  
- GitHub 仓库中的备份文件更新时。"
---

# OpenClaw 备份（优化版）

## 该功能的用途

使用此功能可以**安装、配置并运行**优化的 OpenClaw 备份流程：
- 对 `~/.openclaw` 目录进行完整备份
- 将工作区文件分割成约 90MB 的多个部分，并为每个部分生成 SHA256 哈希值
- 通过 Discord 发送详细的通知（包含备份摘要和恢复步骤）
- 保留最近 N 条备份记录

## 相关文件

- 脚本：`scripts/backup.js`（跨平台通用）
- 参考配置文件：`references/CONFIG.md`

## 安装/配置

1) 将脚本复制到您的工具文件夹中：
```bash
cp scripts/backup.js ~/.openclaw/workspace/tools/openclaw-backup.js
```

2) 配置环境变量（详见 `references/CONFIG.md`）：

**macOS/Linux (bash/zsh):**
```bash
export OPENCLAW_HOME="$HOME/.openclaw"
export OPENCLAW_BACKUP_DIR="$HOME/.openclaw-backup"
export BACKUP_REPO_URL="https://github.com/your/repo.git"
export BACKUP_CHANNEL_ID="1234567890"
export BACKUP_TZ="America/Sao_Paulo"
export BACKUP_MAX_HISTORY=7
```

**Windows (PowerShell):**
```powershell
$env:OPENCLAW_HOME="$env:USERPROFILE\.openclaw"
$env:OPENCLAW_BACKUP_DIR="$env:USERPROFILE\.openclaw-backup"
$env:BACKUP_REPO_URL="https://github.com/your/repo.git"
$env:BACKUP_CHANNEL_ID="1234567890"
$env:BACKUP_TZ="America/Sao_Paulo"
$env:BACKUP_MAX_HISTORY="7"
```

3) 运行一次脚本以完成初始配置：
```bash
node ~/.openclaw/workspace/tools/openclaw-backup.js
```

4) 设置定时任务（OpenClaw 的定时任务在网关环境中执行）：
```bash
openclaw cron add --name "openclaw-backup-daily" \
  --cron "0 5,10,15,20 * * *" --tz "America/Sao_Paulo" \
  --exec "node ~/.openclaw/workspace/tools/openclaw-backup.js"
```

## 恢复数据

请按照备份通知中的说明进行数据恢复。

## 注意事项

- 该备份方案会排除那些会导致备份差异较大的、处于锁定状态或已被删除的文件。
- 需要安装 `git` 和 `node`（版本 >= 18）。
- 通知功能通过 `openclaw message send` 实现（不使用 Webhook）。
- `scripts/openclaw-backup.sh` 是旧版本的脚本（仅适用于 Linux/macOS），将会被替换为 `backup.js`。