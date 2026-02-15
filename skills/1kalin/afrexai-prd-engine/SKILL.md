# PRD引擎 — 已发布的产品需求文档

我们提供了一套完整的产品需求文档编写方法论：从需求构思到详细规范，再到最终功能的实现。这不仅仅是一个JSON模板，而是一个开发者能够实际遵循、利益相关者能够实际批准的完整系统。

## 适用场景

- 将模糊的需求转化为可构建的规范
- 为新功能、新产品或重大重构编写产品需求文档
- 在冲刺计划前审查/改进现有的产品需求文档
- 将大型项目拆分为合适大小的用户故事
- 与产品规范一起创建技术设计文档
- 为AI编码工具（如Claude Code、Cursor、Copilot）准备开发所需的规范

---

## 第一阶段：问题发现与验证

在编写任何需求文档之前，请先回答以下问题。如果跳过这一步，你可能需要重新编写三次需求文档。

### 问题验证 checklist

```yaml
discovery_brief:
  problem:
    statement: "" # One sentence. If you need two, you don't understand it yet.
    who_has_it: "" # Specific persona, not "users"
    frequency: "" # Daily? Weekly? Once? (daily problems > occasional ones)
    current_workaround: "" # What do they do today? (no workaround = maybe not a real problem)
    evidence:
      - type: "" # support_ticket | user_interview | analytics | churned_user | sales_objection
        detail: ""
        date: ""

  impact:
    users_affected: "" # Number or percentage
    revenue_impact: "" # $ at risk or $ opportunity
    strategic_alignment: "" # Which company goal does this serve?

  constraints:
    deadline: "" # Hard date or flexible?
    budget: "" # Engineering weeks available
    dependencies: "" # What must exist first?
    regulatory: "" # Any compliance requirements?

  success_metrics:
    primary: "" # ONE metric that defines success
    secondary: [] # 2-3 supporting metrics
    measurement_method: "" # How will you actually measure this?
    target: "" # Specific number, not "improve"
    timeframe: "" # When do you expect to see results?
```

### 问题陈述模板

**[目标用户群体] 需要 [具体功能]，因为 [原因]，但目前存在 [阻碍因素]，这导致了 [可衡量的负面影响]。**

**示例：**
- ❌ “用户需要更好的入门体验”（过于模糊，无法量化）
- ✅ “每月新增的500名免费试用用户需要在10分钟内体验到‘顿悟时刻’，因为73%的用户在48小时内会流失；而由于12步的设置流程，平均价值实现时间长达34分钟，每月因此损失约1.8万美元的转化机会。”

### 终止条件

在继续之前，请检查以下情况。如果符合任何一条，请立即停止并重新评估：
| 信号 | 行动 |
|--------|--------|
| 没有问题的证据（只是某人的观点） | 要求提供证据。观点不能作为需求。 |
| 解决方案已经确定（“直接开发X”） | 回到问题本身。没有问题的解决方案往往没人会使用。 |
| 成功指标无法衡量 | 需要明确如何衡量，否则就不要开发。 |
| 只影响不到1%的用户且没有收入影响 | 降低优先级。小问题带来的回报也很小。 |
| 在发现过程中需求范围不断扩展 | 固定需求范围。如果所有内容都包含在范围内，那么实际上什么也做不成。 |

---

## 第二阶段：产品需求文档（PRD）的编写

### PRD模板

