---
name: multi-agent-blueprint
version: 2.0.0
description: 经过生产环境测试的蓝图：用于在 OpenClaw 中构建 5 至 10 个代理团队，支持跨代理路由、Telegram 集成以及基于角色的架构设计。
emoji: 🏗️
tags:
  - multi-agent
  - team
  - orchestration
  - blueprint
  - telegram
  - routing
  - cost-optimization
---
# 多智能体蓝图 — 构建你的AI团队

这是一个经过生产测试的模板，用于设置**5-10个专门的AI智能体**，它们作为一个团队协同工作。该模板基于实际部署方案，其中10个智能体通过Telegram进行跨智能体路由、模型分层和集中文件管理。

## 你将获得什么

- **智能体角色模板**：SOUL.md、AGENTS.md、IDENTITY.md、USER.md
- **跨智能体路由**：通过`sessions_send`实现，并使用有效的会话密钥
- **模型分层**策略（Opus/Sonnet/Haiku），以优化成本
- **Telegram多机器人**设置：支持私信隔离和群组@提及
- **文件管理大师模式**：通过一个智能体集中管理文件操作
- **Notion数据库大师模式**：通过一个智能体集中管理数据库操作
- **备用链**：实现弹性多提供者模型路由
- **成本优化配置**：包括缓存、本地模型的心跳检测、上下文修剪
- **RAG/Memory**设置：确保会话间的知识持久性
- **群组聊天头脑风暴**：多个智能体可以在同一个对话中协作

## 架构

```
┌─────────────────────────────────────────────┐
│                   USER                       │
│         (Telegram / Discord / WhatsApp)      │
└──────────┬──────────────────────┬───────────┘
           │ DM                   │ @mention
     ┌─────▼─────┐         ┌─────▼─────┐
     │ CENTRAL   │         │  GROUP    │
     │ (Coordi-  │◄───────►│  CHAT     │
     │  nator)   │ routes  │ (all bots)│
     └─────┬─────┘         └───────────┘
           │ sessions_send
     ┌─────┼─────┬──────┬──────┬──────┐
     ▼     ▼     ▼      ▼      ▼      ▼
   TECH  FINANCE SALES HEALTH MKTG  DATA
    │                                  │
    ▼                                  ▼
   NAS                             NOTION
  (File Master)                  (DB Master)
```

## 快速入门

### 1. 规划你的团队

根据需求选择3-10个角色：

| 角色 | 模型层级 | 示例任务 |
|------|-----------|---------------|
| 协调员 | Opus | 路由任务、监督项目、每日简报 |
| 技术/基础设施 | Opus/Sonnet | DevOps、文件管理、系统管理员 |
| 财务 | Sonnet | 发票处理、预算编制、税务准备、合同管理 |
| 销售 | Haiku | 潜在客户开发、外联脚本、交易跟踪 |
| 市场营销 | Haiku | 内容创作、搜索引擎优化（SEO）、社交媒体管理 |
| 健康管理 | Sonnet | 健身追踪、饮食计划、习惯辅导 |
| 数据/Notion | Sonnet | 数据库操作、报告生成、文档编写 |
| DevOps | Haiku | 监控、警报、系统运行状态检查 |
| 电子商务 | Haiku | 商店审核、产品策略制定、数据分析 |
| 社交媒体/品牌 | 外部提供者* | Twitter/X、LinkedIn、内容调度 |

*社交媒体智能体可以使用如xAI/Grok这样的专用提供者来适应平台特性。*

### 2. 创建智能体目录

```bash
# For each agent:
mkdir -p ~/.openclaw/workspace-{agentname}/memory
mkdir -p ~/.openclaw/agents/{agentname}/agent
```

### 3. 配置OpenClaw

将每个智能体添加到`openclaw.json`的`agents.list`中：

```json5
{
  "id": "finance",
  "name": "finance",
  "workspace": "~/.openclaw/workspace-finance",
  "agentDir": "~/.openclaw/agents/finance/agent",
  "model": "anthropic/claude-sonnet-4-5"
}
```

### 4. 创建智能体文件

每个智能体在其`agentDir`目录下需要4个文件：

#### IDENTITY.md
```markdown
# IDENTITY.md
- **Name:** Atlas
- **Creature:** AI Finance & Legal Advisor
- **Vibe:** Professional, precise, trustworthy
```

