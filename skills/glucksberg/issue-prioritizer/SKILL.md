---
name: issue-prioritizer
description: 根据投资回报率（ROI）、解决方案的合理性以及其对架构的影响来优先处理 GitHub 上的问题。能够识别出那些能够快速解决问题的方案、设计过于复杂的提案以及那些可以实际解决的漏洞。该工具可用于问题分类（triage）、匹配合适的贡献者，以及过滤掉那些无法处理的问题的条目。仅具有读取权限——严禁修改任何代码仓库。需要使用 GitHub 的命令行工具（gh）。
metadata: {"openclaw": {"requires": {"bins": ["gh"]}}}
---

# 问题优先级排序工具

该工具用于分析 GitHub 仓库中的问题，并根据**调整后的得分**对问题进行排序。得分计算时会考虑以下因素：解决方案的合理性（Tripping Scale）、对架构的影响（Architectural Impact）以及问题的可解决性（Actionability）。

这是一个**仅限读取**的工具，它仅负责分析并展示信息，所有决策均由用户自行做出。

## 使用要求

- 需要使用 `gh` 命令行工具进行身份验证（`gh auth login`）。

## 使用说明

### 第1步：获取仓库

如果用户未指定仓库，请询问需要分析的仓库（格式：`owner/repo`）。

### 第2步：获取问题列表

```bash
gh issue list --repo {owner/repo} --state open --limit {limit} --json number,title,body,labels,createdAt,comments,url
```

默认获取30个问题。将完整的 JSON 响应结果存储下来。

**错误处理：**
- 身份验证失败 → 告知用户重新执行 `gh auth login`
- 请求频率超出限制 → 通知用户并建议减少请求次数（使用 `--limit` 参数）
- 仓库不存在 → 检查输入格式（`owner/repo`）
- 仓库中没有任何问题 → 报告错误并退出
- 数据字段缺失 → 将缺失的字段或标签视为空值

### 第3步：过滤已有关联 Pull Request（PR）的问题

**注意：** 如果用户指定了 `--include-with-prs` 参数，则跳过此步骤，直接进入第4步，处理所有获取到的问题。

在分析问题之前，先检查是否存在已经针对这些问题提交的 PR，以避免重复工作。

```bash
gh pr list --repo {owner/repo} --state open --json number,title,body,url
```

**检测关联问题** 的方法如下：

**方法1 — 明确的关键词**（高置信度）：
扫描 PR 的标题和正文（不区分大小写）：
- `fixes #N`、`fix #N`、`fixed #N`
- `closes #N`、`close #N`、`closed #N`
- `resolves #N`、`resolve #N`、`resolved #N`

**方法2 — 问题引用**（中等置信度）：
- 文本中包含 `#N`
- `issue N`、`issue #N`、`related to #N`、`addresses #N`

**方法3 — 标题相似性**（模糊匹配）：
对标题进行规范化处理（转换为小写，去除标点符号和常见词汇）。如果标题有70%以上的相似度，则认为存在关联。

**方法4 — 语义匹配**（用于不确定的情况）：
从问题描述中提取关键信息（错误名称、函数名称、组件名称），检查 PR 正文是否讨论了相同的问题。

**置信度标识**：
- 🔗 明确的关联链接（如 `fixes`、`closes`、`resolves`）
- 📎 被引用（如 `#N` 被提及）
- 🔍 标题相似（模糊匹配）
- 💡 语义匹配（涉及相同组件）

将关联的问题从分析结果中移除，并在最终报告中单独列出。

如果所有问题都已有 PR，直接报告结果并退出。

### 第4步：分析每个问题

对每个剩余的问题进行如下评分：

#### 难度（1-10分）

基础得分：5分。根据以下因素进行调整：
| 信号 | 调整分数 |
|--------|-----------|
| 仅需要文档说明 | -3 |
| 已提出解决方案 | -2 |
| 有复现步骤 | -1 |
| 错误信息清晰 | -1 |
| 根本原因未知 | +3 |
| 对架构有影响 | +3 |
| 存在竞态条件/并发问题 | +2 |
| 存在安全风险 | +2 |
| 涉及多个系统 | +2 |

