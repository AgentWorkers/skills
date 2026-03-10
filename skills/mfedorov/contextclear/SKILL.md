---
name: contextclear
description: 通过 ContextClear API 监控 AI 代理的运行状态、成本和性能。该 API 可用于追踪代理的疲劳程度、令牌使用情况、错误率以及是否存在“幻觉”（即代理产生的错误或异常行为），同时还能帮助优化成本。在大型语言模型（LLM）执行任务后，系统会自动生成相关指标报告。您还可以为异常情况设置警报机制，以便及时发现潜在问题。
---
# ContextClear – 代理内存管理与健康监控

您可以自行监控代理的健康状况，并确保代理在会话之间保持持续的内存状态。

## 设置

### 选项 1：自动注册（推荐）

```bash
python3 {baseDir}/scripts/report.py --register \
  --name "my-agent" \
  --owner "you@email.com" \
  --model "claude-opus-4-6" \
  --provider "Anthropic"
```

此操作会返回一个 `agentId` 和 `apiKey`。请将这两个信息保存下来。

### 选项 2：通过控制面板进行注册

1. 访问 https://www.contextclear.com 进行注册。
2. 从管理员页面获取您的 API 密钥。
3. 通过“管理员” > “代理”选项卡注册您的代理。

### 自动设置（推荐——将上下文恢复功能集成到您的代理中）

注册完成后，运行设置脚本以自动更新您的 `AGENTS.md` 和 `HEARTBEAT.md` 文件：

```bash
python3 {baseDir}/scripts/setup.py \
  --agent-id <your-agent-id> \
  --api-key <your-api-key>
```

此设置会实现以下功能：
- **会话开始时恢复上下文**：代理在数据压缩后调用 `/recover` 功能。
- **在心跳请求时生成上下文快照**：代理会保存当前正在处理的信息。
- 该操作是幂等的（可多次执行而不会产生错误）。

### 配置

请在您的 `HEARTBEAT.md` 文件中添加以下配置：

```markdown
## ContextClear Self-Report
Agent ID: <your-agent-id>
API Key: <your-api-key>
API URL: https://api.contextclear.com/api
```

## 代理内存基础设施

### 会话恢复（在会话开始时执行）

在开始新会话时，调用恢复端点以获取相关信息：

```bash
curl -s {apiUrl}/agents/{agentId}/recover \
  -H "X-API-Key: <api-key>"
```

返回结果：
```json
{
  "lastSession": { "summary": "...", "repos": [...], "files": [...] },
  "openThreads": ["..."],
  "recentWork": { "sessionCount": 3, "totalTurns": 45, "errors": 1 },
  "repeatedAsks": [{ "question": "...", "count": 3, "suggestedFix": "..." }],
  "frequentResources": { "repos": {...}, "tools": {...} }
}
```

### 生成上下文快照（在每次完成实际工作后执行）

在完成有意义的工作后，生成一个上下文快照：

```bash
curl -X POST {apiUrl}/agents/{agentId}/context \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <api-key>" \
  -d '{
    "sessionId": "main-session-2026-03-09",
    "summary": "Built Best Of collections for FW, fixed dup check, removed keyword boost",
    "repos": ["nebulent/fridayswatchlist"],
    "files": ["AuctionService.java", "DiscoverController.java", "BestOfCollections.tsx"],
    "tools": ["MongoDB Atlas (fridayswatchlist)", "Railway deploy", "Bitbucket"],
    "decisions": ["Removed keyword boost regex - hybrid search covers it", "Cache collections for 48h"],
    "openThreads": ["Delete stale Corvette dup", "Update contextclear skill"],
    "environment": { "apiUrl": "api.fridayswatchlist.com", "frontendUrl": "app.fridayswatchlist.com" },
    "tags": ["fridayswatchlist", "performance", "search"],
    "contextTokens": 85000,
    "contextCapacity": 200000,
    "contextUtilizationPct": 42.5
  }'
```

### 检测重复提问行为（当发现重复提问时自动报告）

当您发现自己在询问用户本应已经知道的信息时，系统会自动进行报告：

```bash
curl -X POST {apiUrl}/agents/{agentId}/context/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <api-key>" \
  -d '{"question": "What is the MongoDB connection string?", "sessionId": "main-session-2026-03-09"}'
```

### “我知道什么”——人工智能生成的总结

```bash
curl -s {apiUrl}/agents/{agentId}/what-i-know \
  -H "X-API-Key: <api-key>"
```

该功能会返回一个结构化的知识库，以及人工智能生成的总结，涵盖代理所知道的内容、正在处理的任务以及经常忘记的信息。这些信息会被缓存 4 小时；您可以使用 `?refresh=true` 来重新生成这些信息。

### 上下文缺失情况

```bash
curl -s {apiUrl}/agents/{agentId}/context/gaps \
  -H "X-API-Key: <api-key>"
```

系统会检测到重复出现的未解决请求（次数大于等于 2 次），即代理经常忘记的信息。

### 简报功能

