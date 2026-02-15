---
name: woocommerce
description: |
  WooCommerce REST API integration with managed OAuth. Access products, orders, customers, coupons, shipping, taxes, reports, and webhooks. Use this skill when users want to manage e-commerce operations, process orders, or integrate with WooCommerce stores. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# WooCommerce

您可以使用管理的 OAuth 认证来访问 WooCommerce REST API。该 API 可用于管理电子商务操作中的产品、订单、客户、优惠券、运费、税费等。

## 快速入门

```bash
# List products
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/woocommerce/wp-json/wc/v3/products')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/woocommerce/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 WooCommerce API 端点路径。该网关会将请求代理到您的 WooCommerce 商店，并自动处理认证。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 WooCommerce OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=woocommerce&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'woocommerce'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接

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
    "app": "woocommerce",
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

如果您有多个 WooCommerce 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/woocommerce/wp-json/wc/v3/products')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 产品

#### 列出所有产品

```bash
GET /woocommerce/wp-json/wc/v3/products
```

查询参数：
- `page` - 当前页码（默认值：1）
- `per_page` - 每页显示的项数（默认值：10，最大值：100）
- `search` - 按产品名称搜索
- `status` - 按状态过滤：`draft`、`pending`、`private`、`publish`
- `type` - 按类型过滤：`simple`、`grouped`、`external`、`variable`
- `sku` - 按 SKU 过滤
- `category` - 按类别 ID 过滤
- `tag` - 按标签 ID 过滤
- `featured` - 过滤特色产品
- `on_sale` - 过滤促销产品
- `min_price` / `max_price` - 按价格范围过滤
- `stock_status` - 按库存状态过滤：`instock`、`outofstock`、`onbackorder`
- `orderby` - 排序方式：`date`、`id`、`include`、`title`、`slug`、`price`、`popularity`、`rating`
- `order` - 排序顺序：`asc`、`desc`

**示例：**

```bash
curl -s -X GET "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/products?per_page=20&status=publish" -H "Authorization: Bearer $MATON_API_KEY"
```

**响应：**
```json
[
  {
    "id": 123,
    "name": "Premium T-Shirt",
    "slug": "premium-t-shirt",
    "type": "simple",
    "status": "publish",
    "sku": "TSH-001",
    "price": "29.99",
    "regular_price": "34.99",
    "sale_price": "29.99",
    "stock_quantity": 50,
    "stock_status": "instock",
    "categories": [{"id": 15, "name": "Apparel"}],
    "images": [{"id": 456, "src": "https://..."}]
  }
]
```

#### 获取产品信息

```bash
GET /woocommerce/wp-json/wc/v3/products/{id}
```

**示例：**

```bash
curl -s -X GET "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/products/123" -H "Authorization: Bearer $MATON_API_KEY"
```

#### 创建产品

```bash
POST /woocommerce/wp-json/wc/v3/products
Content-Type: application/json

{
  "name": "New Product",
  "type": "simple",
  "regular_price": "49.99",
  "description": "Full product description",
  "short_description": "Brief description",
  "sku": "PROD-001",
  "manage_stock": true,
  "stock_quantity": 100,
  "categories": [{"id": 15}],
  "images": [{"src": "https://example.com/image.jpg"}]
}
```

**示例：**

```bash
curl -s -X POST "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/products" -H "Content-Type: application/json" -H "Authorization: Bearer $MATON_API_KEY" -d '{"name": "Premium Widget", "type": "simple", "regular_price": "19.99", "sku": "WDG-001"}'
```

#### 更新产品信息

```bash
PUT /woocommerce/wp-json/wc/v3/products/{id}
```

**示例：**

```bash
curl -s -X PUT "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/products/123" -H "Content-Type: application/json" -H "Authorization: Bearer $MATON_API_KEY" -d '{"regular_price": "24.99", "sale_price": "19.99"}'
```

#### 删除产品

```bash
DELETE /woocommerce/wp-json/wc/v3/products/{id}
```

查询参数：
- `force` - 设置为 `true` 以永久删除产品（默认值：`false` 表示将产品移至待删除列表）

#### 复制产品

```bash
POST /woocommerce/wp-json/wc/v3/products/{id}/duplicate
```

### 产品变体

对于可变产品，您可以管理其各个变体：

#### 列出变体

```bash
GET /woocommerce/wp-json/wc/v3/products/{product_id}/variations
```

#### 创建变体

```bash
POST /woocommerce/wp-json/wc/v3/products/{product_id}/variations
Content-Type: application/json