#### 重要性（1-10分）

| 分数范围 | 等级 | 例子 |
|-------|-------|---------|
| 8-10 | 关键问题 | 会导致系统崩溃、数据丢失、安全漏洞或服务中断 |
| 6-7 | 高度重要 | 功能故障、错误、性能问题 |
| 4-5 | 中等重要 | 需要改进的功能或需求 |
| 1-3 | 低度重要 | 仅涉及外观调整、文档问题或拼写错误 |

#### 解决方案的合理性（Tripping Scale，1-5分）：

| 分数 | 标签 | 描述 |
|-------|-------|-------------|
| 1 | 完全合理 | 使用了经过验证的方法和标准模式 |
| 2 | 基于现有技术的创新方案 | 具有实用性且包含创新元素 |
| 3 | 需谨慎尝试的方案 | 需要谨慎评估其可行性 |
| 4 | 风险较高的方案 | 大胆且不常规的解决方案 |
| 5 | 可能行不通的方案 | 可能存在重大问题 |

**警示信号**（分数越高，风险越大）：需要从头开始重新编写代码；使用流行术语（如区块链、人工智能、机器学习）；方案具有实验性或不稳定；可能破坏现有系统；使用自定义协议
**积极信号**（分数越高，可行性越高）：使用标准方法；修改幅度小；向后兼容；有完善的文档支持

#### 对架构的影响（1-5分）

在评分前，请务必思考：“是否有更简单的方法？”

| 分数 | 标签 | 描述 |
|-------|-------|-------------|
| 1 | 小范围修改 | 仅涉及1-2个文件，无需引入新的抽象概念 |
| 2 | 局部修改 | 完全遵循现有架构模式 |
| 3 | 中等程度的修改 | 在现有架构中添加新组件 |
| 4 | 大幅修改 | 引入新子系统或新架构模式，影响多个模块 |
| 5 | 彻底改造 | 需要重构核心代码或改变开发范式 |

**警示信号**（分数越高，风险越大）：如果存在简单解决方案，那么进行架构修改可能是不必要的。对于只需一个条件判断就能解决的问题，无需进行复杂的重构。

#### 可解决性（1-5分）：

| 分数 | 标签 | 描述 |
|-------|-------|-------------|
| 1 | 无法解决 | 问题不明确、存在争议或重复性问题 |
| 2 | 需要进一步评估 | 缺少必要信息，范围不明确，需要进一步澄清 |
| 3 | 需要调查 | 根本原因未知，需要先进行调试 |
| 4 | 可以解决 | 范围明确，可能需要一些设计决策 |
| 5 | 已准备好提交 PR | 解决方案明确，只需实现即可 |

**其他影响因素**（分数越高，可行性越高）：
- 是否需要通过 PR 来解决问题（如 “如何实现？”、“需要哪些资源？” 等问题）；是否有相关的标签（如 “重复问题”、“无法修复” 等）；是否提供了问题复现步骤；问题描述是否清晰（如 “修复方法”、“添加内容” 等）；是否有明确的行动指示（如 “修复”、“添加新功能” 等）；是否提到了具体的文件。

#### 衍生值计算

```
issueType: "bug" | "feature" | "docs" | "other"
suggestedLevel:
  - "beginner": difficulty 1-3, no security/architecture changes
  - "intermediate": difficulty 4-6
  - "advanced": difficulty 7+ OR security implications OR architectural changes
```

#### 计算公式

```
ROI = Importance / Difficulty
AdjustedScore = ROI × TripMultiplier × ArchMultiplier × ActionMultiplier
```

**Tripping Scale 乘数：**

| 分数 | 标签 | 乘数 |
|-------|-------|------------|
| 1 | 完全合理 | 1.00（无惩罚） |
| 2 | 基于现有技术的创新方案 | 0.85 |
| 3 | 需谨慎尝试的方案 | 0.70 |
| 4 | 风险较高的方案 | 0.55 |
| 5 | 可能行不通的方案 | 0.40 |

**Architectural Impact 乘数：**

