---
name: openclaw-session-viewer
description: Generate interactive HTML viewer for OpenClaw conversation sessions. Use when: (1) reviewing conversation history, (2) analyzing context management, (3) debugging session logs, (4) visualizing tool calls and results, (5) understanding token usage. Triggers on "view session", "conversation viewer", "session history", "context viewer", "review this conversation".
---

# OpenClaw 会话查看器

该工具可生成一个交互式的 HTML 查看器，用于显示 OpenClaw 会话日志，其中包含完整的对话记录、工具调用结果以及相关数据。

## 快速入门

```bash
# Extract and view current session
python3 ~/.openclaw/skills/session-viewer/scripts/extract_session.py
open /tmp/session_viewer.html
```

## 命令

### 提取当前会话
```bash
python3 ~/.openclaw/skills/session-viewer/scripts/extract_session.py [--agent main] [--output /tmp/session_viewer.html]
```

### 按 ID 提取特定会话
```bash
python3 ~/.openclaw/skills/session-viewer/scripts/extract_session.py --session-id <uuid>
```

### 列出所有可用会话
```bash
python3 ~/.openclaw/skills/session-viewer/scripts/extract_session.py --list
```

## 查看内容

查看器包含以下部分：
- **侧边栏**：可搜索的所有对话记录
- **用户消息**：原始文本
- **助手回复**：文本内容及可折叠的思考过程
- **工具调用**：包含所有参数的 JSON 数据
- **工具结果**：包含状态码和输出结果的详细信息
- **统计信息**：令牌使用情况、成本、使用的模型等

## 会话日志存储位置

```
~/.openclaw/agents/<agentId>/sessions/
├── sessions.json          # Index: session keys → IDs
└── <session-id>.jsonl     # Conversation log
```

## 使用技巧

- 使用键盘导航键 ↑/↓ 或 j/k 来浏览对话记录
- 可在所有字段（消息、工具调用结果）中进行搜索
- 点击思考过程的标题可展开或折叠相关内容