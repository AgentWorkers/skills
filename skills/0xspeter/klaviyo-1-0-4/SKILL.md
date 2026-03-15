---
name: klaviyo
description: Klaviyo API与托管的OAuth集成：支持访问用户资料、列表、细分群体、营销活动、工作流程、事件数据、指标信息、模板、产品目录以及Webhook功能。当用户需要管理电子邮件营销活动、客户数据或与Klaviyo的工作流程进行集成时，可使用此功能。对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
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
# Klaviyo

您可以使用托管的 OAuth 认证来访问 Klaviyo API。该 API 支持管理电子邮件营销和客户互动相关的各种功能，包括配置文件、列表、受众群体、营销活动、流程、事件、指标、模板、产品目录以及 Webhook 等。

## 快速入门

```bash
# List profiles
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/profiles')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/klaviyo/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Klaviyo API 端点路径。该代理会将请求转发到 `a.klaviyo.com` 并自动插入您的 OAuth 令牌。

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
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## API 版本控制

Klaviyo 使用基于日期的 API 版本控制。请在所有请求中包含 `revision` 头部：

```
revision: 2026-01-15
```

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Klaviyo OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=klaviyo&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'klaviyo'}).encode()
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
    "app": "klaviyo",
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

如果您有多个 Klaviyo 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/profiles')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，代理将使用默认的（最旧的）活动连接。

## API 参考

### 配置文件

用于管理客户数据和同意设置。

#### 获取配置文件信息

```bash
GET /klaviyo/api/profiles
```

查询参数：
- `filter` - 筛选配置文件（例如：`filter=equals(email,"test@example.com")`
- `fields[profile]` - 要包含的字段列表（用逗号分隔）
- `page[cursor]` - 分页游标
- `page[size]` - 每页的结果数量（最多 100 个）
- `sort` - 排序字段（以 `-` 开头表示降序）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/profiles?fields[profile]=email,first_name,last_name&page[size]=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "type": "profile",
      "id": "01GDDKASAP8TKDDA2GRZDSVP4H",
      "attributes": {
        "email": "alice@example.com",
        "first_name": "Alice",
        "last_name": "Johnson"
      }
    }
  ],
  "links": {
    "self": "https://a.klaviyo.com/api/profiles",
    "next": "https://a.klaviyo.com/api/profiles?page[cursor]=..."
  }
}
```

#### 获取单个配置文件信息

```bash
GET /klaviyo/api/profiles/{profile_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/profiles/01GDDKASAP8TKDDA2GRZDSVP4H')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建配置文件

```bash
POST /klaviyo/api/profiles
Content-Type: application/json

