---
name: smart-memory
description: "通过本地的 FastAPI（地址：127.0.0.1:8000）实现持久的认知记忆功能。该系统支持语义搜索、带有重试队列的记忆存储机制以及后台数据检索功能。适用于需要回顾过去的决策、保存重要信息或分析模式规律的场景。"
metadata:
  {"openclaw":{"emoji":"🧠","requires":{"bins":["curl"]}}}
---
# 智能记忆系统

该系统位于 http://127.0.0.1:8000，提供长期存储功能，支持嵌入式数据存储、语义搜索、会话内容捕获以及后台认知处理。

## 使用场景

✅ **适用情况：**
- 回忆之前会议中做出的决策
- 查找与当前主题相关的内容
- 保存重要的决策或思路调整
- 从后台处理结果中获取模式洞察

❌ **不适用情况：**
- 当最近的对话内容已经足够时（使用对话上下文窗口）
- 服务器无法访问（curl 健康检查失败）

## 先决条件

```bash
# Check server health
curl -s http://127.0.0.1:8000/health | jq .

# Start server if needed
cd ~/.openclaw/workspace/smart-memory
. .venv/bin/activate
uvicorn server:app --host 127.0.0.1 --port 8000 &
```

## OpenClaw 配置

**注意：** OpenClaw 内置了 `memory_search` 和 `memory_get` 工具，这些工具使用 FTS（Full-Text Search）来搜索 MEMORY.md 文件。若要使用该系统的智能记忆功能，必须禁用这些内置工具：

```bash
# Disable built-in memory tools so skill tools take precedence
openclaw config set tools.deny '["memory_search", "memory_get"]'
openclaw gateway restart
```

重启后，该系统的 `memory_search` 功能将使用 Nomic 嵌入模型进行语义检索，而非 FTS 文件搜索。

## 搜索记忆

通过语义搜索和重新排序功能来查找相关记忆内容。

```bash
# Basic search
curl -s -X POST http://127.0.0.1:8000/retrieve \
  -H "Content-Type: application/json" \
  -d '{"user_message":"What did we decide about PyTorch?","limit":5}' | jq .

# Filter by memory type
curl -s -X POST http://127.0.0.1:8000/retrieve \
  -H "Content-Type: application/json" \
  -d '{"user_message":"database migration","type":"episodic","limit":3}' | jq .

# Higher relevance threshold
curl -s -X POST http://127.0.0.1:8000/retrieve \
  -H "Content-Type: application/json" \
  -d '{"user_message":"Tappy.Menu activation flow","min_relevance":0.7}' | jq .
```

## 保存记忆

将某个想法、事实或决策持久化。

```bash
# Semantic (factual knowledge)
curl -s -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "user_message":"We settled on CPU-only PyTorch for all installs.",
    "assistant_message":"Confirmed - avoids CUDA wheel bloat and keeps installs consistent.",
    "timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
  }' | jq .

# Episodic (session narrative)
curl -s -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "user_message":"Successfully deployed v2.5 skill architecture after 3 iterations.",
    "assistant_message":"Session captured with retry queue and hot memory integration.",
    "timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
  }' | jq .

# Goal (tracked objective)
curl -s -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "user_message":"GOAL: Complete Content Foundry MVP by end of March.",
    "assistant_message":"Tracking: lead capture → content gen → campaign workflows.",
    "timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
  }' | jq .
```

## 查看洞察结果

检查后台认知处理生成的模式。

```bash
# Pending insights
curl -s http://127.0.0.1:8000/insights/pending | jq .

# All memories
curl -s "http://127.0.0.1:8000/memories?limit=20" | jq '.[] | {id, type, content: .content[:50]}'

# Memory by ID
curl -s http://127.0.0.1:8000/memory/<id> | jq .
```

## 管理“热记忆”

检查和更新当前的对话上下文。

```bash
# View current hot memory
python3 ~/.openclaw/workspace/smart-memory/hot_memory_manager.py get

# Compose with hot memory context
python3 ~/.openclaw/workspace/smart-memory/memory_adapter.py compose -m "What should I prioritize?"

# Auto-update from conversation
~/.openclaw/workspace/smart-memory/smem-hook.sh "user message" "assistant response"

# Re-initialize hot memory
python3 ~/.openclaw/workspace/smart-memory/hot_memory_manager.py init
```

## 常用操作

### 查找项目中的最新决策
```bash
curl -s -X POST http://127.0.0.1:8000/retrieve \
  -H "Content-Type: application/json" \
  -d '{"user_message":"Tappy.Menu activation flow decision recent"}' | jq '.memories[] | {score, content}'
```

### 检查会话连续性
```bash
curl -s -X POST http://127.0.0.1:8000/retrieve \
  -H "Content-Type: application/json" \
  -d '{"user_message":"what we were building last session","type":"episodic"}' | jq '.memories[0].content'
```

### 捕获会话中的思路调整
```bash
CONTENT="Pivot: Moving from X approach to Y because of Z constraint"
curl -s -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d "{
    \"user_message\":\"$CONTENT\",
    \"assistant_message\":\"Important pivot captured.\",
    \"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
  }"
```

### 触发后台认知处理
```bash
curl -s -X POST http://127.0.0.1:8000/run_background -d '{"scheduled":false}' | jq .
```

## 其他说明

- **重试队列**：失败的操作会被记录到 `.memory_retry_queue.json` 文件中，并自动重试。
- **后台认知处理**：定期运行，以整合数据、消除冗余信息并生成新的洞察。
- **热记忆**：会话结束后仍会保留；系统会自动识别对话中的相关项目和问题。
- **会话记录**：会在检查点和会话结束时自动保存。
- **提示插入**：`[ACTIVE CONTEXT]` 标签会通过 `/compose` 功能自动包含当前的热记忆内容。

## 系统提示设置

将以下提示添加到代理的标识信息中：
> “如果与当前对话相关的洞察结果出现，请自然地展示给用户。”