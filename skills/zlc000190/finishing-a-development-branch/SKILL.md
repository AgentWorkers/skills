---
name: finishing-a-development-branch
description: **使用场景：**  
当实现工作已完成、所有测试均已通过，且需要决定如何整合这些成果时，本指南通过提供结构化的选项（如合并请求、提交 Pull Request 或进行代码清理）来指导开发工作的完成过程。
---

# 完成开发分支（Finishing a Development Branch）

## 概述  
本技能通过提供清晰的选项并指导用户选择相应的工作流程，帮助完成开发工作。  

**核心原则：**  
- 验证测试结果 → 提供选项 → 执行用户选择 → 清理工作目录（worktree）。  

**开始时声明：**  
“我将使用‘完成开发分支’技能来完成这项工作。”  

## 流程  

### 第一步：验证测试结果  
**在提供选项之前，先确保所有测试都已通过：**  
```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```  

**如果测试失败：**  
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```  
停止操作，不要进入第二步。  
**如果测试通过：**  
继续执行第二步。  

### 第二步：确定基础分支（Base Branch）  
```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```  
或者询问：  
“这个分支是从主分支（main branch）分离出来的吗？”  

### 第三步：提供选项  
提供以下四个选项：  
```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```  
（请注意：不要添加任何解释，保持选项简洁。）  

### 第四步：执行用户选择  
#### 选项 1：本地合并（Merge Locally）  
```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d <feature-branch>
```  
随后：清理工作目录（步骤 5）。  

#### 选项 2：推送代码并创建 Pull Request（Push and Create PR）  
```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```  
随后：清理工作目录（步骤 5）。  

#### 选项 3：保持现状（Keep As-Is）  
**记录：**  
“保持分支 <name> 的状态不变，工作目录保存在 <path>。”  
（此时无需清理工作目录。）  

#### 选项 4：丢弃分支（Discard）  
**先获取确认：**  
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```  
等待用户明确确认。  
如果确认：  
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```  
随后：清理工作目录（步骤 5）。  

### 第五步：清理工作目录  
**对于选项 1、2 和 4：**  
检查工作目录中是否存在未提交的更改：  
```bash
git worktree list | grep $(git branch --show-current)
```  
如果存在未提交的更改：  
```bash
git worktree remove <worktree-path>
```  
（执行相应的清理操作。）  
**对于选项 3：**  
保持工作目录的原状不变。  

## 快速参考  
| 选项          | 合并（Merge） | 推送代码（Push） | 保持工作目录（Keep Worktree） | 清理分支（Clean up Branch） |
|---------------|---------|----------------|-------------------------|-------------------------|  
| 1. 本地合并      | ✓        | -            | -                          | ✓                          |  
| 2. 创建 Pull Request | -        | ✓            | ✓                          | -                          |  
| 3. 保持现状      | -        | -            | ✓                          | -                          |  
| 4. 丢弃分支      | -        | -            | ✓                          | （强制执行）                      |  

## 常见错误  
- **错误 1：** 跳过测试验证  
  - **问题：** 合并了有问题的代码，导致 Pull Request 失败。  
  **解决方法：** 在提供任何选项之前，务必先验证测试结果。  

- **错误 2：** 提出开放式问题（如“我接下来该做什么？”）  
  - **问题：** 导致选择不明确。  
  **解决方法：** 仅提供四个结构化的选项。  

- **错误 3：** 自动清理工作目录  
  - **问题：** 在某些情况下（如选择选项 2 或 3）错误地删除了工作目录。  
  **解决方法：** 仅在执行选项 1 或 4 时才清理工作目录。  

- **错误 4：** 丢弃分支时未获取确认  
  - **问题：** 可能会意外删除重要数据。  
  **解决方法：** 强制要求用户明确输入“discard”以确认操作。  

## 需注意的事项  
- **绝对禁止：**  
  - 在测试失败的情况下继续执行操作。  
  - 在未验证测试结果的情况下合并代码。  
  - 未经确认就删除工作目录。  
  - 未经请求就强制推送代码。  

- **务必做到：**  
  - 在提供选项之前验证测试结果。  
  - 仅提供四个明确的选项。  
  - 对于选项 4，必须获取用户的确认。  
  - 仅对选项 1 和 4 执行工作目录的清理操作。  

## 集成说明  
- **调用场景：**  
  - **子代理驱动的开发流程（subagent-driven-development）**：在所有任务完成后调用。  
  - **执行计划（executing-plans）**：在所有批次任务完成后调用。  

- **关联技能：**  
  - **使用 Git 工作目录（using-git-worktrees）**：用于清理由该技能创建的工作目录。