---
name: crypto-whale-tracker
version: 1.0.0
description: 使用像 Whale Alert 和 Etherscan 这样的公共 API 来追踪大规模的加密货币转账（即“鲸鱼交易”）。设置相应的阈值，监控钱包活动，并生成格式化的报告。
---
# 🐋 加密货币大户追踪器

实时追踪大规模的加密货币转账，提前了解大户的交易动向，从而在市场做出反应之前掌握先机。

## 快速入门

```bash
# Track whale transfers above 100 BTC
bash scripts/whale_tracker.sh --coin BTC --threshold 100

# Monitor ETH whales with custom timeframe
bash scripts/whale_tracker.sh --coin ETH --threshold 500 --hours 24

# Generate HTML report
bash scripts/whale_tracker.sh --coin BTC --threshold 50 --format html --output whale_report.html

# Track specific wallet
bash scripts/whale_tracker.sh --wallet 0xABC123... --chain ethereum
```

## 工作原理（分步说明）

### 第1步：数据收集
该工具通过查询公共API（如Whale Alert的免费 tier、Etherscan、Blockchair）来获取最近的大额交易记录。基本使用无需API密钥，但使用API密钥可以提高请求速率限制。

### 第2步：过滤
系统会根据您指定的阈值对交易进行过滤，仅包含超过最低金额的交易。已知的交易所钱包会自动被标记出来。

### 第3步：分类
每笔交易会被分类为以下几种类型：
- **交易所 → 交易所**：可能是场外交易或内部转账
- **交易所 → 未知**：可能是提款（看涨信号）
- **未知 → 交易所**：可能是用于出售的存款（看跌信号）
- **未知 → 未知**：大户之间的转账

### 第4步：生成报告
结果会被格式化为一份清晰的报告，包含以下信息：
- 交易哈希和时间戳
- 来源和目的地（附带交易所标签）
- 加密货币的金额及估算的美元价值
- 交易类型和市场信号

## 配置参数

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| `--coin` | BTC | 要追踪的加密货币（BTC、ETH、USDT等） |
| `--threshold` | 100 | 最低转账金额 |
| `--hours` | 12 | 回顾时间周期（以小时为单位） |
| `--format` | text | 输出格式：文本、json、html、csv |
| `--output` | stdout | 输出文件路径 |
| `--wallet` | - | 跟踪特定的钱包地址 |
| `--chain` | bitcoin | 区块链网络 |
| `--api-key` | - | Whale Alert API密钥（可选） |
| `--label` | true | 为已知交易所钱包添加标签 |
| `--top` | 20 | 显示的最大交易数量 |

## 支持的区块链网络

| 区块链网络 | 支持的加密货币 | API来源 |
|-------|------|-----------|
| Bitcoin | BTC | Blockchair、Whale Alert |
| Ethereum | ETH、ERC-20 | Etherscan、Whale Alert |
| BSC | BNB、BEP-20 | BscScan |
| Tron | TRX、TRC-20 | Tronscan |
| Solana | SOL | Solscan |

## 交易所钱包标签
该工具内置了一个已知交易所钱包的数据库，涵盖以下交易所：
- Binance、Coinbase、Kraken、OKX、Bybit |
- Bitfinex、Huobi、KuCoin、Gate.io |
- Gemini、Bitstamp、FTX（历史数据）

## 使用场景

1. **市场情绪分析**：大量资金流入交易所通常预示着后续的抛售行为。
2. **资金积累检测**：大户将资金转移到冷存储中可能表示看涨趋势。
3. **稳定币流动**：USDT/USDC等稳定币的交易动向可能预示着即将发生的买入行为。
4. **警报系统**：可以设置定时任务来定期接收大户交易警报。

## 定时任务示例

```bash
# Check every 30 minutes for BTC whales
*/30 * * * * bash /path/to/whale_tracker.sh --coin BTC --threshold 200 --hours 1 --format json >> /var/log/whale_alerts.json
```

## 输出示例

```
🐋 WHALE ALERT — BTC Transfers > 100 BTC (Last 12h)
══════════════════════════════════════════════════════

#1  🔴 2,500 BTC ($162.5M) — Unknown → Binance
    TX: abc123...def456
    Time: 2025-03-10 14:32 UTC
    Signal: BEARISH (possible sell preparation)

#2  🟢 1,800 BTC ($117.0M) — Coinbase → Unknown
    TX: 789ghi...jkl012
    Time: 2025-03-10 13:15 UTC
    Signal: BULLISH (withdrawal to cold storage)

Summary: 15 whale transfers totaling 12,340 BTC ($802.1M)
  Inflows to exchanges:  5,200 BTC (42.1%)
  Outflows from exchanges: 7,140 BTC (57.9%)
  Net flow: OUTFLOW (bullish signal)
```

## 限制因素

- 免费API的请求速率有限（通常为每分钟10次）。
- 无付费API时，历史数据仅限于约30天。
- 美元价值是基于当前价格估算的。
- 部分钱包标签可能已经过时。

## 相关文件

- `scripts/whale_tracker.sh` — 主追踪脚本
- `tips.md` — 使用技巧和注意事项