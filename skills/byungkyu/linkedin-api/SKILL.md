---
name: linkedin
description: >
  **LinkedIn API集成（支持管理型OAuth）**  
  该功能允许用户分享内容到LinkedIn、管理广告活动、获取个人资料/组织信息，以及访问LinkedIn平台的各项功能。  
  当用户需要将内容发布到LinkedIn、执行广告投放、查看个人资料或组织信息，或与LinkedIn平台进行交互时，可使用此功能。  
  对于其他第三方应用程序，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。  
  使用此功能需要网络连接以及有效的Maton API密钥。
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---
# LinkedIn

您可以使用托管的 OAuth 认证来访问 LinkedIn API。该 API 支持分享帖子、管理广告活动、检索个人资料和组织信息、上传媒体文件以及访问广告库。

## 快速入门

```bash
# Get current user profile
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/linkedin/rest/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('LinkedIn-Version', '202506')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/linkedin/rest/{resource}
```

网关会将请求代理到 `api.linkedin.com`，并自动插入您的 OAuth 令牌。

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

### 必需的头部信息

LinkedIn REST API 需要 `version` 头部信息：

```
LinkedIn-Version: 202506
```

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 LinkedIn OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=linkedin&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'linkedin'}).encode()
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
    "connection_id": "ba10eb9e-b590-4e95-8c2e-3901ff94642a",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T08:00:24.372659Z",
    "last_updated_time": "2026-02-07T08:05:16.609085Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "linkedin",
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

如果您有多个 LinkedIn 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/linkedin/rest/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('LinkedIn-Version', '202506')
req.add_header('Maton-Connection', 'ba10eb9e-b590-4e95-8c2e-3901ff94642a')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用默认的（最旧的）活动连接。

## API 参考

### 个人资料

#### 获取当前用户个人资料

```bash
GET /linkedin/rest/me
LinkedIn-Version: 202506
```

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/linkedin/rest/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('LinkedIn-Version', '202506')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "firstName": {
    "localized": {"en_US": "John"},
    "preferredLocale": {"country": "US", "language": "en"}
  },
  "localizedFirstName": "John",
  "lastName": {
    "localized": {"en_US": "Doe"},
    "preferredLocale": {"country": "US", "language": "en"}
  },
  "localizedLastName": "Doe",
  "id": "yrZCpj2Z12",
  "vanityName": "johndoe",
  "localizedHeadline": "Software Engineer at Example Corp",
  "profilePicture": {
    "displayImage": "urn:li:digitalmediaAsset:C4D00AAAAbBCDEFGhiJ"
  }
}
```

### 分享帖子

#### 创建文本帖子

```bash
POST /linkedin/rest/posts
Content-Type: application/json
LinkedIn-Version: 202506

{
  "author": "urn:li:person:{personId}",
  "lifecycleState": "PUBLISHED",
  "visibility": "PUBLIC",
  "commentary": "Hello LinkedIn! This is my first API post.",
  "distribution": {
    "feedDistribution": "MAIN_FEED"
  }
}
```

**响应：** 返回 `201 Created`，同时 `x-restli-id` 头部包含帖子的 URI。

#### 创建文章/URL 共享

```bash
POST /linkedin/rest/posts
Content-Type: application/json
LinkedIn-Version: 202506

{
  "author": "urn:li:person:{personId}",
  "lifecycleState": "PUBLISHED",
  "visibility": "PUBLIC",
  "commentary": "Check out this great article!",
  "distribution": {
    "feedDistribution": "MAIN_FEED"
  },
  "content": {
    "article": {
      "source": "https://example.com/article",
      "title": "Article Title",
      "description": "Article description here"
    }
  }
}
```

#### 创建图片帖子

首先初始化图片上传，然后上传图片，最后创建帖子。

**步骤 1：初始化图片上传**
```bash
POST /linkedin/rest/images?action=initializeUpload
Content-Type: application/json
LinkedIn-Version: 202506

{
  "initializeUploadRequest": {
    "owner": "urn:li:person:{personId}"
  }
}
```

**响应：**
```json
{
  "value": {
    "uploadUrlExpiresAt": 1770541529250,
    "uploadUrl": "https://www.linkedin.com/dms-uploads/...",
    "image": "urn:li:image:D4D10AQH4GJAjaFCkHQ"
  }
}
```

**步骤 2：上传图片二进制文件**
```bash
PUT {uploadUrl from step 1}
Content-Type: image/png

