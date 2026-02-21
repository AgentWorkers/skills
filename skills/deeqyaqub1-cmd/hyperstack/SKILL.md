---
name: HyperStack — Typed Graph Memory for AI Agents
description: "专为AI代理设计的持久化类型化知识图谱存储系统：  
当用户询问“哪些模块被部署了？”时，系统会提供精确的类型化答案（而非模糊的相似性判断）。  
采用类似Git的存储管理机制：支持分支创建、实验操作、差异对比、合并或删除功能。  
系统具备代理身份识别及信任评分机制。  
支持“时间旅行”功能，可回溯到知识图谱的任意历史状态。  
每张卡片都记录了其来源信息（包括置信度、验证层级及验证者信息）。  
该系统兼容Cursor、Claude Desktop、LangGraph等所有MCP客户端，并支持独立部署（无需额外成本）。  
每次操作的费用仅为0美元。"
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
# HyperStack — 专为AI代理设计的类型化图谱内存系统

## 功能概述

HyperStack为AI代理提供持久化的内存存储，以类型化知识图谱的形式存在。知识以卡片的形式存储，并明确标注了它们之间的关系。查询时能够获得精确的答案，而非模糊的相似性结果。系统支持类似Git的分支管理功能，能够追踪每张卡片的信息来源，并为代理分配信任分数。

**解决的问题：**
```
# DECISIONS.md (what everyone uses today)
- 2026-02-15: Use Clerk for auth
- 2026-02-16: Migration blocks deploy
"What breaks if auth changes?" → grep → manual → fragile
```

**使用HyperStack后可以获得：**
```
"What breaks if auth changes?"  → hs_impact use-clerk        → [auth-api, deploy-prod, billing-v2]
"What blocks deploy?"           → hs_blockers deploy-prod     → [migration-23]
"What's related to stripe?"     → hs_recommend use-stripe     → scored list
"Anything about auth?"          → hs_smart_search             → auto-routed
"Fork memory for experiment"    → hs_fork                     → branch workspace
"What changed in the branch?"   → hs_diff                     → added/changed/deleted
"Trust this agent?"             → hs_profile                  → trustScore: 0.84
```

- 类型化的数据关系
- 精确的查询结果
- 无需使用大型语言模型（LLM）
- 支持在Cursor、Claude Desktop、LangGraph等任何MCP客户端上同时使用

---

## 工具（共14个）

### hs_smart_search ✨ 推荐的入门工具
该工具能够自动选择最适合的检索方式，适用于不确定应使用哪个工具的情况。
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
用于存储或更新卡片信息。支持卡片固定、设置卡片的有效期限（TTL）、记录信息来源以及为卡片添加代理标识。
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

**信任/信息来源字段（均为可选）：**
| 字段 | 类型 | 值 | 含义 |
|-------|------|--------|---------|
| `confidence` | float | 0.0–1.0 | 编写者的信心程度 |
| `truthStratum` | string | `draft` \| `hypothesis` \| `confirmed` | 认知状态 |
| `verifiedBy` | string | 任何字符串 | 确认信息来源的人/事物 |
| `verifiedAt` | datetime | — | 服务器自动设置 |
| `sourceAgent` | string | — | 创建后不可更改 |

**有效的卡片类型：`general`、`person`、`project`、`decision`、`preference`、`workflow`、`event`、`account`、`signal`、`scratchpad`

---

### hs_search
支持在图谱中进行混合语义搜索和关键词搜索。
```
hs_search({ query: "authentication setup" })
```

---

### hs_decide
用于记录带有完整信息来源的决策结果。
```
hs_decide({
  slug: "use-clerk",
  title: "Use Clerk for auth",
  rationale: "Better DX, lower cost vs Auth0",
  affects: "auth-api,user-service",
  blocks: ""
})
```

---

