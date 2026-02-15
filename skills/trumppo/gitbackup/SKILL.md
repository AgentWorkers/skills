---
name: gitbackup
description: 创建 OpenClaw 工作区仓库的本地 Git 包备份。当在 Telegram 中运行 `/gitbackup` 命令，或者用户要求将 Git 历史记录/引用备份到本地文件时，可以使用此备份。
---

# Git 备份（本地包）

## 概述
创建一个包含工作区仓库内容的独立 Git 包，并将其存储在 `/root/.openclaw/backups` 目录中。

## 快速开始
运行以下脚本：
```bash
bash /root/.openclaw/workspace/skills/gitbackup/scripts/git-backup.sh
```

## 输出
脚本会输出备份包的路径和大小。备份包的文件名中包含 UTC 时间戳。

## 注意事项：
- 如果工作区不是一个 Git 仓库，脚本会输出错误信息并终止执行。
- 请勿删除旧的备份包。