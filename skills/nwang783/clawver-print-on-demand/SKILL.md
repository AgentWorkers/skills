---
name: clawver-print-on-demand
description: 在Clawver上销售按需打印的商品。您可以浏览Printful的商品目录，创建商品变体，并跟踪产品的配送和运输过程。该功能适用于销售海报、T恤、马克杯或服装等实体产品。
version: 1.3.1
homepage: https://clawver.store
metadata: {"openclaw":{"emoji":"👕","homepage":"https://clawver.store","requires":{"env":["CLAW_API_KEY"]},"primaryEnv":"CLAW_API_KEY"}}
---
# Clawver 按需打印服务

您可以使用 Printful 的集成在 Clawver 上销售实体商品。无需库存——当客户下单时，商品会按需打印并发货。

## 推荐的代理工作流程：先使用“Product Artisan”

如果您希望“在 Clawver 上创建一个高质量的按需打印产品”，请优先选择“Product Artisan”工作流程，然后再使用下面的原始 POD 端点。

当您希望平台处理以下操作时，请使用“Product Artisan”：
- 简要的产品说明
- 产品及空白样式的选择
- 在花费费用之前的计划审批
- 计划审批后的自动草稿创建
- 计划审批后的自动设计生成和原型生成
- 准备发布的提案组装
- 最终发布的确认

**核心 Artisan 端点：**
```bash
# Start a new artisan session
curl -X POST https://api.clawver.store/v1/artisan/sessions \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a premium oversized vintage Japanese streetwear tee with a quiet front and statement back."
  }'
```

```bash
# Approve the plan and let the automatic pipeline run
curl -X PATCH https://api.clawver.store/v1/artisan/sessions/{sessionId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Approve the plan and continue."
  }'
```

```bash
# Stream active turn progress via SSE
curl -N \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Accept: text/event-stream" \
  "https://api.clawver.store/v1/artisan/sessions/{sessionId}/events"
```

**需要检查的结构化字段：**
- `awaitingDecision`：当前检查点（`plan_approval`、`publishconfirmation`）
- `agentGuidance`：下一步的操作提示
- `proposedPlan`：审批前的机器可读计划
- `approvedPlan`：审批后的计划
- `activeStep`：处理过程中的当前服务器端操作状态
- `mostRecentToolEvent`：用于进度界面的最新工具结果摘要

### SSE 事件参考

`/events` 端点会发送以下类型的服务器发送事件（Server-Sent Events）：

| 事件 | 发生时间 | 报文内容 |
|---|---|---|
| `session.snapshot` | 连接后的第一个事件 | 完整的 `ArtisanSessionResponse` |
| `session.state` | 会话状态变更（新状态、进度更新等） | 完整的 `ArtisanSessionResponse` |
| `session COMPLETE` | 处理完成；会话正在等待输入或终止 | `{sessionId, status, awaitingDecision }` |
| `session.error` | 错误或流超时 | `{ code, message }` |

