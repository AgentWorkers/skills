---
name: clawver-print-on-demand
description: 在Clawver平台上销售按需打印的商品。您可以浏览Printful的商品目录，创建商品变体，并跟踪产品的配送和运输情况。该平台非常适合销售海报、T恤、马克杯或服装等实体产品。
version: 1.3.0
homepage: https://clawver.store
metadata: {"openclaw":{"emoji":"👕","homepage":"https://clawver.store","requires":{"env":["CLAW_API_KEY"]},"primaryEnv":"CLAW_API_KEY"}}
---

# Clawver 按需打印服务

您可以使用 Printful 的集成在 Clawver 平台上销售实体商品。无需库存——当客户下单时，商品会按需打印并发货。

## 先决条件

- 环境变量 `CLAW_API_KEY` 已设置
- 完成了与 Stripe 的集成
- 设计文件为高分辨率图片，格式为 HTTPS URL 或 Base64 编码的数据（平台会自动存储这些文件，无需外部托管；虽然非强制要求，但强烈建议）

有关 `claw-social` 中特定平台的 API 模式的详细信息（包括最佳实践和注意事项），请参阅 `references/api-examples.md`。

## 按需打印服务的运作原理

1. 您使用 Printful 的产品/变体 ID 创建商品。
2. 客户在您的商店中完成购买。
3. Printful 直接将商品打印并寄送给客户。
4. 您获得利润（您的售价减去 Printful 的基础成本以及 2% 的平台费用）。

## 关键概念（请先阅读）

### Printful ID 必须是字符串

`printOnDemand.printfulProductId` 和 `printOnDemand.printfulVariantId` 必须是字符串（例如 `"1"`、`4013"`），尽管 Printful 的目录返回的是数字 ID。

### 活动商品需要配置变体

在发布按需打印商品时（使用 `PATCH /v1/products/{id} {"status":"active"}` 请求），您的商品必须配置一个非空的 `printOnDemand.variants` 数组。

### 上传设计文件（强烈推荐）

您可以不上传设计文件即可销售按需打印商品（使用旧有的同步方式），但强烈建议上传设计文件，因为这可以：
- 将设计文件附加到订单中（如果进行了相应配置）
- 生成用于商品展示的图片预览
- 提高运营的可靠性，减少物流问题

如果您希望平台在商品激活前以及发货时强制要求上传设计文件，请将 `metadata.podDesignMode` 设置为 `"local_upload"`。

### 变体与尺寸选择的关系

当您销售多种尺寸的商品时，请在 `printOnDemand.variants` 中为每种尺寸定义一个条目：
- 每个变体对应商店界面中的一个尺寸选项。
- 如果基于尺寸的定价有所不同，请为每个变体指定 `priceInCents`。
- 如果可用，请包含可选字段：`size`、`inStock`、`availabilityStatus`。
- 使用对买家友好的名称，例如 `"Bella + Canvas 3001 / XL"`。

### 定价规则

- 商店界面、购物车和结账页面会使用所选变体的 `priceInCents` 价格。
- 对于仅包含 `printOnDemand.printfulVariantId` 的旧版商品，系统会使用商品级别的 `priceInCents` 作为默认价格。

### 库存显示

- 库存不足的变体在商店界面的尺寸选择器中会被隐藏。
- 库存不足的变体（`inStock: false`）会在结账时被拒绝（返回 HTTP 400 错误）。
- 请确保更新变体的库存信息（`inStock`、`availabilityStatus`），以保持商品信息的准确性。

## 浏览 Printful 目录

1. 列出目录中的商品：
```bash
curl "https://api.clawver.store/v1/products/printful/catalog?q=poster&limit=10" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

2. 获取某个 Printful 商品的变体信息：
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
- `metadata.podDesignMode: "local_upload"`，以强制在商品激活前和发货时上传设计文件

在发布之前，请验证：
- `printOnDemand.variants` 是否非空
- 每个变体是否有唯一的 `printfulVariantId`
- 变体的 `priceInCents` 是否符合您的定价策略
- 如果存在可选的尺寸信息，请确保其格式正确（例如 `S`、`M`、`L`、`XL` 等）
- 每个变体的库存状态是否准确（库存不足的变体会在结账时被拒绝）

### 第二步（可选，强烈推荐）：上传设计文件

将一个或多个设计文件上传到商品信息中。这些文件可用于预览和实际发货（具体取决于 `podDesignMode` 的设置）。

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

**注意：**
- 通常 `placement` 的值为 `"default"`，除非您知道 Printful 的具体放置位置（例如服装的正面/背面）。
- 使用 `variantIds` 将设计文件与特定的变体关联起来。如果未指定，平台会自动选择合适的文件用于发货和预览。

### 第三步（可选，推荐）：生成并缓存设计预览图

生成 Printful 的预览图，将其缓存到系统中，并在首次成功生成时设置商品的 `printOnDemand.primaryMockup` 属性（该预览图不会覆盖现有的主预览图）。
```bash
curl -X POST https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/mockup \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "placement": "default",
    "variantId": "4012"
  }'
```

如果预览图生成过程中出现错误，系统可能会返回 `202` 状态码，并提供 `retryAfterMs` 参数。请在指定时间后重试。

### 第四步：发布商品

发布商品时，`printOnDemand.variants` 数组必须非空。如果 `metadata.podDesignMode` 设置为 `"local_upload`，则必须在激活前上传至少一张设计文件。
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

### 获取设计的预览链接（仅限管理员）

```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/preview \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 公开预览（针对已激活的商品）

如果商品已激活，您可以请求公开预览（无需 API 密钥）。系统会尝试生成 Printful 的预览图；如果生成失败，则会返回设计的原始图片链接。
```bash
curl https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/public-preview
```

### 更新设计文件的元数据
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

## 跟踪商品发货情况

### 监控订单状态

```bash
curl "https://api.clawver.store/v1/orders?status=processing" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

按需打印商品的订单状态：
- `confirmed`：付款已完成
- `processing`：已发送给 Printful 进行生产
- `shipped`：正在运输中
- `delivered`：已送达客户

订单的付款状态（`paid`、`partially_refunded` 等）会单独记录。

### 获取物流信息

```bash
curl https://api.clawver.store/v1/orders/{orderId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

系统会返回 `trackingUrl` 和 `trackingNumber`（如果可用）。

### 配置发货通知的 Webhook

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