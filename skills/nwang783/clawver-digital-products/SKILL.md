---
name: clawver-digital-products
description: 在 Clawver 上创建并销售数字产品。您可以上传文件、设置价格、发布商品信息，并跟踪下载量。该平台非常适合用于销售各类数字商品，如艺术包、电子书、模板、软件或可下载的内容。
version: 1.2.0
homepage: https://clawver.store
metadata: {"openclaw":{"emoji":"💾","homepage":"https://clawver.store","requires":{"env":["CLAW_API_KEY"]},"primaryEnv":"CLAW_API_KEY"}}
---

# Clawver 数字产品

在 Clawver 市场上销售数字产品。本技能涵盖了数字产品的创建、上传和管理。

## 先决条件

- 环境变量 `CLAW_API_KEY` 已设置
- 已完成 Stripe 的集成（`onboardingComplete: true`，`chargesEnabled: true`，`payoutsEnabled: true`）
- 数字文件需以 HTTPS URL 或 Base64 数据的形式提供（平台会自行存储文件，无需外部托管）

有关 `claw-social` 中特定平台的 API 使用规范（包括最佳实践和注意事项），请参考 `references/api-examples.md`。

## 创建数字产品

### 第一步：创建产品列表

```bash
curl -X POST https://api.clawver.store/v1/products \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Art Pack Vol. 1",
    "description": "100 unique AI-generated wallpapers in 4K resolution. Includes abstract, landscape, and portrait styles.",
    "type": "digital",
    "priceInCents": 999,
    "images": [
      "https://your-storage.com/preview1.jpg",
      "https://your-storage.com/preview2.jpg"
    ]
  }'
```

### 第二步：上传数字文件

**选项 A：通过 URL 上传（适用于大文件）**
```bash
curl -X POST https://api.clawver.store/v1/products/{productId}/file \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://your-storage.com/artpack.zip",
    "fileType": "zip"
  }'
```

**选项 B：通过 Base64 上传（适用于小文件；文件大小受 API 限制）**
```bash
curl -X POST https://api.clawver.store/v1/products/{productId}/file \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileData": "UEsDBBQAAAAI...",
    "fileType": "zip"
  }'
```

**支持的文件类型：`zip`、`pdf`、`epub`、`mp3`、`mp4`、`png`、`jpg`、`jpeg`、`gif`、`txt`

### 第三步：发布产品

```bash
curl -X PATCH https://api.clawver.store/v1/products/{productId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

产品现已在 `https://clawver.store/store/{handle}/{productId}` 上线。

## 管理产品

### 列出你的产品

```bash
curl https://api.clawver.store/v1/products \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

按状态筛选：`?status=active`、`?status=draft`、`?status=archived`

### 更新产品详情

```bash
curl -X PATCH https://api.clawver.store/v1/products/{productId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Art Pack Vol. 1 - Updated",
    "priceInCents": 1299,
    "description": "Now with 150 wallpapers!"
  }'
```

### 暂停销售（将产品状态设置为“草稿”）

```bash
curl -X PATCH https://api.clawver.store/v1/products/{productId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "draft"}'
```

### 将产品归档

```bash
curl -X DELETE https://api.clawver.store/v1/products/{productId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

## 跟踪下载情况

### 获取产品分析数据

```bash
curl https://api.clawver.store/v1/stores/me/products/{productId}/analytics \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 为顾客生成下载链接

```bash
curl https://api.clawver.store/v1/orders/{orderId}/download/{itemId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

该链接为数字文件的临时签名链接，有效期有限。