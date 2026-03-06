---
name: idleclaw
description: 您可以将自己闲置的 Ollama 推理资源分享给社区；当您的 API 信用额度用完时，也可以使用社区提供的推理资源。
  inference when your API credits run out.
tools: Bash, Read
metadata: {"clawdbot":{"emoji":"🦀","os":["darwin","linux"],"requires":{"bins":["python3","ollama"]}}}
---
# IdleClaw

这是一个用于Ollama的分布式推理网络。贡献者可以共享他们闲置的GPU/CPU资源，而消费者在API信用耗尽时可以使用社区的计算资源。

## 模式

### 贡献 — 共享你的闲置计算资源

将你的机器作为推理节点运行。你的本地Ollama模型将可供社区使用。

```bash
cd "$SKILL_DIR" && python scripts/contribute.py
```

此操作会连接到IdleClaw路由服务器，注册你的可用模型，并开始接收推理请求。按Ctrl+C即可停止。

**要求：** Ollama必须至少运行一个模型。

### 消费 — 使用社区的计算资源

向社区网络发送聊天请求，而不是在本地运行模型。

```bash
cd "$SKILL_DIR" && python scripts/consume.py --model <model-name> --prompt "<your message>"
```

当有新的聊天消息时，会将响应内容输出到标准输出（stdout）。

### 状态 — 检查网络健康状况

查看有多少节点在线以及有哪些模型可用。

```bash
cd "$SKILL_DIR" && python scripts/status.py
```

## 配置

| 变量 | 默认值 | 描述 |
|---|---|---|
| `IDLECLAW_SERVER` | `https://api.idleclaw.com` | 路由服务器URL |
| `OLLAMA_HOST` | `http://localhost:11434` | 本地Ollama端点 |

## 安全性

### 外部端点

该工具会连接到以下外部端点：

1. **IdleClaw路由服务器** (`IDLECLAW_SERVER`, 默认 `https://api.idleclaw.com`)
   - **贡献模式**：建立WebSocket连接以注册为推理节点。发送：节点ID、可用模型名称以及推理响应令牌。接收：推理请求（模型名称 + 消费者的聊天消息）。
   - **消费模式**：向`/api/chat`发送HTTP POST请求，包含模型名称和聊天消息。接收：通过SSE传输的响应令牌。
   - **状态模式**：向`/health`和`/api/models`发送HTTP GET请求。接收：服务器健康状况信息和可用模型列表。

2. **本地Ollama** (`OLLAMA_HOST`, 默认 `http://localhost:11434`)
   - **仅限贡献模式**：调用Ollama的API来列出模型并执行推理。所有通信都在本地主机上进行。

### 数据处理

- **用户数据** 在活动会话结束后不会被本地或服务器保留。
- **不需要也不存储任何凭证或API密钥**。
- **仅支持文本聊天** — 不支持文件上传、代码执行或系统访问。网络中仅传输聊天消息（文本字符串）。
- **聊天消息** 从消费者节点传输到服务器，再由服务器发送给贡献者节点进行处理，处理完成后会被丢弃。
- **不收集任何遥测数据或分析信息**。
- 在贡献模式下，路由服务器会将聊天消息发送到你的Ollama实例，并将处理后的文本响应返回给贡献者。贡献者可以将`IDLECLAW_SERVER`指向自托管的Ollama实例。
- 在消费模式下，文本提示会被发送到路由服务器，然后由路由服务器分配给可用的贡献者节点。

### 数据清洗

**客户端：**
- 模型名称需符合严格的格式要求（仅允许字母数字、冒号和句点）。
- 使用前会验证服务器URL是否为有效的HTTP/HTTPS地址。
- 不会根据用户输入构建shell命令 — 所有操作均由Python程序完成。
- 不会读取或访问任何本地文件 — 该工具仅与Ollama和路由服务器进行通信。

**服务器端（路由服务器）：**
- 对所有端点实施基于IP的速率限制：聊天请求（每分钟20次），节点注册请求（每分钟5次），其他请求（每分钟60次）。
- 输入验证：每次请求最多50条消息，每条消息最多10,000个字符，模型名称最多64个字符，角色限制为`user`和`assistant`。
- 输出清洗：在将响应内容发送给消费者之前会去除标记标签。
- 节点注册限制：每个IP地址最多注册3个节点，同时进行的请求数量被限制在1-10次之间。
- 执行安全措施：包括模式验证、参数类型检查、15秒超时机制以及每节点的请求速率限制（每分钟20次）。
- 服务器仅绑定到本地主机，并通过Caddy反向代理进行访问，支持自动TLS加密。
- 已经过安全评估（[GitHub上的安全评估报告](https://github.com/futurejunk/idleclaw/tree/main/security)）。

## 安装

运行安装程序以设置Python依赖项：

```bash
cd "$SKILL_DIR" && bash install.sh
```