```markdown
# PRD: [Feature Name]

**Author:** [Name]
**Status:** Draft | In Review | Approved | In Progress | Shipped
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Approvers:** [Names + roles]

## 1. Problem & Opportunity

[Problem statement from discovery brief — one paragraph max]

### Evidence
- [Evidence point 1 — with data]
- [Evidence point 2 — with data]

### Impact
- Users affected: [number]
- Revenue impact: [$ amount or % change]
- Strategic goal: [which one]

## 2. Solution Overview

[2-3 paragraphs max. What are we building and why this approach?]

### What This Is
- [Bullet list of what's in scope]

### What This Is NOT
- [Explicit exclusions — this prevents scope creep]

### Key Decisions Made
| Decision | Options Considered | Chosen | Rationale |
|----------|-------------------|--------|-----------|
| [Decision 1] | A, B, C | B | [Why] |

## 3. User Stories

[See Phase 3 below for story writing methodology]

## 4. Design & UX

### User Flow
1. User [action] →
2. System [response] →
3. User sees [outcome]

### Wireframes/Mockups
[Link to Figma/screenshots or describe key screens]

### Edge Cases
| Scenario | Expected Behavior |
|----------|------------------|
| [Edge case 1] | [What happens] |
| [Edge case 2] | [What happens] |
| Empty state | [What user sees with no data] |
| Error state | [What user sees on failure] |
| Slow connection | [Loading behavior] |

## 5. Technical Considerations

### Architecture Notes
- [Key technical decisions]
- [New services/APIs needed]
- [Database changes]

### Dependencies
- [External service X]
- [Team Y's API]
- [Library Z]

### Performance Requirements
- Page load: <[X]ms
- API response: <[X]ms
- Concurrent users: [X]

### Security & Privacy
- [Data handling requirements]
- [Auth/permissions needed]
- [PII considerations]

## 6. Release Plan

### Rollout Strategy
- [ ] Feature flag: [flag name]
- [ ] Beta group: [who]
- [ ] % rollout: [10% → 50% → 100%]
- [ ] Rollback plan: [how]

### Launch Checklist
- [ ] QA sign-off
- [ ] Analytics events implemented
- [ ] Monitoring/alerts configured
- [ ] Documentation updated
- [ ] Support team briefed
- [ ] Stakeholders notified

## 7. Success Criteria

| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| [Primary metric] | [X] | [Y] | [Z weeks] |
| [Secondary metric] | [X] | [Y] | [Z weeks] |

### Post-Launch Review
- **1-week check:** [What to look at]
- **1-month review:** [What to measure]
- **Kill/iterate decision:** [Criteria for each]
```

### PRD质量评分标准（分享前需达到）

| 评分维度 | 0-2（较差） | 3-4（合格） | 5（优秀） | 权重 |
|-----------|-----------|----------------|------------|--------|
| **问题清晰度** | 模糊，缺乏数据 | 描述清晰但证据不足 | 问题表述明确且有多个证据支持 | x4 |
| **范围界定** | 所有内容都在范围内 | 有明确的边界 | 明确说明哪些包含在内、哪些不包含 | x3 |
| **故事质量** | 任务描述模糊 | 有具体标准的用户故事 | 符合INVEST原则的用户故事，并有可验证的验收标准 | x4 |
| **边缘情况处理** | 未列出任何边缘情况 | 包含正常流程和1-2种异常情况 | 全面考虑了空值、错误、性能问题、权限问题及并发情况 | x3 |
| **成功指标** | “改进X” | 明确的指标 + 目标值 | 明确的指标 + 基线值 + 目标值 + 时间框架 + 测量方法 | x3 |
| **技术可行性** | 没有技术相关内容 | 仅有架构说明 | 包含依赖关系、性能要求、安全性和迁移计划 | x2 |
| **发布计划** | 未制定发布计划 | “立即发布” | 设置发布标志、发布比例、回滚策略和发布检查清单 | x1 |

**评分方式：** 各维度得分乘以权重之和。总分最高为100分。
- **80-100分：** 可以直接发布，等待审批。
- **60-79分：** 整体不错，但某些部分缺失，需在审查前补充。
- **40-59分：** 需要改进，主要部分不完整。
- **低于40分：** 需重新开始或回到问题发现阶段。

---

## 第三阶段：用户故事方法论

### 用户故事格式