### hs_commit
将成功的决策结果作为永久性卡片保存，并通过`decided`关系自动关联起来。
```
hs_commit({
  taskSlug: "task-auth-refactor",
  outcome: "Successfully migrated all auth middleware to Clerk. Zero regressions.",
  title: "Auth Refactor Completed",
  keywords: ["clerk", "auth", "completed"]
})
→ { committed: true, slug: "commit-task-auth-refactor-...", relation: "decided" }
```

---

### hs_prune
自动删除N天内未更新且未被其他卡片引用的过时卡片。执行前会进行模拟测试。
```
# Preview — safe, no deletions
hs_prune({ days: 30, dry: true })
→ { dryRun: true, wouldPrune: 3, skipped: 2, cards: [...], protected: [...] }

# Execute
hs_prune({ days: 30 })
→ { pruned: 3, skipped: 2 }
```

**安全保障：**
- 被关联的卡片永远不会被删除
- 固定的卡片永远不会被删除
- 设置有效期限的卡片会单独管理

---

### hs_blockers
用于对卡片添加类型化的限制。
```
hs_blockers({ slug: "deploy-prod" })
→ "1 blocker: [migration-23] Auth migration to Clerk"
```

---

### hs_graph
支持图谱的遍历，甚至可以“时间旅行”（查看过去的图谱状态）。
```
hs_graph({ from: "auth-api", depth: 2 })
→ nodes: [auth-api, use-clerk, migration-23, alice]

# Time-travel — graph at any past moment
hs_graph({ from: "auth-api", depth: 2, at: "2026-02-15T03:00:00Z" })
```

---

### hs_impact
支持反向遍历图谱，找出依赖于某张卡片的全部内容。
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
基于共引用量对卡片进行相关性评分，即使没有直接链接也能找到相关卡片。
```
hs_recommend({ slug: "use-stripe" })
→ "[billing-v2] Billing v2 — score: 4"
```

### hs_fork ✨ 新功能（v1.1.0）
可以将工作空间分叉到一个新的分支中进行安全实验，所有卡片都会被复制，父分支保持不变。
```
hs_fork({ branchName: "experiment-v2" })
→ {
    branchWorkspaceId: "clx...",
    branchName: "experiment-v2",
    cardsCopied: 24,
    forkedAt: "2026-02-20T..."
  }
```

**使用场景：**
- 在进行风险较高的更改之前
- 进行实验时
- 测试新的代理推理策略时

---

### hs_diff ✨ 新功能（v1.1.0）
可以精确查看分支与父分支之间的变化内容。采用SQL驱动的方式，结果具有确定性，而非模糊匹配。
```
hs_diff({ branchWorkspaceId: "clx..." })
→ {
    added:   [{ slug: "new-approach", title: "..." }],
    changed: [{ slug: "use-clerk", title: "..." }],
    deleted: []
  }
```

### hs_merge ✨ 新功能（v1.1.0）
可以将分支的更改合并回父分支。提供两种合并策略：“ours”（分支的更改保留）或“theirs”（父分支的更改保留）。
```
# Branch wins — apply all branch changes to parent
hs_merge({ branchWorkspaceId: "clx...", strategy: "ours" })
→ { merged: 24, skipped: 0, strategy: "ours" }

# Parent wins — only copy cards that don't exist in parent
hs_merge({ branchWorkspaceId: "clx...", strategy: "theirs" })
→ { merged: 3, skipped: 21, strategy: "theirs" }
```

### hs_discard ✨ 新功能（v1.1.0）
可以完全删除一个分支，同时删除该分支下的所有卡片，但不会影响父分支。
```
hs_discard({ branchWorkspaceId: "clx..." })
→ { deleted: true, branchWorkspaceId: "clx..." }
```

### hs_identify ✨ 新功能（v1.1.0）
使用SHA256指纹为代理注册唯一标识。该操作是幂等的，每次会话都可以安全调用。
```
hs_identify({ agentSlug: "research-agent", displayName: "Research Agent" })
→ {
    agentSlug: "research-agent",
    fingerprint: "sha256:a3f...",
    isNew: true
  }
```

