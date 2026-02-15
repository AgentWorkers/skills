---
name: google-play
description: |
  Google Play Developer API (Android Publisher) integration with managed OAuth. Manage apps, subscriptions, in-app purchases, and reviews. Use this skill when users want to interact with Google Play Console programmatically. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google Play

使用托管的 OAuth 认证方式访问 Google Play 开发者 API（Android Publisher）。您可以管理应用列表、订阅服务、应用内购买、用户评价等功能。

## 快速入门

```bash
# List in-app products
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-play/androidpublisher/v3/applications/{packageName}/inappproducts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-play/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Android Publisher API 端点路径。该网关会将请求代理到 `androidpublisher.googleapis.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Google OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-play&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-play'}).encode()
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
    "app": "google-play",
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

如果您有多个 Google Play 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-play/androidpublisher/v3/applications/{packageName}/inappproducts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 应用内产品

#### 列出应用内产品

```bash
GET /google-play/androidpublisher/v3/applications/{packageName}/inappproducts
```

#### 获取应用内产品信息

```bash
GET /google-play/androidpublisher/v3/applications/{packageName}/inappproducts/{sku}
```

#### 创建应用内产品

```bash
POST /google-play/androidpublisher/v3/applications/{packageName}/inappproducts
Content-Type: application/json

{
  "packageName": "com.example.app",
  "sku": "premium_upgrade",
  "status": "active",
  "purchaseType": "managedUser",
  "defaultPrice": {
    "priceMicros": "990000",
    "currency": "USD"
  },
  "listings": {
    "en-US": {
      "title": "Premium Upgrade",
      "description": "Unlock all premium features"
    }
  }
}
```

#### 更新应用内产品

```bash
PUT /google-play/androidpublisher/v3/applications/{packageName}/inappproducts/{sku}
Content-Type: application/json

{
  "packageName": "com.example.app",
  "sku": "premium_upgrade",
  "status": "active",
  "purchaseType": "managedUser",
  "defaultPrice": {
    "priceMicros": "1990000",
    "currency": "USD"
  }
}
```

#### 删除应用内产品

```bash
DELETE /google-play/androidpublisher/v3/applications/{packageName}/inappproducts/{sku}
```

### 订阅服务

#### 列出订阅服务

```bash
GET /google-play/androidpublisher/v3/applications/{packageName}/subscriptions
```

#### 获取订阅信息

```bash
GET /google-play/androidpublisher/v3/applications/{packageName}/subscriptions/{productId}
```

#### 创建订阅服务

```bash
POST /google-play/androidpublisher/v3/applications/{packageName}/subscriptions
Content-Type: application/json

{
  "productId": "monthly_premium",
  "basePlans": [
    {
      "basePlanId": "p1m",
      "autoRenewingBasePlanType": {
        "billingPeriodDuration": "P1M"
      }
    }
  ],
  "listings": [
    {
      "languageCode": "en-US",
      "title": "Premium Monthly"
    }
  ]
}
```

### 购买记录

#### 获取购买记录（一次性产品）

```bash
GET /google-play/androidpublisher/v3/applications/{packageName}/purchases/products/{productId}/tokens/{token}
```

#### 确认购买

```bash
POST /google-play/androidpublisher/v3/applications/{packageName}/purchases/products/{productId}/tokens/{token}:acknowledge
Content-Type: application/json

{
  "developerPayload": "optional payload"
}
```

#### 获取订阅购买记录

```bash
GET /google-play/androidpublisher/v3/applications/{packageName}/purchases/subscriptions/{subscriptionId}/tokens/{token}
```

#### 取消订阅

```bash
POST /google-play/androidpublisher/v3/applications/{packageName}/purchases/subscriptions/{subscriptionId}/tokens/{token}:cancel
```

#### 退款订阅

```bash
POST /google-play/androidpublisher/v3/applications/{packageName}/purchases/subscriptions/{subscriptionId}/tokens/{token}:refund
```

### 用户评价

#### 列出评价

```bash
GET /google-play/androidpublisher/v3/applications/{packageName}/reviews
```

#### 获取评价信息

```bash
GET /google-play/androidpublisher/v3/applications/{packageName}/reviews/{reviewId}
```

#### 回复评价

```bash
POST /google-play/androidpublisher/v3/applications/{packageName}/reviews/{reviewId}:reply
Content-Type: application/json

{
  "replyText": "Thank you for your feedback!"
}
```

### 应用更新

#### 创建更新请求

```bash
POST /google-play/androidpublisher/v3/applications/{packageName}/edits
```

#### 获取更新信息

```bash
GET /google-play/androidpublisher/v3/applications/{packageName}/edits/{editId}
```

#### 提交更新

```bash
POST /google-play/androidpublisher/v3/applications/{packageName}/edits/{editId}:commit
```

#### 删除更新请求

```bash
DELETE /google-play/androidpublisher/v3/applications/{packageName}/edits/{editId}
```

## 代码示例

### JavaScript

```javascript
// List in-app products
const packageName = 'com.example.app';
const response = await fetch(
  `https://gateway.maton.ai/google-play/androidpublisher/v3/applications/${packageName}/inappproducts`,
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);

const products = await response.json();
console.log(products);
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
package_name = 'com.example.app'

# List in-app products
response = requests.get(
    f'https://gateway.maton.ai/google-play/androidpublisher/v3/applications/{package_name}/inappproducts',
    headers=headers
)
products = response.json()
print(products)
```

## 注意事项

- 请将 `{packageName}` 替换为您应用的包名（例如：`com.example.app`）。
- 使用 Google Play 开发者 API 需要您的应用已发布到 Google Play。
- 管理订阅服务的前提是您的应用已配置了有效的订阅功能。
- 更新操作是事务性的——先创建更新请求，进行修改，然后提交。
- 重要提示：当 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致 “无效 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Google Play 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 未找到相应的应用或无法访问 |
| 429 | 每个账户的请求速率限制（每秒 10 次） |
| 4xx/5xx | 来自 Google Play API 的传递错误 |

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

### 故障排除：应用名称错误

1. 确保您的 URL 路径以 `google-play` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/google-play/androidpublisher/v3/applications/{packageName}/inappproducts`
- 错误的路径：`https://gateway.maton.ai/androidpublisher/v3/applications/{packageName}/inappproducts`

## 资源

- [Android Publisher API 概述](https://developers.google.com/android-publisher)
- [应用内产品](https://developers.google.com/android-publisher/api-ref/rest/v3/inappproducts)
- [订阅服务](https://developers.google.com/android-publisher/api-ref/rest/v3/monetizationsubscriptions)
- [购买记录](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases/products)
- [用户评价](https://developers.google.com/android-publisher/api-ref/rest/v3/reviews)
- [应用更新](https://developers.google.com/android-publisher/api-ref/rest/v3/edits)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)