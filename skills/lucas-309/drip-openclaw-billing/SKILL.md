---
name: drip-openclaw-billing
description: 使用 Drip 工具为 OpenClaw 工作负载添加运行/事件/使用量遥测数据，以实现可追溯性和计费功能。当需要集成 ClawHub 和 OpenClaw 功能时，请使用此方法——这些功能能够记录任务的完整生命周期、对外部工具的调用情况，以及每位客户的可计费使用量。
---
# Drip OpenClaw 计费功能

使用此功能可以将 OpenClaw 的请求与 Drip 服务集成，以便追踪使用情况并进行计费。

## 先决条件

- 必须配置 `DRIP_API_KEY`。
- 如果不使用 Drip 的默认 API 基址，需要配置 `DRIP_BASE_URL`。
- 为 `POST /v1/runs` 请求配置 `DRIP_WORKFLOW_ID`。
- 如果某些请求可以省略 `customerId`，则需要配置 `OPENCLAW_DEFAULT_customer_ID`。
- 需要根据您的策略配置 `OPENCLAW_TELEMETRY_FAIL_OPEN`（`true` 表示失败后开启服务，`false` 表示失败后关闭服务）。
- 请求用户/租户必须具有有效的 `CustomerId`。
- OpenClaw 需要具备用于请求开始/结束以及工具调用的运行时钩子点。

## ClawHub 部署规范

- 请将此功能与核心产品流程分离，仅通过 OpenClaw 专用的执行路径来调用。
- 在运行时从 ClawHub 的租户/用户身份中获取 `CustomerId`。
- 为事件和使用情况写入传递稳定的、具有幂等性的标识符，以避免重试时产生重复计费。
- 在 `agents/openai.yaml` 中将 `allow_implicit_invocation` 设置为 `false`，以确保此功能仅在被明确调用时执行。
- 如果使用 MCP（Machine Learning Platform）进行交付，请将 `agents/openai.yaml` 中的 `dependencies.tools[0].url` 替换为实际的 Drip MCP 主机地址。

## ClawHub 运行时设置（推荐）

- 模型：`gpt-5`（或您生产环境中的默认模型，并启用工具调用功能）。
- 超时时间：至少为 60 秒，包括运行时间、工具执行时间和使用情况数据生成时间。
- 重试策略：对于临时的 Drip 写入失败，允许最多 2 次重试，并采用退避策略。
- 调用模式：仅允许显式调用（使用 `$drip-openclaw-billing`）。

## 必需的集成模式

对于每个 OpenClaw 请求：

1. 使用 `POST /v1/runs` 启动请求执行。
2. 在每次外部工具/API 调用后，发送 `POST /v1/events` 请求。
3. 如果需要计费，请发送 `POST /v1/usage`（或 `/v1/usage/async`）请求。
4. 使用 `PATCH /v1/runs/:id` 请求结束请求执行。

## SDK 推荐方案

```typescript
import { OpenClawBilling } from '@drip-sdk/node/openclaw';

const billing = new OpenClawBilling({
  apiKey: process.env.DRIP_API_KEY,
  customerId: 'cus_123',
  workflowId: 'wf_openclaw',
});

await billing.withRun(
  { externalRunId: 'openclaw_req_456' },
  async ({ runId }) => {
    await billing.withToolCall(
      {
        runId,
        provider: 'brave',
        endpoint: '/res/v1/web/search',
        query: 'best usdc billing api',
      },
      async () => {
        return fetch('https://api.search.brave.com/res/v1/web/search?q=best+usdc+billing+api');
      },
    );
  },
);
```

## 原生 API 方案

### 启动请求执行

```http
POST /v1/runs
```

```json
{
  "customerId": "cus_123",
  "workflowId": "wf_openclaw",
  "externalRunId": "openclaw_req_456",
  "metadata": { "integration": "openclaw" }
}
```

### 发送工具调用事件

```http
POST /v1/events
```

```json
{
  "customerId": "cus_123",
  "runId": "run_abc",
  "actionName": "google_search",
  "eventType": "TOOL_CALL",
  "outcome": "SUCCEEDED",
  "quantity": 1,
  "idempotencyKey": "openclaw_run_abc_google_search_001",
  "metadata": {
    "provider": "google",
    "endpoint": "/customsearch/v1",
    "statusCode": 200,
    "latencyMs": 285,
    "queryHash": "f2a9ad...",
    "tokens": 0
  }
}
```

### 发送可计费的使用情况数据

```http
POST /v1/usage
```

```json
{
  "customerId": "cus_123",
  "usageType": "google_api_calls",
  "quantity": 1,
  "idempotencyKey": "openclaw_run_abc_google_search_001_usage",
  "metadata": {
    "runId": "run_abc",
    "provider": "google",
    "statusCode": 200,
    "latencyMs": 285
  }
}
```

### 结束请求执行

```http
PATCH /v1/runs/:id
```

```json
{ "status": "COMPLETED" }
```

## 失败处理

```json
{
  "status": "FAILED",
  "errorMessage": "Provider timeout",
  "errorCode": "TOOL_TIMEOUT"
}
```

## 数据映射指南

- `actionName`：`brave_search`、`google_search`、`<provider>_call`
- `eventType`：通常为 `TOOL_CALL` 或 `API_CALL`
- `usageType`：`api_calls` 或特定于提供商的计量类型（例如 `brave_api_calls`）
- `quantity`：通常为 1，除非计量单位另有规定

## 参考资料

- API 示例：`references/API.md`
- 集成文档：`docs/integration/openclaw-integration.md`
- ClawHub 部署元数据：`agents/clawhub.yaml`
- ClawHub 部署/测试运行手册：`OPENCLAW_CLAWHUB_DEPLOY_AND_TEST.md`