---
name: unbounce
description: >
  **Unbounce API集成与托管式OAuth**  
  通过Unbounce API，您可以构建和管理着陆页（landing pages），追踪潜在客户（leads），并分析转化数据（conversion data）。  
  当用户需要使用Unbounce来管理着陆页或追踪潜在客户时，可运用此技能。  
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
# Unbounce

通过管理的 OAuth 访问 Unbounce 的着陆页和潜在客户信息。

## 快速入门

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/unbounce/accounts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/unbounce/{native-api-path}
```

代理服务器会将请求转发到 `api.unbounce.com`，并自动插入您的凭据。

## 认证

所有请求都需要 Maton API 密钥：

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

在 `https://ctrl.maton.ai` 管理您的 Unbounce OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=unbounce&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'unbounce'}).encode()
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
    "connection_id": "9c5cc43b-6f09-4789-ad4d-8162e39a24c1",
    "status": "PENDING",
    "creation_time": "2026-03-04T10:54:06.615371Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "unbounce",
    "method": "OAUTH2",
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

---

## API 参考

### 账户

#### 列出账户

```bash
GET /unbounce/accounts
```

查询参数：
- `sort_order` - `asc` 或 `desc`（默认：按创建日期降序排列）

**响应：**
```json
{
  "metadata": {
    "count": 1,
    "location": "https://api.unbounce.com/accounts"
  },
  "accounts": [
    {
      "id": 4967935,
      "name": "My Account",
      "createdAt": "2026-03-04T10:54:34Z",
      "state": "active",
      "options": {}
    }
  ]
}
```

#### 获取账户信息

```bash
GET /unbounce/accounts/{account_id}
```

**响应：**
```json
{
  "id": 4967935,
  "name": "My Account",
  "createdAt": "2026-03-04T10:54:34Z",
  "state": "active",
  "options": {}
}
```

#### 列出账户页面

```bash
GET /unbounce/accounts/{account_id}/pages
```

#### 列出账户子账户

```bash
GET /unbounce/accounts/{account_id}/sub_accounts
```

---

### 子账户

#### 获取子账户信息

```bash
GET /unbounce/sub_accounts/{sub_account_id}
```

**响应：**
```json
{
  "id": 5699747,
  "accountId": 4967935,
  "name": "ChrisKim",
  "createdAt": "2026-03-04T10:54:35Z",
  "website": null,
  "uuid": "cf72cbb6-17fd-44d1-bbe4-d25dcad6354a",
  "domainsCount": 0
}
```

#### 列出子账户页面

```bash
GET /unbounce/sub_accounts/{sub_account_id}/pages
```

#### 列出子账户域名

```bash
GET /unbounce/sub_accounts/{sub_account_id}/domains
```

#### 列出子账户页面组

```bash
GET /unbounce/sub_accounts/{sub_account_id}/page_groups
```

---

### 页面

#### 列出所有页面

```bash
GET /unbounce/pages
```

查询参数：
- `role` - 按用户角色过滤：`viewer` 或 `author`
- `with_stats` - 如果设置为 `true`，则包含 A/B 测试统计数据
- `limit` - 每页显示的结果数量（默认：50，最大：1000）
- `offset` - 跳过前 N 个结果
- `sort_order` - `asc` 或 `desc`
- `count` - 如果设置为 `true`，则在元数据中仅返回数量
- `from` - 开始日期（RFC 5322 格式）
- `to` - 结束日期（RFC 5322 格式）

**响应：**
```json
{
  "metadata": {
    "count": 1,
    "location": "https://api.unbounce.com/pages"
  },
  "pages": [
    {
      "id": "7cacd6d4-015a-4690-9537-68aac06bd98e",
      "subAccountId": 5699747,
      "name": "Training Template",
      "url": "http://unbouncepages.com/training-template/",
      "state": "unpublished",
      "domain": "unbouncepages.com",
      "createdAt": "2026-03-04T10:56:54Z",
      "lastPublishedAt": null,
      "variantsCount": 0,
      "integrationsCount": 0,
      "integrationsErrorsCount": 0
    }
  ]
}
```

#### 获取页面信息

```bash
GET /unbounce/pages/{page_id}
```

包含测试统计数据（A/B 测试数据）：

**响应：**
```json
{
  "id": "7cacd6d4-015a-4690-9537-68aac06bd98e",
  "name": "Training Template",
  "url": "http://unbouncepages.com/training-template/",
  "state": "unpublished",
  "tests": {
    "current": {
      "champion": "a",
      "hasResults": "false",
      "conversionRate": "0",
      "conversions": "0",
      "visitors": "0",
      "visits": "0"
    }
  }
}
```

#### 列出页面表单字段

```bash
GET /unbounce/pages/{page_id}/form_fields
```

查询参数：
- `include_sub_pages` - 如果设置为 `true`，则包含子页面的表单字段
- `sort_order` - `asc` 或 `desc`
- `count` - 如果设置为 `true`，则仅返回数量