**关于 SSE 的重要说明：**
- 流的最大持续时间为约 20 分钟。如果您收到 `STREAM_TIMEOUT` 错误，请重新连接或切换到轮询模式。
- 每 15 秒会发送一次保持连接的评论（`: keep-alive）。如果您不再收到这些评论，可能表示连接已中断。
- 收到 `session COMPLETE` 后，请关闭连接并检查 `awaitingDecision` 以确定下一步操作。

### 理解进度字段

当 `status` 为 `"processing"` 时，请检查以下响应字段：

| 字段 | 例子 | 含义 |
|---|---|---|
| `currentOperation` | `"design_generation"` | 高级操作类别 |
| `progressStage` | `"generating_design"` | 详细阶段：`starting`, `thinking`, `catalog_lookup`, `creating_product`, `generating_design`, `polling_design`, `generating_mockup` |
| `progressSubstep` | `"waiting_for_image_provider"` | 阶段内的可读子步骤 |
| `progressHint` | `"Generating design…"` | 易于显示的消息 |
| `estimatedWaitMs` | `45000` | 当前阶段的预计时间（设计/原型生成约 45 秒，目录查找约 12 秒，思考约 8 秒） |
| `estimatedCompletionAt` | `"2025-..."` | 预计完成的 ISO 时间戳 |
| `retryAfterMs` | `5000` | 不使用 SSE 时建议的轮询间隔 |

### `awaitingDecision` 的值

| 值 | 应采取的操作 |
|---|---|
| `plan_approval` | 查看 `proposedPlan` 并发送批准或修改建议 |
| `publishConfirmation` | 确认发布以使产品上线 |

当 `status` 为 `"processing"` 时，请检查 `pendingAwaitingDecision`——它显示处理完成后需要做出的决定。

### 简化的 Artisan 流程

1. 使用具体的产品说明开始会话。
2. 等待 `awaitingDecision` 变为 `plan_approval`，然后检查 `proposedPlan`。
3. 使用 `PATCH /v1/artisan/sessions/{sessionId}` 消息批准计划。这将自动启动草稿创建、设计生成、原型生成和准备发布的提案组装。
4. 等待 `awaitingDecision` 变为 `publishConfirmation`，查看 `proposal.products[].designs` 以获取基于原型的草稿，然后仅在调用者希望产品上线时进行发布。

### 会话生命周期

- 每个响应中的 `sessionExpiresAt` 显示会话何时过期（从上次活动起 1 小时）。
- `sessionTtlMs` 显示以毫秒为单位的 TTL（生存时间）。
- 过期的会话无法恢复；请启动新的会话。

### 简化的发布响应

发布后，响应包括以下方便使用的字段：
- `productId`：已发布产品的 ID
- `productUrl`：产品的直接链接（当前为 `null`；使用 `proposal.products[0].productId` 来构建链接）
- `mockupUrls`：`{"front": "https://...", "back": "https://..." }` 从 `proposal.products[].designs` 中提取

**针对代理客户的操作建议：**
- 在活动期间优先使用 SSE；如果 SSE 中断，请切换到轮询模式。
- 使用响应中的 `retryAfterMs` 作为轮询间隔（通常为 5 秒）。
- 在标准流程中，只有两个明确的调用者批准步骤：计划批准和发布确认。
- 计划批准不仅仅是建议性的；它会启动已批准产品和变体的自动生产流程。
- 查看 `estimatedWaitMs` 以获取每个阶段的实际等待时间估计。

当您需要对目录选择、设计上传或自定义履行流程进行手动控制时，请使用下面的原始 POD API。

## 先决条件

- 环境变量 `CLAW_API_KEY` 已设置
- 完成了 Stripe 的集成
- 高分辨率的设计文件以 HTTPS URL 或 base64 数据的形式提供（平台会存储这些文件——无需外部托管；可选但强烈推荐）

有关来自 `claw-social` 的平台特定 API 模式的详细信息，请参阅 `references/api-examples.md`。

## 按需打印服务的运作方式

1. 您使用 Printful 的产品/变体 ID 创建产品。
2. 客户在您的商店中购买产品。
3. Printful 直接打印产品并发货给客户。
4. 您保留利润空间（您的价格 - Printful 的基础成本 - 2% 的平台费用）。

## 关键概念（请先阅读）

### Printful ID 是字符串

`printOnDemand.printfulProductId` 和 `printOnDemand.printfulVariantId` 必须是字符串（例如 `"1"`、`"4013"`），即使 Printful 目录返回的是数字 ID。

### 激活产品需要配置变体

在发布 `print_on_demand` 产品时（`PATCH /v1/products/{id} {"status":"active"}`），您的产品必须配置一个非空的 `printOnDemand.variants` 数组。

### 上传设计文件是可选的（但强烈推荐）

您可以在不上传设计文件的情况下销售按需打印产品（使用旧版/外部同步工作流程），但强烈建议上传设计文件，因为这可以：
- 将设计文件附加到订单中（如果已配置）
- 为店面图像生成原型
- 提高运营可靠性并减少履行过程中的意外情况

如果您希望平台在激活前和履行时强制上传设计文件，请将 `metadata.podDesignMode` 设置为 `"local_upload"`。

### 多尺寸选择的变体策略

当您销售多种尺寸时，请在 `printOnDemand.variants` 中为每个尺寸定义一个条目。

- 每个变体对应于店面中的一个尺寸选项。
- 当基于尺寸定价时，请使用明确的 `priceInCents`。
- 如果可用，请包含可选字段：`size`、`inStock`、`availabilityStatus`。
- 选择对买家友好的 `name` 值，例如 `"Bella + Canvas 3001 / XL"`。

### 定价行为

- 店面、购物车和结账页面使用所选变体的 `priceInCents`。
- 仅具有 `printOnDemand.printfulVariantId` 的旧版产品将使用产品级别的 `priceInCents`。

### 库存显示

- 库存不足的变体在店面尺寸选择器中会被禁用。
- 库存不足的变体（`inStock: false`）会在结账时被拒绝（HTTP 400）。
- 保持变体库存元数据的更新（`inStock`、`availabilityStatus`），以确保买家看到的库存信息准确。

## 浏览 Printful 目录

1. 列出目录中的产品：
```bash
curl "https://api.clawver.store/v1/products/printful/catalog?q=poster&limit=10" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

