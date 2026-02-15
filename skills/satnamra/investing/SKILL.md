---
name: investing
version: 1.0.0
description: 面向立陶宛投资者的个人投资助手。该助手会监控市场、交易型开放式指数基金（ETFs）、加密货币以及养老基金（第三阶段产品），并根据研究结果和市场状况每月提供投资建议。
author: Buba Draugelis
license: MIT
tags:
  - finance
  - investing
  - etf
  - crypto
  - lithuania
  - pension
metadata:
  openclaw:
    emoji: "💰"
---

# 投资技巧

这是一套专为立陶宛投资者量身定制的综合性投资辅助工具，其设计理念源自šešiNuliai.lt的哲学思想。

## 核心投资理念

我们遵循基于证据的被动投资策略：
- **VWCE & Chill**：简单、低成本的全球ETF投资策略
- **长期投资**：投资期限为10年以上
- **资产多元化**：涵盖不同的资产类别和地区
- **低成本**：尽量降低费用，提高投资回报

## 资产配置框架

### 推荐的投资组合（中等风险）

```
📊 Sample Allocation:
├── 70% Stocks (ETFs)
│   ├── 50% VWCE (All-World)
│   ├── 15% IXUS (Ex-US) or EIMI (Emerging)
│   └── 5% Small Cap Value
├── 10% Bonds
│   └── AGGH or Government Bonds
├── 10% Crypto
│   ├── 8% Bitcoin
│   └── 2% Ethereum
└── 10% Cash / Short-term
    └── Savings accounts, MMF
```

投资组合的调整需考虑以下因素：
- 年龄（越年轻，股票配置比例越高）
- 风险承受能力
- 投资期限
- 收入稳定性

## 数据来源

### 立陶宛本地资源
- **šešiNuliai.lt**：个人理财博客（立陶宛语）
- **Investuok.eu**：投资新闻（立陶宛语）
- **Vz.lt**：商业新闻（立陶宛语）
- **Delfi Verslas**：商业资讯板块

### 国际资源
- **Bogleheads**：被动投资社区
- **r/eupersonalfinance**：专注于欧盟的个人理财论坛
- **JustETF**：ETF比较平台
- **Portfolio Visualizer**：投资组合可视化工具

## 市场数据来源
- **Yahoo Finance**：股票/ETF价格数据
- **TradingView**：图表分析工具
- **CoinGecko**：加密货币价格信息
- **ECB**：欧洲中央银行（欧元汇率及利率数据）

## 自动化脚本

### check-etf-prices.sh

```bash
#!/bin/bash
# Check key ETF prices
echo "📈 ETF Prices - $(date '+%Y-%m-%d')"
echo "================================"

# VWCE - Vanguard FTSE All-World
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/VWCE.DE" | \
  jq -r '"VWCE: €" + (.chart.result[0].meta.regularMarketPrice | tostring)'

# EIMI - iShares Emerging Markets
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/EIMI.L" | \
  jq -r '"EIMI: £" + (.chart.result[0].meta.regularMarketPrice | tostring)'

# Bitcoin
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur" | \
  jq -r '"BTC: €" + (.bitcoin.eur | tostring)'
```

### monthly-dca.sh

```bash
#!/bin/bash
# Calculate monthly DCA amounts
BUDGET=${1:-500}  # Monthly investment budget

echo "💰 Monthly DCA Plan - €$BUDGET"
echo "================================"
echo "VWCE (70%):   €$((BUDGET * 70 / 100))"
echo "EIMI (10%):   €$((BUDGET * 10 / 100))"
echo "BTC (10%):    €$((BUDGET * 10 / 100))"
echo "Cash (10%):   €$((BUDGET * 10 / 100))"
```

## 月度投资流程

### 1. 市场行情检查（5分钟）

```
Run: check-etf-prices.sh
Check: Any significant drops (>10%) = buying opportunity
```

### 2. 新闻浏览（10分钟）

```
Scan:
- šešiNuliai.lt - new posts?
- r/eupersonalfinance - hot topics?
- ECB announcements - rate changes?
```

### 3. 执行定期定额投资（DCA）（5分钟）

```
Run: monthly-dca.sh [budget]
Execute trades via:
- Interactive Brokers (ETFs)
- Bitstamp/Kraken (Crypto)
```

### 4. 记录投资情况并反思（5分钟）

```
Update:
- Portfolio tracker spreadsheet
- Note any deviations from plan
- Review annual progress
```

