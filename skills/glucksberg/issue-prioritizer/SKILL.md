---
name: issue-prioritizer
description: 根据投资回报率（ROI）、解决方案的合理性以及其对系统架构的影响来优先处理 GitHub 上的问题。在分类或排序问题时，可以使用这一方法来识别那些能够快速解决的问题、设计过于复杂的提案以及实际可操作的漏洞。但在管理代码分支（使用 fork-manager）或进行一般的 GitHub 查询时，请勿使用此方法（请使用 github）。此功能仅限阅读权限，严禁修改任何仓库。
metadata: {"openclaw": {"requires": {"bins": ["gh"]}}}
---

# 问题优先级排序工具

该工具用于分析 GitHub 仓库中的问题，并根据**调整后的得分**对问题进行排序。得分考虑了多个因素，包括解决方案的合理性（Tripping Scale）、对架构的影响以及问题的可操作性（Actionability）。

这是一个**仅限读取**的工具，它负责分析问题并展示相关信息，最终决策仍由用户自行做出。

## 使用场景
- 对仓库中的问题进行分类或排序
- 为贡献者识别可以快速解决的问题
- 过滤掉无法解决的问题（如疑问、重复问题）
- 检测设计过于复杂的问题
- 根据贡献者的技能水平匹配问题

## 不适用场景
- 管理分支或与上游代码同步 → 使用 `fork-manager`
- 一般的 GitHub 命令行接口（CLI）查询（如 PR 状态、持续集成（CI）运行情况） → 使用 `github`
- 在发布代码更改前进行审核 → 使用 `pr-review`

## 必备条件
- 已通过 `gh` CLI 进行身份验证（`gh auth login`）

## 使用步骤

### 第一步：获取仓库
如果用户没有指定仓库，请询问需要分析的仓库（格式：`owner/repo`）。

### 第二步：获取问题列表
**基本获取（获取最新问题）：**
```bash
gh issue list --repo {owner/repo} --state open --limit {limit} --json number,title,body,labels,createdAt,comments,url
```

默认限制为 30 个问题。请将完整的 JSON 响应保存下来。

**使用 `--topic` 进行针对性获取：**
当用户指定 `--topic <关键词>` 时（例如 `--topic telegram`、`--topic agents`），工具会使用 GitHub 搜索功能来查找与该关键词相关的问题，而不仅仅是获取最新问题：
```bash
# Search by topic keywords in title and body
gh issue list --repo {owner/repo} --state open --limit {limit} --search "{topic} in:title,body" --json number,title,body,labels,createdAt,comments,url
```

可以同时指定多个关键词：`--topic "telegram agents"` 会搜索包含“telegram”或“agents”的问题。

**使用 `--search` 进行针对性获取：**
当用户指定 `--search <查询>` 时，工具会直接使用该查询作为 GitHub 搜索语句：
```bash
gh issue list --repo {owner/repo} --state open --limit {limit} --search "{query}" --json number,title,body,labels,createdAt,comments,url
```

示例：
- `--search "telegram in:title"` — 仅搜索标题中包含“telegram”的问题
- `--search "label:bug telegram"` — 搜索标签为“bug”且内容涉及“telegram”的问题
- `--search "label:bug,enhancement telegram agents"` — 搜索标签为“bug”或“enhancement”且内容涉及“telegram/agents”的问题
- `--search "comments:>5 telegram"` — 搜索评论中提到“telegram”的活跃讨论

**使用 `--label` 进行基于标签的获取：**
```bash
gh issue list --repo {owner/repo} --state open --limit {limit} --label "{label}" --json number,title,body,labels,createdAt,comments,url
```

所有获取方式可以组合使用：`--topic telegram --label bug --limit 50` 会获取最多 50 个与“telegram”相关的未解决问题。

**错误处理：**
- 身份验证失败 → 告知用户运行 `gh auth login`
- 被限制了请求频率 → 通知用户并建议减少请求次数
- 仓库未找到 → 检查输入格式（`owner/repo`）
- 未找到问题 → 报告错误并退出（如果使用了 `--topic` 或 `--search`，建议扩大查询范围）
- 缺少某些字段 → 将空值或缺失的字段视为空内容

