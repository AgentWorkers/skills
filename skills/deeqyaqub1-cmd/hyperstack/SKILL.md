---
name: HyperStack — Memory Hub for AI Agents
description: "AI代理的内存管理系统：一种基于确定性、类型化、时序图的数据结构，具备信任传播机制、安全约束功能以及决策回放功能。用户可以查询“哪些模块被部署了？”——系统会给出精确的类型化答案。支持类似Git的分支操作。提供用于存储情景信息、语义数据和工作数据的API接口。具备决策回放功能，并能检测出决策中的“事后偏见”（即决策结果与实际情况的差异）。系统会根据代理的反馈自动优化边的权重（即数据之间的关联强度）。系统能够识别代理的身份并进行信任评分。用户可以“时间旅行”到过去的任何图状态（即数据结构状态）。该系统兼容Cursor、Claude Desktop、LangGraph等任何MCP客户端，并支持独立部署。无论使用规模多大，每次操作的成本均为0美元。"
user-invocable: true
homepage: https://cascadeai.dev/hyperstack
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env:
        - HYPERSTACK_API_KEY
        - HYPERSTACK_WORKSPACE
    primaryEnv: HYPERSTACK_API_KEY
---
# HyperStack — 人工智能代理的内存中心

## 功能概述

HyperStack 是为人工智能代理设计的内存中心。它采用类型化图谱存储数据，具有三种不同的内存管理机制：**情景记忆**（用于存储事件轨迹和代理行为）、**语义记忆**（用于存储永久性事实）以及**工作记忆**（用于存储临时性数据，基于时间戳管理）。每种内存类型都有各自的保留策略和数据衰减规则。

## 它解决的问题：
```
# DECISIONS.md (what everyone uses today)
- 2026-02-15: Use Clerk for auth
- 2026-02-16: Migration blocks deploy
"What breaks if auth changes?" → grep → manual → fragile
```

## 使用 HyperStack 的优势：
```
"What breaks if auth changes?"  → hs_impact use-clerk         → [auth-api, deploy-prod, billing-v2]
"What blocks deploy?"           → hs_blockers deploy-prod      → [migration-23]
"What's related to stripe?"     → hs_recommend use-stripe      → scored list
"Anything about auth?"          → hs_smart_search              → auto-routed
"Fork memory for experiment"    → hs_fork                      → branch workspace
"What changed in the branch?"   → hs_diff                      → added/changed/deleted
"Trust this agent?"             → hs_profile                   → trustScore: 0.84
"Why did we make this call?"    → mode=replay                  → decision timeline + hindsight flags
"Show episodic memory"          → memoryType=episodic          → decay-scored event traces
"Did this card help agents?"    → hs_feedback outcome=success  → utility score updated
```

- **类型化的数据结构**：确保数据的一致性和可查询性。
- **零 LLM 成本**：所有功能均无需依赖大型语言模型（LLM）。
- **跨平台兼容性**：支持 Cursor、Claude Desktop、LangGraph 等多种平台。

---

## 工具列表（共 15 个）

### hs_smart_search ✨ 推荐的入门工具
该工具能够自动选择最适合的数据检索方式，适用于不确定使用哪个工具的场景。
```
hs_smart_search({ query: "what depends on the auth system?" })
→ routed to: impact
→ [auth-api] API Service — via: triggers
→ [billing-v2] Billing v2 — via: depends-on

hs_smart_search({ query: "authentication setup" })
→ routed to: search
→ Found 3 memories

# Hint a starting slug for better routing
hs_smart_search({ query: "what breaks if this changes?", slug: "use-clerk" })
```

---

### hs_store
用于存储或更新数据卡片。支持卡片固定、设置过期时间（TTL）、记录卡片来源及代理身份信息。
```
# Basic store
hs_store({
  slug: "use-clerk",
  title: "Use Clerk for auth",
  body: "Better DX, lower cost, native Next.js support",
  type: "decision",
  links: "auth-api:triggers,alice:decided"
})

# With trust/provenance
hs_store({
  slug: "finding-clerk-pricing",
  title: "Clerk pricing confirmed",
  body: "Clerk free tier: 10k MAU. Verified on clerk.com/pricing",
  type: "decision",
  confidence: 0.95,
  truthStratum: "confirmed",
  verifiedBy: "tool:web_search"
})

# Pin — never pruned
hs_store({ slug: "core-arch", title: "Core Architecture", body: "...", pinned: true })

# Scratchpad with TTL — auto-deletes
hs_store({ slug: "scratch-001", title: "Working memory", body: "...",
  type: "scratchpad", ttl: "2026-02-21T10:00:00Z" })
```

**卡片字段（可选）：**
| 字段 | 类型 | 值 | 含义 |
|-------|------|--------|---------|
| `confidence` | float | 0.0–1.0 | 编写者的信心程度 |
| `truthStratum` | string | `draft` | `hypothesis` | `confirmed` | 认知状态 |
| `verifiedBy` | string | 生成卡片的来源 |
| `verifiedAt` | datetime | 服务器自动设置 | 卡片验证时间 |
| `sourceAgent` | string | 创建卡片后的不可更改信息 |

