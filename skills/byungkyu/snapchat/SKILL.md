---
name: snapchat
description: >
  **Snapchat营销API集成（支持OAuth认证）**  
  该功能允许用户管理广告账户、广告活动、广告团队、广告内容以及目标受众。当用户需要创建或管理Snapchat广告活动、查看广告效果数据或调整广告定位策略时，可使用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。  
  使用此功能需要网络连接以及有效的Maton API密钥。
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Snapchat

您可以使用托管的 OAuth 认证来访问 Snapchat Marketing API。该 API 允许您管理组织、广告账户、广告活动、广告团队、广告内容、媒体文件以及目标受众。

## 快速入门

```bash
# List your organizations
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/snapchat/v1/me/organizations')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/snapchat/{api-path}
```

Snapchat Marketing API 使用以下路径模式：
```
https://gateway.maton.ai/snapchat/v1/{resource}
```

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

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Snapchat OAuth 连接。

### 列出连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=snapchat&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python3 <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'snapchat'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python3 <<'EOF'
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
    "connection_id": "f5d5458b-fb65-458c-9e51-08844662dd39",
    "status": "ACTIVE",
    "creation_time": "2026-02-14T00:00:00.000000Z",
    "last_updated_time": "2026-02-14T00:00:00.000000Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "snapchat",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 Snapchat 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/snapchat/v1/me/organizations')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'f5d5458b-fb65-458c-9e51-08844662dd39')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，系统将使用默认的（最旧的）活动连接。

## API 参考

### 当前用户

#### 获取当前用户信息

```bash
GET /v1/me
```

**响应：**
```json
{
  "request_status": "SUCCESS",
  "request_id": "...",
  "me": {
    "id": "...",
    "email": "user@example.com",
    "display_name": "User Name"
  }
}
```

#### 列出我的组织

```bash
GET /v1/me/organizations
```

**响应：**
```json
{
  "request_status": "SUCCESS",
  "request_id": "...",
  "organizations": [
    {
      "sub_request_status": "SUCCESS",
      "organization": {
        "id": "63acee69-77ff-4378-8492-3f8d28e8f241",
        "name": "My Organization",
        "country": "US",
        "contact_name": "John Doe",
        "contact_email": "john@example.com"
      }
    }
  ]
}
```

### 组织

#### 获取组织信息

```bash
GET /v1/organizations/{organizationId}
```

#### 列出组织的广告账户

```bash
GET /v1/organizations/{organizationId}/adaccounts
```

#### 列出组织的资金来源

```bash
GET /v1/organizations/{organizationId}/fundingsources
```

#### 列出组织成员

```bash
GET /v1/organizations/{organizationId}/members
```

#### 列出组织角色

```bash
GET /v1/organizations/{organizationId}/roles
```

#### 列出产品目录

```bash
GET /v1/organizations/{organizationId}/catalogs
```

### 广告账户

#### 获取广告账户信息

```bash
GET /v1/adaccounts/{adAccountId}
```

**响应：**
```json
{
  "request_status": "SUCCESS",
  "request_id": "...",
  "adaccounts": [
    {
      "sub_request_status": "SUCCESS",
      "adaccount": {
        "id": "6e916ba9-db2f-40cd-9553-a90e32cedea3",
        "name": "My Ad Account",
        "type": "PARTNER",
        "status": "ACTIVE",
        "organization_id": "...",
        "currency": "USD",
        "timezone": "America/Los_Angeles"
      }
    }
  ]
}
```

#### 列出广告账户的角色

```bash
GET /v1/adaccounts/{adAccountId}/roles
```

### 广告活动

#### 列出广告活动

```bash
GET /v1/adaccounts/{adAccountId}/campaigns
GET /v1/adaccounts/{adAccountId}/campaigns?limit=50
```

**查询参数：**
- `limit` - 结果数量（50-1000）

#### 获取广告活动详细信息

```bash
GET /v1/campaigns/{campaignId}
```

