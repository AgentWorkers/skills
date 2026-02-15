---
name: backlink-analyzer
description: 分析反向链接的概况，以了解链接的权威性、识别有害链接、发现建立链接的机会，并监控竞争对手的链接获取情况。这对离站SEO策略至关重要。
geo-relevance: "low"
---

# 回链分析器

该技能可帮助您分析、监控和优化您的回链状况。它能识别链接的质量，发现潜在的机会，并追踪竞争对手的链接建设活动。

## 适用场景

- 审查当前的回链状况
- 识别有害或不良链接
- 发现链接建设的机会
- 分析竞争对手的链接策略
- 监控新增或丢失的链接
- 评估用于外联的链接质量
- 为链接撤销（disavow）做准备

## 功能概述

1. **回链状况分析**：提供全面的回链概况
2. **质量评估**：评估链接的权威性和相关性
3. **有害链接检测**：识别有害链接
4. **竞争对手分析**：比较不同竞争对手的链接状况
5. **机会发现**：寻找链接建设的潜在机会
6. **趋势监控**：跟踪链接获取的变化
7. **撤销指导**：协助生成链接撤销文件

## 使用方法

### 分析您的回链状况

```
Analyze backlink profile for [domain]
```

### 发现链接建设机会

```
Find link building opportunities by analyzing [competitor domains]
```

### 识别问题链接

```
Check for toxic backlinks on [domain]
```

### 比较竞争对手的回链状况

```
Compare backlink profiles: [your domain] vs [competitor domains]
```

## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md) 以获取工具类别的相关信息。

**当连接到 ~~链接数据库 + ~~SEO 工具时：**
- 自动获取包括引用域名、锚文本分布、链接质量指标（DA/DR）、链接速度和有害链接检测在内的全面回链信息。
- 从 ~~SEO 工具中获取竞争对手的回链数据，用于对比分析。

**仅使用手动数据时：**
- 要求用户提供：
  - 回链数据的 CSV 文件（包含来源域名、锚文本、链接类型）
  - 带有权威性指标的引用域名列表
  - 用于对比的竞争对手域名
  - 最近的链接增减情况（用于追踪变化）
  - 任何已知的有害或垃圾链接

**使用提供的数据进行完整分析。** 在输出中明确标注哪些指标来自自动化收集，哪些来自用户提供的数据。

## 操作步骤

当用户请求回链分析时：

1. **生成回链概况**

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
   DA 80-100: ████ [X]%
   DA 60-79:  ██████ [X]%
   DA 40-59:  ████████████ [X]%
   DA 20-39:  ████████████████ [X]%
   DA 0-19:   ██████████ [X]%
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
   域名：[spam-site-1.com]
   域名：[spam-site-2.com]
   域名：[link-farm.com]
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

5. **寻找链接建设机会**

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

7. **生成回链报告**

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

### CITE 评分系统

在执行 `domain-authority-auditor` 分析后，以下数据将直接用于 CITE 评分：

| 回链指标 | CITE 评分项 | 评分维度 |
|----------------|-----------|-----------|
| 引用域名数量 | C01（引用域名数量） | 引用次数 |
| 权威性分布（DA 分析） | C02（引用域名的质量） | 引用次数 |
| 链接速度 | C04（链接速度） | 引用次数 |
| 地理分布 | C10（链接来源多样性） | 引用次数 |
| 跟随/不跟随链接比例 | T02（跟随链接比例的合理性） | 信任度 |
| 有害链接分析 | T01（链接内容的自然性）、T03（链接流量的连贯性） | 信任度 |
| 竞争对手链接的交集 | T05（链接状况的独特性） | 信任度 |

## 验证要点

### 输入验证
- [ ] 目标域名的回链数据完整且最新
- [ ] 指定了用于对比分析的竞争对手域名
- [ ] 回链数据包含必要的字段（来源域名、锚文本、链接类型）
- [ ] 提供了权威性指标（DA/DR 或等效指标）

### 输出验证
- [ ] 每个指标都标明了数据来源和收集日期
- [ ] 有害链接的评估包含风险说明
- [ ] 链接建设建议具体且可操作
- [ ] 明确标注了每个数据点的来源（链接数据库数据、SEO 工具数据、用户提供的数据或估算值）

## 示例

**用户请求：** “通过分析 HubSpot、Salesforce 和 Mailchimp 来寻找链接建设机会”

**输出：**

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

1. **质量胜过数量** — 一个 DA 80 的链接比十个 DA 20 的链接更有价值
2. **定期监控** — 及时发现丢失或有害的链接
3. **研究竞争对手** — 学习他们的链接建设方法
4. **多样化链接来源** — 混合使用不同类型和内容的链接
5. **谨慎处理链接撤销** — 仅撤销明显有害的链接

## 链接质量评估框架

### 链接质量评分矩阵

