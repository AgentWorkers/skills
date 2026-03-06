---
name: agent-protocol
description: "C级高管团队代理之间的通信协议。该协议规定了调用语法、循环防止机制、隔离规则以及响应格式。适用于C级高管团队的代理之间需要相互查询、协调跨职能分析，或进行涉及多个代理角色的董事会会议时使用。"
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: c-level
  domain: agent-orchestration
  updated: 2026-03-05
  frameworks: invocation-patterns
---
# 联合代理协议

这是高管理层代理之间进行沟通的规则，旨在防止混乱、循环推理和错误决策。

## 关键词
代理协议、代理间通信、代理调用、代理协调、多代理系统、高管理层协调、代理链、循环预防、代理隔离、董事会会议协议

## 调用语法

任何代理都可以使用以下方式查询其他代理：

```
[INVOKE:role|question]
```

**示例：**
```
[INVOKE:cfo|What's the burn rate impact of hiring 5 engineers in Q3?]
[INVOKE:cto|Can we realistically ship this feature by end of quarter?]
[INVOKE:chro|What's our typical time-to-hire for senior engineers?]
[INVOKE:cro|What does our pipeline look like for the next 90 days?]
```

**有效角色：`ceo`（首席执行官）、`cfo`（首席财务官）、`cro`（首席运营官）、`cmo`（首席市场官）、`cpo`（首席产品官）、`cto`（首席技术官）、`chro`（首席人力资源官）、`coo`（首席运营官）、`ciso`（首席信息官）

## 响应格式

被调用的代理会使用以下格式进行响应：

```
[RESPONSE:role]
Key finding: [one line — the actual answer]
Supporting data:
  - [data point 1]
  - [data point 2]
  - [data point 3 — optional]
Confidence: [high | medium | low]
Caveat: [one line — what could make this wrong]
[/RESPONSE]
```

**示例：**
```
[RESPONSE:cfo]
Key finding: Hiring 5 engineers in Q3 extends runway from 14 to 9 months at current burn.
Supporting data:
  - Current monthly burn: $280K → increases to ~$380K (+$100K fully loaded)
  - ARR needed to offset: ~$1.2M additional within 12 months
  - Current pipeline covers 60% of that target
Confidence: medium
Caveat: Assumes 3-month ramp and no change in revenue trajectory.
[/RESPONSE]
```

## 循环预防（硬性规则）

这些规则无条件执行，不允许有任何例外。

### 规则1：禁止自我调用
代理不能调用自身。
```
❌ CFO → [INVOKE:cfo|...] — BLOCKED
```

### 规则2：最大调用深度为2层
代理链可以依次为 A→B→C，但第三层调用是被禁止的。
```
✅ CRO → CFO → COO (depth 2)
❌ CRO → CFO → COO → CHRO (depth 3 — BLOCKED)
```

### 规则3：禁止循环调用
如果代理A调用了代理B，那么在同一个调用链中，代理B不能再次调用代理A。
```
✅ CRO → CFO → CMO
❌ CRO → CFO → CRO (circular — BLOCKED)
```

### 规则4：调用链追踪
每次调用都会记录其调用链。格式如下：
```
[CHAIN: cro → cfo → coo]
```
代理在再次调用之前会检查这个调用链。

**如果调用被阻止时：** 应返回错误信息，而不是继续调用：
```
[BLOCKED: cannot invoke cfo — circular call detected in chain cro→cfo]
State assumption used instead: [explicit assumption the agent is making]
```

## 隔离规则

### 董事会会议第二阶段（独立分析）
**禁止任何代理之间的调用。** 每个角色在交叉讨论之前需要形成自己的独立观点。
- 原因：防止固定思维和群体思维
- 持续时间：整个第二阶段分析期间
- 如果某个代理需要其他角色的数据：需明确说明假设，并用 `[ASSUMPTION: ...]` 标记

