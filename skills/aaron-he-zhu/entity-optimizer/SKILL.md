---
name: entity-optimizer
description: '当用户请求“优化实体的展示效果”、“构建知识图谱”、“改进知识面板”或“进行实体审计”时，请使用该工具。该工具可独立使用，支持公共搜索和人工智能查询测试；当您将其与“知识图谱”+“SEO工具”+“人工智能监控”相结合时，其功能将得到进一步增强，实现自动化的实体分析。'
geo-relevance: "high"
---

# 实体优化器

该技能用于审计、构建和维护搜索引擎及人工智能系统中的实体身份。实体（即搜索引擎和人工智能系统能够识别为独立存在的个人、组织、产品或概念）是谷歌和大型语言模型（LLMs）判断“你是谁”以及“是否应该引用你”的基础。

**实体对SEO和地理信息（GEO）的重要性：**

- **SEO**：谷歌的知识图谱（Knowledge Graph）为知识面板（Knowledge Panels）、丰富搜索结果以及基于实体的排名信号提供了支持。一个定义明确的实体能够在搜索结果页面（SERP）中获得更好的展示位置。
- **GEO**：人工智能系统在生成答案之前会将查询结果映射到相应的实体上。如果人工智能无法识别你的实体，无论你的内容多么优秀，也无法被引用。

## 何时使用此技能

- 建立一个新的品牌/个人/产品作为被认可的实体
- 审计实体在知识图谱、维基数据（Wikidata）和人工智能系统中的存在情况
- 改进或修正知识面板
- 建立实体之间的关联（实体与主题、实体与行业之间的关联）
- 解决实体歧义问题（你的实体与其他实体被混淆）
- 加强实体被引用的信号
- 在推出新品牌、产品或组织后
- 为网站迁移做准备（保持实体身份的一致性）
- 定期进行实体健康检查

## 该技能的功能

1. **实体审计**：评估实体在搜索引擎和人工智能系统中的当前存在情况
2. **知识图谱分析**：检查谷歌知识图谱、维基数据和维基百科的状态
3. **人工智能实体识别测试**：查询人工智能系统，了解它们如何识别和描述该实体
4. **实体信号映射**：识别所有用于确立实体身份的信号
5. **差距分析**：找出缺失或薄弱的实体信号
6. **实体构建计划**：制定可行的计划以建立或加强实体的存在感
7. **歧义解决策略**：解决同名实体之间的混淆问题

## 使用方法

### 实体审计

```
Audit entity presence for [brand/person/organization]
```

```
How well do search engines and AI systems recognize [entity name]?
```

### 建立实体存在感

```
Build entity presence for [new brand] in the [industry] space
```

```
Establish [person name] as a recognized expert in [topic]
```

### 解决实体问题

```
My Knowledge Panel shows incorrect information — fix entity signals for [entity]
```

```
AI systems confuse [my entity] with [other entity] — help me disambiguate
```

## 数据来源

> 有关工具类别的占位符，请参见 [CONNECTORS.md](../../CONNECTORS.md)。

**当连接了知识图谱（knowledge graph）、SEO工具（SEO tool）、AI监控工具（AI monitor）和品牌监控工具（brand monitor）时：**
- 通过知识图谱API查询实体状态
- 从SEO工具中提取品牌搜索数据
- 使用AI监控工具测试实体被引用的情况
- 通过品牌监控工具跟踪品牌提及次数

**仅使用手动数据时：**
- 请用户提供以下信息：
  - 实体名称、类型（个人、组织、品牌、产品、创意作品、事件）
  - 主要网站/域名
  - 已知的现有资料来源（维基百科、维基数据、社交媒体、行业目录）
  - 实体应关联的前三到五个主题/行业
  - 任何已知的歧义问题（其他具有相同或相似名称的实体）

在没有工具的情况下，Claude会根据用户提供的信息提供实体优化策略和建议。用户需要自行执行搜索查询、检查知识面板并测试人工智能系统的响应，以提供分析所需的原始数据。

请使用公开搜索结果、人工智能查询测试和搜索结果页面（SERP）分析来进行审计。注意哪些项目需要工具支持才能进行完整评估。

## 指令

当用户请求实体优化时：

### 第一步：实体发现

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

### 第二步：实体信号审计

评估六个类别中的实体信号。有关详细的47个信号检查清单及验证方法，请参见 [references/entity-signal-checklist.md](./references/entity-signal-checklist.md)。

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

### 第三步：报告与行动计划

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

## 验证检查点

### 输入验证
- [ ] 实体名称和类型已确认
- [ ] 主要域名/网站已确认
- [ ] 目标主题/行业已指定
- [ ] 如果实体名称常见，提供了歧义解决的相关信息