{binary image data}
```

**步骤 3：创建图片帖子**
```bash
POST /linkedin/rest/posts
Content-Type: application/json
LinkedIn-Version: 202506

{
  "author": "urn:li:person:{personId}",
  "lifecycleState": "PUBLISHED",
  "visibility": "PUBLIC",
  "commentary": "Check out this image!",
  "distribution": {
    "feedDistribution": "MAIN_FEED"
  },
  "content": {
    "media": {
      "id": "urn:li:image:D4D10AQH4GJAjaFCkHQ",
      "title": "Image Title"
    }
  }
}
```

### 显示选项

| 值 | 描述 |
|-------|-------------|
| `PUBLIC` | 任何人在 LinkedIn 上都能看到 |
| `CONNECTIONS` | 仅限一级联系人看到 |

### 媒体分享类别

| 值 | 描述 |
|-------|-------------|
| `NONE` | 仅文本帖子 |
| `ARTICLE` | URL/文章分享 |
| `IMAGE` | 图片帖子 |
| `VIDEO` | 视频帖子 |

### 广告库（公共数据）

广告库 API 提供对 LinkedIn 上公共广告数据的访问。这些接口使用带版本号的 REST API。

#### 广告库所需的头部信息

```
LinkedIn-Version: 202506
```

#### 搜索广告

```bash
GET /linkedin/rest/adLibrary?q=criteria&keyword={keyword}
```

查询参数：
- `keyword` (string): 搜索广告内容（多个关键词使用 AND 逻辑）
- `advertiser` (string): 按广告商名称搜索
- `countries` (array): 按 ISO 3166-1 alpha-2 国家代码过滤
- `dateRange` (object): 按发布日期过滤
- `start` (integer): 分页偏移量
- `count` (integer): 每页结果数量（最多 25 条）

**示例 - 按关键词搜索广告：**
```bash
GET /linkedin/rest/adLibrary?q=criteria&keyword=linkedin
```

**示例 - 按广告商名称搜索广告：**
```bash
GET /linkedin/rest/adLibrary?q=criteria&advertiser=microsoft
```

**响应：**
```json
{
  "paging": {
    "start": 0,
    "count": 10,
    "total": 11619543,
    "links": [...]
  },
  "elements": [
    {
      "adUrl": "https://www.linkedin.com/ad-library/detail/...",
      "details": {
        "advertiser": {...},
        "adType": "TEXT_AD",
        "targeting": {...},
        "statistics": {
          "firstImpressionDate": 1704067200000,
          "latestImpressionDate": 1706745600000,
          "impressionsFrom": 1000,
          "impressionsTo": 5000
        }
      },
      "isRestricted": false
    }
  ]
}
```

#### 搜索职位信息

```bash
GET /linkedin/rest/jobLibrary?q=criteria&keyword={keyword}
```

**注意：** 职位信息 API 需要版本号 `202506`。

查询参数：
- `keyword` (string): 搜索职位内容
- `organization` (string): 按公司名称过滤
- `countries` (array): 按国家代码过滤
- `dateRange` (object): 按发布日期过滤
- `start` (integer): 分页偏移量
- `count` (integer): 每页结果数量（最多 24 条）

**示例：**
```bash
GET /linkedin/rest/jobLibrary?q=criteria&keyword=software&organization=google
```

**响应包含：**
- `jobPostingUrl`: 职位列表链接
- `jobDetails`: 标题、位置、描述、薪资、福利
- `statistics`: 浏览量数据

### 营销 API（广告）

营销 API 提供对 LinkedIn 广告平台的访问。这些接口使用带版本号的 REST API。

#### 营销 API 所需的头部信息

```
LinkedIn-Version: 202506
```

#### 列出广告账户

```bash
GET /linkedin/rest/adAccounts?q=search
```

返回当前用户可访问的所有广告账户。

**响应：**
```json
{
  "paging": {
    "start": 0,
    "count": 10,
    "links": []
  },
  "elements": [
    {
      "id": 123456789,
      "name": "My Ad Account",
      "status": "ACTIVE",
      "type": "BUSINESS",
      "currency": "USD",
      "reference": "urn:li:organization:12345"
    }
  ]
}
```

#### 获取广告账户

```bash
GET /linkedin/rest/adAccounts/{adAccountId}
```

#### 创建广告账户

```bash
POST /linkedin/rest/adAccounts
Content-Type: application/json

