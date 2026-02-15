---
name: github-issue-tracker
description: 基于任务的GitHub问题跟踪系统，通过评论、检查清单和标签实现详细的进度可视化。适用于在GitHub上跟踪任务进度、管理团队对特定任务的协作，或处理阻碍项目进展的问题。该系统支持针对每个任务进行更新和讨论。
---

# GitHub 问题跟踪器 - 任务级进度跟踪

**用途**：在 GitHub 问题中提供细粒度的任务级可见性，以便进行详细的进度跟踪和团队协作。

**使用场景**：
- 详细进度跟踪（每个任务的更新）
- 团队对特定任务的协作
- 通过 GitHub 分配任务
- 阻塞问题跟踪
- 任务级的评论和讨论

**集成**：与 `github-sync` 插件以及 `/sw:github:*` 命令兼容

---

## 任务跟踪的工作原理

### 1. GitHub 问题中的任务清单

在创建新问题时，会自动添加任务清单：

```markdown
## Tasks

### Week 1: Foundation (12 tasks)

- [ ] T-001: Create plugin type definitions (6h) @developer1
- [ ] T-002: Create plugin manifest schema (4h) @developer1
- [ ] T-003: Implement PluginLoader (6h) @developer2
- [ ] T-004: Implement PluginManager (8h) @developer2
...

### Week 2: GitHub Plugin (10 tasks)

- [ ] T-013: Create GitHub plugin structure (2h)
- [ ] T-014: Implement github-sync skill (8h)
...
```

**特性**：
- 可点击的复选框（GitHub 内置）
- 时间估算（以括号形式显示）
- 通过 @提及分配任务
- 按阶段/周进行组织

### 2. 每个任务的评论

任务完成后，发布详细的评论：

```markdown
### ✅ Task Completed: T-007

**Title**: Implement Claude plugin installer
**Estimated**: 8h
**Actual**: 7h
**Assignee**: @developer2

**What Changed**:
- Added `compilePlugin()` method to ClaudeAdapter
- Implemented plugin file copying to `.claude/`
- Added unload and status methods
- Updated adapter interface

**Files Modified**:
- `src/adapters/claude/adapter.ts` (+150 lines)
- `src/adapters/adapter-interface.ts` (+35 lines)

**Tests**:
- ✅ Unit tests passing (12 new tests)
- ✅ Integration test: plugin install/uninstall

**Next Task**: T-008 - Implement Cursor plugin compiler

---

**Progress**: 7/48 tasks (15%) | Week 1: 7/12 complete

🤖 Posted by SpecWeave at 2025-10-30 14:30:00
```

**好处**：
- 每个任务的详细变更记录
- 时间跟踪（估算时间与实际时间对比）
- 文件变更摘要
- 测试状态
- 为代码审阅者提供上下文信息

### 3. 任务分配

通过 GitHub 将任务分配给团队成员：

**方法 1：使用 @提及分配任务**
```markdown
- [ ] T-015: Create test suite (8h) @qa-engineer
```

**方法 2：在问题中添加评论**
```
@developer1 Can you take T-003 and T-004 this week?
```

**方法 3：使用 GitHub 项目**
- 将任务拖放到不同的列中（待办、进行中、已完成）
- 任务状态会自动同步

### 4. 阻塞问题

跟踪依赖关系和阻塞因素：

```markdown
### 🚨 Blocked: T-020

**Task**: Implement Kubernetes plugin
**Blocked By**: #127 (Infrastructure setup incomplete)
**Blocking**: T-021, T-022
**Reason**: Need staging cluster before testing K8s plugin

**Resolution**: Wait for #127 to close, then proceed with T-020

---

**ETA**: Blocked since 2025-10-28, expected resolution by 2025-11-01
```

---

## 配置

在 `.specweave/config.yaml` 文件中启用任务级跟踪：

```yaml
plugins:
  settings:
    specweave-github:
      # Task-level tracking
      task_tracking:
        enabled: true

        # Post comment after each task
        post_task_comments: true

        # Update checklist after each task
        update_checklist: true

        # Include file changes in comments
        include_file_changes: true

        # Include time tracking
        include_time_tracking: true

        # Auto-assign tasks based on git author
        auto_assign: true

      # Blocking issue detection
      blocking_issues:
        enabled: true

        # Check for blocking keywords in task descriptions
        keywords: ["blocked by", "depends on", "requires"]
```

