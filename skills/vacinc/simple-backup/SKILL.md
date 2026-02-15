---
name: simple-backup
description: 将备份代理的“大脑”（工作区数据）和“身体”（状态数据）备份到本地文件夹，并可选地通过 rclone 工具同步到云端。
metadata: {"openclaw":{"emoji":"💾","requires":{"bins":["rclone","gpg","tar","jq"]}}}
---

# 简单备份脚本

这是一个功能强大的备份脚本，具备以下特性：
1. **自动检测** OpenClaw 配置文件中指定的工作区（workspace）和状态目录（state directory）；
2. **支持自定义设置**，以便适应非标准的环境配置；
3. 使用 GPG（AES256）对备份数据进行压缩和加密；
4. **定期删除旧备份文件**（支持每日或每小时删除策略）；
5. **可选地** 通过 `rclone` 工具将备份文件同步到云端。

## 设置

1. **依赖项：**
    ```bash
    brew install rclone gnupg jq
    ```

2. **加密密码：** 设置用于加密的密码（请选择一种方式）：
    - 文件：`~/.openclaw/credentials/backup.key`（推荐）
    - 环境变量：`export BACKUP_PASSWORD="secret"`
    - 配置文件：在技能配置（skill config）中添加 `"password": "secret"`。

3. **云端存储（可选）：**
    ```bash
    rclone config
    ```

## 使用方法

```bash
simple-backup
```

## 自动检测

默认情况下，脚本会从 `~/.openclaw/openclaw.json` 文件中自动获取以下路径：
- **工作区路径：** `agentsdefaults_workspace`
- **状态目录路径：** `~/.openclaw`（存放 OpenClaw 配置文件的位置）
- **备份目录路径：** `<workspace>/BACKUPS`

## 自定义配置

对于非标准的环境配置，可以修改 `~/.openclaw/openclaw.json` 文件中的相关路径设置。

```json
{
  "skills": {
    "entries": {
      "simple-backup": {
        "config": {
          "workspaceDir": "/custom/path/workspace",
          "stateDir": "/custom/path/state",
          "skillsDir": "/custom/path/skills",
          "backupRoot": "/custom/path/backups",
          "remoteDest": "gdrive:backups"
        }
      }
    }
  }
}
```

## 配置参考

| 配置键                | 环境变量                | 是否自动检测            | 说明                                      |
|-------------------|-------------------|-------------------|----------------------------------------|
| `workspaceDir`         | `BRAIN_DIR`           | `agentsdefaults_workspace`     | 代理（agent）的工作区路径                 |
| `stateDir`         | `BODY_DIR`           | `~/.openclaw`          | OpenClaw 的状态数据目录                   |
| `skillsDir`         | `SKILLS_DIR`          | `~/openclaw/skills`         | 技能（skills）目录                         |
| `backupRoot`         | `BACKUP_ROOT`         | `<workspace>/BACKUPS`       | 本地备份存储目录                         |
| `remoteDest`         | `REMOTEDEST`         | （未设置时为空）         | Rclone 的远程存储路径                         |
| `maxDays`         | `MAX_DAYS`           | 7                   | 保留每日备份文件的天数                         |
| `hourlyRetentionHours`    | `HOURLY_RETENTION_HOURS`     | 24                   | 保留每小时备份文件的小时数                         |
| `password`         | `BACKUP_PASSWORD`         | （未设置时为空）         | 用于加密的密码                         |

**配置优先级：** 配置文件 → 环境变量 → 自动检测