**使用场景：**
- 在每次代理会话开始时，用于记录完整的操作信息来源

---

### hs_profile ✨ 新功能（v1.1.0）
用于计算代理的信任分数。分数基于已验证卡片的数量和代理的活动频率计算。
```
hs_profile({ agentSlug: "research-agent" })
→ {
    agentSlug: "research-agent",
    trustScore: 0.84,
    verifiedCards: 42,
    cardCount: 50,
    registeredAt: "...",
    lastActiveAt: "..."
  }
```

**信任分数计算公式：**
`(verifiedCards / totalCards) × 0.7 + min(cardCount / 100, 1.0) × 0.3`

---

### hs_my_cards
列出该代理创建的所有卡片。
```
hs_my_cards()
→ "3 cards by agent researcher: [finding-clerk-pricing] [finding-auth0-limits]"
```

### hs_ingest
可以从原始文本中自动提取卡片信息。无需使用大型语言模型。
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
提供令牌使用情况和内存使用情况的统计信息。
```
hs_stats()
→ "Cards: 24 | Tokens stored: 246 | Saving: 94% — $2.07/mo"
```

## 类Git的内存分支管理

可以像管理Git仓库一样管理内存工作空间，安全地进行实验而不会破坏现有数据。
```
# 1. Fork before an experiment
hs_fork({ branchName: "try-new-routing" })

# 2. Make changes in the branch (all hs_store calls go to branch)
hs_store({ slug: "new-approach", title: "...", ... })

# 3. See what changed
hs_diff({ branchWorkspaceId: "clx..." })

# 4a. Merge if it worked
hs_merge({ branchWorkspaceId: "clx...", strategy: "ours" })

# 4b. Or discard if it didn't
hs_discard({ branchWorkspaceId: "clx..." })
```

**注意：** 分支管理功能需要Pro计划或更高级别的订阅才能使用。

---

## 代理身份与信任机制

为代理注册唯一标识，以便追踪其操作信息来源并计算信任分数。
```
# Register at session start
hs_identify({ agentSlug: "research-agent" })

# All subsequent hs_store calls auto-stamp agentIdentityId
hs_store({ slug: "finding-001", ... })  # → auto-linked to research-agent

# Check trust score
hs_profile({ agentSlug: "research-agent" })
→ trustScore: 0.84
```

**推荐做法：** 设置`HYPERSTACK_AGENT_SLUG`环境变量以实现无需配置的自动识别。

---

## 八种图谱查询模式

| 模式 | 工具 | 可查询的内容 |
|------|------|-------------------|
| Smart | `hs_smart_search` | 可以询问任何问题，系统会自动选择合适的检索方式 |
| Forward | `hs_graph` | 这张卡片与其他卡片有何关联？ |
| Impact | `hs_impact` | 什么依赖于这张卡片？哪些功能会受到影响？ |
| Recommend | `hs_recommend` | 有哪些内容与当前查询相关？ |
| Time-travel | `hs_graph` 结合 `at=` 参数 | 过去图谱的状态是什么样的？ |
| Prune | `hs_prune` | 哪些过时的卡片可以安全删除？ |
| Branch diff | `hs_diff` | 这个分支发生了哪些变化？ |
| Trust | `hs_profile` | 这个代理的信任度如何？ |

---

## 卡片的信息来源

每张卡片都包含认知元数据。
```
# Researcher stores a finding with low confidence
hs_store({ slug: "finding-latency", body: "p99 latency ~200ms under load",
  confidence: 0.6, truthStratum: "hypothesis" })

# After human verification
hs_store({ slug: "finding-latency", confidence: 0.95,
  truthStratum: "confirmed", verifiedBy: "human:deeq" })
# → verifiedAt auto-set server-side
```

