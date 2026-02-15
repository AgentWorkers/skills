---
name: xero
description: 通过 Xero API 管理 Xero 财务数据——包括发票、联系人、银行交易和报表。
metadata: {"clawdbot":{"emoji":"💵","requires":{"env":["XERO_ACCESS_TOKEN","XERO_TENANT_ID"]}}}
---

# Xero

云会计平台。

## 环境配置

```bash
export XERO_ACCESS_TOKEN="xxxxxxxxxx"
export XERO_TENANT_ID="xxxxxxxxxx"
```

## 列出联系人

```bash
curl "https://api.xero.com/api.xro/2.0/Contacts" \
  -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID" \
  -H "Accept: application/json"
```

## 创建发票

```bash
curl -X POST "https://api.xero.com/api.xro/2.0/Invoices" \
  -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "Invoices": [{
      "Type": "ACCREC",
      "Contact": {"ContactID": "xxxxx"},
      "LineItems": [{"Description": "Consulting", "Quantity": 1, "UnitAmount": 500}],
      "Date": "2024-01-30",
      "DueDate": "2024-02-28"
    }]
  }'
```

## 查看发票列表

```bash
curl "https://api.xero.com/api.xro/2.0/Invoices" \
  -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID" \
  -H "Accept: application/json"
```

## 获取银行交易记录

```bash
curl "https://api.xero.com/api.xro/2.0/BankTransactions" \
  -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID"
```

## 获取损益报告

```bash
curl "https://api.xero.com/api.xro/2.0/Reports/ProfitAndLoss?fromDate=2024-01-01&toDate=2024-12-31" \
  -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID"
```

## 链接：
- 仪表板：https://go.xero.com
- 文档：https://developer.xero.com/documentation/api/accounting/overview