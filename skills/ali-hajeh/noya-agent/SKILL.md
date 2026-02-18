---
name: noya-agent
description: 与 Noya AI 代理进行交互，用于加密货币交易、预测市场分析、代币研究以及定期定额投资（DCA）策略的制定。当用户需要向 Noya 发送消息、管理对话线程或通过 Noya API 查询代理功能时，可以使用该工具。
---
# Noya Agent

Noya 是一个多智能体 AI 系统，可用于加密货币交易、预测市场（如 Polymarket、Rain）、代币分析以及定期投资（DCA）策略的制定。该技能允许通过其 REST API 以编程方式与 Noya 进行交互。

## 先决条件

1. 在 [agent.noya.ai](https://agent.noya.ai) 注册一个账户。
2. 从“API 密钥”页面（设置 > API 密钥）生成 API 密钥。
3. 安全存储该密钥——该密钥仅在注册时显示一次。

## 认证

所有请求都需要包含 `x-api-key` 头部字段：

```
x-api-key: noya_<your-key>
```

基础 URL：`https://safenet.one`

## 快速入门

### 向 Noya 发送消息

```bash
curl -N https://safenet.one/api/messages/stream \
  -H "Content-Type: application/json" \
  -H "x-api-key: noya_YOUR_KEY" \
  -d '{"message": "What is the current price of ETH?", "threadId": "my-thread-1"}'
```

响应是一个分块的文本流。每个分块都是一个 JSON 对象，用 `--breakpoint--` 进行分隔。

### 列出对话线程

```bash
curl https://safenet.one/api/threads \
  -H "x-api-key: noya_YOUR_KEY"
```

### 获取代理功能

```bash
curl https://safenet.one/api/agents/summarize \
  -H "x-api-key: noya_YOUR_KEY"
```

## 端点

### POST /api/messages/stream

向 Noya 代理发送消息，并接收分块的文本响应。

**请求体：**

| 字段    | 类型   | 是否必填 | 描述                               |
|----------|--------|----------|---------------------------|
| message  | string | 是      | 用户发送的消息                         |
| threadId | string | 是      | 对话线程 ID                           |

**响应：** 分块的文本流。每个分块都是一个 JSON 对象，用 `--breakpoint--\n` 进行分隔。

**分块类型：**

| 类型                 | 描述                                  |
|----------------------|----------------------------------------------|
| `message`            | 代理的文本响应片段                         |
| `tool`               | 工具调用结果及其产生的数据                   |
| `progress`           | 进度更新（当前/总消息量）                     |
| `interrupt`          | 代理请求用户确认                         |
| `reasonForExecution` | 代理解释执行操作的缘由                     |
| `executionSteps`     | 逐步执行计划                         |
| `error`              | 错误信息                             |

**解析示例（JavaScript）：**

```javascript
const response = await fetch("https://safenet.one/api/messages/stream", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": "noya_YOUR_KEY",
  },
  body: JSON.stringify({ message: "Analyze SOL", threadId: "t1" }),
});

const reader = response.body.getReader();
const decoder = new TextDecoder();
let buffer = "";

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  buffer += decoder.decode(value, { stream: true });
  const parts = buffer.split("--breakpoint--\n");
  buffer = parts.pop();
  for (const part of parts) {
    const trimmed = part.trim();
    if (!trimmed || trimmed === "keep-alive") continue;
    const chunk = JSON.parse(trimmed);
    if (chunk.type === "message") {
      process.stdout.write(chunk.message);
    }
  }
}
```

### GET /api/threads

列出已认证用户的所有对话线程。

**响应：**

```json
{
  "success": true,
  "data": { "threads": [{ "id": "...", "name": "...", "created_at": "..." }] }
}
```

### GET /api/threads/:threadId/messages

获取特定线程中的所有消息。

**响应：**

```json
{
  "success": true,
  "data": { "messages": [...] }
}
```

### DELETE /api/threads/:threadId

删除一个对话线程。

### POST /api/chat/completions

兼容 OpenAI 的聊天完成功能。会话历史数据存储在 Redis 中。

**请求体：**

| 字段       | 类型   | 是否必填 | 描述                          |
|-------------|--------|----------|--------------------------------------|
| sessionId   | string | 是      | 会话标识符                         |
| message     | string | 是      | 用户发送的消息                         |
| config      | object | 否       | 模型配置                           |
| tools       | array  | 否       | 使用的工具                         |
| toolResults | array  | 否       | 上次工具调用的结果                     |

### GET /api/agents/summarize

返回所有可用的代理类型及其专长和工具。

## 额外资源

- 完整的 API 规范（包括请求/响应格式）请参阅 [reference.md](reference.md)。
- MCP 服务器可用：`npx noya-agent-mcp`（使用 `NOYA_API_KEY` 环境变量进行配置）