### 输出验证
- [ ] 所有六个信号类别均已评估
- [ ] 使用至少三个查询测试了人工智能对实体的识别能力
- [ ] 检查了知识面板的状态
- [ ] 验证了维基数据和维基百科的状态
- [ ] 已审核了主要网站上的Schema.org标记
- [ ] 每条建议都具体且可操作
- [ ] 行动计划包含了具体的步骤和时间表
- [ ] 与CORE-EEAT A07/A08和CITE I01-I10进行了交叉核对

## 示例

**用户**：“审计我们的B2B SaaS分析平台CloudMetrics在cloudmetrics.io上的实体存在情况”

**输出**：

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

1. **从维基数据开始**——它是最具影响力的可编辑知识库；一个完整的维基数据条目通常会在几周内触发知识面板的创建。
2. `sameAs` 是最强大的Schema.org属性——它直接告诉搜索引擎“我是知识图谱中的这个实体”；务必首先包含维基数据的URL。
3. **优化前后测试人工智能的识别能力**——在优化前后分别查询ChatGPT、Claude、Perplexity和Google AI Overview；这是最直接的地理信息（GEO）指标。
4. **实体信号是相互叠加的**——与内容SEO不同，来自不同来源的实体信号会相互增强；5个薄弱的信号加起来比1个强信号更有效。
5. **一致性比完整性更重要**——在10个平台上保持实体名称和描述的一致性，比仅在2个平台上拥有完美的资料更有效。
6. **不要忽视歧义问题**——如果你的实体名称与其他实体相同，解决歧义是首要任务；否则所有其他信号都将无效。
7. **结合CITE I维度来提供领域背景**——实体审计可以告诉你实体被识别的程度；CITE Identity（I01-I10）可以告诉你该领域在多大程度上代表了该实体；两者结合使用效果最佳。

## 实体类型参考

### 实体类型及关键信号

| 实体类型 | 主要信号 | 辅助信号 | 关键Schema属性 |
|-------------|----------------|-------------------|------------|
| **个人** | 作者页面、社交媒体资料、出版历史 | 演讲记录、获奖情况、媒体提及 | Person, ProfilePage |
| **组织** | 注册记录、维基数据、行业列表 | 媒体报道、合作伙伴关系、获奖情况 | Organization, Corporation |
| **品牌** | 商标、品牌搜索量、社交媒体存在感 | 评论、品牌提及、视觉标识 | Brand, Organization |
| **产品** | 产品页面、评论、比较提及 | 获奖情况、专家推荐、市场份额 | Product, SoftwareApplication |
| **创意作品** | 出版记录、引用情况、评论 | 获奖情况、改编情况、文化影响 | CreativeWork, Book, Movie |
| **事件** | 事件列表、媒体报道、社交媒体讨论 | 赞助情况、演讲者资料、参与情况 | Event |

### 根据不同情况制定的歧义解决策略

| 情况 | 解决策略 |
|-----------|----------|
| **名称相同但实体不同** | 加强所有信号；让信号量来消除歧义 |
| **名称与较大实体冲突** | 一致使用限定词（例如，使用“Acme Software”而不是“Acme”）；建立特定领域的权威性来区分 |
| **名称与相似实体冲突** | 使用地理、行业或产品限定词；确保Schema @id的唯一性和一致性；优先处理维基数据的歧义解决 |
| **缩写/首字母缩写冲突** | 在结构化数据中优先使用全名；仅在实体已确立的上下文中使用缩写 |
| **合并或重命名的实体** | 重定向旧的实体信号；更新所有结构化数据；创建明确的“ formerly known as”内容；更新维基数据 |

## 知识面板优化

### 声明和编辑

1. **谷歌知识面板**：通过谷歌的验证流程进行声明（搜索实体 → 点击“Claim this knowledge panel”）
2. **必应知识面板**：由维基数据和LinkedIn驱动——更新这些来源的信息
3. **AI知识面板**：由训练数据驱动——确保权威来源正确描述实体

### 常见的知识面板问题

| 问题 | 根本原因 | 解决方法 |
|-------|-----------|-----|
| 没有知识面板显示 | 实体不在知识图谱中 | 创建维基数据条目 + 结构化数据 + 权威性提及 |
| 图片错误 | 图片来自错误的页面 | 更新维基数据中的图片；确保关于页面和社交媒体资料中的图片是正确的 |
| 描述错误 | 描述来自错误的来源 | 编辑维基数据中的描述；确保关于页面的第一段中有明确的实体描述 |
| 属性缺失 | 结构化数据不完整 | 向Schema.org标记和维基数据条目中添加属性 |
| 显示的实体错误 | 歧义解决失败 | 加强独特信号；添加限定词；解决维基数据的歧义 |
| 信息过时 | 来源数据未更新 | 更新维基数据、关于页面和所有资料页面 |

