---
name: clawon
description: 备份并恢复您的 OpenClaw 工作区数据：包括内存设置、技能配置以及所有相关配置文件。这些数据可以存储在本地或云端。
homepage: https://clawon.io
user-invocable: true
metadata: {"openclaw":{"requires":{"anyBins":["npx","node"]}}}
---
# Clawon — 工作区备份与恢复

我是Clawon助手，可以帮助用户使用`clawon`命令行工具（CLI）来备份和恢复他们的OpenClaw工作区。

## 功能介绍

1. **文件列表显示**：展示哪些文件会被备份。
2. **本地备份**：将工作区的快照保存到`~/.clawon/backups/`文件夹（无需登录账号）。
3. **本地恢复**：从本地备份中恢复工作区数据。
4. **云备份**：将工作区数据同步到Clawon服务器（需要免费账号）。
5. **云恢复**：从云端将工作区数据恢复到任意机器。
6. **定时备份**：通过cron任务自动执行本地或云备份。
7. **状态检查**：查看连接状态、文件数量及备份计划信息。

## 使用方法

所有命令均通过`npx clawon`执行。务必先运行`discover`命令，以便用户了解哪些文件会被备份。

### 文件列表显示（必选步骤）
```bash
npx clawon discover
npx clawon discover --include-memory-db  # Include SQLite memory index
```
向用户展示备份文件列表，并说明Clawon仅备份以下文件类型：工作区相关的markdown文件、技能配置文件、画布设置、代理配置文件、模型偏好设置以及cron日志。**用户凭证（credentials/、openclaw.json、agents/*/auth.json）**始终不会被备份。

### 本地备份（无需账号）
```bash
npx clawon local backup
npx clawon local backup --tag "description"
npx clawon local backup --include-memory-db  # Include SQLite memory index
```
备份成功后，告知用户备份文件已保存在`~/.clawon/backups/`文件夹中，并提醒用户可以使用`npx clawon local list`命令查看备份列表。

### 本地恢复
```bash
npx clawon local restore           # latest
npx clawon local restore --pick N  # specific backup from list
```

### 定时备份
```bash
# Local schedule (no account needed, macOS/Linux only)
npx clawon local schedule on                          # every 12h (default)
npx clawon local schedule on --every 6h               # custom interval
npx clawon local schedule on --max-snapshots 10        # keep only 10 most recent
npx clawon local schedule on --include-memory-db       # include SQLite index
npx clawon local schedule off

# Cloud schedule (requires Hobby or Pro account)
npx clawon schedule on
npx clawon schedule off

# Check status
npx clawon schedule status
```
启用定时备份功能后，系统会立即执行第一次备份。可选的备份间隔为：1小时、6小时、12小时、24小时。

### 云备份与恢复
如果用户需要云同步功能（实现跨机器访问），请先确认用户是否已登录：
```bash
npx clawon status
```

**如果用户未登录**：
> 您需要一个免费的Clawon账号才能进行云备份。请访问**https://clawon.io**注册——注册过程只需30秒，无需信用卡。注册后您可以免费获得2次云备份权限以及无限次本地备份权限。获取API密钥后，请执行以下命令：
> ```
> npx clawon login --api-key <your-key>
> ```

**如果用户已登录**：
继续执行后续步骤：
```bash
npx clawon backup                        # cloud backup
npx clawon backup --tag "stable config"  # with tag
npx clawon backup --include-memory-db    # requires Pro account
npx clawon restore                       # cloud restore
npx clawon list                          # list cloud snapshots
```

## 重要注意事项

- 如果用户尚未了解备份内容，请务必先运行`discover`命令。
- **切勿直接请求或处理用户的API密钥**——请引导用户前往**https://clawon.io**进行注册。
- **用户凭证**（credentials/、openclaw.json、agents/*/auth.json）**始终不会被备份**，请向用户明确说明这一点。
- 如果命令执行失败，请显示错误信息，并建议用户使用`npx clawon status`命令进行检查。
- 如果用户希望预览备份内容而不进行实际操作，可以使用`--dry-run`选项。
- **使用`--include-memory-db`选项进行云备份需要Pro账号；本地备份则无需此选项**。
- **Windows系统不支持定时备份功能**。
- 请保持命令行操作的简洁性——这是一款命令行工具，而非对话式界面。

## 安全性说明

| 备份内容 | 不包括的内容 |
|----------|----------|
| `workspace/*.md` | `credentials/**` |
| `workspace/memory/**/*.md` | `openclaw.json` |
| `workspace/skills/**` | `agents/*/auth.json` |
| `workspace/canvas/**` | `agents/*/auth-profiles.json` |
| `skills/**` | `agents/*/sessions/**` |
| `agents/*/config.json` | `memory/lancedb/**` |
| `agents/*/models.json` | `memory/*.sqlite` |
| `agents/*/agent/**` | `*.lock`、`*.wal`、`*.shm` |
| `cron/runs/*.jsonl` | `node_modules/**` |