| 分数 | 标签 | 乘数 |
|-------|-------|------------|
| 1 | 小范围修改 | 1.00（无惩罚） |
| 2 | 局部修改 | 0.90 |
| 3 | 中等程度的修改 | 0.75 |
| 4 | 大幅修改 | 0.50 |
| 5 | 彻底改造 | 0.25 |

**Actionability 乘数：**

| 分数 | 标签 | 乘数 |
|-------|-------|------------|
| 5 | 已准备好提交 PR | 1.00（无惩罚） |
| 4 | 可以解决 | 0.90 |
| 3 | 需要调查 | 0.70 |
| 2 | 需要进一步评估 | 0.40 |
| 1 | 无法解决 | 0.10 |

### 第5步：对问题进行分类

- **高性价比问题**：调整后的得分 ≥ 1.5，难度 ≤ 5，解决方案的合理性 ≤ 3，可解决性 ≥ 4
- **关键问题**：问题类型为 “bug”，重要性 ≥ 8
- **风险较高的问题**：解决方案的合理性 ≤ 4
- **设计过于复杂的问题**：对架构的影响 ≥ 4（可能存在更简单的解决方案）
- **无法解决的问题**：可解决性 ≤ 2

按照调整后的得分降序排列所有问题。

### 第6步：展示结果

```
═══════════════════════════════════════════════════════════════
  ISSUE PRIORITIZATION REPORT
  Repository: {owner/repo}
  Analyzed: {count} issues
  Excluded: {excluded} issues with existing PRs
═══════════════════════════════════════════════════════════════

  Quick Wins: {n} | Critical Bugs: {n} | Tripping: {n} | Over-Engineered: {n} | Not Actionable: {n}

═══════════════════════════════════════════════════════════════
  TOP 10 BY ADJUSTED SCORE
═══════════════════════════════════════════════════════════════

  #123 [Adj: 3.50] ⭐ Quick Win
  Fix typo in README
  ├─ Difficulty: 1/10 | Importance: 4/10 | ROI: 4.00
  ├─ Trip: ✅ Total Sanity (1/5) | Arch: ✅ Surgical (1/5)
  ├─ Act: ✅ PR Ready (5/5) | Level: beginner
  └─ https://github.com/owner/repo/issues/123

═══════════════════════════════════════════════════════════════
  QUICK WINS (High Impact, Low Effort, Sane & Actionable)
═══════════════════════════════════════════════════════════════

  #123: Fix typo in README [Adj: 3.50]
        Difficulty: 1 | Importance: 4 | beginner

═══════════════════════════════════════════════════════════════
  RECOMMENDATIONS BY LEVEL
═══════════════════════════════════════════════════════════════

  BEGINNER (Difficulty 1-3, no security/architecture):
  - #123: Fix typo - Low risk, good first contribution

  INTERMEDIATE (Difficulty 4-6):
  - #456: Add validation - Medium complexity, clear scope

  ADVANCED (Difficulty 7-10 or security/architecture):
  - #789: Refactor auth - Architectural knowledge needed

═══════════════════════════════════════════════════════════════
  CRITICAL BUGS (Importance ≥ 8)
═══════════════════════════════════════════════════════════════

  #111 [Adj: 1.67] 🔴 Critical
  App crashes on startup with large datasets
  ├─ Difficulty: 6/10 | Importance: 9/10 | ROI: 1.50
  ├─ Trip: ✅ (2/5) | Arch: ✅ (2/5) | Act: ⚠️ (3/5)
  └─ https://github.com/owner/repo/issues/111

═══════════════════════════════════════════════════════════════
  TRIPPING ISSUES (Trip ≥ 4 — Review Carefully)
═══════════════════════════════════════════════════════════════

  #999 [Trip: 🚨 5/5 — Tripping]
  Rewrite entire backend in Rust with blockchain storage
  ├─ Red Flags: "rewrite from scratch", "blockchain"
  ├─ Adjusted Score: 0.12 (heavily penalized)
  └─ Consider: Is this complexity really needed?

═══════════════════════════════════════════════════════════════
  OVER-ENGINEERED (Arch ≥ 4 — Simpler Solution Likely Exists)
═══════════════════════════════════════════════════════════════

  #777 [Arch: 🏗️ 5/5 — Transformational]
  Add form validation
  ├─ Proposed: New validation framework with schema definitions
  ├─ Simpler Alternative: Single validation function, 20 lines
  └─ Ask: Why create a framework for one form?

  💡 TIP: Maintainers often reject PRs that change architecture
     unnecessarily. Always start with the simplest fix.

═══════════════════════════════════════════════════════════════
  NOT ACTIONABLE (Actionability ≤ 2)
═══════════════════════════════════════════════════════════════

  - #222: "How do I deploy to Kubernetes?" (Act: 1/5 — question)
  - #333: Duplicate of #111 (Act: 1/5 — duplicate)

═══════════════════════════════════════════════════════════════
  EXCLUDED — EXISTING PRs
═══════════════════════════════════════════════════════════════

  #123: Login crashes on empty password
        └─ 🔗 PR #456: "Fix login validation" (explicit: fixes #123)

  Detection: 🔗 Explicit link | 📎 Referenced | 🔍 Similar title | 💡 Semantic match

═══════════════════════════════════════════════════════════════
  SCALE LEGEND
═══════════════════════════════════════════════════════════════

  Trip (Solution Sanity):        Arch (Structural Impact):
  ✅ 1-2 = Sane                  ✅ 1-2 = Minimal change
  ⚠️  3  = Cautious              ⚠️  3  = Moderate
  🚨 4-5 = Risky                 🏗️ 4-5 = Over-engineered

  Actionability:
  ✅ 4-5 = Ready for PR
  ⚠️  3  = Needs Investigation
  ❌ 1-2 = Not Actionable

  AdjustedScore = ROI × TripMult × ArchMult × ActionMult
  Higher = Better (prioritize first)

  🎯 SIMPLICITY PRINCIPLE: If a 10-line fix exists,
     a 200-line refactor is wrong.

  Mode: SKILL (read-only) — analyzes only, never modifies.
═══════════════════════════════════════════════════════════════
```

