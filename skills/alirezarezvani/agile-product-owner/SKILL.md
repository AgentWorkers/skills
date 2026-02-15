---
name: agile-product-owner
description: 敏捷产品管理方法，用于任务列表（backlog）的管理和冲刺（sprint）的执行。内容包括用户故事的编写、验收标准的制定、冲刺计划的制定以及工作进度的跟踪。该方法适用于编写用户故事、创建验收标准、规划冲刺任务、估算任务的工作量（故事点数）、分解大型项目（epics），以及确定任务列表的优先级。
triggers:
  - write user story
  - create acceptance criteria
  - plan sprint
  - estimate story points
  - break down epic
  - prioritize backlog
  - sprint planning
  - INVEST criteria
  - Given When Then
  - user story template
  - sprint capacity
  - velocity tracking
---

# 敏捷产品负责人

这是一套专为产品负责人设计的工具包，用于管理待办事项列表（backlog）和执行冲刺（sprint）任务，包括用户故事（user story）的创建、验收标准的制定、冲刺计划的制定以及工作进度的跟踪。

---

## 目录

- [用户故事创建流程](#user-story-generation-workflow)
- [验收标准模板](#acceptance-criteria-patterns)
- [史诗级任务分解流程](#epic-breakdown-workflow)
- [冲刺计划流程](#sprint-planning-workflow)
- [待办事项列表优先级排序](#backlog-prioritization)
- [参考文档](#reference-documentation)
- [工具](#tools)

---

## 用户故事创建流程

根据INVEST原则（Independent, Negotiable, Valuable, Estimable, Sustainable）创建符合要求的标准用户故事：

1. 确定受益的用户群体（谁会从该功能中受益）
2. 明确所需的功能或能力
3. 详细描述所提供的价值或好处
4. 使用“Given-When-Then”格式编写验收标准
5. 使用斐波那契比例法估算用户故事的工作量（故事点数）
6. 核对是否符合INVEST原则
7. 按优先级将故事添加到待办事项列表中
8. **验证：**故事满足所有INVEST原则；验收标准可被测试

### 用户故事模板

```
As a [persona],
I want to [action/capability],
So that [benefit/value].
```

**示例：**
```
As a marketing manager,
I want to export campaign reports to PDF,
So that I can share results with stakeholders who don't have system access.
```

### 故事类型

| 类型 | 模板 | 示例 |
|------|----------|---------|
| 新功能 | 作为[用户群体]，我希望[执行某动作]，以便[获得某种好处] | 作为用户，我希望能够过滤搜索结果，以便更快地找到所需内容 |
| 改进 | 作为[用户群体]，我需要[某种能力]来实现[目标] | 作为用户，我希望页面加载速度更快，以便更高效地完成任务 |
| 修复漏洞 | 作为[用户群体]，我希望在[特定条件下]看到[预期行为] | 作为用户，我希望在刷新页面时购物车中的信息能够保留 |
| 基础支持 | 作为开发人员，我需要完成[技术任务]来支持[所需功能] | 作为开发人员，我需要实现缓存功能以实现即时搜索 |

### 用户群体参考

| 用户群体 | 典型需求 | 使用场景 |
|---------|--------------|---------|
| 最终用户 | 高效率、简单性、可靠性 | 日常使用功能 |
| 管理员 | 控制权限、系统可见性、安全性 | 系统管理 |
| 高级用户 | 自动化、个性化设置、快捷操作 | 高级工作流程 |
| 新用户 | 指导、学习支持、安全性 | 入职培训 |

---

## 验收标准模板

使用“Given-When-Then”格式编写可测试的验收标准。

### Given-When-Then 模板

```
Given [precondition/context],
When [action/trigger],
Then [expected outcome].
```

**示例：**
```
Given the user is logged in with valid credentials,
When they click the "Export" button,
Then a PDF download starts within 2 seconds.

Given the user has entered an invalid email format,
When they submit the registration form,
Then an inline error message displays "Please enter a valid email address."

Given the shopping cart contains items,
When the user refreshes the browser,
Then the cart contents remain unchanged.
```

### 验收标准检查清单

每个故事都应包含以下类型的验收标准：

| 类型 | 示例 |
|----------|---------|
| 正常流程 | 给定有效输入后，执行某操作，然后显示成功消息 |
| 验证 | 如果必填字段为空，则应拒绝输入 |
| 错误处理 | 当API失败时，必须显示用户友好的提示信息 |
| 性能 | 操作应在2秒内完成 |
| 可访问性 | 仅通过键盘即可完成操作 |

### 根据故事大小确定的最低验收标准数量

| 故事点数 | 最低验收标准数量 |
|--------------|------------------|
| 1-2点 | 3-4条 |
| 3-5点 | 4-6条 |
| 8点以上 | 需将故事拆分 |

完整的模板库请参见`references/user-story-templates.md`。

---

## 历史级任务分解流程

将大型项目（epic）分解为适合在冲刺中完成的子任务：

1. 明确历史级任务的范围和成功标准
2. 确定所有受影响的用户群体
3. 列出每个用户群体所需的所有功能
4. 将功能分组为合理的子任务
5. 确保每个子任务的工作量不超过8点
6. 确定子任务之间的依赖关系
7. 按顺序安排子任务的交付
8. **验证：**每个子任务都能独立实现价值；所有子任务共同覆盖历史级任务的整个范围

### 分解技巧

| 技巧 | 适用场景 | 示例 |
|-----------|-------------|---------|
| 按工作流程步骤分解 | 线性流程 | “结账” → “加入购物车” → “输入支付” → “确认订单” |
| 按用户群体分解 | 多种用户类型 | “管理员仪表盘” → “普通用户仪表盘” |
| 按数据类型分解 | 多种输入方式 | “导入” → “导入CSV” → “导入Excel” |
| 按操作类型分解 | 基本CRUD操作 | “管理用户” → “创建” → “编辑” → “删除” |
| 先完成核心流程 | 降低风险 | “新功能” → “基本操作” → “错误处理” → “边缘情况” |

### 历史级任务示例

**历史级任务：** 用户仪表盘

**分解结果：**
```
Epic: User Dashboard (34 points total)
├── US-001: View key metrics (5 pts) - End User
├── US-002: Customize layout (5 pts) - Power User
├── US-003: Export data to CSV (3 pts) - End User
├── US-004: Share with team (5 pts) - End User
├── US-005: Set up alerts (5 pts) - Power User
├── US-006: Filter by date range (3 pts) - End User
├── US-007: Admin overview (5 pts) - Admin
└── US-008: Enable caching (3 pts) - Enabler
```

---

## 冲刺计划流程

规划冲刺的工作量并选择要执行的子任务：

1. 计算团队的工作能力（冲刺速度 × 团队成员的可用时间）
2. 与利益相关者讨论冲刺目标
3. 从优先级较高的待办事项列表中选择子任务
4. 选择工作量不超过80-85%的子任务
5. 设定额外的挑战性目标（10-15%）
6. 识别子任务之间的依赖关系和潜在风险
7. 将复杂的子任务分解为更小的任务
8. **验证：**已选子任务的总工作量不超过团队能力；所有子任务都有明确的验收标准

### 工作量计算方法

```
Sprint Capacity = Average Velocity × Availability Factor

Example:
Average Velocity: 30 points
Team availability: 90% (one member partially out)
Adjusted Capacity: 27 points

Committed: 23 points (85% of 27)
Stretch: 4 points (15% of 27)
```

### 团队成员可用性因素

| 情况 | 可用性系数 |
|----------|--------|
| 完整的冲刺周期，无休假 | 1.0 |
| 团队成员中有50%缺席 | 0.9 |
| 冲刺期间有假期 | 0.8 |
| 多名成员缺席 | 0.7 |

### 冲刺任务分配模板

```
Sprint Capacity: 27 points
Sprint Goal: [Clear, measurable objective]

COMMITTED (23 points):
[H] US-001: User dashboard (5 pts)
[H] US-002: Export feature (3 pts)
[H] US-003: Search filter (5 pts)
[M] US-004: Settings page (5 pts)
[M] US-005: Help tooltips (3 pts)
[L] US-006: Theme options (2 pts)

STRETCH (4 points):
[L] US-007: Sort options (2 pts)
[L] US-008: Print view (2 pts)
```

完整的冲刺计划流程请参见`references/sprint-planning-guide.md`。

---

## 待办事项列表优先级排序

根据功能价值和实现难度对待办事项列表进行优先级排序。

### 优先级等级

| 优先级 | 定义 | 冲刺目标 |
|----------|------------|---------------|
| 关键 | 影响用户使用、涉及数据安全 | 需立即处理 |
| 高 | 核心功能、满足关键用户需求 | 本次冲刺必须完成 |
| 中等 | 改进措施、提升用户体验 | 下2-3次冲刺完成 |
| 低 | 非强制要求、小规模改进 | 可在后续冲刺中处理 |

### 优先级排序因素

| 因素 | 权重 | 评估要点 |
|--------|--------|-----------|
| 商业价值 | 40% | 对收入有影响吗？用户需求如何？是否符合战略目标？ |
| 用户影响 | 30% | 有多少用户需要使用？使用频率如何？ |
| 风险/依赖性 | 15% | 存在技术风险吗？有外部依赖关系吗？ |
| 实现难度 | 15% | 任务规模如何？复杂度如何？实现过程是否不确定？ |

### 在添加到冲刺计划前需要验证的INVEST原则

在将子任务添加到冲刺计划之前，需要验证每个子任务是否符合以下标准：

| 标准 | 需要验证的内容 | 符合标准的情况 |
|-----------|----------|------------|
| **独立性** | 该任务能否在其他未分配的子任务完成之前独立开发？ | 无阻碍其他任务的依赖关系 |
| **灵活性** | 实现方案是否灵活？ | 是否有多种实现方式？ |
| **价值** | 该任务能否为用户或业务带来实际价值？ | 是否有明确的好处描述（“以便...”） |
| **可估算性** | 团队能否准确估算完成时间？ | 目标是否足够明确？ |
| **规模** | 该任务能否在一个冲刺周期内完成？ | 工作量是否不超过8点？ |
| **可测试性** | 我们能否验证任务是否已经完成？ | 验收标准是否明确？ |

---

## 参考文档

### 用户故事模板

`references/user-story-templates.md`包含：

- 各类型用户故事的标准模板（新功能、改进、修复漏洞、基础支持）
- 验收标准模板（“Given-When-Then”格式）
- INVEST原则验证 checklist
- 用户故事工作量估算指南（斐波那契比例法）
- 常见的用户故事编写误区及解决方法
- 子任务分解技巧

### 冲刺计划指南

`references/sprint-planning-guide.md`包含：

- 冲刺计划会议议程
- 工作量计算公式
- 待办事项列表优先级排序框架（WSJF）
- 冲刺会议流程指南（站立会议、回顾会议、总结会议）
- 工作进度跟踪方法
- “任务完成”的定义标准
- 冲刺指标和目标

---

## 工具

### 用户故事生成工具

```bash
# Generate stories from sample epic
python scripts/user_story_generator.py

# Plan sprint with capacity
python scripts/user_story_generator.py sprint 30
```

该工具可以生成：
- 符合INVEST原则的用户故事
- 使用“Given-When-Then”格式的验收标准
- 用户故事工作量估算（斐波那契比例法）
- 任务优先级分配
- 显示已分配任务和额外挑战性任务的待办事项列表

### 示例输出

```
USER STORY: USR-001
========================================
Title: View Key Metrics
Type: story
Priority: HIGH
Points: 5

Story:
As a End User, I want to view key metrics and KPIs
so that I can save time and work more efficiently

Acceptance Criteria:
  1. Given user has access, When they view key metrics, Then the result is displayed
  2. Should validate input before processing
  3. Must show clear error message when action fails
  4. Should complete within 2 seconds
  5. Must be accessible via keyboard navigation

INVEST Checklist:
  ✓ Independent
  ✓ Negotiable
  ✓ Valuable
  ✓ Estimable
  ✓ Small
  ✓ Testable
```

---

## 冲刺指标

用于跟踪冲刺的进展和团队表现。

### 关键指标

| 指标 | 计算公式 | 目标值 |
|--------|---------|--------|
| 工作效率 | 完成的任务点数 / 总任务点数 | 稳定在±10%范围内 |
| 任务完成率 | 完成的任务点数 / 计划中的任务点数 | >85% |
| 任务范围变化 | 冲刺期间新增或删除的任务点数 | <10% |
| 未完成的任务量 | 未完成的任务点数 | <15% |

### 工作进度跟踪方法

```
Sprint 1: 25 points
Sprint 2: 28 points
Sprint 3: 30 points
Sprint 4: 32 points
Sprint 5: 29 points
------------------------
Average Velocity: 28.8 points
Trend: Stable

Planning: Commit to 24-26 points
```

### “任务完成”的定义

一个任务被视为完成，当满足以下条件：

- 代码编写完成并经过同事审核
- 编写了单元测试并通过测试
- 验收标准得到验证
- 文档更新完毕
- 代码已部署到测试环境
- 产品负责人批准
- 不存在严重的漏洞