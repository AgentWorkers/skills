---
name: local-first-llm
description: "该功能将大型语言模型（LLM）的请求首先路由到本地模型（如 Ollama、LM Studio 或 llamafile），只有在无法使用本地模型时才会回退到云 API。系统会在一个持久的仪表板中记录用户的代币节省情况以及成本节约效果。适用场景包括：  
1. 用户希望先使用本地模型执行任务；  
2. 用户希望降低云 API 使用成本或保护请求的隐私；  
3. 用户希望查看自己的代币节省情况或 LLM 请求路由的详细信息；  
4. 任何需要自动判断使用本地模型还是云模型的请求。  
目前支持 Ollama、LM Studio 和 llamafile 作为本地模型提供者。"
metadata: { "openclaw": { "emoji": "🏠", "requires": { "bins": ["python3"] }, "install": [] } }
---
# 本地优先的LLM（Local-First LLM）策略

首先将请求路由到本地的LLM（Large Language Model），只有在必要时才回退到云端。记录所有的决策过程，以展示实际的token节省情况和成本节约效果。

## 快速入门

### 1. 检查本地LLM是否正在运行

```bash
python3 skills/local-first-llm/scripts/check_local.py
```

返回JSON格式的结果：`{ "any_available": true, "best": { "provider": "ollama", "models": [...] } }`

### 2. 路由请求

```bash
python3 skills/local-first-llm/scripts/route_request.py \
  --prompt "Summarize this meeting transcript" \
  --tokens 800 \
  --local-available \
  --local-provider ollama
```

返回结果：`{ "decision": "local", "reason": "...", "complexity_score": -1 }`

### 3. 记录执行结果

在执行请求后，将其记录下来：

```bash
python3 skills/local-first-llm/scripts/track_savings.py log \
  --tokens 800 \
  --model gpt-4o \
  --routed-to local
```

### 4. 查看仪表盘

```bash
python3 skills/local-first-llm/scripts/dashboard.py
```

---

## 完整的路由工作流程

```
┌─────────────────────────────────────────────────────┐
│  1. check_local.py  →  is a local provider running? │
│                                                      │
│  2. route_request.py  →  local or cloud?             │
│     - sensitivity check  (private data → local)      │
│     - complexity score   (high score → cloud)        │
│     - availability gate  (no local → cloud)          │
│                                                      │
│  3. Execute with the chosen provider                 │
│                                                      │
│  4. track_savings.py log  →  record the outcome      │
│                                                      │
│  5. dashboard.py  →  show cumulative savings         │
└─────────────────────────────────────────────────────┘
```

---

## 路由规则（总结）

| 规则条件                                                         | 路由方式     |
| ----------------------------------------------------------------------------- | ---------- |
| 无法使用本地提供商                                                     | ☁️ 使用云端     |
| 提示中包含敏感信息（如`password`、`secret`、`api key`、`ssn`等）                          | 🏠 使用本地LLM |
| 复杂度评分 ≥ 3                                                       | ☁️ 使用云端     |
| 复杂度评分 < 3                                                       | 🏠 使用本地LLM |

有关详细的评分规则，请参阅 [references/routing-logic.md](references/routing-logic.md)。

---

## 使用本地提供商执行请求

当`route_request.py`返回`"decision": "local"`时，发送请求：

### 使用Ollama

```bash
curl http://localhost:11434/api/generate \
  -d '{"model": "llama3.2", "prompt": "YOUR_PROMPT", "stream": false}'
```

### 使用LM Studio或lamafile（兼容OpenAI）

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "local-model", "messages": [{"role": "user", "content": "YOUR_PROMPT"}]}'
```

---

## 仪表盘

仪表盘的数据来源于`~/.openclaw/local-first-llm/savings.json`文件（该文件会自动生成）。

```
┌─────────────────────────────────────────┐
│    🧠  Local-First LLM — Dashboard      │
├─────────────────────────────────────────┤
│  Local LLM:  ✅  ollama (llama3.2...)   │
├─────────────────────────────────────────┤
│  Total requests:         42             │
│  Routed locally:         31  (73.8%)    │
│  Routed to cloud:        11             │
├─────────────────────────────────────────┤
│  Tokens saved:       84,200             │
│  Cost saved:           $0.4210          │
└─────────────────────────────────────────┘
```

## 重置节省数据

```bash
python3 skills/local-first-llm/scripts/track_savings.py reset
```

---

## 额外参考资料

- **路由评分规则详情**：[references/routing-logic.md](references/routing-logic.md)
- **本地提供商设置**（Ollama、LM Studio、lamafile）：[references/local-providers.md](references/local-providers.md)
- **Token估算与云端成本表**：[references/token-estimation.md](references/token-estimation.md)