{
  "regular_price": "29.99",
  "sku": "TSH-001-RED-M",
  "attributes": [
    {"id": 1, "option": "Red"},
    {"id": 2, "option": "Medium"}
  ]
}
```

#### 更新变体

```bash
PUT /woocommerce/wp-json/wc/v3/products/{product_id}/variations/{id}
```

#### 删除变体

```bash
DELETE /woocommerce/wp-json/wc/v3/products/{product_id}/variations/{id}
```

#### 批量更新变体

```bash
POST /woocommerce/wp-json/wc/v3/products/{product_id}/variations/batch
```

### 产品属性

#### 列出属性

```bash
GET /woocommerce/wp-json/wc/v3/products/attributes
```

#### 创建属性

```bash
POST /woocommerce/wp-json/wc/v3/products/attributes
Content-Type: application/json

{
  "name": "Color",
  "slug": "color",
  "type": "select",
  "order_by": "menu_order"
}
```

#### 获取/更新/删除属性

```bash
GET /woocommerce/wp-json/wc/v3/products/attributes/{id}
PUT /woocommerce/wp-json/wc/v3/products/attributes/{id}
DELETE /woocommerce/wp-json/wc/v3/products/attributes/{id}
```

### 属性术语

```bash
GET /woocommerce/wp-json/wc/v3/products/attributes/{attribute_id}/terms
POST /woocommerce/wp-json/wc/v3/products/attributes/{attribute_id}/terms
GET /woocommerce/wp-json/wc/v3/products/attributes/{attribute_id}/terms/{id}
PUT /woocommerce/wp-json/wc/v3/products/attributes/{attribute_id}/terms/{id}
DELETE /woocommerce/wp-json/wc/v3/products/attributes/{attribute_id}/terms/{id}
```

### 产品类别

#### 列出类别

```bash
GET /woocommerce/wp-json/wc/v3/products/categories
```

#### 创建类别

```bash
POST /woocommerce/wp-json/wc/v3/products/categories
Content-Type: application/json

{
  "name": "Electronics",
  "parent": 0,
  "description": "Electronic products"
}
```

#### 获取/更新/删除类别

```bash
GET /woocommerce/wp-json/wc/v3/products/categories/{id}
PUT /woocommerce/wp-json/wc/v3/products/categories/{id}
DELETE /woocommerce/wp-json/wc/v3/products/categories/{id}
```

### 产品标签

```bash
GET /woocommerce/wp-json/wc/v3/products/tags
POST /woocommerce/wp-json/wc/v3/products/tags
GET /woocommerce/wp-json/wc/v3/products/tags/{id}
PUT /woocommerce/wp-json/wc/v3/products/tags/{id}
DELETE /woocommerce/wp-json/wc/v3/products/tags/{id}
```

### 产品运费类别

```bash
GET /woocommerce/wp-json/wc/v3/products/shipping_classes
POST /woocommerce/wp-json/wc/v3/products/shipping_classes
GET /woocommerce/wp-json/wc/v3/products/shipping_classes/{id}
PUT /woocommerce/wp-json/wc/v3/products/shipping_classes/{id}
DELETE /woocommerce/wp-json/wc/v3/products/shipping_classes/{id}
```

### 产品评论

#### 列出评论

```bash
GET /woocommerce/wp-json/wc/v3/products/reviews
```

查询参数：
- `product` - 按产品 ID 过滤
- `status` - 按状态过滤：`approved`、`hold`、`spam`、`trash`

#### 创建评论

```bash
POST /woocommerce/wp-json/wc/v3/products/reviews
Content-Type: application/json

