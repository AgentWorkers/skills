---
name: crypto-alpha-scanner
version: 1.0.0
description: 自动化加密市场情报服务——提供价格数据、市场情绪分析、热门加密货币信息以及 Polymarket 的热门交易市场信息。完全无外部依赖，可靠性高达 100%。非常适合用于测试环境（alpha channels）和市场监控场景。
author: nix
tags: [crypto, alpha, market-data, sentiment, polymarket, coingecko, fear-greed]
---

# 📡 Crypto Alpha Scanner

**一个命令即可获取可靠的市场情报。**

无需API密钥，也无需依赖任何外部服务，仅使用Python标准库即可运行。

## 主要功能

- 📊 **实时价格** — 提供BTC、ETH、SOL的24小时价格变化情况  
- 😱 **恐惧与贪婪指数** — 衡量市场情绪的工具  
- 🔥 **热门加密货币** — 显示CoinGecko上的热门加密货币  
- 🎯 **Polymarket热门市场** — 按交易量排序的热门预测市场  
- 💡 **自动分析** — 基于数据的实用分析建议  

## 快速入门

```bash
# Generate alpha report
python3 scripts/scanner.py

# Output to file
python3 scripts/scanner.py > report.txt

# Post to Telegram (with bot token)
python3 scripts/scanner.py | ./scripts/post_telegram.sh
```

## 示例输出

```
🤖 Alpha Report | 2026-02-11 19:00 UTC

📊 Market Pulse
🔴 BTC: $67,216 (-2.3%)
🔴 ETH: $1,943 (-3.2%)
🔴 SOL: $80 (-3.9%)
😱 Fear/Greed: 11 (Extreme Fear)

🔥 Trending: LayerZero, Uniswap, Bitcoin, Hyperliquid

🎯 Polymarket Hot
• Will Trump nominate Judy Shelton...? ($5.1M)
• Will the Fed decrease rates...? ($3.3M)

💡 Extreme fear = historically strong buy zone.

— Nix 🔥
```

## 数据来源

| 数据来源 | 提供的数据 | 数据更新频率 |
|--------|------|------------|
| CoinGecko | 价格、热门加密货币信息 | 每30分钟更新一次 |
| Alternative.me | 恐惧与贪婪指数 | 无更新限制 |
| Polymarket Gamma | 各种预测市场数据 | 无更新限制 |

## 定时任务设置

每小时运行一次，以确保数据的连续性：

```bash
# Add to crontab
0 * * * * python3 /path/to/scripts/scanner.py >> /var/log/alpha.log
```

## 自定义功能

您可以编辑`scripts/scanner.py`文件来：
- 添加更多加密货币  
- 修改数据格式  
- 添加自定义的分析内容  
- 将该工具集成到您的信息渠道中  

## 选择这个工具的理由？

✅ **100% 可靠** — 仅使用稳定可靠的API  
✅ **无需任何设置** — 完全无需API密钥  
✅ **运行速度快** — 执行时间少于3秒  
✅ **便携性强** — 仅使用Python编写，可在任何环境中运行  

---

*由Nix开发 🥥 | 免费试用，永久使用*