| 评估因素 | 权重 | 评分 1（低） | 评分 3（中等） | 评分 5（高） |
|--------|--------|--------------|------------------|----------------|
| 域名权威性 | 25% | DR <20 | DR 20-50 | DR 50+ |
| 主题相关性 | 25% | 完全不相关 | 部分相关 | 完全相关 |
| 页面流量 | 15% | 无流量 | 有一定流量 | 流量较大 |
| 链接位置 | 15% | 底部/侧边栏 | 正文（通用内容） | 正文（相关/编辑内容） |
| 锚文本 | 10% | 通用/裸露的 URL | 部分匹配 | 描述性且自然 |
| 链接状态 | 10% | 不跟随/用户生成内容 | 赞助链接（明确标注） | 跟随链接 |

**链接质量总分** = 各因素得分之和 × 权重

### 有害链接识别标准

| 危险信号 | 风险等级 | 应对措施 |
|----------|-----------|--------|
| 来自私人博客网络（PBN）的链接 | 高风险 | 立即撤销 |
| 付费链接但标记为“不跟随” | 高风险 | 联系网站管理员后撤销 |
| 来自被黑的/垃圾网站的链接 | 高风险 | 立即撤销 |
| 来自低质量网站的完全匹配锚文本链接 | 高风险 | 监控并考虑撤销 |
| 来自链接农场/目录网络的链接 | 高风险 | 立即撤销 |
| 来自无关外语网站的链接 | 中等风险 | 监控 |
| 网站全站范围的底部/侧边栏链接 | 中等风险 | 请求移除或标记为“不跟随” |
| 来自爬虫/自动生成内容的链接 | 中等风险 | 立即撤销 |
| 互惠链接策略 | 低至中等风险 | 降低互惠链接的比例 |

## 链接建设策略矩阵

### 策略比较

| 策略 | 难度 | 可扩展性 | 链接质量 | 成效时间 | 适用场景 |
|----------|-----------|-------------|-------------|-----------------|---------|
| **客座投稿** | 中等 | 中等 | 中等至高 | 1-3 个月 | 建立关系并获取链接 |
| **数字公关** | 高 | 高 | 非常高 | 2-6 个月 | 增强品牌权威性和高质量链接 |
| **修复失效链接** | 低至中等 | 中等 | 中等 | 1-2 个月 | 快速获取链接 |
| **资源页面链接** | 低 | 低 | 中等 | 1-2 个月 | 与主题相关的链接 |
| **HARO/主动请求链接** | 中等 | 中等 | 高 | 1-3 个月 | 增强权威性 |
| **原创研究** | 高 | 非常高 | 非常高 | 3-6 个月 | 长期获取高质量链接 |
| **免费工具/计算器** | 非常高 | 非常高 | 6-12 个月 | 被动获取链接 |
| **Skyscraper 技巧** | 中等 | 低 | 中等至高 | 2-4 个月 | 提升特定内容的排名 |
| **未链接的提及** | 低 | 低 | 高 | 1-2 周 | 将现有品牌提及转化为链接 |
| **社区互动** | 低 | 低 | 低至中等 | 持续进行 | 建立领域权威性 |

## 链接建设节奏

| 网站阶段 | 每月目标链接数量 | 策略重点 |
|-----------|-------------------|---------------|
| 新网站（0-6 个月） | 5-10 个高质量链接 | 客座投稿、资源页面、HARO |
| 发展中网站（6-18 个月） | 10-25 个高质量链接 | 数字公关、原创研究 |
| 成熟网站（18 个月以上） | 维护现有链接 + 战略性链接 | 通过内容或数字公关获取链接 |

## 外联最佳实践

### 邮件外联模板

**邮件主题示例：**
- “关于 [他们的文章标题] 的快速问题”
- “[您的 [主题] 页面的相关资源”
- “[共同联系人] 建议我与您联系”
- “在 [他们的页面] 上发现了一个失效链接”

**邮件结构：**
1. 个人化的开场白（提及他们的具体内容——证明您看过该内容）
2. 提供价值（对对方的好处，而非对您的好处）
3. 提出具体请求（明确且易于执行）
4. 提供社交证明（简短说明）
5. 提供便捷的退订方式（不施加压力）

### 外联响应率参考

| 方法 | 平均响应率 | 平均链接获取率 |
|----------|---------------------|---------------------|
| 修复失效链接 | 8-12% | 3-5% |
| 客座投稿请求 | 5-10% | 2-4% |
| 资源页面外联 | 6-10% | 2-4% |
| 未链接的提及 | 15-25% | 10-15% |
| HARO 请求 | 3-8% | 1-3% |
| 数字公关活动 | 5-15% | 2-8% |

## 参考资料

- [链接质量评分标准](./references/link-quality-rubric.md) — 包含评分因素和有害链接识别标准
- [外联模板](./references/outreach-templates.md) — 邮件模板、主题示例和响应率参考
- [警报管理器](../alert-manager/) — 设置链接警报
- [绩效报告器](../performance-reporter/) — 将分析结果纳入报告
- [实体优化器](../entity-optimizer/) — 增强品牌的链接权威性