### 第三步：过滤已有的 PR 相关问题
**注意：** 如果用户指定了 `--include-with-prs`，则跳过此步骤，直接进入第四步处理所有获取到的问题。
在分析问题之前，请检查是否存在已经针对这些问题提交的 PR，以避免重复工作：
```bash
gh pr list --repo {owner/repo} --state open --json number,title,body,url
```

**检测相关问题**（可以使用以下任意一种或多种方法）：
**方法 1 — 明确的关键词**（高置信度）：
扫描 PR 的标题和正文（不区分大小写）：
- `fixes #N`、`fix #N`、`fixed #N`
- `closes #N`、`close #N`、`closed #N`
- `resolves #N`、`resolve #N`、`resolved #N`

**方法 2 — 问题引用**（中等置信度）：
- 文本中包含 “#N”
- `issue N`、`issue #N`、`related to #N`、`addresses #N`

**方法 3 — 标题相似性**（模糊匹配）：
对标题进行规范化处理（转换为小写，去除标点符号和常见词汇）。如果 70% 以上的词汇相同，则认为问题相关。

**方法 4 — 语义匹配**（用于不确定的情况）：
从问题描述中提取关键信息（错误名称、函数名称、组件名称），检查 PR 正文是否讨论了相同的内容。

**置信度标识：**
- 🔗 明确的链接（fixes/closes/resolves）：问题被 PR 解决或关闭
- 📎 被引用（#N 被提及）
- 🔍 标题相似（模糊匹配）
- 💡 语义匹配（组件相同）

将相关问题从分析结果中移除，并在最终报告中单独列出。

如果所有问题都已有 PR，需在报告中说明这一点后退出。

### 第四步：分析每个问题
对每个剩余的问题进行评分：

#### 难度（1-10 分）
基础得分：5 分。根据以下因素进行调整：
| 信号 | 调整分 |
|--------|-----------|
| 仅需要文档说明 | -3 |
| 已提出解决方案 | -2 |
| 有复现步骤 | -1 |
| 错误信息清晰 | -1 |
| 未知的根本原因 | +3 |
| 对架构有影响 | +3 |
| 存在竞态条件或并发问题 | +2 |
| 有安全风险 | +2 |
| 涉及多个系统 | +2 |

#### 重要性（1-10 分）
| 分数范围 | 等级 | 例子 |
|-------|-------|---------|
| 8-10 | 关键 | 会导致系统崩溃、数据丢失、安全漏洞或服务中断 |
| 6-7 | 高 | 功能故障、错误或性能问题 |
| 4-5 | 中等 | 需要改进的功能或特性请求 |
| 1-3 | 低 | 仅涉及外观调整、文档问题或拼写错误 |

#### 解决方案合理性（Tripping Scale，1-5 分）：
| 分数 | 标签 | 描述 |
|-------|-------|-------------|
| 1 | 完全合理 | 使用了经过验证的方法和标准模式 |
| 2 | 基于现有技术的创新 | 具有实际可行性且包含创新元素 |
| 3 | 尚在探索中 | 需要谨慎尝试 |
| 4 | 大胆且风险较高 | 非常规的解决方案 |
| 5 | 可能存在问题 | 可行性存疑 |

**警示信号（加分）：** 需从头开始重写、使用流行术语（如区块链、人工智能、机器学习）、实验性/不稳定的技术、破坏性的更改、自定义协议
**积极信号（减分）：** 使用标准方法、改动较小、向后兼容、基于现有库、文档齐全

#### 对架构的影响（1-5 分）：
在评分前请务必思考：“是否有更简单的方法？”

| 分数 | 标签 | 描述 |
|-------|-------|-------------|
| 1 | 小范围修改 | 仅涉及 1-2 个文件，无需引入新抽象概念 |
| 2 | 局部调整 | 仅在现有架构基础上进行小范围添加 |
| 3 | 中等程度的影响 | 引入新组件 |
| 4 | 影响较大 | 影响多个模块或引入新架构 |
| 5 | 影响深远 | 需要重构核心代码或改变开发范式 |