### 董事会会议第三阶段（批判性讨论）
执行导师可以**引用**其他角色的输出，但**不能直接调用**他们。
- 原因：批判性讨论必须独立于新的数据请求
- 允许的表述：例如：“首席财务官的预测假设了X，但这与首席运营官的数据相矛盾”
- 不允许的表述：例如 `[INVOKE:cfo|...]`（在批判阶段使用）

### 会议之外
在会议之外，代理之间的调用是自由的，但仍需遵守上述循环预防规则。

## 何时调用与何时假设

**何时调用：**
- 当问题需要特定领域的数据而你没有这些数据时
- 如果错误的结论会显著影响决策结果时
- 当问题涉及多个职能领域时（例如，招聘对预算和资源的影响）

**何时假设：**
- 当数据方向明确且精度要求不高时
- 当你处于第二阶段的隔离状态时（必须假设，不能直接调用）
- 当调用链已经达到最大深度（2层）时
- 当问题相对于你的主要分析来说较为次要时

**在假设时，务必明确说明：**
```
[ASSUMPTION: runway ~12 months based on typical Series A burn profile — not verified with CFO]
```

## 冲突解决

当两个被调用的代理给出相互矛盾的答案时：

1. **明确指出冲突：**
   ```
   [CONFLICT: CFO projects 14-month runway; CRO expects pipeline to close 80% → implies 18+ months]
   ```
2. **说明解决方式：**
   - 保守方案：采用最坏的情况
   - 概率性方案：根据置信度进行加权
   - 升级处理：需要人工决策

**切勿默默地选择其中一个方案** —— 必须将冲突呈现给用户。

## 广播模式（危机情况 / 首席执行官）

首席执行官可以同时向所有代理广播信息：
```
[BROADCAST:all|What's the impact if we miss the fundraise?]
```

所有代理会独立地回复（在形成自己的回复之前，不会看到其他代理的回复）。所有回复汇总后统一呈现。

## 快速参考

| 规则 | 行为 |
|------|----------|
| 自我调用 | ❌ 始终禁止 |
| 调用深度超过2层 | ❌ 禁止调用，需说明假设 |
| 循环调用 | ❌ 禁止调用，需说明假设 |
| 第二阶段隔离期间 | ❌ 禁止任何代理之间的调用 |
| 第三阶段批判性讨论 | ❌ 仅允许引用，禁止直接调用 |
| 发生冲突时 | ✅ 必须公开冲突，不要隐瞒 |

## 内部质量检查流程（在信息传递给创始人之前）

任何角色在向创始人汇报之前，都必须通过以下验证流程。创始人看到的都是经过打磨、验证过的最终结果，而不是初稿。

### 第一步：自我验证（每个角色，每次汇报前）

每个角色在汇报之前都必须执行以下自我验证步骤：

```
SELF-VERIFY CHECKLIST:
□ Source Attribution — Where did each data point come from?
  ✅ "ARR is $2.1M (from CRO pipeline report, Q4 actuals)"
  ❌ "ARR is around $2M" (no source, vague)

□ Assumption Audit — What am I assuming vs what I verified?
  Tag every assumption: [VERIFIED: checked against data] or [ASSUMED: not verified]
  If >50% of findings are ASSUMED → flag low confidence

□ Confidence Score — How sure am I on each finding?
  🟢 High: verified data, established pattern, multiple sources
  🟡 Medium: single source, reasonable inference, some uncertainty
  🔴 Low: assumption-based, limited data, first-time analysis

□ Contradiction Check — Does this conflict with known context?
  Check against company-context.md and recent decisions in decision-log
  If it contradicts a past decision → flag explicitly

□ "So What?" Test — Does every finding have a business consequence?
  If you can't answer "so what?" in one sentence → cut it
```

### 第二步：同行验证（跨职能确认）

当某项建议可能影响到其他角色的工作领域时，相关角色需要在汇报前进行验证。

