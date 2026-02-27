---
name: self-prompt
description: Force agent responses to scheduled/automated messages. Use when cron jobs, monitoring scripts, or automated systems send messages that agents ignore. Solves the problem where agents treat system-sent messages as "background info" instead of tasks requiring response. Key pattern: use `openclaw agent` instead of `openclaw message send` to trigger actual agent turns.
---

# 自动提示：强制代理响应

## 问题

当自动化脚本（如cron任务、监控脚本）通过 `openclaw message send` 发送消息时：
- 这些消息会显示在聊天界面中，被归类为“系统消息”
- 代理可能会将这些消息视为后台信息，而不会视为需要处理的任务
- 代理会响应用户的消息，但会忽略自动发送的消息
- 由此导致责任检查、警报和任务无法得到及时处理

## 解决方案

对于需要代理响应的消息，应使用 `openclaw agent` 而不是 `openclaw message send`：

```bash
# OLD (agent may ignore):
openclaw message send --target -GROUP_ID --message "TASK: Do something"

# NEW (agent MUST respond):
RESPONSE=$(openclaw agent \
    --agent AGENT_ID \
    --session-id "agent:AGENT_ID:telegram:group:GROUP_ID" \
    --channel telegram \
    --message "TASK: Do something" \
    --timeout 180)

# Send response to chat:
openclaw message send --target -GROUP_ID --message "$RESPONSE"
```

## 原因

- `openclaw message send` 仅用于创建聊天消息，代理会将其视为普通通知；
- `openclaw agent` 会触发代理的实际处理流程，代理必须对消息进行处理并作出响应。

## 快速入门

### 对于 Bash 脚本

使用 `scripts/send_agent_task.sh`：

```bash
# Simple usage:
~/.openclaw/skills/self-prompt/scripts/send_agent_task.sh \
    "AGENT_ID" \
    "GROUP_ID" \
    "Your task message here"
```

### 对于 Python 脚本

使用 `scripts/send_agent_task.py`：

```python
from send_agent_task import send_and_deliver

success, response = send_and_deliver(
    agent_id="stock-trading",
    group_id="-5283045656", 
    message="TASK: Analyze current positions",
    timeout=180
)
```

## 数据与任务的分离

对于监控脚本，应将数据传输与任务请求分开处理：

```bash
# 1. Send DATA immediately (informational)
openclaw message send --target "$GROUP_ID" --message "📊 Position Data:
$POSITIONS"

# 2. Send TASK via agent (forces response)
RESPONSE=$(openclaw agent \
    --agent "$AGENT_ID" \
    --session-id "agent:$AGENT_ID:telegram:group:$GROUP_ID" \
    --message "Analyze the data above and report findings" \
    --timeout 180)

# 3. Deliver response
openclaw message send --target "$GROUP_ID" --message "📊 Analysis:
$RESPONSE"
```

## 常见使用场景

- **责任检查**  
- **监控警报**  
- **定时研究任务**  

## 会话密钥格式

会话密钥的格式如下：
```
agent:AGENT_ID:CHANNEL:TYPE:TARGET
```

示例：
- `agent:stock-trading:telegram:group:-5283045656`
- `agent:main:telegram:direct:123456789`
- `agent:assistant:discord:channel:987654321`

## 脚本参考

### `send_agent_task.sh`
位置：`scripts/send_agent_task.sh`

- 通过 `openclaw agent` 发送任务请求
- 捕获代理的响应
- 将代理的响应通过 `message send` 发送到指定群组
- 将日志记录到 `~/agent_task.log` 文件中

### `send_agent_task.py`
位置：`scripts/send_agent_task.py`

## 故障排除

- **代理未响应**：
  - 确认代理正在运行：使用 `openclaw gateway status` 命令检查
  - 检查会话密钥格式是否与代理/群组匹配
  - 对于耗时较长的任务，增加超时时间

- **响应未显示在聊天界面**：
  - 确保脚本在捕获代理响应后通过 `message send` 将其发送到聊天界面
  - 检查 `GROUP_ID` 是否正确（群组对应的 ID）
  - 确认使用的通信渠道（如 Telegram、Discord 等）是否正确

- **超时错误**：
  - 对于研究或分析任务，增加超时时间（建议设置为 300–600 秒）
  - 检查代理是否因同时处理过多请求而无法响应