{
  "product_id": 123,
  "review": "Great product!",
  "reviewer": "John Doe",
  "reviewer_email": "john@example.com",
  "rating": 5
}
```

#### 获取/更新/删除评论

```bash
GET /woocommerce/wp-json/wc/v3/products/reviews/{id}
PUT /woocommerce/wp-json/wc/v3/products/reviews/{id}
DELETE /woocommerce/wp-json/wc/v3/products/reviews/{id}
```

---

### 订单

#### 列出所有订单

```bash
GET /woocommerce/wp-json/wc/v3/orders
```

查询参数：
- `page` - 当前页码（默认值：1）
- `per_page` - 每页显示的项数（默认值：10）
- `search` - 搜索订单
- `after` / `before` - 按日期（ISO8601 格式）过滤
- `status` - 订单状态（见下文）
- `customer` - 按客户 ID 过滤
- `product` - 按产品 ID 过滤
- `orderby` - 排序方式：`date`、`id`、`include`、`title`、`slug`
- `order` - 排序顺序：`asc`、`desc`

**订单状态：**
- `pending` - 支付待处理
- `processing` - 支付已收到，等待发货
- `on-hold` - 等待支付确认
- `completed` - 订单已发货
- `cancelled` - 由管理员或客户取消
- `refunded` - 已全额退款
- `failed` - 支付失败

**示例：**

```bash
curl -s -X GET "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/orders?status=processing&per_page=50" -H "Authorization: Bearer $MATON_API_KEY"
```

**响应：**
```json
[
  {
    "id": 456,
    "status": "processing",
    "currency": "USD",
    "total": "129.99",
    "customer_id": 12,
    "billing": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com"
    },
    "line_items": [
      {
        "id": 789,
        "product_id": 123,
        "name": "Premium T-Shirt",
        "quantity": 2,
        "total": "59.98"
      }
    ]
  }
]
```

#### 获取订单信息

```bash
GET /woocommerce/wp-json/wc/v3/orders/{id}
```

#### 创建订单

```bash
POST /woocommerce/wp-json/wc/v3/orders
Content-Type: application/json

{
  "payment_method": "stripe",
  "payment_method_title": "Credit Card",
  "set_paid": true,
  "billing": {
    "first_name": "John",
    "last_name": "Doe",
    "address_1": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "postcode": "12345",
    "country": "US",
    "email": "john@example.com",
    "phone": "555-1234"
  },
  "shipping": {
    "first_name": "John",
    "last_name": "Doe",
    "address_1": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "postcode": "12345",
    "country": "US"
  },
  "line_items": [
    {
      "product_id": 123,
      "quantity": 2
    }
  ]
}
```

#### 更新订单信息

**示例 - 更新订单状态：**

```bash
curl -s -X PUT "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/orders/456" -H "Content-Type: application/json" -H "Authorization: Bearer $MATON_API_KEY" -d '{"status": "completed"}'
```

#### 删除订单

```bash
DELETE /woocommerce/wp-json/wc/v3/orders/{id}
```

### 订单备注

#### 列出订单备注

```bash
GET /woocommerce/wp-json/wc/v3/orders/{order_id}/notes
```

#### 创建订单备注

```bash
POST /woocommerce/wp-json/wc/v3/orders/{order_id}/notes
Content-Type: application/json

{
  "note": "Order shipped via FedEx, tracking #12345",
  "customer_note": true
}
```

- `customer_note`：设置为 `true` 以使备注对客户可见

#### 获取/删除订单备注

```bash
GET /woocommerce/wp-json/wc/v3/orders/{order_id}/notes/{id}
DELETE /woocommerce/wp-json/wc/v3/orders/{order_id}/notes/{id}
```

### 订单退款

#### 列出退款记录

```bash
GET /woocommerce/wp-json/wc/v3/orders/{order_id}/refunds
```

#### 创建退款

```bash
POST /woocommerce/wp-json/wc/v3/orders/{order_id}/refunds
Content-Type: application/json

