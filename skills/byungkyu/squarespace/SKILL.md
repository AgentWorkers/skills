---
name: squarespace
description: >
  **Squarespace Commerce API集成与托管型OAuth**  
  该功能支持用户通过OAuth身份验证来管理Squarespace网站上的产品、库存、订单、客户资料以及交易记录。  
  当用户需要操作Squarespace网站上的电子商务功能时，可选用此技能。  
  对于其他第三方应用程序，建议使用`api-gateway`技能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Squarespace

您可以使用托管的 OAuth 认证来访问 Squarespace Commerce API，该 API 支持产品、库存、订单、客户资料和交易的管理。

## 快速入门

```bash
# List all products (v2 API)
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/squarespace/v2/commerce/products')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('User-Agent', 'MyClaude/1.0')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/squarespace/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Squarespace API 端点路径。该网关会将请求代理到 `api.squarespace.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Squarespace OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=squarespace&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'squarespace'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "squarespace",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 Squarespace 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/squarespace/v2/commerce/products')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('User-Agent', 'MyClaude/1.0')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 库存

#### 列出所有库存

```bash
GET /squarespace/1.0/commerce/inventory
```

查询参数：
- `cursor`（可选）：上一次响应的分页游标

**响应：**
```json
{
  "inventory": [
    {
      "variantId": "5ba1418df4204bb2d21eac3f",
      "sku": "SQ0001",
      "descriptor": "Product Name - Size: Medium",
      "isUnlimited": false,
      "quantity": 25
    }
  ],
  "pagination": {
    "hasNextPage": true,
    "nextPageCursor": "abc123",
    "nextPageUrl": "https://api.squarespace.com/1.0/commerce/inventory?cursor=abc123"
  }
}
```

#### 获取特定库存信息

```bash
GET /squarespace/1.0/commerce/inventory/{variantIds}
```

- `{variantIds}`：用逗号分隔的变体 ID（最多 50 个）

#### 调整库存数量

```bash
POST /squarespace/1.0/commerce/inventory/adjustments
Content-Type: application/json
Idempotency-Key: unique-key-here

{
  "incrementOperations": [{"variantId": "variant-id-1", "quantity": 5}],
  "decrementOperations": [{"variantId": "variant-id-2", "quantity": 2}],
  "setFiniteOperations": [{"variantId": "variant-id-3", "quantity": 100}],
  "setUnlimitedOperations": ["variant-id-4"]
}
```

**响应：** 成功时返回 204（表示没有内容）。

---

### 订单

#### 列出所有订单

```bash
GET /squarespace/1.0/commerce/orders
```

查询参数：
- `customerId`（可选）：按客户 ID 过滤
- `modifiedAfter`（条件性）：ISO 8601 日期时间格式（例如 `2024-01-01T00:00:00Z`）——与 `modifiedBefore` 一起使用
- `modifiedBefore`（条件性）：ISO 8601 日期时间格式——与 `modifiedAfter` 一起使用
- `cursor`（可选）：分页游标
- `fulfillmentStatus`（可选）：`PENDING`、`FULFILLED` 或 `CANCELED`

注意：不能同时使用游标和日期范围参数。必须同时使用日期过滤器。

**响应：**
```json
{
  "result": [
    {
      "id": "order-id",
      "orderNumber": "1001",
      "createdOn": "2024-01-15T10:30:00Z",
      "modifiedOn": "2024-01-15T12:00:00Z",
      "channel": "web",
      "testmode": false,
      "customerEmail": "customer@example.com",
      "fulfillmentStatus": "PENDING",
      "lineItems": [...],
      "subtotal": {"value": "99.99", "currency": "USD"},
      "shippingTotal": {"value": "9.99", "currency": "USD"},
      "taxTotal": {"value": "8.50", "currency": "USD"},
      "grandTotal": {"value": "118.48", "currency": "USD"}
    }
  ],
  "pagination": {
    "hasNextPage": true,
    "nextPageCursor": "abc123",
    "nextPageUrl": "..."
  }
}
```

#### 获取特定订单信息

```bash
GET /squarespace/1.0/commerce/orders/{orderId}
```

#### 创建订单

