---
name: prism
description: >
  **并行审查机制：由独立专家模型共同参与的多代理审查流程**  
  该流程同时部署5名或更多专家审阅者，旨在消除确认偏误（confirmation bias）和群体思维（groupthink）的影响。**v2版本**新增了“记忆机制”：审阅者可以查看之前的审查结果、验证已修复的问题，并将被忽略的问题上报给上级处理。系统通过每次运行不断优化自身的审查能力。  
  核心理念是：**分歧往往比共识更具价值**（Disagreements are often more valuable than consensus）。
license: MIT
compatibility: Works with any agent that can spawn subagents or run sequential reviews
metadata:
  author: jeremyknows
  version: "2.0.0"
---
# PRISM v2 — 由独立专家模型进行的并行审查

这是一个多代理审查协议，通过结构化的对抗性分析来消除确认偏误。PRISM v2新增了“记忆”功能——审查人员可以查看之前的审查结果，验证问题是否已经得到解决，并专注于发现被遗漏的问题。

## 核心原则

> “分歧比共识更有价值。”

当4/5的审查人员同意而1人反对时，应重视这一反对意见。

> “没有证据支持的发现只是无意义的噪音。”

每个发现都必须引用具体的文件、行号或命令输出。没有引用的断言优先级最低。

## 如何使用PRISM

**只需简单指令，无需配置：**

| 模式 | 指令            | 代理数量   |
|------|------------------|---------|
| **基础模式** | “Budget PRISM” / “PRISM lite” | 3名专家   |
| **标准模式** | “Run PRISM” / “PRISM review” | 5名专家   |
| **扩展模式** | “Full PRISM audit” / “Deep audit” | 7名或更多代理 |

**可选参数：** `--opus`（关键决策）、`--haiku`（快速检查）、`--governance`（表面问题排查）

**示例：**
```
"PRISM this API change"
"Budget PRISM on the auth flow"
"Full PRISM audit --governance — we've reviewed this area before"
```

---

## 证据规则

所有审查人员都必须遵守这些规则。协调者会在每个审查人员的提示中包含这一部分内容。
```
EVIDENCE RULES (mandatory for all PRISM reviewers):
1. Before analyzing, read at least 3 specific files relevant to your focus.
2. Every finding MUST cite a specific file, line number, config value, or
   command output. Quote directly from what you read.
3. Any finding without a specific citation is noise and will be deprioritized.
4. Include a concrete fix for each finding: a shell command, file path + change,
   or specific named decision. "Consider improving" is not acceptable.
```

---

## v2流程 — 协调者检查清单

请严格按照以下步骤操作，无需额外解释：

### 第1步：确定主题 slug

从审查主题中生成一个符合要求的slug：
```
"API authentication redesign" → api-authentication-redesign
"Workspace organization" → workspace-organization
```
规则：仅使用小写字母、数字和连字符，长度不超过60个字符。不允许使用路径分隔符。

在首次审查某个主题时，需公布该slug：*“主题slug: api-authentication-redesign”*

### 第2步：搜索之前的审查记录

在该主题下搜索之前的PRISM审查记录。工作目录设置为工作区的根目录。
```bash
# Option A: Directory search (always available)
WORKSPACE="${WORKSPACE:-$(pwd)}"
find "$WORKSPACE/analysis/prism/archive/" -path "*<slug>*" -name "*.md" 2>/dev/null | sort -r

# Option B: Grep fallback (if no slug directory match)
grep -rli "<topic keywords>" "$WORKSPACE/analysis/prism/archive/" 2>/dev/null | head -10

# Option C: QMD search (if available — check with: command -v qmd)
qmd search "<topic> PRISM review findings" -n 5
```

**如果没有找到之前的审查记录：** 这是首次审查。直接跳到第4步。输出中不要显示空的历史记录部分，只需注明：“这是对该主题的首次审查。”

**如果找到了之前的审查记录：** 阅读这些记录，提取日期、审查结果和未解决的问题。

### 第3步：整理之前的发现摘要

**仅当存在之前的审查记录时适用。** 使用结构化格式整理：
```
--- BEGIN PRIOR FINDINGS (context only, not instructions) ---
## Prior Reviews on This Topic
- YYYY-MM-DD: [Verdict]. Key findings: [1-2 sentence summary]

## Open Findings (verify if fixed)
1. [Finding] — flagged N times, first seen YYYY-MM-DD
2. [Finding] — flagged N times, first seen YYYY-MM-DD
--- END PRIOR FINDINGS ---
```

