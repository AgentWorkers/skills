---
name: chargebee
description: |
  Chargebee API integration with managed OAuth. Manage subscriptions, customers, invoices, and hosted checkout pages. Use this skill when users want to interact with Chargebee billing data. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Chargebee

通过管理的OAuth认证访问Chargebee API，以管理订阅、客户、发票和计费流程。

## 快速入门

```bash
# List customers
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/chargebee/api/v2/customers?limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/chargebee/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Chargebee API端点路径。该网关会将请求代理到 `{subdomain}.chargebee.com`（会根据您的连接配置自动替换），并自动处理身份验证。

## 身份验证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的API密钥

1. 在 [maton.ai](https://maton.ai) 注册或登录账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 Chargebee 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=chargebee&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'chargebee'}).encode()
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
    "app": "chargebee",
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

如果您有多个 Chargebee 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/chargebee/api/v2/customers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用默认的（最旧的）活动连接。

## API 参考

### 客户

#### 列出客户

```bash
GET /chargebee/api/v2/customers?limit=10
```

#### 获取客户信息

```bash
GET /chargebee/api/v2/customers/{customerId}
```

#### 创建客户

```bash
POST /chargebee/api/v2/customers
Content-Type: application/x-www-form-urlencoded

first_name=John&last_name=Doe&email=john@example.com
```

#### 更新客户信息

```bash
POST /chargebee/api/v2/customers/{customerId}
Content-Type: application/x-www-form-urlencoded

first_name=Jane
```

### 订阅

#### 列出订阅信息

```bash
GET /chargebee/api/v2/subscriptions?limit=10
```

#### 获取订阅信息

```bash
GET /chargebee/api/v2/subscriptions/{subscriptionId}
```

#### 创建订阅

```bash
POST /chargebee/api/v2/subscriptions
Content-Type: application/x-www-form-urlencoded

plan_id=basic-plan&customer[email]=john@example.com&customer[first_name]=John
```

#### 取消订阅

```bash
POST /chargebee/api/v2/subscriptions/{subscriptionId}/cancel
Content-Type: application/x-www-form-urlencoded

end_of_term=true
```

### 产品价格（产品目录 2.0）

#### 列出产品价格

```bash
GET /chargebee/api/v2/item_prices?limit=10
```

### 产品信息

#### 列出产品

```bash
GET /chargebee/api/v2/items?limit=10
```

### 发票

#### 列出发票信息

```bash
GET /chargebee/api/v2/invoices?limit=10
```

#### 下载发票 PDF

```bash
POST /chargebee/api/v2/invoices/{invoiceId}/pdf
```

### 托管页面

#### 创建新的订阅页面

```bash
POST /chargebee/api/v2/hosted_pages/checkout_new_for_items
Content-Type: application/x-www-form-urlencoded

subscription[plan_id]=basic-plan&customer[email]=john@example.com
```

### 门户会话

#### 创建门户会话

```bash
POST /chargebee/api/v2/portal_sessions
Content-Type: application/x-www-form-urlencoded

customer[id]=cust_123
```

## 过滤

```bash
GET /chargebee/api/v2/subscriptions?status[is]=active
GET /chargebee/api/v2/customers?email[is]=john@example.com
GET /chargebee/api/v2/invoices?date[after]=1704067200
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/chargebee/api/v2/customers?limit=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/chargebee/api/v2/customers',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'limit': 10}
)
```

## 注意事项

- POST 请求使用 `form-urlencoded` 格式的数据。
- 嵌套对象使用方括号表示法：`customer[email]`。
- 时间戳为 Unix 时间戳。
- 列表响应包含 `next_offset` 用于分页。
- 产品目录 2.0：使用 `item_prices` 和 `items`。
- 重要提示：当 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 选项来禁用全局解析。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开，这可能导致 “无效的 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Chargebee 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（10 次/秒） |
| 4xx/5xx | 来自 Chargebee API 的传递错误 |

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

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `chargebee` 开头。例如：
- 正确：`https://gateway.maton.ai/chargebee/api/v2/customers`
- 错误：`https://gateway.maton.ai/api/v2/customers`

## 资源

- [Chargebee API 概述](https://apidocs.chargebee.com/docs/api)
- [客户](https://apidocs.chargebee.com/docs/api/customers)
- [订阅](https://apidocs.chargebee.com/docs/api/subscriptions)
- [发票](https://apidocs.chargebee.com/docs/api/invoices)
- [托管页面](https://apidocs.chargebee.com/docs/api/hosted_pages)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)