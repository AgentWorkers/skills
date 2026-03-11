---
name: Arbitrage Finder
version: 1.0.0
description: 扫描不同交易所之间的价格差异，发现套利机会，并追踪历史上的成功率。
---
# 套利发现器 🔄

通过扫描价格差异、考虑费用和转账时间，并评估盈利能力，来发现跨交易所的套利机会。

## 工作原理 — 逐步说明

### 第一步：配置交易所

设置您想要监控的交易所。该工具使用公开的行情数据API（扫描价格无需API密钥）。

```bash
bash scripts/arbitrage-finder.sh config \
  --exchanges "binance,okx,bybit,coinbase,kraken,kucoin"
```

### 第二步：扫描机会

在所有配置的交易所中，针对特定资产或所有跟踪资产进行扫描：

```bash
# Scan specific pair
bash scripts/arbitrage-finder.sh scan --pair BTC/USDT

# Scan all tracked pairs
bash scripts/arbitrage-finder.sh scan --all

# Scan with minimum spread threshold
bash scripts/arbitrage-finder.sh scan --all --min-spread 0.5
```

### 第三步：分析机会

当发现价差时，结合费用和时机进行综合分析：

```bash
bash scripts/arbitrage-finder.sh analyze \
  --pair ETH/USDT \
  --buy-exchange binance \
  --sell-exchange coinbase \
  --amount 10000
```

分析结果包括：
- 买入价格及总成本（含费用）
- 卖出价格及总收入（扣除费用后）
- 网络转账费用及预计时间
- **净利润/亏损**（扣除所有费用后）
- **机会评分**（0-100分）

### 第四步：查看历史记录

追踪过去的机会及其结果：

```bash
bash scripts/arbitrage-finder.sh history --days 7 --pair BTC/USDT
```

### 第五步：生成报告

```bash
bash scripts/arbitrage-finder.sh report --days 30 --output arb-report.html
```

## 机会评分

每个机会的评分范围为0-100分，依据以下因素：

| 因素 | 权重 | 评分方式 |
|--------|--------|------------------|
| 净价差 | 30% | 所有费用后的实际价差 |
| 流动性 | 25% | 能否以报价价格成交？ |
| 转账速度 | 20% | 转账速度越快，价格风险越低 |
| 历史盈利能力 | 15% | 该交易路径之前是否盈利过？ |
| 波动性风险 | 10% | 转账期间的价格变动风险 |

### 评分解读

- **80-100** 🟢 非常好的机会 — 很有可能盈利 |
- **60-79** 🟡 中等机会 — 执行得当即可盈利 |
- **40-59** 🟠 风险较高 — 利润空间较小，时机至关重要 |
- **0-39** 🔴 不推荐 — 费用可能超过价差收益 |

## 费用参考

| 交易所 | 买价佣金 | 卖价佣金 | 提现（BTC） | 提现（ETH） |
|----------|-----------|-----------|-------------------|-------------------|
| Binance | 0.10% | 0.10% | 0.0001 | 0.00028 |
| Coinbase | 0.40% | 0.60% | 0.0001 | 0.00044 |
| Kraken | 0.16% | 0.26% | 0.00015 | 0.0025 |
| OKX | 0.08% | 0.10% | 0.0001 | 0.00028 |
| Bybit | 0.10% | 0.10% | 0.0002 | 0.0003 |
| KuCoin | 0.10% | 0.10% | 0.0002 | 0.0028 |

> 费用仅供参考，可能会频繁变动。工具会在可用时获取最新的费用信息。

## 转账时间预估

| 网络 | 平均确认时间 | 备注 |
|---------|-----------------|-------|
| Bitcoin | 30-60分钟 | 需要2-6次确认 |
| Ethereum | 5-15分钟 | 通常需要12次以上确认 |
| Solana | 小于1分钟 | 几乎即时 |
| TRON | 1-3分钟 | 需要19次确认 |
| Polygon | 2-5分钟 | 需要128次确认 |

## 风险提示

⚠️ **滑点风险**：大额订单可能无法以显示的价格成交。
⚠️ **转账风险**：在转账/存款期间价格可能会波动。
⚠️ **交易所风险**：存款可能会被延迟或暂停，且不另行通知。
⚠️ **本工具不执行交易**。它仅用于识别和评估机会。