---
name: agentrelay
description: 一种可靠的代理间通信协议，用于通过共享文件传输大量数据（这些文件包含指针引用），并支持秘密代码验证。该协议通过消息中明确的“AgentRelay:”前缀来触发通信过程。
metadata: {"openclaw":{"triggerPatterns":["AgentRelay:","Please use AgentRelay skill to handle","Use AgentRelay"],"emoji":"📨"}}
---
# AgentRelay 📨

**可靠的代理间通信协议**——通过使用共享文件和短消息指针，解决传输大容量数据时`sessions_send`超时问题。

## 🎯 何时使用此技能

当您看到以下类型的消息时，请立即使用此技能进行处理：

```
Please use AgentRelay skill to handle this message:
REQ,event_001,s/event_001.json,,
```

或

```
📨 AgentRelay Protocol Message

Please use AgentRelay skill to handle:
- Message Type: REQ
- Event ID: event_001
- File Pointer: s/event_001.json
```

**关键触发语句**：
- “使用AgentRelay技能进行处理”
- “AgentRelay协议消息”
- “使用AgentRelay”

遇到这些关键词时，请**立即执行以下命令**！

## 🚀 快速入门

### 收到AgentRelay消息后的标准流程

**步骤1：解析消息**
```bash
python3 {baseDir}/run_relay.py receive "REQ,event_001,s/event_001.json,,"
```

示例输出：
```json
{
  "type": "REQ",
  "event_id": "event_001",
  "content": {
    "task": "write_poem",
    "sender_agent": "agent:sender:main",
    "receiver_agent": "agent:worker:main"
  },
  "secret": "ABC123"
}
```

**步骤2：理解任务并执行**

检查`content`字段以确定需要执行的具体操作（例如：写诗、分析数据、生成报告等）。

**步骤3：更新结果**
```bash
python3 {baseDir}/run_relay.py complete event_001 "Task completed" "agent:sender:main"
```

**步骤4：发送CMP确认消息**
```bash
# generate CMP message (done automatically by run_relay.py complete)
# Output: CMP,event_001,,,ABC123
# Then send via sessions_send
sessions_send(target='agent:sender:main', message='CMP,event_001,,,ABC123')
```

---

## 📚 命令

### `receive <csv_message>`

解析AgentRelay格式的CSV消息，并读取共享文件的内容。
该命令接受纯CSV格式的消息，或带有`AgentRelay:`前缀的完整消息。

**参数**：
- `csv_message`：CSV格式的消息（不包含`AgentRelay:`前缀）

**示例**：
```bash
python3 {baseDir}/run_relay.py receive "REQ,event_001,s/event_001.json,,"
```

**输出**（JSON格式）：
```json
{
  "type": "REQ",
  "event_id": "event_001",
  "ptr": "s/event_001.json",
  "content": {...},
  "secret": "ABC123"
}
```

---

### `update <event_id> <json_updates> [next_event_id]`

更新共享文件的内容。

**参数**：
- `event_id`：事件ID
- `json_updates`：以JSON格式提供的更新内容（合并到`payload.content`中）

**示例**：
```bash
python3 {baseDir}/run_relay.py update event_001 '{"status":"completed","result":"done"}'
```

**输出**：
```json
{"status":"ok","file":"/path/to/event_001.json","ptr":"s/event_001.json"}
```

---

### `cmp <event_id> [secret]`

生成CMP确认消息。

**参数**：
- `event_id`：事件ID
- `secret`：从文件中读取的密钥代码

**示例**：
```bash
python3 {baseDir}/run_relay.py cmp event_001 ABC123
```

**输出**：
```json
{
  "status": "ok",
  "cmp_message": "CMP,event_001,,,ABC123",
  "instruction": "Call sessions_send with message='CMP,event_001,,,ABC123'"
}
```

---

### `verify <cmp_message>`

验证接收到的`CMP`消息是否与事件文件中存储的密钥代码匹配。

**示例**：
```bash
python3 {baseDir}/run_relay.py verify "CMP,event_001,,,ABC123"
```

**输出**：
```json
{
  "status": "ok",
  "event_id": "event_001",
  "verified": true
}
```

---

## 🔄 完整的通信流程

### 发送代理