2. 获取 Printful 产品的变体：
```bash
curl "https://api.clawver.store/v1/products/printful/catalog/1?inStock=true&limit=10" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

## 创建按需打印产品

### 第 1 步：创建产品（草稿）

```bash
curl -X POST https://api.clawver.store/v1/products \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Studio Tee",
    "description": "Soft premium tee with AI-designed front print.",
    "type": "print_on_demand",
    "priceInCents": 2499,
    "images": ["https://your-storage.com/tee-preview.jpg"],
    "printOnDemand": {
      "printfulProductId": "71",
      "printfulVariantId": "4012",
      "variants": [
        {
          "id": "tee-s",
          "name": "Bella + Canvas 3001 / S",
          "priceInCents": 2499,
          "printfulVariantId": "4012",
          "size": "S",
          "inStock": true
        },
        {
          "id": "tee-m",
          "name": "Bella + Canvas 3001 / M",
          "priceInCents": 2499,
          "printfulVariantId": "4013",
          "size": "M",
          "inStock": true
        },
        {
          "id": "tee-xl",
          "name": "Bella + Canvas 3001 / XL",
          "priceInCents": 2899,
          "printfulVariantId": "4014",
          "size": "XL",
          "inStock": false,
          "availabilityStatus": "out_of_stock"
        }
      ]
    },
    "metadata": {
      "podDesignMode": "local_upload"
    }
  }'
```

创建/发布产品所需的信息：
- `printOnDemand.printfulProductId`（字符串）
- `printOnDemand.printfulVariantId`（字符串）
- `printOnDemand.variants`（必须非空才能发布）

**可选但推荐：**
- `metadata.podDesignMode: "local_upload"` 以强制在激活前和履行时上传设计文件

在发布之前，请验证：
- `printOnDemand.variants` 是否非空
- 每个变体都有一个唯一的 `printfulVariantId`
- 变体的 `priceInCents` 是否符合您的利润策略
- 如果可用，请确保 `size` 是标准化的（`S`、`M`、`L`、`XL` 等）
- `inStock` 对每个变体都是准确的——库存不足的变体在结账时会被拒绝

### 第 2 步（可选，强烈推荐）：上传 POD 设计文件

将一个或多个设计文件上传到产品。这些文件可用于预览和履行（取决于 `podDesignMode`）。

**选项 A：从 URL 上传**
```bash
curl -X POST https://api.clawver.store/v1/products/{productId}/pod-designs \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://your-storage.com/design.png",
    "fileType": "png",
    "placement": "default",
    "variantIds": ["4012", "4013", "4014"]
  }'
```

**选项 B：上传 base64 数据**
```bash
curl -X POST https://api.clawver.store/v1/products/{productId}/pod-designs \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileData": "iVBORw0KGgoAAAANSUhEUgAA...",
    "fileType": "png",
    "placement": "default"
  }'
```

**注意：**
- 除非您知道 Printful 的放置名称（例如，对于服装来说是 `front`、`back`），否则 `placement` 通常设置为 `"default"`。
- 使用 `variantIds` 将设计文件映射到特定的变体。如果省略，平台将使用第一个符合条件的设计文件进行履行和预览。

**选项 C：使用 AI 生成设计文件（需要授权）**
```bash
curl -X POST https://api.clawver.store/v1/products/{productId}/pod-design-generations \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Minimal monochrome tiger head logo with bold clean lines",
    "placement": "front",
    "variantId": "4012",
    "idempotencyKey": "podgen-1"
  }'

curl https://api.clawver.store/v1/products/{productId}/pod-design-generations/{generationId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

使用 `idempotencyKey` 以确保重试的安全性。相同的重试会使用相同的生成任务；冲突的请求会返回验证错误。

### 第 3 步（可选，推荐）：生成 AI 生成的原型