```bash
POST /squarespace/1.0/commerce/orders
Content-Type: application/json
Idempotency-Key: unique-key-here

{
  "channelName": "External Store",
  "externalOrderReference": "ORDER-12345",
  "customerEmail": "customer@example.com",
  "lineItems": [
    {
      "lineItemType": "PHYSICAL_PRODUCT",
      "variantId": "variant-id",
      "quantity": 2,
      "unitPricePaid": {"currency": "USD", "value": "29.99"}
    }
  ],
  "subtotal": {"currency": "USD", "value": "59.98"},
  "priceTaxInterpretation": "EXCLUSIVE",
  "grandTotal": {"currency": "USD", "value": "59.98"},
  "createdOn": "2024-01-15T10:30:00Z"
}
```

**响应：** 创建成功时返回 201（并附带 Order 对象）

注意：`subtotal` 必须等于 `lineItems.unitPricePaid.value * quantity` 的总和。

#### 履行订单

```bash
POST /squarespace/1.0/commerce/orders/{orderId}/fulfillments
Content-Type: application/json

{
  "shouldSendNotification": true,
  "shipments": [
    {
      "shipDate": "2024-01-16T08:00:00Z",
      "carrierName": "USPS",
      "service": "Priority Mail",
      "trackingNumber": "9400111899223456789012",
      "trackingUrl": "https://tools.usps.com/go/TrackConfirmAction?tLabels=9400111899223456789012"
    }
  ]
}
```

**响应：** 成功时返回 204（表示没有内容）。

---

### 产品

#### 列出商店页面

```bash
GET /squarespace/1.0/commerce/store_pages
```

查询参数：
- `cursor`（可选）：分页游标

**响应：**
```json
{
  "storePages": [
    {
      "id": "store-page-id",
      "title": "Main Store",
      "isEnabled": true,
      "urlSlug": "store"
    }
  ],
  "pagination": {...}
}
```

#### 列出所有产品

```bash
GET /squarespace/v2/commerce/products
```

查询参数：
- `modifiedAfter`（可选）：ISO 8601 日期时间格式
- `modifiedBefore`（可选）：ISO 8601 日期时间格式
- `type`（可选）：用逗号分隔的类型：`PHYSICAL`、`SERVICE`、`GIFT_CARD`、`DIGITAL`
- `cursor`（可选）：分页游标

注意：不能同时使用游标和日期/类型过滤器。

**响应：**
```json
{
  "products": [
    {
      "id": "product-id",
      "type": "PHYSICAL",
      "storePageId": "store-page-id",
      "name": "Product Name",
      "description": "<p>HTML description</p>",
      "url": "https://example.squarespace.com/store/product-slug",
      "urlSlug": "product-slug",
      "tags": ["tag1", "tag2"],
      "isVisible": true,
      "variants": [...],
      "images": [...],
      "createdOn": "2024-01-01T00:00:00Z",
      "modifiedOn": "2024-01-15T12:00:00Z"
    }
  ],
  "pagination": {...}
}
```

#### 获取特定产品信息

```bash
GET /squarespace/v2/commerce/products/{productIds}
```

- `{productIds}`：用逗号分隔的产品 ID（最多 50 个）

#### 创建产品

```bash
POST /squarespace/v2/commerce/products
Content-Type: application/json

{
  "type": "PHYSICAL",
  "storePageId": "store-page-id",
  "name": "New Product",
  "description": "<p>Product description</p>",
  "urlSlug": "new-product",
  "tags": ["new", "featured"],
  "isVisible": true,
  "variants": [
    {
      "sku": "SKU-001",
      "pricing": {
        "basePrice": {"currency": "USD", "value": "49.99"}
      },
      "stock": {"quantity": 100, "unlimited": false}
    }
  ]
}
```

**响应：** 创建成功时返回 201（并附带 Product 对象）

#### 更新产品信息

```bash
POST /squarespace/v2/commerce/products/{productId}
Content-Type: application/json

{
  "name": "Updated Product Name",
  "description": "<p>Updated description</p>",
  "isVisible": true,
  "tags": ["updated", "sale"]
}
```

**响应：** 更新成功时返回 200（并附带 Product 对象）

#### 删除产品

```bash
DELETE /squarespace/v2/commerce/products/{productId}
```

**响应：** 删除成功时返回 204（表示没有内容）。

---

### 产品变体

#### 创建产品变体

```bash
POST /squarespace/v2/commerce/products/{productId}/variants
Content-Type: application/json

{
  "sku": "SKU-002",
  "pricing": {
    "basePrice": {"currency": "USD", "value": "59.99"},
    "salePrice": {"currency": "USD", "value": "49.99"},
    "onSale": true
  },
  "stock": {"quantity": 50, "unlimited": false},
  "attributes": {"Size": "Large"},
  "shippingMeasurements": {
    "weight": {"unit": "POUND", "value": 1.5},
    "dimensions": {"unit": "INCH", "length": 10, "width": 8, "height": 4}
  }
}
```