**重要规则：**
- `confidence`字段表示编写者的信心程度，仅用于展示，不可作为硬性判断依据
- `confirmed`表示在该工作空间内被认为是正确的结果，但不一定是客观事实
- `sourceAgent`字段在卡片创建后不可更改
- `verifiedAt`字段由服务器设置，客户端无法修改

---

## 完整的内存生命周期管理

| 内存类型 | 使用工具 | 行为 |
|-------------|------|-----------|
| 长期保存的事实 | `hs_store` | 永久保存，可搜索，并与图谱关联 |
| 工作中的记忆 | `hs_store`（设置`ttl=`且`type=scratchpad`） | 到期后自动删除 |
| 结果/学习内容 | `hs_commit` | 作为决策结果保存 |
| 过时内容的清理 | `hs_prune` | 删除未使用的卡片，保持图谱完整性 |
| 受保护的事实 | `hs_store`（设置`pinned=true`） | 永远不会被删除 |
| 分支实验 | `hs_fork` → `hs_diff` → `hs_merge` / `hs_discard` | 安全地进行实验 |

---

## 多代理协作

每个代理都有唯一的ID。卡片会自动标记以便追踪其来源。

**推荐的角色分配：**
- **协调者**：`hs_blockers`、`hs_impact`、`hs_graph`、`hs_decide`、`hs_fork`、`hs_merge`
- **研究员**：`hs_search`、`hs_recommend`、`hs_store`、`hs_ingest`、`hs_identify`
- **构建者**：`hs_store`、`hs_decide`、`hs_commit`、`hs_blockers`、`hs_fork`
- **内存管理代理**：`hs_prune`、`hs_stats`、`hs_smart_search`、`hs_diff`、`hs_discard`

---

## 各工具的使用场景

| 使用场景 | 所需工具 |
|--------|------|
| 会话开始 | `hs_identify` → `hs_search` → `hs_recommend` |
| 不确定使用哪种模式 | `hs_smart_search` | 系统会自动选择合适的检索方式 |
| 新项目/新成员入职 | `hs_ingest` | 自动填充相关信息 |
| 做出决策 | `hs_decide` 并附上决策理由和链接 |
| 任务完成 | `hs_commit` | 保存决策结果 |
| 任务受阻 | `hs_store` 并添加相关限制 |
- 在开始工作前 | `hs_blockers` | 检查任务依赖关系 |
- 在进行风险实验前 | `hs_fork` → 在分支中实验 → `hs_merge` 或 `hs_discard` |
- 发现新信息 | `hs_recommend` | 查找相关内容 |
- 管理临时记忆 | `hs_store`（设置`ttl=`且`type=scratchpad`） |
- 定期清理 | `hs_prune`（启用`dry=true`） → 检查后再执行 |
- 调试错误决策 | `hs_graph` 并查看操作时间 |
- 跨代理通信 | `hs_store`（指定目标代理） → `hs_inbox` |
- 检查效率 | `hs_stats` |
- 检查代理信任度 | `hs_profile` |

---

## 设置说明

### MCP（Claude Desktop / Cursor / VS Code / Windsurf）

### Python SDK

### LangGraph

### 自主托管

**配置说明：**
在SDK配置中设置`HYPERSTACK_BASE_URL=http://localhost:3000`。

**可选的环境变量：**
| 变量 | 默认值 | 说明 |
|---|---|---|
| `OPENAI_API_KEY` | — | 启用OpenAI嵌入功能 |
| `EMBEDDING_BASE_URL` | `https://api.openai.com` | 自定义端点（例如Ollama） |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | 嵌入模型名称 |
| `EMBEDDING_API_KEY` | 使用`OPENAI_API_KEY`作为默认值 | 自定义端点的API密钥 |

**完整指南：** https://github.com/deeqyaqub1-cmd/hyperstack-core/blob/main/SELF_HOSTING.md

---

## 数据安全

**注意事项：**
- 绝不要在卡片中存储密码、API密钥、令牌、个人身份信息（PII）或其他敏感数据。即使发生数据泄露，卡片内容也应保持安全。
- 在存储敏感信息之前，必须先获得用户的明确许可。

