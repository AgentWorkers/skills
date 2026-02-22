---
name: signal-pipeline
description: **营销情报管道**：从 RSS、X/Twitter、Telegram 和 Gmail 新闻通讯中收集数据。生成每日更新的内容、每周汇总以及每月的深度分析报告，以支持内容创作。适用于需要构建内容情报系统或跟踪营销/技术趋势的场景。
---
# 信号处理管道（Signal Pipeline）

这是一个市场情报处理管道，它从多个来源收集数据，将这些数据存储到 SQLite 数据库中，并生成用于个人品牌建设的内容。

## 功能概述

- **RSS 源** → 存储到 SQLite 数据库（rss_db.py）
- **X/Twitter** → 存储到 SQLite 数据库（x_monitor.py）
- **Telegram 频道** → 存储到 SQLite 数据库（telegram_monitor.py）
- **Gmail 通讯** → 提取数据（newsletter_monitor.py）
- **每日信号** → 生成草稿帖子
- **每周总结** → 主题分析
- **每月深度分析** → 撰写文章或书籍章节

## 包含的文件

```
signal-pipeline/
├── SKILL.md              # This file
├── README.md             # Setup instructions
├── requirements.txt      # Python dependencies
├── daily_signals.py      # Main script (daily/weekly/monthly)
├── rss_db.py           # RSS feed storage
├── x_monitor.py        # X/Twitter monitoring
├── telegram_monitor.py  # Telegram channel scraping
└── newsletter_monitor.py # Gmail newsletter extraction
```

## 快速入门

```bash
# Install dependencies
cd skills/signal-pipeline
pip install -r requirements.txt

# Run daily signals
python daily_signals.py

# Generate weekly summary
python daily_signals.py --weekly

# Generate monthly report
python daily_signals.py --monthly
```

## 配置

### RSS 源
编辑 `rss_db.py` 以添加您的 RSS 源地址：
```python
new_feeds = [
    ('Feed Name', 'https://example.com/feed.xml'),
]
```

### Telegram 频道
编辑 `telegram_monitor.py`：
```python
CHANNELS = ['channel_name_1', 'channel_name_2']
```

### X 账号
编辑 `x_monitor.py`：
```python
MONITOR_URLS = [
    'https://x.com/username/status/123456789',
]
```

### Gmail 通讯
`newsletter_monitor.py` 使用 `gog` 命令行工具，请确保已正确配置：
```bash
gog gmail search 'newer_than:30d label:newsletter'
```

## 系统要求

- Python 3.8 及以上版本
- `feedparser` 库版本 >= 6.0.0
- `beautifulsoup4` 库版本 >= 4.12.0
- `requests` 库版本 >= 2.31.0
- `httpx` 库版本 >= 0.25.0

## 数据库

系统会创建三个 SQLite 数据库：
- `rss_db.db`：用于存储 RSS 文章
- `x_monitor.db`：用于存储 X/Twitter 数据
- `telegram_db.db`：用于存储 Telegram 帖子

## 使用场景

1. **内容创作**：为 X/Twitter 平台生成每日内容
2. **市场研究**：跟踪行业趋势
3. **竞争情报**：监控竞争对手
4. **个人品牌建设**：持续发布内容
5. **书籍写作**：整理每月的分析报告

## 作者信息

该项目为开源项目，可免费使用和修改。