{
  "data": {
    "type": "profile",
    "attributes": {
      "email": "newuser@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "phone_number": "+15551234567",
      "properties": {
        "custom_field": "value"
      }
    }
  }
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'type': 'profile', 'attributes': {'email': 'newuser@example.com', 'first_name': 'John', 'last_name': 'Doe'}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/profiles', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新配置文件

```bash
PATCH /klaviyo/api/profiles/{profile_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'type': 'profile', 'id': '01GDDKASAP8TKDDA2GRZDSVP4H', 'attributes': {'first_name': 'Jane'}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/profiles/01GDDKASAP8TKDDA2GRZDSVP4H', data=data, method='PATCH')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 合并配置文件

```bash
POST /klaviyo/api/profile-merge
```

#### 获取配置文件列表

```bash
GET /klaviyo/api/profiles/{profile_id}/lists
```

#### 获取配置文件受众群体

```bash
GET /klaviyo/api/profiles/{profile_id}/segments
```

### 列表

用于将订阅者组织到静态列表中。

#### 获取列表信息

```bash
GET /klaviyo/api/lists
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/lists?fields[list]=name,created,updated')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "type": "list",
      "id": "Y6nRLr",
      "attributes": {
        "name": "Newsletter Subscribers",
        "created": "2024-01-15T10:30:00Z",
        "updated": "2024-03-01T14:22:00Z"
      }
    }
  ]
}
```

#### 创建列表

```bash
GET /klaviyo/api/lists/{list_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'type': 'list', 'attributes': {'name': 'VIP Customers'}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/lists', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新列表

```bash
PATCH /klaviyo/api/lists/{list_id}
```

#### 删除列表

```bash
DELETE /klaviyo/api/lists/{list_id}
```

#### 将配置文件添加到列表中

```bash
POST /klaviyo/api/lists/{list_id}/relationships/profiles
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': [{'type': 'profile', 'id': '01GDDKASAP8TKDDA2GRZDSVP4H'}]}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/lists/Y6nRLr/relationships/profiles', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 从列表中删除配置文件

```bash
DELETE /klaviyo/api/lists/{list_id}/relationships/profiles
```

#### 获取列表中的配置文件信息

```bash
GET /klaviyo/api/lists/{list_id}/profiles
```

### 观众群体

根据条件创建动态受众群体。

#### 获取受众群体信息

```bash
GET /klaviyo/api/segments
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/segments?fields[segment]=name,created,updated')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取单个受众群体信息

```bash
GET /klaviyo/api/segments/{segment_id}
```

#### 创建受众群体

```bash
POST /klaviyo/api/segments
```

**示例：**

```bash
PATCH /klaviyo/api/segments/{segment_id}
```

#### 更新受众群体

```bash
DELETE /klaviyo/api/segments/{segment_id}
```

#### 删除受众群体

```bash
GET /klaviyo/api/segments/{segment_id}/profiles
```

#### 获取受众群体配置文件信息

```bash
GET /klaviyo/api/segments/{segment_id}/profiles
```

### 营销活动

设计和发送电子邮件营销活动。

#### 获取营销活动信息

```bash
GET /klaviyo/api/campaigns
```

> **注意：** 需要指定渠道。可以使用 `filter=equals(messages.channel,"email")` 或 `filter=equals(messages.channel,"sms")` 进行筛选。

查询参数：
- `filter` - **必填** - 按渠道筛选（例如：`filter=equals(messages.channel,"email")`
- `fields[campaign]` - 要包含的字段
- `sort` - 按字段排序

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/campaigns?filter=equals(messages.channel,"email")')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "type": "campaign",
      "id": "01GDDKASAP8TKDDA2GRZDSVP4I",
      "attributes": {
        "name": "Spring Sale 2024",
        "status": "Draft",
        "audiences": {
          "included": ["Y6nRLr"],
          "excluded": []
        },
        "send_options": {
          "use_smart_sending": true
        }
      }
    }
  ]
}
```

#### 获取单个营销活动信息

```bash
GET /klaviyo/api/campaigns/{campaign_id}
```

#### 创建营销活动

```bash
POST /klaviyo/api/campaigns
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'type': 'campaign', 'attributes': {'name': 'Summer Newsletter', 'audiences': {'included': ['Y6nRLr']}, 'campaign-messages': {'data': [{'type': 'campaign-message', 'attributes': {'channel': 'email'}}]}}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/campaigns', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新营销活动

```bash
PATCH /klaviyo/api/campaigns/{campaign_id}
```

#### 删除营销活动

```bash
DELETE /klaviyo/api/campaigns/{campaign_id}
```

#### 发送营销活动

```bash
POST /klaviyo/api/campaign-send-jobs
```

#### 获取接收者预估信息

```bash
POST /klaviyo/api/campaign-recipient-estimations
```

### 流程

用于构建自动化的客户互动流程。

#### 获取流程信息

```bash
GET /klaviyo/api/flows
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/flows?fields[flow]=name,status,created,updated')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "type": "flow",
      "id": "VJvBNr",
      "attributes": {
        "name": "Welcome Series",
        "status": "live",
        "created": "2024-01-10T08:00:00Z",
        "updated": "2024-02-15T12:30:00Z"
      }
    }
  ]
}
```

#### 创建流程

```bash
GET /klaviyo/api/flows/{flow_id}
```

> **注意：** 通过 API 创建流程可能会受到限制。通常建议先通过 Klaviyo UI 创建流程，然后再通过 API 进行管理。对于现有流程，可以使用 GET、PATCH 和 DELETE 操作。

#### 更新流程状态