{
  "amount": "25.00",
  "reason": "Product damaged during shipping",
  "api_refund": true
}
```

- `api_refund`：设置为 `true` 以通过支付网关处理退款

#### 获取/删除退款记录

```bash
GET /woocommerce/wp-json/wc/v3/orders/{order_id}/refunds/{id}
DELETE /woocommerce/wp-json/wc/v3/orders/{order_id}/refunds/{id}
```

---

### 客户

#### 列出所有客户

```bash
GET /woocommerce/wp-json/wc/v3/customers
```

查询参数：
- `page` - 当前页码（默认值：1）
- `per_page` - 每页显示的项数（默认值：10）
- `search` - 按名称或电子邮件搜索
- `email` - 按电子邮件地址精确过滤
- `role` - 按角色过滤：`all`、`administrator`、`customer`、`shop_manager`
- `orderby` - 排序方式：`id`、`include`、`name`、`registered_date`
- `order` - 排序顺序：`asc`、`desc`

**示例：**

```bash
curl -s -X GET "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/customers?per_page=25" -H "Authorization: Bearer $MATON_API_KEY"
```

**响应：**
```json
[
  {
    "id": 12,
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe",
    "billing": {
      "first_name": "John",
      "last_name": "Doe",
      "address_1": "123 Main St",
      "city": "Anytown",
      "state": "CA",
      "postcode": "12345",
      "country": "US",
      "email": "john@example.com",
      "phone": "555-1234"
    },
    "shipping": {
      "first_name": "John",
      "last_name": "Doe",
      "address_1": "123 Main St",
      "city": "Anytown",
      "state": "CA",
      "postcode": "12345",
      "country": "US"
    }
  }
]
```

#### 获取客户信息

```bash
GET /woocommerce/wp-json/wc/v3/customers/{id}
```

#### 创建客户

```bash
POST /woocommerce/wp-json/wc/v3/customers
Content-Type: application/json

{
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "username": "janesmith",
  "password": "secure_password",
  "billing": {
    "first_name": "Jane",
    "last_name": "Smith",
    "address_1": "456 Oak Ave",
    "city": "Springfield",
    "state": "IL",
    "postcode": "62701",
    "country": "US",
    "email": "jane@example.com",
    "phone": "555-5678"
  }
}
```

#### 更新客户信息

```bash
PUT /woocommerce/wp-json/wc/v3/customers/{id}
```

#### 删除客户

```bash
DELETE /woocommerce/wp-json/wc/v3/customers/{id}
```

### 客户下载内容

```bash
GET /woocommerce/wp-json/wc/v3/customers/{customer_id}/downloads
```

返回客户可以下载的产品信息。

---

### 优惠券

#### 列出所有优惠券

```bash
GET /woocommerce/wp-json/wc/v3/coupons
```

查询参数：
- `page` - 当前页码（默认值：1）
- `per_page` - 每页显示的项数（默认值：10）
- `search` - 搜索优惠券
- `code` - 按优惠券代码过滤

#### 获取优惠券信息

```bash
GET /woocommerce/wp-json/wc/v3/coupons/{id}
```

#### 创建优惠券

```bash
POST /woocommerce/wp-json/wc/v3/coupons
Content-Type: application/json