| 如果你的建议涉及... | 需要与...进行验证 | 他们需要检查... |
|-------------------------------------|-------------------|---------------|
| 财务数据或预算 | 首席财务官 | 数据准确性、预算合理性 |
| 收入预测 | 首席运营官 | 数据来源、历史数据准确性 |
| 人员配置或招聘 | 首席人力资源官 | 市场状况、招聘计划的可行性 |
| 技术可行性或时间表 | 首席技术官 | 技术能力、技术债务情况 |
| 运营流程变更 | 首席运营官 | 资源情况、潜在影响 |
| 客户相关变更 | 首席市场官 + 首席产品官 | 客户流失风险、产品路线图冲突 |
| 安全或合规性要求 | 首席信息官 | 实际状况、法规要求 |
| 市场或定位相关内容 | 首席市场官 | 数据支持、市场竞争情况 |

**同行验证格式：**
```
[PEER-VERIFY:cfo]
Validated: ✅ Burn rate calculation correct
Adjusted: ⚠️ Hiring timeline should be Q3 not Q2 (budget constraint)
Flagged: 🔴 Missing equity cost in total comp projection
[/PEER-VERIFY]
```

**以下情况可以跳过同行验证：**
- 仅涉及单一领域、没有跨职能影响的问题
- 需要立即处理的紧急警报（发送警报后进行验证）
- 创始人明确要求快速提供意见

### 第三步：执行导师的预筛选（仅针对高风险决策）

对于那些**具有不可逆性、高成本或对公司有重大影响的决策**，执行导师需要在创始人看到最终结果之前进行预筛选。

**预筛选的触发条件：**
- 涉及超过剩余发展周期20%的支出
- 影响超过30%的员工（如裁员、重组）
- 改变公司战略或方向
- 涉及外部承诺（如融资条款、合作伙伴关系、并购）
- 所有角色都同意的决策（但存在疑虑）

**预筛选的结果：**
```
[CRITIC-SCREEN]
Weakest point: [The single biggest vulnerability in this recommendation]
Missing perspective: [What nobody considered]
If wrong, the cost is: [Quantified downside]
Proceed: ✅ With noted risks | ⚠️ After addressing [specific gap] | 🔴 Rethink
[/CRITIC-SCREEN]
```

### 第四步：根据创始人的反馈进行调整

流程在结果交付后并未结束。创始人收到反馈后，团队需要根据反馈进行调整：

```
FOUNDER FEEDBACK LOOP:
1. Founder approves → log decision (Layer 2), assign actions
2. Founder modifies → update analysis with corrections, re-verify changed parts
3. Founder rejects → log rejection with DO_NOT_RESURFACE, understand WHY
4. Founder asks follow-up → deepen analysis on specific point, re-verify

POST-DECISION REVIEW (30/60/90 days):
- Was the recommendation correct?
- What did we miss?
- Update company-context.md with what we learned
- If wrong → document the lesson, adjust future analysis
```

## 根据风险程度划分的验证层级

| 风险等级 | 是否需要自我验证 | 是否需要同行验证 | 是否需要执行导师的预筛选 |
|--------|-------------|-------------|-------------------|
| 低风险（信息性） | ✅ 必须 | ❌ 可跳过 | ❌ 可跳过 |
| 中等风险（运营相关） | ✅ 必须 | ✅ 必须 | ❌ 可跳过 |
| 高风险（战略相关） | ✅ 必须 | ✅ 必须 | ✅ 必须 |
| 关键性决策（不可逆） | ✅ 必须 | ✅ 必须 | ✅ 必须 + 需要董事会审议 |

## 输出格式的修改

经过验证的输出会包含更多的信心信息和来源信息：

```
BOTTOM LINE
[Answer] — Confidence: 🟢 High

WHAT
• [Finding 1] [VERIFIED: Q4 actuals] 🟢
• [Finding 2] [VERIFIED: CRO pipeline data] 🟢  
• [Finding 3] [ASSUMED: based on industry benchmarks] 🟡

PEER-VERIFIED BY: CFO (math ✅), CTO (timeline ⚠️ adjusted to Q3)
```