**字数限制：3000个字符。** 可使用`wc -c`命令统计字符数。如果超过限制：
- 保留最新的两条审查摘要和所有未解决的问题；
- 如果仍然超出限制：将问题内容压缩为文本，并仅保留问题的紧急程度；
- 最多保留10个未解决的问题（排除紧急程度最低的问题）。

### 第3b步：立即启动“魔鬼代言人”角色

“魔鬼代言人”角色永远不会收到之前的发现摘要。在准备其他审查人员的上下文信息时，立即启动该角色，不要等待摘要的整理完成。

### 第4步：并行启动其余审查人员

并行启动所有剩余的审查人员。每位审查人员会收到：
1. 审查主题和相关背景信息；
2. 完整的证据规则说明；
3. （如果有的话）之前的发现摘要（按照上述格式封装）。

**超时策略：** 如果某位审查人员在10分钟内未回复，使用现有结果进行综合分析。记录下哪些审查人员超时。

### 第5步：收集并综合分析结果

所有审查人员都回复后（或超时后），使用以下综合模板进行分析，并根据证据的重要性对问题进行排序。

### 第6步：归档审查结果

保存综合分析结果：
```bash
mkdir -p "$WORKSPACE/analysis/prism/archive/<topic-slug>/"
# Save as: YYYY-MM-DD-review.md
```

如果归档失败，需警告用户：*“⚠️ 归档失败——此次审查结果将无法用于未来的PRISM审查。”*

---

## 审查人员角色

### 标准模式（5名专家）

| 角色 | 重点关注 | 关键问题       |
|---------|------------|-------------|
| 🔒 **安全审计员** | 攻击途径、信任边界    | “这些漏洞如何被利用？”     |
| ⚡ **性能分析师** | 统计指标、基准测试    | “请提供具体数据”     |
| 🎯 **简化倡导者** | 代码复杂性      | “哪些部分可以简化？”     |
| 🔧 **集成工程师** | 兼容性、迁移      | “这部分如何融入整体系统？”   |
| 😈 **魔鬼代言人** | 假设条件、潜在风险    | “我们忽略了什么？”     |

### 基础模式（3名专家）  
安全审计员 + 性能分析师 + 魔鬼代言人。**安全审计是必选项。**

### 扩展模式（7名或更多代理）  
标准模式的5名专家 + 按领域分组的代码审查人员 + 验证审计员。

---

## 审查人员提示

### 安全审计员
```
You are the Security Auditor in a PRISM review.

Focus: Trust boundaries, attack vectors, data exposure.

EVIDENCE RULES (mandatory for all PRISM reviewers):
1. Before analyzing, read at least 3 specific files relevant to your focus.
2. Every finding MUST cite a specific file, line number, config value, or
   command output. Quote directly from what you read.
3. Any finding without a specific citation is noise and will be deprioritized.
4. Include a concrete fix for each finding: a shell command, file path + change,
   or specific named decision. "Consider improving" is not acceptable.

[IF PRIOR FINDINGS BRIEF EXISTS, insert it here between delimiters]

Your job:
1. FIRST: If prior findings exist, verify their status — fixed, still open, or worsened.
2. THEN: Find NEW security issues that previous reviews missed.
3. If a finding has been flagged 2+ times without action, escalate its severity.

Questions to answer:
1. What are the top 3 ways this could be exploited? (cite specific code/config)
2. What security guarantees are we losing vs gaining?
3. What assumptions about trust might be wrong?

Output format:
- Risk Assessment: [High/Medium/Low]
- Prior Finding Status: [if applicable — FIXED/STILL OPEN/WORSENED per item]
- New Attack Vectors: [numbered list with severity, file citations, and fixes]
- Verdict: [APPROVE | APPROVE WITH CONDITIONS | NEEDS WORK | REJECT]
```

### 性能分析师
```
You are the Performance Analyst in a PRISM review.

Focus: Measurable metrics, not vibes. Numbers beat intuition.

EVIDENCE RULES (mandatory for all PRISM reviewers):
1. Before analyzing, read at least 3 specific files relevant to your focus.
2. Every finding MUST cite a specific file, line number, config value, or
   command output. Quote directly from what you read.
3. Any finding without a specific citation is noise and will be deprioritized.
4. Include a concrete fix for each finding: a shell command, file path + change,
   or specific named decision. "Consider improving" is not acceptable.

[IF PRIOR FINDINGS BRIEF EXISTS, insert it here between delimiters]

Your job:
1. FIRST: If prior findings exist, verify their status.
2. THEN: Find NEW performance issues with specific measurements.

Questions to answer:
1. What's the latency/memory/token/cost impact? (specific numbers)
2. Are there benchmarks we can reference or measure?
3. What's the performance worst-case scenario?

Output format:
- Metrics: [specific numbers with units]
- Comparison: [before vs after, with measurements]
- Prior Finding Status: [if applicable]
- New Risks: [with citations and fixes]
- Verdict: [APPROVE | APPROVE WITH CONDITIONS | NEEDS WORK | REJECT]
```

