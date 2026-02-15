---
name: brevo
version: 1.0.0
description: **Brevo（前身为Sendinblue）电子邮件营销API**：用于管理联系人、邮件列表、发送交易邮件以及开展营销活动。适用于导入联系人、发送邮件、管理订阅信息或实现邮件自动化等功能。
---

# Brevo 邮件营销 API

通过 Brevo 的 REST API 管理联系人、发送邮件并实现自动化营销。

## 认证

```bash
BREVO_KEY=$(cat ~/.config/brevo/api_key)
```

所有请求都需要在请求头中添加以下字段：`api-key: $BREVO_KEY`

## 基本 URL

```
https://api.brevo.com/v3
```

## 常见接口

### 联系人

| 操作 | 方法 | 接口地址 |
|--------|--------|----------|
| 创建联系人 | POST | `/contacts` |
| 获取联系人信息 | GET | `/contacts/{email}` |
| 更新联系人信息 | PUT | `/contacts/{email}` |
| 删除联系人 | DELETE | `/contacts/{email}` |
| 列出联系人 | GET | `/contacts?limit=50&offset=0` |
| 查看是否被列入黑名单 | GET | `/contacts?emailBlacklisted=true` |

### 列表

| 操作 | 方法 | 接口地址 |
|--------|--------|----------|
| 获取所有列表 | GET | `/contacts/lists` |
| 创建列表 | POST | `/contacts/lists` |
| 获取列表中的联系人信息 | GET | `/contacts/lists/{listId}/contacts` |
| 将联系人添加到列表中 | POST | `/contacts/lists/{listId}/contacts/add` |
| 从列表中删除联系人 | POST | `/contacts/lists/{listId}/contacts/remove` |

### 邮件

| 操作 | 方法 | 接口地址 |
|--------|--------|----------|
| 发送交易性邮件 | POST | `/smtp/email` |
| 发送营销邮件 | POST | `/emailCampaigns` |
| 获取邮件模板 | GET | `/smtp/templates` |

## 示例

### 创建/更新联系人信息

```bash
curl -X POST "https://api.brevo.com/v3/contacts" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "listIds": [10],
    "updateEnabled": true,
    "attributes": {
      "NOMBRE": "John",
      "APELLIDOS": "Doe"
    }
  }'
```

### 获取联系人信息

```bash
curl "https://api.brevo.com/v3/contacts/user@example.com" \
  -H "api-key: $BREVO_KEY"
```

### 更新联系人属性

```bash
curl -X PUT "https://api.brevo.com/v3/contacts/user@example.com" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "listIds": [10, 15],
    "attributes": {
      "CUSTOM_FIELD": "value"
    }
  }'
```

### 发送交易性邮件

```bash
curl -X POST "https://api.brevo.com/v3/smtp/email" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sender": {"name": "My App", "email": "noreply@example.com"},
    "to": [{"email": "user@example.com", "name": "John"}],
    "subject": "Welcome!",
    "htmlContent": "<p>Hello {{params.name}}</p>",
    "params": {"name": "John"}
  }'
```

### 使用模板发送邮件

```bash
curl -X POST "https://api.brevo.com/v3/smtp/email" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": [{"email": "user@example.com"}],
    "templateId": 34,
    "params": {
      "NOMBRE": "John",
      "FECHA": "2026-02-01"
    }
  }'
```

### 列出所有联系人列表

```bash
curl "https://api.brevo.com/v3/contacts/lists?limit=50" \
  -H "api-key: $BREVO_KEY"
```

### 批量将联系人添加到列表中

```bash
curl -X POST "https://api.brevo.com/v3/contacts/lists/10/contacts/add" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "emails": ["user1@example.com", "user2@example.com"]
  }'
```

## 安全导入规则

在导入联系人时，**务必尊重用户的退订意愿**：

```python
import requests

BREVO_KEY = "your-api-key"
HEADERS = {'api-key': BREVO_KEY, 'Content-Type': 'application/json'}
BASE = 'https://api.brevo.com/v3'

def get_blacklisted():
    """Get all unsubscribed/blacklisted emails"""
    blacklisted = set()
    offset = 0
    while True:
        r = requests.get(
            f'{BASE}/contacts?limit=100&offset={offset}&emailBlacklisted=true',
            headers=HEADERS
        )
        contacts = r.json().get('contacts', [])
        if not contacts:
            break
        for c in contacts:
            blacklisted.add(c['email'].lower())
        offset += 100
    return blacklisted

def safe_import(emails, list_id):
    """Import contacts respecting unsubscribes"""
    blacklisted = get_blacklisted()
    
    for email in emails:
        if email.lower() in blacklisted:
            print(f"Skipped (unsubscribed): {email}")
            continue
        
        r = requests.post(f'{BASE}/contacts', headers=HEADERS, json={
            'email': email,
            'listIds': [list_id],
            'updateEnabled': True
        })
        
        if r.status_code in [200, 201, 204]:
            print(f"Imported: {email}")
        else:
            print(f"Error: {email} - {r.text[:50]}")
```

## 联系人属性

Brevo 使用自定义属性来存储联系人数据：

```json
{
  "attributes": {
    "NOMBRE": "John",
    "APELLIDOS": "Doe",
    "FECHA_ALTA": "2026-01-15",
    "PLAN": "premium",
    "CUSTOM_FIELD": "any value"
  }
}
```

在 Brevo 的控制台中创建属性：联系人 → 设置 → 联系人属性。

## 响应码

| 代码 | 含义 |
|------|---------|
| 200 | 成功（GET 请求） |
| 201 | 创建成功（POST 请求） |
| 204 | 操作成功，但没有返回内容（PUT/DELETE 请求） |
| 400 | 请求错误（请检查请求数据） |
| 401 | API 密钥无效 |
| 404 | 未找到联系人或资源 |

## 最佳实践

1. **在导入联系人之前，务必检查其是否被列入黑名单**。
2. **使用 `updateEnabled: true` 参数来更新现有联系人信息，而不是直接删除他们**。
3. **使用模板来确保交易性邮件的格式统一**。
4. **在批量添加联系人到列表时，使用批量操作**。
5. **将列表 ID 存储在配置文件中，而不是硬编码**。
6. **记录导入操作，以便进行审计追踪**。

## 自动化规则

Brevo 的自动化规则会在以下情况下触发：
- 联系人被添加到列表中。
- 联系人属性被更新。
- 邮件被打开或点击。
- 通过 API 触发自定义事件。

**手动触发自动化规则**：
```bash
curl -X POST "https://api.brevo.com/v3/contacts/import" \
  -H "api-key: $BREVO_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "listIds": [10],
    "emailBlacklist": false,
    "updateExistingContacts": true,
    "emptyContactsAttributes": false,
    "jsonBody": [
      {"email": "user@example.com", "attributes": {"NOMBRE": "John"}}
    ]
  }'
```

## 有用的查询

```bash
# Count contacts in list
curl "https://api.brevo.com/v3/contacts/lists/10" -H "api-key: $BREVO_KEY" | jq '.totalSubscribers'

# Get recent contacts
curl "https://api.brevo.com/v3/contacts?limit=10&sort=desc" -H "api-key: $BREVO_KEY"

# Check if email exists
curl "https://api.brevo.com/v3/contacts/user@example.com" -H "api-key: $BREVO_KEY"

# Get account info
curl "https://api.brevo.com/v3/account" -H "api-key: $BREVO_KEY"
```