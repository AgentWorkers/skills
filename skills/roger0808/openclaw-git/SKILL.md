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

1. 对 `/home/roger/.openclaw` 目录中的文件进行修改。
2. 将所有更改添加到暂存区（`git add .`）。
3. 提交更改，并附上提交信息（默认信息为：“update: $(date)”）。
4. 将更改推送到远程仓库（origin/main）。

## 先决条件

- 在 `/home/roger/.openclaw` 目录下已初始化 Git 仓库。
- 配置了远程仓库（origin）。
- 已配置了登录凭据（或使用 SSH 密钥）。

## 凭据信息

GitHub：
- 用户名：Roger0808
- Token：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

## 脚本参考

有关自动化脚本的详细信息，请参阅 [scripts/git-push.sh](scripts/git-push.sh)。