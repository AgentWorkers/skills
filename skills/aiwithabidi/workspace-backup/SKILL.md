---
name: workspace-backup
description: Automated workspace backup to GitHub — git-based with auto-generated commit messages, proper .gitignore, and restore procedures. Cron-friendly for hands-free backup. Use for backing up your OpenClaw workspace, skills, memory, and configuration.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: git, GitHub SSH access
metadata: {"openclaw": {"emoji": "\ud83d\udcbe", "requires": {"bins": ["git"]}, "homepage": "https://www.agxntsix.ai"}}
---

# 💾 工作区备份

这是一个基于 Git 的自动化备份工具，用于将您的 OpenClaw 工作区备份到 GitHub。该脚本可以设置为定时任务（cron job）或按需运行。

## 主要功能

- 通过一条命令完成备份，并自动生成提交信息
- 为 OpenClaw 工作区智能配置 `.gitignore` 文件
- 在提交信息中包含文件变更的时间戳和摘要
- 可以从历史记录中的任意时间点恢复数据
- 非常适合使用 cron 任务执行（无需终端）

## 设置步骤

### 1. 初始化备份仓库

```bash
cd ~/.openclaw/workspace
git init
git remote add origin git@github.com:YOUR_USER/YOUR_REPO.git
```

### 2. 确保 SSH 密钥已配置

该脚本使用 SSH 进行数据推送。请确保您的部署密钥（deploy key）或 SSH 密钥已正确配置。

### 3. 运行备份脚本

```bash
bash {baseDir}/scripts/backup.sh
```

### 4. 将脚本设置为定时任务

在 OpenClaw 中创建一个 cron 任务：

```json
{
  "name": "workspace-backup",
  "schedule": "0 */6 * * *",
  "command": "bash /home/node/.openclaw/workspace/skills/workspace-backup/{baseDir}/scripts/backup.sh",
  "description": "Backup workspace to GitHub every 6 hours"
}
```

或者通过系统的 crontab 文件进行设置：
```
0 */6 * * * cd /home/node/.openclaw/workspace && bash skills/workspace-backup/{baseDir}/scripts/backup.sh >> /tmp/backup.log 2>&1
```

## 恢复数据的方法

### 恢复整个工作区到最新备份状态
```bash
cd ~/.openclaw/workspace
git fetch origin
git reset --hard origin/main
```

### 从历史记录中恢复特定文件
```bash
git log --oneline -- path/to/file          # find the commit
git checkout <commit-hash> -- path/to/file  # restore it
```

### 恢复到特定时间点
```bash
git log --oneline --before="2026-02-01"    # find commit near that date
git checkout <commit-hash>                  # detached HEAD at that point
# Copy what you need, then: git checkout main
```

### 查看两次备份之间的文件变化
```bash
git log --oneline -10
git diff <older-hash> <newer-hash> --stat
```

## `.gitignore` 文件的配置

如果系统中没有 `.gitignore` 文件，该脚本会自动生成一个，其中包含以下被排除的文件和目录：

- `.venv/` — Python 虚拟环境
- `.data/` — 本地数据库和数据文件
- `.env` — 保密的环境变量
- `node_modules/` — Node.js 依赖库
- `__pycache__/` — Python 字节码文件
- `*.pyc` — 编译后的 Python 文件
- `.DS_Store` — macOS 的元数据文件

## 脚本说明

| 脚本名称 | 功能说明 |
|--------|-------------|
| `{baseDir}/scripts/backup.sh` | 主备份脚本，负责添加文件到仓库、提交更改并推送到 GitHub |

## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，代码仓库位于 [GitHub](https://github.com/aiwithabidi)。

该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)