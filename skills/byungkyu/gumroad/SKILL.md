---
name: gumroad
description: |
  Gumroad API integration with managed OAuth. Access products, sales, subscribers, licenses, and webhooks for your digital storefront.
  Use this skill when users want to manage their Gumroad products, verify licenses, view sales data, or set up webhook notifications.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Gumroad

您可以使用托管的 OAuth 认证来访问 Gumroad API。通过该 API，您可以管理产品、查看销售数据、验证许可证，并为您的数字商店设置 Webhook。

## 快速入门

```bash
# Get current user info
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/gumroad/v2/user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/gumroad/v2/{resource}
```

Gumroad 的网关会将请求代理到 `api.gumroad.com/v2`，并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Gumroad OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=gumroad&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'gumroad'}).encode()
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
    "connection_id": "e1a4444f-2bb8-4e09-9265-3afe71b74b1f",
    "status": "ACTIVE",
    "creation_time": "2026-02-08T06:22:48.654579Z",
    "last_updated_time": "2026-02-08T06:23:07.420381Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "gumroad",
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

如果您有多个 Gumroad 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/gumroad/v2/products')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'e1a4444f-2bb8-4e09-9265-3afe71b74b1f')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户信息

#### 获取当前用户

```bash
GET /gumroad/v2/user
```

**响应：**
```json
{
  "success": true,
  "user": {
    "name": "Chris",
    "currency_type": "usd",
    "bio": null,
    "twitter_handle": null,
    "id": "1690942847664",
    "user_id": "QmTtTnViFSoocHAexgLuJw==",
    "url": "https://chriswave1246.gumroad.com",
    "profile_url": "https://public-files.gumroad.com/...",
    "email": "chris@example.com",
    "display_name": "Chris"
  }
}
```

### 产品操作

#### 列出产品

```bash
GET /gumroad/v2/products
```

**响应：**
```json
{
  "success": true,
  "products": [
    {
      "id": "ABC123",
      "name": "My Product",
      "price": 500,
      "currency": "usd",
      "short_url": "https://gumroad.com/l/abc",
      "sales_count": 10,
      "sales_usd_cents": 5000
    }
  ]
}
```

#### 获取产品信息

```bash
GET /gumroad/v2/products/{product_id}
```

#### 更新产品信息

```bash
PUT /gumroad/v2/products/{product_id}
Content-Type: application/x-www-form-urlencoded

name=Updated%20Name&price=1000
```

#### 启用/禁用产品

```bash
PUT /gumroad/v2/products/{product_id}/disable
Content-Type: application/x-www-form-urlencoded

disabled=true
```

#### 删除产品

```bash
DELETE /gumroad/v2/products/{product_id}
```

**注意：** 无法通过 API 创建新产品。产品必须通过 Gumroad 网站进行创建。

### 优惠码操作

#### 列出优惠码

```bash
GET /gumroad/v2/products/{product_id}/offer_codes
```

#### 获取优惠码信息

```bash
GET /gumroad/v2/products/{product_id}/offer_codes/{offer_code_id}
```

#### 创建优惠码

```bash
POST /gumroad/v2/products/{product_id}/offer_codes
Content-Type: application/x-www-form-urlencoded

name=SUMMER20&amount_off=20
```

参数：
- `name` - 客户输入的优惠码（必填）
- `amount_off` - 优惠金额（以分或百分比表示）（必填）
- `offer_type` - "cents" 或 "percent"（默认值："cents"）
- `max_purchase_count` - 最大使用次数（可选）

#### 更新优惠码信息

```bash
PUT /gumroad/v2/products/{product_id}/offer_codes/{offer_code_id}
Content-Type: application/x-www-form-urlencoded

max_purchase_count=100
```

#### 删除优惠码

```bash
DELETE /gumroad/v2/products/{product_id}/offer_codes/{offer_code_id}
```

### 销售操作

#### 列出销售记录