{
  "name": "New Ad Account",
  "currency": "USD",
  "reference": "urn:li:organization:{orgId}",
  "type": "BUSINESS"
}
```

#### 更新广告账户

```bash
POST /linkedin/rest/adAccounts/{adAccountId}
Content-Type: application/json
X-RestLi-Method: PARTIAL_UPDATE

{
  "patch": {
    "$set": {
      "name": "Updated Account Name"
    }
  }
}
```

#### 列出广告组

广告组隶属于广告账户：

```bash
GET /linkedin/rest/adAccounts/{adAccountId}/adCampaignGroups
```

#### 创建广告组

```bash
POST /linkedin/rest/adAccounts/{adAccountId}/adCampaignGroups
Content-Type: application/json

{
  "name": "Q1 2026 Campaigns",
  "status": "DRAFT",
  "runSchedule": {
    "start": 1704067200000,
    "end": 1711929600000
  },
  "totalBudget": {
    "amount": "10000",
    "currencyCode": "USD"
  }
}
```

#### 获取广告组信息

```bash
GET /linkedin/rest/adAccounts/{adAccountId}/adCampaignGroups/{campaignGroupId}
```

#### 更新广告组

```bash
POST /linkedin/rest/adAccounts/{adAccountId}/adCampaignGroups/{campaignGroupId}
Content-Type: application/json
X-RestLi-Method: PARTIAL_UPDATE

{
  "patch": {
    "$set": {
      "status": "ACTIVE"
    }
  }
}
```

#### 删除广告组

```bash
DELETE /linkedin/rest/adAccounts/{adAccountId}/adCampaignGroups/{campaignGroupId}
```

#### 列出广告活动

广告活动也隶属于广告账户：

```bash
GET /linkedin/rest/adAccounts/{adAccountId}/adCampaigns
```

#### 创建广告活动

```bash
POST /linkedin/rest/adAccounts/{adAccountId}/adCampaigns
Content-Type: application/json

{
  "campaignGroup": "urn:li:sponsoredCampaignGroup:123456",
  "name": "Brand Awareness Campaign",
  "status": "DRAFT",
  "type": "SPONSORED_UPDATES",
  "objectiveType": "BRAND_AWARENESS",
  "dailyBudget": {
    "amount": "100",
    "currencyCode": "USD"
  },
  "costType": "CPM",
  "unitCost": {
    "amount": "5",
    "currencyCode": "USD"
  },
  "locale": {
    "country": "US",
    "language": "en"
  }
}
```

#### 获取广告活动信息

```bash
GET /linkedin/rest/adAccounts/{adAccountId}/adCampaigns/{campaignId}
```

#### 更新广告活动

```bash
POST /linkedin/rest/adAccounts/{adAccountId}/adCampaigns/{campaignId}
Content-Type: application/json
X-RestLi-Method: PARTIAL_UPDATE

