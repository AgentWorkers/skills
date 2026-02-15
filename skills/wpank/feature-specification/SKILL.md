---
name: feature-specification
model: reasoning
description: 将角色文档（persona documents）转换为详细的特性规范（feature specifications），并附上验收标准（acceptance criteria）。这种转换方法适用于将用户需求（user needs）转化为可实现的规范、编写用户故事（user stories）、定义验收标准，或为开发准备特性（features）。
---

# 功能规范（元技能）

该技能负责将人物文档（persona documents）与开发工作进行对接。它将人物文档中识别出的用户需求、痛点以及使用流程转化为结构化、可实施的特性规范，并明确指定验收标准。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install feature-specification
```


---

## 目的

人物文档定义了“谁”以及“为什么需要某个功能”。而特性规范则明确了“需要实现什么”以及“实现的质量标准”。该技能的作用在于：

- 从人物文档中提取出可操作的特性需求；
- 对需求进行结构化处理，让开发人员清楚知道需要开发什么；
- 明确验收标准，以便质量保证（QA）人员知道需要验证什么；
- 在编写任何代码之前，避免项目范围的模糊性。

---

## 适用场景

- 在人物文档（`docs/PERSONA.md` 或 `docs/personas/`）编写完成后；
- 在开始新功能或产品的开发之前；
- 当功能需求缺乏明确的验收标准时；
- 当利益相关者对“完成标准”存在分歧时；
- 当需要将用户反馈转化为开发任务时。

---

## 特性规范模板

请使用以下结构来编写每个特性规范。将规范文件保存在 `docs/specs/` 或 `docs/features/` 目录下。

```markdown
# Feature: [Feature Name]

