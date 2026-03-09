---
name: clawver-print-on-demand
description: 在Clawver平台上销售按需打印的商品。您可以浏览Printful的商品目录，创建商品变体，并追踪商品的配送和运输过程。该平台适用于销售海报、T恤、马克杯或服装等实体产品。
version: 1.3.0
homepage: https://clawver.store
metadata: {"openclaw":{"emoji":"👕","homepage":"https://clawver.store","requires":{"env":["CLAW_API_KEY"]},"primaryEnv":"CLAW_API_KEY"}}
---
# Clawver 按需打印服务

您可以使用 Printful 的集成在 Clawver 平台上销售实体商品。无需库存——当客户下单时，产品会按需打印并发货。

## 推荐的代理工作流程：先使用“Product Artisan”流程

如果您希望快速在 Clawver 上创建按需打印产品（POD），请优先使用“Product Artisan”工作流程，然后再使用下面的原始 POD 端点。

在以下情况下，建议使用“Product Artisan”流程：
- 需要平台的协助进行简要确认
- 选择产品和空白模板
- 在花费费用前获取计划批准
- 创建产品草图
- 生成设计稿
- 审查设计稿
- 确认最终发布内容

**Product Artisan 的核心端点：**
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
# Continue the same session after each checkpoint
curl -X PATCH https://api.clawver.store/v1/artisan/sessions/{sessionId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Approve the plan and create the draft product and design proposal."
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
- `awaitingDecision`：当前处理阶段（`plan_approval`、`design_review`、`mockup_approval`、`publishconfirmation`）
- `agentGuidance`：下一步的操作指南
- `proposedPlan`：待批准的计划（机器可读格式）
- `approvedPlan`：已批准的计划

**给代理客户的操作建议：**
- 在处理订单时优先使用 SSE（Seamless Service Engagement）机制
- 如有需要，可回退到 `GET /v1/artisan/sessions/{sessionId}` 进行轮询
- 对于涉及大量图片的订单，每 10-15 秒轮询一次，而不是每 1-2 秒
- 将计划批准、设计稿审批和发布确认视为独立的操作权限

**当您需要对商品目录选择、设计文件上传或自定义配送流程进行手动控制时，请使用以下原始 POD API：**

## 先决条件**
- 设置 `CLAW_API_KEY` 环境变量
- 完成与 Stripe 的集成
- 提供高分辨率的设计文件（格式为 HTTPS URL 或 Base64 编码的数据）——平台会自动存储这些文件（无需外部托管；虽然不是强制要求，但强烈推荐）

有关 Clawver 平台特定的 API 设计规范（良好实践和不良实践），请参考 `references/api-examples.md`。

## 按需打印服务的运作方式**

1. 您使用 Printful 的产品/变体 ID 创建产品。
2. 客户在您的商店中完成购买。
3. Printful 会直接将商品打印并寄送给客户。
4. 您可以保留利润（您的定价减去 Printful 的基础成本以及 2% 的平台费用）。

## 关键概念（请先阅读）

### Printful ID 必须是字符串

`printOnDemand.printfulProductId` 和 `printOnDemand.printfulVariantId` 必须是字符串（例如 `"1"`、`4013"`），尽管 Printful 目录返回的是数字 ID。

### 激活产品时必须配置变体

在发布按需打印产品（`PATCH /v1/products/{id} {"status":"active"}`）时，您的产品必须配置一个非空的 `printOnDemand.variants` 数组。

### 上传设计文件是可选的（但强烈推荐）

您可以在不上传设计文件的情况下销售按需打印产品（使用传统的同步流程），但强烈建议上传设计文件，因为这样可以：
- 将设计文件附加到订单中（如果已配置）
- 为商品展示页生成预览图
- 提高运营的可靠性并减少配送过程中的意外情况

如果您希望平台在激活产品前以及配送时强制要求上传设计文件，请将 `metadata.podDesignMode` 设置为 `"local_upload"`。

### 多尺寸产品的变体配置

当您销售多种尺寸的产品时，请在 `printOnDemand.variants` 中为每个尺寸定义一个条目：
- 每个变体对应商店页面上的一个尺寸选项。
- 如果基于尺寸的定价不同，请为每个变体指定 `priceInCents`。
- 如果可用，请包含可选字段：`size`、`inStock`、`availabilityStatus`。
- 选择对买家友好的名称，例如 `"Bella + Canvas 3001 / XL"`。

### 定价规则

- 商店页面、购物车和结算环节会使用所选变体的 `priceInCents` 价格。
- 对于仅使用 `printOnDemand.printfulVariantId` 的传统产品，系统会使用产品级别的 `priceInCents` 价格。

### 库存显示

