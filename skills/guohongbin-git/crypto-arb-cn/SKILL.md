---
name: crypto-arb-cn
description: "加密货币套利监控工具 | Cryptocurrency Arbitrage Monitor  
支持币安（Binance）、OKX、Gate.io、火币（Huobi）等交易平台。  
具备实时价格监控、利润计算以及通过Telegram发送通知的功能。  
触发关键词：套利（arbitrage）、加密货币（crypto）、价格差（price difference）。  
帮助用户在可访问的中文交易平台中寻找套利机会。"
---
# 加密货币套利（中国）

监控中国用户可访问的交易平台上的加密货币价格，寻找套利机会。

## 快速入门

```bash
# Single check for opportunities
python scripts/arbitrage_monitor.py --once

# Continuous monitoring (every 30 seconds)
python scripts/arbitrage_monitor.py
```

## 支持的交易平台

| 交易平台 | 手续费 | API |
|----------|-----|-----|
| Binance | 0.1% | ✅ |
| OKX | 0.08% | ✅ |
| Gate.io | 0.2% | ✅ |
| Huobi | 0.2% | ✅ |

## 配置

在 `scripts/arbitrage_monitor.py` 文件中修改以下变量：

```python
# Trading pairs to monitor
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT"]

# Minimum profit threshold (after fees)
MIN_PROFIT_PERCENT = 0.5  # 0.5%

# Check interval (for continuous mode)
INTERVAL = 30  # seconds
```

## 输出格式

当发现套利机会时：

```
💰 BTCUSDT | 币安 → OKX | 利润: 0.65%
   买入: ¥485,230 (币安)
   卖出: ¥488,380 (OKX)
   预计利润: ¥3,150 (每 BTC)
```

## 使用示例

**一次性检查：**
```
用户: 帮我看看现在有没有套利机会
→ Run: python scripts/arbitrage_monitor.py --once
```

**开始监控：**
```
用户: 开始监控套利机会
→ Run: python scripts/arbitrage_monitor.py
```

**添加 Telegram 通知：**
```
用户: 有机会发 Telegram 给我
→ Set up TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
```

## 重要提示

1. **手续费不可忽视**：交易前请务必计算扣除手续费后的实际利润（每笔交易0.1%-0.2%）。
2. **转账时间**：跨交易平台套利需要完成加密货币的转账（通常需要10-60分钟）。
3. **价格波动性**：价格变化迅速，套利机会可能很快消失。
4. **风险提示**：套利存在风险，请用户自行判断是否参与。

## 参考资料

- 有关详细交易平台的 API 文档，请参阅 [references/exchanges.md](references/exchanges.md)。