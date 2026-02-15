---
name: serp-analysis
description: '**使用场景：**  
当用户询问“分析搜索结果”、“SERP分析”、“哪些页面获得了排名”、“SERP的特点是什么”、“为什么这个页面会获得排名”、“针对该查询，首页显示了哪些内容”、“哪些网站针对该关键词获得了排名”，或“Google针对该关键词展示了什么内容”时，可以使用此工具。该工具用于分析搜索引擎结果页面（SERPs），以了解排名因素、SERP的特点、用户意图模式以及人工智能（AI）的相关机制。这对于理解页面获得排名的关键因素至关重要。若需跟踪页面的长期排名变化，请使用“rank-tracker”工具；若需进行关键词研究，请参考“keyword-research”相关内容。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "high"
  tags:
    - seo
    - geo
    - serp
    - search results
    - ranking factors
    - serp features
    - ai overviews
    - featured snippets
    - search intent
  triggers:
    - "analyze search results"
    - "SERP analysis"
    - "what ranks for"
    - "SERP features"
    - "why does this page rank"
    - "featured snippets"
    - "AI overviews"
    - "what's on page one for this query"
    - "who ranks for this keyword"
    - "what does Google show for"
---

# SERP分析

> **[SEO与地理技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理相关技能 · 全部技能可通过 `npx skills add aaron-he-zhu/seo-geo-claude-skills` 安装

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../keyword-research/) · [竞争对手分析](../competitor-analysis/) · **SERP分析** · [内容差距分析](../content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [架构标记生成器](../../build/schema-markup-generator/)

**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容刷新器](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威性审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)

</details>

该技能用于分析搜索引擎结果页面（SERP），以了解哪些内容有助于提高排名、哪些SERP元素会显示出来，以及哪些因素会触发AI生成的答案。在创建内容之前，先了解这些信息是非常重要的。

## 何时使用此技能

- 在为目标关键词创建内容之前
- 了解为什么某些页面能排在第1位
- 识别SERP元素中的优化机会（如特色片段、PAA等）
- 分析AI生成的摘要（AI Overview/SGE）的模式
- 更准确地评估关键词的难度
- 根据排名情况规划内容格式
- 确定特定查询的排名因素

## 该技能的功能

1. **SERP组成分析**：展示结果页面上显示的所有元素
2. **排名因素识别**：揭示顶级结果排名背后的原因
3. **SERP元素映射**：识别特色片段、PAA、知识面板等元素
4. **AI摘要分析**：检查AI摘要何时以及如何出现
5. **意图信号检测**：从SERP组成中判断用户意图
6. **内容格式建议**：根据SERP推荐最佳内容格式
7. **难度评估**：评估内容的实际排名潜力

## 使用方法

### 基础SERP分析

```
Analyze the SERP for [keyword]
```

```
What does it take to rank for [keyword]?
```

### 特定元素分析

```
Analyze featured snippet opportunities for [keyword list]
```

### 竞争对手SERP分析

```
Why does [URL] rank #1 for [keyword]?
```

## 数据来源

> 有关工具类别的占位符，请参阅 [CONNECTORS.md](../../CONNECTORS.md)。

**通过连接 ~~SEO工具 + ~~搜索控制台 + ~~AI监控工具**：
可以自动获取目标关键词的SERP快照，提取排名页面的指标（域名权威性、反向链接、内容长度），提取SERP元素数据，并使用 ~~AI监控工具**检查AI摘要的存在情况。历史SERP变化数据以及移动设备与桌面设备上的差异也可以自动获取。

**仅使用手动数据时**：
请用户提供以下信息：
1. 需要分析的目标关键词
2. SERP截图或搜索结果的详细描述
3. 排名前10位的页面URL
4. 搜索位置和设备类型（移动/桌面）
5. 关于SERP元素的任何观察结果（如特色片段、PAA等）

使用提供的数据进行完整分析。在输出结果中注明哪些指标来自自动收集，哪些来自用户提供的数据。

