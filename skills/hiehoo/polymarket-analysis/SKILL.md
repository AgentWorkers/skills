---
name: polymarket-analysis
description: 分析 Polymarket 的预测市场以寻找交易机会：包括成本套利、大户行为追踪、市场情绪分析、趋势信号以及用户行为监测。请注意，本功能不涉及交易执行。
version: 2.1.0
---

# Polymarket 分析

通过多模态分析，识别 Polymarket 预测市场中的交易机会。

**范围：** 仅用于分析和机会识别，不涉及交易执行。

## 模式

| 模式 | 描述 | 参考文档 |
|------|-------------|-----------|
| **分析** | 一次性市场分析 | 本文件 |
| **监控** | 24/7 市场监控 | `references/market-monitoring-setup.md` |
| **用户资料** | 跟踪用户钱包持仓 | `scripts/fetch-polymarket-user-profile.py` |

## 脚本

```bash
# Monitor market for alerts
python3 scripts/monitor-polymarket-market.py <market_url_or_id>

# Fetch user profile/positions
python3 scripts/fetch-polymarket-user-profile.py <wallet_address> [--trades] [--pnl]
```

## 快速入门

### 市场分析
1. 从用户处获取市场 URL。
2. 通过 `https://gamma-api.polymarket.com/markets?slug={slug}` 获取市场数据。
3. 运行多策略分析。

### 用户资料
```bash
# From profile URL: polymarket.com/profile/0x...
python3 scripts/fetch-polymarket-user-profile.py 0x7845bc5e15bc9c41be5ac0725e68a16ec02b51b5
```

## 核心策略

| 策略 | 描述 | 参考文档 |
|----------|-------------|-----------|
| 对冲套利 | 当价格差小于 $1.00 时执行 | `references/pair-cost-arbitrage.md` |
| 动量策略 | 基于 RSI、MA 指标 | `references/momentum-analysis.md` |
| 大额交易追踪 | 监测大额交易 | `references/whale-tracking.md` |
| 情感分析 | 分析市场情绪（新闻/社交媒体数据） | `references/sentiment-analysis.md` |

## 警报阈值

| 事件 | 阈值 |
|-------|-----------|
| 价格变动 | 1 小时内价格变动 ±5% |
| 大额交易 | 交易金额 > $5,000 |
| 对冲套利机会 | 对冲套利价格差 < $0.98 |
| 交易量激增 | 交易量超过平均值 2 倍 |

## API

| API | 基本 URL | 使用方式 |
|-----|----------|-----|
| Gamma | `gamma-api.polymarket.com` | 市场数据、价格信息 |
| Data | `data-api.polymarket.com` | 用户持仓、交易记录、盈亏情况 |
| CLOB | `clob.polymarket.com` | 订单簿、交易数据 |

详细 API 接口信息请参阅 `references/polymarket-api.md`。

## 参考文献

- `references/polymarket-api.md` - API 接口（Gamma、Data、CLOB）
- `references/market-monitoring-setup.md` - 24/7 市场监控设置
- `references/pair-cost-arbitrage.md` - 对冲套利策略
- `references/momentum-analysis.md` - 动量分析策略
- `references/whale-tracking.md` - 大额交易追踪
- `references/sentiment-analysis.md` - 市场情绪分析