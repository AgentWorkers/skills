---
name: cortex-memory
description: 长期结构化记忆系统，具备知识图谱、实体跟踪、时间推理以及跨会话信息检索功能。该系统由 Cortex API 提供支持。
metadata: {"openclaw": {"emoji": "🧠", "category": "memory", "homepage": "https://github.com/Ubundi/Cortex", "primaryEnv": "CORTEX_API_KEY", "requires": {"env": ["CORTEX_API_KEY", "CORTEX_BASE_URL"], "bins": ["curl", "jq"]}}}
---
# Cortex内存

Cortex为您提供了一种结构化的长期存储机制，其功能超出了`memory_search`的范畴。它能够从文本中提取事实、实体及其之间的关系，并将这些信息存储在知识图中，随后通过混合搜索方式（BM25算法 + 语义分析 + 时间信息 + 图谱遍历）来检索这些数据。

在以下情况下，您应该使用Cortex：
- 在不同会话之间检索信息
- 理解概念、人物或项目之间的相互关系
- 跟踪随时间发生的变化（例如，被取代的事实或用户信念的变化）
- 当`memory_search`返回的结果存在噪声或不完整时

**请勿将Cortex用于**`memory_search`能够有效处理的简单查询（例如，当前会话的上下文信息或今日日志中的关键词匹配）。对于这类查询，请优先使用内置的内存系统；只有在需要更复杂的查询时，才考虑使用Cortex。

**如果同时安装了`@cortex/openclaw-plugin`：**该插件会在每个会话开始前自动将相关数据注入到`<cortex_memories>`标签中。如果您在当前上下文中看到`<cortex_memories>`，说明该会话已经通过Cortex进行了查询——除非您需要不同的查询内容（例如，进一步的实体查找或查询类型更改），否则无需再次调用检索功能。

## 设置

使用Cortex需要设置`CORTEX_API_KEY`和`CORTEX_BASE_URL`这两个环境变量。这些变量的配置信息位于`~/.openclaw/openclaw.json`文件中：

```json
{
  "skills": {
    "entries": {
      "cortex-memory": {
        "enabled": true,
        "apiKey": "sk-cortex-oc-YOUR_KEY",
        "env": {
          "CORTEX_BASE_URL": "https://q5p64iw9c9.execute-api.us-east-1.amazonaws.com/prod"
        }
      }
    }
  }
}
```

## 验证连接

```bash
curl -s "$CORTEX_BASE_URL/health" -H "x-api-key: $CORTEX_API_KEY" | jq .
```

预期响应：`{"status": "ok"}`

## 检索——从长期记忆中查找信息

当您需要从过去的会话中检索事实、实体或关系时，请使用以下方法：

```bash
curl -s -X POST "$CORTEX_BASE_URL/v1/retrieve" \
  -H "x-api-key: $CORTEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg query "QUERY_HERE" \
    --arg query_type "factual" \
    --argjson top_k 10 \
    '{query: $query, query_type: $query_type, top_k: $top_k}')" | jq '.results[] | {type, content, score, metadata}'
```

**检索模式：**
- `full`（默认）——同时使用所有5种检索方式 + 图谱遍历 + 重新排序。检索效果最佳，但速度较慢（根据地区不同，可能需要300-600毫秒）。适用于需要最精确结果的复杂查询。
- `fast`——仅使用BM25算法和语义分析，不进行图谱遍历或重新排序（服务器端处理时间约为80-150毫秒）。适用于需要快速查询且可以接受结果精度较低的情况。在请求体中指定`"mode": "fast"`。

```bash
# Fast mode example — quick entity lookup
curl -s -X POST "$CORTEX_BASE_URL/v1/retrieve" \
  -H "x-api-key: $CORTEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg query "QUERY_HERE" \
    --arg query_type "factual" \
    --arg mode "fast" \
    --argjson top_k 5 \
    '{query: $query, query_type: $query_type, top_k: $top_k, mode: $mode}')" | jq '.results[] | {type, content, score}'
```

**查询类型：**
- `factual`——查询与事实（FACT）和实体（ENTITY）相关的节点（适用于：谁、什么、何时、何地等问题）
- `emotional`——查询与情感（EMOTION）、洞察（INSIGHT）、价值（VALUE）或信念（BELIEF）相关的节点（适用于：用户对某事物的感受如何？）
- `combined`——查询所有类型的节点（默认模式，适用于不确定的情况）

