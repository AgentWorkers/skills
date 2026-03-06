---
name: news-sentiment
version: 1.0.0
description: >
  分析加密货币新闻的情绪（看涨/看跌）  
  扫描 Twitter、新闻网站和社交媒体平台。  
  获取情绪评分和交易信号。
metadata:
  openclaw:
    emoji: 📰
    requires:
      env:
        - DASHSCOPE_API_KEY
      bins:
        - python3
        - curl
---
# 📰 新闻情绪分析器 - 新闻情绪分析工具

该工具用于分析加密货币新闻及社交媒体上的情绪，以生成交易信号。

## 主要功能

- 📊 情绪评分（看涨/看跌/中性）
- 🔍 多源数据分析（Twitter、新闻、Reddit）
- 📈 交易信号生成
- ⚡ 钱币特定情绪分析
- ⚡ 实时更新

## 使用方法

```bash
# Analyze sentiment for a coin
/news-sentiment analyze BTC

# Get market sentiment
/news-sentiment market

# Set alerts
/news-sentiment alert --threshold 0.7
```

## 情绪评分标准

- **0.7 - 1.0**：非常看涨 🚀
- **0.3 - 0.7**：中性 ➡️
- **0.0 - 0.3**：非常看跌 📉

## API 数据来源

- Twitter API (6551.io)
- 新闻API
- 大语言模型（LLM）分析（Dashscope）