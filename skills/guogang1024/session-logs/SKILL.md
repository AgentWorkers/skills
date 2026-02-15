---
name: session-logs
description: 使用 `jq` 来搜索和分析您自己的会话日志（旧的/父级对话）。
metadata: {"openclaw":{"emoji":"📜","requires":{"bins":["jq","rg"]}}}
---

# 会话日志

您可以搜索存储在会话 JSONL 文件中的完整对话历史记录。当用户提及之前的对话或询问之前说了什么内容时，可以使用此功能。

## 触发条件

当用户询问之前的聊天记录、父对话或系统中未保存的历史上下文时，可以使用此功能。

## 存储位置

会话日志存储在以下路径：`~/.clawdbot/agents/<agentId>/sessions/`（请使用系统提示中的 `agent=<id>` 值）：

- **`sessions.json`**：用于将会话键映射到会话 ID 的索引文件
- **`<session-id>.jsonl`**：每个会话的完整对话记录

## 文件结构

每个 `.jsonl` 文件包含以下内容：
- `type`：`session`（元数据）或 `message`
- `timestamp`：ISO 时间戳
- `message.role`：`user`（用户）、`assistant`（助手）或 `toolResult`（工具结果）
- `message.content[]`：文本、思考过程或工具调用（使用 `type=="text"` 过滤器可获取人类可读的内容）
- `message_usage.cost.total`：每次响应所消耗的成本

## 常见查询操作

### 按日期和文件大小列出所有会话
```bash
for f in ~/.clawdbot/agents/<agentId>/sessions/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  size=$(ls -lh "$f" | awk '{print $5}')
  echo "$date $size $(basename $f)"
done | sort -r
```

### 查找特定日期的会话
```bash
for f in ~/.clawdbot/agents/<agentId>/sessions/*.jsonl; do
  head -1 "$f" | jq -r '.timestamp' | grep -q "2026-01-06" && echo "$f"
done
```

### 从会话中提取用户消息
```bash
jq -r 'select(.message.role == "user") | .message.content[]? | select(.type == "text") | .text' <session>.jsonl
```

### 在助手的回复中搜索关键词
```bash
jq -r 'select(.message.role == "assistant") | .message.content[]? | select(.type == "text") | .text' <session>.jsonl | rg -i "keyword"
```

### 获取某个会话的总成本
```bash
jq -s '[.[] | .message.usage.cost.total // 0] | add' <session>.jsonl
```

### 日成本汇总
```bash
for f in ~/.clawdbot/agents/<agentId>/sessions/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  cost=$(jq -s '[.[] | .message.usage.cost.total // 0] | add' "$f")
  echo "$date $cost"
done | awk '{a[$1]+=$2} END {for(d in a) print d, "$"a[d]}' | sort -r
```

### 统计会话中的消息数量和token数量
```bash
jq -s '{
  messages: length,
  user: [.[] | select(.message.role == "user")] | length,
  assistant: [.[] | select(.message.role == "assistant")] | length,
  first: .[0].timestamp,
  last: .[-1].timestamp
}' <session>.jsonl
```

### 分析工具的使用情况
```bash
jq -r '.message.content[]? | select(.type == "toolCall") | .name' <session>.jsonl | sort | uniq -c | sort -rn
```

### 在所有会话中搜索某个短语
```bash
rg -l "phrase" ~/.clawdbot/agents/<agentId>/sessions/*.jsonl
```

## 使用提示

- 会话数据采用只允许追加的 JSONL 格式（每行一个 JSON 对象）
- 大型会话文件可能占用数 MB 的存储空间，可以使用 `head`/`tail` 命令进行样本查看
- `sessions.json` 索引文件将不同的聊天平台（如 Discord、WhatsApp 等）与对应的会话 ID 关联起来
- 被删除的会话文件会带有 `.deleted.<timestamp>` 的后缀

## 快速获取纯文本信息（低噪音提示）
```bash
jq -r 'select(.type=="message") | .message.content[]? | select(.type=="text") | .text' ~/.clawdbot/agents/<agentId>/sessions/<id>.jsonl | rg 'keyword'
```