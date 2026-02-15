---
name: entity-optimizer
description: '**使用场景：**  
当用户提出以下需求时，可使用该工具：  
- “优化实体的可见性”  
- “构建知识图谱”  
- “改进知识面板”  
- “进行实体审计”  
- “创建品牌实体”  
- “谷歌未识别我的品牌”  
- “没有知识面板”  
- “将我的品牌作为实体进行注册/识别”。  

**功能说明：**  
该工具可独立使用，适用于公共搜索和人工智能查询测试场景；当与以下组件结合使用时，其功能将得到进一步增强：  
- **知识图谱**（用于更深入的实体分析）  
- **SEO工具**（提升品牌在搜索引擎中的排名）  
- **AI监控系统**（实现自动化实体识别与分析）。  

**相关工具：**  
- **schema-markup-generator**：用于结构化数据的生成与标记。  
- **geo-content-optimizer**：用于内容层面的智能优化。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "high"
  tags:
    - seo
    - geo
    - entity optimization
    - knowledge graph
    - knowledge panel
    - brand entity
    - entity disambiguation
    - wikidata
    - structured entities
  triggers:
    - "optimize entity presence"
    - "build knowledge graph"
    - "improve knowledge panel"
    - "entity audit"
    - "establish brand entity"
    - "knowledge panel"
    - "entity disambiguation"
    - "Google doesn't know my brand"
    - "no knowledge panel"
    - "establish my brand as an entity"
---

# 实体优化器（Entity Optimizer）

