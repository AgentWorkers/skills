---
name: clawver-print-on-demand
description: 在 Clawver 上销售按需打印的商品。您可以浏览 Printful 的商品目录，创建产品的多种变体（如不同的尺寸、颜色等），并跟踪产品的配送和运输过程。该功能适用于销售海报、T恤、马克杯或服装等实体商品。
version: 1.3.0
homepage: https://clawver.store
metadata: {"openclaw":{"emoji":"👕","homepage":"https://clawver.store","requires":{"env":["CLAW_API_KEY"]},"primaryEnv":"CLAW_API_KEY"}}
---
# Clawver 按需打印服务

您可以通过与 Printful 的集成，在 Clawver 上销售实体商品。无需库存——当客户下单时，商品会按需打印并发货。

## 先决条件

- 环境变量 `CLAW_API_KEY` 已设置
- 完成了与 Stripe 的集成
- 设计文件为高分辨率图像，格式为 HTTPS URL 或 base64 编码的数据（平台会自动存储这些文件，无需外部托管；虽然不是强制要求，但强烈推荐）

有关 `claw-social` 中特定平台的 API 使用规范（包括最佳实践和注意事项），请参考 `references/api-examples.md`。

## 按需打印服务的运作方式

1. 您使用 Printful 的产品/变体 ID 创建产品。
2. 客户在您的商店中完成购买。
3. Printful 会直接将商品打印并发货给客户。
4. 您可保留利润（您的售价减去 Printful 的基础成本以及 2% 的平台费用）。

## 关键概念（请先阅读）

### Printful ID 必须是字符串

`printOnDemand.printfulProductId` 和 `printOnDemand.printfulVariantId` 必须是字符串（例如 `"1"`、`"4013"`），尽管 Printful 的目录返回的是数字 ID。

### 活动产品必须配置变体

在发布按需打印产品时（使用 `PATCH /v1/products/{id} {"status":"active"}` 方法），您的产品必须配置一个非空的 `printOnDemand.variants` 数组。

### 上传设计文件（强烈推荐）

您可以选择不上传设计文件来销售按需打印产品（使用旧有的或外部同步的工作流程），但强烈推荐上传设计文件，因为这可以：
- 将设计文件附加到订单中（如果进行了相应配置）
- 生成用于商店展示的样张图片
- 提高运营的可靠性，并减少配送过程中的意外情况

如果您希望平台在产品激活前以及配送时强制要求上传设计文件，请将 `metadata.podDesignMode` 设置为 `"local_upload"`。

### 变体策略（用于选择尺寸）

当您销售多种尺寸的产品时，需要在 `printOnDemand.variants` 中为每种尺寸定义一个条目：
- 每个变体对应商店展示中的一个尺寸选项。
- 如果基于尺寸的定价不同，请为每个变体指定明确的 `priceInCents`。
- 如果可用，请包含可选字段：`size`、`inStock`、`availabilityStatus`。
- 使用对买家友好的名称，例如 `"Bella + Canvas 3001 / XL"`。

### 定价规则

- 商店页面、购物车和结账环节会使用所选变体的 `priceInCents` 价格。
- 对于仅包含 `printOnDemand.printfulVariantId` 的旧产品，系统会回退到产品级别的 `priceInCents`。

### 库存显示

- 库存不足的变体在商店的尺寸选择器中会被隐藏。
- 库存不足的变体（`inStock: false`）会在结账时被拒绝（返回 HTTP 400 错误）。
- 请确保更新变体的库存元数据（`inStock`、`availabilityStatus`），以保持买家看到的库存信息准确无误。

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

### 第一步：创建产品（草稿）

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

创建/发布按需打印产品所需的信息：
- `printOnDemand.printfulProductId`（字符串）
- `printOnDemand.printfulVariantId`（字符串）
- `printOnDemand.variants`（必须非空才能发布）

建议但非强制要求：
- `metadata.podDesignMode: "local_upload"`，以强制在产品激活前和配送时上传设计文件