## Metadata
- **Priority:** [Must / Should / Could / Won't]
- **Target Persona:** [Persona name from persona docs]
- **Status:** Draft | Review | Approved | In Progress | Complete
- **Estimated Effort:** [T-shirt size: XS / S / M / L / XL]

## Problem Statement
[Directly reference the persona pain point this feature addresses.
Quote or link to the relevant section of persona docs.]

## Solution Description
[High-level description of what the feature does and how it solves
the problem. 2-4 sentences. No implementation details.]

## User Stories

- As a [persona], I want [action], so that [benefit].
- As a [persona], I want [action], so that [benefit].

## Acceptance Criteria

### Scenario: [Happy path description]
- **Given** [precondition]
- **When** [action]
- **Then** [expected result]

### Scenario: [Alternative path description]
- **Given** [precondition]
- **When** [action]
- **Then** [expected result]

### Scenario: [Error case description]
- **Given** [precondition]
- **When** [invalid action]
- **Then** [error handling result]

## Edge Cases
- [ ] [Edge case 1 — description and expected behavior]
- [ ] [Edge case 2 — description and expected behavior]

## Non-Functional Requirements
- **Performance:** [Response time, throughput, load targets]
- **Accessibility:** [WCAG level, keyboard nav, screen reader support]
- **Security:** [Auth requirements, data sensitivity, input validation]
- **Browser/Device:** [Support matrix]

## Dependencies
- [Feature or system this depends on]
- [External API or service required]

## Out of Scope
- [Explicitly list what this feature does NOT include]
- [Prevents scope creep during development]

## Design References
- [Link to mockups, wireframes, or design system components]
- [Screenshots or diagrams if available]
```

---

## 编写有效的用户故事

用户故事将人物需求与开发任务联系起来。请遵循 INVEST 原则：

| 标准 | 含义 | 测试问题 |
|-----------|--------------------------------------|-------------------------------------------|
| 独立性（Independent） | 不依赖于其他功能 | 这个功能可以独立构建并发布吗？ |
| 可协商性（Negotiable） | 细节可以讨论 | 这只是一个讨论的起点，而不是不可更改的契约吗？ |
| 价值性（Valuable） | 能为人物带来实际价值 | 这个功能对人物来说重要吗？ |
| 可估算性（Estimable） | 团队能够估算工作量 | 功能范围是否足够明确，以便进行估算？ |
| 小规模性（Small） | 可以在一个开发周期内完成 | 这个功能可以在一个冲刺中实现吗？ |
| 可测试性（Testable） | 有明确的通过/失败标准 | 质量保证人员能为这个功能编写测试用例吗？ |

### 优秀用户故事与糟糕用户故事的对比

| 拙劣的用户故事 | 缺点 | 优秀的用户故事 |
|---------|------------------|-------------------------|
| “用户可以登录” | 没有明确的人物角色，也没有实际价值 | “作为回头客，我希望能够使用我的电子邮件登录，以便查看我的订单历史” |
| “加快加载速度” | 描述模糊，无法测试 | “作为使用 3G 网络的移动用户，我希望产品列表能在 2 秒内加载完毕，以免我离开页面” |
| “添加管理员面板” | 先提出解决方案，而非明确需求 | “作为店长，我希望能够在没有开发人员帮助的情况下更新产品价格，以便及时响应市场变化” |
| “处理错误” | 没有具体细节 | “作为结账用户，我希望在支付失败时能得到明确的反馈，以便知道是应该重试还是使用其他支付方式” |
| “实现缓存” | 只提到了实现细节，而非具体需求 | “作为经常访问该网站的用户，我希望之前浏览过的页面能够立即加载，以提升浏览体验” |

---

## 验收标准模板

### 模式 1：理想使用流程（Happy Path）

```gherkin
Given a logged-in customer with items in their cart
When they click "Checkout"
Then they are taken to the payment page with their cart summary visible
```

### 模式 2：边界条件（Boundary Conditions）

```gherkin
Given a cart with 100 items (maximum allowed)
When the user tries to add another item
Then they see "Cart limit reached — remove an item to add a new one"
And the item is NOT added to the cart
```

### 模式 3：错误处理（Error Cases）

```gherkin
Given a user submitting the registration form
When the email field contains "not-an-email"
Then the form shows inline validation: "Enter a valid email address"
And the form is NOT submitted
And focus moves to the email field
```

### 模式 4：状态转换（State Transitions）

```gherkin
Given an order with status "Processing"
When the warehouse marks it as shipped
Then the order status changes to "Shipped"
And the customer receives a shipping confirmation email within 5 minutes
And the tracking number is visible on the order detail page
```

### 模式 5：安全性考虑（Security Considerations）

```gherkin
Given a user who is NOT the account owner
When they attempt to access /account/settings via direct URL
Then they receive a 403 Forbidden response
And the access attempt is logged
```

---

## 优先级框架

采用 MoSCoW 优先级评估方法，根据功能对人物角色的影响来决定优先级：

| 优先级 | 标签 | 定义 | 与人物角色的关联 |
|---------|---------|-----------------------------------------------|------------------------------------------|
| P0（Must） | 必须实现 | 没有这个功能，产品将无法使用 | 阻碍人物角色的主要目标 |
| P1（Should） | 应该实现 | 具有重要价值，延迟实现会造成不便 | 解决前三大痛点 |
| P2（Could） | 可以实现 | 提升用户体验，但非必需 | 改善次要的使用流程 |
| P3（Won’t） | 明确决定不在当前版本中实现 | 需求频率较低或属于特定场景 |

**优先级确定流程：**

1. 列出所有候选功能；
2. 将每个功能与人物角色的痛点或使用流程步骤对应起来；
3. 根据功能对人物角色的影响，使用 MoSCoW 原则进行优先级排序；
4. 验证：所有 P0 级别的功能加在一起后，能否构成一个对目标人物角色有用的产品？
5. 调整功能范围，直到所有 P0 级别的功能都能在预定时间内实现。

---

## 规范编写中的常见错误

| 错误类型 | 例子 | 修正方法 |
|-------------------|-----------------------------------|--------------------------------------------------|
| 需求描述模糊 | “系统应该用户友好” | 明确可衡量的标准：“任务完成时间应在 3 次点击内” |
| 未考虑边界情况 | 只描述了理想使用流程 | 需要补充边界条件、错误处理以及多用户同时使用的场景 |
| 缺少验收标准 | “实现搜索功能” | 为每个使用场景明确给出具体条件（例如：在什么情况下、使用什么方法、达到什么结果） |
| 将解决方案误认为是需求 | “使用 Redis 进行缓存” | 明确需求：“重复查询的响应时间应在 50 毫秒内” |
| 未指定相关人物角色 | “用户可以导出数据” | 明确指出是哪些人物角色需要导出数据以及导出的目的 |
| 范围界定不明确 | “支持所有文件格式” | 列出具体的文件格式（例如：PDF、CSV、XLSX） |
| 未经确认的假设 | 假设某些功能（如身份验证）已经存在 | 明确列出所有依赖的系统、API、功能及数据来源 |

---

## 与工作流程的集成

特性规范与更广泛的开发流程紧密关联：

1. **人物文档**（`docs/PERSONA.md`）——用户需求的权威来源；
2. **特性规范**（`docs/specs/`）——该技能的输出结果，也是开发工作的依据；
3. **任务创建**——每个特性规范会转化为一个或多个开发任务；
4. **实现阶段**——开发人员根据规范来确定功能范围和验收标准；
5. **测试阶段**——质量保证人员根据验收标准编写测试用例；
6. **评审阶段**——代码审查时需确认验收标准是否得到满足。

在使用 `/new-feature` 命令或其他类似工作流程时，请遵循以下步骤：

- 首先阅读相关的人物文档；
- 使用该模板生成特性规范；
- 确保验收标准涵盖了理想使用流程、错误处理以及边界情况；
- 在开始开发之前，与利益相关者确认功能优先级。

---

## 绝对禁止的行为：

1. **绝不要在没有参考人物文档的情况下编写特性规范**——每个功能都是为满足用户需求而存在的；
2. **绝不要忽略验收标准**——看似“显而易见”的需求往往会导致最多的错误；
3. **绝不要使用模糊的描述来定义需求**——“快速”、“简单”、“直观”等描述无法用于测试；
4. **绝不要将多个功能合并到一个规范中**——每个规范应只对应一个功能，并明确其范围；
5. **绝不要在用户故事中描述实现细节**——用户故事应只描述功能需求，而非实现方式；
6. **绝不要在未记录边界情况的情况下就将规范标记为“已批准”**——理想使用流程只是实现过程中的简单部分；
7. **绝不要想当然地假设依赖关系**——必须明确列出规范所依赖的所有系统、API、功能及数据来源。