**支持的卡片类型：** `general`、`person`、`project`、`decision`、`preference`、`workflow`、`event`、`account`、`signal`、`scratchpad`

---

### hs_search
支持在图谱中进行混合语义搜索和关键词搜索。
```
hs_search({ query: "authentication setup" })
```

### hs_decide
用于记录决策过程及其完整来源信息。
```
hs_decide({
  slug: "use-clerk",
  title: "Use Clerk for auth",
  rationale: "Better DX, lower cost vs Auth0",
  affects: "auth-api,user-service",
  blocks: ""
})
```

### hs_commit
将代理的成功结果保存为永久性卡片，并通过 `decided` 关联关系自动链接。
```
hs_commit({
  taskSlug: "task-auth-refactor",
  outcome: "Successfully migrated all auth middleware to Clerk. Zero regressions.",
  title: "Auth Refactor Completed",
  keywords: ["clerk", "auth", "completed"]
})
→ { committed: true, slug: "commit-task-auth-refactor-...", relation: "decided" }
```

### hs_feedback ✨ 新功能（v1.0.23）
用于记录卡片对代理成功或失败的影响，促进图谱的自我优化。
```
# Cards that were in context when the task succeeded
hs_feedback({
  cardSlugs: ["use-clerk", "auth-api", "migration-23"],
  outcome: "success",
  taskId: "task-auth-refactor"
})
→ { feedback: true, outcome: "success", cardsAffected: 3, edgesUpdated: 5 }

# Cards that were in context when the task failed
hs_feedback({
  cardSlugs: ["wrong-approach"],
  outcome: "failure",
  taskId: "task-auth-refactor"
})
→ { feedback: true, outcome: "failure", cardsAffected: 1, edgesUpdated: 2 }
```

## 工作原理：
- 每张卡片的边都带有 `utilityScore` 分数；成功时分数增加，失败时分数减少。
- 随着时间的推移，有助于代理成功的卡片在查询中排名更高。
- 图谱会逐渐学习哪些信息真正有用。

**使用场景**：在每次代理任务结束时使用，无论任务结果是成功还是失败。

---

### hs_prune
自动删除 N 天未更新且未被其他卡片引用的过时卡片。执行前请先进行测试。
```
# Preview — safe, no deletions
hs_prune({ days: 30, dry: true })
→ { dryRun: true, wouldPrune: 3, skipped: 2, cards: [...], protected: [...] }

# Execute
hs_prune({ days: 30 })
→ { pruned: 3, skipped: 2 }
```

**安全保障**：
- 被链接的卡片不会被删除。
- 固定的卡片不会被删除。
- 基于 TTL 管理的卡片有特殊处理。

---

### hs_blockers
用于精确过滤特定类型的卡片。
```
hs_blockers({ slug: "deploy-prod" })
→ "1 blocker: [migration-23] Auth migration to Clerk"
```

### hs_graph
支持图谱遍历，支持时间旅行和基于效用值的排序。
```
hs_graph({ from: "auth-api", depth: 2 })
→ nodes: [auth-api, use-clerk, migration-23, alice]

# Time-travel — graph at any past moment
hs_graph({ from: "auth-api", depth: 2, at: "2026-02-15T03:00:00Z" })

# Utility-weighted — highest-value edges first
hs_graph({ from: "auth-api", depth: 2, weightBy: "utility" })

# Decision replay — what did agent know when this card was created?
hs_graph({ from: "use-clerk", mode: "replay" })
```

### hs_impact
用于反向遍历图谱，找出依赖于某张卡片的全部内容。
```
hs_impact({ slug: "use-clerk" })
→ "Impact of [use-clerk]: 3 cards depend on this
   [auth-api] API Service — via: triggers
   [billing-v2] Billing v2 — via: depends-on
   [deploy-prod] Production Deploy — via: blocks"

# Filter by relation
hs_impact({ slug: "use-clerk", relation: "depends-on" })
```

### hs_recommend
基于共引用次数推荐相关卡片。
```
hs_recommend({ slug: "use-stripe" })
→ "[billing-v2] Billing v2 — score: 4"
```

### hs_fork
用于创建安全的工作区分支，便于进行实验。
```
hs_fork({ branchName: "experiment-v2" })
→ {
    branchWorkspaceId: "clx...",
    branchName: "experiment-v2",
    cardsCopied: 24,
    forkedAt: "2026-02-21T..."
  }
```

**使用场景**：在进行风险操作、实验或测试新推理策略前使用。

---

### hs_diff
可清晰查看分支与父分支之间的变化。
```
hs_diff({ branchWorkspaceId: "clx..." })
→ {
    added:    [{ slug: "new-approach", title: "..." }],
    modified: [{ slug: "use-clerk", title: "..." }],
    removed:  []
  }
```

### hs_merge
将分支更改合并回父分支。
**合并策略**：`branch-wins` 或 `parent-wins`。

---