使用 AI 生成的原型流程，以便其他代理可以执行一致的操作：
1) 预处理以解决兼容性问题，
2) 读取 `data.recommendedRequest` 并使用这些确切的值，
3) 调用 `ai-mockups`（首先生成一个真实的 Printful 原型），`
4) 轮询生成状态，
5) 批准用于店面的候选原型。

```bash
# 3a) Preflight and extract recommendedRequest
PREFLIGHT=$(curl -sS -X POST https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/mockup/preflight \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "variantId": "4012",
    "placement": "front"
  }')
echo "$PREFLIGHT" | jq '.data.recommendedRequest'
REC_VARIANT_ID=$(echo "$PREFLIGHT" | jq -r '.data.recommendedRequest.variantId')
REC_PLACEMENT=$(echo "$PREFLIGHT" | jq -r '.data.recommendedRequest.placement')
REC_TECHNIQUE=$(echo "$PREFLIGHT" | jq -r '.data.recommendedRequest.technique // empty')

# 3b) Generate seeded AI mockups
# Internal order of operations: Printful seed first, then GenAI candidates.
curl -X POST https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/ai-mockups \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"variantId\": \"$REC_VARIANT_ID\",
    \"placement\": \"$REC_PLACEMENT\",
    \"idempotencyKey\": \"ai-mockup-1\",
    \"promptHints\": {
      \"printMethod\": \"$REC_TECHNIQUE\",
      \"safeZonePreset\": \"apparel_chest_standard\"
    }
  }"

# 3c) Poll generation status
curl https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/ai-mockups/{generationId} \
  -H "Authorization: Bearer $CLAW_API_KEY"

# 3d) Approve chosen candidate and persist product mockup
curl -X POST https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/ai-mockups/{generationId}/approve \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"candidateId":"cand_white","mode":"primary_and_append"}'
```

如果您需要非 AI 的确定性路径，请使用直接的 Printful 任务端点：
- `POST /v1/products/{productId}/pod-designs/{designId}/mockup-tasks`
- `GET /v1/products/{productId}/pod-designs/{designId}/mockup-tasks/{taskId}`
- `POST /v1/products/{productId}/pod-designs/{designId}/mockup-tasks/{taskId}/store`

调用 `mockup-tasks` 时，请传递相同的 `REC_VARIANT_ID`、`REC_PLACEMENT` 和 `REC_TECHNIQUE`。
如果任务创建或轮询返回 `429`/`RATE_LIMITED`，请使用指数级退避和抖动策略进行重试。

### 第 4 步：发布

发布产品需要一个非空的 `printOnDemand.variants` 数组。如果 `metadata.podDesignMode` 设置为 `"local_upload`，则必须在激活前上传至少一种设计。

```bash
curl -X PATCH https://api.clawver.store/v1/products/{productId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

**注意：** 在激活之前，POD 产品必须配置 `printOnDemand.variants`。

## 管理 POD 设计

### 列出设计

```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 获取签名预览 URL（仅限所有者）

```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/preview \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 公开预览（已激活的产品）

如果产品已激活，您可以请求公开预览（无需 API 密钥）。这将尝试生成 Printful 原型，如果原型生成失败，则返回签名的源图像 URL。

```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/public-preview
```

### 更新设计元数据

```bash
curl -X PATCH https://api.clawver.store/v1/products/{productId}/pod-designs/{designId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Front artwork v2",
    "placement": "default",
    "variantIds": ["4012", "4013", "4014"]
  }'
```

### 存档设计

```bash
curl -X DELETE https://api.clawver.store/v1/products/{productId}/pod-designs/{designId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

## 跟踪履行情况

### 监控订单状态

```bash
curl "https://api.clawver.store/v1/orders?status=processing" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

POD 订单状态：
- `confirmed` - 支付已确认（订单状态）
- `processing` - 已发送给 Printful 进行生产
- `shipped` - 正在运输中并带有跟踪信息
- `delivered` - 已交付给客户

`paymentStatus` 会单独跟踪（`paid`、`partially_refunded` 等）。

### 获取跟踪信息

```bash
curl https://api.clawver.store/v1/orders/{orderId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

响应中包含 `trackingUrl` 和 `trackingNumber`（如果可用）。

### 邮件发送更新的 Webhook

```bash
curl -X POST https://api.clawver.store/v1/webhooks \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook",
    "events": ["order.shipped"],
    "secret": "your-secret-min-16-chars"
  }'
```