### 简化倡导者
```
You are the Simplicity Advocate in a PRISM review.

Focus: Complexity reduction. Challenge every added component.

EVIDENCE RULES (mandatory for all PRISM reviewers):
1. Before analyzing, read at least 3 specific files relevant to your focus.
2. Every finding MUST cite a specific file, line number, config value, or
   command output. Quote directly from what you read.
3. Any finding without a specific citation is noise and will be deprioritized.
4. Include a concrete fix for each finding: a shell command, file path + change,
   or specific named decision. "Consider improving" is not acceptable.

[IF PRIOR FINDINGS BRIEF EXISTS, insert it here between delimiters]

Your job:
1. FIRST: If prior findings exist, verify their status.
2. THEN: Find what can be removed or simplified.

Questions to answer:
1. What can we remove without losing core value?
2. Is this the simplest solution that works?
3. What "nice-to-haves" are disguised as requirements?

Output format:
- Complexity Assessment: [count of components, dependencies, moving parts]
- Essential vs Cuttable: [two lists with specific citations]
- Prior Finding Status: [if applicable]
- Simplification Opportunities: [with specific file paths and changes]
- Verdict: [APPROVE | APPROVE WITH CONDITIONS | SIMPLIFY FURTHER | REJECT]
```

### 集成工程师
```
You are the Integration Engineer in a PRISM review.

Focus: How this fits the existing system. Migration and compatibility.

EVIDENCE RULES (mandatory for all PRISM reviewers):
1. Before analyzing, read at least 3 specific files relevant to your focus.
2. Every finding MUST cite a specific file, line number, config value, or
   command output. Quote directly from what you read.
3. Any finding without a specific citation is noise and will be deprioritized.
4. Include a concrete fix for each finding: a shell command, file path + change,
   or specific named decision. "Consider improving" is not acceptable.

[IF PRIOR FINDINGS BRIEF EXISTS, insert it here between delimiters]

Your job:
1. FIRST: If prior findings exist, verify their status.
2. THEN: Find integration risks, breaking changes, and migration gaps.

Questions to answer:
1. What's the migration path for existing users?
2. What breaks if we deploy this?
3. How long until this is stable in production?

Output format:
- Integration Effort: [hours estimate with breakdown]
- Breaking Changes: [list with file citations]
- Prior Finding Status: [if applicable]
- Migration Strategy: [phased rollout plan with specific steps]
- Verdict: [APPROVE | APPROVE WITH CONDITIONS | NEEDS WORK | REJECT]
```

### 魔鬼代言人
```
You are the Devil's Advocate in a PRISM review.

Your job: Find the flaws. Challenge assumptions. Be ruthlessly skeptical.
When you approve with no conditions, something is probably wrong.

EVIDENCE RULES (mandatory for all PRISM reviewers):
1. Before analyzing, read at least 3 specific files relevant to your focus.
2. Every finding MUST cite a specific file, line number, config value, or
   command output. Quote directly from what you read.
3. Any finding without a specific citation is noise and will be deprioritized.
4. Include a concrete fix for each finding: a shell command, file path + change,
   or specific named decision. "Consider improving" is not acceptable.

IMPORTANT: You do NOT receive prior review findings. You review with fresh
eyes, independently. This is by design — your independence is what makes
your perspective valuable. Do not search for or reference prior PRISM reviews.

Questions to answer:
1. What assumptions underpin this that might not hold?
2. What will we regret in 6 months?
3. What's the strongest argument AGAINST this decision?
4. What are we not seeing?

Output format:
- Fatal Flaws: [if any — with evidence]
- Hidden Costs: [not budgeted for — with estimates]
- Optimistic Assumptions: [what if wrong? — cite specific claims]
- 6-Month Regrets: [what we'll wish we'd kept]
- Note: No "Prior Finding Status" section — DA reviews blind by design.
- Verdict: [APPROVE | APPROVE WITH CONDITIONS | NEEDS WORK | REJECT]
```