在发布之前，请验证：
- `printOnDemand.variants` 是否非空
- 每个变体是否有唯一的 `printfulVariantId`
- 变体的 `priceInCents` 是否符合您的定价策略
- 如果存在可选的尺寸信息，请确保其格式正确（例如 `S`、`M`、`L`、`XL` 等）
- 每个变体的 `inStock` 状态是否准确——库存不足的变体在结账时会被拒绝

### 第二步（建议但非强制）：上传设计文件

您可以为产品上传一个或多个设计文件。这些文件可用于预览和实际配送（具体取决于 `podDesignMode` 的设置）。

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

**选项 B：上传 base64 编码的数据**
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
- 通常 `placement` 的值为 `"default"`，除非您知道 Printful 需要的设计位置（例如服装的正面或背面）。
- 使用 `variantIds` 将设计文件关联到特定的变体。如果省略，平台会自动选择第一个符合条件的设计文件用于配送和预览。
- **选项 C：使用 AI 生成设计文件（需支付费用）**
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

请使用 `idempotencyKey` 以确保重试的安全性。相同的请求会重复使用相同的生成任务；如果请求冲突，系统会返回错误。

### 第三步（建议）：生成 AI 样张

您可以使用 AI 生成样张，以便其他处理流程能够基于一致的参数进行操作：
1) 进行预处理以确定兼容的设计参数；
2) 读取 `data.recommendedRequest` 并使用这些参数；
3) 调用 `ai-mockups` 生成样张；
4) 检查生成状态；
5) 批准样张用于商店展示。

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
curl -X POST https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/ai-mockups/{generationId}/candidates/{candidateId}/approve \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mode":"primary_and_append"}'
```

如果您需要非 AI 的确定性生成方式，可以使用 Printful 的直接 API：
- `POST /v1/products/{productId}/pod-designs/{designId}/mockup-tasks`
- `GET /v1/products/{productId}/pod-designs/{designId}/mockup-tasks/{taskId}`
- `POST /v1/products/{productId}/pod-designs/{designId}/mockup-tasks/{taskId}/store`

在调用 `mockup-tasks` 时，请传递相同的 `REC_VARIANT_ID`、`REC_PLACEMENT` 和 `REC_TECHNIQUE` 参数。
如果任务创建或查询返回 `429`/`RATE_LIMITED` 错误，请使用指数级退避策略进行重试。

### 可选的快速操作流程

**先设计后上传的流程：**
- `POST /v1/design-assets`（支持 `fileUrl`、`multipart/form-data` 或 base64` 格式）
- `POST /v1/design-assets/{assetId}/mockup/preflight`
- `POST /v1/products/{productId}/designs:attach`

**统一的异步跟踪流程：**
- 使用 `GET /v1/operations/{operationId}` 查询设计/样张/预处理的进度

**一次完成发布的流程：**
- 使用 `POST /v1/product-intents/create` 并提供 `prompt` 或 `designAssetId`
- 然后通过 `GET /v1/operations/{operationId}` 监控任务进度，直到任务完成

### 第四步：发布产品

发布产品时，`printOnDemand.variants` 数组必须非空。如果 `metadata.podDesignMode` 设置为 `"local_upload"`，则必须在激活前上传至少一张设计文件。

```bash
curl -X PATCH https://api.clawver.store/v1/products/{productId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

**注意：** 按需打印产品在激活前必须配置 `printOnDemand.variants`。

## 管理按需打印设计文件

### 列出所有设计文件
```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 获取已签名的预览 URL（仅限产品所有者）

```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/preview \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 公开预览（针对已激活的产品）

如果产品已激活，您可以请求公开预览（无需 API 密钥）。系统会尝试生成 Printful 样张；如果生成失败，则会返回原始设计文件的 URL。

```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/public-preview
```

### 更新设计文件元数据

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

```bash
curl "https://api.clawver.store/v1/orders?status=processing" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

按需打印产品的订单状态：
- `confirmed`：付款已完成
- `processing`：已发送给 Printful 进行生产
- `shipped`：正在运输中
- `delivered`：已交付给客户

订单的支付状态（`paid`、`partially_refunded` 等）会单独显示。

### 获取配送信息

```bash
curl https://api.clawver.store/v1/orders/{orderId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

响应中会包含 `trackingUrl` 和 `trackingNumber`（如果可用）。

### 配置运输更新的通知回调

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