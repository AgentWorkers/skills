---
name: unfuck-my-git-state
description: 使用一种分阶段、低风险的恢复流程来诊断并修复损坏的 Git 状态和工作树元数据。当 Git 报告 HEAD 状态不一致、工作树锁定异常、工作树条目丢失、引用（refs）缺失，或者出现诸如“已检出（already checked out）”、“未知版本号（unknown revision）”、“对象名称无效（not a valid object name）”等错误，以及分支操作失败时，都可以使用此流程进行恢复。
---

# 恢复Git仓库的状态（Recover Git Repository State）

本文档旨在提供一种安全、高效的方法来恢复Git仓库的状态，同时避免进一步破坏仓库的结构或数据。

## 核心规则（Core Rules）

1. **先创建快照**：在尝试任何修复操作之前，务必先创建一个仓库的快照。切勿盲目尝试修复。
2. **优先使用非破坏性修复方法**：尽可能采用不会对仓库数据造成永久性影响的修复方式。
3. **将`.git/`目录视为生产数据**：在备份`.git/`目录之前，应将其视为不可修改的生产环境数据。
4. **使用`git symbolic-ref`**：在手动编辑`.git/HEAD`之前，先使用`git symbolic-ref`来获取分支的引用信息。
5. **每次修复后进行验证**：完成修复后，必须运行`references/recovery-checklist.md`中的验证脚本，确保修复操作没有问题。

## 快速工作流程（Fast Workflow）

1. **收集诊断信息**：使用````bash
bash scripts/snapshot_git_state.sh .
````中的脚本收集仓库的诊断信息。
2. **根据问题症状选择相应的修复方案**：根据收集到的诊断信息，使用`references/symptom-map.md`来选择合适的修复方案。
3. **生成非破坏性的修复命令**：使用````bash
bash scripts/guided_repair_plan.sh --repo .
````中的脚本生成相应的非破坏性修复命令。
4. **应用最小的修复方案**：选择最合适的修复方案进行执行。
5. **运行验证**：执行修复后，必须运行`references/recovery-checklist.md`中的验证脚本。
6. **仅在大规模问题时升级处理**：如果验证失败，才需要进一步升级处理。

## 回归测试机制（Regression Testing）

在修改脚本逻辑之前，先使用````bash
bash scripts/regression_harness.sh
````中的脚本进行一次性回归测试，以确保修复不会引入新的问题。

## 修复方案（Playbooks）

### 修复方案A：孤立的工作树元数据（Orphaned Worktree Metadata）
- **症状**：
  - `git worktree list`显示的路径已不存在。
  - 工作树条目中的哈希值无效或为0。
- **步骤**：
  1. 备份`.git/`目录。
  2. 删除`.git/worktrees/<name>`目录下的无效条目。
  3. 重新运行`git prune`命令。

### 修复方案B：分支锁定问题（Phantom Branch Lock）
- **症状**：
  - `git branch -d`或`git branch -D`命令失败，提示“该分支已被工作树使用”。
  - `git worktree list`显示的分支所有权信息不正确。
- **步骤**：
  1. 找到使用该分支的工作树。
  2. 将该工作树切换到另一个分支，或者将`HEAD`指针分离出来。
  3. 重新尝试在主仓库中执行分支操作。

### 修复方案C：分离的HEAD或冲突的HEAD（Detached/Contradictory HEAD）
- **症状**：
  - `git status`显示HEAD处于分离状态。
  - `git branch --show-current`和`git symbolic-ref -q HEAD`的返回结果不一致。
- **步骤**：
  1. 如果分支上下文未知，从当前提交创建一个救援分支。
  2. 重新连接到目标分支。
  3. 完成修复后，再重新连接回目标分支。

### 修复方案D：缺失或损坏的引用（Missing/Broken References）
- **症状**：
  - 出现“unknown revision”、“not a valid object name”或“cannot lock ref”等错误信息。
- **步骤**：
  1. 使用`reflog`命令恢复本地分支的提交记录。
  2. 在确认数据无误后，再尝试修改分支引用。

## 最后手段：手动修复HEAD（Last Resort: Manual HEAD Repair）
- **条件**：只有在备份`.git/`目录之后，才能进行手动修复。
- **推荐方法**：
  1. 使用````bash
git show-ref --verify refs/heads/<branch>
git symbolic-ref HEAD refs/heads/<branch>
````中的脚本进行修复。
- **备用方法**：
  2. 如果`symbolic-ref`无法使用，立即使用````bash
echo "ref: refs/heads/<branch>" > .git/HEAD
````中的脚本进行修复，并运行验证脚本。

## 验证流程（Verification Process）
必须通过`references/recovery-checklist.md`中的验证脚本。验证内容至少包括：
- `git status`命令的执行结果正常，没有致命错误。
- `git symbolic-ref -q HEAD`返回的分支与预期分支一致。
- `git worktree list --porcelain`显示的所有路径都存在，且哈希值有效。
- `git fsck --no-reflogs --full`命令没有新的严重错误。

## 升级处理流程（Escalation Process）
- **备份仓库**：如果所有验证都失败，需要备份`.git/`目录。
- **重新克隆仓库**：从远程仓库重新克隆仓库。
- **恢复未推送的更改**：使用`reflog`和`cherry-pick`命令从旧仓库中恢复未推送的更改。
- **记录故障原因**：详细记录故障发生的原因，并为自动化流程添加相应的防护措施。

## 自动化钩子（Automation Hooks）
在开发用于管理工作树的工具（如`iMi`、脚本或自动化脚本）时，必须确保：
- 在执行任何操作之前创建快照并验证仓库状态。
- 执行操作后必须进行验证。
- 如果发现`HEAD`或引用信息不一致，必须立即停止操作并请求用户确认。
- 对于可能破坏仓库数据的操作，必须要求用户明确确认。

## 参考资源（Resources）
- **问题症状映射表**：`references/symptom-map.md`
- **验证清单**：`references/recovery-checklist.md`
- **诊断快照脚本**：`scripts/snapshot-git_state.sh`
- **修复计划生成脚本**：`scripts/guided_repair_plan.sh`
- **一次性回归测试工具**：`scripts/regression_harness.sh`