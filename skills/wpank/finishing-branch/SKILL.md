---
name: finishing-branch
model: fast
description: 完成开发工作后，需要提供结构化的选项，以便进行合并（merge）、提交 Pull Request（PR）或清理（cleanup）操作。此步骤适用于以下情况：实现工作已经完成，所有测试均已通过，接下来需要决定如何将代码整合到项目中。触发条件包括：分支（branch）的创建完成、分支的合并完成、新的 Pull Request 的提交，或者某个功能（feature）的开发工作已经结束且实现完毕。
---

# 完成开发分支

通过提供明确的选项并执行所选的工作流程来完成开发工作。

## 该技能的作用

在实现完成后，指导您进行测试验证、选择集成方案，并执行相应的操作（合并、提交 Pull Request (PR)、保留分支或丢弃分支）。

## 适用场景

- 实现工作已完成
- 所有测试均已通过
- 准备将工作集成到主分支中

**关键词**: 完成分支、合并、提交 PR、功能开发完成

---

## 流程

### 第一步：验证测试

```bash
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：**立即停止。在测试通过之前不得继续。

```
Tests failing (N failures). Must fix before completing:
[Show failures]
```

**如果测试通过：**进入第二步。

### 第二步：确定基准分支

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

或确认：“该分支是从主分支分离出来的吗？”

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

### 第四步：执行选择

#### 选项 1：本地合并

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
<run tests again>
git branch -d <feature-branch>
```

然后：清理工作区（步骤 5）

#### 选项 2：推送代码并创建 PR

```bash
git push -u origin <feature-branch>

gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

然后：清理工作区（步骤 5）

#### 选项 3：保持原样

报告：“保留分支 `<name>`。工作区保存在 `<path>`。”

**请勿清理工作区。**

#### 选项 4：丢弃分支

**先进行确认：**

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

等待确认结果。如果确认：

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

然后：清理工作区（步骤 5）

### 第五步：清理工作区

**仅适用于选项 1、2 和 4：**

```bash
# Check if in worktree
git worktree list | grep $(git branch --show-current)

# If yes:
git worktree remove <worktree-path>
```

**对于选项 3：**保持工作区不变。

---

## 快速参考

| 选项 | 合并 | 推送代码 | 保留工作区 | 清理分支 |
|--------|-------|------|---------------|----------------|
| 1. 本地合并 | ✓ | - | - | ✓ |
| 2. 创建 PR | - | ✓ | ✓ | - |
| 3. 保持原样 | - | - | ✓ | - |
| 4. 丢弃分支 | - | - | - | ✓ （强制操作） |

---

## 注意事项：

- **绝对禁止**：
- 在测试未通过的情况下继续开发
- 在未验证测试结果的情况下进行合并
- 未经确认就删除工作区数据
- 未经明确请求就强制推送代码
- 跳过提供所有选项的步骤
- 对于选项 2 或 3 自动清理工作区
- 提出开放式问题“我接下来应该做什么？”（请使用结构化的选项）

---

## 集成流程

**调用者：**
- `subagent-development`（所有任务完成后）
- `executing-plans`（所有批次完成后）

**关联技能：**
- `git-worktrees` – 清理由该技能创建的工作区数据