#### 创建广告活动

```bash
POST /v1/adaccounts/{adAccountId}/campaigns
Content-Type: application/json

{
  "campaigns": [{
    "name": "Campaign Name",
    "status": "PAUSED",
    "ad_account_id": "{adAccountId}",
    "start_time": "2026-02-15T00:00:00.000-08:00"
  }]
}
```

#### 更新广告活动

```bash
PUT /v1/adaccounts/{adAccountId}/campaigns
Content-Type: application/json

{
  "campaigns": [{
    "id": "{campaignId}",
    "name": "Updated Campaign Name",
    "status": "ACTIVE"
  }]
}
```

#### 删除广告活动

```bash
DELETE /v1/campaigns/{campaignId}
```

### 广告团队

#### 列出广告团队

```bash
GET /v1/adaccounts/{adAccountId}/adsquads
GET /v1/campaigns/{campaignId}/adsquads
```

#### 获取广告团队信息

```bash
GET /v1/adsquads/{adSquadId}
```

#### 创建广告团队

```bash
POST /v1/campaigns/{campaignId}/adsquads
Content-Type: application/json

{
  "adsquads": [{
    "name": "Ad Squad Name",
    "status": "PAUSED",
    "campaign_id": "{campaignId}",
    "type": "SNAP_ADS",
    "placement": "SNAP_ADS",
    "optimization_goal": "IMPRESSIONS",
    "bid_micro": 1000000,
    "daily_budget_micro": 50000000,
    "start_time": "2026-02-15T00:00:00.000-08:00",
    "targeting": {
      "geos": [{"country_code": "us"}]
    }
  }]
}
```

#### 更新广告团队

```bash
PUT /v1/campaigns/{campaignId}/adsquads
Content-Type: application/json

{
  "adsquads": [{
    "id": "{adSquadId}",
    "name": "Updated Ad Squad Name"
  }]
}
```

#### 删除广告团队

```bash
DELETE /v1/adsquads/{adSquadId}
```

### 广告

#### 列出广告

```bash
GET /v1/adaccounts/{adAccountId}/ads
GET /v1/adsquads/{adSquadId}/ads
```

#### 获取广告详情

```bash
GET /v1/ads/{adId}
```

#### 创建广告

```bash
POST /v1/adsquads/{adSquadId}/ads
Content-Type: application/json

{
  "ads": [{
    "name": "Ad Name",
    "status": "PAUSED",
    "ad_squad_id": "{adSquadId}",
    "creative_id": "{creativeId}",
    "type": "SNAP_AD"
  }]
}
```

#### 更新广告内容

```bash
PUT /v1/adsquads/{adSquadId}/ads
Content-Type: application/json

{
  "ads": [{
    "id": "{adId}",
    "name": "Updated Ad Name"
  }]
}
```

#### 删除广告

```bash
DELETE /v1/ads/{adId}
```

### 广告内容

#### 列出广告内容

```bash
GET /v1/adaccounts/{adAccountId}/creatives
GET /v1/adaccounts/{adAccountId}/creatives?limit=50&sort=updated_at-desc
```

#### 获取广告内容详情

```bash
GET /v1/creatives/{creativeId}
```

#### 创建广告内容

```bash
POST /v1/adaccounts/{adAccountId}/creatives
Content-Type: application/json

{
  "creatives": [{
    "name": "Creative Name",
    "ad_account_id": "{adAccountId}",
    "type": "SNAP_AD",
    "top_snap_media_id": "{mediaId}",
    "headline": "Headline Text",
    "brand_name": "Brand Name",
    "call_to_action": "VIEW_MORE"
  }]
}
```

#### 更新广告内容

```bash
PUT /v1/adaccounts/{adAccountId}/creatives
Content-Type: application/json

{
  "creatives": [{
    "id": "{creativeId}",
    "name": "Updated Creative Name"
  }]
}
```

### 媒体文件

#### 列出媒体文件

