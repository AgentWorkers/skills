---
name: git-workflows-pro
description: 处理高级的 Git 工作流程和恢复任务。当用户需要在交互式 rebase、提交清理、冲突解决、reflog 恢复、cherry-pick、stash、worktree、bisect、子模块（submodule）与子树（subtree）的选择、稀疏检出（sparse checkout）、分支历史记录分析（branch history analysis），或撤销仓库中的危险操作等方面获得帮助时，请使用此功能。
---
# Git 工作流程

在处理复杂的 Git 任务时，应优先考虑安全性、代码历史的清晰度以及仓库结构的稳定性，而非单一命令的便捷性。

始终将用户的实际目标作为工作核心，尽量选择最简单且安全的 Git 操作序列。

## 核心方法

在建议具体命令之前，需要先明确以下几点：
1. 用户的具体目标
2. 代码历史是否已经与其他人共享
3. 该操作是否会修改提交记录（commit）、引用（reference）、工作目录（working tree）或仓库结构
4. 是否需要先创建一个备份点（用于恢复操作）

如果某个操作具有破坏性或难以撤销的效果，请务必先创建一个备份点。

## 默认的安全规则：
- 在修改代码历史之前，先执行 `git status` 命令查看当前状态。
- 在执行重新基线（rebase）、重置（reset）或强制推送（force-push）操作之前，务必确认当前分支及上游分支的状态。
- 在需要保证代码历史清晰度时，优先选择非破坏性的检查方法。
- 当需要明确操作结果时，建议使用 `git switch` 和 `git restore` 而不是旧式的混合操作方式。
- 在进行可能影响代码历史的操作之前，务必先创建一个备份点。
- 除非用户明确同意，否则避免重写已共享的代码历史。

## 高风险操作时的应对策略（优先考虑恢复）

在风险较高的情况下，应尽早采取以下措施：

```bash
git status
git branch backup/$(date +%Y%m%d-%H%M%S)-preop
```

在进行代码历史恢复之前，务必先进行详细检查：

```bash
git reflog --date=local --decorate -n 30
git log --oneline --graph --decorate -n 30
```

有关基于 reflog 的恢复方法、分支恢复以及强制推送操作导致的错误处理，请参阅 `references/recovery.md`。

## 常见任务类型

### 代码历史清理
- 用于合并多个修复提交（squashing fix commits）
- 重新编写提交信息（rewording commit messages）
- 分割错误的提交（splitting a bad commit）
- 删除意外创建的提交（dropping accidental commits）
- 在合并之前准备分支（preparing a branch）

对于本地代码历史或尚未共享的代码历史，建议使用交互式重新基线（interactive rebase）。

### 错误定位
当用户知道代码的“良好状态”和“错误状态”时，可以使用 `git bisect` 来查找导致问题的具体提交。

### 并行分支管理
- 当用户需要同时查看两个分支、希望拥有更清晰的修复流程或避免使用临时存储区（stash）时，可以使用 `git worktree`。

### 冲突处理
在重新基线、合并、选择性地应用代码更改（cherry-pick）或使用临时存储区时，务必谨慎处理冲突，确保保留用户的原始意图。

### 仓库结构管理
当用户需要了解以下信息时，可以使用 `blame`、`grep`、日志图（log graph）等工具：
- 是谁修改了代码
- 问题是什么时候出现的
- 某一行代码的来源是什么
- 是哪个提交改变了代码的当前行为

### 仓库结构调整
在处理以下操作时需格外小心：
- 子模块（submodules）
- 子树（subtrees）
- 稀疏检视模式（sparse checkout）
- 工作目录的优化（worktree pruning）
- 分支重命名（branch renames）
- 默认分支的迁移（default-branch migration）

如果任务涉及复杂的仓库结构调整（而非简单的日常提交操作），请参阅 `references/advanced-patterns.md`。

## 决策规则

### 重新基线（rebase）与合并（merge）的选择
- 对于清理本地功能分支的历史记录，建议使用重新基线。
- 当需要保留共享分支的历史记录时，建议使用合并。
- 如果分支已经被其他人共享，在执行重新基线之前，务必明确告知用户可能带来的数据重写风险。

### 子树（subtree）与子模块（submodule）的选择
- 当用户希望更简单地使用外部代码资源或减少贡献者之间的混淆时，建议使用子树。
- 当用户确实需要一个固定的外部代码依赖时，建议使用子模块。

### 工作目录（worktree）与临时存储区（stash）的选择
- 对于中等或长时间的并行开发任务，建议使用工作目录。
- 对于短暂的代码切换或小范围的修改，建议使用临时存储区。

### 重置（reset）、恢复（restore）与撤销（revert）的选择
- 对于文件级别的撤销操作，建议使用 `restore`。
- 对于本地代码历史或索引结构的修改，建议使用 `reset`。
- 对于已经共享的提交记录，建议使用 `revert`。

## 指导用户的操作规范：
- 在指导用户时，首先要说明需要检查的内容。
- 提供最安全的操作序列。
- 明确指出操作是否会导致代码历史的修改。
- 在风险较高时，提供相应的恢复路径。

保持命令使用的简洁性，仅在必要时才展示所有 Git 命令的详细选项。

## 需要查阅的参考文档
- 如需了解基于 reflog 的恢复方法、意外重置操作、分支恢复以及强制推送导致的错误处理，请参阅 `references/recovery.md`。
- 如需了解交互式重新基线、提交分割、安全强制推送等操作，请参阅 `references/history-surgery.md`。
- 如需了解工作目录（worktree）、`git bisect`、子模块（submodule）等高级使用技巧，请参阅 `references/advanced-patterns.md`。

## 回复 Git 工作流程问题的模板结构：
- **任务目标**：
- **风险等级**：
- **必要的安全检查步骤**：
- **推荐的命令序列**：
- **恢复操作路径**：
- **关于共享代码历史的注意事项**：