```bash
GET /gumroad/v2/sales
```

查询参数：
- `after` - 仅显示此日期之后的销售记录（格式：YYYY-MM-DD）
- `before` - 仅显示此日期之前的销售记录（格式：YYYY-MM-DD）
- `page` - 分页页码

**带过滤条件的示例：**
```bash
GET /gumroad/v2/sales?after=2026-01-01&before=2026-12-31
```

**响应：**
```json
{
  "success": true,
  "sales": [
    {
      "id": "sale_abc123",
      "email": "customer@example.com",
      "seller_id": "seller123",
      "product_id": "prod123",
      "product_name": "My Product",
      "price": 500,
      "currency_symbol": "$",
      "created_at": "2026-01-15T10:30:00Z"
    }
  ]
}
```

#### 获取单笔销售记录

```bash
GET /gumroad/v2/sales/{sale_id}
```

### 订阅者操作

#### 列出订阅者

```bash
GET /gumroad/v2/products/{product_id}/subscribers
```

#### 获取订阅者信息

```bash
GET /gumroad/v2/subscribers/{subscriber_id}
```

**响应：**
```json
{
  "success": true,
  "subscriber": {
    "id": "sub123",
    "product_id": "prod123",
    "product_name": "Monthly Subscription",
    "user_id": "user123",
    "user_email": "subscriber@example.com",
    "status": "alive",
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```

### 许可证操作

#### 验证许可证

```bash
POST /gumroad/v2/licenses/verify
Content-Type: application/x-www-form-urlencoded

product_id={product_id}&license_key={license_key}
```

参数：
- `product_id` - 产品 ID（必填）
- `license_key` - 需要验证的许可证密钥（必填）
- `increment_uses_count` - 增加许可证的使用次数（默认值：true）

**成功响应：**
```json
{
  "success": true,
  "uses": 1,
  "purchase": {
    "seller_id": "seller123",
    "product_id": "prod123",
    "product_name": "My Product",
    "permalink": "abc",
    "email": "customer@example.com",
    "license_key": "ABC-123-DEF",
    "quantity": 1,
    "created_at": "2026-01-15T00:00:00Z"
  }
}
```

**失败响应：**
```json
{
  "success": false,
  "message": "That license does not exist for the provided product."
}
```

#### 启用许可证

```bash
PUT /gumroad/v2/licenses/enable
Content-Type: application/x-www-form-urlencoded

product_id={product_id}&license_key={license_key}
```

#### 禁用许可证

```bash
PUT /gumroad/v2/licenses/disable
Content-Type: application/x-www-form-urlencoded

product_id={product_id}&license_key={license_key}
```

#### 减少许可证的使用次数

```bash
PUT /gumroad/v2/licenses/decrement_uses_count
Content-Type: application/x-www-form-urlencoded

product_id={product_id}&license_key={license_key}
```

### 资源订阅（Webhook）

您可以订阅销售事件和其他事件的通知。

#### 列出资源订阅信息

```bash
GET /gumroad/v2/resource_subscriptions?resource_name=sale
```

参数：
- `resource_name` - 必填值。可选值：`sale`、`refund`、`dispute`、`dispute_won`、`cancellation`、`subscription_updated`、`subscription_ended`、`subscription_restarted`

**响应：**
```json
{
  "success": true,
  "resource_subscriptions": [
    {
      "id": "wX43hzi-s7W4JfYFkxyeiQ==",
      "resource_name": "sale",
      "post_url": "https://example.com/webhook"
    }
  ]
}
```

#### 删除资源订阅

```bash
DELETE /gumroad/v2/resource_subscriptions/{resource_subscription_id}
```

**响应：**
```json
{
  "success": true,
  "message": "The resource_subscription was deleted successfully."
}
```

### 变体类别

#### 列出变量类别

```bash
GET /gumroad/v2/products/{product_id}/variant_categories
```