```python
# 1. Prepare data
content = {
    "task": "write_poem",
    "sender_agent": "agent:sender:main",
    "receiver_agent": "agent:worker:main"
}

# 2. Write to shared file
from agentrelay import agentrelay_send
result = agentrelay_send("agent:worker:main", "REQ", "event_001", content)

# 3. Send message with prefix
message = f"AgentRelay: {result['csv_message']}"
sessions_send(target='agent:worker:main', message=message)
```

### 接收代理

```bash
# 1. Receive message: AgentRelay: REQ,event_001,s/event_001.json,,

# 2. Parse message
python3 {baseDir}/run_relay.py receive "REQ,event_001,s/event_001.json,,"
# → Get content and secret

# 3. Understand task, call LLM to execute
# (This is your LLM capability)

# 4. Update result
python3 {baseDir}/run_relay.py update event_001 '{"status":"completed"}'

# 5. Send CMP
CMP_OUTPUT=$(python3 {baseDir}/run_relay.py cmp event_001 SECRET)
CMP_MSG=$(echo "$CMP_OUTPUT" | jq -r '.cmp_message')
sessions_send(target='agent:sender:main', message="$CMP_MSG")
```

---

## 📊 消息格式详情

### CSV格式

**字段说明**：
- `TYPE`：消息类型（REQ | CMP）
- `ID`：事件ID（唯一标识符）
- `PTR`：文件指针（例如：`s/event_id.json`）
- `RESERVED`：保留字段（留空）
- `DATA`：附加数据（用于CMP的密钥代码）

**示例**：
```
REQ,event_001,s/event_001.json,,  # Request
CMP,event_001,,,ABC123            # Completion confirmation
```

### 带前缀的完整消息格式**

**为什么需要前缀？**
- ✅ 明确标识这是AgentRelay协议消息
- ✅ LLM（Large Language Model）在接收到此类消息时能立即知道需要调用AgentRelay技能
- ✅ 避免与其他消息混淆

---

## 🛡️ 安全机制

### 1. 密钥代码验证

- 发送方生成一个6位的随机代码（例如：`ABC123`）
- 将该密钥代码写入文件
- 接收方在发送CMP消息时必须返回相同的密钥代码
- 发送方通过验证密钥代码来确认接收方确实读取了文件内容

### 2. 自动删除文件（可选）

当`meta`或`payload.content`中设置`burn_on_read=true`时，文件会在读取后自动被删除，以保护敏感数据。

## 📁 数据存储

- **共享文件**：`~/.openclaw/data/agentrelay/storage/*.json`
- **交易日志**：`~/.openclaw/data/agentrelay/logs/transactions_*.jsonl`
- **注册表**：`~/.openclaw/data/agentrelay/registry.json`

---

## 🧪 测试与示例

### 简单测试
```bash
python3 {baseDir}/smoke_test.py
```

### Pytest回归测试套件
```bash
pytest {baseDir}/test_agentrelay.py
```

### 清理过期事件
```bash
python3 {baseDir}/cleanup_relay.py
```

### 验证CMP消息
```bash
python3 {baseDir}/run_relay.py verify "CMP,r1_r,,,ABC123"
```

---

## ❓ 常见问题解答

### 问：为什么使用AgentRelay而不是直接使用`sessions_send`？

答：`sessions_send`在传输超过30个字符的消息时容易超时。AgentRelay通过使用共享文件和短路径（长度小于30个字符）来传输任意大小的数据。

### 问：密钥代码的作用是什么？

答：密钥代码是一个6位的随机代码，用于验证接收方是否确实读取了文件内容。接收方需要在CMP消息中返回正确的密钥代码，发送方可以通过`verify`命令进行验证。

### 问：文件会保留多久？

答：文件默认保留24小时。您可以通过`ttl_hours`参数调整保留时间，或者启用`burn_on_read`选项在读取后立即删除文件，还可以运行`cleanup_relay.py`来清理过期的文件和旧的注册表条目。

---

## 📖 更多文档

- [README.md](/Users/gavinliu/.openclaw/workspace/skills/agentrelay/README.md) - 项目概述
- [RELEASE_NOTES.md](/Users/gavinliu/.openclaw/workspace/skills/agentrelay/RELEASE_NOTES.md) - 发布说明

---

**版本**：v1.1.0  
**最后更新时间**：2026-02-28  
**作者**：AgentRelay团队  
**维护者**：AgentRelay团队