#### SOUL.md（个性与规则）
```markdown
# SOUL.md
You are Atlas. Finance & Legal specialist.

PERSONALITY:
- Professional but approachable
- Numbers-driven, always backs claims with data
- Proactively flags risks and deadlines

EXPERTISE:
- Invoice management, expense tracking
- Tax preparation and compliance
- Contract review and negotiation support

RESPONSE LENGTH:
- DEFAULT: 2-5 sentences. Telegram, not blog posts.
- Short question = short answer. "Done.", "Yes.", "Sent." are fine.
- Longer responses ONLY for: financial breakdowns, step-by-step guides, or when explicitly asked.
- No introductions. Get to the point.
- No repeating the question back.
```

#### AGENTS.md（路由表）
```markdown
# AGENT OPERATING SYSTEM — Atlas

## My Role
Finance & Legal. Invoices, budgets, contracts, tax.

## Cross-Agent Routing
| What | Where | How |
|------|-------|-----|
| Coordination | Central | sessions_send(sessionKey="agent:central:main", ...) |
| File Storage | Tech | sessions_send(sessionKey="agent:techops:main", ...) |
| Database/Notion | Data | sessions_send(sessionKey="agent:data:main", ...) |
| Sales Numbers | Sales | sessions_send(sessionKey="agent:sales:main", ...) |

## What I Handle
- Invoice creation and tracking
- Budget reports and forecasts
- Contract review
- Tax document preparation

## What I DON'T Handle
- File storage → Tech agent (File Master)
- Database updates → Data agent (Notion Master)
- Marketing spend analysis → Marketing agent
```

#### USER.md
```markdown
# USER.md
- **Name:** [Your name]
- **Timezone:** Europe/Berlin
- **Business:** [Your business]
- **Language:** English (casual)
```

### 5. Telegram多机器人设置

通过@BotFather为每个智能体创建一个Telegram机器人，然后进行配置：

```json5
// openclaw.json
{
  // CRITICAL: This prevents session collision between bots
  "session": { "dmScope": "per-account-channel-peer" },

  "channels": {
    "telegram": {
      // DO NOT put botToken here at top level — causes double responses
      "accounts": {
        "finance": {
          "botToken": "YOUR_BOT_TOKEN",
          "dmPolicy": "allowlist",
          "allowFrom": ["YOUR_TELEGRAM_ID"],
          "groups": {
            "-YOUR_GROUP_ID": { "requireMention": true }
          }
        }
      }
    }
  },

  "bindings": [
    {
      "agentId": "finance",
      "match": { "channel": "telegram", "accountId": "finance" }
    }
  ]
}
```

**关键设置：**
- `dmScope: "per-account-channel-peer"` — 防止机器人之间的会话冲突
- `requireMention: true` — 机器人仅在群组中被@提及时才响应
- 不使用顶级的`botToken` — 避免重复响应
- 每个机器人需要与其绑定的`accountId`相匹配

### 6. 模型分层与备用链

```json5
{
  "models": {
    "fallbackOrder": [
      "anthropic/claude-opus-4-6",
      "anthropic/claude-sonnet-4-5",
      "google-gemini-cli/gemini-2.5-flash",
      "ollama/llama3.2:3b",
      "openrouter/anthropic/claude-sonnet-4"
    ]
  }
}
```

**为什么备用链很重要：**
- 主要提供者故障？自动切换到下一个提供者。
- Claude模型被限制使用频率？切换到Gemini模型。
- 互联网中断？使用本地Ollama模型保持心跳检测。
- OpenRouter作为最后手段（按令牌计费）。

### 7. 成本优化配置

```json5
{
  "agents": {
    "defaults": {
      // Heartbeats on FREE local model — saves hundreds of API calls/day
      "heartbeat": { "every": "30m", "model": "ollama/llama3.2:3b" },

      // Auto-prune old context to reduce token usage
      "contextPruning": { "mode": "cache-ttl", "ttl": "5m" },

      // Memory search with caching
      "memorySearch": { "enabled": true, "cache": { "enabled": true } },

      // Enable prompt caching (huge savings on Anthropic)
      "models": {
        "anthropic/claude-opus-4-6": { "params": { "cacheRetention": "long" } },
        "anthropic/claude-sonnet-4-5": { "params": { "cacheRetention": "long" } },
        "anthropic/claude-haiku-4-5": { "params": { "cacheRetention": "none" } }
      }
    }
  }
}
```

