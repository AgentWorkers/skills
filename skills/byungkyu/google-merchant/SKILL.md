---
name: google-merchant
description: |
  Google Merchant Center API integration with managed OAuth. Manage products, inventories, data sources, promotions, and reports for Google Shopping.
  Use this skill when users want to manage their Merchant Center product catalog, check product status, configure data sources, or analyze shopping performance.
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

# Google Merchant Center

您可以使用托管的 OAuth 认证来访问 Google Merchant Center API，从而管理 Google Shopping 的产品、库存、促销活动、数据源和报告。

## 快速入门

```bash
# List products in your Merchant Center account
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-merchant/products/v1/accounts/{accountId}/products')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-merchant/{sub-api}/{version}/accounts/{accountId}/{resource}
```

Merchant API 采用模块化的子 API 结构。请将以下内容替换为相应的服务：
- `{sub-api}`：`products`、`accounts`、`datasources`、`reports`、`promotions`、`inventories`、`notifications`、`conversions`、`lfp`
- `{version}`：`v1`（稳定版本）或 `v1beta`
- `{accountId}`：您的 Google Merchant Center 账户 ID

该网关会将请求代理到 `merchantapi.googleapis.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

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

### 查找您的 Google Merchant Center 账户 ID

您的 Google Merchant Center 账户 ID 是一个数字标识符，可以在 Merchant Center 用户界面 URL 或账户设置中看到。所有 API 调用都需要这个 ID。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Google Merchant OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-merchant&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-merchant'}).encode()
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
    "connection_id": "00726960-095e-47e2-92e6-6e9cdf3e40a1",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T06:41:22.751289Z",
    "last_updated_time": "2026-02-07T06:42:29.411979Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-merchant",
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

如果您有多个 Google Merchant 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-merchant/products/v1/accounts/123456/products')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '00726960-095e-47e2-92e6-6e9cdf3e40a1')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 子 API 结构

Merchant API 分为多个子 API，每个子 API 都有自己的版本：

| 子 API | 功能 | 稳定版本 |
|---------|---------|----------------|
| `products` | 产品目录管理 | v1 |
| `accounts` | 账户设置和用户 | v1 |
| `datasources` | 数据源配置 | v1 |
| `reports` | 分析和报告 | v1 |
| `promotions` | 促销活动 | v1 |
| `inventories` | 本地和区域库存 | v1 |
| `notifications` | Webhook 订阅 | v1 |
| `conversions` | 转换跟踪 | v1 |
| `lfp` | 本地配送合作伙伴关系 | v1beta |

### 产品

#### 列出产品

```bash
GET /google-merchant/products/v1/accounts/{accountId}/products
```

查询参数：
- `pageSize`（整数）：每页的最大结果数量
- `pageToken`（字符串）：分页令牌

#### 获取产品信息

```bash
GET /google-merchant/products/v1/accounts/{accountId}/products/{productId}
```

产品 ID 格式：`contentLanguage~feedLabel~offerId`（例如：`en~US~sku123`

#### 插入产品信息

```bash
POST /google-merchant/products/v1/accounts/{accountId}/productInputs:insert?dataSource=accounts/{accountId}/dataSources/{dataSourceId}
Content-Type: application/json

{
  "offerId": "sku123",
  "contentLanguage": "en",
  "feedLabel": "US",
  "attributes": {
    "title": "Product Title",
    "description": "Product description",
    "link": "https://example.com/product",
    "imageLink": "https://example.com/image.jpg",
    "availability": "in_stock",
    "price": {
      "amountMicros": "19990000",
      "currencyCode": "USD"
    },
    "condition": "new"
  }
}
```

#### 删除产品信息

```bash
DELETE /google-merchant/products/v1/accounts/{accountId}/productInputs/{productId}?dataSource=accounts/{accountId}/dataSources/{dataSourceId}
```

### 库存

#### 列出本地库存

```bash
GET /google-merchant/inventories/v1/accounts/{accountId}/products/{productId}/localInventories
```

#### 插入本地库存信息

```bash
POST /google-merchant/inventories/v1/accounts/{accountId}/products/{productId}/localInventories:insert
Content-Type: application/json

{
  "storeCode": "store123",
  "availability": "in_stock",
  "quantity": 10,
  "price": {
    "amountMicros": "19990000",
    "currencyCode": "USD"
  }
}
```

#### 列出区域库存

```bash
GET /google-merchant/inventories/v1/accounts/{accountId}/products/{productId}/regionalInventories
```

### 数据源

#### 列出数据源

```bash
GET /google-merchant/datasources/v1/accounts/{accountId}/dataSources
```

#### 获取数据源信息

```bash
GET /google-merchant/datasources/v1/accounts/{accountId}/dataSources/{dataSourceId}
```

#### 创建数据源

```bash
POST /google-merchant/datasources/v1/accounts/{accountId}/dataSources
Content-Type: application/json

{
  "displayName": "API Data Source",
  "primaryProductDataSource": {
    "channel": "ONLINE_PRODUCTS",
    "feedLabel": "US",
    "contentLanguage": "en"
  }
}
```

#### 获取数据源数据（触发立即刷新）

```bash
POST /google-merchant/datasources/v1/accounts/{accountId}/dataSources/{dataSourceId}:fetch
```

### 报告

#### 搜索报告

```bash
POST /google-merchant/reports/v1/accounts/{accountId}/reports:search
Content-Type: application/json

