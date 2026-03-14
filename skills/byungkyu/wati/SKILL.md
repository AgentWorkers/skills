---
name: wati
description: >
  **WATI（WhatsApp Team Inbox）API集成与托管认证**  
  该功能支持通过托管认证机制发送WhatsApp消息、管理联系人以及使用消息模板。  
  当用户需要通过WATI发送WhatsApp消息、管理联系人或使用消息模板时，可选用此功能。  
  对于其他第三方应用程序，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 💬
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# WATI

通过管理式认证访问WATI（WhatsApp团队收件箱）API。您可以发送WhatsApp消息、管理联系人以及使用消息模板。

## 快速入门

```bash
# Get contacts list
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/wati/api/v1/getContacts?pageSize=10&pageNumber=1')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/wati/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的WATI API端点路径。该网关会将请求代理到您的WATI实例，并自动插入您的API密钥。

## 认证

所有请求都需要在`Authorization`头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 注册或登录账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的WATI连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=wati&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'wati'}).encode()
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
    "app": "wati",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成授权。

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

如果您有多个WATI连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/wati/api/v1/getContacts?pageSize=10&pageNumber=1')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API参考

### 联系人

#### 获取联系人信息

```bash
GET /wati/api/v1/getContacts?pageSize=10&pageNumber=1
```

**查询参数：**
- `pageSize` - 每页显示的结果数量
- `pageNumber` - 页码（从1开始计数）
- `name`（可选）- 按联系人名称过滤
- `attribute`（可选）- 按属性过滤（格式：`[{"name": "name", "operator": "contain", "value": "test"}]`)
- `createdDate`（可选）- 按创建日期过滤（YYYY-MM-DD）

**属性操作符：** `contain`, `notContain`, `exist`, `notExist`, `==`, `!=`, `valid`, `invalid`

#### 添加联系人

```bash
POST /wati/api/v1/addContact/{whatsappNumber}
Content-Type: application/json

{
  "name": "John Doe",
  "customParams": [
    {
      "name": "member",
      "value": "VIP"
    }
  ]
}
```

#### 更新联系人属性

```bash
POST /wati/api/v1/updateContactAttributes/{whatsappNumber}
Content-Type: application/json

{
  "customParams": [
    {
      "name": "member",
      "value": "VIP"
    }
  ]
}
```

### 消息

#### 获取消息

```bash
GET /wati/api/v1/getMessages/{whatsappNumber}?pageSize=10&pageNumber=1
```

**查询参数：**
- `pageSize` - 每页显示的结果数量
- `pageNumber` - 页码（从1开始计数）

#### 发送会话消息

在活动会话（24小时窗口内）内发送文本消息：

```bash
POST /wati/api/v1/sendSessionMessage/{whatsappNumber}
Content-Type: application/x-www-form-urlencoded

messageText=Hello%20from%20WATI!
```

#### 发送会话文件

在活动会话内发送文件：

```bash
POST /wati/api/v1/sendSessionFile/{whatsappNumber}?caption=Check%20this%20out
Content-Type: multipart/form-data

file=@document.pdf
```

### 消息模板

#### 获取消息模板

```bash
GET /wati/api/v1/getMessageTemplates?pageSize=10&pageNumber=1
```

#### 发送模板消息

向单个联系人发送预先批准的消息模板：

```bash
POST /wati/api/v1/sendTemplateMessage?whatsappNumber={whatsappNumber}
Content-Type: application/json

{
  "template_name": "order_update",
  "broadcast_name": "order_update",
  "parameters": [
    {
      "name": "name",
      "value": "John"
    },
    {
      "name": "ordernumber",
      "value": "12345"
    }
  ]
}
```

#### 批量发送模板消息

向多个联系人发送模板消息：

```bash
POST /wati/api/v1/sendTemplateMessages
Content-Type: application/json

{
  "template_name": "order_update",
  "broadcast_name": "order_update",
  "receivers": [
    {
      "whatsappNumber": "14155551234",
      "customParams": [
        {
          "name": "name",
          "value": "John"
        },
        {
          "name": "ordernumber",
          "value": "12345"
        }
      ]
    },
    {
      "whatsappNumber": "14155555678",
      "customParams": [
        {
          "name": "name",
          "value": "Jane"
        },
        {
          "name": "ordernumber",
          "value": "67890"
        }
      ]
    }
  ]
}
```

#### 通过CSV发送模板消息

```bash
POST /wati/api/v1/sendTemplateMessageCSV?template_name=order_update&broadcast_name=order_update
Content-Type: multipart/form-data

whatsapp_numbers_csv=@contacts.csv
```

### 消息模板（v2 API）

v2 API提供带有消息跟踪ID的增强响应格式。

#### 发送模板消息（v2）

```bash
POST /wati/api/v2/sendTemplateMessage?whatsappNumber={whatsappNumber}
Content-Type: application/json