---

## 命令

### 检查任务状态

```bash
/sw:github:status 0004
```

输出：
```
GitHub Issue: #130
Status: Open (In Progress)

Tasks: 7/48 completed (15%)

Week 1: Foundation
✅ T-001: Create plugin types (Done)
✅ T-002: Create manifest schema (Done)
✅ T-003: Implement PluginLoader (Done)
✅ T-004: Implement PluginManager (Done)
✅ T-005: Implement PluginDetector (Done)
✅ T-006: Update adapter interface (Done)
✅ T-007: Implement Claude installer (Done)
⏳ T-008: Implement Cursor compiler (In Progress)
⏸️ T-009: Implement Copilot compiler (Pending)
```

### 同步任务清单

```bash
/sw:github:sync 0004 --tasks
```

将 GitHub 问题中的任务清单更新为当前任务的进度。

### 在任务上添加评论

```bash
/sw:github:comment 0004 T-008 "Cursor adapter completed, moving to testing phase"
```

在 GitHub 问题中为特定任务发布自定义评论。

---

## 任务的 GitHub 标签

根据任务状态自动应用标签：

| 标签 | 应用时机 | 用途 |
|-------|--------------|---------|
| `in-progress` | 任务开始时 | 任务正在积极处理中 |
| `testing` | 实现任务完成 | 准备进行质量测试 |
| `blocked` | 任务被标记为阻塞 | 需要关注 |
| `review-requested` | 创建了 Pull Request（PR） | 需要代码审阅 |
| `ready-for-merge` | 审阅通过 | 可以合并 |

---

## 团队协作模式

### 模式 1：通过 GitHub 进行每日站会

团队成员在问题中添加评论，更新每日进度：

```markdown
**@developer1** on T-008:
Yesterday: Implemented Cursor adapter skeleton
Today: Adding plugin compilation logic
Blockers: None

**@developer2** on T-014:
Yesterday: Created github-sync skill
Today: Testing sync workflow
Blockers: Waiting for #130 review
```

### 模式 2：代码审阅集成

将 PR 链接到相关任务：

```markdown
### T-007: Claude plugin installer

**PR**: #45
**Status**: Ready for review
**Reviewers**: @tech-lead, @architect

**Changes**:
- Implemented plugin support in Claude adapter
- Added comprehensive tests
- Updated documentation

**Review Checklist**:
- [ ] Code quality (clean, readable)
- [ ] Test coverage (80%+)
- [ ] Documentation updated
- [ ] No security issues
```

### 模式 3：任务交接

转移任务的所有权：

```markdown
@developer1 → @developer2 (T-015)

**Context**:
- Tests framework configured
- Need to write E2E tests for plugin system
- Reference: T-007 implementation

**Handoff Notes**:
- Use Playwright for E2E tests
- Cover happy path + error scenarios
- See `.specweave/increments/0004/tests.md` for test cases
```

---

## 时间跟踪

### 自动时间跟踪

跟踪在任务上花费的时间：

```yaml
# .specweave/increments/0004-plugin-architecture/.metadata.yaml
tasks:
  T-007:
    estimated_hours: 8
    actual_hours: 7
    started_at: 2025-10-30T10:00:00Z
    completed_at: 2025-10-30T17:00:00Z
    assignee: developer2
```

### 时间报告

生成时间报告：

```bash
/sw:github:time-report 0004
```

输出：
```
Time Report: Increment 0004

Estimated: 240 hours (6 weeks)
Actual: 56 hours (1.4 weeks)
Remaining: 184 hours (4.6 weeks)

By Developer:
- developer1: 24h (5 tasks)
- developer2: 32h (2 tasks)

By Phase:
- Week 1 Foundation: 56h / 96h (58%)
- Week 2 GitHub Plugin: 0h / 80h (0%)
- Week 3 Plugins: 0h / 120h (0%)
- Week 4 Docs: 0h / 88h (0%)

Pace: On track (4% ahead of schedule)
```

