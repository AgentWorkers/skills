---
name: git-summary
description: 快速获取当前 Git 仓库的概要信息，包括仓库状态、最近的提交记录、分支以及贡献者列表。
user-invocable: true
metadata: {"openclaw": {"emoji": "📊", "requires": {"bins": ["git"]}, "os": ["darwin", "linux", "win32"]}}
---

# Git 综合技能

该技能提供了对当前 Git 仓库状态的全面概述。

## 使用方法

当用户请求 Git 总结、仓库概览或希望了解 Git 项目的当前状态时，可以在终端中运行以下命令，并以清晰、有条理的格式展示结果。

## 指令

1. **仓库状态**：运行 `git status --short --branch` 以获取当前分支和工作目录的状态。

2. **最近提交的记录**：运行 `git log --oneline -10 --decorate` 以显示带有分支/标签标记的最近 10 条提交记录。

3. **分支概览**：运行 `git branch -a --list` 以列出所有本地和远程分支。

4. **远程信息**：运行 `git remote -v` 以显示已配置的远程仓库。

5. **未提交的更改摘要**：
   - 运行 `git diff --stat` 查看未暂存的更改。
   - 运行 `git diff --cached --stat` 查看已暂存的更改。

6. **贡献者**（可选，用于提供更多背景信息）：运行 `git shortlog -sn --all | head -10` 以显示排名前 10 的贡献者。

## 输出格式

以结构化的格式展示收集到的信息：

```
## 📊 Git Repository Summary

### Current Branch & Status
- Branch: `<branch_name>`
- Status: <clean/dirty with X modified, Y staged, Z untracked>

### Recent Commits (Last 10)
<formatted commit list>

### Branches
- Local: <count> branches
- Remote: <count> branches
<list notable branches>

### Remotes
<list remotes with URLs>

### Uncommitted Changes
<summary of staged and unstaged changes>
```

## 注意事项

- 如果当前环境不是 Git 仓库，请告知用户，并建议使用 `git init` 初始化一个新仓库。
- 对于大型仓库，显示贡献者列表可能需要一些时间；如果预计会出现这种情况，请提前提醒用户。
- 请注意某些信息可能具有敏感性——不要公开包含敏感信息的完整 URL。