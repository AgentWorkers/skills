---
name: session-history
description: 搜索并浏览所有会话中的历史对话记录。适用于回顾之前的工作内容、查找旧的讨论内容、重新启动已中断的对话，或者在用户需要回忆之前讨论过的信息（但这些信息并未保存在内存文件中）时使用。此外，当被要求“记住”之前讨论过的内容、查找关于某个特定主题的对话，或从之前的会话中继续工作时，也可以使用该功能。
---
# 会话历史记录

您可以搜索过去的 OpenClaw 会话记录（这些记录存储在 `~/.openclaw/agents/*/sessions/` 目录下的 JSONL 文件中）。

## 快速参考

```bash
# Search for conversations about a topic
python3 scripts/search_sessions.py "gclid pipeline error"

# List recent sessions
python3 scripts/search_sessions.py --list --days 3

# Search specific agent's history
python3 scripts/search_sessions.py "flight monitor" --agent main

# Wider time range
python3 scripts/search_sessions.py "quantum encryption" --days 30 --max-results 5
```

## 工作流程

1. 使用用户的查询词运行 `search_sessions.py` 脚本来查找相关的会话记录。
2. 使用 `sessions_history` 工具和 `sessionKey` 来获取匹配到的会话的完整上下文信息。
3. 如果 `sessions_history` 无法使用（例如会话已关闭或过旧），则直接使用 `read` 命令读取对应的 JSONL 文件。
4. 对搜索结果进行总结，而不是直接输出原始的会话记录内容。

## 适用场景

- 当用户询问“我们之前讨论过 X 的内容吗？”或“我们上周讨论过 Y 吗？”时。
- 当需要恢复未保存在内存文件中的讨论内容时。
- 当需要查找过去会话中的决策、代码片段或错误信息时。
- 当需要对比会话记录与 `MEMORY.md` 文件中的内容时。

## 提示

- 也可以先尝试使用 `memory_search` 工具——它也会对会话记录进行索引。
- 可以结合使用这两个工具：`memory_search` 用于语义匹配，`search_sessions.py` 用于关键词或精确匹配。
- 该脚本会同时搜索用户和助手发送的消息。
- JSONL 文件的路径格式为：`~/.openclaw/agents/{agent_id}/sessions/{session_uuid}.jsonl`