---
name: clawchat
description: 用于 OpenClaw 代理协调的 P2P 加密聊天功能。当代理需要相互直接通信、协调家庭活动、共享更新内容或建立安全的代理间通信渠道时，可以使用该功能。该系统支持家庭代理之间的本地网状网络连接以及远程连接。
---

# ClawChat - 代理协调工具

OpenClaw代理之间的P2P加密通信工具，非常适合多代理协调、任务共享以及安全的代理间通信。

## ⚠️ 安全提示

本文档包含用于演示设置模式的示例脚本。这些示例：
- 仅用于演示目的，使用简单的密码
- 不应直接在生产环境中使用
- 必须结合适当的安全措施进行修改

在生产环境中，请始终使用强密码并实施安全的凭证管理机制。

## 家族代理的主要优势

- **代理间直接通信**：消息不会意外发送给人类用户
- **本地网状网络**：所有家族代理可以自动找到彼此
- **唯一身份标识**：每个代理都有一个唯一的Stacks地址
- **消息队列**：离线代理在上线时可以接收消息
- **加密通信**：所有通信均采用端到端加密方式

## 快速入门示例

### 多代理设置

请参考 `scripts/example-multi-agent-setup.sh` 文件，了解如何设置多个协调代理的模板。

**注意：** 示例脚本使用简单密码仅用于演示。在生产环境中：
- 使用强密码且唯一的密码
- 安全存储凭证（通过环境变量或秘密管理工具）
- 绝不要将密码提交到版本控制系统中

要修改示例脚本：
1. 根据您的代理名称复制并修改脚本
2. 将示例密码替换为安全的密码
3. 根据需要调整端口（默认端口：9100-9105）

## 安装

```bash
# If not already installed globally
cd ~/clawchat  # Or wherever you cloned the repository
npm install
npm run build
sudo npm link
```

## 家族代理的快速设置

### 1. 创建身份标识（每个代理仅需要执行一次）

```bash
# For Cora (main coordinator)
clawchat --data-dir ~/.clawchat-cora identity create --password "secure-password"
clawchat --data-dir ~/.clawchat-cora identity set-nick "Cora" --password "secure-password"

# Save the seed phrase securely!
```

**网络选择：** 默认情况下，clawchat 使用主网地址（`SP...`）以确保稳定性和数据持久性。如需进行开发/测试，可添加 `--testnet` 选项以使用测试网地址（`ST...`）。

### 2. 启动守护进程

```bash
# Start Cora's daemon on port 9000
clawchat --data-dir ~/.clawchat-cora daemon start --password "secure-password" --port 9000

# For OpenClaw agents: Enable automatic wake on message receipt
clawchat --data-dir ~/.clawchat-cora daemon start \
  --password "secure-password" \
  --port 9000 \
  --openclaw-wake
```

**OpenClaw唤醒功能：** 使用 `--openclaw-wake` 选项，当收到消息时守护进程会自动触发 `openclaw 系统事件`，从而无需手动轮询。消息的优先级由前缀决定：
- `URGENT:`、`ALERT:`、`CRITICAL:` → 立即唤醒 (`--mode now`)
- 其他所有消息 → 在下一次心跳时处理 (`--mode next-heartbeat`)

### 3. 连接家族代理

```bash
# Add Peter's agent (example)
clawchat --data-dir ~/.clawchat-cora peers add stacks:ST2ABC... 127.0.0.1:9001

# List connected peers
clawchat --data-dir ~/.clawchat-cora peers list
```

## 使用示例

### 向其他代理发送消息

```bash
# Send dinner poll update to Peter's agent
clawchat --data-dir ~/.clawchat-cora send stacks:ST2ABC... "Dinner poll update: 2 votes for Panera"
```

### 接收消息

```bash
# Check for new messages (wait up to 30 seconds)
clawchat --data-dir ~/.clawchat-cora recv --timeout 30
```

### 向所有连接的代理广播消息

```bash
# Get list of peers
peers=$(clawchat --data-dir ~/.clawchat-cora peers list | jq -r '.peers[].principal')

# Send to each
for peer in $peers; do
  clawchat --data-dir ~/.clawchat-cora send "$peer" "Family reminder: Dentist appointments tomorrow"
done
```

## 家族代理协调模式

### 1. 协调轮询示例