**警示信号（加分）：** 需要“重写整个系统”、“重构整个模块”、为现有功能引入新框架、涉及多个文件或破坏现有 API 的更改
**积极信号（减分）：** 只涉及单个文件的修改、使用现有工具、遵循现有模式、易于回退

#### 可操作性（1-5 分）：
问题是否可以通过提交 PR 来解决？
| 分数 | 标签 | 描述 |
|-------|-------|-------------|
| 1 | 无法解决 | 仅是疑问或讨论、重复问题、支持请求 |
| 2 | 需要进一步处理 | 缺少信息、范围不明确或需要澄清 |
| 3 | 需要调查 | 根本原因未知，需要先进行调试 |
| 4 | 可以立即处理 | 范围明确，可能需要一些设计决策 |
| 5 | 已准备好提交 PR | 解决方案明确，只需实现即可 |

**其他需要考虑的因素：**
- **阻碍因素**（减分）：疑问（如“我该如何实现？”）、讨论（如“有什么建议？”）、标签（如“重复问题”、“不会修复”）、缺少复现步骤
**提示信号（加分）：** 明确的操作指示（如“修复：”、“添加：”）、提出的解决方案、复现步骤、合适的标签、提及的具体文件

#### 综合得分计算公式
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
| 2 | 基于现有技术的创新 | 0.85 |
| 3 | 尚在探索中 | 0.70 |
| 4 | 大胆且风险较高 | 0.55 |
| 5 | 可能存在问题 | 0.40 |

**Architectural Impact 乘数：**
| 分数 | 标签 | 乘数 |
|-------|-------|------------|
| 1 | 小范围修改 | 1.00（无惩罚） |
| 2 | 局部调整 | 0.90 |
| 3 | 中等程度的影响 | 0.75 |
| 4 | 影响较大 | 0.50 |
| 5 | 影响深远 | 0.25 |

**Actionability 乘数：**
| 分数 | 标签 | 乘数 |
|-------|-------|------------|
| 5 | 已准备好提交 PR | 1.00（无惩罚） |
| 4 | 可以立即处理 | 0.90 |
| 3 | 需要调查 | 0.70 |
| 2 | 需要进一步处理 | 0.40 |
| 1 | 无法解决 | 0.10 |

### 第五步：分类问题
- **可以快速解决的问题**：ROI ≥ 1.5 且难度 ≤ 5 且解决方案合理性 ≤ 3 且可操作性 ≥ 4
- **关键问题**：问题类型为“bug”且重要性 ≥ 8
- **存在问题**：解决方案合理性 ≤ 4
- **设计过于复杂的问题**：对架构的影响 ≥ 4（可能存在更简单的解决方案）
- **无法解决的问题**：可操作性 ≤ 2

按照调整后的得分降序对问题进行排序。

### 第六步：展示结果
```
═══════════════════════════════════════════════════════════════
  ISSUE PRIORITIZATION REPORT
  Repository: {owner/repo}
  Filter: {topic/search/label or "latest"}
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

**可选参数：**
- `--json`：以原始 JSON 格式输出结果
- `--markdown` / `--md`：以 Markdown 表格格式输出结果
- `--quick-wins`：仅显示可以快速解决的问题
- `--level beginner|intermediate|advanced`：根据贡献者的技能水平筛选问题
- `--limit N`：指定要分析的问题数量（默认：30 个）
- `--topic <关键词>`：按关键词搜索问题（例如 `--topic telegram`、`--topic "agents telegram`）
- `--search <查询>`：使用自定义的 GitHub 搜索语句（例如 `--search "label:bug telegram in:title"`）
- `--label <name>`：按 GitHub 标签筛选问题（例如 `--label bug`）
- `--include-with-prs`：忽略 PR 相关问题，显示所有问题

## LLM 深度分析（可选）
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

在将问题正文发送给模型之前，将其截断至 2000 个字符以内。

**适用场景：**
- 问题复杂的仓库
- 需要更高准确性的情况
- 对不熟悉的仓库进行分析

**注意事项：** 分析速度较慢（每个问题约需 2-5 秒），但准确性更高。每个问题需要调用一次 API。

**集成方式：** 对每个问题使用 LLM 进行分析，解析 JSON 结果后将其合并到最终结果中（步骤 5：分类问题）。