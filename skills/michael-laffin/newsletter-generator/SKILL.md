---
name: newsletter-generator
description: 生成包含精选内容、联盟链接以及个性化推荐的自动化电子邮件通讯。适用于创建每日/每周通讯、建立邮件列表，或通过联盟内容实现订阅者参与度的货币化。
---

# 新闻通讯生成器

## 概述

通过精选内容、联盟营销和个人化推荐，自动化生成电子邮件新闻通讯。大规模构建并变现电子邮件列表。

## 核心功能

### 1. 内容精选

- **自动执行：**
  - 精选热门文章和博客帖子
  - 根据关键词/主题查找相关内容
  - 提取关键点和摘要
  - 按主题对内容进行分类（技术、营销、生活方式等）
  - 过滤内容的质量和相关性

### 2. 新闻通讯模板

- **预建的模板包括：**
  - 每日摘要（5-10个链接，简短摘要）
  - 周度汇总（深入分析，精选文章）
  - 行业新闻（以新闻为主，时效性强）
  - 教程系列（教育性内容，分步指导）
  - 产品推荐（包含联盟链接，可变现）

### 3. 联盟营销集成

- **自动包含：**
  - 与内容相关的联盟链接
  - 与新闻通讯主题匹配的产品推荐
  - 符合FTC（美国联邦贸易委员会）规定的披露信息
  - 可追踪的链接用于数据分析
  - 根据用户互动情况优化收入

### 4. 个性化

- **个性化设置：**
  - 订阅者分组
  - 过往互动数据
  - 适合的发送时间（考虑时区）
  - 自定义发件人信息
  - 根据偏好动态生成内容

### 5. 数据分析与优化

- **跟踪和优化：**
  - 开启率和点击率
  - 联盟链接的效果
  - 订阅者增长和流失情况
  - 最受欢迎的内容类型
  - 最佳发送时间

## 快速入门

### 生成每日摘要

```python
# Use scripts/generate_newsletter.py
python3 scripts/generate_newsletter.py \
  --type daily \
  --topic marketing \
  --articles 10 \
  --affiliate-links 3 \
  --output newsletter.md
```

### 生成每周汇总

```python
python3 scripts/generate_newsletter.py \
  --type weekly \
  --topic tech \
  --articles 20 \
  --include-tutorials \
  --include-products \
  --output weekly.md
```

### 从RSS源精选内容

```python
# Use scripts/curate_content.py
python3 scripts/curate_content.py \
  --rss-feeds https://feeds.feedburner.com/example1,https://example2.com/feed \
  --keywords marketing,seo,content \
  --articles 10 \
  --output curated_content.json
```

## 脚本

### `generate_newsletter.py`
从精选内容生成新闻通讯。

**参数：**
- `--type`：新闻通讯类型（每日、每周、每月、汇总、产品推荐）
- `--topic`：主要主题
- `--articles`：包含的文章数量
- `--affiliate-links`：包含的联盟链接数量
- `--include-tutorials`：是否包含教育性内容
- `--include-products`：是否包含产品推荐
- `--tone`：新闻通讯的语气（专业、随意、轻松）
- `--output`：输出文件

**示例：**
```bash
python3 scripts/generate_newsletter.py \
  --type daily \
  --topic digital-marketing \
  --articles 8 \
  --affiliate-links 3 \
  --tone conversational \
  --output newsletter.md
```

### `curate_content.py`
从RSS源或URL中精选内容。

**参数：**
- `--rss-feeds`：逗号分隔的RSS源URL
- `--keywords`：按关键词过滤
- `--max-articles`：精选的最大文章数量
- `--min-relevance`：最低相关性得分（0-1）
- `--output`：输出JSON文件

**示例：**
```bash
python3 scripts/curate_content.py \
  --rss-feeds https://blog.example.com/feed,https://news.example.com/rss \
  --keywords "marketing,seo,growth" \
  --max-articles 15 \
  --output curated.json
```

### `add_affiliate_links.py`
向现有新闻通讯中添加联盟链接。

**参数：**
- `--input`：新闻通讯文件
- `--network`：联盟营销网络（亚马逊、ShareASale、CJ、Impact）
- `--links`：要添加的链接数量
- `--disclosure-position`：披露位置（顶部、底部、内联）

**示例：**
```bash
python3 scripts/add_affiliate_links.py \
  --input newsletter.md \
  --network amazon \
  --links 5 \
  --disclosure-position top
```