{
  "patch": {
    "$set": {
      "status": "ACTIVE"
    }
  }
}
```

#### 删除广告活动

```bash
DELETE /linkedin/rest/adAccounts/{adAccountId}/adCampaigns/{campaignId}
```

### 广告活动状态

| 状态 | 描述 |
|--------|-------------|
| `DRAFT` | 广告活动处于草稿状态 |
| `ACTIVE` | 广告活动正在运行 |
| `PAUSED` | 广告活动已暂停 |
| `ARCHIVED` | 广告活动已归档 |
| `COMPLETED` | 广告活动已结束 |
| `CANCELED` | 广告活动已被取消 |

### 广告活动目标类型

| 目标 | 描述 |
|-----------|-------------|
| `BRAND_AWARENESS` | 提高品牌知名度 |
| `WEBSITE_VISITS` | 促进网站流量 |
| `ENGAGEMENT` | 增加帖子互动 |
| `VIDEO_VIEWS` | 最大化视频观看量 |
| `LEAD_GENERATION` | 通过表单收集潜在客户 |
| `WEBSITE_CONVERSIONS` | 促进网站转化 |
| `JOB_APPLICANTS` | 吸引求职申请 |

### 组织

#### 列出组织访问控制列表

获取当前用户有权访问的组织：

```bash
GET /linkedin/rest/organizationAcls?q=roleAssignee
LinkedIn-Version: 202506
```

**响应：**
```json
{
  "paging": {
    "start": 0,
    "count": 10,
    "total": 2
  },
  "elements": [
    {
      "role": "ADMINISTRATOR",
      "organization": "urn:li:organization:12345",
      "state": "APPROVED"
    }
  ]
}
```

#### 获取组织信息

```bash
GET /linkedin/rest/organizations/{organizationId}
LinkedIn-Version: 202506
```

#### 通过别名查找组织

```bash
GET /linkedin/rest/organizations?q=vanityName&vanityName={vanityName}
```

**示例：**
```bash
GET /linkedin/rest/organizations?q=vanityName&vanityName=microsoft
```

**响应：**
```json
{
  "elements": [
    {
      "vanityName": "microsoft",
      "localizedName": "Microsoft",
      "website": {
        "localized": {"en_US": "https://news.microsoft.com/"}
      }
    }
  ]
}
```

#### 获取组织分享统计信息

```bash
GET /linkedin/rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity={orgUrn}
```

**示例：**
```bash
GET /linkedin/rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn:li:organization:12345
```

#### 获取组织帖子

```bash
GET /linkedin/rest/posts?q=author&author={orgUrn}
```

**示例：**
```bash
GET /linkedin/rest/posts?q=author&author=urn:li:organization:12345
```

### 媒体上传（REST API）

REST API 提供现代媒体上传接口。所有请求都需要 `LinkedIn-Version: 202506` 的头部信息。

#### 初始化图片上传

```bash
POST /linkedin/rest/images?action=initializeUpload
Content-Type: application/json
LinkedIn-Version: 202506

{
  "initializeUploadRequest": {
    "owner": "urn:li:person:{personId}"
  }
}
```

**响应：**
```json
{
  "value": {
    "uploadUrlExpiresAt": 1770541529250,
    "uploadUrl": "https://www.linkedin.com/dms-uploads/...",
    "image": "urn:li:image:D4D10AQH4GJAjaFCkHQ"
  }
}
```

使用 `uploadUrl` 上传图片二进制文件，然后在帖子中使用 `image` 的 URI。

#### 初始化视频上传

```bash
POST /linkedin/rest/videos?action=initializeUpload
Content-Type: application/json
LinkedIn-Version: 202506

{
  "initializeUploadRequest": {
    "owner": "urn:li:person:{personId}",
    "fileSizeBytes": 10000000,
    "uploadCaptions": false,
    "uploadThumbnail": false
  }
}
```

**响应：**
```json
{
  "value": {
    "uploadUrlsExpireAt": 1770541530110,
    "video": "urn:li:video:D4D10AQE_p-P_odQhXQ",
    "uploadInstructions": [
      {"uploadUrl": "https://www.linkedin.com/dms-uploads/..."}
    ]
  }
}
```

#### 初始化文档上传

```bash
POST /linkedin/rest/documents?action=initializeUpload
Content-Type: application/json
LinkedIn-Version: 202506

{
  "initializeUploadRequest": {
    "owner": "urn:li:person:{personId}"
  }
}
```

**响应：**
```json
{
  "value": {
    "uploadUrlExpiresAt": 1770541530896,
    "uploadUrl": "https://www.linkedin.com/dms-uploads/...",
    "document": "urn:li:document:D4D10AQHr-e30QZCAjQ"
  }
}
```

### 广告定位

#### 获取可用的定位选项

```bash
GET /linkedin/rest/adTargetingFacets
```

返回广告活动可用的所有定位选项（共 31 个选项，包括雇主、学历、技能、位置、行业等）。

**响应：**
```json
{
  "elements": [
    {
      "facetName": "skills",
      "adTargetingFacetUrn": "urn:li:adTargetingFacet:skills",
      "entityTypes": ["SKILL"],
      "availableEntityFinders": ["AD_TARGETING_FACET", "TYPEAHEAD"]
    },
    {
      "facetName": "industries",
      "adTargetingFacetUrn": "urn:li:adTargetingFacet:industries"
    }
  ]
}
```

可用的定位选项包括：
- `skills` - 成员技能
- `industries` - 行业类别
- `titles` - 职位名称
- `seniorities` - 职位级别
- `degrees` - 学历
- `schools` - 教育机构
- `employers` / `employersPast` - 当前/过去的雇主
- `locations` / `geoLocations` - 地理定位
- `companySize` - 公司规模范围
- `genders` - 性别定位
- `ageRanges` - 年龄范围定位

## 获取您的个人 ID

要创建帖子，您需要您的 LinkedIn 个人 ID。您可以通过 `/rest/me` 端点获取它：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/linkedin/rest/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('LinkedIn-Version', '202506')
result = json.load(urllib.request.urlopen(req))
print(f"Your person URN: urn:li:person:{result['id']}")
EOF
```

