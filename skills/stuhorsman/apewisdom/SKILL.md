---
name: apewisdom
description: 使用 ApeWisdom API（免费）在 Reddit 上搜索热门股票及情绪波动。该 API 可帮助您发现“网络热股”（meme stocks）、散户投资者的购买热情，以及 r/wallstreetbets 子版块中的情绪变化。
---

# ApeWisdom Reddit Scanner

该工具用于扫描 Reddit（如 r/wallstreetbets、r/stocks 等板块），以获取热门股票代码及情绪波动信息。

## 使用方法

该功能通过 Python 脚本从 ApeWisdom 获取实时数据。

### 基本扫描（热门股票）
获取当前讨论最多的 20 只股票。

```bash
skills/apewisdom/scripts/scan_reddit.py
```

### 寻找情绪波动（股票走势）
筛选出 24 小时内被提及次数增长最快的股票（忽略交易量较低带来的干扰）。这是发现热门股票（如 $SNDK）的最佳方法。

```bash
skills/apewisdom/scripts/scan_reddit.py --sort spike
```

### 指定子版块
可按特定子版块进行筛选。

```bash
# WallStreetBets only
skills/apewisdom/scripts/scan_reddit.py --filter wallstreetbets

# SPACs
skills/apewisdom/scripts/scan_reddit.py --filter SPACs

# Crypto
skills/apewisdom/scripts/scan_reddit.py --filter all-crypto
```

## 输出字段

- `ticker`：股票代码
- `mentions`：过去 24 小时内的提及次数
- `mentions_24h_ago`：24 小时前的提及次数
- `change_pct`：讨论量的百分比变化
- `upvotes`：提及该股票的帖子所获得的总点赞数