---
name: git-crypt-backup
description: 使用 `git-crypt` 加密技术，将 Clawdbot 的工作空间和配置文件备份到 GitHub。这适用于每日自动备份或手动备份/恢复操作。
---

# Git-Crypt 备份

自动将 Clawdbot 工作区（`~/clawd`）和配置文件（`~/.clawdbot`）备份到 GitHub，并使用 git-crypt 对敏感文件进行加密。

## 设置

### 1. 创建 GitHub 仓库（建议使用私有仓库）

```bash
# Create two private repos on GitHub:
# - <username>/clawdbot-workspace
# - <username>/clawdbot-config
```

### 2. 初始化 git-crypt

```bash
# Install git-crypt
brew install git-crypt  # macOS
# apt install git-crypt  # Linux

# Workspace repo
cd ~/clawd
git init
git-crypt init
git remote add origin git@github.com:<username>/clawdbot-workspace.git

# Config repo
cd ~/.clawdbot
git init
git-crypt init
git remote add origin git@github.com:<username>/clawdbot-config.git
```

### 3. 配置加密

**工作区 `.gitattributes`：**
```
SOUL.md filter=git-crypt diff=git-crypt
USER.md filter=git-crypt diff=git-crypt
HEARTBEAT.md filter=git-crypt diff=git-crypt
MEMORY.md filter=git-crypt diff=git-crypt
memory/** filter=git-crypt diff=git-crypt
```

**配置文件 `.gitattributes`：**
```
clawdbot.json filter=git-crypt diff=git-crypt
.env filter=git-crypt diff=git-crypt
credentials/** filter=git-crypt diff=git-crypt
telegram/** filter=git-crypt diff=git-crypt
identity/** filter=git-crypt diff=git-crypt
agents/**/sessions/** filter=git-crypt diff=git-crypt
nodes/** filter=git-crypt diff=git-crypt
```

**配置文件 `.gitignore`：**
```
*.bak
*.bak.*
.DS_Store
logs/
media/
browser/
subagents/
memory/
update-check.json
*.lock
```

### 4. 导出密钥（非常重要！）

```bash
mkdir -p ~/clawdbot-keys
cd ~/clawd && git-crypt export-key ~/clawdbot-keys/workspace.key
cd ~/.clawdbot && git-crypt export-key ~/clawdbot-keys/config.key
```

⚠️ **请安全地存储这些密钥**（例如：1Password、iCloud Keychain、U盘等）

### 5. 进行首次提交并推送

```bash
cd ~/clawd && git add -A && git commit -m "Initial backup" && git push -u origin main
cd ~/.clawdbot && git add -A && git commit -m "Initial backup" && git push -u origin main
```

## 每日备份

运行 `scripts/backup.sh` 脚本：

```bash
~/clawd/skills/git-crypt-backup/scripts/backup.sh
```

或者设置定时任务（cron job）以实现每日自动备份。

## 在新机器上恢复数据

```bash
# 1. Clone repos
git clone git@github.com:<username>/clawdbot-workspace.git ~/clawd
git clone git@github.com:<username>/clawdbot-config.git ~/.clawdbot

# 2. Unlock with keys
cd ~/clawd && git-crypt unlock /path/to/workspace.key
cd ~/.clawdbot && git-crypt unlock /path/to/config.key
```

## 被加密的文件

| 仓库 | 加密后的文件 | 明文文件 |
|------|-----------|-------|
| 工作区 | SOUL/USER/HEARTBEAT/MEMORY.md, memory/** | AGENTS.md, IDENTITY.md, TOOLS.md, drafts/** |
| 配置文件 | clawdbot.json, .env, credentials/**, sessions/** | cron/jobs.json, settings/** |