---
name: hyperstack
description: "**多智能体协作的类型化图内存系统**  
该系统替代了原有的 `GOALS.md` 和 `DECISIONS.md` 文件，采用可查询的卡片和关联关系来管理智能体的行为和决策过程：  
- 可以询问“任务 X 由哪些部分组成？”并获得精确的答案；  
- 可以询问“某个卡片依赖于什么？”并追踪其全部影响；  
- 可以询问“与这个卡片相关的内容有哪些？”并获得评分后的推荐结果；  
- 仅需用简单的英语提问，系统会自动选择合适的查询模式；  
- 可以将重要的卡片固定（“钉住”）以防止被遗忘；  
- 系统会自动清理过时的数据；  
- 智能体的决策结果会被记录为正式的决策内容。  
**整个系统完全不需要任何大型语言模型（LLM）的成本支持。**"
user-invocable: true
homepage: https://cascadeai.dev/hyperstack
metadata:
  openclaw:
    emoji: "🃏"
    requires:
      env:
        - HYPERSTACK_API_KEY
        - HYPERSTACK_WORKSPACE
    primaryEnv: HYPERSTACK_API_KEY
---
# HyperStack — 用于多智能体协作的类型化图谱内存系统

## 功能概述

HyperStack 替代了原有的 markdown 文件协调机制（GOALS.md、DECISIONS.md、WORKING.md），采用了一种类型化的知识图谱，所有智能体都可以对其进行查询。系统提供了五种图谱遍历模式：正向遍历、影响分析、推荐、智能搜索和时间旅行，能够满足智能体提出的所有关联性问题。通过内存修剪机制，系统会自动删除过时的信息；TTL（Time-To-Live）功能用于管理临时性工作记忆；而反馈提交机制则将成功的决策结果永久化。

**旧系统（当前的多智能体协作方式）：**
```
# DECISIONS.md (append-only)
- 2026-02-15: Use Clerk for auth (coder-agent)
- 2026-02-16: Migration blocks production deploy (ops-agent)
```
“如果更改认证方式会引发什么问题？” → 需要逐一检查所有文件 → 这种方式既繁琐又容易出错，且效率低下。

**HyperStack 新系统：**
```
"What breaks if we change auth?"    → hs_impact use-clerk → [auth-api, deploy-prod, billing-v2]
"What blocks deploy?"               → hs_blockers deploy-prod → [migration-23]
"What's related to stripe?"         → hs_recommend use-stripe → scored list of related cards
"What depends on the API?"          → hs_smart_search "what depends on the API?" → auto-routed
"Clean up old memory"               → hs_prune dry=true → preview, then prune
"Agent completed a task"            → hs_commit → outcome stored as decided card
```

- **类型化的关联关系**：确保查询结果的准确性。
- **零 LLM 成本**：完全不依赖大型语言模型（LLM）。

---

## 工具介绍

### hs_search
用于搜索共享的知识图谱，结合了语义分析和关键词匹配功能。
```
hs_search({ query: "authentication setup" })
```

### hs_smart_search ✨ 新功能（v1.0.18）
- **智能路由机制**：根据查询内容自动选择最合适的检索方式（搜索、图谱遍历或影响分析）。
- **适用场景**：不确定使用哪种模式时，或进行自然语言查询时。
- **返回内容**：查询结果及所使用的检索方式。

### 使用场景：
- 不确定使用 `hs_search`、`hs_graph` 还是 `hs_impact` 时。
- 需要查询依赖关系、关联信息或上下文时。
- 在多智能体协作中，当查询智能体不了解图谱结构时。

### hs_store
用于将信息存储到图谱中，并自动添加智能体标识。支持固定卡片以防止被删除，同时支持为临时卡片设置 TTL 有效期。

**支持的卡片类型：** `general`、`person`、`project`、`decision`、`preference`、`workflow`、`event`、`account`、`signal`、`scratchpad`。

### hs_decide
用于记录决策结果，包括决策者、受影响对象及具体影响内容。

### hs_commit ✨ 新功能（v1.0.19）
- 将成功的任务结果作为永久性决策卡片提交，并通过 `decided` 关系自动链接到原始任务。
- 帮助智能体从实际操作中学习经验。
- 每次提交都会生成完整的版本历史记录和嵌入数据，并触发 Webhook。

### 使用场景：
- 任务成功完成后：将结果提交以便其他智能体参考。
- 建立操作性记忆：记录实际生效的操作，而不仅仅是计划中的内容。
- 会话结束前：提交所有已做出的决策以确保其持久保存。

