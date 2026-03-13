---
name: Crypto News Feed
version: 1.0.0
description: 从 RSS 源中聚合加密货币新闻，根据关键词进行筛选，分析新闻的情感倾向，并生成每日摘要的 HTML 报告。
---
# 加密新闻订阅源 📰

> 为您提供个性化的加密新闻聚合服务，并附带情感分析功能。

## 快速参考卡

### 命令概览

| 命令 | 用法 | 输出 |
|---------|-------|--------|
| `fetch` | `bash scripts/crypto-news-feed.sh fetch` | 从所有来源获取最新新闻 |
| `filter` | `bash scripts/crypto-news-feed.sh filter --keywords "bitcoin,ETF"` | 根据关键词过滤新闻 |
| `digest` | `bash scripts/crypto-news-feed.sh digest --date today` | 生成每日 HTML 摘要 |
| `sentiment` | `bash scripts/crypto-news-feed.sh sentiment --keyword "ethereum"` | 获取指定主题的情感评分 |
| `sources` | `bash scripts/crypto-news-feed.sh sources` | 显示已配置的 RSS 源列表 |
| `add-source` | `bash scripts/crypto-news-feed.sh add-source --url URL --name NAME` | 添加新的 RSS 源 |
| `trending` | `bash scripts/crypto-news-feed.sh trending` | 显示热门话题 |

### 默认 RSS 源列表

```
📡 CoinDesk          https://www.coindesk.com/arc/outboundfeeds/rss/
📡 CoinTelegraph     https://cointelegraph.com/rss
📡 The Block         https://www.theblock.co/rss.xml
📡 Decrypt           https://decrypt.co/feed
📡 Bitcoin Magazine   https://bitcoinmagazine.com/feed
📡 Blockworks        https://blockworks.co/feed
📡 DL News           https://www.dlnews.com/rss/
```

### 情感评分系统

```
Score Range    Label         Emoji    Meaning
─────────────────────────────────────────────────
 0.6 to  1.0  Very Bullish  🟢🟢    Strong positive language
 0.2 to  0.6  Bullish       🟢      Positive outlook
-0.2 to  0.2  Neutral       ⚪      Balanced/factual
-0.6 to -0.2  Bearish       🔴      Negative outlook
-1.0 to -0.6  Very Bearish  🔴🔴    Strong negative language
```

### 内置关键词分类

- **去中心化金融 (DeFi):** defi, yield, liquidity, farming, pool, swap, AMM
- **非同质化代币 (NFT):** nft, opensea, blur, collection, mint, pfp
- **第二层网络 (L2):** layer2, rollup, arbitrum, optimism, zksync, base
- **监管政策:** sec, regulation, lawsuit, ban, approve, etf
- **网络热词 (Meme):** meme, doge, shib, pepe, bonk, wif

### 过滤示例

```bash
# DeFi news only
bash scripts/crypto-news-feed.sh filter --category defi

# Multiple keywords
bash scripts/crypto-news-feed.sh filter --keywords "solana,jupiter,jito"

# Bullish news only
bash scripts/crypto-news-feed.sh filter --min-sentiment 0.2

# Last 24 hours, bearish signals
bash scripts/crypto-news-feed.sh filter --hours 24 --max-sentiment -0.2

# Combine filters
bash scripts/crypto-news-feed.sh filter --keywords "bitcoin" --min-sentiment 0.3 --hours 48
```

### 每日摘要输出

`digest` 命令会生成 `crypto-digest-YYYY-MM-DD.html` 文件，其中包含：

1. **📊 市场情感概览** — 所有文章的平均情感评分
2. **🔥 热门文章** — 最受关注的文章
3. **📈 热门话题** — 被提及最多的关键词
4. **📰 所有文章** — 带有情感标签的完整文章列表
5. **📉 情感时间线** — 每小时的情感变化图表

### 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `NEWS_feed_DIR` | `./crypto-news` | 输出目录 |
| `NEWS_MAX_AGE` | `72` | 文章的最大保存时间（小时） |
| `NEWS_SOURCES_FILE` | `~/.crypto-news-sources.json` | 自定义 RSS 源配置文件 |
| `NEWS_CACHE_TTL` | `1800` | 缓存有效期（秒） |

### 自动化功能

```bash
# Add to crontab for daily 8am digest
0 8 * * * cd /path/to/workspace && bash skills/crypto-news-feed/scripts/crypto-news-feed.sh digest --date today
```