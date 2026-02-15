---
name: seo-content-brief
description: |
  SEO content brief creation with keyword research, search intent analysis, and content structure.
  Covers SERP analysis, heading hierarchy, word count targets, and internal linking strategy.
  Use for: content briefs, SEO writing, blog strategy, content planning, keyword targeting.
  Triggers: seo content brief, content brief, seo brief, keyword research, search intent,
  content strategy, blog brief, seo writing, content planning, keyword targeting,
  serp analysis, content outline, seo article, blog seo
allowed-tools: Bash(infsh *)
---

# SEO内容简报

通过[inference.sh](https://inference.sh)命令行工具创建基于数据的内容简报。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Research target keyword
infsh app run tavily/search-assistant --input '{
  "query": "best project management tools for small teams 2024"
}'

# Analyze top-ranking content
infsh app run exa/search --input '{
  "query": "project management tools small teams comparison guide"
}'
```

## 内容简报模板

在开始编写之前，每个内容简报都应回答以下问题：

```markdown
# Content Brief: [Working Title]

## Target
- **Primary keyword:** [exact keyword]
- **Secondary keywords:** [3-5 related terms]
- **Search intent:** [informational / commercial / transactional / navigational]
- **Target word count:** [X,XXX words]
- **Target URL:** /blog/[slug]

## Search Intent Analysis
- What is the searcher trying to accomplish?
- What format do top results use? (listicle, guide, comparison, tutorial)
- What questions need answering?

## Outline
H1: [Title with primary keyword]
  H2: [Section 1]
    H3: [Subsection]
  H2: [Section 2]
  ...

## Competitors to Beat
1. [URL] — [word count] — [what they do well] — [gap/weakness]
2. [URL] — [word count] — [what they do well] — [gap/weakness]
3. [URL] — [word count] — [what they do well] — [gap/weakness]

## Unique Angle
What makes this piece different/better than what already ranks?

## Internal Links
- Link TO: [existing pages to link to from this article]
- Link FROM: [existing pages that should link to this new article]
```

## 搜索意图类型

| 意图 | 搜索者需求 | 内容格式 | 示例查询 |
|--------|-------------------|----------------|--------------|
| **信息型** | 了解某事物 | 教程、解释性文章 | “什么是CI/CD” |
| **商业型** | 购买前比较 | 对比文章、列表文章、评测 | “2024年最佳CI/CD工具” |
| **交易型** | 购买/注册 | 产品页面、价格页面 | “GitHub Actions的价格” |
| **导航型** | 查找特定页面 | —（无需针对此类意图） | “GitHub登录” |

**根据搜索意图选择合适的格式。** 如果排名前10的结果都是列表文章，就写列表文章；如果是教程，就写教程。违背搜索结果页面（SERP）的格式会适得其反。

## SERP分析流程

```bash
# Step 1: See what currently ranks
infsh app run tavily/search-assistant --input '{
  "query": "[your target keyword]"
}'

# Step 2: Analyze top-ranking content
infsh app run tavily/extract --input '{
  "urls": ["https://top-result-1.com/article", "https://top-result-2.com/article"]
}'

# Step 3: Find related questions (People Also Ask)
infsh app run tavily/search-assistant --input '{
  "query": "[keyword] questions people ask FAQ"
}'