{
  "query": "SELECT offer_id, title, clicks, impressions FROM product_performance_view WHERE date BETWEEN '2026-01-01' AND '2026-01-31'"
}
```

可用的报告表格：
- `product_performance_view`：按产品显示点击量、展示次数和点击率
- `product_view`：当前库存信息及问题
- `price_competitiveness_product_view`：与竞争对手的价格对比
- `price_insights_product_view`：建议定价
- `best_sellers_product_cluster_view`：按类别显示畅销产品
- `competitive_visibility_competitor_view`：竞争对手的可见性

### 促销活动

#### 列出促销活动

```bash
GET /google-merchant/promotions/v1/accounts/{accountId}/promotions
```

#### 获取促销活动信息

```bash
GET /google-merchant/promotions/v1/accounts/{accountId}/promotions/{promotionId}
```

#### 插入促销活动信息

```bash
POST /google-merchant/promotions/v1/accounts/{accountId}/promotions:insert
Content-Type: application/json

{
  "promotionId": "promo123",
  "contentLanguage": "en",
  "targetCountry": "US",
  "redemptionChannel": ["ONLINE"],
  "attributes": {
    "longTitle": "20% off all products",
    "promotionEffectiveDates": "2026-02-01T00:00:00Z/2026-02-28T23:59:59Z"
  }
}
```

### 账户

#### 获取账户信息

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}
```

#### 列出子账户

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}:listSubaccounts
```

#### 获取业务信息

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/businessInfo
```

#### 获取配送设置

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/shippingSettings
```

#### 列出用户

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/users
```

#### 列出计划

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/programs
```

#### 列出地区

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/regions
```

#### 列出在线退货政策

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/onlineReturnPolicies
```

### 通知

#### 列出通知订阅

```bash
GET /google-merchant/notifications/v1/accounts/{accountId}/notificationsubscriptions
```

#### 创建通知订阅

```bash
POST /google-merchant/notifications/v1/accounts/{accountId}/notificationsubscriptions
Content-Type: application/json

{
  "registeredEvent": "PRODUCT_STATUS_CHANGE",
  "callBackUri": "https://example.com/webhook"
}
```

### 转换来源

#### 列出转换来源

```bash
GET /google-merchant/conversions/v1/accounts/{accountId}/conversionSources
```

## 分页

API 使用基于令牌的分页机制：

```bash
GET /google-merchant/products/v1/accounts/{accountId}/products?pageSize=50
```

当存在更多结果时，响应中会包含 `nextPageToken`：

```json
{
  "products": [...],
  "nextPageToken": "CAE..."
}
```

使用该令牌获取下一页的数据：

```bash
GET /google-merchant/products/v1/accounts/{accountId}/products?pageSize=50&pageToken=CAE...
```

## 代码示例

### JavaScript

```javascript
const accountId = '123456789';
const response = await fetch(
  `https://gateway.maton.ai/google-merchant/products/v1/accounts/${accountId}/products`,
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

account_id = '123456789'
response = requests.get(
    f'https://gateway.maton.ai/google-merchant/products/v1/accounts/{account_id}/products',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项

- 产品 ID 的格式为 `contentLanguage~feedLabel~offerId`（例如：`en~US~sku123`）
- 产品只能在类型为 `API` 的数据源中插入/更新/删除。
- 插入/更新产品后，可能需要几分钟才能在系统中显示。
- 货币值以微单位（micro）表示（实际数值需除以 1,000,000）。
- API 使用子 API 版本控制——建议使用稳定的 `v1` 而不是 `v1beta`。
- 重要提示：当使用 `curl` 命令时，如果 URL 中包含括号，请使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Google Merchant 连接 |
| 401 | Maton API 密钥无效或缺失，或无法访问指定的账户 |
| 403 | 拒绝执行请求的操作 |
| 404 | 资源未找到 |
| 429 | 请求次数限制 |
| 4xx/5xx | 来自 Google Merchant API 的传递错误 |

### 常见错误

**“调用者无法访问该账户”**：指定的账户 ID 使用您的 OAuth 凭据无法访问。请确认您有权访问该 Google Merchant Center 账户。

**“GCP 项目未注册”**：v1 稳定版本需要注册 GCP 项目。请使用 `v1beta` 或注册您的项目。

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

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `google-merchant` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/google-merchant/products/v1/accounts/{accountId}/products`
- 错误的路径：`https://gateway.maton.ai/products/v1/accounts/{accountId}/products`

## 资源

- [Merchant API 概述](https://developers.google.com/merchant/api/overview)
- [Merchant API 参考](https://developers.google.com/merchant/api/reference/rest)
- [产品指南](https://developers.google.com/merchant/api/guides/products/overview)
- [数据源指南](https://developers.google.com/merchant/api/guides/datasources)
- [报告指南](https://developers.google.com/merchant/api/guides/reports)
- [产品数据规范](https://support.google.com/merchants/answer/7052112)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)