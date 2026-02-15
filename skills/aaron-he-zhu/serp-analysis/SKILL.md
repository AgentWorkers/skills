---
name: serp-analysis
description: 分析搜索引擎结果页面（SERPs），以了解排名因素、SERP页面的特点、用户意图模式以及与人工智能相关的触发条件。这对于理解影响页面排名的各种因素至关重要。
geo-relevance: "high"
---

# SERP分析

该技能用于分析搜索引擎结果页面（Search Engine Results Pages），以揭示哪些内容在排名中表现良好、哪些SERP功能会被展示出来，以及哪些因素会触发人工智能生成的答案。在创建内容之前，了解这些信息至关重要。

## 适用场景

- 在为目标关键词创建内容之前
- 了解为什么某些页面能够排在第1位
- 识别SERP功能的应用机会（如特色片段、PAA等）
- 分析人工智能生成的答案（AI Overview）的模式
- 更准确地评估关键词的难度
- 根据排名情况规划内容格式
- 确定特定查询的排名因素

## 功能概述

1. **SERP组成分析**：梳理结果页面上显示的所有元素
2. **排名因素识别**：分析顶级结果为何能够获得高排名
3. **SERP功能识别**：找出特色片段（Featured Snippet）、PAA（People Also Ask）等元素
4. **人工智能生成答案分析**：研究人工智能生成的答案何时以及如何出现
5. **用户意图检测**：从SERP的组成中判断用户的需求
6. **内容格式建议**：根据SERP的展示情况提供最佳内容格式建议
7. **难度评估**：评估内容的实际排名潜力

## 使用方法

### 基础SERP分析

```
Analyze the SERP for [keyword]
```

```
What does it take to rank for [keyword]?
```

### 特定功能分析

```
Analyze featured snippet opportunities for [keyword list]
```

```
Which of these keywords trigger AI Overviews? [keyword list]
```

### 竞争对手SERP分析

```
Why does [URL] rank #1 for [keyword]?
```

## 数据来源

> 有关工具的更多信息，请参阅 [CONNECTORS.md](../../CONNECTORS.md)。

**当连接了 ~~SEO工具 + ~~搜索控制台 + ~~人工智能监控工具时：**
可以自动获取目标关键词的SERP快照，提取排名页面的指标（如域名权威度、反向链接、内容长度），提取SERP功能数据，并使用 ~~人工智能监控工具** 检查是否存在人工智能生成的答案。还可以自动获取历史SERP变化数据以及移动设备与桌面设备上的显示差异。

**仅使用手动数据时：**
请用户提供以下信息：
1. 需要分析的目标关键词
2. SERP的截图或搜索结果的详细描述
3. 排名前10位的页面URL
4. 搜索位置和设备类型（移动设备/桌面设备）
5. 对SERP功能的任何观察结果（如特色片段、PAA等）

使用提供的数据进行完整分析。在输出结果中明确标注哪些数据来自自动化收集，哪些数据来自用户提供。

## 操作步骤

当用户请求SERP分析时：

1. **理解查询意图**
   如有需要，进一步确认：
   - 需要分析的目标关键词
   - 搜索位置/语言
   - 设备类型（移动设备/桌面设备）
   - 关于SERP的具体问题