#### 获取变量类别信息

```bash
GET /gumroad/v2/products/{product_id}/variant_categories/{variant_category_id}
```

#### 创建变量类别

```bash
POST /gumroad/v2/products/{product_id}/variant_categories
Content-Type: application/x-www-form-urlencoded

title=Size
```

#### 删除变量类别

```bash
DELETE /gumroad/v2/products/{product_id}/variant_categories/{variant_category_id}
```

### 变体

#### 列出变量信息

```bash
GET /gumroad/v2/products/{product_id}/variant_categories/{variant_category_id}/variants
```

#### 创建变量

```bash
POST /gumroad/v2/products/{product_id}/variant_categories/{variant_category_id}/variants
Content-Type: application/x-www-form-urlencoded

name=Large&price_difference=200
```

#### 更新变量信息

```bash
PUT /gumroad/v2/products/{product_id}/variant_categories/{variant_category_id}/variants/{variant_id}
Content-Type: application/x-www-form-urlencoded

name=Extra%20Large
```

#### 删除变量

```bash
DELETE /gumroad/v2/products/{product_id}/variant_categories/{variant_category_id}/variants/{variant_id}
```

### 自定义字段

#### 列出自定义字段

```bash
GET /gumroad/v2/products/{product_id}/custom_fields
```

#### 创建自定义字段

```bash
POST /gumroad/v2/products/{product_id}/custom_fields
Content-Type: application/x-www-form-urlencoded

name=Company%20Name&required=true
```

#### 更新自定义字段

```bash
PUT /gumroad/v2/products/{product_id}/custom_fields/{name}
Content-Type: application/x-www-form-urlencoded

required=false
```

#### 删除自定义字段

```bash
DELETE /gumroad/v2/products/{product_id}/custom_fields/{name}
```

## 分页

Gumroad 对返回列表的 API 端点使用基于页码的分页机制：

```bash
GET /gumroad/v2/sales?page=1
GET /gumroad/v2/sales?page=2
```

继续增加页码，直到收到空列表为止。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/gumroad/v2/products',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/gumroad/v2/products',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

### Python（验证许可证）

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/gumroad/v2/licenses/verify',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    data={
        'product_id': 'your_product_id',
        'license_key': 'CUSTOMER-LICENSE-KEY'
    }
)
result = response.json()
if result['success']:
    print(f"License valid! Uses: {result['uses']}")
else:
    print(f"Invalid: {result['message']}")
```

## 注意事项

- 所有响应都包含一个 `success` 布尔字段，用于表示操作是否成功。
- 无法通过 API 创建新产品——产品必须通过 Gumroad 网站进行创建。
- POST/PUT 请求使用 `application/x-www-form-urlencoded` 的内容类型（而非 JSON）。
- 价格以分为单位（例如：500 表示 $5.00）。
- 许可证密钥不区分大小写。
- 资源订阅的 Webhook 会向您指定的 URL 发送 POST 请求。
- **重要提示：** 当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中，环境变量（如 `$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 缺少 Gumroad 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到（响应中包含 `success: false`） |
| 429 | 请求频率受限 |
| 4xx/5xx | 来自 Gumroad API 的传递错误 |

Gumroad 的错误通常会返回 HTTP 404 错误，并附带 JSON 格式的错误信息：
```json
{
  "success": false,
  "message": "Error description"
}
```

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量。

```bash
echo $MATON_API_KEY
```

2. 通过列出所有连接来验证 API 密钥是否有效。

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称错误

1. 确保您的 URL 路径以 `gumroad` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/gumroad/v2/user`
- 错误的路径：`https://gateway.maton.ai/v2/user`

## 资源

- [Gumroad API 概述](https://gumroad.com/api)
- [创建 API 应用程序](https://help.gumroad.com/article/280-create-application-api)
- [许可证密钥帮助](https://help.gumroad.com/article/76-license-keys)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)