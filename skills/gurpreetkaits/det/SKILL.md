---
name: det
description: >
  **DailyExpenseTracker API集成**  
  用于记录开支、查看余额以及管理交易。当用户提及“开支”、“消费”、“交易”、“钱包”或“DailyExpenseTracker”（DET）时，请使用该API。
---
# DailyExpenseTracker (DET)

## API

**基础URL:** `https://dailyexpensetracker.in/api`
**Token:** 请在 `openclaw.json` 文件的 `skills.entries.det.apiToken` 中设置
**认证头:** `Authorization: Bearer <token>`

## 钱包

可以通过 `/api/wallets` 端点动态获取钱包信息。首次获取后，会将钱包ID缓存到本地。

## 添加支出记录

```bash
curl -X POST "https://dailyexpensetracker.in/api/transactions" \
  -H "Authorization: Bearer $DET_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "wallet_id": 1,
    "category_id": 5,
    "amount": 100,
    "type": "expense",
    "transaction_date": "2026-02-21",
    "description": "Groceries"
  }'
```

**必填字段:** wallet_id, amount, type, transaction_date
**类型:** expense (支出), income (收入), transfer (转账)

## 获取交易记录

```bash
curl "https://dailyexpensetracker.in/api/transactions?per_page=10" \
  -H "Authorization: Bearer $DET_TOKEN"
```

## 获取钱包余额

```bash
curl "https://dailyexpensetracker.in/api/wallets" \
  -H "Authorization: Bearer $DET_TOKEN"
```

## 获取支出类别

```bash
curl "https://dailyexpensetracker.in/api/categories" \
  -H "Authorization: Bearer $DET_TOKEN"
```

## 规则

- **务必使用API** - 绝不要直接写入数据库
- **字段名称为 `transaction_date`**，而非 `date`
- **默认钱包**: HDFC BANK (1)，除非另有指定
- **记录大额支出**（>₹5000）前请先确认