```yaml
story:
  id: "US-001"
  title: "" # Action-oriented: "Add priority field to tasks table"
  persona: "" # Who benefits
  narrative: "As a [persona], I want [capability] so that [benefit]"
  acceptance_criteria:
    - criterion: "" # Verifiable statement
      type: "functional" # functional | performance | security | ux
  priority: 1 # Execution order (dependencies first)
  size: "" # XS | S | M | L | XL
  status: "todo" # todo | in_progress | review | done
  notes: "" # Runtime observations
  depends_on: [] # Story IDs this depends on
  blocked_by: [] # External blockers
```

### INVEST原则（每个用户故事都必须满足）

| 原则 | 标准 | 测试方法 |
|--------|-----------|------|
| **I**（独立性） | 可以在其他未完成的故事独立构建 | 不存在循环依赖关系 |
| **N**（可协商性） | 细节可以调整（“做什么”是固定的，“怎么做”是灵活的） | 存在多种实现方式 |
| **V**（价值性） | 单独使用时能为用户或业务带来价值 | 即使只实现这个功能，用户/利益相关者也会关心吗？ |
| **E**（可估算性） | 团队能够估算工作量 | 没有重大未知因素（如果有未知因素，先进行探索性开发） |
| **S**（规模适中） | 可以在一个冲刺周期内完成（或AI工具可以处理） | 最多需要1-3天的工作量 |
| **T**（可测试性） | 有可验证的验收标准 | 每个标准都有对应的测试用例 |

### 验收标准

**好的验收标准应该是：**
- 二元的（通过/失败，不主观）
- 具体的（用数字表达，而非形容词）
- 独立的（可以单独测试）

| ❌ 不符合 | ✅ 符合 |
|--------|---------|
| “运行正确” | “API在95%的请求率下，100个并发用户的情况下响应时间小于200毫秒” |
| “用户友好” | “表单在字段模糊时能在100毫秒内显示验证错误” |
| “安全” | “没有`admin`权限的用户请求会被返回403错误代码” |
| “能处理错误” | “在网络超时时显示重试按钮，并提供缓存数据（如果可用）”

**必须包含的通用标准：**
- 使用TypeScript项目时，代码通过类型检查（`tsc --noEmit --strict`）
- 所有现有测试依然通过
- 新功能有测试覆盖

### 用户故事规模估算指南

| 规模 | 范围 | 时间 | 示例 |
|------|-------|------|---------|
| **XS** | 配置更改、复制更新、环境变量设置 | <2小时 | “更新错误信息文本” |
| **S** | 单个组件/功能，无新的依赖关系 | 2-4小时 | “在表单中添加日期选择器” |
| **M** | 包含数据库、API和用户界面的功能模块 | 1-2天 | “为任务添加优先级筛选器” |
| **L** | 多组件功能，涉及新逻辑 | 2-3天 | “添加实时通知功能” |
| **XL** | 规模过大，需要拆分 | — | — |

### 用户故事排序：依赖关系金字塔

用户故事的排序必须自下而上进行：

```
Level 1: Schema & Data (migrations, models, seed data)
    ↑
Level 2: Backend Logic (services, APIs, business rules)
    ↑
Level 3: Integration (API routes, auth, middleware)
    ↑
Level 4: UI Components (forms, tables, modals)
    ↑
Level 5: UX Polish (animations, empty states, loading)
    ↑
Level 6: Analytics & Monitoring (events, dashboards)
```

每个层级的用户故事仅依赖于其下方的层级。在API实现之前，切勿先开发用户界面。

### 分割策略

当一个用户故事规模过大时，可以使用以下策略进行拆分：