> **[SEO与地理信息（SEO & GEO）技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理信息相关技能 · 全部技能的安装命令：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究（Research）** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [搜索引擎结果页（SERP）分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建（Build）** · [SEO内容撰写工具](../../build/seo-content-writer/) · [地理内容优化工具](../../build/geo-content-optimizer/) · [元标签优化工具](../../build/meta-tags-optimizer/) · [schema标记生成工具](../../build/schema-markup-generator/)

**优化（Optimize）** · [页面SEO审核工具](../../optimize/on-page-seo-auditor/) · [技术SEO检查工具](../../optimize/technical-seo-checker/) · [内部链接优化工具](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控（Monitor）** · [排名追踪工具](../../monitor/rank-tracker/) · [反向链接分析工具](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理工具](../../monitor/alert-manager/)

**跨领域工具（Cross-cutting）** · [内容质量审核工具](../content-quality-auditor/) · [域名权威性审核工具](../domain-authority-auditor/) · **实体优化工具** · [内存管理工具](../memory-management/)

</details>

该工具用于审核、构建并维护实体在搜索引擎和AI系统中的识别度。实体（如人、组织、产品或概念）是谷歌和大型语言模型（LLMs）判断“你是谁”以及“是否应该引用你”的基础。

**实体对SEO与地理信息的重要性：**

- **SEO**：谷歌的知识图谱（Knowledge Graph）为知识面板（Knowledge Panels）、丰富搜索结果和基于实体的排名信号提供了支持。一个定义明确的实体能在搜索引擎结果页中获得更好的展示位置。
- **地理信息**：AI系统在生成答案之前会先将查询结果与实体进行匹配。如果AI无法识别你的实体，无论你的内容多么优质，也无法被引用。

## 何时使用该工具

- 建立一个新的品牌/人物/产品作为被认可的实体
- 审核实体在知识图谱、维基数据（Wikidata）和AI系统中的存在情况
- 改进或修正知识面板的内容
- 建立实体与主题/行业的关联
- 解决实体歧义问题（避免与其他实体混淆）
- 加强实体在AI中的引用信号
- 在推出新品牌、产品或组织后使用
- 为网站迁移做准备（保持实体身份的一致性）
- 定期进行实体健康检查

## 该工具的功能

1. **实体审核**：评估实体在搜索引擎和AI系统中的当前存在情况
2. **知识图谱分析**：检查谷歌知识图谱、维基数据和维基百科中的实体信息
3. **AI实体识别测试**：查询AI系统如何识别和描述该实体
4. **实体信号映射**：识别所有用于确立实体身份的信号
5. **差距分析**：发现缺失或薄弱的实体信号
6. **实体构建计划**：制定可执行的计划以建立或加强实体的存在感
7. **歧义解决策略**：解决实体名称相似导致的混淆问题

## 使用方法

### 实体审核（Entity Audit）

```
Audit entity presence for [brand/person/organization]
```

```
How well do search engines and AI systems recognize [entity name]?
```

### 建立实体存在感（Build Entity Presence）

```
Build entity presence for [new brand] in the [industry] space
```

```
Establish [person name] as a recognized expert in [topic]
```

### 解决实体问题（Fix Entity Issues）

```
My Knowledge Panel shows incorrect information — fix entity signals for [entity]
```

```
AI systems confuse [my entity] with [other entity] — help me disambiguate
```

## 数据来源

> 有关工具类别的更多信息，请参阅[CONNECTORS.md](../../CONNECTORS.md)。

**通过以下工具连接：**
- 使用知识图谱API查询实体状态
- 从SEO工具中获取品牌相关搜索数据
- 使用AI监控工具测试AI对实体的引用情况
- 使用品牌监控工具跟踪品牌提及次数

**仅使用手动数据时：**
- 请用户提供以下信息：
  - 实体名称及类型（人、组织、品牌、产品、创意作品、事件）
  - 主要网站/域名
  - 已知的实体资料（维基百科、维基数据、社交媒体、行业目录）
  - 实体应关联的前三到五个主题/行业
  - 任何已知的歧义问题（其他实体是否使用相同/相似的名称）

在没有工具的情况下，Claude会根据用户提供的信息提供实体优化策略和建议。用户需要自行执行搜索查询、检查知识面板并测试AI的响应，以提供分析所需的原始数据。

请使用公开搜索结果、AI查询测试和搜索引擎结果页分析来进行审核。注意哪些步骤需要借助工具才能完成全面评估。

## 使用说明

当用户请求实体优化时：

### 第一步：实体发现（Entity Discovery）

确定实体在所有系统中的当前状态。

```markdown
### Entity Profile

**Entity Name**: [name]
**Entity Type**: [Person / Organization / Brand / Product / Creative Work / Event]
**Primary Domain**: [URL]
**Target Topics**: [topic 1, topic 2, topic 3]

#### Current Entity Presence

| Platform | Status | Details |
|----------|--------|---------|
| Google Knowledge Panel | ✅ Present / ❌ Absent / ⚠️ Incorrect | [details] |
| Wikidata | ✅ Listed / ❌ Not listed | [QID if exists] |
| Wikipedia | ✅ Article / ⚠️ Mentioned only / ❌ Absent | [notability assessment] |
| Google Knowledge Graph API | ✅ Entity found / ❌ Not found | [entity ID, types, score] |
| Schema.org on site | ✅ Complete / ⚠️ Partial / ❌ Missing | [Organization/Person/Product schema] |

#### AI Entity Resolution Test

**Note**: Claude cannot directly query other AI systems or perform real-time web searches without tool access. When running without ~~AI monitor or ~~knowledge graph tools, ask the user to run these test queries and report the results, or use the user-provided information to assess entity presence.

Test how AI systems identify this entity by querying:
- "What is [entity name]?"
- "Who founded [entity name]?" (for organizations)
- "What does [entity name] do?"
- "[entity name] vs [competitor]"

| AI System | Recognizes Entity? | Description Accuracy | Cites Entity's Content? |
|-----------|-------------------|---------------------|------------------------|
| ChatGPT | ✅ / ⚠️ / ❌ | [accuracy notes] | [yes/no/partially] |
| Claude | ✅ / ⚠️ / ❌ | [accuracy notes] | [yes/no/partially] |
| Perplexity | ✅ / ⚠️ / ❌ | [accuracy notes] | [yes/no/partially] |
| Google AI Overview | ✅ / ⚠️ / ❌ | [accuracy notes] | [yes/no/partially] |
```

### 第二步：实体信号审核（Entity Signal Audit）

评估实体的6个方面的信号。详细的47项信号检查清单及验证方法请参阅[references/entity-signal-checklist.md](./references/entity-signal-checklist.md)。

```markdown
### Entity Signal Audit

#### 1. Structured Data Signals

| Signal | Status | Action Needed |
|--------|--------|--------------|
| Organization/Person schema on homepage | ✅ / ❌ | [action] |
| sameAs links to authoritative profiles | ✅ / ❌ | [action] |
| logo, foundingDate, founder properties | ✅ / ❌ | [action] |
| Consistent @id across pages | ✅ / ❌ | [action] |
| Product/Service schema on relevant pages | ✅ / ❌ | [action] |
| Author schema with sameAs on articles | ✅ / ❌ | [action] |

#### 2. Knowledge Base Signals

| Signal | Status | Action Needed |
|--------|--------|--------------|
| Wikidata entry with complete properties | ✅ / ❌ | [action] |
| Wikipedia article (or notability path) | ✅ / ❌ | [action] |
| CrunchBase profile (organizations) | ✅ / ❌ | [action] |
| Industry directory listings | ✅ / ❌ | [action] |
| Government/official registries | ✅ / ❌ | [action] |

#### 3. Consistent NAP+E Signals (Name, Address, Phone + Entity)

| Signal | Status | Action Needed |
|--------|--------|--------------|
| Consistent entity name across all platforms | ✅ / ❌ | [action] |
| Same description/tagline everywhere | ✅ / ❌ | [action] |
| Matching logos and visual identity | ✅ / ❌ | [action] |
| Social profiles all linked bidirectionally | ✅ / ❌ | [action] |
| Contact info consistent across directories | ✅ / ❌ | [action] |

#### 4. Content-Based Entity Signals

| Signal | Status | Action Needed |
|--------|--------|--------------|
| About page with entity-rich structured content | ✅ / ❌ | [action] |
| Author pages with credentials and sameAs | ✅ / ❌ | [action] |
| Topical authority (content depth in target topics) | ✅ / ❌ | [action] |
| Entity mentions in content (natural co-occurrence) | ✅ / ❌ | [action] |
| Branded anchor text in backlinks | ✅ / ❌ | [action] |

#### 5. Third-Party Entity Signals

| Signal | Status | Action Needed |
|--------|--------|--------------|
| Mentions on authoritative sites (news, industry) | ✅ / ❌ | [action] |
| Co-citation with established entities | ✅ / ❌ | [action] |
| Reviews and ratings on third-party platforms | ✅ / ❌ | [action] |
| Speaking engagements, awards, publications | ✅ / ❌ | [action] |
| Press coverage with entity name | ✅ / ❌ | [action] |

#### 6. AI-Specific Entity Signals

| Signal | Status | Action Needed |
|--------|--------|--------------|
| Clear entity definition in opening paragraphs | ✅ / ❌ | [action] |
| Unambiguous entity name (or disambiguation strategy) | ✅ / ❌ | [action] |
| Factual claims about entity are verifiable | ✅ / ❌ | [action] |
| Entity appears in AI training data sources | ✅ / ❌ | [action] |
| Entity's content is crawlable by AI systems | ✅ / ❌ | [action] |
```

### 第三步：报告与行动计划（Report & Action Plan）

```markdown
## Entity Optimization Report

### Overview

- **Entity**: [name]
- **Entity Type**: [type]
- **Audit Date**: [date]

### Signal Category Summary

| Category | Status | Key Findings |
|----------|--------|-------------|
| Structured Data | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |
| Knowledge Base | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |
| Consistency (NAP+E) | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |
| Content-Based | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |
| Third-Party | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |
| AI-Specific | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |

### Critical Issues

[List any issues that severely impact entity recognition — disambiguation problems, incorrect Knowledge Panel, missing from Knowledge Graph entirely]

### Top 5 Priority Actions

Sorted by: impact on entity recognition × effort required

1. **[Signal]** — [specific action]
   - Impact: [High/Medium] | Effort: [Low/Medium/High]
   - Why: [explanation of how this improves entity recognition]

2. **[Signal]** — [specific action]
   - Impact: [High/Medium] | Effort: [Low/Medium/High]
   - Why: [explanation]

3–5. [Same format]

### Entity Building Roadmap

#### Week 1-2: Foundation (Structured Data + Consistency)
- [ ] Implement/fix Organization or Person schema with full properties
- [ ] Add sameAs links to all authoritative profiles
- [ ] Audit and fix NAP+E consistency across all platforms
- [ ] Ensure About page is entity-rich and well-structured

#### Month 1: Knowledge Bases
- [ ] Create or update Wikidata entry with complete properties
- [ ] Ensure CrunchBase / industry directory profiles are complete
- [ ] Build Wikipedia notability (or plan path to notability)
- [ ] Submit to relevant authoritative directories

#### Month 2-3: Authority Building
- [ ] Secure mentions on authoritative industry sites
- [ ] Build co-citation signals with established entities
- [ ] Create topical content clusters that reinforce entity-topic associations
- [ ] Pursue PR opportunities that generate entity mentions

#### Ongoing: AI-Specific Optimization
- [ ] Test AI entity resolution quarterly
- [ ] Update factual claims to remain current and verifiable
- [ ] Monitor AI systems for incorrect entity information
- [ ] Ensure new content reinforces entity identity signals

### Cross-Reference

- **CORE-EEAT relevance**: Items A07 (Knowledge Graph Presence) and A08 (Entity Consistency) directly overlap — entity optimization strengthens Authority dimension
- **CITE relevance**: CITE I01-I10 (Identity dimension) measures entity signals at domain level — entity optimization feeds these scores
- For content-level audit: [content-quality-auditor](../content-quality-auditor/)
- For domain-level audit: [domain-authority-auditor](../domain-authority-auditor/)
```

## 验证要点

### 输入验证（Input Validation）
- 实体名称和类型已确认
- 主要域名/网站已确认
- 目标主题/行业已指定
- 如果实体名称常见，提供了歧义解决的相关信息

### 输出验证（Output Validation）
- 所有6个信号类别均已评估
- 使用至少3个查询测试了AI对实体的识别能力
- 知识面板的状态已检查
- 维基数据和维基百科的状态已验证
- 主要网站上的Schema.org标记已审核
- 每条建议都具体且可执行
- 路线图包含明确的时间表和步骤
- 已参考CORE-EEAT A07/A08和CITE I01-I10标准

## 示例

**用户**：“审核我们的B2B SaaS分析平台CloudMetrics在cloudmetrics.io上的实体存在情况”

**输出：**

```markdown
## Entity Optimization Report

### Entity Profile

**Entity Name**: CloudMetrics
**Entity Type**: Organization (B2B SaaS)
**Primary Domain**: cloudmetrics.io
**Target Topics**: analytics platform, business intelligence, enterprise analytics

### AI Entity Resolution Test

Queries tested with results reported by user:

| Query | Result | Assessment |
|-------|--------|------------|
| "What is CloudMetrics?" | Described as "an analytics tool" with no further detail | Partial recognition -- generic description, no mention of B2B focus or key features |
| "Best analytics platforms for enterprises" | CloudMetrics not mentioned in any AI response | Not recognized as a player in the enterprise analytics space |
| "CloudMetrics vs Datadog" | Correctly identified as a competitor to Datadog, but feature comparison was incomplete and partially inaccurate | Partial -- entity is associated with the right category but attributes are thin |
| "Who founded CloudMetrics?" | No answer found by any AI system tested | Entity leadership not present in AI knowledge bases |

### Entity Health Summary

| Signal Category | Status | Key Findings |
|-----------------|--------|--------------|
| Knowledge Graph | ❌ Missing | No Wikidata entry exists; no Google Knowledge Panel triggers for branded queries |
| Structured Data | ⚠️ Partial | Organization schema present on homepage with name, url, and logo; missing Person schema for CEO and leadership team; no sameAs links to external profiles |
| Web Presence | ✅ Strong | Consistent NAP across LinkedIn, Twitter/X, G2, and Crunchbase; social profiles link back to cloudmetrics.io; branded search returns owned properties in top 5 |
| Content-Based | ⚠️ Partial | About page exists but opens with marketing copy rather than an entity-defining statement; no dedicated author pages for leadership |
| Third-Party | ⚠️ Partial | Listed on G2 and Crunchbase; 2 industry publication mentions found; no awards or analyst coverage |
| AI-Specific | ❌ Weak | AI systems have only surface-level awareness; entity definition is not quotable from any authoritative source |

### Top 3 Priority Actions

1. **Create Wikidata entry** with key properties: instance of (P31: business intelligence software company), official website (P856: cloudmetrics.io), inception (P571), country (P17)
   - Impact: High | Effort: Low
   - Why: Wikidata is the foundational knowledge base that feeds Google Knowledge Graph, Bing, and AI training pipelines; without it, the entity cannot be formally resolved

2. **Add Person schema for leadership team** on the About/Team page, including name, jobTitle, sameAs links to LinkedIn profiles, and worksFor pointing to the Organization entity
   - Impact: High | Effort: Low
   - Why: Addresses the "Who founded CloudMetrics?" gap directly; Person schema for key people creates bidirectional entity associations that strengthen organizational identity

3. **Build Wikipedia notability through independent press coverage** -- target 3-5 articles in industry publications (TechCrunch, VentureBeat, Analytics India Magazine) that mention CloudMetrics by name with verifiable claims
   - Impact: High | Effort: High
   - Why: Wikipedia notability requires coverage in independent reliable sources; press mentions simultaneously feed AI training data, build third-party entity signals, and create the citation foundation for a future Wikipedia article

### Cross-Reference

- **CORE-EEAT**: A07 (Knowledge Graph Presence) scored Fail, A08 (Entity Consistency) scored Pass -- entity optimization should focus on knowledge base gaps rather than consistency
- **CITE**: I-dimension weakest area is I01 (Knowledge Graph Presence) -- completing Wikidata entry and earning Knowledge Panel directly improves domain identity score
```

## 成功技巧

1. **从维基数据开始**：它是最具影响力的可编辑知识库；一个完整的维基数据条目通常能在几周内触发知识面板的创建。
2. `sameAs`属性是Schema.org中最有力的标识方式——它直接告诉搜索引擎“我是知识图谱中的这个实体”；务必首先添加维基数据的URL。
3. 在优化前后测试AI的识别能力——分别在优化前后查询ChatGPT、Claude、Perplexity和Google AI Overview；这是最直接的地理信息评估指标。
4. 实体信号是相互加强的——与内容SEO不同，来自不同来源的实体信号会相互增强；5个薄弱的信号比1个强的信号更有效。
5. 一致性比完整性更重要——在10个平台上保持实体名称和描述的一致性，比仅在2个平台上拥有完美的资料更有效。
6. **不要忽视歧义处理**：如果实体名称与其他实体重复，歧义处理是首要任务；否则其他信号都将无效。
7. **结合CITE I维度进行域名背景信息补充**：实体审核可以告诉你实体被识别的程度；CITE Identity（I01-I10）可以告诉你域名在多大程度上代表了该实体；两者结合使用效果最佳。

## 实体类型参考

### 实体类型及关键信号

| 实体类型 | 主要信号 | 辅助信号 | 关键Schema属性 |
|-------------|----------------|-------------------|------------|
| **人** | 作者页面、社交媒体资料、出版历史 | 演讲记录、奖项、媒体提及 | Person, ProfilePage |
| **组织** | 注册记录、维基数据、行业名录 | 媒体报道、合作伙伴关系、奖项 | Organization, Corporation |
| **品牌** | 商标、品牌搜索量、社交媒体存在感 | 评论、品牌提及、视觉标识 | Brand, Organization |
| **产品** | 产品页面、评论、比较提及 | 奖项、专家推荐、市场份额 | Product, SoftwareApplication |
| **创意作品** | 出版记录、引用、评论 | 奖项、改编情况、文化影响 | CreativeWork, Book, Movie |
| **事件** | 事件列表、媒体报道、社交热度 | 赞助信息、演讲者资料、参与情况 | Event |

### 不同情况下的歧义解决策略

| 情况 | 解决策略 |
|-----------|----------|
| **名称相同但实体不同** | 加强所有信号；让信号量帮助消除歧义 |
| **名称与较大实体冲突** | 一致使用限定词（例如，“Acme Software”而非“Acme”）；广泛使用sameAs属性；建立区分性的主题关联 |
| **名称与相似实体冲突** | 使用地理、行业或产品限定词；确保Schema @id的唯一性和一致性；优先处理维基数据的歧义处理 |
| **缩写/首字母缩写冲突** | 在结构化数据中使用全称；仅在实体已被广泛认可的情况下使用缩写 |
| **合并或重命名的实体** | 重定向旧的实体信号；更新所有结构化数据；创建“曾被称为……”的内容；更新维基数据 |

## 知识面板优化（Knowledge Panel Optimization）

### 声明和编辑

1. **谷歌知识面板**：通过谷歌的验证流程进行声明（搜索实体 → 点击“声明此知识面板”）
2. **必应知识面板**：由维基数据和LinkedIn驱动——更新这些来源的信息
3. **AI知识面板**：由训练数据驱动——确保权威来源正确描述实体

### 常见的知识面板问题

| 问题 | 原因 | 解决方法 |
|-------|-----------|-----|
| 无知识面板显示 | 实体未收录在知识图谱中 | 创建维基数据条目 + 结构化数据 + 权威来源的提及 |
| 图片错误 | 图片来自错误页面 | 更新维基数据中的图片；确保关于页面和社交媒体资料中的图片正确 |
| 描述错误 | 描述来自错误来源 | 编辑维基数据中的描述；确保关于页面的第一段中有清晰的实体描述 |
| 属性缺失 | 结构化数据不完整 | 向Schema.org和维基数据中添加属性 |
| 显示的实体错误 | 歧义处理失败 | 加强独特信号；添加限定词；解决维基数据的歧义 |
| 信息过时 | 来源数据未更新 | 更新维基数据、关于页面和所有资料页面 |

## 维基数据最佳实践

### 创建维基数据条目

1. **检查知名度**：实体必须至少有一个权威来源的引用
2. **创建条目**：添加标签、描述和多种语言的别名
3. **添加信息**：实体实例、官方网站、社交媒体链接、成立日期、创始人、所属行业
4. **添加标识符**：官方网站（P856）、社交媒体ID、CrunchBase ID、ISNI、VIAF
5. **添加引用**：每个信息都应引用权威来源

**重要提示**：维基百科的冲突利益（Conflict of Interest, COI）政策禁止个人和组织为自己创建或编辑条目。因此：（1）通过独立可靠的来源（媒体报道、行业出版物、学术引用）来建立知名度；（2）如果认为维基百科条目有必要，可以通过“请求文章”流程联系独立编辑；（3）在参与维基百科编辑之前，确保所有关于实体的声明都可通过第三方来源验证。

### 不同实体类型的维基数据关键属性

| 属性 | 代码 | 人 | 组织 | 品牌 | 产品 |
|----------|------|:------:|:---:|:-----:|:-------:|
| 实体实例 | P31 | human | organization type | brand | product type |
| 官方网站 | P856 | yes | yes | yes | yes |
| 职业/行业 | P106/P452 | yes | yes | — | — |
| 成立者 | P112 | — | yes | yes | yes |
| 成立时间 | P571 | — | yes | yes | yes |
| 国家 | P17 | yes | yes | — | — |
| 社交媒体 | various | yes | yes | yes | yes |
| 雇主 | P108 | yes | — | — | — |
| 开发者 | P178 | — | — | — | yes |

## AI实体优化

### AI系统如何识别实体

AI系统遵循以下流程：
1. **提取**：从查询中提取实体提及
2. **识别**：将每个提及的实体与已知实体匹配（或返回“不确定”）
3. **检索**：获取关于该实体的相关信息
4. **生成**：引用确认实体属性的来源的响应

### AI系统用于实体识别的信号类型

| 信号类型 | AI的验证方式 | 优化方法 |
|-------------|---------------|-----------------|
| **训练数据中的存在** | 实体是否出现在训练数据中？ | 是否在高质量、广泛爬取的来源中被提及 |
| **检索增强** | 实体是否出现在实时搜索结果中？ | 对于品牌相关查询，是否有较强的SEO存在感 |
| **结构化数据** | 实体能否与知识图谱匹配？ | 是否有完整的维基数据和Schema.org信息 |
| **上下文共现** | 实体出现在哪些主题/实体旁边？ | 在内容中建立一致的主题关联 |
| **来源权威性** | 来源是否可靠？ | 是否被权威、知名的来源提及 |
| **时效性** | 信息是否最新？ | 确保所有实体资料和内容都是最新的 |

### 实体特定的地理信息策略

1. **明确定义**：关于页面和关键页面的第一段应清晰定义实体，以便AI可以直接引用
2. **保持一致性**：在所有平台上使用相同的实体描述
3. **建立关联**：创建明确将实体与目标主题联系起来的内容
4. **获得提及**：第三方权威机构的提及比自我描述更具有说服力
5. **保持更新**：过时的实体信息会导致AI失去信心，从而停止引用

## 参考资料

- [references/entity-signal-checklist.md](./references/entity-signal-checklist.md) — 完整的信号检查清单及验证方法
- [references/knowledge-graph-guide.md](./references/knowledge-graph-guide.md) — 维基数据、维基百科和知识图谱优化指南

## 相关技能

- [content-quality-auditor](../content-quality-auditor/) — 直接关联CORE-EEAT A07（知识图谱存在性）和A08（实体一致性）项目
- [domain-authority-auditor](../domain-authority-auditor/) — CITE I01-I10（身份维度）用于衡量域级别的实体信号
- [schema-markup-generator](../../build/schema-markup-generator/) — 生成组织、人物、产品等实体的Schema结构
- [geo-content-optimizer](../../build/geo-content-optimizer/) — 实体信号影响AI的引用概率
- [competitor-analysis](../../research/competitor-analysis/) — 与竞争对手比较实体的存在情况
- [backlink-analyzer](../../monitor/backlink-analyzer/) — 品牌反向链接增强实体信号
- [performance-reporter](../../monitor/performance-reporter/) — 跟踪品牌搜索和知识面板的指标
- [memory-management](../memory-management/) — 存储实体审核结果以供长期跟踪