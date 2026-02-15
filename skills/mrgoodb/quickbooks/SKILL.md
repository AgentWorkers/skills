---
name: quickbooks
description: 通过 Intuit API 管理 QuickBooks Online 财务系统中的发票、客户、付款和报表。
metadata: {"clawdbot":{"emoji":"💰","requires":{"env":["QUICKBOOKS_ACCESS_TOKEN","QUICKBOOKS_REALM_ID"]}}}
---

# QuickBooks Online

适用于小型企业的会计管理工具。

## 环境配置

```bash
export QUICKBOOKS_ACCESS_TOKEN="xxxxxxxxxx"
export QUICKBOOKS_REALM_ID="123456789"  # Company ID
export QB_BASE="https://quickbooks.api.intuit.com/v3/company"
```

## 客户列表

```bash
curl "$QB_BASE/$QUICKBOOKS_REALM_ID/query?query=select * from Customer" \
  -H "Authorization: Bearer $QUICKBOOKS_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

## 创建发票

```bash
curl -X POST "$QB_BASE/$QUICKBOOKS_REALM_ID/invoice" \
  -H "Authorization: Bearer $QUICKBOOKS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "CustomerRef": {"value": "1"},
    "Line": [{
      "Amount": 100.00,
      "DetailType": "SalesItemLineDetail",
      "SalesItemLineDetail": {"ItemRef": {"value": "1"}}
    }]
  }'
```

## 查看发票列表

```bash
curl "$QB_BASE/$QUICKBOOKS_REALM_ID/query?query=select * from Invoice" \
  -H "Authorization: Bearer $QUICKBOOKS_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

## 获取公司信息

```bash
curl "$QB_BASE/$QUICKBOOKS_REALM_ID/companyinfo/$QUICKBOOKS_REALM_ID" \
  -H "Authorization: Bearer $QUICKBOOKS_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

## 创建付款记录

```bash
curl -X POST "$QB_BASE/$QUICKBOOKS_REALM_ID/payment" \
  -H "Authorization: Bearer $QUICKBOOKS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "CustomerRef": {"value": "1"},
    "TotalAmt": 100.00,
    "Line": [{"Amount": 100.00, "LinkedTxn": [{"TxnId": "123", "TxnType": "Invoice"}]}]
  }'
```

## 链接：
- 仪表板：https://quickbooks.intuit.com
- 文档：https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account