### `schedule_newsletter.py`
安排新闻通讯的发送时间（生成发送计划）。

**参数：**
- `--newsletter`：新闻通讯文件
- `--send-time`：最佳发送时间
- `--timezone`：订阅者的时区
- `--segments`：订阅者分组
- `--output`：用于电子邮件服务提供商（ESP）的发送计划文件

**示例：**
```bash
python3 scripts/schedule_newsletter.py \
  --newsletter newsletter.md \
  --send-time "09:00" \
  --timezone "America/Chicago" \
  --output schedule.json
```

### `analytics_report.py`
生成分析报告和优化建议。

**参数：**
- `--metrics-file`：来自ESP的指标数据
- `--period`：时间周期（7天、30天、90天）
- `--output`：报告文件

## 新闻通讯模板

### 每日摘要模板

```
Subject: [Topic] Daily Digest - [Date]

---

## Today's Top Stories

[Article 1 Title]
[Summary]
[Read more →] [Affiliate Link if applicable]

[Article 2 Title]
[Summary]
[Read more →]

...

## Quick Tip
[Brief actionable tip with affiliate link]

## Featured Resource
[Product/Tool recommendation]
[Brief description]
[Get it here →] [Affiliate Link]

---

[FTC Disclosure]
```

### 周度汇总模板

```
Subject: [Topic] Weekly Roundup - Top [N] Stories

---

## This Week's Highlights

[Deep Dive Article 1]
[Comprehensive summary]
[Read the full article →]

[Deep Dive Article 2]
[Comprehensive summary]
[Read the full article →]

## Tutorial Corner
[Step-by-step tutorial]
[Product recommendations with affiliate links]

## Industry News
[3-5 key news stories]
[Brief updates]

## Recommended Resources
[Product recommendations with affiliate links]

---

[FTC Disclosure]
```

## 最佳实践

### 主题行
- 保持50个字符以内，以便在移动设备上显示
- 使用数字和括号（例如 [每日摘要]、[每周]
- 包含紧迫感或好奇心元素
- 对不同的主题行进行A/B测试

### 内容平衡
- 70% 有价值的内容（教育性内容）
- 20% 精选内容（他人的文章）
- 10% 促销内容（联盟链接/销售信息）

### 联盟链接
- 每封新闻通讯包含1-3个链接
- 与内容相关联
- 在顶部明确标注披露信息
- 可追踪的链接用于数据分析

### 发送时间
- **B2B**：周二至周四，上午9-11点
- **B2C**：周末，下午6-8点
- **普通新闻通讯**：周二/周三，上午8-10点
- **促销邮件**：周一或周五

## 自动化流程

### 每日新闻通讯生成

```bash
# Generate daily newsletter at 8 AM
0 8 * * * /path/to/newsletter-generator/scripts/generate_newsletter.py \
  --type daily \
  --topic tech \
  --articles 10 \
  --affiliate-links 3 \
  --output /path/to/newsletters/daily_$(date +\%Y\%m\%d).md
```

### 周度汇总

```bash
# Generate weekly newsletter every Sunday at 9 AM
0 9 * * 0 /path/to/newsletter-generator/scripts/generate_newsletter.py \
  --type weekly \
  --topic marketing \
  --articles 20 \
  --include-tutorials \
  --output /path/to/newsletters/weekly_$(date +\%Y\%m\%d).md
```

## 集成机会

### 与内容回收工具集成
```bash
# 1. Recycle article to newsletter format
content-recycler/scripts/recycle_content.py \
  --input article.md \
  --platforms email

# 2. Add affiliate links
newsletter-generator/scripts/add_affiliate_links.py \
  --input email_version.md
```

### 与SEO文章生成工具集成
```bash
# 1. Generate SEO article
seo-article-gen --keyword "newsletter topic"

# 2. Curate related content
newsletter-generator/scripts/curate_content.py --keywords "newsletter topic"

# 3. Generate newsletter
newsletter-generator/scripts/generate_newsletter.py
```

## 收入影响

**电子邮件营销统计数据：**
- 平均打开率：20-30%
- 平均点击率：2-5%
- 联盟营销转化率：1-3%
- 每1000名订阅者的收入：50-500美元/月

**扩展潜力：**
- 每天发送1封新闻通讯 × 1000名订阅者 = 每天50-500美元
- 每周发送1封新闻通讯 × 10,000名订阅者 = 每周500-5,000美元

---

**构建您的订阅列表。自动变现。轻松扩展。**