**何时使用Cortex进行检索，何时使用`memory_search`：**

| 情况 | 使用`memory_search` | 使用Cortex检索 | 检索模式 |
|---|---|---|---|
| 当前会话的上下文信息 | 是 | 否 | — |
| 简单的关键词查询 | 是 | 否 | — |
- 跨会话的事实信息 | 否 | 通常结果不稳定 | **是** | 通常使用`fast`模式即可 |
- 实体之间的关系（例如：“X与Y的关系是什么？”） | 否 | 无法通过图谱遍历获取 | **是** | 必须使用`full`模式 |
- 时间变化（例如：“X发生了哪些变化？”） | 否 | 无法追踪变化 | **是** | 必须使用`full`模式 |
- 项目范围内的查询 | 否 | 可能存在跨项目的数据干扰 | **是** | 通常使用`fast`模式即可 |
- 实体查找（例如：“Sarah Chen是谁？”） | 部分信息可能缺失 | **是** | 需要同时查询实体节点及其相关事实 | 快速查询时使用`fast`模式，详细查询时使用`full`模式 |

## 记录——将信息存储到长期记忆中

当用户要求您记住某些重要内容，或者遇到需要长期保存的高价值信息时，请使用以下方法：

```bash
curl -s -X POST "$CORTEX_BASE_URL/v1/ingest" \
  -H "x-api-key: $CORTEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg text "TEXT_TO_REMEMBER" \
    --arg session_id "openclaw:$(date +%Y-%m-%d)" \
    '{text: $text, session_id: $session_id}')" | jq '{nodes_created, edges_created, facts: [.facts[].core], entities: [.entities[].name]}'
```

响应结果将显示提取到的内容：
- `facts`——从文本中提取的事实陈述
- `entities`——带有别名的命名实体（如人名、公司名称、地点等）
- `nodes_created` / `edges_created`——创建的图谱节点和关系边

**何时需要记录信息：**
- 用户明确要求您记住某些内容
- 会议中做出的关键决策
- 关于人物、项目或用户偏好的重要信息
- 在将内容写入`MEMORY.md`文件后，也需要将其同步到Cortex中进行结构化存储

**会话ID的命名规则：**
- 通用会话：`openclaw:YYYY-MM-DD`（例如：`openclaw:2026-02-17`）
- 项目范围内的会话：`openclaw:project-name:topic`（例如：`openclaw:project-frontend:memory-md`）
- 日志文件（由npm插件用于文件同步）：`openclaw:project-name:daily:YYYY-MM-DD`
- 用户偏好设置：`openclaw:preferences`

会话ID用于限定查询范围——通过匹配会话ID前缀，可以针对特定项目进行查询。

## 合并对话内容——会话结束

在会话结束时，您可以合并会议中的关键对话内容，并标注发言者信息：

```bash
curl -s -X POST "$CORTEX_BASE_URL/v1/ingest/conversation" \
  -H "x-api-key: $CORTEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg session_id "openclaw:$(date +%Y-%m-%d):session-topic" \
    --argjson messages '[
      {"role": "user", "content": "FIRST USER MESSAGE"},
      {"role": "assistant", "content": "FIRST ASSISTANT RESPONSE"},
      {"role": "user", "content": "SECOND USER MESSAGE"}
    ]' \
    '{messages: $messages, session_id: $session_id}')" | jq '{nodes_created, edges_created, facts: [.facts[].core]}'
```

**何时使用此功能：**
- 在会议中做出重要决策或获得新信息后
- 请不要合并所有对话内容——仅合并具有长期价值的对话片段
- 仅合并关键内容，而不是整个对话记录
- 保留5-15条关键信息，而非全部对话记录

## 初始化——首次运行

首次安装时，需要将用户现有的`MEMORY.md`文件导入系统，以构建知识图谱。

**对于较小的`MEMORY.md`文件**（少于50行/约4KB，适用于大多数用户）：

```bash
MEMORY_CONTENT=$(cat ~/.openclaw/workspace/MEMORY.md 2>/dev/null || echo "")
if [ -n "$MEMORY_CONTENT" ]; then
  curl -s -X POST "$CORTEX_BASE_URL/v1/ingest" \
    -H "x-api-key: $CORTEX_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg text "$MEMORY_CONTENT" --arg session_id "openclaw:bootstrap" \
      '{text: $text, session_id: $session_id}')" | jq '{nodes_created, edges_created, facts: (.facts | length), entities: (.entities | length)}'
fi
```

