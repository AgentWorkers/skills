---
name: hyperstack
description: "用于多智能体协作的类型化图内存（Typed Graph Memory）。将 `GOALS.md` 和 `DECISIONS.md` 文件替换为可查询的卡片（queryable cards）和关系（relations）。通过提问“哪些任务与任务 X 相关联？”（What tasks are associated with task X?），可以获得精确的答案，而不仅仅是文本片段。"
user-invocable: true
homepage: https://cascadeai.dev/hyperstack
metadata:
  openclaw:
    emoji: "🃏"
    requires:
      env:
        - HYPERSTACK_API_KEY
    primaryEnv: HYPERSTACK_API_KEY
---
# HyperStack — 用于多智能体协作的类型化图谱内存系统

## 功能简介

HyperStack 通过构建一个类型化的知识图谱，替代了原有的 Markdown 文件（如 GOALS.md、DECISIONS.md、WORKING.md）作为智能体之间的协调工具。任何智能体都可以通过这个图谱来查询所需信息。

**旧版 OpenClaw 多智能体系统中的协调方式**：
```
# DECISIONS.md (append-only)
- 2026-02-15: Use Clerk for auth (coder-agent)
- 2026-02-16: Migration blocks production deploy (ops-agent)
```
“哪些模块需要部署？” → `grep -r "blocks.*deploy" *.md` → 需要手动搜索，且效率低下

**HyperStack 新系统中的协调方式**：
```
"What blocks deploy?" → hs_blockers deploy-prod → [migration-23] Auth migration to Clerk
```

- 使用类型化的数据结构，提供精确的查询结果；
- 完全不需要使用大型语言模型（LLM）。

## 主要工具

### hs_search
在共享的知识图谱中进行搜索，结合语义分析和关键词匹配功能。
```
hs_search({ query: "authentication setup" })
```

### hs_store
将信息存储到图谱中，并自动添加智能体的标识。
```
hs_store({
  slug: "use-clerk",
  title: "Use Clerk for auth",
  body: "Better DX, lower cost, native Next.js support",
  type: "decision",
  links: "auth-api:triggers,alice:decided"
})
```

### hs_decide
记录决策内容，包括决策者、受影响对象以及决策所阻塞的内容。
```
hs_decide({
  slug: "use-clerk",
  title: "Use Clerk for auth",
  rationale: "Better DX, lower cost vs Auth0",
  affects: "auth-api,user-service",
  blocks: ""
})
```

### hs_blockers
检查某个任务或信息会被哪些模块阻塞，返回精确的类型化结果，而非模糊搜索结果。
```
hs_blockers({ slug: "deploy-prod" })
→ "1 blocker: [migration-23] Auth migration to Clerk"
```

### hs_graph
从任意节点开始遍历知识图谱，查看节点之间的关联关系、所有权信息及依赖关系。支持时间回溯功能：通过指定时间戳，可以还原图谱在特定时间点的状态。
```
hs_graph({ from: "auth-api", depth: 2 })
→ nodes: [auth-api, use-clerk, migration-23, alice]
→ edges: [auth-api→triggers→use-clerk, migration-23→blocks→deploy-prod]

# Time-travel: see the graph at a specific moment
hs_graph({ from: "auth-api", depth: 2, at: "2026-02-15T03:00:00Z" })
```

### hs_my_cards
列出当前智能体创建的所有信息卡片。
```
hs_my_cards()
→ "3 cards by agent researcher: [finding-clerk-pricing] [finding-auth0-limits]"
```

### hs_ingest
从原始文本中自动提取信息。用户只需粘贴对话记录、会议笔记或项目描述，HyperStack 便会自动提取其中涉及的人员、决策内容、偏好设置及技术栈信息。整个过程不消耗任何 LLM 资源（基于正则表达式处理）。
```
hs_ingest({ text: "We're using Next.js 14 and PostgreSQL. Alice decided to use Clerk for auth." })
→ "✅ Created 3 cards from 78 chars:
  [tech-nextjs] Next.js 14 (preference)
  [tech-postgresql] PostgreSQL (preference)
  [decision-use-clerk] Use Clerk for auth (decision)"
```

### hs_inbox
接收其他智能体发送给当前智能体的信息卡片。通过这种共享机制实现多智能体间的协作：智能体 A 可以存储信息，智能体 B 通过 `hs_inbox` 功能立即获取这些信息。
```
hs_inbox({})
→ "Inbox for cursor-mcp: 1 card(s)
  [review-needed] Review auth migration (signal) from=claude-desktop-mcp"
```