## 指令

当用户请求SERP分析时：

1. **理解查询意图**
   如有需要，澄清以下信息：
   - 需要分析的目标关键词
   - 搜索位置/语言
   - 设备类型（移动/桌面）
   - 关于SERP的特定问题

2. **绘制SERP组成图**
   记录所有显示的元素：
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
   │ [AI摘要 / SGE]（如果存在）        │
   ├─────────────────────────────────────────┤
   │ [广告] - 展示区内的[X]个广告              │
   ├─────────────────────────────────────────┤
   │ [特色片段]（如果存在）         │
   ├─────────────────────────────────────────┤
   │ [自然搜索结果#1]                     │
   │ [自然搜索结果#2]                     │
   │ [用户也问]（如果存在）          │
   │ [自然搜索结果#3]                     │
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
   对于排名前10的结果：
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

5. **分析SERP元素**
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

6. **确定搜索意图**
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

7. **计算难度**
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

8. **生成建议**
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
   
   H2：[基于PAA/排名靠前内容的章节]
   H2：[基于PAA/排名靠前内容的章节]
   H2：[基于PAA/排名靠前内容的章节]
   
   [针对PAA优化的FAQ部分]
   
   [带有呼吁行动的结论]
   ```
   
   ### Next Steps

   1. [Immediate action]
   2. [Content creation action]
   3. [Optimization action]
   ```

## 验证要点

### 输入验证
- [ ] 目标关键词明确指定
- [ ] 搜索位置和设备类型已确认
- [ ] SERP数据是最新的（日期已确认）
- [ ] 已识别或提供了排名前10位的页面URL

### 输出验证
- [ ] 每条建议都引用了具体的数据点（而非泛泛而谈）
- [ ] SERP组成图中的所有元素都已记录
- [ ] 排名因素是根据实际排名前10位的分析结果确定的（而非猜测）
- [ ] 内容要求基于当前SERP中的观察结果
- [ ] 每个数据点的来源已明确说明（来自~~SEO工具数据、~~AI监控数据或用户提供的数据）

## 示例

**用户**：“分析‘如何开始播客’的SERP”

**输出**：

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

### 多关键词SERP比较

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

1. **编写内容前务必检查SERP** —— 不要盲目猜测，要核实情况
2. **内容格式要与SERP相匹配** —— 如果列表在SERP中显示，就编写列表形式的内容
3. **识别SERP元素中的优化机会** —— 这类内容的竞争通常较低
4. **注意SERP的稳定性** —— 稳定的SERP更难被打破
5. **研究异常情况** —— 为什么排名较低的资源也能排在前面？这可能是一个优化机会！
6. **考虑AI摘要的优化** —— 这个方面越来越重要

## SERP元素分类

### 元素类型及触发条件

| SERP元素 | 触发条件 | 内容要求 | 优化方法 |
|-------------|-------------------|---------------------|---------------------|
| 特色片段（段落） | 询问/定义类型的查询 | 40-60字的直接回答，放在H2标题下 | 立即给出答案，然后进行详细解释 |
| 特色片段（列表） | “如何”、“最佳”、“顶级”等类型的查询 | 使用编号或项目符号列表 | 使用编号步骤或分级列表 |
| 特色片段（表格） | 比较/数据类型的查询 | 结构良好的HTML表格 | 创建对比表格 |
| “用户也问” | 信息量较大的查询 | 简洁的回答段落 | 将相关问题作为H2/H3标题 |
| 知识面板 | 实体相关的查询 | 使用schema标记和维基百科内容 | 结构化数据 + 权威引用 |
| 图片集 | 视觉/产品相关的查询 | 优化后的图片并添加alt文本 | 使用描述性的文件名和适当的alt文本 |
| 视频轮播 | 操作指南/教程类型的查询 | 带有字幕的视频内容 | 优化YouTube视频并使用视频schema |
| 本地相关内容 | 与位置相关的查询 | 使用Google企业资料 | 优化本地SEO |
| 购物相关结果 | 产品/购买相关的查询 | 使用产品schema和Google Merchant功能 | 优化产品展示 |
| 网站链接 | 导航/品牌相关的查询 | 清晰的网站结构 | 逻辑清晰的导航结构 |

### AI摘要分析框架

| 分析维度 | 需要关注的内容 | 重要性 |
|-------------------|-----------------|----------------|
| **触发率** | 该查询是否会产生AI摘要？ | 并非所有查询都会产生AI摘要 |
| **来源选择** | 引用了哪些域名？数量是多少？ | 显示AI使用的权威性来源 |
| **引用格式** | 直接引用还是合成内容 | 显示AI偏好的内容格式 |
| **答案结构** | 项目符号、段落、表格 | 表示最佳的内容格式 |
| **事实呈现方式** | 引用的统计数据、定义、列表 | 显示哪些内容元素会被引用 |
| **更新频率** | 引用的来源更新频率如何？ | 显示内容的时效性 |

### 从SERP组成中判断搜索意图

| SERP组成 | 暗示的搜索意图 | 内容策略 |
|-----------------|---------------|-----------------|
| 所有博客文章 | 信息类查询 | 创建全面的指南 |
| 产品页面 + 购物相关内容 | 交易类查询 | 优化产品/类别页面 |
| 评论与产品混合 | 商业类查询 | 创建对比/评论类内容 |
| 视频占主导 | 视频/教学类查询 | 创建带有字幕的视频内容 |
| 显示本地相关内容 | 本地相关查询 | 优化本地SEO |
| 新闻类结果 | 热门/时效性强的内容 | 及时发布有新闻价值的内容 |
| 论坛/Reddit结果 | 社区/观点类查询 | 创建具有观点性的、适合讨论的内容 |

## SERP稳定性评估

### 稳定性指标

| 指标 | 稳定性信号 | 不稳定性信号 |
|-----------|-----------------|-------------------|
| 排名前3位的页面是否长期不变 | 排名前3位的页面是否在6个月内未变化 | 排名前3位中是否有新页面出现 |
| 域名多样性 | 排名前10位的域名是否来自2-3个不同的域名 | 排名前10位的域名是否来自8个以上的不同域名 |
| SERP元素的变化 | 特定元素是否持续出现 | 特定元素是否出现或消失 |
| 算法敏感性 | 更新后页面排名是否稳定 | 更新后排名是否发生较大变动 |

### 基于SERP的优化机会评估

| SERP信号 | 机会等级 | 建议的行动 |
|------------|------------------|-------------------|
| 排名前5位中权威性较低的网站 | 高 | 创建更优质的内容以超越它们 |
| 内容过时的情况 | 高 | 发布新鲜、更新的内容 |
| 内容较少的情况 | 高 | 创建全面的内容 |
| 论坛/用户生成内容（UGC）排名较高 | 高 | 创建权威性的替代内容 |
| 所有引用来源权威性低于90的网站 | 低 | 选择相关的长期搜索词进行优化 |
| AI摘要的引用来源较少 | 中等 | 优化以获得AI的引用 |

## 参考资料

- [SERP元素分类](./references/serp-feature-taxonomy.md) —— 完整的SERP元素分类，包括触发条件和优化方法

## 相关技能

- [关键词研究](../keyword-research/) —— 查找需要分析的关键词
- [竞争对手分析](../competitor-analysis/) —— 深入研究竞争对手的排名情况
- [页面SEO审核器](../../optimize/on-page-seo-auditor/) —— 根据分析结果进行优化
- [地理内容优化器](../../build/geo-content-optimizer/) —— 优化以获得AI的引用
- [元标签优化器](../../build/meta-tags-optimizer/) —— 通过元标签优化SERP的显示效果
- [排名追踪器](../../monitor/rank-tracker/) —— 跟踪关键词在SERP中的排名变化
- [性能报告器](../../monitor/performance-reporter/) —— 随时间跟踪SERP的可见性指标