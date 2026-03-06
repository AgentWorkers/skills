---
name: quick-backup-restore
description: "当用户请求“备份 OpenClaw”、“恢复快照”、“回滚内存设置”、“检查备份状态”、“查看备份历史记录”、“撤销代理更改”或“设置时间机器备份”时，请使用此功能。"
metadata: { "openclaw": { "emoji": "⏱", "requires": { "bins": ["bash", "openssl"] }, "install": [{ "id": "setup", "kind": "shell", "label": "Run Quick Backup and Restore (time machine) setup", "command": "sudo bash {baseDir}/bin/setup.sh" }], "homepage": "https://github.com/marzliak/quick-backup-restore" } }
---
# ⏱🦞 快速备份与恢复（时间机器功能）

您的 OpenClaw 代理会随着时间的推移不断积累内存数据、偏好设置以及运行上下文信息——而这些代理也可能会出错（例如覆盖现有数据或损坏自身的运行状态）。在这种情况下，您需要回到“精确的”2小时前的状态，而不是使用昨天的备份数据或进行完整的系统恢复。

该功能会为代理生成每小时一次的快照，并使用 Restic 工具进行加密存储。只有在出现故障时，系统才会通过 Telegram 向您发送通知。

## 概述

“快速备份与恢复”功能通过每小时生成一次快照来保护 OpenClaw 的运行时上下文（包括内存数据、会话信息、凭据和配置设置）。该功能通过 cron 任务自动运行，您也可以手动触发备份操作，或者恢复过去 72 小时内的任意数据点。

**存储目录：** `{baseDir}/../../../var/backups/quick-backup-restore`（或根据 `{baseDir}/config.yaml` 中的配置文件指定）  
**日志文件：** `/var/log/quick-backup-restore.log`  
**密码文件：** `/etc/quick-backup-restore.pass`  

---

## 用户请求设置或安装“快速备份与恢复”功能时：

1. 首先检查是否已安装：
   ```bash
   restic -r /var/backups/quick-backup-restore --password-file /etc/quick-backup-restore.pass snapshots 2>/dev/null && echo "Already initialized"
   ```
   如果未安装，需让用户填写 `{baseDir}/config.yaml` 文件中的 `bot_token` 和 `chat_id`，然后运行：
   ```bash
   sudo bash {baseDir}/bin/setup.sh
   ```
   通过查看日志文件 `/var/log/quick-backup-restore.log` 来确认安装是否成功：

   ```bash
   tail -5 /var/log/quick-backup-restore.log
   ```

---

## 用户请求手动备份时：

```bash
sudo bash {baseDir}/bin/backup.sh
```

完成后再次查看日志文件以确认备份是否成功：

```bash
tail -5 /var/log/quick-backup-restore.log
```

---

## 用户请求查看备份状态或历史记录时：

- 查看最近的 10 条日志记录：
   ```bash
   tail -20 /var/log/quick-backup-restore.log
   ```
- 列出所有快照（最新记录在前）：
   ```bash
   restic -r /var/backups/quick-backup-restore --password-file /etc/quick-backup-restore.pass snapshots
   ```
- 查看最近两个快照之间的变化：
   ```bash
   SNAPS=$(restic -r /var/backups/quick-backup-restore --password-file /etc/quick-backup-restore.pass snapshots --json | jq -r '.[-2:][].id')
   restic -r /var/backups/quick-backup-restore --password-file /etc/quick-backup-restore.pass diff $SNAPS
   ```

---

## 用户请求恢复数据时：

- **交互式恢复（推荐，建议先进行测试）：**
   ```bash
   sudo bash {baseDir}/bin/restore.sh
   ```
- **从最新快照中恢复特定文件：**
   ```bash
   sudo bash {baseDir}/bin/restore.sh latest --file /root/.openclaw/workspace/MEMORY.md --target /tmp/tc-restore
   # 预览恢复结果后手动移动文件：
   # cp /tmp/tc-restore/root/.openclaw/workspace/MEMORY.md /root/.openclaw/workspace/MEMORY.md
   ```
- **通过快照 ID 恢复数据：**
   ```bash
   sudo bash {baseDir}/bin/restore.sh <snapshot_id>
   ```
   在执行完整恢复操作之前，请务必先与用户确认。

---

## 用户请求检查备份仓库的完整性时：

```bash
restic -r /var/backups/quick-backup-restore --password-file /etc/quick-backup-restore.pass check
```

---

## 用户请求修改配置时：

请使用用户提供的配置信息（如备份计划、保留策略、存储路径和 Telegram 凭据）更新 `{baseDir}/config.yaml` 文件，然后重新运行 `setup.sh` 命令以应用更改：

```bash
sudo bash {baseDir}/bin/setup.sh
```

---

## 重要说明：

- **静默运行**：`cron` 任务每小时在 05:00 运行一次，并将日志记录到 `/var/log/quick-backup-restore.log`。除非发生故障，否则不会输出任何信息。
- **仅在工作失败时通过 Telegram 发送通知**。如果用户未配置 `bot_token` 和 `chat_id`，则只会记录故障信息。
- **此功能仅用于防止“代理在最近 3 天内造成的问题”**，并非用于灾难性数据恢复（灾难性恢复应依赖外部备份方案，例如将数据备份到远程服务器）。
- **密码安全**：Restic 仓库采用 AES-256 加密，密码存储在 `/etc/quick-backup-restore.pass` 文件中（权限设置为 600）。丢失密码会导致无法访问所有快照。
- **切勿将 `secrets.env` 或 `.pass` 文件提交到 Git 仓库**，这些文件会被 `.gitignore` 文件排除在外。