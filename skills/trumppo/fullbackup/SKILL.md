---
name: fullbackup
description: 使用现有的 `backup-local.sh` 脚本，为 OpenClaw 工作区和配置创建一个完整的本地备份。该备份文件可用于 Telegram 中的 `/fullbackup` 功能，或在用户请求完整本地备份时使用。
---

# 完整备份（本地存档）

## 概述
运行本地完整备份脚本，并将生成的存档文件存储在 `/root/.openclaw/backups` 目录下。

## 快速开始
运行随附的封装脚本：
```bash
bash /root/.openclaw/workspace/skills/fullbackup/scripts/full-backup.sh
```

## 输出
输出存档文件的路径和大小。

## 注意事项
- 备份脚本会自动排除一些不需要备份的文件（如缓存文件和日志文件）。
- 请勿删除旧的备份文件。