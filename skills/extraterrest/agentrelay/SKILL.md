---
name: agentrelay
description: 一种可靠的代理间通信协议，用于通过共享文件传输大量数据（包括指针引用），并支持秘密代码验证。该协议通过消息中明确的“AgentRelay:”前缀来触发通信过程。
metadata: {"openclaw":{"triggerPatterns":["AgentRelay:","Please use AgentRelay skill to handle","Use AgentRelay"],"emoji":"📨"}}
---
# AgentRelay 📨

**可靠的代理间通信协议**——通过使用共享文件和短消息指针，解决大型数据传输时`sessions_send`超时问题。

## 🎯 何时使用此技能

当您看到以下类型的消息时，请立即使用此技能进行处理：

```
Please use AgentRelay skill to handle this message:
REQ,r1_r,s/r1_r.json,,
```

或

```
📨 AgentRelay Protocol Message

Please use AgentRelay skill to handle:
- Message Type: REQ
- Event ID: r1_r  
- File Pointer: s/r1_r.json
```

**关键触发短语**：
- “使用AgentRelay技能进行处理”
- “AgentRelay协议消息”
- “使用AgentRelay”

看到这些关键词时，请**立即执行以下命令**！

## 🚀 快速入门

### 收到AgentRelay消息后的标准流程

**步骤1：解析消息**
```bash
python3 {baseDir}/run_relay.py receive "REQ,r1_r,s/r1_r.json,,"
```

示例输出：
```json
{
  "type": "REQ",
  "event_id": "r1_r",
  "content": {"task": "write_poem", "sender_color": "red"},
  "secret": "ABC123"
}
```

**步骤2：理解任务并执行**

检查`content`字段以确定需要执行的具体操作（例如：写诗、分析数据、生成报告等）。

**步骤3：更新结果**
```bash
python3 {baseDir}/run_relay.py complete r1_r "Task completed" "agent:red:red"
```

**步骤4：发送CMP确认消息**
```bash
# generate CMP message (done automatically by run_relay.py complete)
# Output: CMP,r1_r,,,ABC123
# Then send via sessions_send
sessions_send(target='agent:red:red', message='CMP,r1_r,,,ABC123')
```

---

## 📚 命令

### `receive <csv_message>`

解析AgentRelay格式的CSV消息，并读取共享文件的内容。

**参数**：
- `csv_message`：CSV格式的消息（不包含`AgentRelay:`前缀）

**示例**：
```bash
python3 {baseDir}/run_relay.py receive "REQ,r1_r,s/r1_r.json,,"
```

**输出**（JSON格式）：
```json
{
  "type": "REQ",
  "event_id": "r1_r",
  "ptr": "s/r1_r.json",
  "content": {...},
  "secret": "ABC123"
}
```

---

### `update <event_id> <json_updates>`

更新共享文件的内容。

**参数**：
- `event_id`：事件ID
- `json_updates`：JSON格式的更新内容（合并到`payload.content`中）

**示例**：
```bash
python3 {baseDir}/scripts/handle_relay.py update r1_r '{"status":"completed","result":"done"}'
```

**输出**：
```json
{"status":"ok","file":"/path/to/r1_r.json","ptr":"s/r1_r.json"}
```

---

### `ack <event_id> <secret>`

生成ACK确认消息。

**参数**：
- `event_id`：事件ID
- `secret`：从文件中读取的密钥代码

**示例**：
```bash
python3 {baseDir}/scripts/handle_relay.py ack r1_r ABC123
```

**输出**：
```json
{
  "status": "ok",
  "ack_message": "ACK,r1_r,,,ABC123",
  "instruction": "Call sessions_send with message='ACK,r1_r,,,ABC123'"
}
```

---

## 🔄 完整的通信流程

### 发送代理
```python
# 1. Prepare data
content = {
    "task": "write_poem",
    "sender": "red",
    "receiver": "orange",
    "sender_color": "red",
    "receiver_color": "orange"
}

# 2. Write to shared file
from agentrelay.api import agentrelay_send
result = agentrelay_send("orange", "REQ", "r1_r", content)

# 3. Send message with prefix
message = f"AgentRelay: {result['csv_message']}"
sessions_send(target='agent:orange:main', message=message)
```

