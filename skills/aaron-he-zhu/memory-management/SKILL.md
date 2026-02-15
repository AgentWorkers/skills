---
name: memory-management
description: '**使用场景：**  
当用户请求“记住项目上下文”、“保存SEO数据”、“跟踪活动进度”、“存储关键词信息”、“管理项目记忆”、“下次使用时参考这些信息”、“保存我的关键词数据”或“记录此次活动的详细信息”时，该功能可发挥作用。该系统采用双层内存架构（热缓存 + 冷存储），用于存储SEO/GEO项目的相关数据，包括关键词、竞争对手信息、各项指标以及活动状态，并具备智能的推广/优化功能。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "low"
  tags:
    - seo
    - geo
    - project memory
    - context management
    - campaign tracking
    - data persistence
    - keyword tracking
    - project context
  triggers:
    - "remember project context"
    - "save SEO data"
    - "track campaign progress"
    - "store keyword data"
    - "manage project memory"
    - "save progress"
    - "project context"
    - "remember this for next time"
    - "save my keyword data"
    - "keep track of this campaign"
---

# 内存管理


> **[SEO与GEO技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与GEO相关技能 · 全部安装方法：`npx skills add aaron-he-zhu/seo-geo-claude-skills`


<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [架构标记生成器](../../build/schema-markup-generator/)

**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容复习器](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域技能** · [内容质量审核器](../content-quality-auditor/) · [域名权威审核器](../domain-authority-auditor/) · [实体优化器](../entity-optimizer/) · **内存管理**


</details>

该技能为SEO和GEO项目实现了一个双层内存系统：保留一个用于存储活跃上下文的热缓存，以及一个用于存储详细历史数据的冷存储。它能够自动提升频繁被引用的内容，同时移除过时的数据，从而确保上下文加载的效率以及项目内存使用的合理性。


## 何时使用此技能

- 为新SEO项目设置内存结构时
- 完成审核、排名检查或性能报告后
- 开始新的营销活动或优化计划时
- 需要更新项目上下文（如新关键词、竞争对手信息或优先级）时
- 需要查找历史数据或项目专用术语时
- 工作超过30天后，需要清理和归档过时数据时
- 当上下文检索速度变慢或内容杂乱时


## 该技能的功能

1. **热缓存管理**：维护`CLAUDE.md`（约100行），其中包含始终被加载的活跃上下文。
2. **冷存储组织**：在内存的子目录中结构化存储详细档案。
3. **上下文查找**：实现从热缓存到冷存储的高效查找流程。
4. **提升/降级**：根据引用频率在两个存储层之间移动数据。
5. **术语表管理**：管理项目专用术语和缩写。
6. **更新触发机制**：在审核、报告或排名检查后更新内存。
7. **归档管理**：系统地为旧数据添加时间戳并进行归档。


## 使用方法

### 初始化内存结构

```
Set up SEO memory for [project name]
```

```
Initialize memory structure for a new [industry] website optimization project
```

### 分析后更新

```
Update memory after ranking check for [keyword group]
```

```
Refresh hot cache with latest competitor analysis findings
```

### 查询存储的上下文

```
What are our hero keywords?
```

```
Show me the last ranking update date for [keyword category]
```

```
Look up our primary competitors and their domain authority
```

### 提升和降级机制

```
Promote [keyword] to hot cache
```

```
Archive stale data that hasn't been referenced in 30+ days
```

### 术语表管理

```
Add [term] to project glossary: [definition]
```

```
What does [internal jargon] mean in this project?
```


## 数据来源

> 有关工具类别的占位符，请参阅[CONNECTORS.md](../../CONNECTORS.md)。

**当[SEO工具 + 分析工具 + 搜索控制台]连接时：**
- 自动从历史数据中填充内存：关键词排名变化、竞争对手的域名权威度变化、流量指标、转化数据、反向链接概况。该技能会获取当前排名，并在发生重大变化时发出警报，并更新热缓存和冷存储。

**仅使用手动数据时：**
- 要求用户提供：
  - 当前的目标关键词及其优先级
  - 主要竞争对手（3-5个域名）
  - 关键性能指标及最后更新日期
  - 活动中的营销活动及其状态
  - 任何项目专用的术语或缩写

- 使用提供的数据创建内存结构。请在`CLAUDE.md`中注明哪些数据需要手动更新，哪些数据可以自动刷新。


## 指令

当用户请求进行SEO内存管理时：

### 1. 初始化内存结构

对于新项目，请创建以下结构：

```markdown
## Directory Structure

project-root/
├── CLAUDE.md                           # Hot cache (~100 lines)
└── memory/
    ├── glossary.md                     # Project terminology
    ├── keywords/
    │   ├── hero-keywords.md           # Top priority keywords
    │   ├── secondary-keywords.md      # Medium priority
    │   ├── long-tail-keywords.md      # Long-tail opportunities
    │   └── historical-rankings.csv    # Dated ranking data
    ├── competitors/
    │   ├── primary-competitors.md     # Top 3-5 competitors
    │   ├── [competitor-domain].md     # Individual reports
    │   └── analysis-history/          # Dated analyses
    ├── audits/
    │   ├── technical/                 # Technical SEO audits
    │   ├── content/                   # Content audits
    │   ├── domain/                    # Domain authority (CITE) audits
    │   └── backlink/                  # Backlink audits
    ├── content-calendar/
    │   ├── active-calendar.md         # Current quarter
    │   ├── published-content.md       # Performance tracking
    │   └── archive/                   # Past calendars
    └── reports/
        ├── monthly/                   # Monthly reports
        ├── quarterly/                 # Quarterly reports
        └── campaign/                  # Campaign-specific reports
```

### 2. 热缓存（CLAUDE.md）结构

使用此模板创建或更新`CLAUDE.md`：

```markdown
# [Project Name] - SEO Memory (Hot Cache)

**Last Updated**: [Date]
**Project Status**: [Active/Maintenance/Growth]

## Active Target Keywords (Top 10-20)

### Hero Keywords (Priority 1)
| Keyword | Current Rank | Target Rank | Volume | Status |
|---------|--------------|-------------|--------|--------|
| [keyword 1] | #[X] | #[Y] | [vol] | [tracking/optimizing/achieved] |
| [keyword 2] | #[X] | #[Y] | [vol] | [tracking/optimizing/achieved] |

### Secondary Keywords (Priority 2)
| Keyword | Current Rank | Target Rank | Volume | Status |
|---------|--------------|-------------|--------|--------|
| [keyword 1] | #[X] | #[Y] | [vol] | [tracking/optimizing/achieved] |

_Full keyword database: memory/keywords/_

## Primary Competitors (Top 3-5)

1. **[Competitor 1]** (DA: [X])
   - Main strengths: [brief]
   - Our position vs. them: [ahead/behind/competitive]

2. **[Competitor 2]** (DA: [X])
   - Main strengths: [brief]
   - Our position vs. them: [ahead/behind/competitive]

_Detailed analyses: memory/competitors/_

## Current Optimization Priorities

1. **[Priority 1]** - [Brief description]
   - Status: [not started/in progress/completed]
   - Expected impact: [high/medium/low]
   - Deadline: [date]

2. **[Priority 2]** - [Brief description]
   - Status: [not started/in progress/completed]
   - Expected impact: [high/medium/low]
   - Deadline: [date]

## Key Metrics Snapshot

**Last Metrics Update**: [Date]

| Metric | Current | Previous | Change | Target |
|--------|---------|----------|--------|--------|
| Organic Traffic | [X] | [X] | [+/-X%] | [target] |
| Avg. Position | [X] | [X] | [+/-X] | [target] |
| Total Keywords Ranking | [X] | [X] | [+/-X] | [target] |
| Page 1 Rankings | [X] | [X] | [+/-X] | [target] |
| Domain Authority | [X] | [X] | [+/-X] | [target] |
| CITE Score | [X] | [X] | [+/-X] | [target] |
| Last Content Audit Score | [score]/100 | ([rating]) | — [date] | [page audited] |
| Total Backlinks | [X] | [X] | [+/-X%] | [target] |

_Historical data: memory/reports/_

## Active Campaigns

### [Campaign Name 1]
- **Duration**: [Start date] - [End date]
- **Goal**: [Specific goal]
- **Status**: [planning/active/completed]
- **Progress**: [X]%
- **Key activities**: [brief list]

### [Campaign Name 2]
- **Duration**: [Start date] - [End date]
- **Goal**: [Specific goal]
- **Status**: [planning/active/completed]
- **Progress**: [X]%
- **Key activities**: [brief list]

_Campaign archives: memory/reports/campaign/_

## Quick Reference Notes

- [Important note 1]
- [Important note 2]
- [Important note 3]

_For project terminology, see: memory/glossary.md_
```

### 3. 术语表结构（memory/glossary.md）

```markdown
# [Project Name] - SEO Glossary

**Purpose**: Project-specific terminology, brand terms, internal jargon, and abbreviations.

**Last Updated**: [Date]

## Brand Terms

| Term | Full Name | Context |
|------|-----------|---------|
| [abbreviation] | [full name] | [when/how it's used] |

## Product Names

| Internal Name | Public Name | Category |
|---------------|-------------|----------|
| [code name] | [market name] | [product type] |

## Custom Segments

| Segment Name | Definition | Keyword Count |
|--------------|------------|---------------|
| Hero KWs | Top 10 revenue-driving keywords | 10 |
| Quick Wins | Low-difficulty, high-value targets | 25 |
| Brand Defense | Brand + modifier combinations | 15 |

## Competitor Shorthand

| Shorthand | Full Domain | Notes |
|-----------|-------------|-------|
| Comp A | competitor-a.com | Main competitor, [industry] |
| Comp B | competitor-b.com | Niche competitor, [specialty] |

## Project Acronyms

| Acronym | Full Term | Definition |
|---------|-----------|------------|
| [ABC] | [Full term] | [What it means in this project] |

## Internal Jargon

| Phrase | Meaning | Example Usage |
|--------|---------|---------------|
| [phrase] | [definition] | "Check rankings for [phrase]" |

## Historical Context

- **Project started**: [Date]
- **Major algorithm updates affecting us**: [List with dates]
- **Site migrations/redesigns**: [List with dates]
- **Key milestones**: [List with dates]

---

_This glossary helps decode project shorthand and maintain consistency across reports and communications._
```

### 4. 上下文查找流程

当用户查询不明确的术语时，请按照以下步骤进行查找：

**步骤1：检查CLAUDE.md（热缓存）**
- 该术语是否在活跃关键词中？
- 该术语是否在主要竞争对手的相关信息中？
- 该术语是否在当前的优先事项或营销活动中？

**步骤2：检查memory/glossary.md**
- 该术语是否被定义为项目专用术语？
- 该术语是否是自定义段落或缩写？

**步骤3：检查冷存储**
- 在`memory/keywords/`中搜索历史数据
- 在`memory/competitors/`中搜索过去的分析结果
- 在`memory/reports/`中搜索已归档的提及内容

**步骤4：询问用户**
- 如果在任何层中都找不到该术语，请请求用户进一步说明
- 如果是项目专用术语，请将其添加到术语表中


**示例查找流程：**

```markdown
User: "Update rankings for our hero KWs"

Step 1: Check CLAUDE.md → Found "Hero Keywords (Priority 1)" section
Step 2: Extract keyword list from hot cache
Step 3: Execute ranking check
Step 4: Update both CLAUDE.md and memory/keywords/historical-rankings.csv
```


### 5. 提升逻辑

**在以下情况下将其提升到热缓存：**

- **关键词提升触发条件**：
  - 该关键词在7天内被提及超过3次
  - 该关键词的排名发生了显著变化（位置变化超过5位）
  - 该关键词被新的营销活动所针对
  - 该关键词突然导致流量激增

**竞争对手提升触发条件**：
  - 该竞争对手在最近的3次分析中被提及超过3次
  - 该竞争对手表现出积极的SEO活动
  - 该竞争对手发布了竞争内容

**指标提升触发条件**：
  - 该指标经常被用于报告生成
  - 该指标表现出异常行为
  - 该指标与当前的优先事项或营销活动相关


**提升操作：**
```markdown
1. Add item to relevant section in CLAUDE.md
2. Add note: "Promoted [date] - [reason]"
3. Keep detailed data in cold storage
4. Set reminder to review in 30 days
```


### 6. 降级逻辑

**在以下情况下将其降级到冷存储：**

- **关键词降级触发条件**：
  - 该关键词30天内未被提及
  - 该关键词的目标排名已稳定超过60天
  - 该关键词不再属于当前的营销策略
  - 该关键词被更高优先级的关键词取代

**竞争对手降级触发条件**：
  - 该竞争对手60天内没有显著活动
  - 该竞争对手的相关性排名跌出前5名
  - 该竞争对手不再针对相同的关键词

**营销活动降级触发条件**：
  - 该营销活动已完成超过30天
  - 该营销活动被取消或无限期推迟


**降级操作：**
```markdown
1. Remove from CLAUDE.md
2. Archive full data in memory/[category]/archive/
3. Add line to CLAUDE.md: "Last reviewed [category]: [date]"
4. Keep 1-line summary if historically significant
```


### 7. 更新触发机制

在特定事件发生后，系统地更新内存：

**排名检查后：**
```markdown
1. Update CLAUDE.md → Hero Keywords table (current ranks)
2. Append to memory/keywords/historical-rankings.csv
3. Note any keywords with significant movement
4. Update "Last Metrics Update" date in CLAUDE.md
5. If hero keyword moves ±5 positions, create alert note
```

**竞争对手分析后：**
```markdown
1. Update CLAUDE.md → Primary Competitors section (DA, position vs. them)
2. Save full report to memory/competitors/analysis-history/YYYY-MM-DD-analysis.md
3. Update individual competitor files if detailed findings
4. Note new competitor strategies in hot cache
```

**审核后（技术/内容/反向链接）：**
```markdown
1. Save full report to memory/audits/[type]/YYYY-MM-DD-[audit-name].md
2. Extract top 3-5 action items → CLAUDE.md Current Optimization Priorities
3. Update Key Metrics Snapshot if audit includes metrics
4. Create campaign entry if audit spawns new initiative
```

**月度/季度报告后：**
```markdown
1. Save report to memory/reports/[period]/YYYY-MM-report.md
2. Update all metrics in CLAUDE.md Key Metrics Snapshot
3. Review hot cache → demote stale items
4. Update campaign statuses
5. Archive completed campaigns
```


### 8. 归档管理

**月度归档流程：**
```markdown
1. Review CLAUDE.md for items not referenced in 30 days
2. Move stale items to appropriate cold storage
3. Create monthly snapshot: memory/snapshots/YYYY-MM-CLAUDE.md
4. Compress old historical-rankings.csv (keep only last 90 days in main file)
5. Update glossary with new terms from the month
```

**季度归档流程：**
```markdown
1. Review entire cold storage structure
2. Compress files older than 6 months
3. Create quarterly summary report
4. Update project timeline in glossary
5. Audit all active campaigns → archive completed ones
```


### 跨技能内存集成

该技能与其他SEO技能协同工作：

- **当关键词研究运行时**：
  - 将发现的关键词添加到`memory/keywords/`中
  - 如果关键词具有高价值，将其提升到`CLAUDE.md`中
  - 如果出现新的术语，更新术语表

- **当排名追踪器运行时**：
  - 更新`historical-rankings.csv`文件
  - 更新`CLAUDE.md`中的“热门关键词”表格
  - 为热缓存中的重要变化添加标记

- **当竞争对手分析运行时**：
  - 更新`memory/competitors/`中的竞争对手文件
  - 更新`CLAUDE.md`中的“主要竞争对手”部分
  - 如果新竞争对手的排名超过当前的前5名，将其添加进来

- **当内容差距分析运行时**：
  - 将全部分析结果存储在`memory/audits/content/`中
  - 将优化机会提升到`CLAUDE.md`的优先事项中
  - 更新内容日历，包含推荐的主题

- **当SEO内容编写器生成内容时**：
  - 将内容记录到`memory/content-calendar/published-content.md`中
  - 记录目标关键词和发布日期
  - 设置提醒，在30天后检查性能

- **当内容质量审核器运行时**：
  - 将完整报告保存到`memory/audits/content/YYYY-MM-DD-core-eeat-[page-slug].md`中
  - 使用最新分数更新`CLAUDE.md`中的关键指标
  - 如果分数低于60（表示质量较差），在“活跃营销活动”部分进行标记
  - 跟踪各项指标的分数变化趋势

- **当域名权威审核器运行时**：
  - 将完整报告保存到`memory/audits/domain/YYYY-MM-DD-cite-audit.md`中
  - 更新`CLAUDE.md`中的关键指标快照
  - 记录被否决的条目状态和各项指标的分数
  - 如有之前的CITE审核结果，进行对比


## 验证检查点

### 结构验证
- `CLAUDE.md`存在且长度不超过150行（目标长度约为100行）
- `memory/`目录结构与模板匹配
- `glossary.md`存在，并已填充项目基本信息
- 所有历史数据文件的文件名或元数据中包含时间戳


### 内容验证
- `CLAUDE.md`的“最后更新”日期是最新的
- 热缓存中的每个关键词都包含当前的排名、目标排名和状态
- 每个竞争对手都包含域名权威度和排名评估
- 每个活跃的营销活动都包含状态百分比和预期完成日期
- 关键指标快照显示“之前的”数值以供对比


### 查找验证
- 测试查找流程：引用一个术语 → 验证它是否在正确的层中被找到
- 测试提升操作：手动将某个条目提升 → 验证它是否出现在`CLAUDE.md`中
- 测试降级操作：手动将某个条目归档 → 验证它是否从`CLAUDE.md`中移除
- 术语表包含`CLAUDE.md`中使用的所有自定义段落和缩写


### 更新验证
- 排名检查后，`historical-rankings.csv`中添加了带有当天日期的新行
- 竞争对手分析后，`analysis-history/`文件中有日期标记
- 审计后，重要的操作项目会出现在`CLAUDE.md`的优先事项中
- 月度报告后，指标快照反映了新的数据


## 示例

**用户**：“更新我们热门关键词的排名”

**助手**：
```markdown
I'll update rankings for your hero keywords. Let me check the hot cache for the list.

[Reads CLAUDE.md, finds Hero Keywords section:]
- keyword research tools (currently #15, target #5)
- best seo software (currently #23, target #10)
- free backlink checker (currently #8, target #3)
- content optimization guide (currently #12, target #5)
- technical seo audit (currently #18, target #8)

[If ~~SEO tool connected: runs automated ranking check]
[If manual: asks user for current rankings]

---

## Ranking Update - December 15, 2024

| Keyword | Previous | Current | Change | Target | Status |
|---------|----------|---------|--------|--------|--------|
| keyword research tools | #15 | #12 | ↑3 | #5 | Improving ⭐ |
| best seo software | #23 | #24 | ↓1 | #10 | Stable |
| free backlink checker | #8 | #6 | ↑2 | #3 | Near target ⭐⭐ |
| content optimization guide | #12 | #11 | ↑1 | #5 | Improving |
| technical seo audit | #18 | #16 | ↑2 | #8 | Improving |

### Notable Changes
- **free backlink checker** moved to #6 (only 3 positions from target!)
- **keyword research tools** gained 3 positions (strong movement)
- All other keywords showing stable or positive movement

### Updated Files
1. CLAUDE.md → Hero Keywords table updated with current ranks
2. memory/keywords/historical-rankings.csv → New row added:
   `2024-12-15,keyword research tools,12,best seo software,24,free backlink checker,6,...`

### Recommendations
1. Push additional content/backlinks to "free backlink checker" pages to hit #3 target
2. Investigate why "keyword research tools" suddenly gained 3 positions (replicate success)
3. Monitor "best seo software" for any negative trends

Hot cache refreshed. Next ranking check recommended: December 22, 2024.
```


---

**用户**：“‘快速胜利’在我们的项目中是什么意思？”

**助手**：
```markdown
Let me look that up in the project memory.

[Step 1: Check CLAUDE.md → not found]
[Step 2: Check memory/glossary.md → found!]

From your project glossary:

**Quick Wins**
- **Definition**: Low-difficulty, high-value target keywords
- **Keyword Count**: 25 keywords
- **Context**: This segment includes keywords where you can achieve page 1 rankings within 30-60 days due to low competition, despite having decent search volume

According to your memory files, your current quick wins are stored in:
`memory/keywords/long-tail-keywords.md` (tagged with "quick-win" label)

Would you like me to show you the current list of quick win keywords?
```


---

**用户**：“为一个新的户外装备电子商务网站设置内存结构”

**助手**：
```markdown
I'll set up the two-layer memory system for your outdoor gear e-commerce site.

## Creating Directory Structure

[Creates: memory/glossary.md, memory/keywords/, memory/competitors/, etc.]

## CLAUDE.md (Hot Cache) - Initial Setup

I'll need some information to populate the hot cache:

1. **Target Keywords**: What are your top 10 hero keywords?
   (e.g., "hiking backpacks", "camping tents", "outdoor clothing")

2. **Primary Competitors**: Who are your top 3-5 competitors?
   (e.g., rei.com, backcountry.com, moosejaw.com)

3. **Current Metrics** (if available):
   - Domain authority?
   - Current organic traffic?
   - Any existing rankings?

4. **Active Initiatives**:
   - Are you launching a new category?
   - Running a content campaign?
   - Focusing on any specific product line?

5. **Project Terminology**:
   - Any internal product names or abbreviations?
   - How do you segment your keyword strategy?

Please provide what you have, and I'll create your initial CLAUDE.md and glossary. We can start with basics and enrich as we gather more data.

---

Once you provide this information, I'll generate:
- CLAUDE.md with your initial hot cache
- memory/glossary.md with project terminology
- memory/keywords/ structure with placeholder files
- memory/competitors/ with initial competitor list
- memory/content-calendar/active-calendar.md for Q1 2025

After setup, you can use commands like:
- "Update rankings for hero keywords"
- "Add new competitor [domain]"
- "Promote [keyword] to hot cache"
- "Archive campaigns from Q3 2024"
```


## 高级功能

### 智能上下文加载

```
Load full context for [campaign name]
```
- 获取与营销活动相关的热缓存和所有冷存储文件


### 内存健康检查

```
Run memory health check
```
- 审查内存结构：查找孤立文件、缺失的时间戳、过时的热缓存内容以及损坏的引用


### 批量提升/降级

```
Promote all keywords ranking in top 10 to hot cache
```

```
Demote all completed campaigns from Q3 2024
```


### 内存快照

```
Create memory snapshot for [date/milestone]
```
- 在重要里程碑（如网站上线、算法更新等）时，获取整个内存结构的即时副本


### 跨项目内存管理

```
Compare memory with [other project name]
```
- 识别多个项目之间的关键词重叠、竞争对手交集以及策略相似性


## 实际限制

- **并发访问**：如果多个Claude会话同时更新内存，后续的写入操作可能会覆盖之前的数据。可以通过为审核报告使用带时间戳的文件名来避免这种情况，而不是直接覆盖单个文件。
- **冷存储检索**：`memory/`子目录中的文件只有在明确请求时才会被加载。它们不会自动显示在Claude的界面中。热缓存（`CLAUDE.md`）是跨会话的主要数据访问机制。
- **CLAUDE.md的大小**：热缓存应保持简洁（不超过200行）。如果文件过大，应将旧指标归档到冷存储中。
- **数据更新频率**：内存反映的是每个技能最后一次运行的时间。超过90天的过时数据应被标记为需要更新


## 成功技巧

1. **保持热缓存简洁** - `CLAUDE.md`的长度不应超过150行。如果文件过大，应尽快将其降级。
2. **为所有文件添加时间戳** - 冷存储中的每个文件名或元数据中都应包含YYYY-MM-DD格式的日期。
3. **在每次重要操作后更新数据** - 确保内存内容与实际情况保持一致。在排名检查、审核或报告后立即更新数据。
4. **充分利用术语表** - 如果发现需要重复解释某个术语，请将其添加到术语表中。
5. **每周检查热缓存** - 快速扫描以确保所有内容仍然相关且有效。
6. **尽可能自动化** - 如果连接了SEO工具或搜索控制台，设置自动更新`historical-rankings.csv`的机制。
7. **积极归档数据** - 与其让热缓存变得混乱，不如将数据存入冷存储。
8. **在各层之间建立链接** `CLAUDE.md`应始终指明详细数据的存储位置（例如：“完整数据：memory/keywords/”）。
9. **更新时间戳** - 更新`CLAUDE.md`时，务必更新“最后更新”日期。
10. **利用内存保持数据连续性** - 如果在不同分析会话之间切换，内存可以确保不会遗漏任何信息


## 参考资料

- [CORE-EEAT内容基准](../../references/core-eeat-benchmark.md) — 存储在内存中的内容质量评分
- [CITE域名评分](../../references/cite-domain-rating.md) — 存储在内存中的域名权威度评分


## 相关技能

- [排名追踪器](../../monitor/rank-tracker/) — 提供排名数据以更新内存
- [竞争对手分析](../../research/competitor-analysis/) — 生成用于存储的竞争对手报告
- [关键词研究](../../research/keyword-research/) — 发现关键词并添加到内存中
- [性能报告器](../../monitor/performance-reporter/) — 生成触发内存更新的报告
- [内容差距分析](../../research/content-gap-analysis/) — 识别用于优化优先级的关键指标
- [SEO内容编写器](../../build/seo-content-writer/) — 将发布的内容记录到内存日历中
- [内容质量审核器](../content-quality-auditor/) — 将内容审核结果存储在内存中以供跟踪
- [域名权威审核器](../domain-authority-auditor/) — 将域名权威度审核结果存储在内存中以供跟踪
- [实体优化器](../entity-optimizer/) — 存储实体审核结果以供长期跟踪