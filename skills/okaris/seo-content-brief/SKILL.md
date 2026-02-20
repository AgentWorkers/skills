---
name: seo-content-brief
description: "**SEO内容简报的创建方法：包括关键词研究、搜索意图分析以及内容结构设计**  
本指南涵盖了以下关键内容：  
1. **SERP分析**（搜索引擎结果页面分析）  
2. **标题层级设计**  
3. **字数目标设定**  
4. **内部链接策略**  
适用场景：  
- 内容撰写计划  
- SEO策略制定  
- 博客内容规划  
- 关键词定位  
相关术语：  
- SEO内容简报（SEO Content Brief）  
- 关键词研究（Keyword Research）  
- 搜索意图分析（Search Intent Analysis）  
- 内容结构（Content Structure）  
- SERP（Search Engine Results Page）  
- 标题层级（Heading Hierarchy）  
- 字数目标（Word Count Goals）  
- 内部链接（Internal Links）  
**主要内容：**  
1. **关键词研究**：  
   - 如何识别目标受众的搜索关键词  
   - 关键词的相关性和竞争程度分析  
   - 选择适合网站内容的关键词  
2. **搜索意图分析**：  
   - 理解用户搜索关键词的真正意图  
   - 根据搜索意图优化内容  
3. **内容结构设计**：  
   - 明确文章的逻辑结构和段落划分  
   - 使用有效的标题和子标题来引导读者阅读  
4. **SERP分析**：  
   - 分析关键词在搜索结果页面上的表现  
   - 了解用户对相关内容的偏好  
5. **标题层级**：  
   - 设计吸引人的标题（H1、H2、H3等）  
   - 确保标题与内容紧密相关  
6. **字数目标**：  
   - 根据搜索引擎算法和用户阅读习惯设定合适的字数  
7. **内部链接策略**：  
   - 在网站内部创建合理的链接结构  
   - 通过内部链接提高页面的权重和可访问性  
**使用建议：**  
- 将本指南作为内容创作和SEO策略制定的参考工具  
- 定期更新和维护相关数据和策略  
**触发词：**  
- SEO内容简报（SEO Content Brief）  
- 关键词研究（Keyword Research）  
- 搜索意图分析（Search Intent Analysis）  
- 内容策略（Content Strategy）  
- 博客内容规划（Blog Content Planning）  
- 关键词定位（Keyword Targeting）  
- SERP分析（SERP Analysis）  
- 内容大纲（Content Outline）  
- SEO文章（SEO Article）  
- 博客SEO（Blog SEO）"
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

