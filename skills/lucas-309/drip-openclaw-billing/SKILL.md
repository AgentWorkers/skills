---
name: drip-openclaw-billing
description: 使用 Drip 工具为 OpenClaw 工作负载添加运行/事件/使用情况的遥测数据，以实现可追溯性和计费功能。在集成 ClawHub 和 OpenClaw 功能时，该工具非常有用——它可以记录任务的完整生命周期、对外部工具的调用情况，以及每位客户的可计费使用量。
---
# Drip OpenClaw 计费技能

使用此技能可以将 OpenClaw 请求与 Drip 服务集成，以便对使用情况進行追踪和计费。

## 先决条件

- 已配置 `DRIP_API_KEY`。
- `DRIP_BASE_URL` 已配置为官方可信的 Drip API 域名。
- 为 `POST /v1/runs` 请求配置了 `DRIP_WORKFLOW_ID`。
- 如果请求可以省略 `customerId`，则需配置 `OPENCLAW_DEFAULT_CUSTOMER_ID`。
- `OPENCLAW_TELEMETRY_FAIL_OPEN` 已根据您的策略进行配置（`true` 表示失败时开启服务，`false` 表示失败时关闭服务）。
- 请求用户/租户具有有效的 `customerId`。
- OpenClaw 运行时已设置请求开始/结束以及工具调用的钩子点。

## 所需凭证（具有授权权限）

- 必需的环境变量：
  - `DRIP_API_KEY`（主要凭证）
  - `DRIP_BASE_URL`（可信的 Drip API 主机地址）
  - `DRIP_WORKFLOW_ID`
- 可选的环境变量：
  - `OPENCLAW_DEFAULT_customer_ID`
  - `OPENCLAW_TELEMETRY_FAIL/Open`
  - `OPENCLAW_BILL_SKILL_CALLS`

像 `BRAVE_API_KEY` 或 `GOOGLE_API_KEY` 这样的提供商密钥不是此计费技能所必需的。只有在您的代理运行时直接调用这些提供商的服务时才需要提供这些密钥。

## ClawHub 部署规范

- 将此技能与核心产品流程分离；仅通过 OpenClaw 特定的执行路径来调用它。
- 在运行时从 ClawHub 租户/用户身份中解析 `customerId`。
- 为事件和使用情况写入传递稳定的、具有幂等性的标识符，以避免重试时产生重复费用。
- 在 `agents/openai.yaml` 中设置 `allow_implicit_invocation: false`，以确保此技能仅在显式调用时运行。
- 在启用生产流量之前，验证 `DRIP_BASE_URL` 是否指向官方可信的 Drip 端点。

## ClawHub 运行时设置（推荐）

- 模型：`gpt-5`（或您生产环境中的默认模型，且已启用工具调用功能）。
- 超时时间：至少为 `60秒`（包括运行时间、工具调用时间以及使用情况数据的生成时间）。
- 重试策略：对于临时的 Drip 写入失败，最多重试 `2` 次，并采用退避策略。
- 调用模式：仅允许显式调用（使用命令 `$drip-openclaw-billing`）。

## 所需的集成模式

对于每个 OpenClaw 请求：

1. 通过 `POST /v1/runs` 启动运行。
2. 在每次外部工具/API 调用后，通过 `POST /v1/events` 发送事件数据。
3. 如果需要计费，请通过 `POST /v1/usage`（或 `/v1/usage/async`）发送使用情况数据。
4. 通过 `PATCH /v1/runs/:id` 结束运行。

## 避免发送过多数据（强制要求）

仅发送计费和诊断所需的最低限度的执行元数据：

- 允许的元数据字段：
  - `integration`、`requestId`、`provider`、`endpoint`、`statusCode`、`latencyMs`、`queryHash`、`tokens`
  - `source`、`action`、`tenantId`、`requesterId`、`runId`、`workflowId`、`error`
- 禁止的元数据字段：
  - 原始查询文本
  - 原始提示或模型输出
  - 授权头
  - API 密钥、密码、机密信息
  - 完整的请求/响应正文

如果需要查询上下文，请仅发送 `queryHash`（sha256 哈希值），切勿发送原始查询文本。

## SDK 选项（推荐）

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

## 原始 API 选项

### 启动运行

```http
POST /v1/runs
```

### 发送工具事件

```http
POST /v1/events
```

### 发送可计费的使用情况数据

```http
POST /v1/usage
```

### 结束运行

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

### 处理失败情况

```json
{
  "status": "FAILED",
  "errorMessage": "Provider timeout",
  "errorCode": "TOOL_TIMEOUT"
}
```

## 映射指南

- `actionName`：`brave_search`、`google_search`、`<provider>_call`
- `eventType`：通常为 `TOOL_CALL` 或 `API_CALL`
- `usageType`：`api_calls` 或特定于提供商的计量类型（如 `brave_api_calls`）
- `quantity`：通常为 `1`，除非需要按计量单位进行计数

## 参考资料

- API 示例：`references/API.md`
- 集成文档：`docs/integration/openclaw-integration.md`
- ClawHub 部署元数据：`agents/clawhub.yaml`
- ClawHub 部署/测试运行手册：`OPENCLAW_CLAWHUB_DEPLOY_AND_TEST.md`