### hs_webhook (Team+)
允许智能体注册 Webhook，当有信息卡片指向该智能体时，系统会实时发送通知。例如：智能体 A 存储阻塞信息后，智能体 B 会自动收到通知。
```
hs_webhook({
  url: "https://your-server.com/webhook",
  events: "card.created,signal.received"
})
```

### hs_stats ✨ 新功能（v1.0.15）
提供工作空间的令牌使用情况统计和内存使用情况报告。显示使用 HyperStack 而非手动加载所有数据相比能节省多少资源。此功能需订阅 Pro 计划才能使用。
```
hs_stats()
→ "HyperStack Stats for workspace: default
   Cards: 24 | Tokens stored: 246 | Stale: 0
   Without HyperStack: 246 tokens/msg ($11.07/mo)
   With HyperStack:    200 tokens/msg ($9.00/mo)
   Saving: 15% — $2.07/mo
   
   Card breakdown:
   decisions: 8 | preferences: 6 | general: 10"
```

### hs_agent_tokens (Team+) ✨ 新功能（v1.0.15）
允许为每个智能体创建、列出和撤销受限的访问令牌。不再需要所有智能体共享一个统一的 API 密钥，而是根据需求分配相应的权限。此功能需订阅 Team 计划。

## 多智能体系统设置

每个智能体都有自己的唯一标识。系统会自动为卡片添加创建者的标签，方便追踪信息来源。

**推荐角色**：
- **协调者**：负责任务分配、监控阻塞情况（使用 `hs_blockers`、`hs_graph`、`hs_decide` 工具）
- **研究员**：负责信息收集与存储（使用 `hs_search`、`hs_store`、`hs_ingest` 工具）
- **实施者**：负责执行任务并记录技术决策（使用 `hs_store`、`hs_decide`、`hs_blockers` 工具）

## 设置方式

### 选项 A：VPS 或自托管环境（推荐）
在本地机器或 VPS 上运行 SDK，通过浏览器进行身份验证，无需手动管理 API 密钥。
```bash
npm i hyperstack-core
npx hyperstack-core login          # opens browser, approve device, done
npx hyperstack-core init openclaw-multiagent
```
凭据保存在 `~/.hyperstack/credentials.json` 文件中，所有命令和工具均可自动完成身份验证。

### 选项 B：通过 OpenClaw 环境变量配置
1. 获取免费 API 密钥：https://cascadeai.dev/hyperstack
2. 在 OpenClaw 环境变量中设置 `HYPERSTACK_API_KEY=hs_your_key`
3. 相关工具可立即使用

### 选项 C：程序化方式（Node.js 适配器）
```js
import { createOpenClawAdapter } from "hyperstack-core/adapters/openclaw";
const adapter = createOpenClawAdapter({ agentId: "builder" });
await adapter.onSessionStart({ agentName: "Builder", agentRole: "Implementation" });
// adapter.tools: hs_search, hs_store, hs_decide, hs_blockers, hs_graph, hs_my_cards, hs_ingest
await adapter.onSessionEnd({ summary: "Completed auth migration" });
```

## 工作原理

SDK 在用户的机器或 VPS 上运行。所有 `hs_store`、`hs_search`、`hs_blockers` 的请求都会发送到 HyperStack 的 API。用户拥有自己的智能体账户，而图谱本身由 HyperStack 托管。

**免费版本**：支持 10 张卡片，提供关键词搜索功能。
**Pro 计划（每月 29 美元）**：支持 100 张卡片，支持图谱遍历、语义搜索、时间回溯功能以及令牌使用情况统计。
**Team 计划（每月 59 美元）**：支持 500 张卡片，提供 5 个团队 API 密钥、Webhook 功能以及无限数量的工作空间，同时支持为每个智能体创建受限的访问令牌。

## 使用场景

- **会议开始时**：使用 `hs_search` 查找相关背景信息
- **新项目/员工入职时**：使用 `hs_ingest` 从现有文档中自动填充信息
- **做出决策后**：使用 `hs_decide` 记录决策内容及理由
- **任务被阻塞时**：使用 `hs_store` 记录阻塞关系
- **开始工作前**：使用 `hs_blockers` 检查任务依赖关系
- **调试错误决策时**：使用 `hs_graph` 查看决策时的背景信息
- **智能体间传递信息时**：使用 `hs_store` 设置 `targetAgent` 参数，其他智能体可通过 `hs_inbox` 接收信息
- **评估系统效率时**：使用 `hs_stats` 查看令牌使用情况和内存使用状况
- **限制智能体权限时**：使用 `hs_agent_tokens` 为每个智能体分配必要的访问权限

