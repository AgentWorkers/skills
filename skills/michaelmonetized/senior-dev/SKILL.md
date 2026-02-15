---
name: senior-dev
description: **生产开发工作流程**  
该流程包括 TODO 任务跟踪、Graphite 提交请求（PRs）、GitHub 问题报告、Vercel 部署检查以及 SMS 通知功能。适用于新任务的启动、错误修复、功能实现，以及任何需要进度跟踪和代码审核的开发工作。
---

# 高级开发人员

这是一个包含12个步骤的生产工作流程，确保在代码压缩过程中信息的连续性。

## 工作流程

### 1. 设置
```bash
cd ~/Projects/<project>
```
在 `TODO.md` 文件中创建或添加任务：
```markdown
## [Date] Task: <description>
- [ ] Subtask 1
- [ ] Subtask 2
```

### 2-3. 执行并跟踪
完成任务后，将待办事项标记为已完成。
更新 `CHANGELOG.md` 文件（如果不存在则创建）：
```markdown
## [Unreleased]
### Added/Changed/Fixed
- Description of change
```

### 4-5. 分支创建与验证
```bash
git add -A
git diff --staged  # Verify changes match request
```

### 6-7. 创建 Pull Request (PR)
分支命名格式：`(问题|功能|修复)/<简短描述>`
```bash
gt create "feature/add-dark-mode" -m "Add dark mode toggle"
gt submit
```

**如果此操作用于修复问题**，请先创建问题：
```bash
gh issue create --title "Bug: description" --body "Details..."
# Note the issue number
gt create "issue/42-fix-login-bug" -m "Fix login bug (#42)"
gt submit
```

### 8-9. 审查周期
等待审阅者的反馈，并根据反馈进行修改：
```bash
# Make fixes
git add -A
gt modify -m "Address review feedback"
gt submit
```

### 10-11. 合并后的部署检查
在 Pull Request 合并后：
```bash
git checkout main && git pull
```

**对于 Vercel 项目：**
```bash
# Watch deployment (polls until Ready/Error, auto-fetches logs on failure)
vl
```

如果构建失败 → 使用 `gh issue create` 命令创建问题，并附上错误日志，然后从步骤 6 重新开始。

### 12. 报告与清理
完成任务的报告格式：
> ✅ [项目] 任务已完成
> PR: <URL>
> 部署：成功/失败

## 快速参考

| 步骤 | 命令 | 用途 |
|------|---------|---------|
| 分支创建 | `git add -A` | 将所有更改添加到暂存区 |
| 验证 | `git diff --staged` | 提交前查看更改 |
| 创建分支 | `git create "类型/名称" -m "描述"` | 创建并提交分支 |
| 提交 Pull Request | `git submit` | 提交 Pull Request |
| 创建问题 | `gh issue create` | 跟踪 bug 或任务 |
| 部署 | `vl` | 监控构建过程，错误时自动获取日志 |

## 分支前缀

- `feature/` — 新功能分支
- `fix/` — 修复问题分支
- `issue/` — 与 GitHub 问题关联（包含问题编号）
- `chore/` — 维护、依赖项、配置相关的分支

## 需要维护的文件

- **TODO.md** — 活动任务跟踪（在代码压缩后仍能保留信息）
- **CHANGELOG.md** — 版本历史记录
- **PLAN.md** — 架构决策（可选）

## 所需工具

- `gt` — [Graphite CLI](https://graphite.dev)：用于管理多层级的 Pull Request
- `gh` — [GitHub CLI](https://cli.github.com)：用于处理 GitHub 问题
- `vl` — Vercel 部署监控工具（或 `vercel` CLI）