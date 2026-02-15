---
name: review-summarizer
description: 从多个平台（如 Amazon、Google、Yelp、TripAdvisor）抓取、分析并汇总产品评论。提取关键信息、情感分析结果、产品的优缺点以及用户推荐。这些数据可用于产品研究（例如进行套利）、创建联盟营销内容或辅助购买决策。
---

# 评论摘要工具

## 概述

该工具能够自动从多个平台抓取并分析产品评论，提取有价值的洞察信息。生成的摘要包含情感分析、优缺点识别以及基于数据的推荐结果。

## 核心功能

### 1. 多平台评论抓取

**支持的平台：**
- 亚马逊（产品评论）
- 谷歌（地图、购物）
- Yelp（商家和产品评论）
- TripAdvisor（酒店、餐厅、景点）
- 自定义平台（通过URL模式匹配）

**抓取选项：**
- 所有评论或特定时间范围
- 仅限已验证的购买记录
- 按评分（1-5星）筛选
- 包含图片和媒体文件
- 设置评论数量上限

### 2. 情感分析

**分析内容：**
- 总体情感得分（-1.0至+1.0）
- 情感分布（正面/中性/负面）
- 影响情感的主要因素（导致正面/负面评论的原因）
- 情感趋势（随时间的变化）
- 基于具体方面的分析（如电池寿命、质量、配送等）

### 3. 洞察提取

**自动识别：**
- 评论中提到的主要优点
- 常见的问题和缺点
- 用户的常见问题
- 产品的使用场景和应用方式
- 相关产品的竞争情况
- 针对特定功能的反馈

### 4. 摘要生成

**输出格式：**
- 执行摘要（150-200字）
- 按类别详细分类的总结
- 优缺点列表及出现频率
- 统计摘要（平均评分、评论数量等）
- 可导出的CSV文件（用于分析）
- 用于文档的Markdown格式报告

### 5. 推荐系统

**推荐依据：**
- 总体情感得分
- 评论数量和更新时间
- 已验证购买的比例
- 基于具体方面的评分
- 产品之间的竞争情况

## 快速入门

### 摘要亚马逊产品评论

```python
# Use scripts/scrape_reviews.py
python3 scripts/scrape_reviews.py \
  --url "https://amazon.com/product/dp/B0XXXXX" \
  --platform amazon \
  --max-reviews 100 \
  --output amazon_summary.md
```

### 比较多个平台的评论

```python
# Use scripts/compare_reviews.py
python3 scripts/compare_reviews.py \
  --product "Sony WH-1000XM5" \
  --platforms amazon,google,yelp \
  --output comparison_report.md
```

### 生成简短摘要

```python
# Use scripts/quick_summary.py
python3 scripts/quick_summary.py \
  --url "https://amazon.com/product/dp/B0XXXXX" \
  --brief \
  --output summary.txt
```

## 脚本

### `scrape_reviews.py`
从单个URL抓取并分析评论。

**参数：**
- `--url`：产品或商家评论的URL（必填）
- `--platform`：平台（亚马逊、谷歌、Yelp、TripAdvisor）（省略时自动检测）
- `--max-reviews`：要获取的最大评论数量（默认：100）
- `--verified-only`：仅限已验证的购买记录
- `--min-rating`：包含的最低评分（1-5星）
- `--time-range`：时间范围（7天、30天、90天、全部）（默认：全部）
- `--output`：输出文件（默认：summary.md）
- `--format`：输出格式（Markdown、JSON、CSV）

**示例：**
```bash
python3 scripts/scrape_reviews.py \
  --url "https://amazon.com/dp/B0XXXXX" \
  --platform amazon \
  --max-reviews 200 \
  --verified-only \
  --format markdown \
  --output product_summary.md
```

### `compare_reviews.py`
比较多个平台上的产品评论。

**参数：**
- `--product`：产品名称或关键词（必填）
- `--platforms`：用逗号分隔的平台（默认：全部）
- `--max-reviews`：每个平台的最大评论数量（默认：50）
- `--output`：输出文件
- `--format`：输出格式（Markdown、JSON）

**示例：**
```bash
python3 scripts/compare_reviews.py \
  --product "AirPods Pro 2" \
  --platforms amazon,google,yelp \
  --max-reviews 75 \
  --output comparison.md
```

### `sentiment_analysis.py`
分析评论文本的情感。

**参数：**
- `--input`：输入文件或文本（必填）
- `--type`：输入类型（文件、文本、URL）
- `--aspects`：要分析的具体方面（用逗号分隔）
- `--output`：输出文件