```bash
# Session-start briefing
curl -s {apiUrl}/agents/{agentId}/briefing -H "X-API-Key: <api-key>"

# Daily briefing
curl -s {apiUrl}/agents/{agentId}/briefing/daily -H "X-API-Key: <api-key>"

# Weekly briefing
curl -s {apiUrl}/agents/{agentId}/briefing/weekly -H "X-API-Key: <api-key>"
```

## 心跳请求集成

### 推荐的心跳请求流程

```markdown
## ContextClear (HEARTBEAT.md)

**Step 1: Check vacation**
curl -s {apiUrl}/agents/{agentId}/vacation -H "X-API-Key: <key>"
If onVacation: true → HEARTBEAT_OK immediately.

**Step 2: Report metrics**
Use session_status to get tokens, then POST /api/metrics/{agentId}

**Step 3: Report context snapshot (if real work was done)**
POST /api/agents/{agentId}/context with summary of what was worked on.

**Step 4: Check for context recovery (first heartbeat of day)**
GET /api/agents/{agentId}/recover — review and self-correct any gaps.
```

## 报告指标

### 基本报告

```bash
python3 {baseDir}/scripts/report.py \
  --agent-id <id> --api-key <key> \
  --tokens-in 50000 --tokens-out 2000 \
  --cost 1.25 --context-util 65
```

### 结合工具/实际反馈数据

```bash
python3 {baseDir}/scripts/report.py \
  --agent-id <id> --api-key <key> \
  --event-type HEARTBEAT \
  --tokens-in 50000 --tokens-out 2000 \
  --tool-calls 12 --tool-failures 1 \
  --grounded-responses 8 --total-responses 10 \
  --memory-searches 3
```

### 从代理代码中获取数据（使用 curl 命令）

```bash
curl -X POST {apiUrl}/metrics/{agentId} \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <api-key>" \
  -d '{
    "eventType": "HEARTBEAT",
    "inputTokens": 5000,
    "outputTokens": 500,
    "contextUtilization": 65.0,
    "toolCalls": 8,
    "toolFailures": 1,
    "memorySearches": 2
  }'
```

## 服务器端计算的内容

| 指标          | 用户输入的内容                |
|----------------|-------------------------|
| **幻觉评分**       | `toolCalls`, `toolFailures`, `groundedResponses`, `totalResponses` |
| **质量下降评分**     | `correctionCycles`, `compilationErrors`, `contextUtilization` |
| **疲劳评分**       | 从事件数据中自动计算             |
| **上下文缺失情况**     | 通过重复提问行为自动检测           |

## 端点接口

| 方法            | 端点地址                | 描述                          |
|----------------|-----------------------------|
| `POST`          | `/api/metrics/register`       | 自动注册代理                |
| `POST`          | `/api/metrics/{agentId}`       | 报告指标事件                    |
| `GET`          | `/api/agents/{id}`         | 代理详细信息                    |
| `POST`          | `/api/agents/{id}/context`       | 保存上下文快照                    |
| `GET`          | `/api/agents/{id}/context`       | 最新上下文信息                    |
| `GET`          | `/api/agents/{id}/recover`       | 恢复上下文简报                    |
| `POST`          | `/api/agents/{id}/context/ask`       | 报告重复提问行为                    |
| `GET`          | `/api/agents/{id}/context/gaps`       | 上下文缺失情况                    |
| `GET`          | `/api/agents/{id}/what-i-know`       | 人工智能生成的总结                    |
| `GET`          | `/api/agents/{id}/briefing`       | 最新简报                        |
| `GET`          | `/api/agents/{id}/briefing/daily`     | 每日简报                        |
| `GET`          | `/api/agents/{id}/briefing/weekly`     | 每周简报                        |
| `GET`          | `/api/agents/{id}/vacation`       | 代理休假状态                    |
| `POST`          | `/api/agents/{id}/context/reload`       | 请求重新加载上下文                    |
| `GET`          | `/api/agents/{id}/context/reload/pending` | 检查是否有待重新加载的任务              |
| `POST`          | `/api/agents/{id}/context/reload/{reloadId}/ack` | 确认重新加载请求                    |

## 上下文重新加载（用户发起）

用户可以通过界面请求重新加载特定的上下文快照。
在会话开始或心跳请求时，可以检查是否有待重新加载的任务：

```bash
curl -s {apiUrl}/agents/{agentId}/context/reload/pending \
  -H "X-API-Key: <api-key>"
```

如果存在待重新加载的任务（响应状态为 HTTP 200），响应中会包含快照数据。应用这些数据以恢复上下文，然后确认操作已完成：

```bash
curl -X POST {apiUrl}/agents/{agentId}/context/reload/{reloadId}/ack \
  -H "X-API-Key: <api-key>"
```

如果没有待重新加载的任务，端点会返回 HTTP 204（表示没有内容）。

## 控制面板

- https://www.contextclear.com – 代理群组管理控制面板
- https://www.contextclear.com/what-i-know – 人工智能知识总结
- https://www.contextclear.com/memory – 上下文快照、缺失情况、简报
- https://www.contextclear.com/lounge – 代理休息区
- https://www.contextclear.com/admin – 代理管理及警报设置