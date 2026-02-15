---
name: google-trends
version: 1.0.0
description: 监控 Google Trends：获取热门搜索词，比较关键词，并追踪用户兴趣的变化趋势。适用于市场研究、内容规划和趋势分析。
author: Buba Draugelis
license: MIT
tags:
  - trends
  - marketing
  - research
  - seo
  - content
metadata:
  openclaw:
    emoji: "📈"
---

# 谷歌趋势监控

监控和分析谷歌趋势数据，用于市场研究、内容规划和趋势跟踪。

## 功能

1. **每日热门搜索词** - 了解当今任何国家的热门搜索词
2. **关键词兴趣变化** - 关键词的历史趋势数据
3. **关键词比较** - 比较多个关键词
4. **相关主题与查询** - 发现相关的搜索内容
5. **地区兴趣分布** - 查看关键词在哪些地区最受欢迎

## 使用方法

### 获取每日热门搜索词

使用 `web_fetch` 获取谷歌趋势的 RSS 数据：

```bash
# US Daily Trends
curl -s "https://trends.google.com/trending/rss?geo=US" | head -100

# Lithuania
curl -s "https://trends.google.com/trending/rss?geo=LT" | head -100

# Worldwide
curl -s "https://trends.google.com/trending/rss?geo=" | head -100
```

### 检查关键词兴趣

如需详细分析关键词，请访问谷歌趋势官方网站：

```bash
# Open in browser
open "https://trends.google.com/trends/explore?q=bitcoin&geo=US"

# Or fetch via web_fetch for basic data
web_fetch "https://trends.google.com/trends/explore?q=bitcoin"
```

### 比较关键词

```bash
# Compare multiple terms (comma-separated)
open "https://trends.google.com/trends/explore?q=bitcoin,ethereum,solana&geo=US"
```

## 脚本

### trends-daily.sh

获取今日的热门搜索词：

```bash
#!/bin/bash
# Usage: ./trends-daily.sh [country_code]
# Example: ./trends-daily.sh LT

GEO="${1:-US}"
curl -s "https://trends.google.com/trending/rss?geo=$GEO" | \
  grep -o '<title>[^<]*</title>' | \
  sed 's/<[^>]*>//g' | \
  tail -n +2 | \
  head -20
```

### trends-compare.sh

生成关键词比较链接：

```bash
#!/bin/bash
# Usage: ./trends-compare.sh keyword1 keyword2 keyword3
# Example: ./trends-compare.sh bitcoin ethereum solana

KEYWORDS=$(echo "$@" | tr ' ' ',')
echo "https://trends.google.com/trends/explore?q=$KEYWORDS"
```

## 示例工作流程

### 早晨市场研究

```
1. Get US trending searches
2. Get LT trending searches  
3. Check if any trends relate to our business
4. Report interesting findings
```

### 内容规划

```
1. Compare potential blog topics
2. Find which has more search interest
3. Check seasonal patterns
4. Decide on content focus
```

### 竞争对手监控

```
1. Compare brand names
2. Track interest over time
3. Identify when competitors spike
4. Investigate causes
```

## Cron 作业集成

设置自动化的趋势监控任务：

```javascript
// Example cron job for daily trends report
{
  "name": "Daily Trends Report",
  "schedule": { "kind": "cron", "expr": "0 9 * * *" },
  "payload": {
    "kind": "agentTurn",
    "message": "Get today's Google Trends for US and LT. Summarize top 10 trends for each. Highlight any tech/business related trends."
  }
}
```

## 国家代码

常见的国家代码：
- US - 美国
- LT - 立陶宛
- DE - 德国
- GB - 英国
- FR - 法国
- JP - 日本
- (empty) - 全球

## 限制

- 谷歌趋势不提供官方 API
- 高频率使用可能会受到流量限制
- 数据为相对值（非绝对数字）
- 历史数据仅提供约 5 年的详细视图

## 提示

1. **使用具体术语** - 例如使用 “iPhone 15 Pro” 而不是 “iPhone”
2. **注意季节性变化** - 一些趋势具有周期性
3. **与基准数据进行比较** - 使用稳定的关键词作为参考
4. **查看相关查询** - 发现新的市场机会
5. **监控竞争对手** - 随时间跟踪品牌的热度变化