{
  "code": "SUMMER2024",
  "discount_type": "percent",
  "amount": "15",
  "description": "Summer promotion - 15% off",
  "date_expires": "2024-08-31T23:59:59",
  "individual_use": true,
  "usage_limit": 100,
  "usage_limit_per_user": 1,
  "minimum_amount": "50.00",
  "maximum_amount": "500.00",
  "free_shipping": false,
  "exclude_sale_items": true
}
```

**折扣类型：**
- `percent` - 百分比折扣
- `fixed_cart` - 全部购物车固定金额折扣
- `fixed_product` - 每个产品固定金额折扣

**优惠券属性：**
- `code` - 优惠券代码（必填）
- `amount` - 折扣金额
- `discount_type` - 折扣类型
- `description` - 优惠券描述
- `date_expires` - 有效期（ISO8601 格式）
- `individual_use` - 不能与其他优惠券合并使用
- `product_ids` - 优惠券适用的产品 ID 列表
- `excluded_product_ids` - 被排除的产品 ID 列表
- `usage_limit` - 优惠券可使用次数
- `usage_limit_per_user` - 每位用户的使用限制
- `limit_usage_to_x_items` - 折扣适用的最大商品数量
- `free_shipping` - 启用免费配送
- `product_categories` - 适用的商品类别 ID 列表
- `excluded_product_categories` - 被排除的商品类别 ID 列表
- `exclude_sale_items` - 排除促销商品
- `minimum_amount` - 最小购物车总额要求
- `maximum_amount` - 最大购物车总额限制
- `emailrestrictions` - 允许的电子邮件地址列表

#### 更新优惠券

```bash
PUT /woocommerce/wp-json/wc/v3/coupons/{id}
```

#### 删除优惠券

```bash
DELETE /woocommerce/wp-json/wc/v3/coupons/{id}
```

---

### 税费

#### 税率

```bash
GET /woocommerce/wp-json/wc/v3/taxes
POST /woocommerce/wp-json/wc/v3/taxes
GET /woocommerce/wp-json/wc/v3/taxes/{id}
PUT /woocommerce/wp-json/wc/v3/taxes/{id}
DELETE /woocommerce/wp-json/wc/v3/taxes/{id}
POST /woocommerce/wp-json/wc/v3/taxes/batch
```

**创建税率示例：**

```bash
curl -s -X POST "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/taxes" -H "Content-Type: application/json" -H "Authorization: Bearer $MATON_API_KEY" -d '{"country": "US", "state": "CA", "rate": "7.25", "name": "CA State Tax", "shipping": true}'
```

#### 税类

```bash
GET /woocommerce/wp-json/wc/v3/taxes/classes
POST /woocommerce/wp-json/wc/v3/taxes/classes
DELETE /woocommerce/wp-json/wc/v3/taxes/classes/{slug}
```

---

### 运费

#### 运费区域

```bash
GET /woocommerce/wp-json/wc/v3/shipping/zones
POST /woocommerce/wp-json/wc/v3/shipping/zones
GET /woocommerce/wp-json/wc/v3/shipping/zones/{id}
PUT /woocommerce/wp-json/wc/v3/shipping/zones/{id}
DELETE /woocommerce/wp-json/wc/v3/shipping/zones/{id}
```

**创建运费区域示例：**

```bash
curl -s -X POST "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/shipping/zones" -H "Content-Type: application/json" -H "Authorization: Bearer $MATON_API_KEY" -d '{"name": "US West Coast", "order": 1}'
```

#### 更新运费区域信息

```bash
GET /woocommerce/wp-json/wc/v3/shipping/zones/{zone_id}/locations
PUT /woocommerce/wp-json/wc/v3/shipping/zones/{zone_id}/locations
```

#### 运费区域位置信息

```bash
curl -s -X PUT "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/shipping/zones/1/locations" -H "Content-Type: application/json" -H "Authorization: Bearer $MATON_API_KEY" -d '[{"code": "US:CA", "type": "state"}, {"code": "US:OR", "type": "state"}, {"code": "US:WA", "type": "state"}]'
```

#### 更新运费区域位置信息

```bash
curl -s -X PUT "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/shipping/zones/1/locations" -H "Content-Type: application/json" -H "Authorization: Bearer $MATON_API_KEY" -d '[{"code": "US:CA", "type": "state"}, {"code": "US:OR", "type": "state"}, {"code": "US:WA", "type": "state"}]'
```

#### 运费方式

```bash
GET /woocommerce/wp-json/wc/v3/shipping/zones/{zone_id}/methods
POST /woocommerce/wp-json/wc/v3/shipping/zones/{zone_id}/methods
GET /woocommerce/wp-json/wc/v3/shipping/zones/{zone_id}/methods/{id}
PUT /woocommerce/wp-json/wc/v3/shipping/zones/{zone_id}/methods/{id}
DELETE /woocommerce/wp-json/wc/v3/shipping/zones/{zone_id}/methods/{id}
```

#### 全局运费方式

```bash
GET /woocommerce/wp-json/wc/v3/shipping_methods
GET /woocommerce/wp-json/wc/v3/shipping_methods/{id}
```

---

### 支付网关

```bash
GET /woocommerce/wp-json/wc/v3/payment_gateways
GET /woocommerce/wp-json/wc/v3/payment_gateways/{id}
PUT /woocommerce/wp-json/wc/v3/payment_gateways/{id}
```

**示例 - 启用支付网关：**

```bash
curl -s -X PUT "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/payment_gateways/stripe" -H "Content-Type: application/json" -H "Authorization: Bearer $MATON_API_KEY" -d '{"enabled": true}'
```

---

### 设置

#### 列出设置组

```bash
GET /woocommerce/wp-json/wc/v3/settings
```

#### 列出组内的设置

```bash
GET /woocommerce/wp-json/wc/v3/settings/{group}
```

常见组：`general`、`products`、`tax`、`shipping`、`checkout`、`account`、`email`

#### 获取/更新设置

```bash
GET /woocommerce/wp-json/wc/v3/settings/{group}/{id}
PUT /woocommerce/wp-json/wc/v3/settings/{group}/{id}
```

**示例 - 更新商店地址：**

```bash
curl -s -X PUT "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/settings/general/woocommerce_store_address" -H "Content-Type: application/json" -H "Authorization: Bearer $MATON_API_KEY" -d '{"value": "123 Commerce St"}'
```

#### 批量更新设置

```bash
POST /woocommerce/wp-json/wc/v3/settings/{group}/batch
```

---

### Webhook

#### 列出所有 Webhook

```bash
GET /woocommerce/wp-json/wc/v3/webhooks
```

#### 创建 Webhook

```bash
POST /woocommerce/wp-json/wc/v3/webhooks
Content-Type: application/json