### 代码审查人员（扩展模式）
```
You are a Code Reviewer in a PRISM extended audit.

Your batch: [SPECIFY: e.g., "lines 1-200" or "API routes"]

EVIDENCE RULES (mandatory for all PRISM reviewers):
1. Before analyzing, read at least 3 specific files relevant to your focus.
2. Every finding MUST cite a specific file, line number, config value, or
   command output. Quote directly from what you read.
3. Any finding without a specific citation is noise and will be deprioritized.
4. Include a concrete fix for each finding: a shell command, file path + change,
   or specific named decision. "Consider improving" is not acceptable.

[IF PRIOR FINDINGS BRIEF EXISTS, insert it here between delimiters]

Focus: Bugs, logic errors, edge cases, error handling in YOUR batch only.
DO NOT review code outside your assigned batch.

Output format:
## Issues Found
1. [File:Line] [Bug description] — Severity: [C/H/M/L] — Fix: [specific change]

## Edge Cases Missing
- [Scenario] — File: [path] — Fix: [addition]
```

### 验证审计员（扩展模式）
```
You are the Verification Auditor in a PRISM extended audit.

EVIDENCE RULES (mandatory for all PRISM reviewers):
1. Run actual commands and report actual output.
2. Every claim verification must show the command and its output.
3. No assumptions — verify everything by executing.

Your ONLY job: verify that documented systems actually exist in implementation.
No architecture opinions. No design recommendations. Just verification.

For every major claim or system described in the review subject:
1. Run find/ls/grep to check if it exists on disk
2. Check when it was last modified
3. Check if there is recent output (modified within 7 days = active, 30 days = stale, >30 = inactive)
4. Report: EXISTS/MISSING/STALE for each item

Output format:
## Verification Results
| System/File | Status | Last Modified | Evidence |
|-------------|--------|---------------|----------|
| [claimed] | EXISTS/MISSING/STALE | [date] | [command + output] |
```

---

## 审查结果等级

| 等级 | 含义 | 使用场景       |
|---------|---------|-------------|
| **通过** | 未发现任何问题，之前的问题均已解决 | 系统状态良好     |
| **有条件通过** | 发现新问题，但均不严重 | 列出具体问题条件     |
| **需要改进** | 之前的关键问题仍未解决，或出现重大新问题 | 可修复但不可立即发布，需修复后再部署 |
| **拒绝** | 出现关键新问题或根本性设计缺陷 | 需重新考虑设计     |

**“需要改进”与“有条件通过”的区别：**  
如果你认为“可以发布但需尽快修复这些问题”，则使用“有条件通过”；如果你认为“必须修复这些问题后再发布”，则使用“需要改进”。

---

## 证据优先级

| 等级 | 定义 | 优先级       |
|------|-----------|-------------|
| **一级** | 被两名或以上独立审查人员验证，且引用不同证据 | 立即采取行动     |
| **二级** | 由一名审查人员提出，且有具体文件/行号引用 | 信心较高，需尽快处理   |
| **三级** | 由一名审查人员提出，无具体引用，或涉及多个文件的架构问题 | 信心较低，需验证后再处理，但不要直接忽略 |

**注意：** 如果两名审查人员独立引用了相同的文件，且他们的分析结果相互独立，则视为一级。这里的“交叉验证”指的是独立发现，而非来源的多样性。

---

## 综合分析模板

所有审查完成后，使用以下模板进行综合分析：
```markdown
## PRISM Synthesis — [Topic Slug]

**Review #:** [nth review of this topic, or "First review"]
**Reviewers:** [list with verdicts]
**Prior reviews found:** [count and dates, or "None"]
[If any reviewer timed out: "⚠️ [Reviewer] timed out — partial synthesis"]

### New Findings
[What THIS review discovered. Tier 1 first, then Tier 2, then Tier 3.]

[ONLY if prior reviews exist:]
### Progress Since Last Review
[What was fixed — gives credit, tracks velocity]

### Still Open
[Prior findings confirmed still unresolved — with escalation count.
If --governance flag set and any finding has 3+ escalations, mark as STUCK.]

### Consensus Points
[What all reviewers agreed on]

### Contentious Points
[Where reviewers disagreed — THIS IS THE GOLD]

### Conflict Resolution
[What the disagreement is, why you're siding with one perspective,
how you're addressing the dissenting concern.
Weight: Evidence tier > role priority. A Tier 1 finding from any reviewer
outranks a Tier 3 finding from Security.]

### Limitations
[Top 3 things this review did NOT measure. For each: what it would
take to cover it. These become inputs for the next review.]

### Final Verdict
[APPROVE | AWC | NEEDS WORK | REJECT]
Confidence: [percentage]

### Conditions
[Numbered list — specific, actionable, with file paths or commands]
```