### hs_prune ✨ 新功能（v1.0.19）
- 自动删除 N 天未更新且未被其他卡片引用的过时卡片。
- 固定的卡片和 TTL 临时卡片永远不会被删除。执行操作前请务必先使用 `dry=true` 进行预览。

**安全保障：**
- 被其他卡片引用的卡片永远不会被删除（保持图谱完整性）。
- 被标记为 `pinned` 的卡片永远不会被删除。
- TTL 临时卡片遵循自身设定的过期规则，不会被自动删除。
- 使用 `dry=true` 时仅进行预览，不会执行删除操作。

### 使用场景：
- 定期维护：删除废弃的任务和过时的信息。
- 在进行重大重构前：清理可能干扰检索的过时数据。
- 执行操作前请务必先进行预览和检查。

### hs_blockers
用于查看哪些因素会阻碍任务/卡片的执行。返回精确的类型化阻塞信息，而非模糊搜索结果。

### hs_graph
从指定卡片开始正向遍历知识图谱，展示卡片之间的连接关系和所有权信息。支持时间旅行功能：通过传入时间戳可查看任意时间点的图谱状态。

### hs_impact ✨ 新功能（v1.0.16）
- 反向遍历：找出依赖或受特定卡片影响的所有元素。

### hs_recommend ✨ 新功能（v1.0.16）
- 根据卡片在图谱中的共引用次数（共引用评分）推荐相关卡片。

### hs_my_cards
列出当前智能体创建的所有卡片。

### hs_ingest
从原始文本中自动提取卡片信息，完全不依赖大型语言模型。

### hs_inbox
检查其他智能体是否向当前智能体发送了相关卡片。

### hs_stats （专业版+）
提供工作空间的令牌使用情况和内存使用统计信息。

### hs_webhook （团队版+）
允许注册 Webhook 以实现实时通知。

### hs_agent_tokens （团队版+）
支持为每个智能体创建、列出和撤销令牌。

---

## 六种图谱遍历模式

HyperStack 的图谱 API 覆盖了智能体可能提出的所有关联性问题：

| 遍历模式 | 工具 | 可解答的问题 |
|--------|------|-------------------|
| 智能搜索 | `hs_smart_search` | 可以提出任何问题，系统会自动选择合适的检索方式 |
| 正向遍历 | `hs_graph` | 这张卡片与其他卡片有何关联？ |
| 影响分析 | `hs_impact` | 这张卡片依赖于哪些元素？如果它发生变化会引发什么问题？ |
| 推荐 | `hs_recommend` | 即使没有直接链接，也能找到相关内容 |
| 时间旅行 | `hs_graph`（配合 `at=` 参数） | 某一时刻图谱的具体结构是怎样的？ |
| 修剪 | `hs_prune` | 哪些过时的信息可以安全删除？ |

---

## 内存模型

HyperStack 完整管理了智能体的整个内存生命周期：

| 内存类型 | 工具 | 行为 |
|-------------|------|-----------|
| 长期存储的数据 | `hs_store` | 永久保存，可搜索，且与图谱关联 |
| 临时工作记忆 | `hs_store`（配合 `ttl=` 和 `type=scratchpad`） | 到期后自动删除 |
| 成功的决策结果 | `hs_commit` | 作为永久性决策卡片保存 |
| 过时信息的清理 | `hs_prune` | 删除未使用的卡片，同时保持图谱完整性 |
| 被保护的卡片 | `hs_store`（配合 `pinned=true`） | 永远不会被删除 |

---

## 多智能体协作设置

每个智能体都有唯一的 ID，卡片会自动标记创建者信息。

**推荐角色：**
- **协调者**：负责任务分配，监控潜在的阻碍因素（使用 `hs_blockers`、`hs_impact`、`hs_graph`、`hs_decide`）。
- **研究员**：负责调查和存储研究结果（使用 `hs_search`、`hs_recommend`、`hs_store`、`hs_ingest`）。
- **执行者**：负责实施操作并记录技术决策（使用 `hs_store`、`hs_decide`、`hs_commit`、`hs_blockers`）。
- **内存管理器**：负责维护图谱的健康状态（使用 `hs_prune`、`hs_stats`、`hs_smart_search`）。

---

## 设置方式

### 选项 A：MCP（Claude Desktop / Cursor / VS Code / Windsurf）
```json
{
  "mcpServers": {
    "hyperstack": {
      "command": "npx",
      "args": ["-y", "hyperstack-mcp"],
      "env": { "HYPERSTACK_API_KEY": "hs_your_key" }
    }
  }
}
```

### 选项 B：OpenClaw 环境变量配置
1. 获取免费 API 密钥：https://cascadeai.dev/hyperstack
2. 在 OpenClaw 环境变量中设置 `HYPERSTACK_API_KEY=hs_your_key`
3. 相关工具可立即使用。

