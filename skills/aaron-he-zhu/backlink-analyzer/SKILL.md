---
name: backlink-analyzer
description: '**使用场景：**  
当用户请求“分析反向链接”、“检查链接质量”、“查找有害链接”、“寻找链接建设机会”、“进行站外SEO优化”、“了解哪些网站链接到了我的网站”、“我的网站中有垃圾链接”、“如何获得更多反向链接”或“取消某些链接的关联”时，可以使用该工具。该工具能够分析反向链接的来源、质量及权威性，识别有害链接，发现潜在的链接建设机会，并监控竞争对手的链接获取情况。对于站内链接分析，请参考“internal-linking-optimizer”；关于竞争对手的链接分析，请参阅“competitor-analysis”。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "low"
  tags:
    - seo
    - backlinks
    - link building
    - link profile
    - toxic links
    - off-page seo
    - link authority
    - domain authority
    - link acquisition
  triggers:
    - "analyze backlinks"
    - "check link profile"
    - "find toxic links"
    - "link building opportunities"
    - "off-page SEO"
    - "backlink audit"
    - "link quality"
    - "who links to me"
    - "I have spammy links"
    - "how do I get more backlinks"
    - "disavow links"
---

# 反链分析工具

> **[SEO与地理定位技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理定位相关技能 · 全部技能安装方式：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容撰写工具](../../build/seo-content-writer/) · [地理内容优化工具](../../build/geo-content-optimizer/) · [元标签优化工具](../../build/meta-tags-optimizer/) · [schema标记生成工具](../../build/schema-markup-generator/)

**优化** · [页面SEO审核工具](../../optimize/on-page-seo-auditor/) · [技术SEO检查工具](../../optimize/technical-seo-checker/) · [内部链接优化工具](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名追踪工具](../rank-tracker/) · **反链分析工具** · [性能报告工具](../performance-reporter/) · [警报管理工具](../alert-manager/)