{
  "name": "Order Created",
  "topic": "order.created",
  "delivery_url": "https://example.com/webhooks/woocommerce",
  "status": "active"
}
```

**Webhook 主题：**
- `order.created`、`order.updated`、`orderdeleted`、`order.restored`
- `product.created`、`product.updated`、`productdeleted`、`product.restored`
- `customer.created`、`customer.updated`、`customerdeleted`
- `coupon-created`、`coupon.updated`、`coupondeleted`、`coupon.restored`

#### 获取/更新/删除 Webhook

```bash
GET /woocommerce/wp-json/wc/v3/webhooks/{id}
PUT /woocommerce/wp-json/wc/v3/webhooks/{id}
DELETE /woocommerce/wp-json/wc/v3/webhooks/{id}
```

---

### 报告

#### 列出可用报告

```bash
GET /woocommerce/wp-json/wc/v3/reports
```

#### 销售报告

```bash
GET /woocommerce/wp-json/wc/v3/reports/sales
```

查询参数：
- `period` - 报告周期：`week`、`month`、`last_month`、`year`
- `date_min` / `date_max` - 自定义日期范围

#### 热销商品报告

```bash
GET /woocommerce/wp-json/wc/v3/reports/top_sellers
```

#### 优惠券汇总

```bash
GET /woocommerce/wp-json/wc/v3/reports/coupons/totals
```

#### 客户汇总

```bash
GET /woocommerce/wp-json/wc/v3/reports/customers/totals
```

#### 订单汇总

```bash
GET /woocommerce/wp-json/wc/v3/reports/orders/totals
```

#### 产品汇总

```bash
GET /woocommerce/wp-json/wc/v3/reports/products/totals
```

#### 评论汇总

```bash
GET /woocommerce/wp-json/wc/v3/reports/reviews/totals
```

---

### 数据

#### 列出所有数据端点

```bash
GET /woocommerce/wp-json/wc/v3/data
```

#### 大陆

```bash
GET /woocommerce/wp-json/wc/v3/data/continents
GET /woocommerce/wp-json/wc/v3/data/continents/{code}
```

#### 国家

```bash
GET /woocommerce/wp-json/wc/v3/data/countries
GET /woocommerce/wp-json/wc/v3/data/countries/{code}
```

#### 货币

```bash
GET /woocommerce/wp-json/wc/v3/data/currencies
GET /woocommerce/wp-json/wc/v3/data/currencies/{code}
GET /woocommerce/wp-json/wc/v3/data/currencies/current
```

---

### 系统状态

```bash
GET /woocommerce/wp-json/wc/v3/system_status
GET /woocommerce/wp-json/wc/v3/system_status/tools
POST /woocommerce/wp-json/wc/v3/system_status/tools/{id}
```

---

## 批量操作

大多数资源支持批量操作，可以创建、更新和删除多个项目：

```bash
POST /woocommerce/wp-json/wc/v3/{resource}/batch
Content-Type: application/json