### 选项 C：程序化方式（Node.js 适配器）
```js
import { createOpenClawAdapter } from "hyperstack-core/adapters/openclaw";
const adapter = createOpenClawAdapter({ agentId: "builder" });
await adapter.onSessionStart({ agentName: "Builder", agentRole: "Implementation" });
await adapter.onSessionEnd({ summary: "Completed auth migration" });
```

---

## 各工具的使用场景

| 使用场景 | 推荐工具 |
|--------|------|
| 会话开始 | 使用 `hs_search` 和 `hs_recommend` 获取上下文信息 |
| 不确定使用哪种模式 | 使用 `hs_smart_search`（系统会自动选择合适的模式） |
- 新项目/入职培训 | 使用 `hs_ingest` 从现有文档中自动填充信息 |
- 做出决策 | 使用 `hs_decide` 并附上决策理由和链接 |
- 任务完成 | 使用 `hs_commit` 将结果保存为决策卡片 |
- 任务受阻 | 使用 `hs_store` 并添加 `blocks` 关系 |
- 开始工作前 | 使用 `hs_blockers` 检查任务依赖关系 |
- 发现新问题 | 使用 `hs_recommend` 查找相关背景信息 |
- 管理临时工作记忆 | 使用 `hs_store`（配合 `ttl=` 和 `type=scratchpad`） |
- 定期维护 | 使用 `hs_prune`（设置 `dry=true` 进行预览，再执行删除操作） |
- 调试错误决策 | 使用 `hs_graph` 并指定时间戳 |
- 跨智能体通信 | 使用 `hs_store` 并指定目标智能体，其他智能体通过 `hs_inbox` 接收通知 |
- 检查效率 | 使用 `hs_stats` 查看令牌使用情况 |
- 限制智能体权限 | 为每个智能体创建专属令牌（使用 `hs_agent_tokens`） |

---

## 数据安全

**重要提示：**
- 绝不要存储密码、API 密钥、令牌、个人身份信息（PII）或任何敏感数据。即使发生数据泄露，卡片内容也应保持安全。
- 在存储任何数据之前，请务必获得用户明确授权。

## 价格方案

- **免费版**：提供 10 张卡片、关键词搜索功能及 REST API 接口。
- **专业版（每月 29 美元）**：提供 100 张卡片、所有图谱遍历模式、语义搜索和数据分析功能。
- **团队版（每月 59 美元）**：提供 500 张卡片、5 个团队 API 密钥和 Webhook 功能。
- **企业版（每月 149 美元）**：提供 2,000 张卡片、20 个团队账户和单点登录（SSO）功能。

## 更新日志

### v1.0.19（2026年2月20日）
- **新增功能：** `hs_prune` — 基于预览机制的自动内存修剪功能：删除 N 天未更新且未被其他卡片引用的过时卡片。优先考虑数据安全，不会删除被引用的卡片或被标记为固定的卡片。
- **新增功能：** `hs_commit` — 基于反馈的决策保存机制：将成功任务结果作为永久性决策卡片保存，并通过 `decided` 关系链接到原始任务。帮助智能体积累实际操作经验。
- **新增字段：** 卡片上的 `pinned` 标签：可永久保护卡片不被删除，适用于核心架构决策或关键约束条件。
- **新增功能：** `scratchpad` 卡片类型：用于临时存储的卡片，配合 `ttl` 参数实现自动过期管理。

### v1.0.18（2026年2月20日）
- 新增 `hs_smart_search` — 智能路由机制（自动选择检索模式）。
- 与 MCP v1.6.0、hyperstack-py v1.1.0 和 hyperstack-langgraph v1.3.0 兼容。

### v1.0.17（2026年2月19日）
- 修复元数据相关问题。

### v1.0.16（2026年2月19日）
- 新增 `hs_impact` — 反向图谱遍历功能。
- 新增 `hs_recommend` — 基于共引用次数推荐相关卡片的功能。

### v1.0.15（2026年2月17日）
- 新增 `hs_stats` — 提供令牌使用情况和内存使用统计信息（专业版+）。
- 新增 `hs_agent_tokens` — 为每个智能体设置权限（团队版+）。

### v1.0.14（2026年2月17日）
- 新增 `hs_ingest`、`hs_inbox` 和 `hs_webhook`/`hs_webhooks` 功能。

### v1.0.13 及更早版本
- 提供了 `hs_search`、`hs_store`、`hs_decide`、`hs_blockers`、`hs_graph` 和 `hs_my_cards` 等基础功能。