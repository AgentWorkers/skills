---
name: stock_data
description: "从 Simplywall.st 获取全面的股票数据。当用户询问任何全球股票的股价、估值、财务信息、股息或投资分析时，可以使用此功能。"
metadata:
  openclaw:
    emoji: "📈"
    version: "1.0.0"
    author: "OpenClaw Community"
    requires:
      envVars: ["ZAI_API_KEY"]
---
# 股票数据 - Simplywall.st

从 Simplywall.st 获取任何全球股票的全面股票数据。

## 使用场景

- 用户询问股票价格（例如：“ADRO 的股价是多少？”）
- 用户希望进行估值分析（例如：“ADRO 是被低估还是被高估了？”）
- 用户需要财务数据（例如：“BBCA 的收入是多少？”）
- 用户想要了解股息信息（例如：“TLKM 的股息率是多少？”）
- 用户请求投资分析（例如：“NVDA 的投资分析如何？”

## 输入参数

| 参数 | 类型 | 是否必填 | 描述 |
|---------|--------|---------|-------------|
| ticker | string | 是 | 股票代码（例如：ADRO, AAPL, BBRI） |
| exchange | string | 否 | 交易所代码（例如：IDX, NASDAQ, NYSE） |

## 输出结构

```json
{
  "success": true,
  "ticker": "ADRO",
  "exchange": "IDX",
  "data": {
    "company": {
      "name": "PT Alamtri Resources Indonesia Tbk",
      "description": "Company description...",
      "country": "Indonesia",
      "founded": 2004,
      "website": "www.alamtri.com"
    },
    "price": {
      "lastSharePrice": 2300,
      "currency": "IDR",
      "return7D": 0.036,
      "return1Yr": 0.055
    },
    "valuation": {
      "marketCap": 3908.23,
      "peRatio": 13.07,
      "pbRatio": 0.85,
      "pegRatio": 0.41,
      "intrinsicDiscount": -39.06,
      "status": "overvalued"
    },
    "financials": {
      "eps": 0.0104,
      "roe": 8.77,
      "roa": 3.09,
      "debtEquity": 0.12
    },
    "dividend": {
      "yield": 13.48,
      "futureYield": 5.64,
      "payingYears": 10,
      "payoutRatio": 1.88
    },
    "forecast": {
      "earningsGrowth1Y": 0.51,
      "roe1Y": 9.74,
      "analystCount": 10
    },
    "snowflake": {
      "value": 3,
      "future": 6,
      "past": 2,
      "health": 6,
      "dividend": 4
    },
    "recentEvents": [
      {
        "title": "Investor sentiment improves...",
        "description": "..."
      }
    ],
    "fetchedAt": "2026-02-22T08:30:00Z"
  }
}
```

## 示例用法

```
User: "Cek saham ADRO gimana?"
→ Call stock_data(ticker="ADRO")

User: "What's Apple's P/E ratio?"
→ Call stock_data(ticker="AAPL", exchange="NASDAQ")

User: "Berapa dividend yield TLKM?"
→ Call stock_data(ticker="TLKM")
```

## 支持的交易所

| 交易所 | 代码 | 示例股票代码 |
|------|---------|-----------------|
| 印度尼西亚 | IDX | ADRO, BBRI, BBCA, TLKM |
| 美国纳斯达克 | NASDAQ | AAPL, NVDA, GOOGL |
| 美国纽约证券交易所 | NYSE | JPM, BAC, WMT |
| 澳大利亚 | ASX | BHP, CBA, RIO |
| 英国 | LSE | HSBA, BP, SHEL |
| 加拿大 | TSX | RY, TD, CNR |
| 新加坡 | SGX | DBS, OCBC |

## 数据来源

- 数据来自 S&P Global Market Intelligence，通过 Simplywall.st 提供
- 价格数据每日更新
- 估值基于专有模型计算
- 仅供参考，不构成投资建议

## 所需环境

- `ZAI_API_KEY`：用于网络请求的 Z.AI API 密钥