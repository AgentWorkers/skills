---
name: pi-workflow
description: >
  **工作流程编排：用于 Pi 的任务管理、自我提升及代码质量标准**  
  适用于新项目的启动、多步骤任务（3 步以上）的管理、从错误中吸取经验教训、编写可验证的代码，以及在项目完成前设置质量检查点。该系统包含计划模板、进度跟踪功能、代码修复的自主权，以及一个用于记录经验教训的系统，以防止重复出现相同错误。
---
# Pi 工作流编排

该技能提供了 Pi 在任务管理、质量保证和持续自我提升方面的结构化方法。

## 核心工作流

### 1. 计划节点默认设置
对于任何非简单的任务（包含 3 个以上步骤或需要架构决策的任务），请进入计划模式：
- 提前编写详细的规范以减少歧义；
- 如果出现问题，立即停止并重新规划，不要继续推进；
- 计划模式不仅用于构建阶段，也用于验证步骤。

### 2. 子代理策略
- 充分利用子代理来保持主界面整洁；
- 将研究、探索和并行分析任务交给子代理处理；
- 对于复杂问题，通过子代理增加计算资源来加速解决；
- 每个子代理负责执行一个具体的任务，以确保专注性。

### 3. 自我提升循环
- 用户进行任何修改后：更新 `tasks/lessons.md` 文件中的元数据（优先级、状态、领域、问题模式）；
- 将命令失败记录到 `tasks/errors.md` 文件中，以便分析问题模式；
- 将功能请求记录到 `tasks/feature_requests.md` 文件中，为未来的工作做准备；
- 为自己制定规则，防止重复犯同样的错误；
- 不断迭代这些经验教训，直到错误率降低；
- 在每次会议开始时回顾相关项目的经验教训；
- 使用 `Recurrence-Count` 功能跟踪重复出现的模式（当出现 3 次或以上时提高优先级）。

### 4. 完成前的验证
- 在确认任务能够正常工作之前，切勿将其标记为已完成；
- 在必要时，对比主代码和修改后的代码行为；
- 问自己：“一个资深工程师会批准这个修改吗？”；
- 运行测试，检查日志，验证正确性。

### 5. 追求优雅的解决方案（平衡原则）
- 对于非简单的修改：暂停并思考“是否有更优雅的实现方式”；
- 如果某个解决方案显得不够完善，那么“利用现有的知识来实现更优雅的方案”；
- 对于简单且显而易见的修改，不必过度设计；
- 在展示自己的工作成果之前，先自我质疑其合理性。

### 6. 自主修复漏洞
- 收到漏洞报告后，直接修复它，不要寻求帮助；
- 指向日志、错误信息以及失败的测试结果，然后进行修复；
- 用户无需了解具体修复细节；
- 在没有指导的情况下，自行修复失败的持续集成（CI）测试。

## 任务管理
1. **先制定计划**：将计划内容写入 `tasks/todo.md` 文件中，并列出可检查的步骤；
2. **验证计划**：在开始实施之前进行确认；
3. **跟踪进度**：完成每个步骤后将其标记为已完成；
4. **解释修改内容**：在每个步骤中提供高层次的总结；
5. **记录结果**：在 `tasks/todo.md` 文件中添加结果说明；
6. **总结经验教训**：在修改完成后更新 `tasks/lessons.md` 文件。

## 文件组织结构
- `tasks/todo.md` — 当前项目的待办任务；
- `tasks/lessons.md` — 修正内容、见解和最佳实践（结构化存储）；
- `tasks/errors.md` — 命令失败、API 错误和异常情况（新记录）；
- `tasks/feature_requests.md` — 缺失的功能或功能请求（新记录）；
- `memory/YYYY-MM-DD.md` — 每日的会议日志；
- `MEMORY.md` — 用户整理的个人记忆记录。

详细参考 [WORKFLOW_ORCHESTRATION.md](references/workflow_orchestration.md)。

有关理念和框架的详细信息，请参阅 [LESSONS.md](references/lessons.md)。

有关结构化课程格式和文件分区的详细信息，请参阅 [PHASE1-PHASE2-ENHANCED-LESSONS.md](references/phase1-phase2-enhanced-lessons.md)。

有关如何将工作区的课程内容同步到技能系统中的详细信息，请参阅 [LESSONS_UPDATE_guide.md](references/lessons_update_guide.md)。

## 捕获经验教训
### 课程格式（第 1 阶段及后续版本）
每条经验教训都包含结构化的元数据，以便于过滤和识别重复出现的模式：

```markdown
## [LRN-YYYYMMDD-XXX] rule_name (category)

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | in_progress | resolved | promoted
**Area**: backend | infra | tests | docs | config
**Pattern-Key**: category.pattern_name (optional, for recurring detection)

### Summary
One-line description

### Details
Full context and examples

### Applied to
Projects or files where this was used

### Metadata
- Source: correction | insight | user_feedback
- Related Files: path/to/file
- Tags: tag1, tag2
- See Also: LRN-20250225-001 (if related to existing entry)
- Recurrence-Count: 1 (increment if you see it again)
- First-Seen: 2025-02-23
- Last-Seen: 2025-02-23
```

### 错误与功能需求（新记录）
将失败情况和功能需求分开记录，以便更好地管理：

**错误**（`tasks/errors.md`）：
- 命令失败、API 错误、异常情况；
- 包括可复现的环境信息和建议的修复方法。

**功能需求**（`tasks/feature_requests.md`）：
- 缺失的功能或希望添加的功能；
- 包括复杂度评估和实现建议。

### 同步到技能系统
定期将工作区的课程内容合并到已发布的技能系统中：

```bash
# From openclaw-workflow repo
python3 scripts/sync_lessons.py --workspace ~/.openclaw/workspace

# Dry run (preview changes)
python3 scripts/sync_lessons.py --workspace ~/.openclaw/workspace --dry-run
```

这将工作区的课程内容合并到 `references/lessons.md` 文件中，以便进行版本控制和共享。

## 钩子（可选）
启用自动提醒功能，以促进自我提升：

```bash
openclaw hooks enable pi-workflow
```

这会在会议开始时自动显示提醒信息，内容包括：
- 何时记录经验教训/错误/功能需求；
- 格式和元数据字段的规范；
- 重复模式的检测方法；
- 课程内容的升级路径。

详细信息请参阅 `hooks/openclaw/HOOK.md`。

---

## 核心原则
- **简单优先**：尽可能简化每个修改，尽量减少对代码的影响；
- **杜绝偷懒行为**：找出根本原因，避免使用临时解决方案，遵循资深开发者的标准；
- **最小化影响**：修改应仅针对必要的部分进行，避免引入新的错误。