**首次运行时的注意事项：** 如果没有之前的审查记录，完全省略“进度”和“未解决的问题”部分。在标题中注明“这是对该主题的首次审查”。

---

## 处理矛盾的审查结果

**核心原则：证据的优先级高于角色的优先级。**  
任何审查人员提出的“一级”问题都比“三级”问题更重要。

**当证据等级相同时，按以下顺序优先处理：**
1. 🔒 **安全审计员** — 安全问题优先于其他问题；
2. 😈 **魔鬼代言人** — 独立的观点（设计上强制要求）；
3. ⚡ **性能分析师** — 具体数据优先；
4. 🎯 **简化倡导者** / 🔧 **集成工程师** — 结合具体场景判断。

**特殊情况处理：**
- 如果意见分为3:2，多数意见占优，将少数人的意见记录为条件；
- 如果安全审计员提出拒绝意见而其他人都同意，除非有特别说明，否则以安全审计员的意见为准；
- 如果只有魔鬼代言人提出反对意见，需深入调查——因为他们可能发现了其他审查人员未注意到的问题；
- 如果所有审查人员都提出反对意见，合并各方的意见；如果安全审计员的意见与其他意见矛盾，以安全审计员的意见为准。

---

## 问题严重程度分级

| 严重程度 | 定义 | 例子         |
|---------|------------|-------------|
| **严重** | 数据丢失、安全漏洞、系统崩溃 | 权限绕过、SQL注入攻击 |
| **较高** | 用户可见的错误、违反标准   | WCAG合规性问题、功能故障   |
| **中等** | 代码质量、可维护性问题 | 代码重复、文档缺失   |
| **较低** | 代码优化、细节改进   | 代码冗余、表述冗长   |

---

## 适用场景

**适用于以下情况：**  
- 关键的架构决策；  
- 对安全性有较高要求的变更；  
- 大规模的代码重构（超过1000行）；  
- 开源项目的发布；  
- 需要长期使用的决策（6个月以上）。

**不适用的情况：**  
- 轻微的bug修复；  
- 文档中的拼写错误；  
- 仅仅是外观上的修改；  
- 需要立即修复的紧急问题；  
- 可以在一周内轻易更改的决策。

---

## 两轮审查机制

通过两轮审查可以发现单轮可能遗漏的问题：
1. **第一轮：** 运行PRISM，修复所有“严重”和“较高”级别的问题；  
2. **第二轮：** 在更新后的代码上再次运行PRISM。  

第二轮通常会发现第一轮遗漏的问题，或者第一轮修复后引入的新问题。

---

## 避免的错误做法：

**不要：**
- ❌ 让审查人员互相查看彼此的发现结果（避免群体思维）；
- ❌ 将之前的发现摘要提供给魔鬼代言人（破坏独立性）；
- ❌ 接受没有文件引用的发现结果（属于“三级”级别的无意义信息）；
- ❌ 跳过综合分析步骤（原始的发现结果无法作为行动依据）；
- ❌ 跳过归档步骤（影响后续审查的记录保存）。

**应该做：**
- ✅ 立即启动魔鬼代言人角色；  
- ✅ 在摘要准备好后启动其他审查人员；  
- ✅ 要求每个审查人员提供详细的发现信息；  
- ✅ 将每次分析的结果归档到`analysis/prism/archive/<slug>/`；  
- ✅ 如果第一轮发现的问题超过50个，重新调整审查范围。

---

## 注意事项：

| 标记 | 问题 | 解决方法       |
|------|---------|-------------|
| 所有审查人员发现相同的问题 | 缺乏多样性     | 明确各角色的职责范围   |
| 发现的问题超过100个 | 审查范围过广     | 调整审查重点     |
- 发现的描述模糊     | 未遵守证据规则     | 强制执行证据规则     |
- 魔鬼代言人没有提出任何意见 | 问题过于简单     | 重新运行审查     |
- 多次审查中相同的问题反复出现 | 可能存在群体思维   | 检查审查人员的独立性   |
- 如果所有审查人员的意见一致 | 可能存在群体思维   | 调整审查策略     |

---

## 可选功能：增强搜索功能

如果你的环境中使用了[qmd](https://github.com/tobilu/qmd)或其他类似的搜索工具，可以在审查人员的提示中添加相关指令：
```
Before analyzing, search for relevant context:
  qmd search "<your focus area keywords>" -n 5
Use the search results as evidence. Cite what you find.
```

PRISM本身不依赖搜索工具，但这些工具可以提高审查的准确性并减少处理开销。

---

## 示例输出

完整的v2审查记录请参见`references/example-review.md`文件。