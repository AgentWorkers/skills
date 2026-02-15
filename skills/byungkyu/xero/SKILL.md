---
name: xero
description: |
  Xero API integration with managed OAuth. Manage contacts, invoices, payments, accounts, and run financial reports. Use this skill when users want to interact with Xero accounting data. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Xero

使用托管的 OAuth 认证方式访问 Xero API，可以管理联系人、发票、支付记录、银行交易，并生成财务报告。

## 快速入门

```bash
# List contacts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/xero/api.xro/2.0/Contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/xero/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Xero API 端点路径。该网关会将请求代理到 `api.xero.com`，并自动添加您的 OAuth 令牌和 `Xero-Tenant-Id` 标头。

## 认证

所有请求都需要在 `Authorization` 标头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Xero OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=xero&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'xero'}).encode()
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
    "app": "xero",
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

如果您有多个 Xero 连接，请使用 `Maton-Connection` 标头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/xero/api.xro/2.0/Contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 联系人

#### 列出联系人

```bash
GET /xero/api.xro/2.0/Contacts
```

#### 获取联系人信息

```bash
GET /xero/api.xro/2.0/Contacts/{contactId}
```

#### 创建联系人

```bash
POST /xero/api.xro/2.0/Contacts
Content-Type: application/json

{
  "Contacts": [{
    "Name": "John Doe",
    "EmailAddress": "john@example.com",
    "Phones": [{"PhoneType": "DEFAULT", "PhoneNumber": "555-1234"}]
  }]
}
```

### 发票

#### 列出发票

```bash
GET /xero/api.xro/2.0/Invoices
```

#### 创建发票

```bash
POST /xero/api.xro/2.0/Invoices
Content-Type: application/json

{
  "Invoices": [{
    "Type": "ACCREC",
    "Contact": {"ContactID": "xxx"},
    "LineItems": [{
      "Description": "Service",
      "Quantity": 1,
      "UnitAmount": 100.00,
      "AccountCode": "200"
    }]
  }]
}
```

### 账户

#### 列出账户信息

```bash
GET /xero/api.xro/2.0/Accounts
```

### 支付记录

#### 列出支付记录

```bash
GET /xero/api.xro/2.0/Payments
```

### 银行交易

#### 列出银行交易记录

```bash
GET /xero/api.xro/2.0/BankTransactions
```

### 报告

#### 利润与损失报告

```bash
GET /xero/api.xro/2.0/Reports/ProfitAndLoss?fromDate=2024-01-01&toDate=2024-12-31
```

#### 资产负债表

```bash
GET /xero/api.xro/2.0/Reports/BalanceSheet?date=2024-12-31
```

#### 试算平衡表

```bash
GET /xero/api.xro/2.0/Reports/TrialBalance?date=2024-12-31
```

### 组织信息

```bash
GET /xero/api.xro/2.0/Organisation
```

## 发票类型

- `ACCREC` - 应收账款（销售发票）
- `ACCPAY` - 应付账款（账单）

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/xero/api.xro/2.0/Contacts',
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
    'https://gateway.maton.ai/xero/api.xro/2.0/Contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
```

## 注意事项

- `Xero-Tenant-Id` 标头会自动添加到请求中。
- 日期格式为 `YYYY-MM-DD`。
- 可以使用数组在单个请求中创建多个记录。
- 使用 `where` 查询参数进行过滤。
- 重要提示：当 URL 包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 命令以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能会导致 “无效 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Xero 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求限制（每秒 10 次） |
| 4xx/5xx | 来自 Xero API 的传递错误 |

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

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `xero` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/xero/api.xro/2.0/Contacts`
- 错误的路径：`https://gateway.maton.ai/api.xro/2.0/Contacts`

## 资源

- [Xero API 概述](https://developer.xero.com/documentation/api/accounting/overview)
- [联系人](https://developer.xero.com/documentation/api/accounting/contacts)
- [发票](https://developer.xero.com/documentation/api/accounting/invoices)
- [账户](https://developer.xero.com/documentation/api/accounting/accounts)
- [支付记录](https://developer.xero.com/documentation/api/accounting/payments)
- [报告](https://developer.xero.com/documentation/api/accounting/reports)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)