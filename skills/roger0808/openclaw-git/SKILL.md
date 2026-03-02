---
name: openclaw-git
description: Git automation for OpenClaw workspace. Use when user needs to commit and push changes from /home/roger/.openclaw to the remote repository. Triggers on: git commit, git push, save changes, backup openclaw.
---

# OpenClaw Git

用于 OpenClaw 工作区的自动化 Git 提交和推送操作。

## 快速入门

### 提交并推送更改

```bash
# Default commit message
~/.openclaw/workspace/skills/openclaw-git/scripts/git-push.sh

# Custom commit message
~/.openclaw/workspace/skills/openclaw-git/scripts/git-push.sh "Your commit message"
```

## 功能说明

1. 提交 `/home/roger/.openclaw` 目录中的所有更改。
2. 将所有更改添加到暂存区（`git add .`）。
3. 添加提交信息（默认信息为：“update: $(date)”）。
4. 将更改推送到远程仓库（origin/main）。

## 在技能上传工作流中的使用

在将技能上传到 ClawHub 时，使用 OpenClaw Git 来备份工作区的所有更改：

### 完整的技能上传工作流

```bash
# Step 1: Upload skill to ClawHub (manual or scripted)
cd ~/.openclaw/workspace/skills/<skill-name>
clawhub publish . --version <version> --changelog "description"

# Step 2: Commit and push all workspace changes using OpenClaw Git
~/.openclaw/workspace/skills/openclaw-git/scripts/git-push.sh "Upload <skill-name> v<version> and sync workspace"

# Alternative: Use default timestamp message
~/.openclaw/workspace/skills/openclaw-git/scripts/git-push.sh
```

### 被备份的内容

- 技能代码的更改
- 文档更新（SKILL.md、TOOLS.md、MEMORY.md）
- 配置文件
- 学习记录（.learnings）
- 每日的记忆记录文件

### 集成点

此脚本会在“技能上传”工作流结束后自动执行，以确保所有更改在完成上传前都被保存到 Git 中。

---

## 先决条件

- 在 `/home/roger/.openclaw` 目录中已初始化 Git 仓库。
- 配置了远程仓库（origin）。
- 已配置了登录凭据（或使用 SSH 密钥）。

## 凭据信息

GitHub：
- 用户名：Roger0808
- Token：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

## 脚本参考

有关自动化脚本的详细信息，请参阅 [scripts/git-push.sh](scripts/git-push.sh)。