---

## 定价方案

| 订阅计划 | 价格 | 可使用的卡片数量 | 提供的功能 |
|------|-------|-------|---------|
| 免费 | $0 | 10张卡片 | 仅支持搜索 |
| Pro | $29/月 | 100张卡片 | 支持所有8种查询模式、分支管理及代理身份识别 |
| Team | $59/月 | 500张卡片 | 支持所有查询模式、Webhook及代理令牌 |
| Business | $149/月 | 2000张卡片 | 支持所有查询模式、单点登录（SSO）及20个用户 |
| 自主托管 | $0 | 无限卡片数量 | 全部功能可用 |

**免费获取API密钥：** https://cascadeai.dev/hyperstack

---

## 更新日志

### v1.1.0（2026年2月20日）

#### 新功能：
- **Git风格的内存分支管理**：新增4个工具
  - `hs_fork`：将工作空间分叉到新分支，所有卡片都被复制，父分支保持不变
  - `hs_diff`：通过SQL查询分支与父分支之间的变化（新增/修改/删除）
  - `hs_merge`：将分支更改合并回父分支（选择“ours”或“theirs”策略）
  - `hs_discard`：完全删除分支
  - 分支管理功能需要Pro计划或更高级别的订阅
  - 分支批量处理时每次最多处理25个卡片，以符合无服务器架构的限制
  - 差异对比使用SQL查询，结果具有确定性，数据存储在Postgres数据库中

#### 新功能：
- **代理身份与信任评分**：新增2个工具
  - `hs_identify`：使用SHA256指纹为代理注册唯一标识
  - `hs_profile`：计算代理的信任分数：`(verifiedCards / totalCards) × 0.7 + min(cardCount / 100, 1.0) × 0.3`
  - 设置`HYPERSTACK_AGENT_SLUG`环境变量可实现无需配置的自动识别
  - 所有使用`hs_store`的调用都会自动添加`agentIdentityId`

#### 自主托管说明：
- Docker镜像：`ghcr.io/deeqyaqub1-cmd/hyperstack:latest`
- 在所有SDK中设置`HYPERSTACK_BASE_URL`环境变量，指向自己的Postgres服务器
- 完整的自主托管指南：https://github.com/deeqyaqub1-cmd/hyperstack-core/blob/main/SELF_HOSTING.md

#### SDK更新：
- `hyperstack-mcp` → v1.9.0（新增14个工具）
- `hyperstack-py` → v1.4.0（新增`hs_fork`、`hs_diff`、`hs_merge`、`hs_discard`、`hs_identify`功能）
- `hyperstack-langgraph` → v1.4.0（功能与`hyperstack-py`相同）

### v1.0.20（2026年2月20日）
- 所有卡片都添加了`confidence`、`truthStratum`、`verifiedBy`、`verifiedAt`、`sourceAgent`字段
- 安全性改进：移除了`hs_webhook`和`hs_agent_tokens`功能（仅限管理员使用）
- 后端性能优化：改进了数据清理逻辑

### v1.0.19（2026年2月20日）
- `hs_prune`功能增加了模拟测试机制
- `hs_commit`功能支持基于反馈的决策更新
- 新增`pinned`字段，防止卡片被永久删除
- `scratchpad`卡片类型支持设置有效期限

### v1.0.18（2026年2月20日）
- `hs_smart_search`功能加入了自动选择最佳检索方式的逻辑

### v1.0.16（2026年2月19日）
- `hs_impact`功能支持反向图谱遍历
- `hs_recommend`功能加入了基于共引用量的语义评分

### v1.0.13–v1.0.15（早期版本）
- 基础功能更新：`hs_search`、`hs_store`、`hs_decide`、`hs_blockers`、`hs_graph`、`hs_my_cards`、`hs_ingest`、`hs_inbox`、`hs_stats`