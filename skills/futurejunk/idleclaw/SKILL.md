---
name: idleclaw
description: 您可以将闲置的 Ollama 推理资源分享给社区；当您的 API 信用额度用完时，也可以使用社区提供的推理资源。
  inference when your API credits run out.
tools: Bash, Read
metadata: {"clawdbot":{"emoji":"🦀","os":["darwin","linux"],"requires":{"bins":["python3","ollama"]}}}
---
# IdleClaw

这是一个用于Ollama的分布式推理网络。贡献者可以共享他们闲置的GPU/CPU资源，而消费者在API信用耗尽时可以使用社区的计算资源。

## 模式

### **贡献模式 — 共享你的闲置计算资源**

将你的机器设置为推理节点。你的本地Ollama模型将可供社区使用。

```bash
cd "$SKILL_DIR" && python scripts/contribute.py
```

这会连接到IdleClaw路由服务器，注册你的可用模型，并开始接收推理请求。按Ctrl+C即可停止。

**要求：** Ollama必须至少运行一个模型。

### **消费模式 — 使用社区的推理资源**

直接向社区网络发送聊天请求，而无需在本地运行模型。

```bash
cd "$SKILL_DIR" && python scripts/consume.py --model <model-name> --prompt "<your message>"
```

当有新的响应数据时，会将它们以流的形式输出到标准输出（stdout）。

### **状态模式 — 检查网络状态**

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
   - **贡献模式**：建立WebSocket连接以注册为推理节点。发送：节点ID、可用模型名称以及推理结果。接收：推理请求（模型名称、聊天消息和可选的工具配置）。
   - **消费模式**：向`/api/chat`发送HTTP POST请求，包含模型名称和聊天消息。接收：通过SSE传输的流式响应数据。
   - **状态模式**：向`/health`和`/api/models`发送HTTP GET请求。接收：服务器状态信息和可用模型列表。

2. **本地Ollama** (`OLLAMA_HOST`, 默认 `http://localhost:11434`)
   - **仅限贡献模式**：调用Ollama的API来列出模型并执行推理。所有通信都在本地主机上进行。

### 数据处理

- **所有用户数据在活动会话结束后都会从本地或服务器上清除**。
- **不需要也不存储任何凭证或API密钥**。
- **所有通信都是文本形式的**——服务器、节点和Ollama之间的所有消息都是通过WebSocket或HTTP传输的JSON文本。不传输二进制数据、文件上传、图片或可执行文件。
- **不执行任何本地代码**——贡献者节点仅作为中继，它将JSON格式的推理参数转发给Ollama，并将JSON格式的响应结果转发回服务器。节点不执行任何工具，不运行shell命令，也不访问文件系统。所有工具的执行都在服务器端完成，响应验证后进行。
- **聊天消息**（文本字符串）从消费者节点传输到服务器，再由服务器转发给贡献者节点，之后会被丢弃。
- **不收集任何遥测数据或分析信息**。
- 在贡献模式下，路由服务器将推理请求发送给节点，节点再将请求转发给你的本地Ollama实例。Ollama返回JSON格式的响应，节点再将其转发回去。贡献者可以将`IDLECLAW_SERVER`指向自己托管的Ollama实例。
- 在消费模式下，文本提示会被发送到路由服务器，服务器再将其转发给可用的贡献者节点。

### 数据清洗

**客户端：**
- 在将推理参数传递给Ollama之前会进行验证：只转发白名单中的键（`model`, `messages`, `stream`, `think`, `keep_alive`, `options`, `tools`, `format`）。未知的键会被剔除。
- 请求的模型名称必须与节点注册的模型名称匹配——未注册模型的请求会被拒绝。
- 实施消息限制：每次请求最多50条消息，每条消息内容最多10,000个字符。
- 只有已知的响应字段会被转发回服务器（`role`, `content`, `thinking`, `tool_calls`）。
- 在消费模式下，模型名称需要符合严格的格式要求（仅允许字母数字、冒号和句点）。
- 在贡献模式下，请求的模型名称必须与节点从Ollama注册的模型名称一致。
- 服务器URL在使用前会进行HTTP/HTTPS格式的验证。
- 不会根据用户输入构建shell命令——所有操作都由Python代码完成。
- 不会读取或访问任何本地文件——该工具仅与Ollama和路由服务器进行通信。

**服务器端（路由服务器）：**
- 对所有端点实施基于IP的速率限制：聊天请求（每分钟20次），节点注册请求（每分钟5次），其他请求（每分钟60次）。
- 输入验证：每次请求最多50条消息，每条消息最多10,000个字符，模型名称长度限制为64个字符，角色仅限于`user`和`assistant`。
- 输出清洗：在将响应内容发送给消费者之前会去除标记标签。
- 节点注册限制：每个IP地址最多注册3个节点，同时进行的请求数量被限制在1-10次之间。
- 工具执行安全措施：验证输入格式、检查参数类型、设置15秒的超时限制、限制每个节点的请求频率（每分钟20次）。
- 服务器仅绑定到本地主机，通过Caddy反向代理进行访问，并自动启用TLS加密。
- 已经过红队测试，相关安全评估结果记录在[GitHub文档](https://github.com/futurejunk/idleclaw/blob/main/security/SECURITY.md)中。

## 安装

运行安装程序以设置Python依赖项：

```bash
cd "$SKILL_DIR" && bash install.sh
```