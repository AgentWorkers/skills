---
name: social-sentiment
description: "针对Twitter、Reddit和Instagram上的品牌及产品进行情感分析。监控公众舆论，追踪品牌声誉，及时发现公关危机，大规模识别用户的投诉与赞扬——支持分析超过7万条帖子，并提供批量CSV导出功能，同时兼容Python和pandas编程语言。该服务基于超过15亿条已索引的帖子数据，提供高效的社会舆论监测与品牌监控功能。"
homepage: https://xpoz.ai
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["mcporter"],
            "skills": ["xpoz-setup"],
            "network": ["mcp.xpoz.ai"],
            "credentials": "Xpoz account (free tier) — auth via xpoz-setup skill (OAuth 2.1)",
          },
      },
  }
tags:
  - sentiment-analysis
  - brand-monitoring
  - social-media
  - twitter
  - reddit
  - instagram
  - analytics
  - brand-sentiment
  - reputation
  - social-listening
  - opinion-mining
  - brand-tracking
  - competitor-analysis
  - public-opinion
  - crisis-detection
  - NLP
  - reputation
  - mcp
  - xpoz
  - opinion
  - market-research
---

# 社交情感分析

**从人们在社交媒体上的真实言论中了解他们的真实想法。**

您可以分析任何品牌、产品、话题或个人在 Twitter、Reddit 和 Instagram 上的情感倾向。该工具能够识别正面和负面的主题，标记出广为传播的投诉内容，比较不同品牌之间的舆论，并追踪舆论随时间的变化——这一切都依赖于 Xpoz MCP 提供的超过 15 亿条已索引的帖子数据。

**处理能力：** 通过批量 CSV 导出和自动化代码分析，每次分析可以处理数千到数万条帖子。这里提供的是完整的数据集，而非样本数据。

---

## ⚡ 先决条件

