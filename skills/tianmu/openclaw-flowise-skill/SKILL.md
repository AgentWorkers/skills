---
name: flowise
description: 通过 REST API 与 Flowise AI 工作流程进行交互。当用户提到 Flowise、聊天流程（chatflows），或希望向 Flowise 的机器人/代理发送消息时，可以使用此功能。该 API 支持列出工作流程、发送预测结果以及管理对话内容。
---

# Flowise 技能

通过 REST API 与 Flowise AI 平台进行交互。

## 配置

将 Flowise 的设置存储在 `TOOLS.md` 文件中：

```markdown
### Flowise
- Server: http://localhost:3000
- API Key: your-api-key-here
- Default Flow ID: your-default-flow-id (optional)
- Default Timeout: 300

#### Flows
| Flow ID | 名称 | 用途 | 参数 |
|---------|------|------|------|
| abc123 | 客服助手 | 处理客户咨询、售后问题 | - |
| def456 | 代码助手 | 代码生成、调试、技术问答 |  form格式: `script`=要执行的脚本, `device`=设备(可选) |
| ghi789 | 文档助手 | 文档总结、RAG知识库查询 | - |
```

## 流选择

在调用 Flowise 时，将用户的请求与相应的流程匹配：
1. 查看 `TOOLS.md` 文件中的 `Flows` 表格。
2. 选择“用途”最符合用户需求的流程。
3. 如果没有匹配的流程，使用默认流程 ID。
4. 如果用户指定了具体的流程名称，使用该流程名称。

## 快速参考

### 发送消息（预测）

```bash
curl -X POST "${FLOWISE_URL}/api/v1/prediction/${FLOW_ID}" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello, how are you?"}'
```

### 带流式响应发送

```bash
curl -X POST "${FLOWISE_URL}/api/v1/prediction/${FLOW_ID}" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me a story", "streaming": true}'
```

### 带会话/对话记录发送

```bash
curl -X POST "${FLOWISE_URL}/api/v1/prediction/${FLOW_ID}" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"question": "What did I ask before?", "sessionId": "user-123"}'
```

### 列出所有聊天流程

```bash
curl -X GET "${FLOWISE_URL}/api/v1/chatflows" \
  -H "Authorization: Bearer ${API_KEY}"
```

### 获取聊天流程详情

```bash
curl -X GET "${FLOWISE_URL}/api/v1/chatflows/${FLOW_ID}" \
  -H "Authorization: Bearer ${API_KEY}"
```

## 预测的常用参数

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `question` | 字符串 | 要发送的消息 |
| `streaming` | 布尔值 | 是否启用流式响应（默认：false） |
| `sessionId` | 字符串 | 会话 ID（用于存储对话记录） |
| `overrideConfig` | 对象 | 覆盖流程配置（如温度、最大令牌数等） |
| `history` | 数组 | 手动提供对话历史记录 |
| `uploads` | 数组 | 上传的文件（图片、文档） |

### 流程特定的变量

某些流程支持自定义变量。请在请求中传递这些变量：

```json
{
  "question": "查询订单状态",
  "overrideConfig": {
    "vars": {
      "orderId": "12345",
      "userId": "user-abc"
    }
  }
}
```

### 使用 `TOOLS.md` 中的参数

查看 `TOOLS.md` 文件中的“参数”列，以了解以下信息：
- 必填参数
- 默认值
- 该流程所需的自定义变量

示例条目：
```
| abc123 | RAG知识库 | 文档查询 | sessionId=必填, variables={"namespace": "docs"} |
```

调用该流程时，请包含指定的参数。

## 覆盖配置示例

覆盖模型设置或其他流程参数：

```json
{
  "question": "Explain quantum computing",
  "overrideConfig": {
    "temperature": 0.7,
    "maxTokens": 500
  }
}
```

## 上传文件

```bash
curl -X POST "${FLOWISE_URL}/api/v1/prediction/${FLOW_ID}" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "question=Analyze this document" \
  -F "files=@/path/to/document.pdf"
```

## 使用 `form` 对象进行请求

某些流程使用 `form` 对象来接收结构化输入参数：

```bash
curl -X POST "${FLOWISE_URL}/api/v1/prediction/${FLOW_ID}" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "form": {
      "script": "d.send_keys(\"小红书\")",
      "device": "192.168.1.100:5555"
    }
  }'
```

查看 `TOOLS.md` 文件中的“参数”列，以识别需要使用 `form` 对象的流程。将参数传递到 `form` 对象中。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 200 | 成功 |
| 400 | 请求错误 - 检查输入格式 |
| 401 | 未经授权 - 检查 API 密钥 |
| 404 | 流程未找到 - 核实流程 ID |
| 500 | 服务器错误 - 查看 Flowise 日志 |

## 工作流程

1. 查看 `TOOLS.md` 文件中的 Flowise 服务器 URL 和 API 密钥。
2. 如果未配置，请询问用户以下信息：
   - Flowise 服务器 URL（例如：`http://localhost:3000`）
   - API 密钥（如果启用了身份验证）
   - 要使用的流程 ID
3. 使用 `curl` 和 `exec` 命令调用 API。
4. 解析 JSON 响应并展示结果。

## 提示

- 一致使用 `sessionId` 以保持对话上下文。
- 对于较长的响应，启用 `streaming: true`。
- 先使用 `/api/v1/ping` 端点测试连接是否正常。
- 如果用户未指定流程 ID，列出所有可用的流程。