### 8. RAG/Memory设置

确保智能体在会话重置后仍能保留重要信息：

```json5
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "providers": ["local"],   // local = free, no API costs
        "search": { "mode": "hybrid" },  // BM25 + vector
        "cache": { "enabled": true, "maxEntries": 50000 }
      }
    }
  }
}
```

智能体会在会话压缩前将重要上下文存储在`memory/*.md`文件中。在下一个会话中，`memory_search`会自动检索相关内容。

## 设计模式

### 文件管理大师模式
通过**一个智能体**路由所有文件操作：
- 其他智能体不会直接访问文件系统或NAS
- 文件管理大师负责存储、检索和备份
- 文件位置的唯一信息来源
- 只需要一个智能体拥有SSH/NAS访问权限

```
Agent → sessions_send → File Master → SSH → NAS
                              ↓
                        Confirmation back
```

### Notion/数据库大师模式
通过**一个智能体**路由所有数据库操作：
- 集中管理API凭证
- 避免写入冲突
- 只有一个智能体了解完整的数据库架构

```
Agent → sessions_send → DB Master → Notion API → Database
                              ↓
                        Confirmation back
```

### 协调员模式
一个中央智能体充当路由器：
- 首先接收所有用户请求
- 通过`sessions_send`将请求路由给相应的专家智能体
- 收集结果并反馈给用户
- 适合希望有一个统一入口点的用户

### 专家直接模式
用户直接与所需专家智能体沟通：
- 通过私信向财务智能体咨询发票问题
- 通过私信向销售智能体咨询交易策略
- 通过私信向健康管理智能体获取健身建议
- 最快的沟通方式——无需额外的路由开销

### 群组头脑风暴模式
在Telegram群组中，多个智能体可以通过`requireMention: true`进行交流：
- 通过@提及特定智能体来请求专业帮助
- 智能体之间可以互相查看对方的回复
- 非常适合策略讨论、计划制定和评审

## 跨智能体通信

智能体之间通过`sessions_send`进行通信：

```javascript
// From any agent's tool call:
sessions_send({
  sessionKey: "agent:techops:main",
  message: "Store this file on NAS: quarterly-report.pdf at /finance/reports/"
})
```

**会话密钥格式：**`agent:{agentId}:main`

**重要提示：**接收消息的智能体会在自己的会话中使用自己的工具和权限处理消息。回复会自动路由回去。

## 模型分层策略

| 模型层级 | 模型 | 月度成本* | 适用场景 |
|------|-------|--------------|----------|
| **高级** | Opus 4.6 | $$$ | 协调员 + 技术负责人（复杂推理、多步骤任务） |
| **标准** | Sonnet 4.5 | $$ | 财务、健康、数据（良好推理、成本较低） |
| **经济型** | Haiku 4.5 | $ | 销售、市场营销、DevOps（简单任务、快速响应） |
| **免费** | Ollama本地模型 | $0 | 心跳检测、基本功能 |
| **外部提供者** | xAI Grok / GPT | 价格不一 | 专门任务（社交媒体、研究） |

*使用Claude订阅可以覆盖大部分使用需求。Haiku模型几乎免费。*

**经验法则：**使用最便宜的模型来完成任务。以后可以随时升级特定智能体。

## 常见错误

| 编号 | 错误 | 修复方法 |
|---|---------|-----|
| 1 | 所有智能体都使用Opus模型 | 使用分层策略——Haiku模型可以处理70%的任务 |
| 2 | 未设置`dmScope: per-account-channel-peer` | 会导致会话冲突 |
| 3 | 群组中未设置`requireMention: true` | 机器人会对所有消息做出响应（造成混乱） |
| 4 | 在Telegram配置中使用顶级`botToken` | 会导致重复响应 |
| 5 | 未启用`agentToAgent.enabled` | 跨智能体路由功能将失效 |
| 6 | 会话压缩前未清除内存 | 会话重置时会导致上下文丢失 |
| 7 | 多个智能体直接操作文件 | 会导致状态不一致和竞争条件 |
| 8 | 多个智能体共享同一工作空间 | 会导致文件冲突和内存问题 |
| 9 | 未设置备用链 | 单个提供者故障会导致所有智能体停止工作 |
| 10 | 未同步agentDir和工作空间 | 会导致配置不一致 |