## 代码示例

### JavaScript - 创建文本帖子

```javascript
const personId = 'YOUR_PERSON_ID';

const response = await fetch(
  'https://gateway.maton.ai/linkedin/rest/posts',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json',
      'LinkedIn-Version': '202506'
    },
    body: JSON.stringify({
      author: `urn:li:person:${personId}`,
      lifecycleState: 'PUBLISHED',
      visibility: 'PUBLIC',
      commentary: 'Hello from the API!',
      distribution: {
        feedDistribution: 'MAIN_FEED'
      }
    })
  }
);
```

### Python - 创建文本帖子

```python
import os
import requests

person_id = 'YOUR_PERSON_ID'

response = requests.post(
    'https://gateway.maton.ai/linkedin/rest/posts',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': '202506'
    },
    json={
        'author': f'urn:li:person:{person_id}',
        'lifecycleState': 'PUBLISHED',
        'visibility': 'PUBLIC',
        'commentary': 'Hello from the API!',
        'distribution': {
            'feedDistribution': 'MAIN_FEED'
        }
    }
)
```

## 速率限制

| 限制类型 | 每日限制（UTC） |
|---------------|-------------------|
| Member | 150 次请求/天 |
| Application | 100,000 次请求/天 |

## 注意事项

- 个人 ID 在每个应用程序中是唯一的，不能在不同应用程序之间转移。
- `author` 字段必须使用 URI 格式：`urn:li:person:{personId}`。
- 所有帖子都需要 `lifecycleState: "PUBLISHED"`。
- 图片/视频上传是一个三步过程：初始化上传、上传二进制文件、创建帖子。
- 所有 REST API 调用都需要包含 `LinkedIn-Version: 202506` 头部信息。
- 个人资料图片 URL 可能会过期；如有需要请重新获取。
- 重要提示：使用 `curl` 命令时，如果 URL 包含括号，请使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 缺少 LinkedIn 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 权限不足（检查 OAuth 范围） |
| 404 | 资源未找到 |
| 422 | 请求体或 URI 格式无效 |
| 429 | 达到速率限制 |
| 4xx/5xx | 来自 LinkedIn API 的传递错误 |

### 错误响应格式

```json
{
  "status": 403,
  "serviceErrorCode": 100,
  "code": "ACCESS_DENIED",
  "message": "Not enough permissions to access resource"
}
```

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

1. 确保您的 URL 路径以 `linkedin` 开头。例如：
- 正确：`https://gateway.maton.ai/linkedin/rest/me`
- 错误：`https://gateway.maton.ai/rest/me`

## OAuth 范围

| 范围 | 描述 |
|-------|-------------|
| `openid` | OpenID Connect 认证 |
| `profile` | 读取基本个人资料 |
| `email` | 读取电子邮件地址 |
| `w_member_social` | 创建、修改和删除帖子 |

## 资源

- [LinkedIn API 概述](https://learn.microsoft.com/en-us/linkedin/)
- [在 LinkedIn 上分享指南](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin)
- [个人资料 API](https://learn.microsoft.com/en-us/linkedin/shared/integrations/people/profile-api)
- [使用 LinkedIn 登录](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2)
- [认证指南](https://learn.microsoft.com/en-us/linkedin/shared/authentication/)
- [营销 API](https://learn.microsoft.com/en-us/linkedin/marketing/)
- [广告账户](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-accounts)
- [广告活动管理](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns)
- [广告库 API](https://www.linkedin.com/ad-library/api/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)