---
name: clawver-print-on-demand
description: 在 Clawver 上销售按需打印的商品。您可以浏览 Printful 的商品目录，创建产品变体，并跟踪产品的配送和运输情况。该工具非常适合用于销售海报、T恤、马克杯或服装等实物产品。
version: 1.3.0
homepage: https://clawver.store
metadata: {"openclaw":{"emoji":"👕","homepage":"https://clawver.store","requires":{"env":["CLAW_API_KEY"]},"primaryEnv":"CLAW_API_KEY"}}
---
# Clawver 按需打印服务

您可以通过与 Printful 的集成，在 Clawver 平台上销售实体商品。无需库存管理——客户下单后，商品会按需打印并寄出。

## 先决条件

- 环境变量 `CLAW_API_KEY` 已设置
- 已完成与 Stripe 的集成
- 设计文件需为高分辨率图片，格式为 HTTPS URL 或 Base64 编码的数据（平台会自动存储这些文件，无需外部托管；虽然非强制要求，但强烈建议）

有关特定于平台的 API 使用规范（包括最佳实践和注意事项），请参考 `references/api-examples.md`。

## 按需打印服务的运作原理

1. 您使用 Printful 的产品/变体 ID 创建商品。
2. 客户在您的商店中完成购买。
3. Printful 会直接将商品打印并寄送给客户。
4. 您可保留利润（您的售价减去 Printful 的基础成本以及 2% 的平台费用）。

## 关键概念（请先阅读）

### Printful ID 必须为字符串

`printOnDemand.printfulProductId` 和 `printOnDemand.printfulVariantId` 必须是字符串（例如 `"1"`、`4013"`），尽管 Printful 的目录返回的是数字 ID。

### 活动商品需要配置变体

在发布按需打印商品时（使用 `PATCH /v1/products/{id} {"status":"active"}` 方法），您的商品必须配置有非空的 `printOnDemand.variants` 数组。

### 上传设计文件（强烈建议）

您可以不上传设计文件即可销售按需打印商品（采用旧版或外部同步的工作流程），但强烈建议上传设计文件，因为这可以：
- 将设计文件附加到订单中（如果已配置）
- 生成用于商店展示的图片预览
- 提高运营的可靠性，并减少物流问题

如果您希望平台在商品激活前以及发货时强制要求上传设计文件，请将 `metadata.podDesignMode` 设置为 `"local_upload"`。

### 变体设置（用于选择商品尺寸）

当您销售多种尺寸的商品时，请在 `printOnDemand.variants` 中为每种尺寸定义一个条目：
- 每个变体对应商店展示中的一个尺寸选项。
- 如果基于尺寸的定价不同，请为每个变体指定 `priceInCents`。
- 如果可用，请包含可选字段：`size`、`inStock`、`availabilityStatus`。
- 使用对买家友好的名称，例如 `"Bella + Canvas 3001 / XL"`。

### 定价规则

- 商店展示、购物车和结账页面会使用所选变体的 `priceInCents` 价格。
- 仅使用 `printOnDemand.printfulVariantId` 的旧版商品会使用商品级别的 `priceInCents` 价格。

### 库存显示

- 库存不足的变体在商店的尺寸选择器中会被隐藏。
- 库存不足的变体（`inStock: false`）会在结账时被拒绝（返回 HTTP 400 错误）。
- 请保持变体的库存元数据（`inStock`、`availabilityStatus`）的准确性，以确保买家看到的信息是正确的。

## 浏览 Printful 目录

1. 列出目录中的商品：
```bash
curl "https://api.clawver.store/v1/products/printful/catalog?q=poster&limit=10" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

2. 获取某个 Printful 商品的详细信息（包括其变体）：
```bash
curl "https://api.clawver.store/v1/products/printful/catalog/1?inStock=true&limit=10" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

## 创建按需打印商品

### 第一步：创建商品（草稿）

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

创建/发布按需打印商品所需的信息：
- `printOnDemand.printfulProductId`（字符串）
- `printOnDemand.printfulVariantId`（字符串）
- `printOnDemand.variants`（必须非空才能发布）

建议但非强制要求：
- `metadata.podDesignMode: "local_upload"`——以确保在商品激活前和发货时上传设计文件

在发布之前，请验证：
- `printOnDemand.variants` 是否非空
- 每个变体是否有唯一的 `printfulVariantId`
- 变体的 `priceInCents` 是否符合您的定价策略
- 如果存在可选的尺寸信息，请确保其格式正确（如 `S`、`M`、`L`、`XL` 等）
- 每个变体的库存状态（`inStock`）是否准确；库存不足的变体在结账时会被拒绝

### 第二步（建议）：上传设计文件

您可以为商品上传一个或多个设计文件。这些文件可用于预览和实际发货（具体取决于 `podDesignMode` 的设置）：
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
- 使用 `variantIds` 将设计文件与特定的变体关联起来；如果省略，平台会自动选择合适的文件用于发货和预览。

### 第三步（建议）：生成 AI 预览图

您可以使用 AI 生成预览图的功能：
1) 预先检查输入数据的兼容性
2) 读取 `data.recommendedRequest` 并使用这些数据
3) 调用 `ai-mockups` 函数生成预览图
4) 查看生成状态
5) 审批生成的预览图是否适合用于商店展示

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

如果您需要非 AI 生成的方式，可以直接使用 Printful 的相关 API：
- `POST /v1/products/{productId}/pod-designs/{designId}/mockup-tasks`
- `GET /v1/products/{productId}/pod-designs/{designId}/mockup-tasks/{taskId}`
- `POST /v1/products/{productId}/pod-designs/{designId}/mockup-tasks/{taskId}/store`

调用 `mockup-tasks` 时，请传递相同的 `REC_VARIANT_ID`、`REC_PLACEMENT` 和 `REC_TECHNIQUE` 参数。
如果任务创建或查询返回 `429` 或 `RATE_LIMITED` 错误，请尝试重试，并采用指数级退避策略。

### 第四步：发布商品

发布商品时，`printOnDemand.variants` 数组必须非空。如果 `metadata.podDesignMode` 设置为 `"local_upload"`，则必须在激活前上传至少一张设计文件。

```bash
curl -X PATCH https://api.clawver.store/v1/products/{productId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

**注意：** 按需打印商品在激活前必须配置 `printOnDemand.variants`。

## 管理按需打印商品的设计文件

### 列出所有设计文件
```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 获取设计的预览 URL（仅限商品所有者）

```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/preview \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 公开预览（针对已激活的商品）

如果商品已激活，您可以请求公开预览（无需 API 密钥）。系统会尝试生成 Printful 预览图；如果生成失败，则会返回设计的原始图片 URL。

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

## 监控订单状态

### 监控订单进度

按需打印商品的订单状态包括：
- `confirmed`：付款已完成
- `processing`：已发送给 Printful 进行生产
- `shipped`：正在运输中（提供追踪信息）
- `delivered`：已交付给客户

订单的付款状态（`paid`、`partially_refunded` 等）会单独显示。

### 获取追踪信息

```bash
curl https://api.clawver.store/v1/orders/{orderId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

响应中会包含 `trackingUrl` 和 `trackingNumber`（如果可用）。

### 邮寄更新的通知

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