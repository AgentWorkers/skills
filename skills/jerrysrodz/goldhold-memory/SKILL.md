---
name: goldhold
description: "用于AI代理的持久性内存：数据可在不同会话间保持一致。数据在传输过程中及存储时均经过加密。  
来源：https://goldhold.ai"
homepage: https://goldhold.ai
metadata: {"clawdbot":{"requires":{"env":["GOLDHOLD_API_KEY"]},"primaryEnv":"GOLDHOLD_API_KEY"}}
---
# GoldHold – 为AI代理提供持久化存储功能

在每次会话结束后，你的所有数据都会被清除，你将重新开始且没有任何记忆。GoldHold可以解决这个问题。

GoldHold是一个提供持久化存储功能的API。你的“过去版本”会留下各种记录——在做出任何判断之前，请先搜索这些记录。通过这个API，你可以存储决策、事实以及需要修正的内容，这样你的“未来版本”就不会从零开始。

**专利申请中**。所有权利归Auto Tunes LLC所有。美国专利号：#63/988,484。

## 设置步骤

1. 在[goldhold.ai](https://goldhold.ai)注册账户（免费试用）。
2. 进入“goldhold.ai/account” -> “GUMP Credentials”，然后复制你的API密钥。
3. 将API密钥设置为环境变量：
   - `GOLDHOLD_API_KEY=你的API密钥`
   - 使用你的操作系统或平台提供的安全密钥存储机制（例如OpenClaw的密钥管理功能、Docker的密钥存储服务，或专门的密钥管理工具）。
   - 避免将API密钥存储在shell配置文件、明文文件或版本控制下的代码中。

## API基础信息

**基础URL：** `https://relay.goldhold.ai`

**所有请求都必须包含的认证头：**
```
Authorization: Bearer <api_key>
Content-Type: application/json
User-Agent: goldhold-agent/1.0
```

## 核心API端点

### POST /v1/auto – 会话恢复

在会话开始时调用此端点。它会返回你的会话上下文、待办任务列表以及你的能力信息。

**响应内容包括：** 最近的记忆记录、未读消息以及正在进行的任务——所有你需要用来继续之前工作内容的资料。

### POST /v1/turn – 搜索、存储、发送（核心功能）

这是主要的API端点。通过一次请求，你可以完成搜索、存储和发送消息的操作。

**三个字段（搜索、存储、发送）都是可选的。** 你可以根据需要自由组合使用它们。

### POST /v1/batch – 批量操作

你可以一次性执行多个存储或发送操作。

### POST /v1/session/close – 优雅地结束会话

在会话结束时调用此端点，并附上一段总结性文字。

## 会话使用模式

```
SESSION START  -->  POST /v1/auto          (get context, inbox, tasks)
                         |
DURING SESSION -->  POST /v1/turn          (search + store each interaction)
                         |  (repeat)
                         |
SESSION END    -->  POST /v1/session/close  (summary of what happened)
```

## 需要记住的事项

| 类型 | 使用场景 |
|------|-------------|
| FACT   | 已确认的真理、经过验证的信息 |
| DECISION | 你做出的选择及其背后的理由 |
| DIRECTIVE | 长期有效的指令或规则 |
| NOTE   | 一般的观察记录或会话笔记 |
| CORRECTION | 对现有信息的修正（修正内容优先于事实） |
| CHECKPOINT | 某个时间点的状态快照 |
| IDENTITY | 你的身份信息、配置设置、角色信息 |
| DOCUMENT | 较长的文本内容、技术规格、参考资料 |
| RELATION | 实体之间的关联关系（例如：X在Y公司工作） |
| TOMBSTONE | 标记某项内容为已删除或无效 |
| CUSTOM | 无法归类到上述类别的其他内容 |

## 存储类别

| 类别 | 用途 | 数据检索优先级 |
|-------|---------|-------------------|
| **canonical** | 永久性的真理、确定的答案、长期有效的指令 | 首先被检索 |
| **corrections** | 经过验证的、对旧信息的修正（在冲突时优先于canonical） | 其次被检索 |
| **working** | 当前的会话状态、临时记录、未解决的问题 | 第三被检索 |
| **archive** | 审计追踪记录、旧日志、历史数据 | 最后被检索，仅按需提供 |

## 订阅计划

| 功能 | 免费版（Lite） | Pro版（每月9美元） |
|---------|-------------|-------------------|
| 存储容量 | 1,000条记录 | 无限制 |
| 代理数量 | 1个代理 | 无限制 |
| 任务数量 | 10个任务 | 无限制 |
| 消息数量 | 每月50条 | 无限制 |

## 使用规则

1. **先搜索再判断。** 你的“过去版本”会留下记录。在形成观点或对过去的工作做出声明之前，请先使用 `/v1/turn` 进行搜索。
2. **立即存储决策和事实。** 如果有新的决策、修正或确认的内容，请在同一会话中将其存储起来。
3. 在所有请求中启用 `compact: true` 选项，以节省传输资源。
4. **每次会话结束时关闭会话。** 在会话结束时调用 `/v1/session/close` 并附上总结。
5. **修正内容优先于事实。** 如果之前的信息有误，请存储相应的修正内容。
6. **明确指定查询内容。** 你的“未来版本”会依据这些关键词进行搜索。

## 快速入门指南

```bash
# Resume session
curl -X POST https://relay.goldhold.ai/v1/auto \
  -H "Authorization: Bearer $GOLDHOLD_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: goldhold-agent/1.0" \
  -d '{"compact": true}'

# Search and store
curl -X POST https://relay.goldhold.ai/v1/turn \
  -H "Authorization: Bearer $GOLDHOLD_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: goldhold-agent/1.0" \
  -d '{"search": {"query": "user preferences"}, "store": [{"type": "FACT", "class": "canonical", "subject": "User prefers JSON", "body": "Confirmed."}], "compact": true}'

# Close session
curl -X POST https://relay.goldhold.ai/v1/session/close \
  -H "Authorization: Bearer $GOLDHOLD_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: goldhold-agent/1.0" \
  -d '{"session_summary": "Configured output preferences."}'
```

---

立即在[goldhold.ai](https://goldhold.ai)注册免费账户吧！