```bash
GET /v1/adaccounts/{adAccountId}/media
GET /v1/adaccounts/{adAccountId}/media?limit=50&sort=created_at-desc
```

#### 获取媒体文件详情

```bash
GET /v1/media/{mediaId}
```

### 像素资源

#### 列出像素资源

```bash
GET /v1/adaccounts/{adAccountId}/pixels
```

#### 获取特定像素资源

```bash
GET /v1/pixels/{pixelId}
```

### 目标受众

#### 列出目标受众群体

```bash
GET /v1/adaccounts/{adAccountId}/segments
```

#### 获取目标受众信息

```bash
GET /v1/segments/{segmentId}
```

### 统计数据

#### 获取广告账户统计信息

```bash
GET /v1/adaccounts/{adAccountId}/stats?granularity=DAY&start_time=2026-02-01&end_time=2026-02-14
```

**查询参数：**
- `granularity` - 数据粒度（`HOUR`, `DAY`, `LIFETIME`）
- `start_time` - 开始日期（YYYY-MM-DD）
- `end_time` - 结束日期（YYYY-MM-DD）

#### 获取广告活动统计信息

```bash
GET /v1/campaigns/{campaignId}/stats?granularity=DAY&start_time=2026-02-01&end_time=2026-02-14
```

### 定位策略

#### 获取国家列表

```bash
GET /v1/targeting/geo/country
```

#### 按国家划分地区列表

```bash
GET /v1/targeting/geo/{countryCode}/region
```

示例：`GET /v1/targeting/geo/us/region`

#### 获取操作系统类型

```bash
GET /v1/targeting/device/os_type
```

#### 获取位置分类

```bash
GET /v1/targeting/location/categories_loi
```

### 广告库（公开广告库）

广告库 API 允许您访问 Snapchat 的公开广告信息。此 API 不需要认证，但可以通过 Maton 门户进行访问。

#### 列出赞助内容

```bash
GET /v1/ads_library/sponsored_content
```

**响应：**
```json
{
  "request_status": "SUCCESS",
  "request_id": "...",
  "sponsored_content": [
    {
      "sub_request_status": "SUCCESS",
      "sponsored_content": {
        "id": "...",
        "name": "Content Name",
        "status": "ACTIVE"
      }
    }
  ]
}
```

#### 搜索赞助内容

```bash
POST /v1/ads_library/sponsored_content/search
Content-Type: application/json

{
  "limit": 50
}
```

#### 按广告主名称和国家搜索广告

```bash
POST /v1/ads_library/ads/search
Content-Type: application/json

{
  "paying_advertiser_name": "Nike",
  "countries": ["fr", "de"],
  "limit": 50
}
```

**参数：**
- `paying_advertiser_name`（必填）- 要搜索的广告主名称
- `countries`（必填）- 2 位小写字母组成的 ISO 国家代码数组（例如：`["fr", "de", "gb"]`
- `start_date` - 时间范围的开始日期（ISO 8601 格式）
- `end_date` - 时间范围的结束日期（ISO 8601 格式）
- `status` - 过滤条件（例如：`"ACTIVE", "PAUSED"）
- `limit` - 返回的结果数量

**注意：** 并非所有国家都可以在广告库中找到。支持欧盟国家（如 fr, de, gb 等）。由于地区限制，美国广告可能无法显示。

**响应：**
```json
{
  "request_status": "SUCCESS",
  "request_id": "...",
  "paging": {
    "next_link": "..."
  },
  "ad_previews": [
    {
      "sub_request_status": "SUCCESS",
      "ad_preview": {
        "id": "...",
        "name": "Ad Name",
        "ad_account_name": "Advertiser Name",
        "status": "ACTIVE",
        "creative_type": "WEB_VIEW",
        "headline": "Ad Headline",
        "call_to_action": "SHOP NOW"
      }
    }
  ]
}
```

## 分页

Snapchat API 使用基于游标的分页机制（`limit` 参数，范围为 50-1000），并返回包含 `next_link` 的 `paging` 对象。

```bash
GET /v1/adaccounts/{adAccountId}/campaigns?limit=50
```

**响应：**
```json
{
  "request_status": "SUCCESS",
  "campaigns": [...],
  "paging": {
    "next_link": "https://adsapi.snapchat.com/v1/adaccounts/{id}/campaigns?cursor=..."
  }
}
```

要获取下一页，请使用 `next_link`（请将主机替换为 Maton 门户的地址）：

```bash
GET /v1/adaccounts/{adAccountId}/campaigns?cursor=...
```

## 排序

某些 API 端点支持使用 `sort` 参数进行排序：

```bash
GET /v1/adaccounts/{adAccountId}/creatives?sort=updated_at-desc
GET /v1/adaccounts/{adAccountId}/media?sort=created_at-desc
```

支持的排序方式：`updated_at-desc`, `created_at-desc`

## 代码示例

### JavaScript

```javascript
// List organizations
const response = await fetch(
  'https://gateway.maton.ai/snapchat/v1/me/organizations',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.organizations);