**响应：** 创建成功时返回 201（并附带 ProductVariant 对象）

注意：要使用 `attributes`，产品必须先通过更新产品设置相应的 `variantAttributes`（例如 `"variantAttributes": ["Size"]`）。

#### 更新产品变体

```bash
POST /squarespace/v2/commerce/products/{productId}/variants/{variantId}
Content-Type: application/json

{
  "sku": "SKU-002-UPDATED",
  "pricing": {
    "basePrice": {"currency": "USD", "value": "64.99"},
    "onSale": false
  }
}
```

**响应：** 更新成功时返回 200（并附带 ProductVariant 对象）

注意：此端点无法更新库存和图片信息。

#### 删除产品变体

```bash
DELETE /squarespace/v2/commerce/products/{productId}/variants/{variantId}
```

**响应：** 删除成功时返回 204（表示没有内容）

注意：不能删除产品的唯一变体。

---

### 产品图片

#### 上传图片

```bash
POST /squarespace/v2/commerce/products/{productId}/images
Content-Type: multipart/form-data

curl "https://gateway.maton.ai/squarespace/v2/commerce/products/{productId}/images" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "User-Agent: MyClaude/1.0" \
  -X POST \
  -F file=@image.png
```

**响应：** 202（表示图片已上传）

**要求：**
- 图片尺寸：小于 60MP
- 文件类型：JPEG、JPG、PNG、GIF
- 文件大小：最大 20MB（建议小于 500KB）
- 每个产品最多允许上传 100 张图片

#### 检查上传状态

```bash
GET /squarespace/v2/commerce/products/{productId}/images/{imageId}/status
```

**响应：**
```json
{
  "status": "PROCESSING"
}
```

状态值：`PROCESSING`、`READY`、`ERROR`

#### 更新图片（替代文本）

```bash
POST /squarespace/v2/commerce/products/{productId}/images/{imageId}
Content-Type: application/json

{
  "altText": "Product image description"
}
```

**响应：** 更新成功时返回 200（并附带 ProductImage 对象）

#### 重新排序图片

```bash
POST /squarespace/v2/commerce/products/{productId}/images/{imageId}/order
Content-Type: application/json

{
  "afterImageId": "other-image-id"
}
```

使用 `null` 作为 `afterImageId` 可将图片移动到顶部。

**响应：** 204（表示操作成功）

#### 将图片分配给产品变体

```bash
POST /squarespace/v2/commerce/products/{productId}/variants/{variantId}/image
Content-Type: application/json

{
  "imageId": "image-id"
}
```

使用 `null` 作为 `imageId` 可从产品变体中移除图片。

**响应：** 204（表示操作成功）

#### 删除图片

```bash
DELETE /squarespace/v2/commerce/products/{productId}/images/{imageId}
```

**响应：** 删除成功时返回 204（表示没有内容）

---

### 客户资料（Profiles）

#### 列出所有客户资料

```bash
GET /squarespace/1.0/profiles
```

查询参数：
- `cursor`（可选）：分页游标
- `filter`（可选）：用 semicolon 分隔的过滤条件（例如 `isCustomer,true;hasAccount,true`）
- `sortDirection`（可选）：`asc` 或 `dsc`（默认：`dsc`）
- `sortField`（可选）：`createdOn`、`id`、`email` 或 `lastName`（默认：`id`）

过滤选项：
- `isCustomer,true` 或 `isCustomer,false`
- `hasAccount,true` 或 `hasAccount,false`
- `email,customer@example.com`

**响应：**
```json
{
  "profiles": [
    {
      "id": "profile-id",
      "firstName": "John",
      "lastName": "Doe",
      "email": "john@example.com",
      "hasAccount": true,
      "isCustomer": true,
      "createdOn": "2024-01-01T00:00:00Z",
      "address": {
        "address1": "123 Main St",
        "city": "New York",
        "state": "NY",
        "countryCode": "US",
        "postalCode": "10001"
      },
      "acceptsMarketing": true,
      "transactionsSummary": {
        "orderCount": 5,
        "totalOrderAmount": {"value": "499.95", "currency": "USD"}
      }
    }
  ],
  "pagination": {...}
}
```