| 分割策略 | 适用场景 | 示例 |
|----------|------------|---------|
| **按功能模块** | 全栈功能 | “添加数据库模式” → “添加API” → “添加用户界面” |
| **按操作流程** | CRUD操作 | “创建任务” → “读取任务列表” → “更新任务” → “删除任务” |
| **按用户角色** | 多角色功能 | “管理员创建模板” → “用户填写模板” → “查看结果” |
| **按正常/异常流程** | 复杂业务流程 | “支付成功” → “支付失败” → “支付超时” |
| **按平台** | 跨平台功能 | “支持iOS” → “支持Android” → “支持Web” |
| **探索性开发** | 高不确定性 | “先进行探索性开发：评估认证库（2小时）” → “使用选定的库实现认证功能” |

---

## 第四阶段：为AI编码工具准备PRD

当产品需求文档将由AI编码工具（如Claude Code、Cursor、Copilot Workspace等）执行时，需要做以下调整：

### 适用于AI编码工具的用户故事格式

```yaml
agent_story:
  id: "US-001"
  title: "Add priority field to tasks table"
  context: |
    The tasks table is in src/db/schema.ts using Drizzle ORM.
    Priority values should be: high, medium, low (default: medium).
    See existing fields for naming conventions.
  acceptance_criteria:
    - "Add `priority` column to `tasks` table in src/db/schema.ts"
    - "Type: enum('high', 'medium', 'low'), default 'medium', not null"
    - "Generate migration: `npx drizzle-kit generate`"
    - "Run migration: `npx drizzle-kit push`"
    - "Verify: `tsc --noEmit --strict` passes"
    - "Verify: existing tests pass (`npm test`)"
  files_to_touch:
    - src/db/schema.ts
    - drizzle/ (generated migration)
  commands_to_run:
    - "npx drizzle-kit generate"
    - "npx drizzle-kit push"
    - "tsc --noEmit --strict"
    - "npm test"
  done_when: "All verify commands pass with exit code 0"
```

### 适用于AI编码工具的规则

1. **明确文件路径**。AI工具无法猜测项目的结构。
2. **提供验证指令**。AI工具需要明确的完成标准。
3. **每个用户故事只涉及少量文件**。如果一个用户故事涉及超过50个文件，那么这个故事就太复杂了。
4. **列出需要处理的文件**。这有助于减少AI工具的探索时间，避免错误。
5. **顺序非常重要**。AI工具是按顺序执行的，错误的顺序会导致错误累积。
6. **提供具体的执行命令**。不要只是说“运行迁移”，而要给出具体的命令（例如 `npx drizzle-kit push`）。

### 项目上下文文件

为了方便AI工具执行，需要为PRD创建一个 `PROJECT_CONTEXT.md` 文件：

```markdown
# Project Context

## Stack
- Framework: [Next.js 14 / Express / etc.]
- Language: [TypeScript strict mode]
- Database: [PostgreSQL via Drizzle ORM]
- Testing: [Vitest + Testing Library]
- Styling: [Tailwind CSS]

## Key Directories
- src/db/ — Database schema and migrations
- src/api/ — API routes
- src/components/ — React components
- src/lib/ — Shared utilities
- tests/ — Test files (mirror src/ structure)

## Conventions
- File naming: kebab-case
- Component naming: PascalCase
- Max file length: 300 lines
- Max function length: 50 lines
- All exports typed, no `any`

## Commands
- `npm run dev` — Start dev server
- `npm test` — Run tests
- `npm run build` — Production build
- `tsc --noEmit --strict` — Type check
- `npx drizzle-kit generate` — Generate migration
- `npx drizzle-kit push` — Apply migration

## Current State
- [What exists today relevant to the PRD]
- [Any tech debt or gotchas the agent should know]
```

---

## 第五阶段：审查与审批

### 审查流程（在分享PRD之前）

**完整性检查：**
- 问题陈述有明确的证据支持（不仅仅是主观意见）
- “不包含的内容”部分已经列出且具体明确
- 每个用户故事都有至少3个验收标准
- 边缘情况已经涵盖（包括空值状态、错误状态、权限问题和并发访问情况）
- 成功指标包括基线值、目标值和时间框架
- 技术部分涵盖了性能、安全性和依赖关系等问题

