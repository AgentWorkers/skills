---
name: Git
slug: git
version: 1.0.8
description: "Git提交、分支、基线重置（rebase）、合并（merge）、冲突解决（conflict resolution）、历史记录恢复（history recovery）、团队工作流程（team workflows），以及用于日常版本控制的安全操作所需的命令。在以下情况下使用这些内容：  
(1) 当任务涉及Git、仓库（repository）、提交（commit）、分支（branch）、合并（merge）、基线重置（rebase）或拉取请求（pull request）时；  
(2) 当历史记录的安全性、团队协作或数据恢复成为关键问题时；  
(3) 当自动化工具应自动执行Git相关的操作，而非依赖人工临时处理时。"
homepage: https://clawic.com/skills/git
changelog: Simplified the skill name and kept the stateless activation guidance
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["git"]},"os":["linux","darwin","win32"]}}
---
## 使用场景

当任务涉及 Git 仓库、分支、提交（commit）、合并（merge）、基线重置（rebase）、拉取请求（pull request）、冲突解决（conflict resolution）、历史记录检查（history inspection）或数据恢复（recovery）时，请使用这些技能。这些技能是“无状态”的（stateless），只要工作中包含 Git 相关操作，就应该默认应用这些技能。

## 快速参考

| 主题          | 文件          |
|---------------|--------------|
| 基本命令        | `commands.md`      |
| 高级操作        | `advanced.md`      |
| 分支管理策略     | `branching.md`      |
| 冲突解决        | `conflicts.md`      |
| 历史记录与恢复     | `history.md`      |
| 团队工作流程     | `collaboration.md`     |

## 核心规则

1. **切勿强制推送到共享分支（shared branches）**——仅在特性分支（feature branches）上使用 `--force-with-lease` 选项。
2. **尽早提交，频繁提交**——小规模的提交更易于审查、回滚和进行二分查找（bisect）。
3. **编写有意义的提交信息**——提交信息的第一行长度应少于 72 个字符，并使用祈使句式。
4. **推送前先拉取（pull before push）**——在推送之前务必执行 `git pull --rebase`，以避免合并冲突。
5. **合并前进行清理**——使用 `git rebase -i` 合并修复后的提交（fixup commits）。

## 团队工作流程

**特性分支流程（Feature Branch Flow）：**
1. `git checkout -b feature/name` 从主分支（main）创建特性分支。
2. 进行提交并定期推送。
3. 提交 Pull Request（PR）以获取代码审查。
4. 合并修改到主分支。
5. 删除特性分支。

**热修复流程（Hotfix Flow）：**
1. `git checkout -b hotfix/issue` 从主分支创建热修复分支。
2. 修复问题、测试代码并提交。
3. 将修复内容合并到主分支以及开发分支（如果存在的话）。
4. 给修复版本添加标签。

**每日同步（Daily Sync）：**
```bash
git fetch --all --prune
git rebase origin/main  # or merge if team prefers
```

## 提交信息（Commit Messages）

- 使用常规的提交格式：`类型（type）：范围（scope）：描述（description）`
- 提交信息的第一行长度应少于 72 个字符。
- 提交类型包括：`feat`（新增功能）、`fix`（修复问题）、`docs`（文档更新）、`style`（代码风格调整）、`refactor`（代码重构）、`test`（测试）、`chore`（杂务）。

## 推送安全（Push Safety）

- 使用 `git push --force-with-lease` 而不是 `--force`——这样可以防止覆盖他人的工作。
- 如果推送被拒绝，先执行 `git pull --rebase` 再重试。
- 绝不要强制推送到主分支（main/master）。

## 冲突解决（Conflict Resolution）

- 编辑冲突文件后，确认没有残留的标记：`grep -r "<<<\|>>>\|===" .`
- 在完成合并前测试代码是否能够正常编译。
- 如果合并过程变得复杂，使用 `git merge --abort` 中断操作，然后尝试使用 `git rebase`。

## 分支管理（Branch Management）

- 在本地删除已合并的分支：`git branch -d 分支名称`。
- 清理远程分支的跟踪记录：`git fetch --prune`。
- 在创建 Pull Request 之前，将特性分支重基线到最新的主分支。
- 在推送之前使用 `git rebase -i` 合并混乱的提交。

## 安全检查清单（Safety Checklist）

在执行破坏性操作（如 `reset --hard`、`rebase`、`force push`）之前，请确认：
- [ ] 这是一个共享分支吗？→ 不要修改历史记录。
- [ ] 我有未提交的更改吗？→ 先将更改暂存或提交。
- [ ] 我在正确的分支上吗？→ 使用 `git branch` 进行确认。
- [ ] 远程分支是否是最新的？→ 先执行 `git fetch`。

## 常见错误

- **`git user.email` 设置错误**——在重要提交前使用 `git config user.email` 进行检查。
- **目录为空**——Git 不会跟踪空目录，请添加 `.gitkeep` 文件。
- **子模块（submodules）**——克隆时务必使用 `--recurse-submodules` 选项。
- **HEAD 指向错误的分支**——使用 `git switch -` 返回到正确的分支。
- **推送被拒绝**——通常需要先执行 `git pull --rebase`。
- **在解决冲突时使用 `stash pop`**——可能会导致暂存的内容丢失，改用 `stash apply`。
- **大文件**——对于超过 50MB 的文件，请使用 Git LFS；切勿提交敏感信息。
- **大小写敏感问题**——Mac/Windows 系统不区分大小写，Linux 系统会区分大小写，这可能导致持续集成（CI）失败。

## 数据恢复命令（Recovery Commands）

- 撤销上一个提交并保留更改：`git reset --soft HEAD~1`
- 恢复未暂存的更改：`git restore 文件名`
- 查找丢失的提交记录：`git reflog`（保留约 90 天的历史记录）
- 恢复已删除的分支：`git checkout -b 分支名称 <从 reflog 中获取的 SHA>`。
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

## 总结（Quick Summary）___

## 相关技能（Related Skills）

如果用户需要，可以使用以下工具进行安装：
- `clawhub install <slug>`：用于集成 GitLab 的持续集成/持续部署（CI/CD）和 Pull Request 功能。
- `docker`：用于容器化工作流程。
- `code`：用于代码质量和最佳实践管理。

## 反馈（Feedback）

- 如果觉得这些内容有用，请给项目点赞：`clawhub star git`。
- 保持信息更新：`clawhub sync`。