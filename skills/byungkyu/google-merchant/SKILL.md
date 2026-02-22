---
name: google-merchant
description: >
  **Google Merchant Center API集成与托管式OAuth**  
  该功能支持用户管理Google Shopping平台上的产品信息、库存数据、数据源、促销活动以及生成相关报告。  
  当用户需要维护其 Merchant Center 产品目录、查询产品状态、配置数据源或分析购物行为时，可选用此功能。  
  对于其他第三方应用程序，建议使用 `api-gateway` 功能（https://clawhub.ai/byungkyu/api-gateway）。  
  使用该功能需要网络连接以及有效的Maton API密钥。
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

您可以使用托管的OAuth身份验证来访问Google Merchant Center API，从而管理产品、库存、促销活动、数据源和报告信息，以支持Google Shopping功能。

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

## 基本URL

```
https://gateway.maton.ai/google-merchant/{sub-api}/{version}/accounts/{accountId}/{resource}
```

Merchant API采用模块化的子API结构。请将以下内容替换为相应的服务名称：
- `{sub-api}`：`products`、`accounts`、`datasources`、`reports`、`promotions`、`inventories`、`notifications`、`conversions`
- `{version}`：`v1`
- `{accountId}`：您的Google Merchant Center账户ID

该API通过`merchantapi.googleapis.com`代理请求，并自动插入您的OAuth令牌。