{
  "create": [
    {"name": "New Product 1", "regular_price": "19.99"},
    {"name": "New Product 2", "regular_price": "29.99"}
  ],
  "update": [
    {"id": 123, "regular_price": "24.99"}
  ],
  "delete": [456, 789]
}
```

**响应：**
```json
{
  "create": [...],
  "update": [...],
  "delete": [...]
}
```

## 分页

WooCommerce 使用基于页面的分页机制，并在响应头中提供相关信息：

**查询参数：**
- `page` - 页码（默认值：1）
- `per_page` - 每页显示的项数（默认值：10，最大值：100）
- `offset` - 开始的偏移量

**响应头：**
- `X-WP-Total` - 总项目数
- `X-WP-TotalPages` - 总页数
- `Link` - 包含 `next`、`prev`、`first`、`last` 分页链接

**示例：**

```bash
curl -s -I -X GET "https://gateway.maton.ai/woocommerce/wp-json/wc/v3/products?page=2&per_page=25" -H "Authorization: Bearer $MATON_API_KEY"
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/woocommerce/wp-json/wc/v3/orders?status=processing',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const orders = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/woocommerce/wp-json/wc/v3/products',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'per_page': 50, 'status': 'publish'}
)
products = response.json()
```

### 使用商品明细创建订单

```python
import os
import requests

order_data = {
    "payment_method": "stripe",
    "set_paid": True,
    "billing": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "address_1": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "postcode": "12345",
        "country": "US"
    },
    "line_items": [
        {"product_id": 123, "quantity": 2},
        {"product_id": 456, "quantity": 1}
    ]
}

response = requests.post(
    'https://gateway.maton.ai/woocommerce/wp-json/wc/v3/orders',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json=order_data
)
order = response.json()
```

## 注意事项

- 所有货币金额均以保留两位小数的字符串形式返回。
- 日期采用 ISO8601 格式：`YYYY-MM-DDTHH:MM:SS`。
- 资源 ID 为整数。
- API 要求在 WordPress 中启用“漂亮永久链接”（pretty permalinks）功能。
- 使用 `context=edit` 参数可以访问可写入的字段。
- 重要提示：当使用 curl 命令时，如果 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`），请使用 `curl -g` 以避免全局解析问题。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析，可能会导致“无效 API 密钥”错误。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 请求错误或数据无效 |
| 401 | 认证无效或缺失 |
| 403 | 禁止访问 - 权限不足 |
| 404 | 资源未找到 |
| 500 | 内部服务器错误 |

**错误响应格式：**
```json
{
  "code": "woocommerce_rest_invalid_id",
  "message": "Invalid ID.",
  "data": {
    "status": 404
  }
}
```

### 故障排除：API 密钥问题

1. 确保已设置 `MATON_API_KEY` 环境变量：

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

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `woocommerce` 开头。例如：
- 正确格式：`https://gateway.maton.ai/woocommerce/wp-json/wc/v3/products`
- 错误格式：`https://gateway.maton.ai/wp-json/wc/v3/products`

## 资源

