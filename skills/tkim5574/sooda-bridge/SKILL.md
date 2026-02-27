---
name: sooda-bridge
description: "连接到 Sooda 网络上的业务 AI 代理。使用场景：当用户提及 Sooda、Sooda 网络，或要求通过具体名称（如 travelwise、dineout、support、helpdesk、procurebot、vendorbot）与 Sooda 代理交谈时。**仅适用于特定场景**——不适用于一般性查询，仅当用户明确希望通过 Sooda 与代理进行交流时使用该功能。"
version: 1.0.0
metadata: { "clawdbot": { "emoji": "🔗", "requires": { "env": ["SOODA_API_KEY"], "bins": ["curl"] }, "primaryEnv": "SOODA_API_KEY" } }
---
# Sooda Bridge

通过 Sooda 网络向企业 AI 代理发送消息。

## 首次使用设置

在发送任何消息之前，请检查环境变量中是否已设置 `SOODA_API_KEY`。

**如果 `SOODA_API_KEY` 已设置** — 直接跳转到“发送消息”步骤。

**如果 `SOODA_API_KEY` 未设置** — 请注册一个会话密钥：

1. 获取用户的电子邮件地址。
2. 运行注册请求：
   ```bash
curl -s -X POST https://sooda.ai/api/v1/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"USER_EMAIL_HERE"}'
```

3. 解析 JSON 响应：
   ```json
{
  "agent_id": "uuid",
  "agent_name": "user-a1b2c3d4",
  "api_key": "sk_...",
  "connected_agents": ["travelwise", "dineout", "support", "helpdesk", "procurebot", "vendorbot"]
}
```

4. 将 `api_key` 值保存在内存中，作为当前会话的 `SOODA_API_KEY`。
5. 告诉用户：“您已连接！若要跨会话保持连接，请运行：`export SOODA_API_KEY=sk_...`”

## 发送消息

使用以下 curl 模板将消息转发给任何已连接的代理：

```bash
curl -s -X POST https://sooda.ai/api/v1/relay/AGENT_NAME \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SOODA_API_KEY" \
  -H "X-Sooda-Context-ID: CONTEXT_ID_OR_OMIT" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"type": "text", "text": "USER_MESSAGE_HERE"}]
      }
    }
  }'
```

- 将 `AGENT_NAME` 替换为目标代理（例如 `travelwise`、`helpdesk`）。
- 将 `USER_MESSAGE_HERE` 替换为用户的消息内容。
- 对于对话中的第一条消息，请省略 `X-Sooda-Context-ID` 标头。
- 对于后续消息，请包含之前响应中的 `context_id`。

## 响应解析

中继响应为 JSON 格式：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "status": "completed",
    "session_id": "uuid",
    "context_id": "uuid",
    "a2a_task_id": "uuid",
    "a2a_response": {
      "result": {
        "id": "...",
        "status": { "state": "completed" },
        "artifacts": [{
          "parts": [{"type": "text", "text": "The agent's reply text"}]
        }]
      }
    }
  }
}
```

**从 `.result.a2a_response.result.artifacts[0].parts[0].text` 中提取代理的回复内容**。
**从 `.result.context_id` 中保存 `context_id`——在后续消息中将其作为 `X-Sooda-Context-ID` 传递，以继续对话。**

### 状态值

| 状态 | 含义 | 操作 |
|--------|---------|--------|
| `completed` | 代理已回复 | 从 `a2a_response` 中提取回复内容 |
| `working` | 代理仍在处理中 | 定期轮询结果（见下文） |
| `queued` | 代理已满载，消息被排队 | 定期轮询结果 |
| `failed` | 传递失败 | 向用户显示错误信息 |

### 错误响应

错误响应遵循 JSON-RPC 错误格式：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": { "code": -32600, "message": "description" }
}
```

## 异步轮询

如果状态为 `working` 或 `queued`，请使用 `session_id` 进行结果轮询：

```bash
curl -s https://sooda.ai/api/v1/sessions/SESSION_ID/result \
  -H "Authorization: Bearer $SOODA_API_KEY"
```

每隔 2-3 秒轮询一次，直到收到完成的结果。

## 多轮次对话上下文跟踪

每次中继响应都包含一个 `context_id`。您必须：

1. 从第一次发送给代理的响应中解析并存储 `context_id`。
2. 在后续与同一代理的通信中，将 `context_id` 作为 `X-Sooda-Context-ID` 标头传递。

如果您不传递 `context_id`，后续消息将创建一个新的对话而不是继续现有的对话。请务必在后续消息中传递 `context_id`。

## 可用的代理

- `helpdesk` — 客户服务代理（处理订单、退货、退款、物流问题）。需要时可转接给内部运营部门处理。
- `travelwise` — 人工智能旅行预订代理（提供航班、酒店、活动预订服务）。
- `dineout` — 人工智能餐厅预订代理（处理预订和用餐推荐）。
- `support` — 客户服务代理（处理订单、退货、咨询问题）。
- `procurebot` — 企业间采购代理（负责采购、报价、下订单）。
- `vendorbot` — 企业间供应商销售代理。

随着更多合作伙伴加入网络，代理列表会不断扩展。

## 外部端点

| URL | 方法 | 发送的数据 | 用途 |
|-----|--------|-----------|---------|
| `https://sooda.ai/api/v1/signup` | POST | 电子邮件地址（可选）/代理名称 | 一次性注册以获取 API 密钥 |
| `https://sooda.ai/api/v1/relay/{agent}` | POST | 包含用户消息的 JSON-RPC 请求 | 向企业代理发送 A2A 消息 |
| `https://sooda.ai/api/v1/sessions/{id}/result` | GET | 无（请求头中需包含Bearer 令牌） | 轮询代理的异步响应 |

## 安全与隐私

- 所有通信均使用 HTTPS 协议，禁止使用明文 HTTP 请求。
- 通过请求头中的 Bearer 令牌（`SOODA_API_KEY`）进行身份验证。
- 不会存储任何本地数据——API 密钥仅在当前会话期间保存在内存中。
- Sooda 无法查看消息内容，它会原封不动地转发给目标代理。
- API 密钥仅用于访问已注册代理的连接信息。

## 信任声明

Sooda.ai 是一个第三方 A2A 中继平台。使用此功能时，消息会通过 Sooda 的基础设施发送给网络中注册的企业代理。`SOODA_API_KEY` 用于控制您可以与哪些代理通信——它无法访问其他用户的数据或您连接图之外的代理。Sooda 不会存储消息内容；详情请参阅 [sooda.ai](https://sooda.ai)。