**示例：**
```bash
python3 scripts/sentiment_analysis.py \
  --input reviews.txt \
  --type file \
  --aspects battery,sound,quality \
  --output sentiment_report.md
```

### `quick_summary.py`
生成简短的执行摘要。

**参数：**
- `--url`：评论URL（必填）
- `--brief`：仅生成简短摘要（无详细分类）
- `--words`：摘要的字数（默认：150）
- `--output`：输出文件

**示例：**
```bash
python3 scripts/quick_summary.py \
  --url "https://yelp.com/biz/example-business" \
  --brief \
  --words 100 \
  --output summary.txt
```

### `export_data.py`
导出评论数据以供进一步分析。

**参数：**
- `--input`：摘要文件或JSON数据（必填）
- `--format`：输出格式（CSV、JSON、Excel）
- `--output`：输出文件

**示例：**
```bash
python3 scripts/export_data.py \
  --input product_summary.json \
  --format csv \
  --output reviews_data.csv
```

## 输出格式

### Markdown摘要结构

```markdown
# Product Review Summary: [Product Name]

## Overview
- **Platform:** Amazon
- **Reviews Analyzed:** 247
- **Average Rating:** 4.3/5.0
- **Overall Sentiment:** +0.72 (Positive)

## Key Insights

### Top Pros
1. Excellent sound quality (89 reviews)
2. Great battery life (76 reviews)
3. Comfortable fit (65 reviews)

### Top Cons
1. Expensive (34 reviews)
2. Connection issues (22 reviews)
3. Limited color options (18 reviews)

## Sentiment Analysis
- **Positive:** 78% (193 reviews)
- **Neutral:** 15% (37 reviews)
- **Negative:** 7% (17 reviews)

## Recommendation
✅ **Recommended** - Strong positive sentiment with high customer satisfaction.
```

## 最佳实践

### 用于套利研究
1. **跨平台比较**：对比亚马逊和eBay的卖家评分
2. **关注风险信号**：高退货率、质量投诉
3. **验证真实性**：仅使用已验证的购买记录
4. **分析趋势**：近期评论与旧评论的情感倾向

### 用于联盟营销内容
1. **提取真实用户反馈**：使用客户的实际评价
2. **了解使用场景**：用户如何使用该产品
3. **发现痛点**：产品解决的问题
4. **增强可信度**：利用大量评论的数据

### 用于购买决策
1. **查看近期评论**：最近30-90天的评论
2. **关注1星评论**：了解最糟糕的情况
3. **考虑自身需求**：确保产品功能符合你的使用场景
4. **比较替代产品**：使用`compare_reviews.py`进行比较

## 集成机会

### 与价格追踪工具集成
利用评论摘要验证套利机会：
```bash
# 1. Find arbitrage opportunity
price-tracker/scripts/compare_prices.py --keyword "Sony WH-1000XM5"

# 2. Validate with reviews
review-summarizer/scripts/scrape_reviews.py --url [amazon_url]
review-summarizer/scripts/scrape_reviews.py --url [ebay_url]

# 3. Make informed decision
```

### 与内容生成工具集成
根据评论洞察生成内容：
```bash
# 1. Summarize reviews
review-summarizer/scripts/scrape_reviews.py --url [amazon_url]

# 2. Use insights in article
seo-article-gen --keyword "[product name] review" --use-insights review_summary.json

# 3. Recycle across platforms
content-recycler/scripts/recycle_content.py --input article.md
```

## 自动化应用

### 周期性评论监控

```bash
# Monitor competitor products
0 9 * * 1 /path/to/review-summarizer/scripts/compare_reviews.py \
  --product "competitor-product" \
  --platforms amazon,google \
  --output /path/to/competitor_analysis.md
```

### 负面趋势警报

```bash
# Check for sentiment drops below threshold
if [ $(grep -o "Sentiment: -" summary.md | wc -l) -gt 0 ]; then
  echo "Negative sentiment alert" | mail -s "Review Alert" user@example.com
fi
```

## 数据隐私与伦理

- 仅抓取公开可用的评论
- 遵守robots.txt文件和平台的评分限制
- 不存储个人身份信息（PII）
- 统计数据，不暴露个别评论者的信息
- 遵守各平台的服务条款

## 限制

- 部分平台存在评分限制
- 无法获取所有平台的购买验证状态
- 假评论可能影响分析结果
- 不同平台的语言支持不同
- 有些平台禁止抓取评论

---

**基于数据做出决策。自动化研究流程。提升智能水平。**