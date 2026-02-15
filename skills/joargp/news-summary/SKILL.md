---
name: news-summary
description: 当用户请求获取新闻更新、每日简报或了解全球发生的事件时，应使用此技能。该技能会从可靠的国际RSS源中获取新闻，并能够生成语音摘要。
---

# 新闻摘要

## 概述

通过 RSS 源从可信的国际新闻来源获取并汇总新闻。

## RSS 源

### 英国广播公司（BBC，主要来源）
```bash
# World news
curl -s "https://feeds.bbci.co.uk/news/world/rss.xml"

# Top stories
curl -s "https://feeds.bbci.co.uk/news/rss.xml"

# Business
curl -s "https://feeds.bbci.co.uk/news/business/rss.xml"

# Technology
curl -s "https://feeds.bbci.co.uk/news/technology/rss.xml"
```

### 路透社
```bash
# World news
curl -s "https://www.reutersagency.com/feed/?best-regions=world&post_type=best"
```

### 美国国家公共电台（NPR）
```bash
curl -s "https://feeds.npr.org/1001/rss.xml"
```

### 卡塔尔半岛电视台（Al Jazeera，关注全球南方地区）
```bash
curl -s "https://www.aljazeera.com/xml/rss/all.xml"
```

## 解析 RSS 数据

提取新闻标题和描述：
```bash
curl -s "https://feeds.bbci.co.uk/news/world/rss.xml" | \
  grep -E "<title>|<description>" | \
  sed 's/<[^>]*>//g' | \
  sed 's/^[ \t]*//' | \
  head -30
```

## 工作流程

### 文本摘要
1. 获取 BBC 的全球头条新闻
2. （可选）补充路透社或美国国家公共电台的新闻
3. 概述重点新闻内容
4. 按地区或主题对新闻进行分类

### 语音摘要
1. 生成文本摘要
2. 使用 OpenAI 的文本转语音（TTS）功能将其转换为语音
3. 以音频消息的形式发送出去

```bash
curl -s https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1-hd",
    "input": "<news summary text>",
    "voice": "onyx",
    "speed": 0.95
  }' \
  --output /tmp/news.mp3
```

## 示例输出格式

```
📰 News Summary [date]

🌍 WORLD
- [headline 1]
- [headline 2]

💼 BUSINESS
- [headline 1]

💻 TECH
- [headline 1]
```

## 最佳实践

- 保持摘要简洁（5-8 条主要新闻）
- 优先报道突发新闻和重大事件
- 语音播报时长控制在 2 分钟以内
- 平衡西方和全球南方地区的新闻视角
- 如有需要，注明新闻来源