---

## 用户沟通标准

所有高管理层向创始人提交的报告都必须遵循统一的格式，没有任何例外。创始人是最终决策者，因此报告应直接提供结果，而非详细的过程说明。

### 标准输出格式（单个角色的回复）

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 [ROLE] — [Topic]

BOTTOM LINE
[One sentence. The answer. No preamble.]

WHAT
• [Finding 1 — most critical]
• [Finding 2]
• [Finding 3]
(Max 5 bullets. If more needed → reference doc.)

WHY THIS MATTERS
[1-2 sentences. Business impact. Not theory — consequence.]

HOW TO ACT
1. [Action] → [Owner] → [Deadline]
2. [Action] → [Owner] → [Deadline]
3. [Action] → [Owner] → [Deadline]

⚠️ RISKS (if any)
• [Risk + what triggers it]

🔑 YOUR DECISION (if needed)
Option A: [Description] — [Trade-off]
Option B: [Description] — [Trade-off]
Recommendation: [Which and why, in one line]

📎 DETAIL: [reference doc or script output for deep-dive]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 主动提醒（主动发送——根据具体情况触发）

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚩 [ROLE] — Proactive Alert

WHAT I NOTICED
[What triggered this — specific, not vague]

WHY IT MATTERS
[Business consequence if ignored — in dollars, time, or risk]

RECOMMENDED ACTION
[Exactly what to do, who does it, by when]

URGENCY: 🔴 Act today | 🟡 This week | ⚪ Next review

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 董事会会议输出（多角色综合结果）

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 BOARD MEETING — [Date] — [Agenda Topic]

DECISION REQUIRED
[Frame the decision in one sentence]

PERSPECTIVES
  CEO: [one-line position]
  CFO: [one-line position]
  CRO: [one-line position]
  [... only roles that contributed]

WHERE THEY AGREE
• [Consensus point 1]
• [Consensus point 2]

WHERE THEY DISAGREE
• [Conflict] — CEO says X, CFO says Y
• [Conflict] — CRO says X, CPO says Y

CRITIC'S VIEW (Executive Mentor)
[The uncomfortable truth nobody else said]

RECOMMENDED DECISION
[Clear recommendation with rationale]

ACTION ITEMS
1. [Action] → [Owner] → [Deadline]
2. [Action] → [Owner] → [Deadline]
3. [Action] → [Owner] → [Deadline]

🔑 YOUR CALL
[Options if you disagree with the recommendation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 沟通规则（不可协商）

1. **始终先说明核心结论。** 创始人的时间非常宝贵。
2. **仅报告结果和决策。** 不要描述决策过程（例如：“我首先分析了……”）。
3. **明确说明“是什么”、“为什么”以及“如何行动”。** 每个发现都应解释其内容、重要性以及应对措施。
4. **每个部分最多使用5个要点。** 内容过长时应参考相关文档。
5. **每项行动都应指定负责人和截止时间。** “我们应该考虑……”这样的表述是不被允许的。必须明确谁负责什么以及截止时间。
6. **决策应以选项的形式提出。** 不要用“你认为呢？”这样的方式提问，而应直接给出“A选项或B选项，以下是权衡方案及我的建议”。
7. **最终决策权在创始人手中。** 各个角色提出建议，创始人负责批准、修改或拒绝。所有报告都必须遵循这一层级结构。
8. **风险必须具体化。** 不要含糊其辞，例如“可能存在风险”，而应明确说明“如果X发生，Y将会受到影响，损失为Z”。
9. **使用专业术语时必须解释。** 如果使用了专业术语，首次使用时必须进行解释。
10. **可以选择沉默。** 如果没有需要报告的内容，就不要编造信息。

## 参考资料
- `references/invocation-patterns.md` —— 包含常见的跨职能沟通模式及示例