## 扩展指南

### 单人创始人 — 从小规模开始（3个智能体）
```
Coordinator (Opus) → Tech (Sonnet) → Sales (Haiku)
```
这可以满足80%的需求。只有在出现明确的角色需求时再增加智能体。

### 业务扩展（5-7个智能体）
```
Coordinator → Tech → Finance → Sales → Marketing
                                    → Data/Notion
```

### 完整团队（8-10个智能体）
```
Coordinator → Tech (File Master)
           → Finance/Legal
           → Sales
           → Marketing
           → Health/Personal
           → Data/Notion (DB Master)
           → DevOps (Monitoring)
           → E-Commerce
           → Social/Brand
```

### 成本估算
| 团队规模 | Claude订阅费用 | 额外API费用 | 总费用 |
|-----------|-------------------|-----------------|-------|
| 3个智能体 | 约20美元/月 | 约0-5美元 | 约20-25美元/月 |
| 5个智能体 | 约20美元/月 | 约5-10美元 | 约25-30美元/月 |
| 10个智能体 | 约20美元/月 | 约10-20美元 | 约30-40美元/月 |

*Ollama模型的心跳检测费用为0美元。Haiku模型几乎不产生额外费用。启用缓存功能可降低50-90%的成本。*

## 会话管理

### 自动重置
配置会话重置机制以防止上下文溢出：
```json5
{
  "session": {
    "maxIdleMinutes": 45,
    "dailyResetUtc": "04:00"
  }
}
```

### 内存持久化
智能体应在重置前保存重要上下文：
```markdown
<!-- In agent's BOOTSTRAP.md -->
## Memory Flush
Before session compaction, save key decisions, dates, and action items
to memory/*.md files using the write tool.
```

## 常见问题解答

**Q：所有智能体都需要自己的Telegram机器人吗？**
A：只有当你希望通过私信直接与它们沟通时才需要。智能体也可以仅通过`sessions_send`（后端接口）进行交互，无需Telegram机器人。

**Q：智能体可以共享工作空间吗？**
A：不可以。每个智能体需要自己的工作空间以避免文件冲突和内存问题。

**Q：当上下文信息过多时会发生什么？**
A：OpenClaw会自动压缩会话。启用内存清除功能，以便智能体在压缩前将重要信息保存到`memory/*.md`文件中。

**Q：我可以混合使用不同的提供者（Anthropic + Google + Ollama + xAI）吗？**
A：可以。每个智能体可以使用不同的模型和提供者。通过备用链实现灵活性。

**Q：如何调试跨智能体路由？**
A：检查配置中的`agentToAgent.enabled`设置。使用简单的ping测试进行验证：
```
sessions_send(sessionKey="agent:techops:main", message="ping — reply pong")
```

**Q：如何向现有团队添加新的智能体？**
A：创建工作空间和智能体目录，将其添加到`agents.list`中，生成4个配置文件，创建Telegram机器人（可选），更新其他智能体的路由表，然后重启系统。

**Q：智能体可以调用外部API吗？**
A：可以，通过`exec`（curl/scripts）或专用技能实现。API密钥应保存在`.env`文件中，而不是智能体文件中。

**Q：关于速率限制怎么办？**
A：备用链会自动处理这个问题。如果Claude模型被限制使用频率，请求会自动切换到下一个提供者。启用缓存功能也可以显著减少令牌消耗。

## 更新日志

### v2.0.0
- 新增了Notion/数据库大师模式
- 新增了RAG/Memory设置指南
- 新增了备用链配置
- 新增了会话管理相关内容
- 更新了成本估算（包含具体数字）
- 新增了10个常见错误示例
- 新增了关于新智能体、外部API和速率限制的常见问题解答
- 所有示例均使用英文
- 优化了扩展指南并添加了成本表格

### v1.1.0
- 统一了所有智能体的名称和示例
- 删除了具体的设置细节

### v1.0.0
- 初始版本发布