```

### Python

```python
import os
import requests

# List organizations
response = requests.get(
    'https://gateway.maton.ai/snapchat/v1/me/organizations',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
print(data['organizations'])
```

### 示例：列出所有广告活动

```python
import os
import requests

org_id = "YOUR_ORG_ID"
headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# Get ad accounts
response = requests.get(
    f'https://gateway.maton.ai/snapchat/v1/organizations/{org_id}/adaccounts',
    headers=headers
)
ad_accounts = response.json()['adaccounts']

# List campaigns for each ad account
for aa in ad_accounts:
    ad_account_id = aa['adaccount']['id']
    campaigns = requests.get(
        f'https://gateway.maton.ai/snapchat/v1/adaccounts/{ad_account_id}/campaigns',
        headers=headers
    ).json()
    print(f"Ad Account: {aa['adaccount']['name']}")
    print(f"Campaigns: {campaigns}")
```

## 注意事项

- **货币单位**：所有货币值均以微货币（1 USD = 1,000,000 微货币）为单位。
- **批量操作**：创建/更新操作支持使用数组进行批量处理。
- **响应格式**：所有响应包含 `request_status`, `request_id` 以及包含 `sub_request_status` 的实体数组。
- **时间戳**：使用带有时区的 ISO 8601 格式（例如：`2026-02-15T00:00:00.000-08:00`）。
- **广告库国家**：并非所有国家都可以在广告库中找到。支持欧盟国家（如 fr, de, gb 等）。
- **转换 API**：转换 API 使用不同的基础 URL（`tr.snapchat.com`），目前不通过此门户路由。
- **公共资料 API**：公共资料 API 可能不可用或需要单独配置。
- **重要提示**：当将 curl 输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）在某些 shell 环境中可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或参数无效 |
| 401 | API 密钥无效或令牌过期 |
| 403 | 没有权限 |
| 404 | 资源未找到 |
| 429 | 请求次数受限 |
| 4xx/5xx | 来自 Snapchat API 的传递错误 |

### 响应错误格式

```json
{
  "request_status": "ERROR",
  "request_id": "...",
  "debug_message": "Error details",
  "display_message": "User-friendly message"
}
```

## 参考资源

- [Snapchat 广告 API 介绍](https://developers.snap.com/api/marketing-api/Ads-API/introduction)
- [API 使用规范](https://developers.snap.com/api/marketing-api/Ads-API/api-patterns)
- [广告活动管理](https://developers.snap.com/api/marketing-api/Ads-API/campaigns)
- [广告内容管理](https://developers.snap.com/api/marketing-api/Ads-API/creatives)
- [定位策略](https://developers.snap.com/api/marketing-api/Ads-API/targeting)
- [广告库 API](https://developers.snap.com/api/marketing-api/Ads-Gallery-Api/using-the-api)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持团队](mailto:support@maton.ai)