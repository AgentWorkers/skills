---
name: Git
slug: git
version: 1.0.4
description: Git 版本控制。
homepage: https://clawic.com/skills/git
changelog: Added essential commands reference and advanced operations guide. Now covers stash, tags, cherry-pick, bisect, worktree, reflog, and sparse checkout.
---
## 使用场景

用户需要具备 Git 的专业知识，从基本操作到复杂的工作流程都能熟练掌握。该工具（Agent）可处理分支管理、合并、重新基线（rebase）、冲突解决以及团队协作相关的任务。

## 快速参考

| 主题 | 文件名 |
|-------|------|
| 基本命令 | `commands.md` |
| 高级操作 | `advanced.md` |
| 分支策略 | `branching.md` |
| 冲突解决 | `conflicts.md` |
| 代码历史与恢复 | `history.md` |
| 团队协作 | `collaboration.md` |

## 核心规则

1. **切勿强制推送到共享分支**——仅在特性分支（feature branches）上使用 `--force-with-lease` 选项。
2. **尽早提交，频繁提交**——小规模的提交更易于审核、回滚或进行故障排除（bisect）。
3. **编写有意义的提交信息**——提交信息的第一行长度应控制在 72 个字符以内，并使用祈使句式。
4. **推送前先拉取代码**——在推送之前务必执行 `git pull --rebase`，以避免合并冲突。
5. **合并前进行代码清理**——使用 `git rebase -i` 合并相关的修复提交（fixup commits）。

## 推送安全注意事项

- 使用 `git push --force-with-lease` 而不是 `--force`，以防止覆盖他人的代码。
- 如果推送被拒绝，先执行 `git pull --rebase` 再重试。
- 绝不要强制推送到 `main` 或 `master` 分支。

## 提交信息规范

- 使用标准的提交格式：`类型（范围）：描述`
- 提交信息的第一行长度应控制在 72 个字符以内。
- 仅在项目有统一要求时才包含提交范围（scope）。

## 冲突解决

- 编辑冲突文件后，确认没有遗留标记：`grep -r "<<<\|>>>\|==" .`
- 在完成合并之前测试代码是否能正常编译。
- 如果合并过程变得复杂，使用 `git merge --abort` 中止操作，然后尝试使用 `git rebase`。

## 分支维护

- 在本地删除已合并的分支：`git branch -d 分支名`
- 在创建 Pull Request（PR）之前，将特性分支重新基线到最新的 `main` 分支。
- 在推送之前，使用 `git rebase -i` 合并杂乱无章的提交。

## 恢复操作

- 回退上一次提交的同时保留修改内容：`git reset --soft HEAD~1`
- 删除未暂存的修改：`git restore 文件名`
- 当一次提交包含多个修改时，使用 `git add -p` 进行部分暂存。

## 常见误区

- 在进行重要提交之前，确认 `git user.email` 与预期的提交者信息一致。
- 空目录不会被 Git 跟踪——如有需要，添加 `.gitkeep` 文件。
- 使用子模块时，务必使用 `--recurse-submodules` 选项进行克隆。
- 在尝试推送之前，检查远程分支是否已被删除。

## 安全检查清单

在执行可能破坏代码的操作之前，请确认：
- [ ] 这是一个共享分支吗？→ 不要修改代码历史记录。
- [ ] 我有未提交的修改吗？→ 先将修改暂存或提交。
- 我在正确的分支上吗？→ 使用 `git branch` 进行确认。
- 远程分支是否是最新的？→ 先执行 `git fetch`。

## 相关技能

如果用户需要，可以使用以下命令进行安装：
- `clawhub install <slug>`：
  - `gitlab`：用于 GitLab 的持续集成/持续部署（CI/CD）和合并请求管理。
  - `docker`：用于结合版本控制的容器化工作流程。
  - `javascript`：用于 Web 开发的 JavaScript 相关技能。

## 反馈建议

- 如果觉得本文档有用，请使用 `clawhub star git` 给予支持。
- 保持信息更新：定期执行 `clawhub sync` 命令。