### hs_discard
彻底删除整个分支，包括所有卡片和工作区内容。
```
hs_discard({ branchWorkspaceId: "clx..." })
→ { discarded: true, branchWorkspaceId: "clx...", parentSlug: "default" }
```

### hs_identify
为代理生成唯一的 SHA256 哈希值，确保每次会话的识别一致性。
```
hs_identify({ agentSlug: "research-agent", displayName: "Research Agent" })
→ {
    registered: true,
    agentSlug: "research-agent",
    fingerprint: "sha256:a3f...",
    trustScore: 0.5
  }
```

**使用场景**：在每次代理会话开始时使用，以便追踪完整的数据来源。

### hs_profile
计算代理的信任分数。
**信任公式**：`(verifiedCards/totalCards) × 0.7 + min(cardCount/100, 1.0) × 0.3`

---

### hs_my_cards
列出该代理创建的所有卡片。
```
hs_my_cards()
→ "3 cards by agent researcher: [finding-clerk-pricing] [finding-auth0-limits]"
```

### hs_ingest
从原始文本中自动提取卡片信息，无需 LLM。
```
hs_ingest({ text: "We're using Next.js 14 and PostgreSQL. Alice decided to use Clerk for auth." })
→ "✅ Created 3 cards from 78 chars"
```

### hs_inbox
检查其他代理是否向该代理发送了卡片。
```
hs_inbox({})
→ "Inbox for cursor-mcp: 1 card(s)"
```

### hs_stats （高级功能）
提供令牌使用情况和内存使用统计信息。
```
hs_stats()
→ "Cards: 24 | Tokens stored: 246 | Saving: 94% — $2.07/mo"
```

## 内存中心的三层结构

HyperStack 提供三种不同类型的内存接口，它们都基于同一个类型化图谱：

### 情景记忆
- **卡片类型**：`general` 或 `event` — 用于存储事件轨迹和代理行为。
- **排序方式**：按创建时间降序。
- **保留策略**：30 天的软衰减机制：
  - 0–7 天：`decayScore` 为 1.0（最新）
  - 8–30 天：`decayScore` 逐渐降至 0.2
  >30 天：`decayScore` 为 0.1（视为过时，但不会被删除）。
- **代理优惠**：如果设置了 `sourceAgent`，数据保留时间减半。
- **额外字段**：`decayScore`、`daysSinceCreated`、`isStale`。
- **元数据**：`segment: "episodic"`、`retentionPolicy: "30-day-decay"`。

### 语义记忆
- **卡片类型**：`decision`、`person`、`project`、`workflow`、`preference`、`account` — 用于存储永久性事实。
- **排序方式**：按更新时间降序。
- **保留策略**：数据永久保存，无过期限制。
- **额外字段**：`confidence`、`truth_stratum`、`verified_by`、`verifiedAt`、`isVerified`。
- **元数据**：`segment: "semantic"`、`retentionPolicy: "permanent"`。

### 工作记忆
- **卡片类型**：`ttl` 不为空 — 用于存储临时性数据，基于 TTL 管理。
- **排序方式**：按更新时间降序。
- **保留策略**：卡片会自动过期。
- **代理优惠**：如果设置了 `sourceAgent`，TTL 时长延长 1.5 倍。
- **额外字段**：`ttl`、`expiresAt`、`isExpired`、`ttlExtended`。
- **元数据**：`segment: "working"`、`retentionPolicy: "ttl-based"`。

## 决策回放
能够精确还原代理做出决策时的知识状态，标记决策时不存在的卡片（有助于避免事后偏见）。

## 功用值加权边
每条边都带有 `utilityScore`，该分数会根据代理反馈动态更新。有助于代理成功的卡片排名更高，失败任务中的卡片则会逐渐被淘汰。

## Git 风格的内存分支管理
可以像使用 Git 仓库一样管理内存分支，安全地进行实验而不影响现有数据。

## 代理身份与信任机制
为代理注册唯一标识，以便追踪数据来源和计算信任分数。

## 十种图谱使用模式
每种模式都有特定的使用方式，可帮助用户解决不同问题。

## 安全与数据管理
**重要提示**：切勿在卡片中存储密码、API 密钥、令牌或个人身份信息。数据泄露时，卡片内容应保持安全。存储敏感信息前务必获得用户确认。

## 价格方案
提供多种定价方案，满足不同需求。

## 数据安全
**注意事项**：严禁在卡片中存储敏感信息。

## 文档更新记录
### v1.0.23 (2026年2月21日)
- 新增三种内存类型：`episodic`、`semantic`、`working`。
- 新增决策回放功能，便于审计代理的决策过程。
- 优化了路由逻辑和分支管理功能。
- 更新了 SDK 和文档结构。

## 下载与安装指南
- 安装指南：https://github.com/deeqyaqub1-cmd/hyperstack-core/blob/main/SELF_HOSTING.md

## 更多信息
- 获取免费 API 密钥：https://cascadeai.dev/hyperstack

希望这份文档能帮助您更好地了解 HyperStack 的功能和用法！如有任何疑问，请随时联系我们。