## 第三阶段（养老金投资策略）

### 适用条件

1. **雇主提供的养老金贡献**：务必全额领取
2. **处于高税率区间**（边际税率超过32%）
3. **投资期限较长**（距离退休至少15年以上）
4. **适用2019年之前的法规**（某些条款可能更优惠）

### 推荐的投资基金

| 基金 | 年管理费率（TER） | 说明 |
|------|-----|-------|
| Goindex III pakopa | 0.40% | 跟踪指数，低成本 |
| Swedbank Index | 0.45% | 也是指数基金 |
| Luminor Index | 0.50% | 可选的投资方案 |

**避免选择：** 年管理费率超过1%的主动管理型基金

### 年度优化策略

1. 首先充分利用雇主提供的养老金贡献
2. 计算税收优惠与投资成本之间的差额
3. 考虑使用IBKR等个人经纪账户来管理超额部分
4. 每年评估基金表现

## 加密货币投资策略

### 主要投资品种（占加密货币总投资的90%）

- **比特币（BTC）**：占加密货币投资的80%
- **以太坊（ETH）**：占20%

### 投资规则

1. 单一资产的投资比例不得超过总投资额的10%
2. 采用定期定额投资（DCA）方式，避免试图预测市场走势
3. 对大额资金采用自我托管方式（如Ledger或Trezor）
4. 长期持有（至少5年以上）

### 在欧盟地区的购买渠道

- **Bitstamp**：费用较低，受欧盟监管
- **Kraken**：安全性较高，支持SEPA转账
- **Coinbase**：操作便捷，但费用较高

## 应急资金准备

在开始投资之前，请确保：

```
Emergency Fund = 3-6 months expenses
Location: High-yield savings account
Current best rates (LT):
- Swedbank Taupomasis: ~3%
- SEB Taupomoji: ~2.5%
- Revolut Savings: ~3.5%
```

## 立陶宛的税收政策

### 资本利得税

- **资本利得税率为15%**
- **持有期限要求**：与美国的政策不同，长期持有无税收优惠
- **亏损**：可在同一年内用于抵扣收益

### 第三阶段养老金投资的税收优惠

- **雇主贡献部分**：可从应税收入中扣除（每年最高1,500欧元）
- **提取养老金**：需缴纳15%的税款（退休后免税）

### 加密货币投资的相关税收规定

- **实现收益需缴纳15%的税款**
- **需仔细记录成本基础**
- **每年进行税务申报**

## 定时任务

### 日价格提醒

```javascript
{
  "name": "Daily Market Check",
  "schedule": { "kind": "cron", "expr": "0 9 * * 1-5" },
  "payload": {
    "kind": "agentTurn",
    "message": "Check VWCE, BTC prices. Alert if >5% change from yesterday."
  }
}
```

### 月度投资提醒

```javascript
{
  "name": "Monthly DCA Reminder",
  "schedule": { "kind": "cron", "expr": "0 10 1 * *" },
  "payload": {
    "kind": "agentTurn",
    "message": "Monthly DCA time! Check budget, run monthly-dca.sh, execute trades."
  }
}
```

### 季度投资回顾

```javascript
{
  "name": "Quarterly Portfolio Review",
  "schedule": { "kind": "cron", "expr": "0 10 1 1,4,7,10 *" },
  "payload": {
    "kind": "agentTurn",
    "message": "Quarterly review: Check allocation drift, rebalance if >5% off target, update spreadsheet."
  }
}
```

## 参考资源

### 书籍
- 《简单财富之路》（The Simple Path to Wealth）——JL Collins著
- 《随机漫步华尔街》（A Random Walk Down Wall Street）——Burton Malkiel著
- 《Bogleheads的投资指南》（The Bogleheads’ Guide to Investing）

### 网站
- **šešiNuliai.lt**（立陶宛语个人理财网站）
- **Bogleheads.org**：被动投资社区网站
- **JustETF.com**：ETF信息平台
- **r/eupersonalfinance**：欧盟个人理财论坛

### 工具

- **Portfolio Visualizer**：投资组合可视化工具
- **IBKR**：经纪服务平台
- **Notion/Sheets**：数据追踪工具

## 免责声明

本文档仅供参考，并不构成专业金融建议。请自行进行充分研究。过去的投资表现不能保证未来的收益，投资存在亏损风险。

---

*本投资策略基于šešiNuliai.lt、Bogleheads社区及欧盟个人理财社区的研究成果制定。*