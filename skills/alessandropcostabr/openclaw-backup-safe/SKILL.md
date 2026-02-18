---
name: openclaw-backup
description: >
  **备份与恢复 OpenClaw 数据**  
  当用户需要创建备份、设置自动备份计划、从备份中恢复数据或管理备份策略时，可以使用该功能。该功能会正确处理 `~/.openclaw` 目录的归档操作，并确保某些文件或文件夹被排除在备份范围之外。
---
# OpenClaw 备份

用于备份和恢复 OpenClaw 的配置信息、凭据以及工作区数据。

## 创建备份

运行备份脚本：

```bash
./scripts/backup.sh [backup_dir]
```

默认备份路径：`~/openclaw-backups/`

备份文件名称：`openclaw-YYYY-MM-DD_HHMM.tar.gz`

## 备份的内容：

- `openclaw.json` - 主配置文件
- `credentials/` - API 密钥、令牌
- `agents/` - 代理配置文件、认证信息
- `workspace/` - 内存数据、SOUL.md 文件、用户文件
- `telegram/` - 会话数据
- `cron/` - 定时任务配置

## 不会被备份的内容：

- `completions/` - 缓存数据（会自动重新生成）
- `*.log` - 日志文件

## 使用 Cron 设置每日备份

使用 OpenClaw 的 Cron 任务实现每日自动备份，并设置通知功能：

```json
{
  "name": "daily-backup",
  "schedule": {"kind": "cron", "expr": "0 3 * * *", "tz": "UTC"},
  "payload": {
    "kind": "agentTurn",
    "message": "Run ~/.openclaw/workspace/skills/openclaw-backup/scripts/backup.sh and report result to user."
  },
  "sessionTarget": "isolated",
  "delivery": {"mode": "announce"}
}
```

## 恢复数据

请参阅 [references/restore.md](references/restore.md) 以获取详细的恢复步骤。

**快速恢复方法：**

```bash
openclaw gateway stop
mv ~/.openclaw ~/.openclaw-old
tar -xzf ~/openclaw-backups/openclaw-YYYY-MM-DD_HHMM.tar.gz -C ~
openclaw gateway start
```

## 备份文件轮换

该脚本会自动保留最近 7 份备份文件。