```bash
PATCH /klaviyo/api/flows/{flow_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'type': 'flow', 'id': 'VJvBNr', 'attributes': {'status': 'draft'}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/flows/VJvBNr', data=data, method='PATCH')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 删除流程

```bash
DELETE /klaviyo/api/flows/{flow_id}
```

#### 获取流程操作信息

```bash
GET /klaviyo/api/flows/{flow_id}/flow-actions
```

#### 获取流程中的消息

```bash
GET /klaviyo/api/flows/{flow_id}/flow-messages
```

### 事件

用于跟踪客户互动和行为。

#### 获取事件信息

```bash
GET /klaviyo/api/events
```

查询参数：
- `filter` - 筛选事件（例如：`filter=equals(metric_id,"ABC123")`
- `fields[event]` - 要包含的字段
- `sort` - 按字段排序（默认：`-datetime`）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/events?filter=greater-than(datetime,2024-01-01T00:00:00Z)&page[size]=50')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "type": "event",
      "id": "4vRpBT",
      "attributes": {
        "metric_id": "TxVpCr",
        "profile_id": "01GDDKASAP8TKDDA2GRZDSVP4H",
        "datetime": "2024-03-15T14:30:00Z",
        "event_properties": {
          "value": 99.99,
          "product_name": "Running Shoes"
        }
      }
    }
  ]
}
```

#### 获取单个事件信息

```bash
GET /klaviyo/api/events/{event_id}
```

#### 创建事件

```bash
POST /klaviyo/api/events
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'type': 'event', 'attributes': {'profile': {'data': {'type': 'profile', 'attributes': {'email': 'customer@example.com'}}}, 'metric': {'data': {'type': 'metric', 'attributes': {'name': 'Viewed Product'}}}, 'properties': {'product_id': 'SKU123', 'product_name': 'Blue T-Shirt', 'price': 29.99}}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/events', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 批量创建事件

```bash
POST /klaviyo/api/event-bulk-create-jobs
```

### 指标

用于访问性能数据和分析信息。

#### 获取指标信息

```bash
GET /klaviyo/api/metrics
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/metrics')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "type": "metric",
      "id": "TxVpCr",
      "attributes": {
        "name": "Placed Order",
        "created": "2024-01-01T00:00:00Z",
        "updated": "2024-03-01T00:00:00Z",
        "integration": {
          "object": "integration",
          "id": "shopify",
          "name": "Shopify"
        }
      }
    }
  ]
}
```

#### 获取单个指标信息

```bash
GET /klaviyo/api/metrics/{metric_id}
```

#### 查询指标聚合数据

```bash
POST /klaviyo/api/metric-aggregates
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'type': 'metric-aggregate', 'attributes': {'metric_id': 'TxVpCr', 'measurements': ['count', 'sum_value'], 'interval': 'day', 'filter': ['greater-or-equal(datetime,2024-01-01)', 'less-than(datetime,2024-04-01)']}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/metric-aggregates', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 模板

用于管理电子邮件模板。

#### 获取模板信息

```bash
GET /klaviyo/api/templates
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/templates?fields[template]=name,created,updated')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取单个模板信息

```bash
GET /klaviyo/api/templates/{template_id}
```

#### 创建模板

```bash
POST /klaviyo/api/templates
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'type': 'template', 'attributes': {'name': 'Welcome Email', 'editor_type': 'CODE', 'html': '<html><body><h1>Welcome!</h1></body></html>'}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/templates', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新模板

```bash
PATCH /klaviyo/api/templates/{template_id}
```

#### 删除模板

```bash
DELETE /klaviyo/api/templates/{template_id}
```

#### 渲染模板

```bash
POST /klaviyo/api/template-render
```

#### 复制模板

```bash
POST /klaviyo/api/template-clone
```

### 产品目录

用于管理产品目录。

#### 获取产品目录信息

```bash
GET /klaviyo/api/catalog-items
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/catalog-items?fields[catalog-item]=title,price,url')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "type": "catalog-item",
      "id": "$custom:::$default:::PROD-001",
      "attributes": {
        "title": "Blue Running Shoes",
        "price": 129.99,
        "url": "https://store.example.com/products/blue-running-shoes"
      }
    }
  ]
}
```

#### 获取单个产品目录项信息

```bash
GET /klaviyo/api/catalog-items/{catalog_item_id}
```

#### 创建产品目录项

```bash
POST /klaviyo/api/catalog-items
```

#### 更新产品目录项

```bash
PATCH /klaviyo/api/catalog-items/{catalog_item_id}
```

#### 删除产品目录项

```bash
DELETE /klaviyo/api/catalog-items/{catalog_item_id}
```

#### 获取产品目录变体

```bash
GET /klaviyo/api/catalog-variants
```

#### 获取产品目录分类

```bash
GET /klaviyo/api/catalog-categories
```

### 标签

用于对资源进行分类。