## 维基数据最佳实践

### 创建维基数据条目

1. **检查知名度**：实体必须至少有一个权威性的参考来源
2. **创建条目**：添加标签、描述和多种语言的别名
3. **添加信息**：实例、官方网站、社交媒体链接、成立日期、创始人、行业
4. **添加标识符**：官方网站（P856）、社交媒体ID、CrunchBase ID、ISNI、VIAF
5. **添加参考来源**：每个信息都应该有权威来源的引用

**重要提示**：维基百科的冲突利益（Conflict of Interest, COI）政策禁止个人和组织为自己创建或编辑条目。因此，不建议直接编辑维基百科：(1) 通过独立的可靠来源（媒体报道、行业出版物、学术引用）来建立知名度；(2) 如果认为需要编辑维基百科条目，可以通过“请求文章”（Requested Articles）流程联系独立的维基百科编辑；(3) 在任何涉及维基百科之前，确保关于实体的所有声明都可通过第三方来源进行验证。

### 不同实体类型的维基数据关键属性

| 属性 | 代码 | 个人 | 组织 | 品牌 | 产品 |
|----------|------|:------:|:---:|:-----:|:-------:|
| 实例 | P31 | human | organization type | brand | product type |
| 官方网站 | P856 | yes | yes | yes | yes |
| 职业/行业 | P106/P452 | yes | yes | — | — |
| 创立者 | P112 | — | yes | yes | yes |
| 成立时间 | P571 | — | yes | yes | yes |
| 国家 | P17 | yes | yes | — | — |
| 社交媒体 | various | yes | yes | yes | yes |
| 雇主 | P108 | yes | — | — | — |
| 开发者 | P178 | — | — | — | yes |

## 人工智能实体优化

### 人工智能系统如何识别实体

```
User query → Entity extraction → Entity resolution → Knowledge retrieval → Answer generation
```

人工智能系统遵循以下流程：
1. **提取** 查询中的实体提及
2. **识别** 每个提及对应的实体（或无法识别 → 显示“我不确定”）
3. **检索** 与该实体相关的信息
4. **生成** 引用确认实体属性的来源的响应

### 人工智能用于实体识别的信号类型

| 信号类型 | 人工智能检查内容 | 优化方法 |
|-------------|---------------|-----------------|
| **训练数据中的存在** | 该实体是否出现在训练数据集中？ | 是否在高质量、广泛爬取的来源中被提及 |
| **检索增强** | 该实体是否出现在实时搜索结果中？ | 对于品牌查询，该实体在搜索结果中的显示频率是否高 |
| **结构化数据** | 该实体是否与知识图谱匹配？ | 维基数据和Schema.org的数据是否完整 |
| **上下文共现** | 该实体与哪些主题/实体一起出现？ | 在内容中建立一致的主题关联 |
| **来源权威性** | 来源是否可靠？ | 来源是否来自权威、知名的来源 |
| **时效性** | 信息是否最新？ | 确保所有实体资料和内容都是最新的 |

### 实体特定的地理信息（GEO）策略

1. **明确定义**：关于页面和关键页面的第一段应明确描述实体，以便人工智能可以直接引用
2. **保持一致性**：在所有平台上使用相同的实体描述
3. **建立关联**：创建明确将实体与目标主题联系起来的内容
4. **获得提及**：第三方权威性的提及比自我描述更具说服力
5. **保持更新**：过时的实体信息会导致人工智能失去信心，从而停止引用

## 参考资料

关于实体优化的详细指南：
- [references/entity-signal-checklist.md](./references/entity-signal-checklist.md) — 完整的信号检查清单及验证方法
- [references/knowledge-graph-guide.md](./references/knowledge-graph-guide.md) — 维基数据、维基百科和知识图谱优化指南

## 相关技能

- [content-quality-auditor](../content-quality-auditor/) — 直接关联到CORE-EEAT的A07（知识图谱存在性）和A08（实体一致性）项目
- [domain-authority-auditor](../domain-authority-auditor/) — CITE I01-I10（身份维度）用于衡量领域层面的实体信号
- [schema-markup-generator](../../build/schema-markup-generator/) — 生成组织、个人、产品等实体的Schema结构
- [geo-content-optimizer](../../build/geo-content-optimizer/) — 实体信号影响人工智能的引用概率
- [competitor-analysis](../../research/competitor-analysis/) — 与竞争对手比较实体的存在情况
- [backlink-analyzer](../../monitor/backlink-analyzer/) — 品牌链接增强实体信号
- [performance-reporter](../../monitor/performance-reporter/) — 跟踪品牌搜索和知识面板的指标
- [memory-management](../memory-management/) — 存储实体审计结果以供长期跟踪