**响应：**
```json
{
  "metadata": {
    "count": 3
  },
  "formFields": [
    {
      "id": "name",
      "name": "Name",
      "type": "text",
      "validations": {
        "required": false
      }
    },
    {
      "id": "email",
      "name": "Email",
      "type": "text",
      "validations": {
        "required": false,
        "email": true
      }
    },
    {
      "id": "telephone",
      "name": "Telephone",
      "type": "text",
      "validations": {
        "required": false,
        "phone": true
      }
    }
  ]
}
```

---

### 潜在客户

#### 列出页面上的潜在客户

```bash
GET /unbounce/pages/{page_id}/leads
```

查询参数：
- `limit` - 每页显示的结果数量（默认：50，最大：1000）
- `offset` - 跳过前 N 个结果
- `sort_order` - `asc` 或 `desc`
- `from` - 开始日期（RFC 5322 格式）
- `to` - 结束日期（RFC 5322 格式）

**响应：**
```json
{
  "metadata": {
    "count": 0,
    "delete": {
      "href": "https://api.unbounce.com/pages/{page_id}/lead_deletion_request",
      "method": "POST"
    }
  },
  "leads": []
}
```

#### 获取潜在客户信息

```bash
GET /unbounce/pages/{page_id}/leads/{lead_id}
```

或直接通过以下方式获取：

```bash
GET /unbounce/leads/{lead_id}
```

**响应：**
```json
{
  "id": "f79d7b6e-b3e8-484c-9584-d21c7afba238",
  "created_at": "2026-03-04T11:52:50.705Z",
  "page_id": "7cacd6d4-015a-4690-9537-68aac06bd98e",
  "variant_id": "a",
  "submitter_ip": "127.0.0.1",
  "form_data": {
    "name": "Test User",
    "email": "test@example.com",
    "telephone": "1234567890"
  },
  "extra_data": {
    "cookies": {}
  }
}
```

#### 创建潜在客户

```bash
POST /unbounce/pages/{page_id}/leads
Content-Type: application/json
```

**请求体：**
```json
{
  "conversion": true,
  "visitor_id": "127.0.0.1234567890",
  "form_submission": {
    "variant_id": "a",
    "submitter_ip": "127.0.0.1",
    "form_data": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone_number": "1234567890"
    }
  }
}
```

**响应：**
```json
{
  "id": "f79d7b6e-b3e8-484c-9584-d21c7afba238",
  "created_at": "2026-03-04T11:52:50.705Z",
  "page_id": "7cacd6d4-015a-4690-9537-68aac06bd98e",
  "variant_id": "a",
  "submitter_ip": "127.0.0.1",
  "form_data": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "1234567890"
  }
}
```

通过 API 创建的潜在客户在其 `extra_data` 中会包含 `"created_by": "api"`。

---

### 域名

#### 获取域名信息

```bash
GET /unbounce/domains/{domain_id}
```

#### 列出域名页面

```bash
GET /unbounce/domains/{domain_id}/pages
```

---

### 页面组

#### 列出页面组页面

```bash
GET /unbounce/page_groups/{page_group_id}/pages
```

查询参数：
- `limit` - 每页显示的结果数量（默认：50，最大：1000）
- `offset` - 跳过前 N 个结果
- `sort_order` - `asc` 或 `desc`
- `from` / `to` - 日期范围过滤

---

### 用户

#### 获取当前用户信息

```bash
GET /unbounce/users/self
```

**响应：**
```json
{
  "id": 5031726,
  "email": "user@example.com",
  "firstName": "Chris",
  "lastName": "Kim",
  "metadata": {
    "related": {
      "subAccounts": ["https://api.unbounce.com/sub_accounts/5699747"],
      "accounts": ["https://api.unbounce.com/accounts/4967935"]
    }
  }
}
```

#### 通过 ID 获取用户信息

```bash
GET /unbounce/users/{user_id}
```

---

## 分页

Unbounce 使用基于偏移量的分页方式：

```bash
GET /unbounce/pages?limit=50&offset=0
```

**参数：**
- `limit` - 每页显示的结果数量（默认：50，最大：1000）
- `offset` - 要跳过的结果数量
- `sort_order` - 排序方向：`asc` 或 `desc`

**响应元数据包含：**
```json
{
  "metadata": {
    "count": 100
  }
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/unbounce/pages', {
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  }
});
const data = await response.json();
console.log(data);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/unbounce/pages',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'
    }
)
print(response.json())
```

## 注意事项

- 所有响应都包含用于导航的 HATEOAS 链接。
- 日期格式：RFC 5322（例如：`2026-03-04T10:54:34Z`）。
- 页面 ID 是 UUID，账户/子账户 ID 是整数。
- 页面状态：`published` 或 `unpublished`。
- 账户状态：`active` 或 `suspended`。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 200 | 成功 |
| 401 | 验证失败或凭据缺失 |
| 404 | 资源未找到 |
| 429 | 请求频率限制 |

## 资源

- [Unbounce API 文档](https://developer.unbounce.com/api_reference/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)