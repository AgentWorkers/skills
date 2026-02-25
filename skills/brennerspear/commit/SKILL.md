---
name: commit
description: 根据当前的更改创建一个带有上下文信息的 Git 提交，然后推送该分支。
allowed-tools: [Bash]
---
## 上下文信息

- 当前的 Git 状态：!`git status`
- 当前的 Git 差异（已暂存和未暂存的变化）：!`git diff HEAD`
- 当前分支：!`git branch --show-current`
- 最近的提交记录：!`git log --oneline -10`

## 你的任务

根据上述信息，将所有更改暂存到 Git 中，创建一个带有说明性信息的提交，并将当前分支推送到远程仓库（origin）。

所需步骤：
1. 将所有更改暂存到 Git 中。
2. 创建一个提交。
3. 将当前分支推送到远程仓库 origin（如有需要，使用 `--set-upstream origin <branch>`）。

请勿使用交互式命令，也不要输出额外的注释。