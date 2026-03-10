---
name: openclaw-backup-restore
description: 将 OpenClaw 的配置文件、代理程序、会话记录以及工作区数据备份到私有 Git 仓库中，或从该仓库中恢复这些数据。此功能适用于用户需要手动触发备份操作、将系统迁移到新机器上，或从之前的配置状态恢复系统的情况。
---
# OpenClaw 备份与恢复

这是一项专门用于管理 OpenClaw 数据生命周期的技能。该技能通过使用外部由 Git 管理的备份目录来保持生产环境的整洁性，并确保数据能够被完全恢复。

## 策略

1. **隔离**：Git 操作在独立的目录中进行，远离实际的 `.openclaw` 运行时环境，以避免数据污染。
2. **精简备份内容**：备份过程中会排除 `node_modules`、日志文件和临时文件等大型文件。
3. **冗余备份**：可以通过 Cron 任务定期自动执行备份操作。

---

## 设置

在使用此技能之前，您需要在 `openclaw.json` 文件中设置您的私有备份仓库 URL。脚本会使用该 URL 来上传和下载数据。

```bash
openclaw config set skills.entries.openclaw-backup-restore.env.OPENCLAW_BACKUP_REPO "git@github.com:your-username/your-repo.git"
```

## 如何备份

要手动执行备份并将数据同步到远程仓库，请按照以下步骤操作：
1. 代理程序需要执行位于该技能 `scripts/` 目录下的 `backup.sh` 脚本。
2. 脚本会：
   - 从 OpenClaw 配置文件中读取仓库 URL。
   - 使用 `rsync` 命令将 `${HOME}/.openclaw/` 目录的内容同步到 `${HOME}/openclaw-backup/` 目录（同时遵循 `.gitignore` 文件中的排除规则）。
   - 添加时间戳后提交更改，并将备份推送到远程的 `main` 分支。

**触发语句**：`Backup OpenClaw now`（立即备份 OpenClaw 数据），`Sync my data to GitHub`（将我的数据同步到 GitHub）。

---

## 如何恢复

要在新机器或现有机器上恢复 OpenClaw 环境，请按照以下步骤操作：
1. 确保您的 SSH 密钥已添加到相应的 Git 服务提供商（例如 GitHub）中。
2. 代理程序需要执行位于该技能 `scripts/` 目录下的 `restore.sh` 脚本。
3. 恢复过程包括：
   - 从 OpenClaw 配置文件中读取仓库 URL。
   - 从配置的仓库中克隆或拉取最新的备份数据。
   - 将文件同步回 `${HOME}/.openclaw/` 目录。
   - 重新安装 Node.js 依赖项，并运行 `openclaw doctor --yes` 命令来修正环境路径设置。
4. 重启 OpenClaw 服务：`openclaw gateway restart`。

**触发语句**：`Restore OpenClaw from backup`（从备份中恢复 OpenClaw），`Migrate my data`（迁移我的数据）。

---

## 技术细节

- **备份目录**：`${HOME}/openclaw-backup`
- **源目录**：`${HOME}/.openclaw`
- **排除的文件和目录**：在技能的 `.gitignore` 文件中列出（包括 `node_modules/`、`logs/`、`completions/`、`tmp/`、`dist/` 等目录）。

---

## 恢复检查清单

如果在 **全新的机器上** 进行恢复，请执行以下步骤：
1. 首先安装 OpenClaw 的命令行工具（CLI）。
2. 设置 `OPENCLAW_BACKUP_REPO` 配置项。
3. 配置与 Git 服务提供商的 SSH 访问权限。
4. 运行该技能提供的恢复脚本。
5. 如果需要重新安装 OpenClaw 服务，请运行 `openclaw onboard` 命令。