#### 获取标签信息

```bash
GET /klaviyo/api/tags
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/tags')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建标签

```bash
POST /klaviyo/api/tags
```

#### 更新标签

```bash
PATCH /klaviyo/api/tags/{tag_id}
```

#### 删除标签

```bash
DELETE /klaviyo/api/tags/{tag_id}
```

#### 为营销活动或流程添加标签

```bash
POST /klaviyo/api/tag-campaign-relationships
```

#### 为标签组添加标签

```bash
POST /klaviyo/api/tag-flow-relationships
```

#### 获取标签组信息

```bash
GET /klaviyo/api/tag-groups
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/tag-groups')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建标签组

```bash
POST /klaviyo/api/tag-groups
```

#### 更新标签组

```bash
PATCH /klaviyo/api/tag-groups/{tag_group_id}
```

#### 删除标签组

```bash
DELETE /klaviyo/api/tag-groups/{tag_group_id}
```

### 优惠券

用于管理折扣代码。

#### 获取优惠券信息

```bash
GET /klaviyo/api/coupons
```

**示例：**

```bash
POST /klaviyo/api/coupons
```

**示例：**

> **注意：** `external_id` 必须符合正则表达式 `^[0-9_A-z]+$`（仅允许字母、数字和下划线，不允许使用连字符）。

#### 获取优惠券代码

```bash
GET /klaviyo/api/coupon-codes
```

> **注意：** 此端点需要一个过滤参数。您必须根据优惠券 ID 或配置文件 ID 进行筛选。

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/coupon-codes?filter=equals(coupon.id,"SUMMER_SALE_2024")')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建优惠券代码

```bash
POST /klaviyo/api/coupon-codes
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'type': 'coupon-code', 'attributes': {'unique_code': 'SAVE20NOW', 'expires_at': '2025-12-31T23:59:59Z'}, 'relationships': {'coupon': {'data': {'type': 'coupon', 'id': 'SUMMER_SALE_2024'}}}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/coupon-codes', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Webhook

用于配置事件通知。

#### 获取 Webhook 信息

```bash
GET /klaviyo/api/webhooks
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/webhooks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建 Webhook

```bash
POST /klaviyo/api/webhooks
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'type': 'webhook', 'attributes': {'name': 'Order Placed Webhook', 'endpoint_url': 'https://example.com/webhooks/klaviyo', 'enabled': True}, 'relationships': {'webhook-topics': {'data': [{'type': 'webhook-topic', 'id': 'campaign:sent'}]}}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/webhooks', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取 Webhook 信息

```bash
GET /klaviyo/api/webhooks/{webhook_id}
```

#### 更新 Webhook

```bash
PATCH /klaviyo/api/webhooks/{webhook_id}
```

#### 删除 Webhook

```bash
DELETE /klaviyo/api/webhooks/{webhook_id}
```

#### 获取 Webhook 主题信息

```bash
GET /klaviyo/api/webhook-topics
```

### 账户

用于检索账户信息。

#### 获取账户信息

```bash
GET /klaviyo/api/accounts
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/accounts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 图片

用于管理上传的图片。

#### 获取图片信息

```bash
GET /klaviyo/api/images
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/images')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取图片信息

```bash
GET /klaviyo/api/images/{image_id}
```

#### 从 URL 上传图片

```bash
POST /klaviyo/api/images
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'type': 'image', 'attributes': {'import_from_url': 'https://example.com/image.jpg', 'name': 'Product Image'}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/images', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 表单

用于管理注册表单。

#### 获取表单信息

```bash
GET /klaviyo/api/forms
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/forms')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**示例：**

```bash
GET /klaviyo/api/forms/{form_id}
```

#### 获取表单版本信息

```bash
GET /klaviyo/api/forms/{form_id}/form-versions
```

### 评论

用于管理产品评论。

#### 获取评论信息

```bash
GET /klaviyo/api/reviews
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/reviews')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**示例：**

```bash
GET /klaviyo/api/reviews/{review_id}
```

#### 获取单个评论信息

```bash
PATCH /klaviyo/api/reviews/{review_id}
```

#### 更新评论

```bash
PATCH /klaviyo/api/reviews/{review_id}
```

### 通用内容

用于管理可重用的电子邮件内容块。

#### 获取通用内容信息