1. **必须配置并认证 Xpoz MCP**。请按照 [xpoz-setup](https://clawhub.ai/skills/xpoz-setup) 的说明进行设置。
   验证 Xpoz 是否已准备好：

```bash
mcporter call xpoz.checkAccessKeyStatus
```

如果 `hasAccessKey: false`，请先完成 xpoz-setup 的设置，然后再返回到这里。

---

## 工作原理

---

## 使用方法

### 基本用法：单一品牌/产品

> “分析 Notion 的情感倾向”
> “人们对 Cursor IDE 有什么看法？”
> “目前公众对特斯拉的看法如何？”

### 比较模式

> “比较 Notion 和 Obsidian 的情感倾向”
> “Figma 和 Canva 的情感倾向有何不同？”

### 话题/事件追踪

> “新款 iPhone 发布时的舆论如何？”
> “人们对 OpenAI 的最新公告有何反应？”

---

## 第一步：在所有平台上进行搜索

针对目标品牌/产品/话题，在这三个平台上同时进行搜索。

### 生成搜索查询

为每个平台创建 2-3 条查询，以覆盖不同的方面：

1. **直接提及** — 品牌/产品名称（最广泛的查询）
2. **痛点** — 抱怨、问题、不满（针对负面内容）
3. **正面评价** — 爱好、推荐、最佳、出色（针对正面内容）

**以 “Notion” 为例：**
- `"Notion"`（直接提及 — 这是主要的高量查询）
- `"Notion" AND (slow OR buggy OR frustrating OR hate OR terrible OR worst OR broken)`（负面）
- `"Notion" AND (love OR amazing OR best OR recommend OR perfect OR great)`（正面）

### Twitter

```bash
mcporter call xpoz.getTwitterPostsByKeywords \
  query='"BRAND_NAME"' \
  startDate="YYYY-MM-DD" \
  limit=100 \
  fields='["id","text","authorUsername","likeCount","retweetCount","replyCount","impressionCount","createdAtDate"]'
```

**重要提示：** 必须持续获取结果：

```bash
mcporter call xpoz.checkOperationStatus operationId="OPERATION_ID"
```

每 5 秒查询一次，直到查询状态变为 `completed`。

### Reddit

```bash
mcporter call xpoz.getRedditPostsByKeywords \
  query='"BRAND_NAME"' \
  startDate="YYYY-MM-DD" \
  limit=100
```

### Instagram

```bash
mcporter call xpoz.getInstagramPostsByKeywords \
  query='"BRAND_NAME"' \
  startDate="YYYY-MM-DD" \
  limit=100 \
  fields='["id","caption","username","likeCount","commentCount","createdAtDate"]'
```

### 默认时间范围

- 除非用户另有指定，否则使用 **过去 30 天** 的数据
- 对于事件或新产品发布，需缩小时间范围

---

## 第二步：批量下载 CSV 数据（至关重要，切勿跳过）

**这正是该工具强大的关键所在。** 每次 Xpoz 搜索都会在响应中返回一个 `dataDumpExportOperationId`。该 ID 可用于下载完整的结果集（每个查询最多 64,000 行）。

**切勿仅读取 API 响应中的前 100 条结果就认为分析完成。** 那只是抽样，并非真正的分析。请下载完整的 CSV 数据。

### 如何获取 CSV 数据

1. 每次搜索完成后，记录响应中的 `dataDumpExportOperationId`。
2. 持续查询，直到 CSV 数据下载完成：

```bash
mcporter call xpoz.checkOperationStatus operationId="op_datadump_XXXXX"
```

3. 下载完成后，您将获得一个 `downloadUrl`，请使用该链接下载数据：

```bash
curl -o /tmp/twitter-sentiment.csv "DOWNLOAD_URL"
```

4. 对每个平台的搜索结果重复此步骤。

### 下载的内容

每个 CSV 文件包含所有请求的字段：
- **Twitter CSV：** id, text, authorUsername, likeCount, retweetCount, replyCount, impressionCount, createdAtDate
- **Reddit CSV：** id, title, body, authorUsername, subredditName, score, numComments, createdAtDate
- **Instagram CSV：** id, caption, username, likeCount, commentCount, createdAtDate

### 数据量预估

| 品牌规模 | Twitter | Reddit | Instagram | 总计 |
|------------|---------|--------|-----------|-------|
| 小众产品 | 100-500 | 10-50 | 10-50 | ~200-600 |
| 中端工具 | 1K-10K | 50-500 | 50-200 | ~1K-10K |
| 大型品牌 | 10K-64K | 500-5K | 200-2K | ~10K-70K |

对于数据量非常大的品牌，可以缩小时间范围，以便在保持分析效果的同时控制数据集的大小。

---

## 第三步：使用代码进行大规模分析

**使用 Python 和 pandas 分析完整的 CSV 数据集。** 分析工作是通过自动化分类和汇总整个数据集来完成的，而不是逐条阅读帖子。

### 分析脚本

编写并执行一个 Python 脚本：

```python
import pandas as pd
import re
from collections import Counter

# Load all CSVs
twitter_df = pd.read_csv('/tmp/twitter-sentiment.csv')
reddit_df = pd.read_csv('/tmp/reddit-sentiment.csv')
instagram_df = pd.read_csv('/tmp/instagram-sentiment.csv')

# === SENTIMENT CLASSIFICATION ===
# Keyword-based classification (fast, works at scale)

POSITIVE_KEYWORDS = [
    'love', 'amazing', 'best', 'great', 'awesome', 'excellent', 'perfect',
    'recommend', 'incredible', 'fantastic', 'game changer', 'game-changer',
    'impressed', 'beautiful', 'brilliant', 'outstanding', 'favorite',
    'happy', 'excited', 'wonderful', 'solid', 'reliable', 'smooth',
    'intuitive', 'powerful', 'clean', 'fast', 'helpful', 'goat', 'fire',
    'lfg', 'must-have', 'must have', 'worth it', 'changed my life'
]

NEGATIVE_KEYWORDS = [
    'hate', 'terrible', 'worst', 'awful', 'horrible', 'broken', 'buggy',
    'slow', 'expensive', 'overpriced', 'frustrating', 'disappointed',
    'unusable', 'garbage', 'trash', 'scam', 'malware', 'insecure',
    'unsafe', 'security', 'vulnerability', 'leak', 'privacy', 'risky',
    'annoying', 'painful', 'nightmare', 'waste', 'regret', 'sucks',
    'god-awful', 'god awful', 'rip-off', 'don\'t use', 'do not use',
    'giving up', 'uninstalled', 'switched away', 'cancel'
]

def classify_sentiment(text):
    """Classify a post as positive, negative, neutral, or mixed."""
    if not isinstance(text, str):
        return 'neutral', 0
    text_lower = text.lower()
    pos_hits = sum(1 for kw in POSITIVE_KEYWORDS if kw in text_lower)
    neg_hits = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text_lower)
    
    if pos_hits > 0 and neg_hits > 0:
        return 'mixed', pos_hits - neg_hits
    elif pos_hits > 0:
        return 'positive', pos_hits
    elif neg_hits > 0:
        return 'negative', -neg_hits
    else:
        return 'neutral', 0

# Apply to Twitter
twitter_df['sentiment'], twitter_df['intensity'] = zip(
    *twitter_df['text'].apply(classify_sentiment)
)

# Apply to Reddit (use title + body if available)
reddit_text = reddit_df['title'].fillna('') + ' ' + reddit_df.get('body', pd.Series([''] * len(reddit_df))).fillna('')
reddit_df['sentiment'], reddit_df['intensity'] = zip(
    *reddit_text.apply(classify_sentiment)
)

# Apply to Instagram
instagram_df['sentiment'], instagram_df['intensity'] = zip(
    *instagram_df['caption'].apply(classify_sentiment)
)

# === ENGAGEMENT WEIGHTING ===
import numpy as np

# Twitter engagement score
twitter_df['engagement'] = (
    twitter_df.get('likeCount', 0).fillna(0) +
    twitter_df.get('retweetCount', 0).fillna(0) * 2 +
    twitter_df.get('replyCount', 0).fillna(0) * 1.5
)
twitter_df['weighted_score'] = twitter_df['intensity'] * np.log2(1 + twitter_df['engagement'])

# === AGGREGATE METRICS ===
for label, df in [('Twitter', twitter_df), ('Reddit', reddit_df), ('Instagram', instagram_df)]:
    total = len(df)
    pos = (df['sentiment'] == 'positive').sum()
    neg = (df['sentiment'] == 'negative').sum()
    neu = (df['sentiment'] == 'neutral').sum()
    mix = (df['sentiment'] == 'mixed').sum()
    print(f"\n=== {label} ({total} posts) ===")
    print(f"  Positive: {pos} ({pos/total*100:.1f}%)")
    print(f"  Negative: {neg} ({neg/total*100:.1f}%)")
    print(f"  Neutral:  {neu} ({neu/total*100:.1f}%)")
    print(f"  Mixed:    {mix} ({mix/total*100:.1f}%)")

# === THEME EXTRACTION ===
# Define theme keyword groups
THEMES = {
    'Performance / Speed': ['slow', 'fast', 'speed', 'performance', 'lag', 'loading'],
    'Pricing / Cost': ['expensive', 'cheap', 'price', 'pricing', 'cost', 'free', 'overpriced', 'afford', 'worth'],
    'Security': ['security', 'secure', 'unsafe', 'malware', 'vulnerability', 'privacy', 'leak', 'plaintext'],
    'Ease of Use / UX': ['intuitive', 'easy', 'simple', 'hard', 'difficult', 'confusing', 'ux', 'ui', 'clean'],
    'Setup / Installation': ['install', 'setup', 'set up', 'configure', 'getting started', 'onboarding'],
    'Features': ['feature', 'missing', 'need', 'wish', 'want', 'add', 'support'],
    'Customer Support': ['support', 'help', 'response', 'team', 'community'],
    'Reliability / Bugs': ['bug', 'crash', 'broken', 'error', 'issue', 'fix', 'stable', 'reliable'],
}

def extract_themes(text):
    if not isinstance(text, str):
        return []
    text_lower = text.lower()
    return [theme for theme, keywords in THEMES.items() if any(kw in text_lower for kw in keywords)]

# Apply to all datasets
all_posts = pd.concat([
    twitter_df[['text', 'sentiment', 'engagement']].rename(columns={'text': 'content'}).assign(platform='twitter'),
    reddit_df[['title', 'sentiment']].rename(columns={'title': 'content'}).assign(platform='reddit', engagement=0),
    instagram_df[['caption', 'sentiment']].rename(columns={'caption': 'content'}).assign(platform='instagram', engagement=0),
])
all_posts['themes'] = all_posts['content'].apply(extract_themes)

# Theme frequency by sentiment
from collections import defaultdict
theme_stats = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0, 'mixed': 0, 'total': 0})
for _, row in all_posts.iterrows():
    for theme in row['themes']:
        theme_stats[theme][row['sentiment']] += 1
        theme_stats[theme]['total'] += 1

print("\n=== THEMES ===")
for theme, stats in sorted(theme_stats.items(), key=lambda x: x[1]['total'], reverse=True):
    print(f"  {theme}: {stats['total']} mentions (pos={stats['positive']}, neg={stats['negative']}, neu={stats['neutral']})")

# === VIRAL FLAGS ===
# Posts with outsized engagement
if 'engagement' in twitter_df.columns:
    viral = twitter_df.nlargest(10, 'engagement')[['text', 'authorUsername', 'likeCount', 'retweetCount', 'impressionCount', 'sentiment']]
    print("\n=== TOP 10 VIRAL POSTS (Twitter) ===")
    for _, row in viral.iterrows():
        print(f"  [{row['sentiment'].upper()}] @{row['authorUsername']} — {row.get('likeCount',0)} likes, {row.get('impressionCount',0)} imp")
        print(f"    {str(row['text'])[:120]}...")

# === OVERALL SCORE ===
# Weighted by engagement: positive posts add, negative subtract, normalize to 0-100
pos_weight = twitter_df[twitter_df['sentiment'] == 'positive']['weighted_score'].sum()
neg_weight = twitter_df[twitter_df['sentiment'] == 'negative']['weighted_score'].abs().sum()
total_weight = pos_weight + neg_weight
if total_weight > 0:
    raw_score = (pos_weight - neg_weight) / total_weight  # -1 to 1
    normalized = int((raw_score + 1) * 50)  # 0 to 100
    print(f"\n=== OVERALL SCORE: {normalized}/100 ===")
```

### 关键分析原则：

1. **分析所有帖子，而非样本数据** — 这就是我们需要下载完整 CSV 数据的原因。
2. **基于关键词的分类更有效** — 逐一阅读 10,000 条帖子效果不佳；关键词匹配能提高效率。
3. **互动量很重要** — 获得 500 个赞的投诉与没有赞的投诉意义不同。
4. **通过关键词组提取主题** — 确定人们实际讨论的内容。
5. **通过互动量异常值检测热门帖子** — 标记出传播范围广的帖子。

### 自定义关键词列表

上面的 `POSITIVE_KEYWORDS`、`NEGATIVE_KEYWORDS` 和 `THEMES` 字典仅供参考。请根据具体品牌/产品进行定制：
- 对于 **游戏产品**：添加 “fun”、“addictive”、“boring”、“grind”、“pay to win” 等关键词。
- 对于 **SaaS 工具**：添加 “integration”、“API”、“downtime”、“onboarding” 等关键词。
- 对于 **消费品品牌**：添加 “quality”、“shipping”、“return”、“customer service” 等关键词。

### 脚本的输出结果

脚本会生成原始数据。您可以使用这些数据编写最终报告。大型语言模型（LLM）会解读数据、识别模式并生成可操作的见解。脚本负责处理大量的数据分析工作；而 LLM 则负责分析数据的实际含义。

---

## 第四步：生成报告

运行分析脚本后，将分析结果整理成结构化的报告。

### 报告结构

#### 1. 情感得分（标题数字）

```
Overall Sentiment: 72/100 (Mostly Positive)

Posts analyzed: 14,832 (not a sample — full dataset)

Breakdown:
  😊 Positive: 58% (8,603 posts)
  😠 Negative: 24% (3,560 posts)
  😐 Neutral:  18% (2,669 posts)

Platform breakdown:
  Twitter:   68/100 (12,400 posts analyzed)
  Reddit:    61/100 (1,932 posts analyzed)
  Instagram: 82/100 (500 posts analyzed)
```

**得分计算方法：**
- **基于互动量的加权得分：**(pos_weight - neg_weight) / total_weight**，范围为 0-100
- 0-30 = 非常负面，31-45 = 负面，46-55 = 中立，56-70 = 正面，71-100 = 非常正面

#### 2. 主要主题

按出现频率列出热门主题，并附上情感分析和代表性引文：

```
📈 POSITIVE THEMES

1. "Ease of Use" — 1,847 mentions (72% positive)
   Top posts by engagement:
   "Notion's database views just clicked for me. Game changer." — @user (234 likes)
   "Switched from Confluence to Notion and never looked back" — r/productivity (189 upvotes)

📉 NEGATIVE THEMES

1. "Performance / Speed" — 2,038 mentions (81% negative)
   Top posts by engagement:
   "Notion is unusable with large databases. 10+ second load times." — @dev (567 likes)
```

#### 3. 热门帖子

标记出在所有平台上互动量最高的 10 条帖子。每条帖子的信息包括：
- 情感分类
- 完整文本引文
- 互动量指标
- 发布平台及链接

#### 4. 最有影响力的账号

列出讨论该品牌的最具影响力的账号（根据其所有帖子的总互动量）：
- 账号名称、平台、粉丝数量（如果可用）
- 他们的整体立场（正面/负面/中性）
- 他们互动量最高的帖子

#### 5. 竞品对比（如需）

提供每个品牌的对比数据，使用相同的方法进行统计。

#### 6. 可操作的见解

根据分析结果提出 3-5 条建议：
- 哪些负面主题需要解决？
- 哪些正面主题需要加强宣传？
- 哪些热门帖子需要回应？
- 针对不同平台的策略建议

---

## 比较模式

在比较两个或多个品牌时：

1. 分别对每个品牌执行完整的分析流程。
2. 使用相同的时间范围、查询结构和关键词列表。
3. 下载每个品牌的 CSV 数据并运行相同的分析脚本。
4. 对比各品牌的分析结果。
5. 注意数据量的差异（提及次数多并不一定意味着情感倾向更好）。

---

## 定时任务（可选）

为了实现持续监控，用户可以设置定时任务：

```
"Run social sentiment analysis for [brand] weekly and email me the report"
```

您可以使用 OpenClaw 的定时任务功能来定期执行此分析任务。

---

## 数据存储

存储分析结果以追踪趋势：

```bash
mkdir -p data/social-sentiment
# Save CSVs and analysis results per run
# data/social-sentiment/{brand}-{date}-twitter.csv
# data/social-sentiment/{brand}-{date}-reddit.csv
# data/social-sentiment/{brand}-{date}-instagram.csv
# data/social-sentiment/{brand}-{date}-analysis.json
```

如果之前有分析记录，请在报告中添加 **趋势线**：

```
📈 TREND (last 4 weeks)
  Week 1: 68/100 (analyzed 12,400 posts)
  Week 2: 65/100 (analyzed 11,800 posts) ↓ pricing backlash
  Week 3: 70/100 (analyzed 13,200 posts) ↑ new feature launch
  Week 4: 72/100 (analyzed 14,832 posts) ↑ stabilizing
```

---

## 优化建议

- **下载完整 CSV 数据** — 切勿仅依赖 API 返回的前 100 条结果。CSV 数据才是分析的关键。
- **明确品牌名称** — 使用具体的品牌名称（例如 “Notion” 而不是 “notion app”），以避免误判。
- **避免歧义** — 如果品牌名称是通用词汇（如 “Slack”、“Rust”），请添加上下文信息。
- **自定义关键词列表** — 默认的正面/负面关键词仅供参考。请根据实际情况添加相关词汇。
- **Reddit 上的评论更真实** — 长篇评论往往包含用户的真实看法；Reddit 的社区文化更倾向于正面内容。
- **Instagram 的数据偏正面** — 该平台倾向于展示正面内容，请调整分析预期。
- **Twitter 反映实时反应** — 适用于追踪事件引发的情感变化和大量数据。
- **30 天的时间范围是最合适的** — 数据量足够分析趋势，同时也能反映最新情况。
- **对于数据量极大的品牌（超过 50,000 条帖子）** — 应缩小时间范围以避免数据过载。

---

## 负责任的使用方式

- 仅分析 **公开可见的** 社交媒体内容。
- 不得利用情感分析数据骚扰或针对个人。
- 如实呈现分析结果，避免选择性引用数据以误导他人。
- 在外部分享结果时公开说明分析方法。
- 需要尊重用户的隐私，理解公开帖子并不等于同意被大规模监控。

---

## 资源

- **Xpoz：** [xpoz.ai](https://xpoz.ai) — 提供社交智能分析功能的平台。
- **设置指南：** [ClawHub 上的 xpoz-setup](https://clawhub.ai/skills/xpoz-setup) — 一次性认证流程。
- **搜索参考：** [ClawHub 上的 xpoz-social-search](https://clawhub.ai/skills/xpoz-social-search) — 完整的查询模板。

**专为 ClawHub 开发 • 由 Xpoz 提供支持**