---
name: hubspot
description: HubSpot CRM与CMS的API集成，支持联系人（Contacts）、公司（Companies）、交易（Deals）、负责人（Owners）以及内容管理（Content Management）的功能。
homepage: https://github.com/kwall1/hubspot-skill
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["curl","jq"],"env":["HUBSPOT_ACCESS_TOKEN"]},"primaryEnv":"HUBSPOT_ACCESS_TOKEN"}}
---
# HubSpot Skill

通过 REST API 与 HubSpot 客户关系管理（CRM）和内容管理系统（CMS）进行交互。

## 设置

设置您的 HubSpot 私有应用访问令牌：
```
HUBSPOT_ACCESS_TOKEN=pat-na2-xxxxx
```

## API 基址

所有端点的基址为：`https://api.hubapi.com`

授权头部：`Bearer $HUBSPOT_ACCESS_TOKEN`

---

## CRM 对象

### 联系人

**创建联系人：**
```bash
curl -s -X POST -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"email":"test@example.com","firstname":"Test","lastname":"User","phone":"555-1234","company":"Acme Inc","jobtitle":"Manager"}}' \
  "https://api.hubapi.com/crm/v3/objects/contacts" | jq
```

**列出联系人：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/objects/contacts?limit=10" | jq
```

**搜索联系人：**
```bash
curl -s -X POST -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"email","operator":"CONTAINS_TOKEN","value":"example.com"}]}],"limit":10}' \
  "https://api.hubapi.com/crm/v3/objects/contacts/search" | jq
```

**通过 ID 获取联系人：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/objects/contacts/{contactId}?properties=email,firstname,lastname,phone,company" | jq
```

**通过电子邮件获取联系人：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/objects/contacts/{email}?idProperty=email" | jq
```

### 公司

**列出公司：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/objects/companies?limit=10&properties=name,domain,industry" | jq
```

**搜索公司：**
```bash
curl -s -X POST -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"name","operator":"CONTAINS_TOKEN","value":"acme"}]}],"limit":10}' \
  "https://api.hubapi.com/crm/v3/objects/companies/search" | jq
```

**通过 ID 获取公司：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/objects/companies/{companyId}?properties=name,domain,industry,numberofemployees" | jq
```

### 交易

**创建交易：**
```bash
curl -s -X POST -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"dealname":"New Deal","amount":"10000","closedate":"2026-06-01","description":"Deal notes here"}}' \
  "https://api.hubapi.com/crm/v3/objects/deals" | jq
```

**列出交易：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/objects/deals?limit=10&properties=dealname,amount,dealstage,closedate" | jq
```

**搜索交易：**
```bash
curl -s -X POST -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"dealstage","operator":"EQ","value":"closedwon"}]}],"limit":10}' \
  "https://api.hubapi.com/crm/v3/objects/deals/search" | jq
```

**通过 ID 获取交易：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/objects/deals/{dealId}?properties=dealname,amount,dealstage,closedate,pipeline" | jq
```

### 所有者

**列出所有者（用户）：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/owners" | jq
```

---

## 更新与分配所有者

**更新联系人属性：**
```bash
curl -s -X PATCH -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"phone":"555-9999","jobtitle":"Director"}}' \
  "https://api.hubapi.com/crm/v3/objects/contacts/{contactId}" | jq
```

**将所有者分配给联系人：**
```bash
curl -s -X PATCH -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"hubspot_owner_id":"{ownerId}"}}' \
  "https://api.hubapi.com/crm/v3/objects/contacts/{contactId}" | jq
```

**将所有者分配给交易：**
```bash
curl -s -X PATCH -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"hubspot_owner_id":"{ownerId}"}}' \
  "https://api.hubapi.com/crm/v3/objects/deals/{dealId}" | jq
```

---

## 关联关系

**获取公司的关联联系人：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v4/objects/companies/{companyId}/associations/contacts" | jq
```

**获取联系人的关联交易：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v4/objects/contacts/{contactId}/associations/deals" | jq
```

**创建关联关系（交易到联系人）：**
```bash
curl -s -X POST -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputs":[{"from":{"id":"{dealId}"},"to":{"id":"{contactId}"},"types":[{"associationCategory":"HUBSPOT_DEFINED","associationTypeId":3}]}]}' \
  "https://api.hubapi.com/crm/v4/associations/deals/contacts/batch/create" | jq
```

常见的关联类型 ID：
- 3：交易到联系人
- 5：交易到公司
- 1：联系人到公司

---

## 属性（数据结构）

**列出联系人属性：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/properties/contacts" | jq '.results[].name'
```

**列出公司属性：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/properties/companies" | jq '.results[].name'
```

**列出交易属性：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/properties/deals" | jq '.results[].name'
```

---

## CMS

### 页面

**列出网站页面：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/cms/v3/pages/site-pages?limit=10" | jq
```

**列出登录页面：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/cms/v3/pages/landing-pages?limit=10" | jq
```

### 域名

**列出域名：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/cms/v3/domains" | jq
```

---

## 文件

**列出文件：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/files/v3/files?limit=10" | jq
```

**搜索文件：**
```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/files/v3/files/search?name=logo" | jq
```

---

## 搜索操作符

在搜索端点中，可以使用以下操作符作为过滤条件：

| 操作符 | 描述 |
|----------|-------------|
| `EQ` | 等于 |
| `NEQ` | 不等于 |
| `LT` | 小于 |
| `LTE` | 小于或等于 |
| `GT` | 大于 |
| `GTE` | 大于或等于 |
| `CONTAINS_TOKEN` | 包含单词 |
| `NOT_CONTAINS_TOKEN` | 不包含单词 |
| `HAS_PROPERTY` | 具有该属性 |
| `NOTHAS_PROPERTY` | 不具有该属性 |

---

## PowerShell 示例

在 Windows/PowerShell 中，使用 `Invoke-RestMethod` 命令进行操作：

```powershell
$headers = @{ 
  "Authorization" = "Bearer $env:HUBSPOT_ACCESS_TOKEN"
  "Content-Type" = "application/json" 
}

# List contacts
Invoke-RestMethod -Uri "https://api.hubapi.com/crm/v3/objects/contacts?limit=10" -Headers $headers

# Search contacts
$body = @{
  filterGroups = @(@{
    filters = @(@{
      propertyName = "email"
      operator = "CONTAINS_TOKEN"
      value = "example.com"
    })
  })
  limit = 10
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method POST -Uri "https://api.hubapi.com/crm/v3/objects/contacts/search" -Headers $headers -Body $body
```

---

## 注意事项

- 支持完整的 CRUD 操作（创建、读取、更新、删除），具体取决于权限范围。
- 私有应用的请求速率限制为每 10 秒 100 次请求。
- 分页：使用 `paging.next.after` 参数来获取下一页数据。
- 门户 ID 存在于记录 URL 中，例如：`https://app-na2.hubspot.com/contacts/{portalId}/record/...`