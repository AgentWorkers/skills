---
name: Git (Essentials + Workflows + Advanced)
slug: git
version: 1.0.7
description: 完整的版本控制功能，包括必要的命令、团队工作流程、分支策略以及恢复技术。
homepage: https://clawic.com/skills/git
changelog: Translated all auxiliary files to English
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["git"]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md`。默认设置为“最佳实践模式”（无需配置）。

## 使用场景

适用于需要掌握 Git 技能的用户——从基本操作到复杂工作流程。该工具可处理分支管理、合并、基线重构、冲突解决以及团队协作等任务。

## 架构

数据存储在 `~/git/` 目录下。具体结构请参阅 `memory-template.md`。

```
~/git/
└── memory.md    # User preferences (optional)
```

## 快速参考

| 主题 | 文件名 |
|-------|------|
| 基本命令 | `commands.md` |
| 高级操作 | `advanced.md` |
| 分支策略 | `branching.md` |
| 冲突解决 | `conflicts.md` |
| 代码历史与恢复 | `history.md` |
| 团队工作流程 | `collaboration.md` |
| 设置指南 | `setup.md` |
| 内存管理 | `memory-template.md` |

## 核心规则

1. **切勿强制推送到共享分支**——仅在特性分支（feature branches）上使用 `--force-with-lease` 选项。
2. **尽早提交，频繁提交**——小规模的提交更易于审查、回滚和进行故障排除（bisect）。
3. **编写有意义的提交信息**——提交信息的第一行长度应少于 72 个字符，并使用祈使句式。
4. **推送前先拉取代码**——始终执行 `git pull --rebase` 以避免合并冲突。
5. **合并前进行代码清理**——使用 `git rebase -i` 合并相关的修复提交。

## 团队工作流程

**特性分支（Feature Branch）流程：**
1. 从主分支（main）创建特性分支：`git checkout -b feature/name`
2. 进行代码修改并定期推送：`git commit`
3. 提交更改并请求审查：`git push`
4. 合并修改到主分支：`git merge`
5. 删除特性分支：`git branch -d feature-name`

**热修复（Hotfix）流程：**
1. 从主分支创建热修复分支：`git checkout -b hotfix/issue`
2. 修复问题并测试代码：`git commit`
3. 将热修复代码合并到主分支以及开发分支（如果存在）：`git merge`
4. 给修复版本添加标签：`git tag`

**每日同步：**
```bash
git fetch --all --prune
git rebase origin/main  # or merge if team prefers
```

## 提交信息规范

- 使用标准的提交格式：`类型(范围): 描述`
- 提交信息的第一行长度应少于 72 个字符。
- 常见提交类型包括：`feat`（新增功能）、`fix`（修复问题）、`docs`（修改文档）、`style`（优化代码风格）、`refactor`（重构代码）、`test`（测试代码）、`chore`（日常维护）。

## 安全推送规则

- 使用 `git push --force-with-lease` 而非 `--force`——以防止覆盖他人的代码。
- 如果推送被拒绝，先执行 `git pull --rebase` 再重试。
- 绝不要强制推送到主分支（main/master）。

## 冲突解决

- 编辑冲突文件后，确认没有遗留冲突标记：`grep -r "<<<\|>>>\|===" .`
- 合并前确保代码能够正常编译。
- 如果合并过程复杂，使用 `git merge --abort` 中止合并，然后尝试使用 `git rebase`。

## 分支管理规范

- 在本地删除已合并的分支：`git branch -d 分支名称`
- 清理远程分支的跟踪记录：`git fetch --prune`
- 创建 Pull Request 之前，先将特性分支重基线到最新的主分支。
- 在推送前使用 `git rebase -i` 合并复杂的提交。

## 安全检查清单

在执行破坏性操作（如 `reset --hard`、`rebase`、`force push`）之前，请确认：
- [ ] 这是否是一个共享分支？→ 不要修改代码历史记录。
- [ ] 有未提交的更改吗？→ 先将更改暂存或提交。
- [ ] 我是否在正确的分支上？→ 使用 `git branch` 进行确认。
- [ ] 远程分支是否是最新的？→ 先执行 `git fetch`。

## 常见错误与解决方法

- **`git user.email` 设置错误**——在重要提交前使用 `git config user.email` 核对。
- **目录为空**——Git 会忽略空目录，请为这些目录添加 `.gitkeep` 文件。
- **子模块（Submodules）**——克隆时务必使用 `--recurse-submodules` 选项。
- **HEAD 指向错误的分支**——使用 `git switch -` 返回到正确的分支。
- **推送被拒绝**——通常需要先执行 `git pull --rebase`。
- **使用 `stash pop` 时出现问题**——会导致暂存内容丢失，改用 `stash apply`。
- **大文件处理**——对于超过 50MB 的文件，请使用 Git LFS；切勿提交敏感信息。
- **大小写敏感问题**——Mac/Windows 系统不区分大小写，Linux 系统会区分大小写，这可能导致持续集成（CI）失败。

## 数据恢复命令

- 撤销最近一次提交并保留更改：`git reset --soft HEAD~1`
- 恢复未暂存的更改：`git restore 文件名`
- 查找丢失的提交记录：`git reflog`（保留约 90 天的提交历史）
- 恢复被删除的分支：`git checkout -b 分支名称 <sha-from-reflog>`
- 当提交包含多个更改时，使用 `git add -p` 进行部分暂存。

## 使用二分查找（Bisect）进行调试

查找引入错误的提交：```bash
git bisect start
git bisect bad                    # current commit is broken
git bisect good v1.0.0            # this version worked
# Git checks out middle commit, test it, then:
git bisect good                   # or git bisect bad
# Repeat until Git finds the culprit
git bisect reset                  # return to original branch
```

## 总结

```bash
git status -sb                    # short status with branch
git log --oneline -5              # last 5 commits
git shortlog -sn                  # contributors by commit count
git diff --stat HEAD~5            # changes summary last 5 commits
git branch -vv                    # branches with tracking info
git stash list                    # pending stashes
```

## 相关技能

如果用户需要，可以使用以下命令进行安装：
- `clawhub install <slug>`：用于配置 GitLab CI/CD 和合并请求管理。
- `docker`：用于容器化工作流程。
- `code`：用于代码质量和最佳实践的维护。

## 反馈建议

- 如果觉得本文档有用，请给 `clawhub` 添加星标（star）：`clawhub star git`
- 保持信息更新：`clawhub sync`