# Step 4: Find content gaps
infsh app run exa/search --input '{
  "query": "[keyword] [subtopic competitors miss]"
}'
```

### 从排名结果中提取哪些信息

| 数据点 | 原因 |
|-----------|-----|
| **字数** | 确定你的最低字数要求（至少达到排名前三的结果的字数） |
| **标题结构** | 显示Google认为哪些内容是完整的 |
| **涵盖的主题** | 他们涵盖的所有主题，你都必须涵盖 |
| **遗漏的主题** | 你可以借此机会提供更全面的内容 |
| **内容格式** | 列表文章、指南、教程、对比文章 |
| **使用的媒体** | 图片、视频、表格、信息图 |
| **内部/外部链接** | 用于评估内容质量的信号 |

## 关键词研究

### 关键词指标

| 指标 | 含义 | 目标 |
|--------|--------------|--------|
| **搜索量** | 每月的搜索次数 | 取决于领域（长尾关键词可能需要超过100次搜索量） |
| **关键词难度** | 竞争程度 | 新网站<30，成熟网站<50 |
| **CPC** | 广告商的出价 | CPC越高，商业价值越大 |
| **搜索意图** | 用户的需求 | 必须与你的内容类型相匹配 |

### 寻找关键词

```bash
# Seed keyword research
infsh app run tavily/search-assistant --input '{
  "query": "project management software long tail keywords related searches"
}'

# Find question-based keywords
infsh app run exa/search --input '{
  "query": "questions about project management tools for startups"
}'

# Competitor keyword analysis
infsh app run tavily/search-assistant --input '{
  "query": "site:competitor.com/blog top performing pages topics"
}'
```

### 关键词聚类

将相关的关键词归类到同一篇文章中：

```
Primary: "best project management tools for small teams"
Cluster:
  - "project management software small business"
  - "project management tools comparison"
  - "simple project management app"
  - "project management for startups"
  - "affordable project management software"
```

**每个关键词簇对应一个页面。** 不要为每个关键词变体创建单独的页面，否则会导致关键词之间的竞争（即“关键词 cannibalization”现象）。

## 标题结构

### 规则

| 规则 | 原因 |
|------|-----|
| 每页一个H1标题 | SEO标准，包含主要关键词 |
| H2标题作为主要章节 | 每个H2标题应针对一个次要关键词或问题 |
| H3标题作为子章节 | 用于细分较长的H2章节 |
| H1标题中包含主要关键词 | 直接影响排名 |
| H2标题中包含次要关键词 | 体现内容的主题相关性 |
| 一些H2标题采用问答形式 | 有助于吸引“人们也想知道”的内容 |
| 保持逻辑层次结构 | 不能跳过标题层级（例如：H1 → H3，不能缺少H2）

### 示例结构

```
H1: Best Project Management Tools for Small Teams (2025)
  H2: How We Evaluated These Tools
  H2: Top 10 Project Management Tools Compared
    H3: 1. Tool A — Best for [use case]
    H3: 2. Tool B — Best for [use case]
    ...
  H2: Feature Comparison Table
  H2: How to Choose the Right Tool for Your Team
    H3: Team Size Considerations
    H3: Budget Considerations
  H2: Frequently Asked Questions
    H3: What is the easiest project management tool?
    H3: Do small teams need project management software?
  H2: Conclusion