**重要提示：**v1 API需要一次性开发者注册。请参阅[开发者注册](#developer-registration)部分。

## 身份验证

所有请求都必须在`Authorization`头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：**将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在[maton.ai](https://maton.ai)上登录或创建账户。
2. 进入[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

### 查找您的Google Merchant Center账户ID

您的Google Merchant Center账户ID是一个数字标识符。以下是获取方法：
1. 登录[Google Merchant Center](https://merchants.google.com/)。
2. 查看URL，其中包含您的账户ID：`https://merchants.google.com/mc/overview?a=ACCOUNT_ID`。

## 开发者注册

**重要提示：**在使用v1 API之前，您必须完成一次开发者注册，以便将您的账户与API关联起来。

### 第一步：获取您的账户ID

**选项A：首先尝试通过API获取**

尝试使用v1beta端点列出账户。如果成功，您可以自动获取账户ID：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-merchant/accounts/v1beta/accounts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
try:
    result = json.load(urllib.request.urlopen(req))
    for account in result.get('accounts', []):
        print(f"Account ID: {account['accountId']}, Name: {account['accountName']}")
except Exception as e:
    print(f"v1beta not available - use Option B to get your account ID manually")
EOF
```

**选项B：通过Google Merchant Center UI获取（如果选项A失败）**

如果v1beta端点不可用或返回错误：
1. 登录[Google Merchant Center](https://merchants.google.com/)。
2. 您的账户ID位于URL中：`https://merchants.google.com/mc/overview?a=YOUR_ACCOUNT_ID`

例如，如果您的URL是`https://merchants.google.com/mc/overview?a=123456789`，则您的账户ID为`123456789`。

### 第二步：注册API访问权限

使用您的账户ID和电子邮件调用`registerGcp`端点：

```bash
python <<'EOF'
import urllib.request, os, json

account_id = 'YOUR_ACCOUNT_ID'  # From Step 1
developer_email = 'your-email@example.com'  # Your Google account email

data = json.dumps({'developerEmail': developer_email}).encode()
req = urllib.request.Request(
    f'https://gateway.maton.ai/google-merchant/accounts/v1/accounts/{account_id}/developerRegistration:registerGcp',
    data=data,
    method='POST'
)
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')

result = json.load(urllib.request.urlopen(req))
print(json.dumps(result, indent=2))
EOF
```

**响应：**
```json
{
  "name": "accounts/123456789/developerRegistration",
  "gcpIds": ["216141799266"]
}
```

### 第三步：验证注册

注册完成后，v1端点将可以正常使用：

```bash
python <<'EOF'
import urllib.request, os, json
account_id = 'YOUR_ACCOUNT_ID'
req = urllib.request.Request(f'https://gateway.maton.ai/google-merchant/accounts/v1/accounts/{account_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**注意：**每个Google Merchant Center账户只需注册一次。注册后，该账户的所有v1端点都将可用。

## 连接管理

您可以在`https://ctrl.maton.ai`管理您的Google Merchant OAuth连接。

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

在浏览器中打开返回的`url`以完成OAuth授权。

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

如果您有多个Google Merchant连接，请使用`Maton-Connection`头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-merchant/products/v1/accounts/123456/products')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '00726960-095e-47e2-92e6-6e9cdf3e40a1')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，系统将使用默认的（最旧的）活动连接。

## API参考

### 子API结构

Merchant API分为多个子API：

| 子API | 功能 | 版本 |
|---------|---------|---------|
| `products` | 产品目录管理 | v1 |
| `accounts` | 账户设置和用户 | v1 |
| `datasources` | 数据源配置 | v1 |
| `reports` | 分析和报告 | v1 |
| `promotions` | 促销活动（需先注册） | v1 |
| `inventories` | 本地和区域库存 | v1 |
| `notifications` | Webhook订阅 | v1 |
| `conversions` | 转换跟踪 | v1 |

### 账户

#### 列出账户

```bash
GET /google-merchant/accounts/v1/accounts
```

使用您的OAuth凭据列出所有可访问的Google Merchant Center账户。此操作可用于查找您的账户ID。

#### 获取账户信息

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}
```

#### 列出子账户

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}:listSubaccounts
```

**注意：**此端点仅适用于多客户账户（MCAs）。标准商户账户会收到403错误。

#### 获取业务信息

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/businessInfo
```

#### 更新业务信息

```bash
PATCH /google-merchant/accounts/v1/accounts/{accountId}/businessInfo?updateMask=customerService
Content-Type: application/json

{
  "customerService": {
    "email": "support@example.com"
  }
}
```

#### 获取主页信息

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/homepage
```

#### 获取运输设置

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/shippingSettings
```

#### 插入运输设置

```bash
POST /google-merchant/accounts/v1/accounts/{accountId}/shippingSettings:insert
Content-Type: application/json

{
  "services": [
    {
      "serviceName": "Standard Shipping",
      "deliveryCountries": ["US"],
      "currencyCode": "USD",
      "deliveryTime": {
        "minTransitDays": 3,
        "maxTransitDays": 7,
        "minHandlingDays": 0,
        "maxHandlingDays": 1
      },
      "rateGroups": [
        {
          "singleValue": {
            "flatRate": {
              "amountMicros": "0",
              "currencyCode": "USD"
            }
          }
        }
      ],
      "active": true
    }
  ]
}
```

#### 列出用户

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/users
```

#### 获取用户信息

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/users/{email}
```

#### 列出计划

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/programs
```

#### 列出地区

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/regions
```

#### 列出账户问题

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/issues
```

#### 列出在线退货政策

```bash
GET /google-merchant/accounts/v1/accounts/{accountId}/onlineReturnPolicies
```

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

产品ID格式：`contentLanguage~feedLabel~offerId`（例如：`en~US~sku123`）

#### 插入产品信息

```bash
POST /google-merchant/products/v1/accounts/{accountId}/productInputs:insert?dataSource=accounts/{accountId}/dataSources/{dataSourceId}
Content-Type: application/json

{
  "offerId": "sku123",
  "contentLanguage": "en",
  "feedLabel": "US",
  "productAttributes": {
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

**注意：**产品只能插入到类型为`input: "API"`的数据源中。如有需要，请先创建一个API数据源。

#### 删除产品信息

```bash
DELETE /google-merchant/products/v1/accounts/{accountId}/productInputs/{productId}?dataSource=accounts/{accountId}/dataSources/{dataSourceId}
```

### 库存

#### 列出本地库存

```bash
GET /google-merchant/inventories/v1/accounts/{accountId}/products/{productId}/localInventories
```

**注意：**本地库存仅适用于`LOCAL`渠道的产品。请使用类似`local~en~US~sku123`的产品ID。

#### 插入本地库存信息

```bash
POST /google-merchant/inventories/v1/accounts/{accountId}/products/{productId}/localInventories:insert
Content-Type: application/json

{
  "storeCode": "store123"
}
```

**注意：**`storeCode`必须是您在Google Merchant Center账户中配置的有效商店代码。可能还有其他库存属性，请参考[Google Merchant API参考](https://developers.google.com/merchant/api/reference/rest)以获取完整的字段列表。

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
    "feedLabel": "US",
    "contentLanguage": "en"
  }
}
```

**响应：**
```json
{
  "name": "accounts/123456/dataSources/789",
  "dataSourceId": "789",
  "displayName": "API Data Source",
  "primaryProductDataSource": {
    "feedLabel": "US",
    "contentLanguage": "en"
  },
  "input": "API"
}
```

#### 更新数据源信息

```bash
PATCH /google-merchant/datasources/v1/accounts/{accountId}/dataSources/{dataSourceId}?updateMask=displayName
Content-Type: application/json

{
  "displayName": "Updated Name"
}
```

#### 删除数据源

```bash
DELETE /google-merchant/datasources/v1/accounts/{accountId}/dataSources/{dataSourceId}
```

#### 获取数据源信息（立即刷新）

```bash
POST /google-merchant/datasources/v1/accounts/{accountId}/dataSources/{dataSourceId}:fetch
```

**注意：**仅适用于类型为`FILE`的数据源。API和UI数据源无法通过此方法获取。

### 报告

#### 搜索报告

```bash
POST /google-merchant/reports/v1/accounts/{accountId}/reports:search
Content-Type: application/json

{
  "query": "SELECT offer_id, title, clicks, impressions FROM product_performance_view WHERE date BETWEEN '2026-01-01' AND '2026-01-31'"
}
```

**示例：查询product_view（需要`id`字段）：**
```json
{
  "query": "SELECT id, offer_id, title, item_issues FROM product_view LIMIT 10"
}
```

**注意：**`product_view`表在SELECT子句中需要`id`字段。**

可用的报告表：
- `product_performance_view` - 按产品统计的点击量、展示次数和点击率
- `product_view` - 包含属性和问题的当前库存信息（SELECT子句中需要`id`）
- `price_competitiveness_product_view` - 与竞争对手的价格对比
- `price_insights_product_view` - 建议售价
- `best_sellers_product_cluster_view` - 按类别划分的热销产品
- `competitive_visibility_competitor_view` - 竞争对手的可见性

### 促销活动

**注意：**促销活动需要您的Google Merchant Center账户注册促销计划。否则会收到403错误。

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
  "callBackUri": "https://example.com/webhook",
  "allManagedAccounts": true
}
```

**注意：**您必须指定`allManagedAccounts: true`或`targetAccount: "accounts/{accountId}"，以指示订阅适用于哪些账户。

**使用targetAccount的替代方法：**
```json
{
  "registeredEvent": "PRODUCT_STATUS_CHANGE",
  "callBackUri": "https://example.com/webhook",
  "targetAccount": "accounts/123456789"
}
```

#### 删除通知订阅

```bash
DELETE /google-merchant/notifications/v1/accounts/{accountId}/notificationsubscriptions/{subscriptionId}
```

### 转换来源

#### 列出转换来源

```bash
GET /google-merchant/conversions/v1/accounts/{accountId}/conversionSources
```

#### 创建转换来源

```bash
POST /google-merchant/conversions/v1/accounts/{accountId}/conversionSources
Content-Type: application/json

{
  "merchantCenterDestination": {
    "displayName": "My Conversion Source",
    "destination": "SHOPPING_ADS",
    "currencyCode": "USD",
    "attributionSettings": {
      "attributionLookbackWindowDays": 30,
      "attributionModel": "CROSS_CHANNEL_LAST_CLICK"
    }
  }
}
```

#### 删除转换来源

```bash
DELETE /google-merchant/conversions/v1/accounts/{accountId}/conversionSources/{conversionSourceId}
```

## 分页

API使用基于令牌的分页机制：

```bash
GET /google-merchant/products/v1/accounts/{accountId}/products?pageSize=50
```

当还有更多结果时，响应中会包含`nextPageToken`：

```json
{
  "products": [...],
  "nextPageToken": "CAE..."
}
```

使用该令牌访问下一页：

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

- **需要开发者注册**：在使用v1端点之前，您必须为每个Google Merchant Center账户完成[开发者注册](#developer-registration)。
- 产品ID的格式为`contentLanguage~feedLabel~offerId`（例如：`en~US~sku123`）。
- 产品只能插入/更新/删除到类型为`input: "API"`的数据源中。
- 插入/更新产品后，可能需要几分钟才能显示处理结果。
- 货币值以微单位（micro）表示（实际数值需除以1,000,000）。
- 本地库存仅适用于`LOCAL`渠道的产品（不适用于`ONLINE`渠道的产品）。
- 促销活动API要求您的账户已注册促销计划。
- `List Sub-accounts`端点仅适用于多客户账户（MCAs）。
- **重要提示：**当URL包含括号时，使用`curl -g`来禁用全局解析。
- **重要提示：**在将curl输出传递给`jq`或其他命令时，某些shell环境中环境变量`$MATON_API_KEY`可能无法正确展开。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 请求无效或缺少Google Merchant连接 |
| 401 | Maton API密钥无效或缺失，或GCP项目未注册（请参阅[开发者注册](#developer-registration) |
| 403 | 权限被拒绝——账户未注册所需计划或功能不可用 |
| 404 | 资源未找到 |
| 429 | 请求次数限制 |
| 4xx/5xx | 来自Google Merchant API的传递错误 |

### 常见错误

**“GCP项目未注册”**：您需要完成开发者注册。请参阅[开发者注册](#developer-registration)部分。
**“调用者无法访问这些账户”**：指定的账户ID无法使用您的OAuth凭据访问。请确认您有权访问该Google Merchant Center账户。
**“促销计划未启用”**：您的Google Merchant Center账户未注册促销计划。请在 Merchant Center设置中启用该计划。
**“此方法仅适用于多客户账户”**：您正在调用仅适用于多客户账户（MCAs）的端点。
**“渠道不匹配”**：您尝试访问的本地库存信息适用于`ONLINE`渠道的产品，但实际上应使用`LOCAL`渠道的产品。

### 故障排除：API密钥问题

1. 确保设置了`MATON_API_KEY`环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

确保您的URL路径以`google-merchant`开头。例如：
- 正确的路径：`https://gateway.maton.ai/google-merchant/products/v1/accounts/{accountId}/products`
- 错误的路径：`https://gateway.maton.ai/products/v1/accounts/{accountId}/products`

### 故障排除：GCP项目未注册

如果您收到“GCP项目未注册”的错误：
1. **完成开发者注册**：请参阅[开发者注册](#developer-registration)部分。
2. 从Google Merchant Center UI中获取您的账户ID（URL中的`?a=`后面的部分）。
3. 使用您的账户ID和电子邮件调用`registerGcp`端点。
4. 注册成功后，重新尝试原始请求。

## 资源

- [Merchant API概述](https://developers.google.com/merchant/api/overview)
- [Merchant API参考](https://developers.google.com/merchant/api/reference/rest)
- [产品指南](https://developers.google.com/merchant/api/guides/products/overview)
- [数据源指南](https://developers.google.com/merchant/api/guides/datasources)
- [报告指南](https://developers.google.com/merchant/api/guides/reports)
- [产品数据规范](https://support.google.com/merchants/answer/7052112)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)