### 接收代理
```bash
# 1. Receive message: AgentRelay: REQ,r1_r,s/r1_r.json,,

# 2. Parse message
python3 {baseDir}/scripts/handle_relay.py receive "REQ,r1_r,s/r1_r.json,,"
# → Get content and secret

# 3. Understand task, call LLM to execute
# (This is your LLM capability)

# 4. Update result
python3 {baseDir}/scripts/handle_relay.py update r1_r '{"status":"completed"}'

# 5. Send ACK
ACK_OUTPUT=$(python3 {baseDir}/scripts/handle_relay.py ack r1_r SECRET)
ACK_MSG=$(echo "$ACK_OUTPUT" | jq -r '.ack_message')
sessions_send(target='agent:red:main', message="$ACK_MSG")
```

---

## 📊 消息格式详情

### CSV格式

**字段说明**：
- `TYPE`：消息类型（REQ | ACK | NACK | PING）
- `ID`：事件ID（唯一标识符）
- `PTR`：文件路径（例如：`s/event_id.json`）
- `RESERVED`：保留字段（留空）
- `DATA`：附加数据（ACK所需的密钥代码）

**示例**：
```
REQ,r1_r,s/r1_r.json,,          # Request
ACK,r1_r,,,ABC123               # Confirmation
NACK,r1_r,,,File not found      # Rejection
PING,test_1,,,,                 # Heartbeat test
```

### 完整的消息格式（包含前缀）

```
AgentRelay: REQ,r1_r,s/r1_r.json,,
```

**为什么需要前缀？**
- ✅ 明确标识这是AgentRelay协议的消息
- ✅ LLM（大型语言模型）在接收到此类消息时能立即知道需要调用AgentRelay技能
- ✅ 避免与其他消息混淆

---

## 🛡️ 安全机制

### 1. 密钥代码验证

- 发送方生成一个6位的随机代码（例如：`ABC123`）
- 将该密钥代码写入文件
- 接收方在发送ACK时必须返回相同的密钥代码
- 发送方验证密钥代码是否匹配，以确保接收方确实读取了文件内容

### 2. **读取后自动删除文件（可选）**

当设置`burn_on_read=true`时，文件会在读取后被自动删除，以保护敏感数据。

### 3. 完整性检查

文件内容包含SHA-256哈希值，以防止篡改。

---

## 📁 数据存储

- **共享文件**：`~/.openclaw/data/agentrelay/storage/*.json`
- **交易日志**：`~/.openclaw/data/agentrelay/logs/transactions_*.jsonl`
- **注册表**：`~/.openclaw/data/agentrelay/registry.json`

---

## 🧪 测试与示例

### Ping测试
```bash
python3 {baseDir}/scripts/ping_relay.py
```

### 5跳中继测试
```bash
python3 {baseDir}/examples/relay_5hops.py
```

### 10跳中继测试
```bash
python3 {baseDir}/examples/relay_10hops.py
```

---

## ❓ 常见问题解答

### Q：为什么使用AgentRelay而不是直接的`sessions_send`？

A：`sessions_send`在传输超过30个字符的消息时容易超时。AgentRelay通过使用共享文件和短路径（长度小于30个字符）来传输任意大小的数据。

### Q：密钥代码的作用是什么？

A：密钥代码是一个6位的随机代码，用于验证接收方是否确实读取了文件。接收方在发送ACK时必须返回正确的密钥代码。

### Q：文件保留时间是多少？

A：文件默认保留24小时。您可以通过`ttl_hours`参数进行调整，或者启用`burn_on_read`选项以在读取后立即删除文件。

---

## 📖 更多文档

- [README.md](https://github.com/your-repo/agentrelay/blob/main/README.md) - 项目概述
- [ARCHITECTURE.md](https://github.com/your-repo/agentrelay/blob/main/ARCHITECTURE.md) - 架构设计
- [API.md](https://github.com/your-repo/agentrelay/blob/main/API.md) - API参考
- [DEPLOYMENT.md](https://github.com/your-repo/agentrelay/blob/main/DEPLOYMENT.md) - 部署指南

---

**版本**：v1.0.1-alpha.3  
**最后更新时间**：2026-02-28  
**作者**：AgentRelay团队  
**维护者**：AgentRelay团队