### 通用信息
- [WooCommerce REST API 文档](https://woocommerce.github.io/woocommerce-rest-api-docs/)
- [API 认证指南](https://woocommerce.github.io/woocommerce-rest-api-docs/#authentication)
- [WooCommerce 开发者资源](https://developer.woocommerce.com/)

### 产品相关
- [产品](https://woocommerce.github.io/woocommerce-rest-api-docs/#products)
- [产品变体](https://woocommerce.github.io/woocommerce-rest-api-docs/#product-variations)
- [产品属性](https://woocommerce.github.io/woocommerce-rest-api-docs/#product-attributes)
- [产品属性术语](https://woocommerce.github.io/woocommerce-rest-api-docs/#product-attribute-terms)
- [产品类别](https://woocommerce.github.io/woocommerce-rest-api-docs/#product-categories)
- [产品标签](https://woocommerce.github.io/woocommerce-rest-api-docs/#product-tags)
- [产品运费类别](https://woocommerce.github.io/woocommerce-rest-api-docs/#product-shipping-classes)
- [产品评论](https://woocommerce.github.io/woocommerce-rest-api-docs/#product-reviews)

### 订单相关
- [订单](https://woocommerce.github.io/woocommerce-rest-api-docs/#orders)
- [订单备注](https://woocommerce.github.io/woocommerce-rest-api-docs/#order-notes)
- [退款](https://woocommerce.github.io/woocommerce-rest-api-docs/#refunds)

### 客户相关
- [客户](https://woocommerce.github.io/woocommerce-rest-api-docs/#customers)

### 优惠券相关
- [优惠券](https://woocommerce.github.io/woocommerce-rest-api-docs/#coupons)

### 税费相关
- [税率](https://woocommerce.github.io/woocommerce-rest-api-docs/#tax-rates)
- [税类](https://woocommerce.github.io/woocommerce-rest-api-docs/#tax-classes)

### 运费相关
- [运费区域](https://woocommerce.github.io/woocommerce-rest-api-docs/#shipping-zones)
- [运费区域位置](https://woocommerce.github.io/woocommerce-rest-api-docs/#shipping-zone-locations)
- [运费方式](https://woocommerce.github.io/woocommerce-rest-api-docs/#shipping-zone-methods)
- [全局运费方式](https://woocommerce.github.io/woocommerce-rest-api-docs/#shipping-methods)

### 支付与设置相关
- [支付网关](https://woocommerce.github.io/woocommerce-rest-api-docs/#payment-gateways)
- [设置](https://woocommerce.github.io/woocommerce-rest-api-docs/#settings)
- [设置选项](https://woocommerce.github.io/woocommerce-rest-api-docs/#setting-options)

### Webhook 相关
- [Webhook](https://woocommerce.github.io/woocommerce-rest-api-docs/#webhooks)

### 报告相关
- [报告](https://woocommerce.github.io/woocommerce-rest-api-docs/#reports)
- [销售报告](https://woocommerce.github.io/woocommerce-rest-api-docs/#sales-reports)
- [热销商品报告](https://woocommerce.github.io/woocommerce-rest-api-docs/#top-sellers-report)
- [优惠券汇总](https://woocommerce.github.io/woocommerce-rest-api-docs/#coupons-totals)
- [客户汇总](https://woocommerce.github.io/woocommerce-rest-api-docs/#customers-totals)
- [订单汇总](https://woocommerce.github.io/woocommerce-rest-api-docs/#orders-totals)
- [产品汇总](https://woocommerce.github.io/woocommerce-rest-api-docs/#products-totals)
- [评论汇总](https://woocommerce.github.io/woocommerce-rest-api-docs/#reviews-totals)

### 数据相关
- [数据](https://woocommerce.github.io/woocommerce-rest-api-docs/#data)
- [大陆](https://woocommerce.github.io/woocommerce-rest-api-docs/#continents)
- [国家](https://woocommerce.github.io/woocommerce-rest-api-docs/#countries)
- [货币](https://woocommerce.github.io/woocommerce-rest-api-docs/#currencies)

### 系统相关
- [系统状态](https://woocommerce.github.io/woocommerce-rest-api-docs/#system-status)
- [系统状态工具](https://woocommerce.github.io/woocommerce-rest-api-docs/#system-status-tools)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)