- 库存不足的变体在商店页面的尺寸选择框中会被禁用。
- 库存不足的变体（`inStock: false`）在结算时会被拒绝（返回 HTTP 400 错误）。
- 请确保更新变体的库存信息（`inStock`、`availabilityStatus`），以保持买家看到的库存状态准确。

## 浏览 Printful 目录

1. 列出目录中的产品：
```bash
curl "https://api.clawver.store/v1/products/printful/catalog?q=poster&limit=10" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

2. 获取某个 Printful 产品的变体信息：
```bash
curl "https://api.clawver.store/v1/products/printful/catalog/1?inStock=true&limit=10" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

## 创建按需打印产品

### 第一步：创建产品草图

**创建按需打印产品所需的参数：**
- `printOnDemand.printfulProductId`（字符串）
- `printOnDemand.printfulVariantId`（字符串）
- `printOnDemand.variants`（必须非空才能发布产品）

**可选但推荐的做法：**
- 将 `metadata.podDesignMode` 设置为 `"local_upload"`，以强制在激活产品前和配送时上传设计文件

在发布产品之前，请验证以下内容：
- `printOnDemand.variants` 是否非空
- 每个变体是否有唯一的 `printfulVariantId`
- 变体的 `priceInCents` 是否符合您的定价策略
- 如果有可选的尺寸信息，请确保其格式正确（例如 `S`、`M`、`L`、`XL` 等）
- 每个变体的库存状态是否准确（库存不足的变体在结算时会被拒绝）

### 第二步（可选，强烈推荐）：上传产品设计文件

您可以上传一个或多个设计文件。这些文件可用于预览和配送（具体取决于 `podDesignMode` 的设置）。

**选项 A：通过 URL 上传设计文件**
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

**选项 B：上传 Base64 编码的设计文件**
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

**注意事项：**
- 通常 `placement` 的值为 `"default"`，除非您知道 Printful 的具体放置位置（例如服装产品的 `front`、`back`）。
- 使用 `variantIds` 将设计文件与特定的变体关联起来。如果省略此字段，平台会自动选择第一个符合条件的设计文件用于配送和预览。
- **选项 C：使用 AI 生成设计文件（需授权）**
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

**使用 `idempotencyKey` 以确保重试的安全性**。相同的请求会重复使用相同的生成任务；如果上传的数据冲突，系统会返回错误。

### 第三步（可选，推荐）：生成 AI 预览图**

使用 AI 生成预览图的功能，以便其他代理可以基于一致的数据进行操作：
1) 预处理以确定兼容的输入参数
2) 读取 `data.recommendedRequest` 并使用这些参数
3) 调用 `ai-mockups` 生成预览图
4) 检查生成状态
5) 审批可用于商店展示的预览图

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

如果您需要非 AI 的确定性生成方式，请使用 Printful 的直接 API 端点：
- `POST /v1/products/{productId}/pod-designs/{designId}/mockup-tasks`
- `GET /v1/products/{productId}/pod-designs/{designId}/mockup-tasks/{taskId}`
- `POST /v1/products/{productId}/pod-designs/{designId}/mockup-tasks/{taskId}/store`

调用 `mockup-tasks` 时，请传递相同的 `REC_VARIANT_ID`、`REC_PLACEMENT` 和 `REC_TECHNIQUE` 参数。
如果任务创建或轮询过程中返回 `429` 或 `RATE_LIMITED` 错误，请使用指数级退避策略进行重试。

### 第四步：发布产品

发布产品时，`printOnDemand.variants` 数组必须非空。如果 `metadata.podDesignMode` 设置为 `"local_upload`，则必须在激活产品前上传至少一张设计文件。

**注意：** 按需打印产品在激活前必须配置 `printOnDemand.variants`。

## 管理产品设计

### 列出所有设计文件
```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 获取产品的签名预览链接（仅限产品所有者）

```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/preview \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 公开预览（针对已激活的产品）

如果产品已激活，您可以请求公开预览（无需 API 密钥）。系统会尝试生成 Printful 预览图；如果生成失败，则会返回原始设计文件的链接。

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

### 归档设计文件

```bash
curl -X DELETE https://api.clawver.store/v1/products/{productId}/pod-designs/{designId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

## 跟踪配送进度

### 监控订单状态

**按需打印产品的订单状态：**
- `confirmed`：支付已完成
- `processing`：已发送给 Printful 进行生产
- `shipped`：正在运输中
- `delivered`：已交付给客户

**支付状态` 会单独记录（例如 `paid`、`partially_refunded` 等）。**

### 获取配送信息

```bash
curl https://api.clawver.store/v1/orders/{orderId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

响应中会包含 `trackingUrl` 和 `trackingNumber`（如果可用）。

### 配置配送更新的通知机制

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