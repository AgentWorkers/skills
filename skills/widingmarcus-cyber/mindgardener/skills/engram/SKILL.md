---
name: engram
description: "具有知识图谱和基于“惊喜”机制的持久化存储层：能够从 Markdown 文件中提取实体信息、生成维基页面、评估预测错误率以及恢复上下文内容。"
homepage: https://github.com/maweding/agent-engram
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"],"pip":["agent-engram"]}}}
---
# Engram — 代理记忆系统

为你的代理提供一个能够在会话之间持续保存数据的“大脑”。无需数据库或服务器，只需使用 Markdown 文件即可。

## 设置

```bash
pip install agent-engram
```

在 `engram.yaml`（工作区根目录）中进行配置：
```yaml
workspace: .
provider: gemini          # or openai, anthropic, ollama, compatible
model: gemini-2.0-flash   # any model your provider supports
```

设置你的 API 密钥：
```bash
export GEMINI_API_KEY=...   # or OPENAI_API_KEY, ANTHROPIC_API_KEY
```

对于本地模型（免费使用）：
```yaml
provider: ollama
model: llama3.2
```

## 日常工作流程

### 每次会话结束后 — 提取发生的事情：
```bash
engram extract                          # Process today's daily log
engram extract --date 2026-02-16        # Process specific date
engram extract --all                    # Process all unprocessed dates
```

这些信息会被保存到 `memory/entities/` 目录中形成实体页面，并被保存到 `memory/graph.jsonl` 文件中形成实体关系三元组。

### 查询已知信息：
```bash
engram recall "Kadoa"                   # Entity page + graph neighbors
engram recall "peter"                   # Fuzzy match → Peter Steinberger
engram entities                         # List all known entities
```

### 今天有什么令人惊讶的事情？
```bash
engram surprise                         # Prediction error scoring
engram surprise --date 2026-02-16       # Score specific date
```

### 输出结果：
```
🔴 [0.8] Repo renamed to openclaw/openclaw
🟡 [0.7] HOT BUG: Session Path Regression
🟢 [0.2] Routine PR work
📉 Learning rate: 0.60
```

### 夜间处理 — 将信息巩固到长期记忆中：
```bash
engram consolidate                      # Promote high-surprise events to MEMORY.md
```

### 维护：
```bash
engram decay --dry-run                  # Show stale entities
engram decay --execute                  # Archive entities not referenced in 30+ days
engram merge --detect                   # Find duplicate entities
engram merge "steipete" "Peter Steinberger"  # Merge two entities
engram viz                              # Render knowledge graph (Mermaid)
engram stats                            # Memory statistics
```

## 工作原理

1. **数据提取** — 大语言模型（LLM）读取每日生成的 Markdown 日志，提取实体、关系和事件信息。
2. **事件识别** — 采用两阶段预测机制：预测可能发生的情况 → 与实际发生的情况进行比较 → 计算差异（即“惊讶度”）。
3. **信息巩固** — 只有那些具有高“惊讶度”的事件才会被保存到 `MEMORY.md` 文件中（即完成“夜间巩固”过程）。
4. **数据淘汰** — 30 天后未被引用的实体会被自动归档，而活跃的实体则会得到强化。

## 推荐的 Cron 任务设置

每晚运行完整的“夜间巩固”流程：
```bash
# In your agent's cron (e.g., 03:00 daily):
engram extract && engram surprise && engram consolidate && engram decay --execute
```

或者使用 Clawdbot 的 Cron 任务：
```json
{"name": "engram-nightly", "schedule": {"kind": "cron", "expr": "0 3 * * *"}, "payload": {"kind": "systemEvent", "text": "Run nightly engram cycle: engram extract && engram surprise && engram consolidate"}}
```

## 多代理设置

多个代理可以共享同一个知识图谱：
```bash
# Shared entities directory (symlink from each agent's workspace)
ln -s /shared/memory/entities /agent-a/memory/entities
ln -s /shared/memory/entities /agent-b/memory/entities
```

每个代理都会向共享的知识图谱中写入数据，从而汇总所有代理的知识信息。

## 文件结构

```
memory/
├── 2026-02-17.md           # Daily log (you write this)
├── entities/               # Auto-generated wiki pages
│   ├── Kadoa.md
│   ├── OpenClaw.md
│   └── Peter-Steinberger.md
├── graph.jsonl             # Knowledge graph triplets
├── prediction-errors.jsonl # PE scores history
└── surprise-scores.jsonl   # Surprise history
```

## 使用技巧

- 实体页面使用纯 Markdown 格式编写；如果 LLM 生成了错误信息，可以手动进行编辑。
- 在每日日志中使用 `[[wikilinks]]` 标签来辅助数据提取。
- 可以使用 `jq` 命令查询 `graph.jsonl` 文件：`jq 'select(.object == "Kadoa")' memory/graph.jsonl`
- 通过 Git 对 `memory/` 目录进行版本控制，以记录所有更改历史。