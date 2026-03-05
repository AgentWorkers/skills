---
name: memory-management
version: "3.0.0"
description: '当用户请求“记住项目上下文”、“保存SEO数据”、“跟踪活动进度”、“存储关键词数据”、“管理项目信息”、“下次使用时记住这些内容”、“保存我的关键词数据”或“跟踪这个活动”时，应使用此技能。该技能管理一个双层内存系统（热缓存 + 冷存储），用于存储SEO/GEO项目的相关信息，包括关键词、竞争对手数据、各项指标以及活动状态，并支持智能的推广/降级策略。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
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
    - context-memory
    - project-memory
    - seo-tracking
    - campaign-tracking
    - session-context
    - hot-cache
    - project-continuity
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

**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容刷新器](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域技能** · [内容质量审核器](../content-quality-auditor/) · [域名权威度审核器](../domain-authority-auditor/) · [实体优化器](../entity-optimizer/) · **内存管理**


</details>

该技能为SEO和GEO项目实现了双层内存系统：一层用于存储活跃的上下文数据（热缓存），另一层用于存储详细的历史数据（冷存储）。系统会自动将频繁被引用的内容提升到热缓存中，将过时的数据降级到冷存储中，从而确保上下文加载的效率以及项目内存使用的合理性。


## 何时使用该技能

- 为新SEO项目设置内存结构时
- 完成审核、排名检查或性能报告后
- 开始新的营销活动或优化计划时
- 需要更新项目上下文（如新增关键词、竞争对手信息或优先级调整时）
- 需要查找历史数据或项目专用术语时
- 工作超过30天后，需要清理和归档过时数据时
- 当上下文检索速度变慢或数据混乱时


## 该技能的功能

1. **热缓存管理**：维护`CLAUDE.md`文件（约100行），其中包含始终会被加载的活跃上下文数据。
2. **冷存储组织**：在内存的子目录中整理详细的档案数据。
3. **上下文查找**：实现从热缓存到冷存储的高效查找流程。
4. **内容提升/降级**：根据数据的使用频率在两个存储层之间移动数据。
5. **术语管理**：管理项目专用的术语和缩写。
6. **更新触发机制**：在审核、报告或排名检查后更新内存。
7. **归档管理**：对旧数据进行时间戳标记并系统地归档。


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

### 内容提升与降级

```
Promote [keyword] to hot cache
```

```
Archive stale data that hasn't been referenced in 30+ days
```

### 术语管理

```
Add [term] to project glossary: [definition]
```

```
What does [internal jargon] mean in this project?
```


## 数据来源

> 有关工具类别的占位符，请参阅[CONNECTORS.md](../../CONNECTORS.md)。

**当[SEO工具 + 分析工具 + 搜索控制台]连接时**：
系统会自动从历史数据中填充内存：关键词的排名变化、竞争对手的域名权威度变化、流量指标、转化数据、反向链接概况等。该技能会获取当前排名，并在发生重大变化时发出警报，同时更新热缓存和冷存储。

**仅使用手动数据时**：
要求用户提供以下信息：
1. 当前的目标关键词及其优先级。
2. 主要竞争对手（3-5个域名）。
3. 关键性能指标及最后更新时间。
4. 正在进行的营销活动及其状态。
5. 任何项目专用的术语或缩写。

根据提供的数据创建内存结构。请在`CLAUDE.md`中注明哪些数据需要手动更新，哪些数据可以自动刷新。


## 使用说明

当用户请求进行SEO内存管理时：

### 1. 初始化内存结构

对于新项目，创建以下结构：

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

> **模板**：请参阅[references/hot-cache-template.md](./references/hot-cache-template.md)以获取完整的`CLAUDE.md`热缓存模板，以及[references/glossary-template.md](./references/glossary-template.md)以获取项目术语表模板。


### 4. 上下文查找流程

当用户查询某个不明确的内容时，按照以下步骤进行查找：

**步骤1：检查CLAUDE.md（热缓存）**
- 该内容是否在活跃关键词中？
- 该内容是否在主要竞争对手的信息中？
- 该内容是否在当前的优先事项或营销活动中？

**步骤2：检查memory/glossary.md**
- 该内容是否被定义为项目专用术语？
- 该内容是否为自定义段落或缩写？

**步骤3：检查冷存储**
- 在`memory/keywords/`中搜索历史数据。
- 在`memory/competitors/`中搜索过往的分析结果。
- 在`memory/reports/`中搜索已归档的提及记录。

**步骤4：询问用户**
- 如果在任何存储层中都找不到该内容，请用户提供更多信息。
- 如果是项目专用术语，请将其添加到术语表中。

示例查找流程：


```markdown
User: "Update rankings for our hero KWs"

Step 1: Check CLAUDE.md → Found "Hero Keywords (Priority 1)" section
Step 2: Extract keyword list from hot cache
Step 3: Execute ranking check
Step 4: Update both CLAUDE.md and memory/keywords/historical-rankings.csv
```


### 5. 内容提升与降级逻辑

> **参考资料**：请参阅[references/promotion-demotion-rules.md](./references/promotion-demotion-rules.md)，了解详细的提升/降级规则（包括关键词、竞争对手、指标和营销活动）以及相应的操作流程。


### 6. 更新触发机制、归档管理及跨技能集成

> **参考资料**：请参阅[references/update-triggers-integration.md](./references/update-triggers-integration.md)，了解排名检查、竞争对手分析、审核和报告后的完整更新流程；以及与所有8个相关技能（关键词研究、排名追踪器、竞争对手分析、内容差距分析、SEO内容编写器、内容质量审核器、域名权威度审核器）的集成方式。


## 验证要点

### 结构验证
- `CLAUDE.md`文件存在且长度不超过150行（建议控制在100行左右）。
- `memory/`目录结构与模板一致。
- `glossary.md`文件存在，并且已填充项目的基本信息。
- 所有历史数据文件的文件名或元数据中包含时间戳。


### 内容验证
- `CLAUDE.md`的“最后更新”日期是最新的。
- 热缓存中的每个关键词都包含当前的排名、目标排名和状态信息。
- 每个竞争对手都有域名权威度和排名评估信息。
- 每个正在进行的营销活动都有状态百分比和预计完成日期。
- 关键指标快照显示了之前的数据以便对比。


### 查找验证
- 测试查找流程：尝试查找某个术语，确认它能在正确的存储层中被找到。
- 测试内容提升：手动将某个内容提升到热缓存中，确认它确实出现在`CLAUDE.md`中。
- 测试内容降级：手动将某个内容归档，确认它已从`CLAUDE.md`中移除。
- 术语表中包含`CLAUDE.md`中使用的所有自定义段落和缩写。


### 更新验证
- 排名检查后，`historical-rankings.csv`文件中会添加包含当天日期的新记录。
- 竞争对手分析后，`analysis-history/`文件中会添加日期戳。
- 审计完成后，最重要的行动项会出现在`CLAUDE.md`的优先事项列表中。
- 月度报告发布后，指标快照会反映新的数据。


## 示例

> **参考资料**：请参阅[references/examples.md](./references/examples.md)，其中包含三个完整的示例：(1) 使用内存刷新更新关键词排名；(2) 术语表的查找流程；(3) 为新电子商务项目初始化内存。


## 高级功能

### 智能上下文加载

```
Load full context for [campaign name]
```

检索热缓存以及与营销活动相关的所有冷存储文件。


### 内存健康检查

```
Run memory health check
```

检查内存结构：查找孤立文件、缺失的时间戳、过时的热缓存内容以及损坏的引用链接。


### 批量内容提升/降级

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

在重要里程碑（如网站发布、算法更新等）时，对整个内存结构进行即时备份。


### 跨项目内存管理

```
Compare memory with [other project name]
```

识别多个项目之间的关键词重叠、竞争对手交集和策略相似性。


## 实际限制

- **并发访问**：如果多个Claude会话同时更新内存，后续的写入操作可能会覆盖之前的数据。建议使用带时间戳的文件名来保存审计报告，避免覆盖单个文件。
- **冷存储数据的检索**：`memory/`子目录中的文件仅在明确请求时才会被加载。它们不会自动显示在Claude的界面中。热缓存（`CLAUDE.md`）是跨会话的数据访问主要途径。
- **CLAUDE.md的大小**：热缓存应保持简洁（不超过200行）。如果文件过大，应将旧数据归档到冷存储中。
- **数据更新频率**：内存中的数据反映的是各技能最后一次运行的时间。超过90天的旧数据应被标记为需要更新。


## 成功使用的小贴士

1. **保持热缓存简洁**：`CLAUDE.md`的长度不应超过150行。如果文件过大，应尽快将旧数据降级到冷存储。
2. **为所有文件添加时间戳**：冷存储中的文件名或元数据中必须包含YYYY-MM-DD格式的日期。
3. **每次进行重要操作后更新数据**：确保内存内容与实际情况保持一致。在排名检查、审核或报告后立即更新数据。
4. **充分利用术语表**：如果某个术语被多次使用，应将其添加到术语表中。
5. **每周检查热缓存**：快速扫描以确保所有内容仍然相关且有效。
6. **尽可能实现自动化**：如果连接了SEO工具或搜索控制台，设置自动更新`historical-rankings.csv`文件的机制。
7. **积极归档数据**：将数据存放在冷存储中，避免热缓存过于臃肿。
8. **明确数据存储位置**：`CLAUDE.md`中应明确指出详细数据的存储位置（例如：“完整数据：memory/keywords/”）。
9. **更新时间戳**：更新`CLAUDE.md`时，务必更新“最后更新”日期。
10. **利用内存保持数据连续性**：在不同分析会话之间切换时，内存能确保不会丢失任何信息。


## 参考资料

- [CORE-EEAT内容评分](../../references/core-eeat-benchmark.md) — 存储在内存中的内容质量评分。
- [CITE域名评分](../../references/cite-domain-rating.md) — 存储在内存中的域名权威度评分。


## 相关技能

- [rank-tracker](../../monitor/rank-tracker/) — 提供用于更新内存的排名数据。
- [competitor-analysis](../../research/competitor-analysis/) — 生成用于存储的竞争对手报告。
- [keyword-research](../../research/keyword-research/) — 发现可用于更新内存的关键词。
- [performance-reporter](../../monitor/performance-reporter/) — 生成触发内存更新的报告。
- [content-gap-analysis](../../research/content-gap-analysis/) — 识别用于热缓存优化的优先事项。
- [seo-content-writer](../../build/seo-content-writer/) — 将发布的内容记录到内存日历中。
- [content-quality-auditor](../content-quality-auditor/) — 将内容审核结果存储在内存中以便跟踪。
- [domain-authority-auditor](../domain-authority-auditor/) — 将域名审核结果存储在内存中以便跟踪。
- [entity-optimizer](../entity-optimizer/) — 随时间存储实体审核结果以便跟踪。