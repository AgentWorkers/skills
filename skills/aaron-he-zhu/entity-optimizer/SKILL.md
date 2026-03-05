---
name: entity-optimizer
version: "3.0.0"
description: '此技能适用于以下场景：用户请求“优化实体展示效果”、“构建知识图谱”、“改进知识面板功能”、“进行实体审计”、“创建品牌实体”、“谷歌无法识别我的品牌”、“没有知识面板”或“将我的品牌确立为独立实体”。该技能可独立使用，适用于公共搜索和人工智能查询测试；当与知识图谱、SEO工具及人工智能监控工具结合使用时，其功能将得到进一步增强（实现自动化实体分析）。关于结构化数据的实现方式，请参考 `schema-markup-generator`；如需针对内容层面进行人工智能优化，请参阅 `geo-content-optimizer`。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
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
    - knowledge-graph
    - google-knowledge-panel
    - entity-seo
    - brand-entity
    - entity-recognition
    - knowledge-base
    - dbpedia
    - brand-presence
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
# 实体优化器 (Entity Optimizer)

> **[SEO与地理信息（SEO & GEO）技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含20项SEO与地理信息相关的技能 · 全部技能可通过 `npx skills add aaron-he-zhu/seo-geo-claude-skills` 安装

<details>
<summary>浏览全部20项技能</summary>

**研究 (Research):**  
- [关键词研究](../../research/keyword-research/)  
- [竞争对手分析](../../research/competitor-analysis/)  
- [搜索引擎排名分析](../../research/serp-analysis/)  
- [内容差距分析](../../research/content-gap-analysis/)  

**构建 (Build):**  
- [SEO内容撰写工具](../../build/seo-content-writer/)  
- [地理内容优化器](../../build/geo-content-optimizer/)  
- [元标签优化器](../../build/meta-tags-optimizer/)  
- [结构化数据生成工具](../../build/schema-markup-generator/)  

**优化 (Optimize):**  
- [页面SEO审核工具](../../optimize/on-page-seo-auditor/)  
- [技术SEO检查工具](../../optimize/technical-seo-checker/)  
- [内部链接优化工具](../../optimize/internal-linking-optimizer/)  
- [内容更新工具](../../optimize/content-refresher/)  

**监控 (Monitor):**  
- [排名跟踪工具](../../monitor/rank-tracker/)  
- [反向链接分析工具](../../monitor/backlink-analyzer/)  
- [性能报告工具](../../monitor/performance-reporter/)  
- [警报管理工具](../../monitor/alert-manager/)  

**跨领域技能 (Cross-cutting Skills):**  
- [内容质量审核工具](../content-quality-auditor/)  
- [域名权威性审核工具](../domain-authority-auditor/)  
- **实体优化器** (Entity Optimizer)  
- [内存管理工具](../memory-management/)  

**功能说明:**  
该工具用于审核、构建并维护实体在搜索引擎和AI系统中的识别度。实体（如人物、组织、产品、概念）是谷歌和大型语言模型（LLMs）判断“品牌是什么”以及“是否应引用该品牌”的基础。  

**实体对SEO与地理信息的重要性:**  
- **SEO**: 谷歌的知识图谱（Knowledge Graph）为知识面板（Knowledge Panels）和基于实体的排名信号提供支持；明确的实体信息有助于提升在搜索结果中的显示位置。  
- **地理信息**: AI系统在生成答案前会先将查询结果映射到相应的实体上；如果无法识别实体，无论内容多么优质，也无法被引用。  

**使用场景:**  
- 建立新的品牌/人物/产品作为被认可的实体  
- 审核实体在知识图谱、Wikidata及AI系统中的存在情况  
- 优化或修正知识面板内容  
- 建立实体与主题/行业的关联  
- 解决实体名称混淆的问题  
- 强化AI系统的实体引用机制  
- 新品牌/产品/组织上线后进行优化  
- 网站迁移前确保实体信息的完整性  

**功能详情:**  
1. **实体审核 (Entity Audit):** 评估实体在搜索引擎和AI系统中的当前状态。  
2. **知识图谱分析 (Knowledge Graph Analysis):** 检查实体在谷歌知识图谱、Wikidata和维基百科中的信息。  
3. **AI实体识别测试 (AI Entity Resolution Test):** 测试AI系统如何识别和描述该实体。  
4. **实体信号映射 (Entity Signal Mapping):** 识别所有用于确立实体身份的信号。  
5. **差距分析 (Gap Analysis):** 发现缺失或薄弱的实体信号。  
6. **实体构建计划 (Entity Building Plan):** 制定具体策略以建立或强化实体存在感。  
7. **消歧策略 (Disambiguation Strategy):** 解决实体名称相似导致的混淆问题。  

**使用方法:**  
- **实体审核 (Entity Audit):** [代码示例]  
- **构建实体存在感 (Build Entity Presence):** [代码示例]  
- **修复实体问题 (Fix Entity Issues):** [代码示例]  

**数据来源:**  
请参阅 [CONNECTORS.md](../../CONNECTORS.md) 以获取工具类别的相关信息。  

**工具集成示例:**  
- 通过连接知识图谱、SEO工具、AI监控工具和品牌监控工具，可以查询实体状态、获取品牌搜索数据、测试AI系统的引用情况以及跟踪品牌提及次数。  
- 如仅使用手动数据，用户需提供以下信息：  
  - 实体名称及类型（人物、组织、品牌、产品、创意作品、事件）  
  - 主要网站/域名  
  - 已知的实体信息来源（维基百科、Wikidata、社交媒体、行业目录）  
  - 实体应关联的顶级3-5个主题/行业  
  - 任何已知的名称混淆问题  

**注意事项:**  
用户需自行执行搜索查询、检查知识面板内容并测试AI系统的响应，以提供分析所需的数据。部分功能需要特定工具的支持。  

**操作步骤:**  
1. **发现实体 (Entity Discovery):** 确定实体在所有系统中的当前状态。  
2. **审核实体信号 (Entity Signal Audit):** 根据[references/entity-signal-checklist.md](./references/entity-signal-checklist.md)中的47项信号标准进行评估。  
3. **生成报告与行动计划 (Report & Action Plan):** 制定具体可行的优化方案。  

**验证要点:**  
- 实体名称和类型已确认。  
- 目标主题/行业已明确。  
- 如实体名称常见，需提供相关消歧信息。  
- 所有6类信号均已完成评估。  
- AI识别测试已通过至少3次查询验证。  
- 实体在知识图谱和维基百科中的状态已核实。  
- 主要网站上的结构化数据标记已审核。  
- 每条建议均具有可操作性，并附有时间表。  

**示例:**  
参见 [references/example-audit-report.md](./references/example-audit-report.md)，了解一家B2B SaaS公司（CloudMetrics）的实体审核报告示例，包括AI识别测试结果、实体健康状况总结及优先行动事项。  

**成功技巧:**  
- **优先使用Wikidata**: 它是最具影响力的可编辑知识库；完整的Wikidata条目通常能在几周内触发知识面板的生成。  
- `sameAs`属性至关重要：它直接告诉搜索引擎“我是知识图谱中的这个实体”。  
- 优化前后需测试AI系统的识别能力。  
- 实体信号具有叠加效应：来自不同来源的信号会相互增强；5个弱信号的总效果优于1个强信号。  
- 一致性比完整性更重要：在多个平台上保持实体名称和描述的统一性。  
- **重视消歧处理**: 若实体名称与其他内容重复，消歧处理是首要任务。  
- **结合CITE I-dimension**: 实体审核可评估实体被识别的程度；CITE Identity（I01-I10）可评估域名对该实体的代表能力。  

**相关参考资料:**  
- [references/entity-type-reference.md](./references/entity-type-reference.md): 提供各类实体的关键信号、结构及消歧策略。  
- [references/knowledge-panel-wikidata-guide.md](./references/knowledge-panel-wikidata-guide.md): 包含知识面板创建/编辑方法、常见问题及解决方案、Wikidata条目生成指南。  

**相关技能:**  
- [content-quality-auditor](../content-quality-auditor/): 直接关联CORE-EEAT A07（知识图谱存在性）和A08（实体一致性）指标。  
- [domain-authority-auditor](../domain-authority-auditor/): 用于评估域名层面的实体信号。  
- [schema-markup-generator](../../build/schema-markup-generator/): 生成组织、人物、产品等实体的结构化数据。  
- [geo-content-optimizer](../../build/geo-content-optimizer/): 增强AI系统的实体引用概率。  
- [competitor-analysis](../../research/competitor-analysis/): 比较实体在竞争对手中的表现。  
- [backlink-analyzer](../../monitor/backlink-analyzer/): 增强实体的反向链接信号。  
- [performance-reporter](../../monitor/performance-reporter/): 跟踪品牌搜索和知识面板指标。  
- [memory-management](../memory-management/): 长期存储实体审核结果以供后续分析。