---
name: revenue-tracker
description: 跟踪 {AGENT_NAME} 的收入和支出情况，生成财务报告，并分析其在各个平台上的盈利能力。
---

# 收入追踪器

用于跟踪所有平台上的收入、支出和盈利能力。

## 指导说明

1. **在 `~/.openclaw/revenue/transactions.jsonl` 文件中记录交易**：
   ```json
   {"date": "2026-02-10", "type": "income", "platform": "coconala", "amount": 3000, "fee": 660, "net": 2340, "description": "GAS automation", "currency": "JPY"}
   {"date": "2026-02-10", "type": "expense", "category": "api", "amount": 750, "description": "Cloudflare Workers", "currency": "JPY"}
   ```

2. **计算净收入**：
   ```bash
   # Daily income
   jq -s '[.[] | select(.date=="2026-02-10" and .type=="income")] | map(.net) | add' ~/.openclaw/revenue/transactions.jsonl
   
   # Monthly expenses
   jq -s '[.[] | select(.date | startswith("2026-02") and .type=="expense")] | map(.amount) | add' ~/.openclaw/revenue/transactions.jsonl
   ```

3. **平台费用参考**：

| 平台 | 费用比例 | 支付方式 |
|------|---------|---------|
| Coconala | 22% | 每月（最低 ¥3,000） |
| Fiverr | 20% | 每两周（最低 $5） |
| Upwork | 10-20% | 每周（最低 $100） |
| Moltbook | 1-2% | 即时支付（加密货币） |
| Note.com | 15%（需付费） | 每月 |
| Gumroad | 10% | 每周 |
| Direct | 0% | 按发票支付 |

4. **生成报告**：

   ### 每日报告
   ```
   📊 Daily Revenue — 2026-02-10
   Income:  ¥3,000 (Coconala ×1)
   Expense: ¥0
   Net:     ¥2,340 (after fees)
   ```

   ### 每周报告
   ```
   📊 Weekly Revenue — Week 6, 2026
   | Platform | Orders | Gross | Fees | Net |
   |----------|--------|-------|------|-----|
   | Coconala | 2 | ¥6,000 | ¥1,320 | ¥4,680 |
   | Note | 5 views | ¥500 | ¥75 | ¥425 |
   | Total | — | ¥6,500 | ¥1,395 | ¥5,105 |
   
   Expenses: ¥850 (API ¥750, Domain ¥100)
   Profit:   ¥4,255
   ```

   ### 每月报告
   ```
   📊 Monthly Revenue — February 2026
   Total Income:    ¥XX,XXX
   Total Expenses:  ¥X,XXX
   Net Profit:      ¥XX,XXX
   Profit Margin:   XX%
   Goal Progress:   XX% of ¥300,000
   
   By Platform: [bar chart using Unicode blocks]
   ████████░░ Coconala  60%
   ███░░░░░░░ Note      20%
   ██░░░░░░░░ Crypto    15%
   █░░░░░░░░░ Other      5%
   ```

5. **目标跟踪**：
   ```json
   {"month": "2026-02", "target": 300000, "actual": 0, "progress": 0}
   ```

## 里程碑

| 等级 | 月度目标 | 进度 |
|------|---------|--------|
| 🥉 青铜 | ¥10,000 | |
| 🥈 银 | ¥50,000 | |
| 🥇 金 | ¥100,000 | |
| 💎 钻石 | ¥300,000 | 目标：辞职 |
| 👑 皇冠 | ¥1,000,000 | |

## 安全注意事项

- **切勿在社交媒体上公开具体金额**——使用模糊的表述（如“赚了些钱”）
- **不要在任何共享或公开文件中将客户名称与金额关联** |
- **将 `transactions.jsonl` 文件设置为私密文件**——将其添加到 `.gitignore` 列表中 |
- **备份财务数据**——重要记录需妥善保存

## 所需条件

- 具备访问 `~/.openclaw/revenue/` 目录的文件系统权限 |
- 需要 `jq` 工具来查询 JSONL 文件 |
- 无需使用任何外部 API 密钥