## 数据安全

**重要提示**：
- 绝不存储密码、API 密钥、令牌、个人身份信息（PII）或任何敏感数据。即使发生数据泄露，这些信息也不会被泄露。
- 在存储任何数据之前，必须先获得用户的明确授权。

## 更新日志

### v1.0.15（2026年2月17日）

#### ✨ `hs_stats` — 令牌使用情况与内存管理（Pro+计划）
- 新增功能：用户可以查看 HyperStack 节省了多少资源以及内存使用状况。
  - 提供详细的报告，包括：
    - 存储的卡片数量及内存中使用的令牌总数
    - 使用 HyperStack 的选择性数据检索方式与手动加载所有数据相比的节省成本
    - 每月节省的费用（基于每天 100 条消息、按 GPT-4 计费标准计算）
    - 卡片类型统计（如决策、偏好设置、项目等）
    - 过去 7 天的活动记录（读取、写入操作、令牌使用情况）
    - 30 天以上未更新的卡片列表（可能需要重新审核）

**使用场景**：智能体可以在会议结束时调用 `hs_stats` 以评估系统效率，这也是从免费版本升级到 Pro 计划的合理理由。

#### ✨ `hs_agent_tokens` — 为每个智能体分配受限权限（Team+计划）
- 新功能：每个智能体都可以拥有自己的访问令牌：
  - `canRead`：限制智能体可以读取的卡片类型
  - `canWrite`：限制智能体可以写入的卡片类型
  - `allowedStacks`：限制智能体可以访问的技术栈
  - `expiresIn`：设置令牌的有效期限（秒级）
  - 令牌前缀区分：`hsa_` 表示智能体专属令牌，`hs_` 表示全局通用令牌

#### v1.0.14（2026年2月17日）

#### ✨ `hs_ingest` — 从原始文本中自动提取信息（无需 LLM 资源）
- 在 v1.0.14 之前，需要手动调用 `hs_store` 为每条信息创建卡片，效率较低。
- 新版本支持从原始文本（如对话记录、会议笔记等）中自动提取结构化卡片，无需使用 LLM 或访问 OpenAI API。
  - 支持提取以下类型的信息：
    - **决策内容**（如 “我们决定……”）
    - **偏好设置**（如 “我们总是使用……”）
    - **人员信息**（如 “Alice 是负责人”）
    - **项目信息**（如 “我们正在开发……”）
    - **工作流程**（如 “先做 X，再做 Y”）
    - **技术栈信息**（自动识别 40 多种框架和数据库，并汇总到一张卡片中）

**使用场景**：用户只需粘贴项目文档或会议记录，系统即可快速生成完整的信息图谱。

#### ✨ `hs_inbox` — 智能体定向接收信息卡片
- 在 v1.0.14 之前，智能体只能手动存储带有 `targetAgent` 字段的卡片，无法自动接收其他智能体发送的信息。
- 新版本支持查询指向当前智能体的卡片，可根据时间戳筛选信息，确保智能体仅看到最近收到的消息。

#### ✨ `hs_webhook` / `hs_webhooks` — 实时通知功能（Team+计划）
- 团队计划用户可以注册 Webhook，当有信息卡片指向他们时立即收到通知。
- 支持事件过滤（如 `card.created`、`card.updated`、`signal.received` 等）。
- 使用 HMAC 签名机制进行验证。

#### 🔧 CLI 登录的 OAuth 设备认证流程
- `npx hyperstack-core login` 现在支持 RFC 8628 规范的 OAuth 设备认证流程。用户只需在浏览器中批准授权码，系统会自动保存凭据，无需手动复制 API 密钥。

### v1.0.13 及更早版本 — 核心功能

HyperStack 的基础功能包括：
- **`hs_search`：提供混合关键词搜索和语义搜索功能。关键词搜索免费，语义搜索（基于 pgvector 的向量相似度计算）需订阅 Pro 计划。
- **`hs_store`：支持创建或更新卡片，并自动添加元数据（如卡片标题、内容、类型、关键词、关联关系等）。
- **`hs_decide`：专门用于记录决策内容，包括决策者、受影响对象及阻塞关系。
- **`hs_blockers`：根据给定的卡片 ID，在图谱中查找阻塞该卡片的模块。
- **`hs_graph`：支持从任意节点遍历图谱，支持配置遍历深度（1-3 层）和时间回溯功能。
- **`hs_my_cards`：列出当前智能体创建的所有卡片，便于智能体自查自己的信息使用情况。