**对于较大的`MEMORY.md`文件**（包含大量经过整理的信息，通常由高级用户使用）：请根据Markdown标题（##或###）将文件分割成多个部分，然后分别导入。一次性导入大量文件可能会导致请求超时或提取效果不佳。

```bash
# Split MEMORY.md at ## headings and ingest each section
MEMORY_FILE=~/.openclaw/workspace/MEMORY.md
if [ -f "$MEMORY_FILE" ]; then
  SECTION="" TOTAL_FACTS=0 TOTAL_ENTITIES=0
  while IFS= read -r line || [ -n "$line" ]; do
    if echo "$line" | grep -q '^## ' && [ -n "$SECTION" ]; then
      RESULT=$(curl -s -X POST "$CORTEX_BASE_URL/v1/ingest" \
        -H "x-api-key: $CORTEX_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$(jq -n --arg text "$SECTION" --arg session_id "openclaw:bootstrap" \
          '{text: $text, session_id: $session_id}')")
      TOTAL_FACTS=$((TOTAL_FACTS + $(echo "$RESULT" | jq '.facts | length')))
      TOTAL_ENTITIES=$((TOTAL_ENTITIES + $(echo "$RESULT" | jq '.entities | length')))
      SECTION=""
    fi
    SECTION="$SECTION$line
"
  done < "$MEMORY_FILE"
  # Ingest final section
  if [ -n "$SECTION" ]; then
    RESULT=$(curl -s -X POST "$CORTEX_BASE_URL/v1/ingest" \
      -H "x-api-key: $CORTEX_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$(jq -n --arg text "$SECTION" --arg session_id "openclaw:bootstrap" \
        '{text: $text, session_id: $session_id}')")
    TOTAL_FACTS=$((TOTAL_FACTS + $(echo "$RESULT" | jq '.facts | length')))
    TOTAL_ENTITIES=$((TOTAL_ENTITIES + $(echo "$RESULT" | jq '.entities | length')))
  fi
  echo "Bootstrap complete: $TOTAL_FACTS facts, $TOTAL_ENTITIES entities extracted."
fi
```

安装完成后，请运行此脚本一次，并告知用户提取到了多少条事实和实体。

## 错误处理**
- `401 Unauthorized`——API密钥无效或缺失。请让用户检查`CORTEX_API_KEY`的值。
- `422 Validation Error`——请求格式错误。请检查JSON请求数据。
- `500 Internal Server Error`——Cortex API出现故障。尝试重新请求一次，如果问题仍然存在，请切换回使用`memory_search`。
- 网络超时——无法连接到Cortex。此时请仅使用内置的内存系统，并通知用户。

如果Cortex无法使用，请**始终切换回`memory_search`。**切勿因Cortex API问题而阻碍用户的正常使用。

## 示例**

### “我加入了哪家公司？”
```bash
curl -s -X POST "$CORTEX_BASE_URL/v1/retrieve" \
  -H "x-api-key: $CORTEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "What company did the user join?", "query_type": "factual", "top_k": 5}' | jq '.results[] | {type, content, score}'
```

### “请记住我更喜欢PostgreSQL而不是MySQL”
```bash
curl -s -X POST "$CORTEX_BASE_URL/v1/ingest" \
  -H "x-api-key: $CORTEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "User prefers PostgreSQL over MySQL for all database projects.", "session_id": "openclaw:preferences"}' | jq '{facts: [.facts[].core], entities: [.entities[].name]}'
```

### “认证服务与API网关之间的关系是什么？”
```bash
curl -s -X POST "$CORTEX_BASE_URL/v1/retrieve" \
  -H "x-api-key: $CORTEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "How does the auth service relate to the API gateway?", "query_type": "factual", "top_k": 10}' | jq '.results[] | {type, content, score, metadata}'
```

## 安全性注意事项：
- **绝不要**在响应、日志或工具输出中显示`CORTEX_API_KEY`。
- **绝不要**将敏感的用户数据（如密码、令牌或凭证）包含在发送给Cortex的文本中。
- Cortex API采用了租户级别的数据库隔离机制——用户的数据不会被其他用户访问。