**跨领域工具** · [内容质量审核工具](../../cross-cutting/content-quality-auditor/) · [域名权威性审核工具](../../cross-cutting/domain-authority-auditor/) · [实体优化工具](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

此工具可帮助您分析、监控和优化您的反链状况。它能够识别链接的质量，发现潜在的链接构建机会，并追踪竞争对手的链接构建活动。

## 适用场景

- 审核当前的反链情况
- 识别有害或不良链接
- 发现链接构建的机会
- 分析竞争对手的链接构建策略
- 监控新链接和丢失的链接
- 评估用于外联的链接质量
- 为链接删除请求做准备

## 功能介绍

1. **概况分析**：提供全面的反链状况概览
2. **质量评估**：评估链接的权威性和相关性
3. **有害链接检测**：识别有害链接
4. **竞争对手分析**：比较不同竞争对手的反链情况
5. **机会发现**：寻找链接构建的潜在机会
6. **趋势监控**：跟踪链接获取的变化
7. **删除请求指导**：协助生成链接删除请求文件

## 使用方法

### 分析您的反链状况

```
Analyze backlink profile for [domain]
```

### 发现链接构建机会

```
Find link building opportunities by analyzing [competitor domains]
```

### 识别问题

```
Check for toxic backlinks on [domain]
```

### 比较竞争对手的反链状况

```
Compare backlink profiles: [your domain] vs [competitor domains]
```

## 数据来源

> 请参阅[CONNECTORS.md](../../CONNECTORS.md)以了解工具类别的相关信息。

**当与 ~~链接数据库** 和 ~~SEO工具** 配合使用时：  
- 自动从 ~~链接数据库** 中获取包括引用域名、锚文本分布、链接质量指标（DA/DR）、链接速度和有害链接检测在内的全面反链信息；  
- 从 ~~SEO工具** 中获取竞争对手的反链数据，用于对比分析。

**仅使用手动数据时：**  
- 要求用户提供以下数据：  
  - 反链导出CSV文件（包含来源域名、锚文本、链接类型）  
  - 带有权威性指标的引用域名列表  
  - 用于比较的竞争对手域名  
  - 最近的链接增减情况（如需追踪变化）  
  - 任何已知的有害或垃圾链接  

**使用提供的数据进行完整分析**。在输出结果中明确标注哪些指标来自自动化收集，哪些来自用户提供的数据。

## 操作步骤

当用户请求反链分析时：

1. **生成概况报告**  
   ```markdown
   ## Backlink Profile Overview
   
   **Domain**: [domain]
   **Analysis Date**: [date]
   
   ### Key Metrics
   
   | Metric | Value | Industry Avg | Status |
   |--------|-------|--------------|--------|
   | Total Backlinks | [X] | [Y] | [Above/Below avg] |
   | Referring Domains | [X] | [Y] | [status] |
   | Domain Authority | [X] | [Y] | [status] |
   | Domain Rating | [X] | [Y] | [status] |
   | Dofollow Links | [X] ([Y]%) | [Z]% | [status] |
   | Nofollow Links | [X] ([Y]%) | [Z]% | [status] |
   
   ### Link Velocity
   
   | Period | New Links | Lost Links | Net Change |
   |--------|-----------|------------|------------|
   | Last 30 days | [X] | [Y] | [+/-Z] |
   | Last 90 days | [X] | [Y] | [+/-Z] |
   | Last year | [X] | [Y] | [+/-Z] |
   
   ### Authority Distribution
   
   ```  
   DA 80-100： ████ [X]%  
   DA 60-79： ██████ [X]%  
   DA 40-59： ████████████ [X]%  
   DA 20-39： ████████████████ [X]%  
   DA 0-19： ██████████ [X]%  
   ```
   
   **Profile Health Score**: [X]/100
   ```

2. **分析链接质量**  
   ```markdown
   ## Link Quality Analysis
   
   ### Top Quality Backlinks
   
   | Source Domain | DA | Link Type | Anchor | Target Page |
   |---------------|-----|-----------|--------|-------------|
   | [domain 1] | [DA] | Editorial | [anchor] | [page] |
   | [domain 2] | [DA] | Guest Post | [anchor] | [page] |
   | [domain 3] | [DA] | Resource | [anchor] | [page] |
   
   ### Link Type Distribution
   
   | Type | Count | Percentage | Assessment |
   |------|-------|------------|------------|
   | Editorial | [X] | [Y]% | ✅ High quality |
   | Guest posts | [X] | [Y]% | ✅ Good |
   | Resource pages | [X] | [Y]% | ✅ Good |
   | Directory | [X] | [Y]% | ⚠️ Moderate |
   | Forum/Comments | [X] | [Y]% | ⚠️ Low quality |
   | Sponsored/Paid | [X] | [Y]% | ⚠️ Risky |
   
   ### Anchor Text Analysis
   
   | Anchor Type | Count | Percentage | Status |
   |-------------|-------|------------|--------|
   | Brand name | [X] | [Y]% | ✅ Natural |
   | Exact match | [X] | [Y]% | ⚠️ [Warning if >30%] |
   | Partial match | [X] | [Y]% | ✅ Natural |
   | URL/Naked | [X] | [Y]% | ✅ Natural |
   | Generic | [X] | [Y]% | ✅ Natural |
   
   **Top Anchor Texts**:
   1. "[anchor 1]" - [X] links
   2. "[anchor 2]" - [X] links
   3. "[anchor 3]" - [X] links
   
   ### Geographic Distribution
   
   | Country | Links | Percentage |
   |---------|-------|------------|
   | [Country 1] | [X] | [Y]% |
   | [Country 2] | [X] | [Y]% |
   | [Country 3] | [X] | [Y]% |
   ```

3. **识别有害链接**  
   ```markdown
   ## Toxic Link Analysis
   
   ### Risk Summary
   
   **Toxic Score**: [X]/100
   **High Risk Links**: [X]
   **Medium Risk Links**: [X]
   **Action Required**: [Yes/No]
   
   ### Toxic Link Indicators
   
   | Risk Type | Count | Examples |
   |-----------|-------|----------|
   | Spammy domains | [X] | [domains] |
   | Link farms | [X] | [domains] |
   | PBN suspected | [X] | [domains] |
   | Irrelevant sites | [X] | [domains] |
   | Foreign language spam | [X] | [domains] |
   | Penalized domains | [X] | [domains] |
   
   ### High-Risk Links to Review
   
   | Source Domain | Risk Score | Issue | Recommendation |
   |---------------|------------|-------|----------------|
   | [domain 1] | 95/100 | Link farm | Disavow |
   | [domain 2] | 85/100 | Spam site | Disavow |
   | [domain 3] | 72/100 | PBN | Investigate |
   
   ### Disavow Recommendations
   
   **Domains to disavow** ([X] total):
   ```  
   domain:[spam-site-1.com]  
   domain:[spam-site-2.com]  
   domain:[link-farm.com]  
   ```
   
   **Individual URLs to disavow** ([X] total):
   ```  
   [specific-url-1]  
   [specific-url-2]  
   ```
   ```

4. **与竞争对手对比**  
   ```markdown
   ## Competitive Backlink Analysis
   
   ### Profile Comparison
   
   | Metric | You | Competitor 1 | Competitor 2 | Competitor 3 |
   |--------|-----|--------------|--------------|--------------|
   | Referring Domains | [X] | [X] | [X] | [X] |
   | Domain Authority | [X] | [X] | [X] | [X] |
   | Domain Rating | [X] | [X] | [X] | [X] |
   | Link Velocity (30d) | [X] | [X] | [X] | [X] |
   | Avg Link DA | [X] | [X] | [X] | [X] |
   
   ### Unique Referring Domains
   
   **Links only you have**: [X] domains
   **Links competitors share**: [X] domains  
   **Links competitors have, you don't**: [X] domains ⬅️ Opportunity
   
   ### Link Intersection Analysis
   
   **Sites linking to competitors but not you**:
   
   | Domain | DA | Links to Comp 1 | Comp 2 | Comp 3 | Opportunity |
   |--------|-----|-----------------|--------|--------|-------------|
   | [domain 1] | [DA] | ✅ | ✅ | ✅ | High - All competitors |
   | [domain 2] | [DA] | ✅ | ✅ | ❌ | High - 2 competitors |
   | [domain 3] | [DA] | ✅ | ❌ | ❌ | Medium - 1 competitor |
   
   ### Content Getting Most Links (Competitor Analysis)
   
   | Competitor | Content | Backlinks | Content Type |
   |------------|---------|-----------|--------------|
   | [Comp 1] | [Title/URL] | [X] | [Type] |
   | [Comp 2] | [Title/URL] | [X] | [Type] |
   | [Comp 3] | [Title/URL] | [X] | [Type] |
   
   **Insight**: [What content types attract most links in this niche]
   ```

5. **寻找链接构建机会**  
   ```markdown
   ## Link Building Opportunities
   
   ### High-Priority Opportunities
   
   #### 1. Link Intersection Prospects
   
   Sites linking to multiple competitors but not you:
   
   | Domain | DA | Why Link | Contact Approach |
   |--------|-----|----------|------------------|
   | [domain 1] | [DA] | [resource page about X] | Suggest your resource |
   | [domain 2] | [DA] | [links to similar tools] | Pitch your tool |
   | [domain 3] | [DA] | [industry roundup] | Request inclusion |
   
   #### 2. Broken Link Opportunities
   
   | Source Page | Broken Link | Suggested Replacement |
   |-------------|-------------|----------------------|
   | [URL] | [broken URL] | [your relevant page] |
   | [URL] | [broken URL] | [your relevant page] |
   
   #### 3. Unlinked Mentions
   
   | Site | Mention | Your Page to Link |
   |------|---------|-------------------|
   | [domain] | Mentioned your brand | [homepage] |
   | [domain] | Referenced your data | [research page] |
   
   #### 4. Resource Page Opportunities
   
   | Resource Page | Topic | Your Relevant Content |
   |---------------|-------|----------------------|
   | [URL] | [topic] | [your content] |
   | [URL] | [topic] | [your content] |
   
   #### 5. Guest Post Prospects
   
   | Site | DA | Topic Fit | Contact |
   |------|-----|-----------|---------|
   | [domain] | [DA] | [relevance] | [contact info/page] |
   | [domain] | [DA] | [relevance] | [contact info/page] |
   
   ### Link Building Priority Matrix
   
   | Opportunity Type | Effort | Impact | Priority |
   |------------------|--------|--------|----------|
   | Link intersection | Medium | High | ⭐⭐⭐⭐⭐ |
   | Broken links | Low | Medium | ⭐⭐⭐⭐ |
   | Unlinked mentions | Low | Medium | ⭐⭐⭐⭐ |
   | Resource pages | Medium | High | ⭐⭐⭐⭐ |
   | Guest posts | High | High | ⭐⭐⭐ |
   ```

6. **跟踪链接变化**  
   ```markdown
   ## Link Change Tracking
   
   ### New Links (Last 30 Days)
   
   | Source | DA | Type | Anchor | Date |
   |--------|-----|------|--------|------|
   | [domain 1] | [DA] | [type] | [anchor] | [date] |
   | [domain 2] | [DA] | [type] | [anchor] | [date] |
   | [domain 3] | [DA] | [type] | [anchor] | [date] |
   
   **Total new links**: [X]
   **Average DA of new links**: [X]
   **Best new link**: [domain] (DA [X])
   
   ### Lost Links (Last 30 Days)
   
   | Source | DA | Reason | Action |
   |--------|-----|--------|--------|
   | [domain 1] | [DA] | Page removed | Reach out |
   | [domain 2] | [DA] | Link removed | Investigate |
   | [domain 3] | [DA] | Site down | Monitor |
   
   **Total lost links**: [X]
   **Net change**: [+/-X]
   
   ### Links to Recover
   
   | Lost Link | Value | Recovery Strategy |
   |-----------|-------|-------------------|
   | [domain 1] | High | Contact webmaster |
   | [domain 2] | High | Update content they linked to |
   ```

7. **生成反链报告**  
   ```markdown
   # Backlink Analysis Report
   
   **Domain**: [domain]
   **Report Date**: [date]
   **Period Analyzed**: [period]
   
   ## Executive Summary
   
   Your backlink profile is [healthy/needs attention/concerning].
   
   **Key Stats**:
   - Referring domains: [X] ([+/-Y] vs last month)
   - Average link authority: [X] DA
   - Link velocity: [X] new links/month
   - Toxic link percentage: [X]%
   
   ## Profile Strengths
   
   1. ✅ [Strength 1]
   2. ✅ [Strength 2]
   3. ✅ [Strength 3]
   
   ## Areas of Concern
   
   1. ⚠️ [Concern 1]
   2. ⚠️ [Concern 2]
   
   ## Opportunities Identified
   
   | Opportunity | Potential Links | Effort | Priority |
   |-------------|-----------------|--------|----------|
   | Link intersection | [X] sites | Medium | High |
   | Broken links | [X] sites | Low | High |
   | Resource pages | [X] sites | Medium | Medium |
   
   ## Competitive Position
   
   Your referring domains rank #[X] among [Y] competitors.
   
   | Rank | Domain | Referring Domains |
   |------|--------|-------------------|
   | 1 | [domain] | [X] |
   | 2 | [domain] | [X] |
   | 3 | [domain] | [X] |
   
   ## Recommended Actions
   
   ### Immediate (This Week)
   - [ ] Disavow [X] toxic links identified
   - [ ] Reach out to [X] unlinked mentions
   
   ### Short-term (This Month)
   - [ ] Pursue [X] link intersection opportunities
   - [ ] Fix [X] broken link opportunities
   - [ ] Recover [X] recently lost links
   
   ### Long-term (This Quarter)
   - [ ] Create linkable asset targeting [topic]
   - [ ] Launch guest posting campaign
   - [ ] Build [X] resource page links
   
   ## KPIs to Track
   
   | Metric | Current | 3-Month Target |
   |--------|---------|----------------|
   | Referring domains | [X] | [Y] |
   | Average DA of new links | [X] | [Y] |
   | Link velocity | [X]/mo | [Y]/mo |
   | Toxic link % | [X]% | <5% |
   ```

### CITE数据映射  

在该分析之后运行`domain-authority-auditor`时，以下数据会直接用于CITE评分：  
| 反链指标 | CITE项目 | 维度 |
|----------------|-----------|-----------|
| 引用域名数量 | C01（引用域名数量） | 引用次数 |
| 权威性分布（DA细分） | C02（引用域名的质量） | 引用次数 |
| 链接速度 | C04（链接速度） | 引用次数 |
| 地理分布 | C10（链接来源多样性） | 引用次数 |
| 跟随/非跟随链接比例 | T02（跟随链接比例的合理性） | 信任度 |
| 有害链接分析 | T01（链接的自然性）、T03（链接流量的连贯性） | 信任度 |
| 竞争对手链接交叉情况 | T05（链接的唯一性） | 信任度 |

## 验证要点

### 输入验证  
- 目标域名的反链数据完整且最新  
- 指定了用于对比分析的竞争对手域名  
- 反链数据包含必要的字段（来源域名、锚文本、链接类型）  
- 权威性指标（DA/DR或等效指标）可用  

### 输出验证  
- 每个指标都标明了数据来源和收集日期  
- 有害链接的评估包含风险说明  
- 链接构建建议具体且可操作  
- 明确指出每个数据点的来源（来自~~链接数据库**、~~SEO工具** 或用户提供）

## 示例  

**用户请求**：“通过分析HubSpot、Salesforce和Mailchimp来寻找链接构建机会”

**输出结果**：  
```markdown
## Link Intersection Analysis

### Sites linking to 2+ competitors (not you)

| Domain | DA | HubSpot | Salesforce | Mailchimp | Opportunity |
|--------|-----|---------|------------|-----------|-------------|
| g2.com | 91 | ✅ | ✅ | ✅ | Get listed/reviewed |
| capterra.com | 89 | ✅ | ✅ | ✅ | Submit for review |
| entrepreneur.com | 92 | ✅ | ✅ | ❌ | Pitch guest post |
| techcrunch.com | 94 | ✅ | ❌ | ✅ | PR/news pitch |

### Top 5 Immediate Opportunities

1. **G2.com** (DA 91) - All competitors listed
   - Action: Create detailed G2 profile
   - Effort: Low
   - Impact: High authority + referral traffic

2. **Entrepreneur.com** (DA 92) - 2 competitors have links
   - Action: Pitch contributed article
   - Effort: High
   - Impact: High authority + brand exposure

3. **MarketingProfs** (DA 75) - All competitors featured
   - Action: Apply for expert contribution
   - Effort: Medium
   - Impact: Relevant audience + quality link

### Estimated Impact

If you acquire links from top 10 opportunities:
- New referring domains: +10
- Average DA of new links: 82
- Estimated ranking impact: +2-5 positions for competitive keywords
```

## 成功技巧  

1. **质量优于数量** — 一个DA 80的链接比十个DA 20的链接更有价值  
2. **定期监控** — 及时发现丢失的链接和有害链接  
3. **研究竞争对手** — 学习他们的链接构建方法  
4. **多样化链接来源** — 混合不同类型的链接和锚文本  
5. **谨慎处理链接删除请求** — 仅删除明显有害的链接  

## 链接质量评估框架

### 链接质量评分矩阵  

| 因素 | 权重 | 评分1（低） | 评分3（中等） | 评分5（高） |
|--------|--------|--------------|------------------|----------------|
| 域名权威性 | 25% | DR <20 | DR 20-50 | DR 50+ |
| 主题相关性 | 25% | 不相关或小众主题 | 广泛相关 | 相同主题/领域 |
| 页面流量 | 15% | 无流量 | 有少量流量 | 流量较大 |
| 链接位置 | 15% | 底部/侧边栏 | 正文（通用） | 正文（相关/编辑性） |
| 锚文本 | 10% | 通用/裸链接 | 部分匹配 | 描述性且自然 |
| 链接状态 | 10% | 非跟随/用户生成内容 | 赞助链接（明确标注） | 跟随链接 |

**链接质量总分** = 各因素得分 × 权重  

### 有害链接识别标准  

| 危险信号 | 风险等级 | 应对措施 |
|----------|-----------|--------|
| 来自私人博客网络（PBN） | 高风险 | 删除链接 |
| 付费链接但标记为“非跟随” | 高风险 | 联系网站管理员后删除链接 |
| 来自被黑的/垃圾网站 | 高风险 | 删除链接 |
| 来自低质量网站的精确匹配链接 | 高风险 | 监控并考虑删除链接 |
| 来自链接农场/目录网络的链接 | 高风险 | 删除链接 |
| 来自无关外语网站的链接 | 中等风险 | 监控链接 |
| 网站全局的底部/侧边栏链接 | 中等风险 | 请求删除或设置为“非跟随” |
| 来自抓取工具/自动生成内容的链接 | 中等风险 | 删除链接 |
| 互惠链接策略 | 低至中等风险 | 降低互惠链接的比例 |

## 链接构建策略矩阵

### 策略比较  

| 策略 | 难度 | 可扩展性 | 链接质量 | 成果时间 | 适用场景 |
|----------|-----------|-------------|-------------|-----------------|---------|
| **客座投稿** | 中等 | 中等 | 中等至高 | 1-3个月 | 建立关系并获取链接 |
| **数字公关** | 高 | 高 | 非常高 | 2-6个月 | 增强品牌权威性和高质量链接 |
| **修复失效链接** | 低至中等 | 中等 | 中等 | 1-2个月 | 快速获取链接 |
| **资源页面链接** | 低 | 低 | 中等 | 1-2个月 | 与领域相关的链接 |
| **HARO/主动请求合作** | 中等 | 中等 | 高 | 1-3个月 | 增强权威性和媒体提及 |
| **原创研究** | 高 | 非常高 | 非常高 | 3-6个月 | 长期获取高质量链接 |
| **免费工具/计算器** | 非常高 | 非常高 | 6-12个月 | 被动获取链接 |
| **Skyscraper技术** | 中等 | 低 | 中等至高 | 2-4个月 | 提升特定内容的排名 |
| **未链接的媒体提及** | 低 | 低 | 高 | 1-2周 | 转化现有的品牌提及 |
| **社区互动** | 低 | 低 | 低至中等 | 持续进行 | 建立领域权威性 |

## 链接构建节奏  

| 网站阶段 | 每月目标链接数量 | 策略重点 |
|-----------|-------------------|---------------|
| 新网站（0-6个月） | 5-10个高质量链接 | 客座投稿、资源页面、HARO |
| 发展中网站（6-18个月） | 10-25个高质量链接 | 数字公关、原创研究、Skyscraper技术 |
| 成熟网站（18个月以上） | 维护现有链接 + 战略性链接构建 | 通过内容或数字公关被动获取链接 |

## 外联最佳实践

### 邮件外联框架  

**主题行示例：**  
- “关于[他们的文章标题]的快速问题”  
- “[您的[主题]页面的资源”  
- “[共同联系人]建议我与您联系”  
- “在[他们的页面]发现了一个失效链接”  

**邮件结构：**  
1. 个人化的开场白（提及他们的具体内容——证明您看过该内容）  
2. 提供价值（对对方的好处，而非对您自己的好处）  
3. 提出具体请求（明确且易于执行）  
4. 提供社交证明（简短，不超过一行）  
5. 提供便捷的退订方式（无压力）  

### 外联回复率基准  

| 方法 | 平均回复率 | 平均链接获取率 |
|----------|---------------------|---------------------|
| 修复失效链接 | 8-12% | 3-5% |
| 客座投稿请求 | 5-10% | 2-4% |
| 资源页面外联 | 6-10% | 2-4% |
| 未链接的媒体提及 | 15-25% | 10-15% |
| HARO请求 | 3-8% | 1-3% |
| 数字公关活动 | 5-15% | 2-8% |

## 参考资料  

- [链接质量评分标准](./references/link-quality-rubric.md) — 包含权重因素和有害链接识别标准的评分矩阵  
- [外联模板](./references/outreach-templates.md) — 邮件模板、主题行示例和回复率基准  

## 相关技能  

- **域名权威性审核工具**（../../cross-cutting/domain-authority-auditor/） — 反链数据直接用于CITE评分；在此分析后运行以获得完整的域名评分  
- **竞争对手分析工具**（../../research/competitor-analysis/） — 全面分析竞争对手  
- **内容差距分析工具**（../../research/content-gap-analysis/） — 创建可链接的内容  
- **警报管理工具**（../alert-manager/） — 设置链接警报  
- **性能报告工具**（../performance-reporter/） — 将结果纳入报告  
- **实体优化工具**（../../cross-cutting/entity-optimizer/） — 品牌化链接可增强实体信号