{
  "template_name": "order_update",
  "broadcast_name": "order_update",
  "parameters": [
    {
      "name": "name",
      "value": "John"
    }
  ]
}
```

**响应：**
```json
{
  "result": true,
  "error": null,
  "templateName": "order_update",
  "receivers": [
    {
      "localMessageId": "38aca0c0-f80a-409c-81ed-607fa5206529",
      "waId": "14155551234",
      "isValidWhatsAppNumber": true,
      "errors": []
    }
  ],
  "parameters": [
    {"name": "name", "value": "John"}
  ]
}
```

#### 批量发送模板消息（v2）

```bash
POST /wati/api/v2/sendTemplateMessages
Content-Type: application/json

{
  "template_name": "order_update",
  "broadcast_name": "order_update",
  "receivers": [
    {
      "whatsappNumber": "14155551234",
      "customParams": [
        {"name": "name", "value": "John"}
      ]
    },
    {
      "whatsappNumber": "14155555678",
      "customParams": [
        {"name": "name", "value": "Jane"}
      ]
    }
  ]
}
```

**响应：**
```json
{
  "result": true,
  "error": null,
  "templateName": "order_update",
  "receivers": [
    {
      "localMessageId": "c486f386-d86d-431d-aa3b-fb1b6c494e58",
      "waId": "14155551234",
      "isValidWhatsAppNumber": true,
      "errors": []
    },
    {
      "localMessageId": "d597f497-e97e-542e-bb4c-718gb6d5a069",
      "waId": "14155555678",
      "isValidWhatsAppNumber": true,
      "errors": []
    }
  ]
}
```

### 交互式消息

#### 发送交互式按钮消息

```bash
POST /wati/api/v1/sendInteractiveButtonsMessage?whatsappNumber={whatsappNumber}
Content-Type: application/json

{
  "header": {
    "type": "text",
    "text": "Order Status"
  },
  "body": "Your order #12345 is ready. What would you like to do?",
  "footer": "Reply within 24 hours",
  "buttons": [
    {
      "text": "Track Order"
    },
    {
      "text": "Contact Support"
    }
  ]
}
```

#### 发送交互式列表消息

```bash
POST /wati/api/v1/sendInteractiveListMessage?whatsappNumber={whatsappNumber}
Content-Type: application/json

{
  "header": "Choose an option",
  "body": "Please select from the menu below",
  "footer": "Powered by WATI",
  "buttonText": "View Options",
  "sections": [
    {
      "title": "Products",
      "rows": [
        {
          "title": "Product A",
          "description": "Best seller item"
        },
        {
          "title": "Product B",
          "description": "New arrival"
        }
      ]
    }
  ]
}
```

### 操作符

#### 分配操作符

```bash
POST /wati/api/v1/assignOperator?email=agent@example.com&whatsappNumber={whatsappNumber}
```

### 媒体

#### 获取媒体文件

```bash
GET /wati/api/v1/getMedia?fileName={fileName}
```

## 分页

WATI使用基于页的分页机制：

```bash
GET /wati/api/v1/getContacts?pageSize=50&pageNumber=1
```

**参数：**
- `pageSize` - 每页显示的结果数量
- `pageNumber` - 页码（从1开始计数）

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/wati/api/v1/getContacts?pageSize=10&pageNumber=1',
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

response = requests.get(
    'https://gateway.maton.ai/wati/api/v1/getContacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'pageSize': 10, 'pageNumber': 1}
)
data = response.json()
```

### 发送模板消息

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/wati/api/v1/sendTemplateMessage',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    params={'whatsappNumber': '14155551234'},
    json={
        'template_name': 'order_update',
        'broadcast_name': 'order_update',
        'parameters': [
            {'name': 'name', 'value': 'John'},
            {'name': 'ordernumber', 'value': '12345'}
        ]
    }
)
```

## 注意事项

- WhatsApp号码应包含国家代码，且不能包含+号或空格（例如：`14155551234`）
- 会话消息只能在客户最后一条消息后的24小时内发送
- 模板消息需要预先获得WhatsApp的批准
- 交互式消息（按钮/列表）有WhatsApp规定的字符限制
- 重要提示：当URL包含方括号时，使用 `curl -g` 可以防止全局解析
- 重要提示：当将curl输出传递给 `jq` 或其他命令时，在某些shell环境中 `$MATON_API_KEY` 环境变量可能无法正确解析

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到WATI连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 超过请求频率限制 |
| 4xx/5xx | 来自WATI API的传递错误 |

## 资源

- [WATI API文档](https://docs.wati.io/reference/introduction)
- [WATI帮助中心](https://docs.wati.io/)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)