---

## 与 GitHub 项目的集成

### 自动化的看板

将任务与 GitHub 项目同步：

**看板列**：
1. **待办事项**：待处理的任务
2. **准备中**：可以开始的任务
3. **进行中**：当前正在处理的任务
4. **审阅中**：打开的 PR，需要审阅
5. **已完成**：已完成的任务

**自动移动规则**：
- 任务开始 → 移动到“进行中”
- 创建 PR → 移动到“审阅中”
- PR 合并 → 移动到“已完成”

### 里程碑跟踪

将任务与 GitHub 里程碑关联：

```yaml
# .specweave/config.yaml
plugins:
  settings:
    specweave-github:
      milestones:
        "v0.4.0":
          increments:
            - 0004-plugin-architecture
            - 0005-user-authentication
          due_date: 2025-11-30
```

GitHub 里程碑视图可以显示多个任务的进度。

---

## 高级功能

### 任务依赖关系

在 `tasks.md` 文件中定义任务依赖关系：

```markdown
### T-008: Implement Cursor compiler

**Dependencies**: T-006, T-007
**Blocks**: T-011, T-012

**Description**: ...
```

SpecWeave 会确保依赖关系的正确顺序，并在尝试处理被阻塞的任务时发出警告。

### 子任务

将复杂任务分解为子任务：

```markdown
### T-014: Implement github-sync skill (8h)

**Subtasks**:
- [ ] T-014.1: Create SKILL.md (1h)
- [ ] T-014.2: Implement export (increment → issue) (3h)
- [ ] T-014.3: Implement import (issue → increment) (2h)
- [ ] T-014.4: Add progress updates (1h)
- [ ] T-014.5: Write tests (1h)
```

子任务会以嵌套复选框的形式显示在 GitHub 问题中。

### 外部问题链接

引用外部阻塞问题：

```markdown
### T-020: Kubernetes plugin

**Blocked By**:
- #127 (this repo): Infrastructure setup
- https://github.com/kubernetes/kubernetes/issues/12345: K8s API bug

**Resolution Plan**:
1. Wait for #127 (ETA: 2025-11-01)
2. Work around K8s bug using alternative API
```

---

## 通知

### 任务分配通知

GitHub 会自动通知任务分配者：

```
@developer1 you were assigned T-015 in #130
```

### 阻塞通知

当阻塞问题得到解决时，通知被阻塞任务的分配者：

```
@developer2 Task T-020 is unblocked (#127 was closed)
```

### 截止日期提醒

当任务进度落后时发出警告：

```
⚠️ T-008 is 2 days overdue (estimated: 2 days, actual: 4 days)
```

---

## 故障排除

**清单未更新？**
- 确认配置文件中的 `update_checklist: true` 是否设置正确
- 检查 GitHub API 权限（仓库写入权限）
- 手动同步：`/sw:github:sync 0004 --tasks`

**评论未发布？**
- 检查 `post_task_comments: true` 是否启用
- 确认是否已通过 GitHub CLI 进行身份验证：`gh auth status`
- 检查 API 使用率限制：`gh api rate_limit`

**时间跟踪不准确？**
- 检查 `.metadata.yaml` 文件中的任务时间戳
- 检查元数据是否被手动修改
- 重新同步：`/sw:github:sync 0004 --force`

---

## 最佳实践

1. **保持任务的可完成性**：每个任务应在一次工作会话（2-8 小时）内完成
2. **每日更新清单**：至少每天同步一次进度
3. **指定任务负责人**：为任务分配具体的开发人员以确保责任明确
4. **标记阻塞问题**：立即标记阻塞问题以便及时处理
5. **链接 PR**：在 PR 标题中始终引用任务 ID（例如：`T-007：添加插件支持`）
6. **添加上下文评论**：在交接任务时提供详细说明
7. **调整时间估算**：根据实际花费的时间调整估算时间

---

## 相关工具

- **github-sync**：用于高层次的问题与任务同步
- **github-manager agent**：用于管理 GitHub 操作的 AI 工具
- **命令**：所有 `/sw:github:*` 命令

---

**版本**：1.0.0
**插件**：specweave-github
**最后更新时间**：2025-10-30