#### 获取特定客户资料

```bash
GET /squarespace/1.0/profiles/{profileIds}
```

- `{profileIds}`：用逗号分隔的客户资料 ID（最多 50 个）

---

### 交易

#### 列出所有交易记录

```bash
GET /squarespace/1.0/commerce/transactions
```

查询参数：
- `modifiedAfter`（条件性）：ISO 8601 日期时间格式——与 `modifiedBefore` 一起使用
- `modifiedBefore`（条件性）：ISO 8601 日期时间格式——与 `modifiedAfter` 一起使用
- `cursor`（可选）：分页游标

注意：在按日期过滤时，必须同时使用 `modifiedAfter` 和 `modifiedBefore`。

**响应：**
```json
{
  "documents": [
    {
      "id": "document-id",
      "createdOn": "2024-01-15T10:30:00Z",
      "modifiedOn": "2024-01-15T12:00:00Z",
      "customerEmail": "customer@example.com",
      "salesOrderId": "order-id",
      "voided": false,
      "totalSales": {"value": "99.99", "currency": "USD"},
      "totalNetSales": {"value": "99.99", "currency": "USD"},
      "totalTaxes": {"value": "8.50", "currency": "USD"},
      "total": {"value": "108.49", "currency": "USD"},
      "payments": [
        {
          "id": "payment-id",
          "amount": {"value": "108.49", "currency": "USD"},
          "creditCardType": "VISA",
          "provider": "STRIPE",
          "paidOn": "2024-01-15T10:35:00Z"
        }
      ]
    }
  ],
  "pagination": {...}
}
```

#### 获取特定交易记录

```bash
GET /squarespace/1.0/commerce/transactions/{documentIds}
```

- `{documentIds}`：用逗号分隔的交易记录 ID（最多 50 个）

---

## 分页

Squarespace 使用基于游标的分页机制。要获取下一页，请使用 `cursor` 参数：

```json
{
  "pagination": {
    "hasNextPage": true,
    "nextPageCursor": "cursor-value",
    "nextPageUrl": "https://api.squarespace.com/..."
  }
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/squarespace/v2/commerce/products',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'User-Agent': 'MyClaude/1.0'
    }
  }
);
const data = await response.json();
console.log(data.products);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/squarespace/v2/commerce/products',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'User-Agent': 'MyClaude/1.0'
    }
)
products = response.json()['products']
```

## 注意事项

- **产品 API 使用版本 `v2`**（例如，`/squarespace/v2/commerce/products`）
- 商店页面端点使用版本 `1.0`（例如，`/squarespace/1.0/commerce/store_pages`）
- 库存、订单、客户资料和交易 API 都使用版本 `1.0`
- 所有请求都需要包含描述您应用程序的 `User-Agent` 头部
- 没有自定义 `User-Agent` 的请求将受到更严格的速率限制
- 每批请求最多允许 50 个条目（库存、产品、客户资料、交易）
- 创建订单的速率限制更为严格：每个网站每小时最多 100 次请求
- 对于库存调整和创建订单操作，必须使用 `Idempotency-Key` 头部
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）在某些 shell 环境中可能无法正确显示

## 速率限制

- 一般限制：每分钟 300 次请求
- 创建订单：每个网站每小时最多 100 次请求（需要 API 密钥认证）
- 超过限制会导致返回 429 错误（表示请求过多），并需要等待 1 分钟后才能再次尝试

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求参数无效或缺少 Squarespace 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 405 | 对于该产品类型，不允许使用此方法 |
| 409 | 发生冲突（例如 SKU 重复、同时进行修改等） |
| 429 | 超过速率限制 |
| 4xx/5xx | 来自 Squarespace API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称错误

确保您的 URL 路径以 `squarespace` 开头。例如：

- 正确格式：`https://gateway.maton.ai/squarespace/1.0/commerce/products`
- 错误格式：`https://gateway.maton.ai/1.0/commerce/products`

## 资源

- [Squarespace Commerce API 概述](https://developers.squarespace.com/commerce-apis/overview)
- [库存 API](https://developers.squarespace.com/commerce-apis/inventory-overview)
- [订单 API](https://developers.squarespace.com/commerce-apis/orders-overview)
- [产品 API](https://developers.squarespace.com/commerce-apis/products-overview)
- [客户资料 API](https://developers.squarespace.com/commerce-apis/profiles-overview)
- [交易 API](https://developers.squarespace.com/commerce-apis/transactions-overview)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)