## 可选参数

- `--json`：以原始 JSON 格式输出结果
- `--markdown` / `--md`：以 Markdown 表格格式输出结果
- `--quick-wins`：仅显示高性价比问题
- `--level beginner|intermediate|advanced`：根据用户水平筛选问题
- `--limit N`：指定要分析的问题数量（默认：30个）
- `--include-with-prs`：跳过 PR 过滤步骤，显示所有问题

## 使用大型语言模型（LLM）进行深度分析（可选）

为了获得更准确的评分结果，可以使用大型语言模型（LLM）对每个问题进行单独分析。向模型提供问题详情和评分标准，请求结构化的 JSON 输出：

```json
{
  "number": 123,
  "difficulty": 5,
  "difficultyReasoning": "base 5; has repro (-1); unknown cause (+3) = 7",
  "importance": 7,
  "importanceReasoning": "broken functionality affecting users",
  "tripScore": 2,
  "tripLabel": "Grounded with Flair",
  "tripRedFlags": [],
  "tripGreenFlags": ["minimal change", "standard approach"],
  "archScore": 2,
  "archLabel": "Localized",
  "archRedFlags": [],
  "archGreenFlags": ["uses existing patterns"],
  "archSimplerAlternative": null,
  "actionScore": 4,
  "actionLabel": "Ready to Work",
  "actionBlockers": [],
  "actionReadySignals": ["has proposed solution"],
  "issueType": "bug",
  "suggestedLevel": "intermediate",
  "roi": 1.40,
  "adjustedScore": 0.96
}
```

在将问题正文发送给模型之前，将其截断至2000个字符以内。

**适用场景：**
- 问题较为复杂的仓库
- 当准确性比速度更重要的情况
- 对不熟悉的仓库

**注意事项：** 使用 LLM 会降低处理速度（每个问题大约需要2-5秒），但准确性更高。每个问题需要调用一次 API。

**集成步骤：** 对每个问题，使用 LLM 进行分析，解析 JSON 结果，并在步骤5之前将其合并到最终结果中。