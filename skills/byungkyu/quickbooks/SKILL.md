---
name: quickbooks
description: |
  QuickBooks API integration with managed OAuth. Manage customers, invoices, payments, bills, and run financial reports. Use this skill when users want to interact with QuickBooks accounting data. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# QuickBooks

您可以使用受管理的OAuth身份验证来访问QuickBooks Online API，从而管理客户、供应商、发票、支付信息，并生成财务报告。

## 快速入门

```bash
# Query customers
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/quickbooks/v3/company/:realmId/query?query=SELECT%20*%20FROM%20Customer%20MAXRESULTS%20100')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/quickbooks/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的QuickBooks API端点路径。该网关会将请求代理到 `quickbooks.api.intuit.com`。`:realmId` 占位符会自动替换为您从连接配置中获取的公司ID。

## 身份验证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的QuickBooks OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=quickbooks&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'quickbooks'}).encode()
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
    "app": "quickbooks",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth身份验证。

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

如果您有多个QuickBooks连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/quickbooks/v3/company/:realmId/companyinfo/:realmId')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 公司信息

```bash
GET /quickbooks/v3/company/:realmId/companyinfo/:realmId
```

### 客户

#### 查询客户

```bash
GET /quickbooks/v3/company/:realmId/query?query=SELECT%20*%20FROM%20Customer%20MAXRESULTS%20100
```

#### 获取客户信息

```bash
GET /quickbooks/v3/company/:realmId/customer/{customerId}
```

#### 创建客户

```bash
POST /quickbooks/v3/company/:realmId/customer
Content-Type: application/json

{
  "DisplayName": "John Doe",
  "PrimaryEmailAddr": {"Address": "john@example.com"},
  "PrimaryPhone": {"FreeFormNumber": "555-1234"}
}
```

#### 更新客户信息

需要使用之前GET请求返回的 `Id` 和 `SyncToken`：

```bash
POST /quickbooks/v3/company/:realmId/customer
Content-Type: application/json

{
  "Id": "123",
  "SyncToken": "0",
  "DisplayName": "John Doe Updated"
}
```

### 发票

#### 查询发票

```bash
GET /quickbooks/v3/company/:realmId/query?query=SELECT%20*%20FROM%20Invoice%20MAXRESULTS%20100
```

#### 创建发票

```bash
POST /quickbooks/v3/company/:realmId/invoice
Content-Type: application/json

{
  "CustomerRef": {"value": "123"},
  "Line": [
    {
      "Amount": 100.00,
      "DetailType": "SalesItemLineDetail",
      "SalesItemLineDetail": {
        "ItemRef": {"value": "1"},
        "Qty": 1
      }
    }
  ]
}
```

#### 删除发票

```bash
POST /quickbooks/v3/company/:realmId/invoice?operation=delete
Content-Type: application/json

{
  "Id": "123",
  "SyncToken": "0"
}
```

### 支付

#### 创建支付记录

```bash
POST /quickbooks/v3/company/:realmId/payment
Content-Type: application/json

{
  "CustomerRef": {"value": "123"},
  "TotalAmt": 100.00,
  "Line": [
    {
      "Amount": 100.00,
      "LinkedTxn": [{"TxnId": "456", "TxnType": "Invoice"}]
    }
  ]
}
```

### 报告

#### 利润与损失报告

```bash
GET /quickbooks/v3/company/:realmId/reports/ProfitAndLoss?start_date=2024-01-01&end_date=2024-12-31
```

#### 资产负债表

```bash
GET /quickbooks/v3/company/:realmId/reports/BalanceSheet?date=2024-12-31
```

### 批量操作

```bash
POST /quickbooks/v3/company/:realmId/batch
Content-Type: application/json

{
  "BatchItemRequest": [
    {"bId": "1", "Query": "SELECT * FROM Customer MAXRESULTS 2"},
    {"bId": "2", "Query": "SELECT * FROM Vendor MAXRESULTS 2"}
  ]
}
```

## 查询语言

QuickBooks支持类似SQL的查询语言：

```sql
SELECT * FROM Customer WHERE DisplayName LIKE 'John%' MAXRESULTS 100
```

运算符：`=`, `LIKE`, `<`, `>`, `<=`, `>=`, `IN`

## SyncToken

所有更新操作都需要当前的 `SyncToken`：
1. 通过GET请求获取当前的 `SyncToken`。
2. 在POST请求的请求体中包含 `Id` 和 `SyncToken`。
3. 如果 `SyncToken` 不匹配，更新操作将失败。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/quickbooks/v3/company/:realmId/query?query=SELECT%20*%20FROM%20Customer',
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
    'https://gateway.maton.ai/quickbooks/v3/company/:realmId/query',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'query': 'SELECT * FROM Customer MAXRESULTS 10'}
)
```

## 注意事项

- `:realmId` 会自动由系统替换为正确的值。
- 所有查询都需要进行URL编码。
- 使用 `MAXRESULTS` 参数来限制查询结果的数量。
- 日期格式为 `YYYY-MM-DD`。
- 通过将 `Active` 属性设置为 `false` 来实现软删除（即不立即删除数据）。
- **重要提示：** 当URL中包含方括号（如 `fields[]`, `sort[]`, `records[]`）时，使用 `curl -g` 命令可以避免glob解析问题。
- **重要提示：** 在将curl输出传递给 `jq` 或其他命令时，某些shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确解析，这可能导致“无效API密钥”的错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立QuickBooks连接 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（10次/秒） |
| 4xx/5xx | 来自QuickBooks API的传递错误 |

### 故障排除：API密钥问题

1. 确保已设置 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出所有连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的URL路径以 `quickbooks` 开头。例如：
   - 正确的路径：`https://gateway.maton.ai/quickbooks/v3/company/:realmId/query`
   - 错误的路径：`https://gateway.maton.ai/v3/company/:realmId/query`

## 资源

- [QuickBooks API概述](https://developer.intuit.com/app/developer/qbo/docs/get-started)
- [客户信息](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/customer)
- [发票信息](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/invoice)
- [支付信息](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/payment)
- [报告信息](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/profitandloss)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)