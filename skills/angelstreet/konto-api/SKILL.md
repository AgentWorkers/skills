# Konto — 个人财务 API

用于查询 Konto（银行账户、投资、资产、贷款、交易）中的个人财务数据。

## 设置
```bash
# ~/.openclaw/secrets/konto.env
export KONTO_API_KEY="konto_xxxxxxxxxxxx"
export KONTO_URL="https://konto.angelstreet.io"
```

## 常见问题解答

### “我拥有多少比特币？”
```bash
source ~/.openclaw/secrets/konto.env
curl -s -H "Authorization: Bearer $KONTO_API_KEY" "$KONTO_URL/api/v1/investments" | jq '.investments[] | select(.code | test("BTC|bitcoin"; "i")) | {label, quantity, current_value}'
```

### “我的净资产是多少？”
```bash
curl -s -H "Authorization: Bearer $KONTO_API_KEY" "$KONTO_URL/api/v1/summary" | jq '{patrimoine_net, accounts: .accounts.total_balance, investments: .investments.total_value, assets: .assets.total_value, loans: .loans.total_remaining}'
```

### “我的贷款什么时候到期？”
```bash
curl -s -H "Authorization: Bearer $KONTO_API_KEY" "$KONTO_URL/api/v1/loans" | jq '.loans[] | {name, remaining_amount, end_date, monthly_payment}'
```

### “我有哪些订阅服务？”
```bash
curl -s -H "Authorization: Bearer $KONTO_API_KEY" "$KONTO_URL/api/v1/summary" | jq '{count: .subscriptions.count, monthly: .subscriptions.monthly}'
```

### “我在住房上的支出是多少？”
```bash
curl -s -H "Authorization: Bearer $KONTO_API_KEY" "$KONTO_URL/api/v1/transactions?months=6&category=logement" | jq '{total: .total, transactions: [.transactions[] | {date, label, amount}]}'
```

### “财务概览”
```bash
curl -s -H "Authorization: Bearer $KONTO_API_KEY" "$KONTO_URL/api/v1/summary"
```

## 辅助脚本
```bash
bash ~/.openclaw/workspace/skills/konto/scripts/konto.sh summary
bash ~/.openclaw/workspace/skills/konto/scripts/konto.sh investments
bash ~/.openclaw/workspace/skills/konto/scripts/konto.sh transactions 3  # last 3 months
bash ~/.openclaw/workspace/skills/konto/scripts/konto.sh loans
bash ~/.openclaw/workspace/skills/konto/scripts/konto.sh assets
bash ~/.openclaw/workspace/skills/konto/scripts/konto.sh accounts
```

## 端点
| 端点          | 描述                          |
|--------------|-------------------------------------------|
| `GET /api/v1/summary` | 完整的财务概览（从此处开始查询）         |
| `GET /api/v1/accounts` | 银行账户列表                         |
| `GET /api/v1/transactions?months=6&category=X` | 分类后的交易记录                   |
| `GET /api/v1/investments` | 投资组合（ETF、股票、加密货币）                |
| `GET /api/v1/assets` | 房产、车辆等实物资产                     |
| `GET /api/v1/loans` | 在途贷款                         |

## 完整的 API 参考文档
请参阅 `~/shared/projects/konto/docs/api.md`，以获取包括分析端点在内的完整文档。

## 使用范围
此技能使用 **个人** 使用范围键（免费）。如需进行跨用户分析（专业版），请参阅 `konto-analytics` 技能。