**质量检查：**
- 没有规模超过“L”级别的用户故事（超过L级别的故事需要拆分）
- 所有验收标准都是二元的（通过/失败）
- 不存在故事之间的循环依赖关系
- 依赖关系金字塔的排序正确
- 发布计划中包含回滚策略

**可读性检查：**
- 执行摘要少于3句话
- 非技术人员也能理解问题描述部分
- 工程师可以直接根据用户故事部分开始开发
- 所有专业术语都有明确的定义

### 审批流程

```
Author writes PRD
    ↓
Self-review (score with rubric — must be ≥60)
    ↓
Peer review (another PM or tech lead)
    ↓
Engineering review (feasibility + sizing)
    ↓
Stakeholder approval (PM lead or product director)
    ↓
Status → Approved
    ↓
Sprint planning (stories → backlog)
```

### 常见的审查反馈及解决方法

| 反馈 | 解决方法 |
|----------|-----|
| “这个功能解决了什么问题？” | 问题陈述不够明确，请提供更多证据。 |
| “这个功能太复杂了” | 将功能拆分为多个小部分，先发布最有价值的部分（MVP）。 |
| “我们怎么知道这个功能是否有效？” | 成功指标不明确，请提供具体的指标和时间框架。 |
| “边缘情况怎么处理？” | 边缘情况未列出，请补充完整。 |
| “这个功能什么时候发布？” | 请提供包含里程碑的时间表，而不仅仅是截止日期。 |
| “谁批准了这个功能？” | 请添加审批人信息并获取明确的签字确认。 |

---

## 第六阶段：跟踪与迭代

### PRD的状态管理

### 进度跟踪

可以在PRD文档本身或关联的跟踪工具中记录用户故事的完成情况：

```yaml
progress:
  total_stories: 12
  done: 7
  in_progress: 2
  blocked: 1
  todo: 2
  completion: "58%"
  
  blocked_items:
    - story: "US-008"
      blocker: "Waiting for payments API access from finance team"
      since: "2025-01-15"
      escalation: "Pinged finance lead, follow up Friday"

  velocity:
    stories_per_week: 3.5
    estimated_completion: "2025-02-01"
```

### 上线后的审查模板

```yaml
post_launch:
  shipped_date: ""
  review_date: "" # 2-4 weeks after ship

  metrics:
    primary:
      metric: ""
      baseline: ""
      target: ""
      actual: ""
      verdict: "" # hit | miss | exceeded

    secondary:
      - metric: ""
        actual: ""
        verdict: ""

  qualitative:
    user_feedback: []
    support_tickets: "" # count related to this feature
    unexpected_outcomes: []

  process_retro:
    what_went_well: []
    what_didnt: []
    estimation_accuracy: "" # actual vs estimated effort
    scope_changes: "" # what changed after approval

  decision: "" # iterate | maintain | deprecate | expand
  next_actions: []
```

---

## 常用命令

| 命令 | 功能 |
|---------|-------------|
| “为[功能]编写PRD” | 从需求发现到用户故事的全套文档 |
| “将这个功能拆分为用户故事” | 将功能描述转化为符合INVEST原则的用户故事 |
| “审查这个PRD” | 根据质量标准进行评分并提供具体反馈 |
| “使这个PRD适合AI工具使用” | 将PRD中的用户故事转换为适合AI工具的格式 |
| “这个PRD缺少什么？” | 根据模板分析缺失的部分 |
| “拆分这个用户故事” | 将一个大型用户故事拆分为多个符合INVEST原则的小故事 |
| “评估这个PRD的质量” | 根据质量标准进行评分 |
| “为[项目]生成项目上下文文件” | 为AI工具生成PROJECT_CONTEXT.md文件 |
| “为[功能]生成上线后的审查模板” | 生成包含指标的审查模板 |
| “跟踪进度” | 根据用户故事的状态更新完成情况 |