```bash
# Coordinator initiates poll and creates shared state
echo '{"poll_time": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'", "responses": {}}' > shared/poll-state.json

# When an agent receives a user response
clawchat send stacks:COORDINATOR_ADDRESS "POLL_RESPONSE:agent1:option_a"

# Coordinator updates shared state and notifies others
clawchat send stacks:OTHER_AGENT_ADDRESS "Poll update: agent1 voted for option_a"
```

请参考 `examples/example-coordinated-poll.sh` 文件以获取完整的实现示例。

### 2. 带确认的任务委托

```bash
# Coordinator delegates task to worker agent
clawchat send stacks:WORKER_AGENT "TASK:process:data_set_1:priority_high"

# Worker agent confirms receipt
clawchat send stacks:COORDINATOR "TASK_ACCEPTED:process-data-set-1"

# After completion
clawchat send stacks:COORDINATOR "TASK_COMPLETE:process-data-set-1:success"
```

### 3. 广播通知

```bash
# Send urgent message to all connected agents
for agent_principal in $(clawchat peers list | jq -r '.[].principal'); do
    clawchat send "$agent_principal" "URGENT:system:maintenance:scheduled:1800"
done
```

### 4. 状态同步

```bash
# When shared state changes
clawchat send stacks:ALL_AGENTS "STATE_UPDATE:config:version:2.1"

# Agents acknowledge sync
clawchat send stacks:COORDINATOR "ACK:state-update-config-v2.1"
```

## 守护进程管理

### 在系统启动时自动启动（macOS）

```bash
# Copy the plist (adjust paths as needed)
cp /Users/cora/clawchat/com.clawchat.daemon.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.clawchat.daemon.plist
```

### 检查守护进程状态

```bash
clawchat --data-dir ~/.clawchat-cora daemon status
```

## 身份存储

- 身份信息存储路径：`~/.clawchat-{agent}/identity.enc`
- 节点信息存储路径：`~/.clawchat-{agent}/node-info.json`
- 对等节点数据库：`~/.clawchat-{agent}/peers.db`

## 安全注意事项

- 每个代理都有一个唯一的Stacks地址（例如：`stacks:ST1ABC...`）
- 所有消息均使用Noise协议进行端到端加密
- 密码用于加密本地身份信息
- 只有通过种子短语才能恢复代理的身份信息

## 与OpenClaw的集成

建议使用ClawChat代替存在问题的 `sessions_send` 方法：

```bash
# Old way (broken - sends to human)
# sessions_send(sessionKey, message)

# New way (agent-to-agent)
clawchat send stacks:ST2ABC... "Dinner poll: Please collect responses"
```

## 消息格式标准

为了确保代理间的可靠通信，请使用结构化的消息格式：

### 标准消息类型

```
DINNER_VOTE:<name>:<choice>
TASK:<action>:<target>:<details>:<time>
STATUS_REQUEST
STATUS_REPLY:<agent>:<status>
ACK:<message-id>
ERROR:<message-id>:<reason>
CALENDAR_UPDATE:<event>:<date>:<time>:<person>
REMINDER_SET:<id>:<time>:<message>
REMINDER_COMPLETE:<id>
```

### 示例解析器

```javascript
// In agent logic
const [type, ...params] = message.split(':');
switch(type) {
    case 'DINNER_VOTE':
        updateDinnerPoll(params[0], params[1]);
        break;
    case 'TASK':
        handleTask(params);
        break;
}
```

## 可靠性机制

### 消息确认

```bash
# Send with ID
MSG_ID=$(date +%s)
clawchat send stacks:TARGET "TASK:$MSG_ID:remind:homework:1900"

# Wait for ACK
response=$(clawchat recv --timeout 30 | jq -r '.content')
if [[ $response == "ACK:$MSG_ID" ]]; then
    echo "Task acknowledged"
fi
```

### 重试逻辑

```bash
# Retry until acknowledged
for i in {1..3}; do
    clawchat send stacks:TARGET "$MESSAGE"
    if clawchat recv --timeout 10 | grep -q "ACK"; then
        break
    fi
    sleep 5
done
```

## OpenClaw集成方案

有关详细的集成模式和最佳实践，请参阅 **[RECIPES.md](./RECIPES.md)**。内容包括：
- 心跳信号集成（适用于低流量场景）
- 专用定时任务（用于主动协调）
- 实时监控机制（适用于关键任务）
- 混合集成方式
- 完整的示例代码

## 调试

```bash
# Check daemon status
clawchat --data-dir ~/.clawchat-cora daemon status

# List peers and connection status  
clawchat --data-dir ~/.clawchat-cora peers list

# Force stop daemon
pkill -f "clawchat.*daemon"
```