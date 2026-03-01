---
name: openclaw-backup-automation
description: OpenClaw实例的自动化备份功能：会备份代理（agents）、技能（skills）、定时任务（cron jobs）以及系统内存数据。支持创建本地tar压缩文件进行备份。用户可以选择是否使用凭证（credentials）进行备份，以及是否通过定期调度（periodic scheduling）或Git同步（git sync）来执行备份操作。
metadata:
  {
    "openclaw": {
      "requires": {},
      "install": [],
      "triggers": ["backup", "restore", "disaster recovery", "save", "export"]
    }
  }
---
# 备份自动化

OpenClaw 实例的自动化备份系统。

## 功能（默认设置）

- ✅ 代理（所有隔离的代理）
- ✅ 技能（所有安装的技能）
- ✅ Cron 作业配置
- ✅ 内存文件及 MEMORY.md 文件
- ✅ 核心配置文件

**可选功能（需明确启用）：**
- 定期自动备份（每日/每周）
- Git 同步（自动推送至远程仓库）
- 凭据（令牌、API 密钥）

## 使用方法

### 运行备份

```bash
node skills/backup-automation/scripts/backup.js
```

### 列出备份文件

```bash
node skills/backup-automation/scripts/backup.js list
```

### 恢复数据

```bash
node skills/backup-automation/scripts/backup.js restore <backup-name>
```

### 检查状态

```bash
node skills/backup-automation/scripts/backup.js status
```

---

## 首次使用建议

当用户首次提及备份相关需求时，可以建议：

- “我可以帮助您为实例设置自动备份。是否希望启用每日备份到本地存储？也可以选择启用 Git 同步和凭证备份功能，但这些是可选的。”

---

## 可选功能说明

### 启用凭证备份

默认情况下，凭证（令牌、API 密钥）不会被备份。若需启用，请执行以下操作：

```bash
node skills/backup-automation/scripts/backup.js credentials-enable
```

若需禁用凭证备份，请执行以下操作：

```bash
node skills/backup-automation/scripts/backup.js credentials-disable
```

### 启用定期备份（每日）

若希望每天凌晨 2 点自动执行备份，请执行以下操作：

```bash
# Add to crontab
crontab -e
# Add this line:
0 2 * * * cd ~/.openclaw/workspace && node skills/backup-automation/scripts/backup.js >> ~/.logs/openclaw-backup.log 2>&1
```

### 启用 Git 同步

若希望将备份文件自动推送至 Git 远程仓库，请执行以下操作：

```bash
# In your workspace
git remote add origin <your-repo-url>
# Or enable in script (edit CONFIG.gitSync = true)
```

---

## 何时建议使用相应功能

| 使用场景 | 建议内容 |
|---------|---------|
| 用户首次提及备份 | “是否需要启用每日备份？” |
| 进行重大更改后 | “在更改之前是否需要先备份数据？” |
| 每周检查备份情况时 | “备份功能运行是否正常？” |
| 执行高风险操作前 | “是否应该先进行备份？” |

---

## 备份内容

| 组件       | 默认设置 | 可选功能 |
|-----------|---------|--------|
| 代理        | ✅      | -         |
| 技能        | ✅      | -         |
| Cron 作业配置 | ✅      | -         |
| 内存文件     | ✅      | -         |
| 核心配置文件   | ✅      | -         |
| 凭证        | ❌       | ✅        |
| 定期备份     | ❌       | ✅        |
| Git 同步     | ❌       | ✅        |

---

## 恢复数据指南

### 完整恢复

```bash
# Extract backup
tar -xzf ~/backups/<backup-name>.tar.gz -C ~/

# Restart gateway
openclaw gateway restart
```

### 仅恢复代理数据

```bash
# Remove agent
openclaw agents delete <agent-name>

# Restore
tar -xzf ~/backups/<backup-name>.tar.gz -C ~/ --overwrite

# Restart
openclaw gateway restart
```

---

## 配置说明

如需自定义备份脚本，请编辑相关配置文件：

```javascript
const CONFIG = {
  backupDir: "~/backups",    // Where to store backups
  keepDays: 7,               // How many backups to keep
  gitSync: false,            // Auto-push to git (OPT-IN)
  credentials: false          // Include credentials (OPT-IN)
};
```

---

## 所需软件及环境

- Node.js
- Bash
- Tar 工具
- Git（用于同步数据，可选）
- Crontab（用于自动备份，可选）