```bash
GET /klaviyo/api/template-universal-content
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/template-universal-content')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建通用内容

```bash
POST /klaviyo/api/template-universal-content
```

#### 更新通用内容

```bash
PATCH /klaviyo/api/template-universal-content/{content_id}
```

#### 删除通用内容

```bash
DELETE /klaviyo/api/template-universal-content/{content_id}
```

### 批量操作

- **批量订阅配置文件**：批量管理电子邮件/SMS 订阅。
- **批量取消订阅配置文件**：批量取消订阅配置文件。
- **批量暂停配置文件**：批量暂停配置文件的订阅。
- **批量恢复配置文件的订阅**：批量恢复配置文件的订阅。
- **批量导入配置文件**：批量导入配置文件。

#### 获取批量导入作业信息

```bash
GET /klaviyo/api/profile-bulk-import-jobs
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/profile-bulk-import-jobs')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**示例：**

```bash
POST /klaviyo/api/profile-bulk-import-jobs
```

## 过滤

Klaviyo 使用 JSON:API 过滤语法。常用操作符如下：

| 操作符 | 示例 |
|----------|---------|
| `equals` | `filter=equals(email,"test@example.com")` |
| `contains` | `filter=contains(name,"newsletter")` |
| `greater-than` | `filter=greater-than(datetime,2024-01-01T00:00:00Z)` |
| `less-than` | `filter=less-than(created,2024-03-01)` |
| `greater-or-equal` | `filter=greater-or-equal(updated,2024-01-01)` |
| `any` | `filter=any(status,["draft","scheduled"])` |

可以使用 `and` 连接多个过滤条件：

```
filter=and(equals(status,"active"),greater-than(created,2024-01-01))
```

## 分页

Klaviyo 使用基于游标的分页机制：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/profiles?page[size]=50&page[cursor]=CURSOR_TOKEN')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

响应中包含分页链接：

```json
{
  "data": [...],
  "links": {
    "self": "https://a.klaviyo.com/api/profiles",
    "next": "https://a.klaviyo.com/api/profiles?page[cursor]=WzE2..."
  }
}
```

## 精简字段集

仅请求特定字段以减少响应大小：

```bash
# Request only email and first_name for profiles
?fields[profile]=email,first_name

# Request specific fields for included relationships
?include=lists&fields[list]=name,created
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/klaviyo/api/profiles?fields[profile]=email,first_name',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'revision': '2024-10-15'
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
    'https://gateway.maton.ai/klaviyo/api/profiles',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'revision': '2024-10-15'
    },
    params={'fields[profile]': 'email,first_name'}
)
data = response.json()
```

## 注意事项

- 所有请求都遵循 JSON:API 规范。
- 时间戳采用 ISO 8601 RFC 3339 格式（例如：`2024-01-16T23:20:50.52Z`）。
- 资源 ID 为字符串（通常经过 Base64 编码）。
- 使用精简字段集以优化响应大小。
- 请在请求中包含 `revision` 头部以进行 API 版本控制（推荐使用 `2026-01-15`）。
- 某些 POST 端点在成功创建资源时返回 `200` 而不是 `201`。
- 优惠券的 `external_id` 必须符合正则表达式 `^[0-9_A-z]+$`（不允许使用连字符）。
- 使用 API 创建流程可能会受到限制；通常建议先通过 Klaviyo UI 创建流程，然后再通过 API 进行管理。
- **重要提示：** 当 URL 中包含方括号（如 `fields[]`、`page[]`）时，使用 `curl -g` 选项以避免全局解析问题。
- **重要提示：** 在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致 “Invalid API key” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或未建立 Klaviyo 连接 |
| 401 | 无效或未设置的 Maton API 密钥 |
| 403 | 禁止访问 - 权限不足 |
| 404 | 资源未找到 |
| 429 | 请求速率限制（基于固定时间窗口的算法） |
| 4xx/5xx | 来自 Klaviyo API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保已设置 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出所有连接来验证 API 密钥的有效性：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称错误

1. 确保您的 URL 路径以 `klaviyo` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/klaviyo/api/profiles`
- 错误的路径：`https://gateway.maton.ai/api/profiles`

## 资源链接

- [Klaviyo API 文档](https://developers.klaviyo.com)
- [API 参考](https://developers.klaviyo.com/en/reference/api_overview)
- [Klaviyo 开发者门户](https://developers.klaviyo.com/en)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持团队](mailto:support@maton.ai)