```

## 字数目标

| 内容类型 | 字数 | 适用场景 |
|-------------|-----------|------|
| 简短博客 | 800-1,200字 | 新闻、更新、观点分享 |
| 标准博客 | 1,500-2,000字 | 教程、操作指南 |
| 长篇指南 | 2,500-4,000字 | 综合性指南、对比分析 |
| 专题内容 | 4,000-7,000字 | 详尽的指南、专题页面 |
| 术语表/定义 | 300-800字 | 快速参考 |

**规则：** 字数应达到或超过排名前三的结果的平均字数。不要为了凑字数而添加无意义的文字。

## 页面内SEO检查清单

| 元素 | 规则 |
|---------|------|
| **标题标签** | 包含主要关键词和吸引人的开头，50-60个字符 |
| **元描述** | 包含关键词，150-160个字符，并包含行动号召（CTA） |
| **URL路径** | 简短且富含关键词：`/best-project-management-tools` |
| **H1标题** | 包含主要关键词，符合搜索意图 |
| **前100个单词** | 自然地包含主要关键词 |
| **图片alt文本** | 描述性文本，适当位置包含关键词 |
| **内部链接** | 3-5个指向相关内容的链接 |
| **外部链接** | 2-3个权威来源的链接 |
| **schema标记** | 在适用的情况下添加FAQ、HowTo或Article的schema标签 |

## 内容差异化

### 独特的角度

| 角度 | 示例 |
|-------|---------|
| **原始数据** | “我们调查了500名产品经理——以下是他们使用的工具” |
| **专家引语** | 采访专业人士以获取独到见解 |
| **真实案例** | 屏幕截图、案例研究，而不仅仅是描述 |
| **更全面的内容** | 涵盖竞争对手忽略的子主题 |
| **更及时的内容** | 最新的数据、最新的工具、最近的变化 |
| **更好的视觉效果** | 对比表格、信息图、决策树 |

```bash
# Generate comparison infographic
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:800px;background:white;padding:40px;font-family:system-ui\"><h2 style=\"font-size:28px;color:#1e293b;text-align:center;margin-bottom:30px\">Project Management Tools Comparison</h2><table style=\"width:100%;border-collapse:collapse;font-size:16px\"><tr style=\"background:#f1f5f9\"><th style=\"padding:12px;text-align:left;border-bottom:2px solid #cbd5e1\">Feature</th><th style=\"padding:12px;text-align:center;border-bottom:2px solid #cbd5e1\">Tool A</th><th style=\"padding:12px;text-align:center;border-bottom:2px solid #cbd5e1\">Tool B</th><th style=\"padding:12px;text-align:center;border-bottom:2px solid #cbd5e1\">Tool C</th></tr><tr><td style=\"padding:12px;border-bottom:1px solid #e2e8f0\">Free tier</td><td style=\"padding:12px;text-align:center;border-bottom:1px solid #e2e8f0\">✅</td><td style=\"padding:12px;text-align:center;border-bottom:1px solid #e2e8f0\">✅</td><td style=\"padding:12px;text-align:center;border-bottom:1px solid #e2e8f0\">❌</td></tr></table></div>"
}'
```

## 内部链接策略

| 类型 | 目的 |
|------|---------|
| **专题页面 → 子主题页面** | 专题页面链接到所有子主题文章 |
| **子主题页面 → 专题页面** | 子主题文章链接回专题页面 |
| **相关文章之间的链接** | 相关文章之间互相链接 |
| **上下文相关的链接** | 在提到相关主题时自然地添加链接 |

### 规则

- 每篇文章至少包含3-5个内部链接 |
- 链接文本应具有描述性（不要使用“点击这里”这样的通用文本） |
- 链接到相关页面，而不是随意的链接 |
- 更新旧文章以添加新的链接 |
- 最重要的页面应拥有最多的内部链接

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 未进行SERP分析 | 盲目写作，格式错误 | 写作前务必分析排名前三的结果 |
| 错误的意图匹配 | 本应提供对比内容却写了教程，反之亦然 | 确保内容格式与搜索结果页面一致 |
| 关键词堆砌 | 会被惩罚，阅读体验差 | 自然地使用关键词，密度控制在1-2% |
| 忽略“人们也想知道”的问题 | 会错过容易获得的排名机会 | 在内容中回答这些问题 |
| 文章太短 | 无法与内容全面的结果竞争 | 字数应达到或超过排名前三的结果 |
| 没有独特角度 | 变成另一篇普通的文章 | 使用原始数据、专家引语、更好的视觉效果 |
| 关键词竞争 | 多个页面争夺同一个关键词 | 每个关键词簇对应一个页面 |
| 没有内部链接 | 错误地浪费了链接资源，导致网站结构不佳 | 每篇文章至少包含3-5个内部链接 |
| 缺少元描述 | Google会自动生成元描述（但质量可能不佳） | 自己编写包含关键词和行动号召的吸引人元描述 |

## 相关技能

```bash
npx skills add inferencesh/skills@seo
npx skills add inferencesh/skills@technical-blog-writing
npx skills add inferencesh/skills@web-search
```

浏览所有应用程序：`infsh app list`