2. **梳理SERP组成**
   记录结果页面上显示的所有元素：
   ```markdown
   ## SERP Analysis: "[keyword]"
   
   **Search Details**
   - Keyword: [keyword]
   - Location: [location]
   - Device: [mobile/desktop]
   - Date: [date]
   
   ### SERP Layout Overview
   
   ```
   ┌─────────────────────────────────────────┐
   │ [人工智能生成答案 / SGE] （如果存在）        │
   ├─────────────────────────────────────────┤
   │ [广告] - 屏幕上方有[X]条广告              │
   ├─────────────────────────────────────────┤
   │ [特色片段] （如果存在）         │
   ├─────────────────────────────────────────┤
   │ [自然搜索结果 #1]                     │
   │ [自然搜索结果 #2]                     │
   │ [用户也问] （如果存在）          │
   │ [自然搜索结果 #3]                     │
   │ ...                                     │
   ├─────────────────────────────────────────┤
   │ [相关搜索]                      │
   └─────────────────────────────────────────┘
   ```
   
   ### SERP Features Present
   
   | Feature | Present | Position | Opportunity |
   |---------|---------|----------|-------------|
   | AI Overview | Yes/No | Top | [analysis] |
   | Featured Snippet | Yes/No | [pos] | [analysis] |
   | People Also Ask | Yes/No | [pos] | [analysis] |
   | Knowledge Panel | Yes/No | Right | [analysis] |
   | Image Pack | Yes/No | [pos] | [analysis] |
   | Video Results | Yes/No | [pos] | [analysis] |
   | Local Pack | Yes/No | [pos] | [analysis] |
   | Shopping Results | Yes/No | [pos] | [analysis] |
   | News Results | Yes/No | [pos] | [analysis] |
   | Sitelinks | Yes/No | [pos] | [analysis] |
   ```

3. **分析排名靠前的页面**
   对于排名前10位的页面，进行详细分析：
   ```markdown
   ### Top 10 Organic Results Analysis
   
   #### Position #1: [Title]
   
   **URL**: [url]
   **Domain**: [domain]
   **Domain Authority**: [DA]
   
   **Content Analysis**:
   - Type: [Blog/Product/Guide/etc.]
   - Word Count: [X] words
   - Publish Date: [date]
   - Last Updated: [date]
   
   **On-Page Factors**:
   - Title: [exact title]
   - Title contains keyword: Yes/No
   - Meta description: [description]
   - H1: [heading]
   - URL structure: [clean/keyword-rich/etc.]
   
   **Content Structure**:
   - Headings (H2s): [list key sections]
   - Media: [X] images, [X] videos
   - Tables/Lists: Yes/No
   - FAQ section: Yes/No
   
   **Estimated Metrics**:
   - Page backlinks: [X]
   - Referring domains: [X]
   - Social shares: [X]
   
   **Why It Ranks #1**:
   1. [Factor 1]
   2. [Factor 2]
   3. [Factor 3]
   
   [Repeat for positions #2-10]
   ```

4. **识别排名模式**
   ```markdown
   ### Ranking Patterns Analysis
   
   **Common Characteristics of Top 5 Results**:
   
   | Factor | Avg/Common Value | Importance |
   |--------|-----------------|------------|
   | Word Count | [X] words | High/Med/Low |
   | Domain Authority | [X] | High/Med/Low |
   | Page Backlinks | [X] | High/Med/Low |
   | Content Freshness | [timeframe] | High/Med/Low |
   | HTTPS | [X]% | High/Med/Low |
   | Mobile Optimized | [X]% | High/Med/Low |
   
   **Content Format Distribution**:
   - How-to guides: [X]/10
   - Listicles: [X]/10
   - In-depth articles: [X]/10
   - Product pages: [X]/10
   - Other: [X]/10
   
   **Domain Type Distribution**:
   - Brand/Company sites: [X]/10
   - Media/News sites: [X]/10
   - Niche blogs: [X]/10
   - Aggregators: [X]/10
   
   **Key Success Factors Identified**:
   
   1. **[Factor 1]**: [Explanation + evidence]
   2. **[Factor 2]**: [Explanation + evidence]
   3. **[Factor 3]**: [Explanation + evidence]
   ```

5. **分析SERP功能**
   ```markdown
   ### Featured Snippet Analysis
   
   **Current Snippet Holder**: [URL]
   **Snippet Type**: [Paragraph/List/Table/Video]
   **Snippet Content**: 
   > [Exact text/description of snippet]
   
   **How to Win This Snippet**:
   1. [Strategy based on current snippet]
   2. [Content format recommendation]
   3. [Structure recommendation]
   
   ---
   
   ### People Also Ask (PAA) Analysis
   
   **Questions Appearing**:
   1. [Question 1] → Currently answered by: [URL]
   2. [Question 2] → Currently answered by: [URL]
   3. [Question 3] → Currently answered by: [URL]
   4. [Question 4] → Currently answered by: [URL]
   
   **PAA Optimization Strategy**:
   - Include these questions as H2/H3 headings
   - Provide direct, concise answers (40-60 words)
   - Use FAQ schema markup
   
   ---
   
   ### AI Overview Analysis
   
   **AI Overview Present**: Yes/No
   **AI Overview Type**: [Summary/List/Comparison/etc.]
   
   **Sources Cited in AI Overview**:
   1. [Source 1] - [Why cited]
   2. [Source 2] - [Why cited]
   3. [Source 3] - [Why cited]
   
   **AI Overview Content Patterns**:
   - Pulls definitions from: [source type]
   - Lists information as: [format]
   - Cites statistics from: [source type]
   
   **How to Get Cited in AI Overview**:
   1. [Specific recommendation]
   2. [Specific recommendation]
   3. [Specific recommendation]
   ```

6. **判断搜索意图**
   ```markdown
   ### Search Intent Analysis
   
   **Primary Intent**: [Informational/Commercial/Transactional/Navigational]
   
   **Evidence**:
   - SERP features suggest: [analysis]
   - Top results are: [content types]
   - User likely wants: [description]
   
   **Intent Breakdown**:
   - Informational signals: [X]%
   - Commercial signals: [X]%
   - Transactional signals: [X]%
   
   **Content Format Implication**:
   Based on intent, your content should:
   - Format: [recommendation]
   - Tone: [recommendation]
   - CTA: [recommendation]
   ```

7. **计算内容难度**
   ```markdown
   ### Difficulty Assessment
   
   **Overall Difficulty Score**: [X]/100
   
   **Difficulty Factors**:
   
   | Factor | Score | Weight | Impact |
   |--------|-------|--------|--------|
   | Top 10 Domain Authority | [avg] | 25% | [High/Med/Low] |
   | Top 10 Page Authority | [avg] | 20% | [High/Med/Low] |
   | Backlinks Required | [est.] | 20% | [High/Med/Low] |
   | Content Quality Bar | [rating] | 20% | [High/Med/Low] |
   | SERP Stability | [rating] | 15% | [High/Med/Low] |
   
   **Realistic Assessment**:
   
   - **New site (DA <20)**: [Can rank?] [Timeframe]
   - **Growing site (DA 20-40)**: [Can rank?] [Timeframe]
   - **Established site (DA 40+)**: [Can rank?] [Timeframe]
   
   **Easier Alternatives**:
   If too difficult, consider:
   - [Alternative keyword 1] - Difficulty: [X]
   - [Alternative keyword 2] - Difficulty: [X]
   ```

8. **生成优化建议**
   ```markdown
   ## SERP Analysis Summary & Recommendations
   
   ### Key Findings
   
   1. [Most important finding]
   2. [Second important finding]
   3. [Third important finding]
   
   ### Content Requirements to Rank
   
   To compete for "[keyword]", you need:
   
   **Minimum Requirements**:
   - [ ] Word count: [X]+ words
   - [ ] Backlinks: [X]+ referring domains
   - [ ] Domain Authority: [X]+
   - [ ] Content format: [type]
   - [ ] Include: [specific elements]
   
   **Differentiators to Win**:
   - [ ] [Unique angle from analysis]
   - [ ] [Missing element in current results]
   - [ ] [SERP feature opportunity]
   
   ### SERP Feature Strategy
   
   | Feature | Winnable? | Strategy |
   |---------|-----------|----------|
   | Featured Snippet | Yes/No | [strategy] |
   | PAA | Yes/No | [strategy] |
   | AI Overview | Yes/No | [strategy] |
   
   ### Recommended Content Outline
   
   Based on SERP analysis:
   
   ```
   标题：[优化后的标题]
   
   H1：[主要标题]
   
   [引言 - 直接回应用户意图]
   
   H2：[基于PAA/排名靠前内容的部分]
   H2：[基于PAA/排名靠前内容的部分]
   H2：[基于PAA/排名靠前内容的部分]
   
   [针对PAA优化的FAQ部分]
   
   [包含呼吁行动（CTA）的结论]
   ```
   
   ### Next Steps

   1. [Immediate action]
   2. [Content creation action]
   3. [Optimization action]
   ```

## 验证要点

### 输入验证
- [ ] 目标关键词已明确指定
- [ ] 搜索位置和设备类型已确认
- [ ] SERP数据是最新的（日期已确认）
- [ ] 已识别或提供了排名前10位的页面URL

### 输出验证
- [ ] 每条建议都引用了具体的数据
- [ ] SERP的组成及所有功能均已记录在案
- [ ] 排名因素是基于对排名前10位页面的实际分析得出的（而非猜测）
- [ ] 内容要求基于当前SERP中的观察结果
- [ ] 每个数据来源均已明确说明（来自SEO工具、人工智能监控工具或用户提供）

## 示例

**用户请求：** “分析‘如何开始播客’的SERP”

**输出结果：**
```markdown
# SERP Analysis: "how to start a podcast"

## SERP Overview

**Intent**: Informational (100%)
**Difficulty**: 72/100 (High)
**AI Overview**: Yes - comprehensive guide format

### SERP Features Present

| Feature | Present | Analysis |
|---------|---------|----------|
| AI Overview | ✅ | Lists steps, cites 3 sources |
| Featured Snippet | ✅ | Step-by-step list from Buzzsprout |
| People Also Ask | ✅ | 4 questions visible, expandable |
| Video Results | ✅ | 3 YouTube videos mid-page |
| Image Pack | ❌ | |

### Top 5 Results Analysis

| Pos | Domain | DA | Word Count | Format | Backlinks |
|-----|--------|-----|------------|--------|-----------|
| 1 | Buzzsprout | 71 | 8,500 | Ultimate Guide | 2,400 |
| 2 | Spotify | 93 | 3,200 | How-to Guide | 890 |
| 3 | Podcastinsights | 58 | 12,000 | Mega Guide | 1,800 |
| 4 | Transistor | 62 | 5,500 | Tutorial | 720 |
| 5 | HubSpot | 91 | 6,200 | Complete Guide | 1,100 |

### Why #1 Ranks First

Buzzsprout's guide succeeds because:
1. **Comprehensive** - Covers every step in detail
2. **Updated** - Current year in title, recent updates
3. **Structured** - Clear numbered steps (owns featured snippet)
4. **Authoritative** - Podcast hosting company (topical authority)
5. **Supporting content** - Links to detailed sub-guides

### Featured Snippet Opportunity

**Current format**: Ordered list (steps)
**Current holder**: Buzzsprout

**To win snippet**:
- Create cleaner, more scannable list format
- Keep steps to 8-10 items max
- Start each step with action verb
- Include "how to start a podcast" in H2

### AI Overview Analysis

**Sources cited**:
1. Buzzsprout - "Choose your podcast topic"
2. Spotify for Podcasters - "Record and edit"
3. Wikipedia - Definition of podcasting

**Pattern**: AI pulls step-by-step instructions from guides with clear structure

### Content Requirements

To rank on page 1:
- **Word count**: 5,000+ words minimum
- **Format**: Step-by-step ultimate guide
- **Backlinks**: 500+ from relevant domains
- **Updates**: Must show current year
- **Unique angle**: Equipment comparisons, cost breakdowns, or specific niche focus

### Recommended Strategy

Given high difficulty, consider:
1. Target long-tail: "how to start a podcast for free" (Difficulty: 45)
2. Target niche: "how to start a podcast about [topic]" (Difficulty: 30)
3. Create supporting video content for video carousel
4. Focus on PAA optimization for quick wins
```

## 高级分析

### 多关键词SERP对比
```
Compare SERPs for [keyword 1], [keyword 2], [keyword 3]
```

### 历史SERP变化
```
How has the SERP for [keyword] changed over time?
```

### 地域SERP差异
```
Compare SERP for [keyword] in [location 1] vs [location 2]
```

### 移动设备与桌面设备的SERP差异
```
Analyze mobile vs desktop SERP differences for [keyword]
```

## 成功技巧

1. **撰写内容前务必检查SERP** —— 不要盲目猜测，要核实实际情况
2. **使内容格式与SERP相匹配** —— 如果列表在SERP中占主导地位，那么内容也应采用列表形式
3. **识别SERP功能的应用机会** —— 这些功能的竞争程度通常低于排名第一的内容
4. **注意SERP的稳定性** —— 稳定的SERP更难被打破
5. **研究异常情况** —— 为什么排名较低的网站也能排在高位？这可能是优化机会！
6. **考虑优化人工智能生成的答案** —— 这种功能的重要性日益增加

## SERP功能分类

### 功能类型及触发条件

| SERP功能 | 触发条件 | 内容要求 | 优化方法 |
|-------------|-------------------|---------------------|---------------------|
| 特色片段（段落形式） | 包含问题或定义的查询 | 使用H2标签展示40-60字的直接答案 | 首先给出直接答案，再展开详细解释 |
| 特色片段（列表形式） | 包含“如何”、“最佳”、“顶级”等关键词的查询 | 使用编号或项目符号列出内容 | 使用编号步骤或排名列表 |
| 特色片段（表格形式） | 包含比较或数据的查询 | 使用结构良好的HTML表格展示 | 创建对比表格 |
| 用户也问（People Also Ask） | 包含信息性的查询 | 使用H2或H3标签展示简洁的答案段落 |
| 知识面板（Knowledge Panel） | 包含实体信息的查询 | 使用Schema标记和Wikipedia链接 | 提供结构化的数据和权威引用 |
| 图片展示 | 包含图片或产品的查询 | 优化图片并添加alt文本 | 使用描述性的文件名和适当的alt文本 |
| 视频轮播 | 包含操作指南或教程的查询 | 提供带有字幕的视频内容 | 优化视频并添加视频Schema标签 |
| 本地信息展示 | 包含地理位置相关的查询 | 使用Google Business Profile | 优化本地SEO |
| 购物结果 | 包含产品或购买信息的查询 | 使用产品Schema和Google Merchant数据 | 优化产品展示 |
| 网站链接 | 包含导航或品牌相关的查询 | 确保网站结构清晰 | 使用合理的层次结构和面包屑导航 |

### 人工智能生成答案分析框架

| 分析维度 | 需要关注的内容 | 重要性说明 |
|-------------------|-----------------|----------------|
| **触发频率** | 该查询是否会触发人工智能生成的答案？ | 并非所有查询都会触发人工智能回答 |
| **引用来源** | 引用了哪些域名？数量是多少？ | 可以看出人工智能参考的权威来源 |
| **引用格式** | 是直接引用还是合成内容？ | 可以看出人工智能偏好的内容格式 |
| **答案结构** | 使用项目符号、段落还是表格？ | 可以判断最佳的内容格式 |
| **事实呈现方式** | 是否包含统计数据、定义或列表？ | 可以看出哪些内容元素会被引用 |
| **更新频率** | 引用的来源更新频率如何？ | 可以看出内容更新的及时性 |

### 从SERP组成中判断搜索意图

| SERP组成 | 预示的搜索意图 | 内容策略建议 |
|-----------------|---------------|-----------------|
| 全部博客文章 | 信息性内容 | 创建全面的指南 |
| 产品页面或购物相关内容 | 交易相关内容 | 优化产品或分类页面 |
| 包含评论和产品内容的页面 | 商业调查相关内容 | 创建比较或评论类内容 |
| 视频占主导地位 | 视觉或教学类内容 | 创建带有字幕的视频内容 |
| 显示本地信息的页面 | 本地相关内容 | 优化本地SEO |
| 新闻类结果 | 时效性强或具有新闻价值的内容 | 及时发布相关内容 |
| 论坛或Reddit上的结果 | 社区或观点相关的内容 | 创建有观点性的、适合讨论的内容 |

## SERP稳定性评估

### 稳定性指标

| 指标 | 稳定性信号 | 波动性信号 |
|-----------|-----------------|-------------------|
| 排名前3位的页面是否长期不变 | 排名前3位的页面是否连续6个月以上未变化 | 排名前3位中是否有新页面出现 |
| 域名多样性 | 排名前10位的域名是否来自2-3个不同的网站 | 排名前10位的域名是否超过8个 |
| SERP功能的变化 | 特定功能是否持续出现或消失 | 特定功能是否稳定出现或消失 |
| 算法对页面排名的影响 | 算法更新后页面排名是否稳定 | 算法更新是否会导致页面排名大幅变动 |

### 基于SERP的优化机会评估

| SERP信号 | 优化机会等级 | 建议采取的行动 |
|------------|------------------|-------------------|
| 排名前5位中权威度较低的网站 | 高 | 创建更优质的内容以超越这些网站 |
| 内容过时的情况 | 高 | 发布新鲜、更新的内容 |
| 内容较少的情况 | 高 | 创建更全面的内容 |
| 论坛或用户生成内容（UGC）排名较高的情况 | 高 | 创建权威性的替代内容 |
| 所有网站的权威度都低于90的情况 | 低 | 选择相关的长尾关键词进行优化 |
| 人工智能生成答案的引用来源较少的情况 | 中等 | 优化内容以增加被引用的机会 |

## 参考资料

- [SERP功能分类](./references/serp-feature-taxonomy.md) —— 完整的SERP功能分类，包括触发条件和优化方法

## 相关技能

- [关键词研究](../keyword-research/) —— 查找需要分析的关键词
- [竞争对手分析](../competitor-analysis/) —— 深入研究竞争对手的排名情况
- [页面SEO审计](../../optimize/on-page-seo-auditor/) —— 根据分析结果优化页面内容
- [地理内容优化工具](../../build/geo-content-optimizer/) —— 优化内容以增加人工智能的引用
- [元标签优化工具](../../build/meta-tags-optimizer/) —— 通过元标签优化SERP的显示效果
- [排名追踪工具](../../monitor/rank-tracker/) —— 跟踪关键词在SERP中的排名变化
- [性能报告工具](../../monitor/performance-reporter/) —— 长期跟踪SERP的可见性指标