> **安装说明：** [安装脚本](https://cli.inference.sh)仅会检测您的操作系统/架构，从`dist.inference.sh`下载相应的二进制文件，并验证其SHA-256校验和。无需提升权限或后台进程。也可[手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

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
| **信息性** | 了解某事物 | 指南、教程、解释性文章 | “什么是CI/CD” |
| **商业性** | 购买前比较 | 对比文章、列表文章、评测 | “2024年最佳CI/CD工具” |
| **交易性** | 购买/注册 | 产品页面、价格页面 | “GitHub Actions的价格” |
| **导航性** | 查找特定页面 | —（不针对此类型） | “GitHub登录” |

**根据搜索意图选择合适的格式。** 如果搜索结果前10条都是列表文章，就写一篇列表文章；如果是教程，就写一篇教程。与搜索引擎的展示格式不符会导致排名下降。

## 搜索引擎结果页面（SERP）分析过程

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

### 从搜索结果中提取哪些信息

| 数据点 | 原因 |
|-----------|-----|
| **字数** | 确定您的最低字数要求（至少达到排名前三的文章的字数） |
| **标题结构** | 显示谷歌认为的完整覆盖范围 |
| **涵盖的主题** | 搜索结果涵盖的所有主题都必须包含在您的内容中 |
| **遗漏的主题** | 这是您提供更全面内容的机会 |
| **内容格式** | 列表文章、指南、教程、对比文章 |
| **使用的媒体** | 图片、视频、表格、信息图 |
| **内部/外部链接** | 用于评估内容质量的参考信号 |

## 关键词研究

### 关键词指标

| 指标 | 含义 | 目标 |
|--------|--------------|--------|
| **搜索量** | 每月的搜索次数 | 取决于领域（长尾关键词可能需要更多搜索量） |
| **关键词难度** | 竞争程度 | 新网站<30，成熟网站<50 |
| **点击成本（CPC）** | 广告商的出价 | CPC越高，商业价值越大 |
| **搜索意图** | 用户的需求 | 必须与您的内容类型相匹配 |

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

将相关的关键词组合成一篇内容：

```
Primary: "best project management tools for small teams"
Cluster:
  - "project management software small business"
  - "project management tools comparison"
  - "simple project management app"
  - "project management for startups"
  - "affordable project management software"
```

**每个关键词集群对应一个页面。** 不要为每个关键词变体创建单独的页面，否则会导致关键词竞争（即“关键词 cannibalization”现象）。

## 标题结构

### 规则

| 规则 | 原因 |
|------|-----|
| 每页一个H1标题 | SEO标准，包含主要关键词 |
| H2标题作为主要章节 | 每个H2标题应针对一个次要关键词或问题 |
| H3标题作为子章节 | 分割较长的H2内容 |
| H1标题中包含主要关键词 | 直接影响排名 |
| H2标题中包含次要关键词 | 体现内容的主题相关性 |
| 一些H2标题采用问答形式 | 有助于吸引“人们也想知道”的内容 |
| 逻辑层次结构 | 不能跳过标题级别（例如：H1 → H3，中间必须有H2） |

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

| 内容类型 | 字数要求 | 适用场景 |
|-------------|-----------|------|
| 简短博客 | 800-1,200字 | 新闻、更新、观点分享 |
| 标准博客 | 1,500-2,000字 | 操作指南、教程 |
| 长篇指南 | 2,500-4,000字 | 综合性指南、对比分析 |
| 专题内容 | 4,000-7,000字 | 权威指南、中心页面 |
| 术语表/定义 | 300-800字 | 快速参考 |

**规则：** 字数应达到排名前三的文章的平均字数。不要为了凑字数而添加无意义的内容。**

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
| **结构化数据标记** | 根据内容类型使用FAQ、HowTo或Article结构化数据标记 |

## 内容差异化

### 独特的角度

| 方法 | 示例 |
|-------|---------|
| **原始数据** | “我们调查了500位产品经理——这是他们的使用情况” |
| **专家引语** | 采访专业人士以获取独到见解 |
| **真实案例** | 屏幕截图、案例研究，而不仅仅是描述 |
| **更全面的内容** | 涵盖竞争对手未涉及的分支主题 |
| **更时效性的内容** | 最新数据、最新工具、最新变化 |
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
| **中心页面 → 分支页面** | 专题页面链接到所有相关文章 |
| **分支页面 → 中心页面** | 分支页面链接回中心页面 |
| **分支页面之间** | 相关文章相互链接 |
| **上下文相关的链接** | 在提到相关主题时自然插入链接 |

### 规则

- 每篇文章至少包含3-5个内部链接 |
- 链接文本应具有描述性（不要使用“点击这里”这样的通用文本）
- 链接到相关页面，而非随机页面 |
- 更新旧文章以添加新内容的链接 |
- 最重要的页面应拥有最多的内部链接

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 未进行SERP分析 | 盲目写作，格式错误 | 写作前务必分析排名前三的文章 |
| 错误的意图匹配 | 本应提供对比的内容却写成了指南，反之亦然 | 确保内容格式与SERP结果一致 |
| 关键词堆砌 | 会被搜索引擎处罚，阅读体验差 | 自然地使用关键词，密度控制在1-2% |
| 忽视“人们也想知道”的问题 | 会错过容易获得排名的机会 | 在内容中回答这些问题 |
| 内容太短 | 无法与内容全面的文章竞争 | 字数应达到排名前三的文章水平 |
| 缺乏独特角度 | 内容千篇一律 | 使用原始数据、专家引语、更好的视觉效果 |
| 关键词竞争 | 多个页面重复相同内容 | 每个关键词集群对应一个页面 |
| 无内部链接 | 链接效果不佳，网站结构混乱 | 每篇文章至少包含3-5个内部链接 |
| 缺少元描述 | Google会自动生成元描述（但可能不够准确） | 自己编写包含关键词和行动号召的吸引人元描述 |

## 相关技能

```bash
npx skills add inference-sh/skills@seo
npx skills add inference-sh/skills@technical-blog-writing
npx skills add inference-sh/skills@web-search
```

浏览所有应用程序：`infsh app list`