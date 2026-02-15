---
name: alert-manager
description: '**使用场景：**  
当用户请求“设置SEO警报”、“监控排名情况”、“在排名下降时接收通知”、“接收流量变化警报”、“关注竞争对手动态”、“在排名下降时收到提醒”、“获取流量变化通知”或“监控关键词的变化”时，可使用该功能。该功能用于设置和管理与关键SEO及地理位置（GEO）指标相关的警报，包括排名下降、流量变化、技术问题以及竞争对手的动态。通过该功能，用户可以实现对问题的主动监控并迅速作出响应。如需详细的排名分析，请参阅`rank-tracker`；如需全面的报告，请参阅`performance-reporter`。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "low"
  tags:
    - seo
    - geo
    - alerts
    - monitoring
    - ranking alerts
    - traffic monitoring
    - competitor alerts
    - seo notifications
    - proactive monitoring
  triggers:
    - "set up SEO alerts"
    - "monitor rankings"
    - "notify me when rankings drop"
    - "traffic alerts"
    - "watch competitor changes"
    - "alert me"
    - "ranking notifications"
    - "alert me if rankings drop"
    - "notify me of traffic changes"
    - "watch my keywords for changes"
---

# 警报管理器

> **[SEO与地理定位技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含20项SEO与地理定位相关技能 · 全部技能的安装命令：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [结构化标记生成器](../../build/schema-markup-generator/)

**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容更新器](../../optimize/content-refresher/)

**监控** · [排名追踪器](../rank-tracker/) · [反向链接分析器](../backlink-analyzer/) · [性能报告器](../performance-reporter/) · **警报管理器**

**跨领域技能** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威度审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)

</details>

该技能可帮助您为关键的SEO和地理定位指标设置主动监控警报。当排名下降、流量发生显著变化、出现技术问题或竞争对手有行动时，系统会及时通知您。

## 适用场景

- 设置SEO监控系统
- 创建排名下降警报
- 监控技术SEO的健康状况
- 跟踪竞争对手的动态
- 在内容表现发生变化时发出警报
- 监控地理定位/AI相关指标的变化
- 设置品牌提及警报

## 功能概述

1. **警报配置**：设置自定义警报阈值
2. **多指标监控**：跟踪排名、流量和技术问题
3. **阈值管理**：定义警报触发条件
4. **优先级分类**：根据严重程度对警报进行分类
5. **通知设置**：配置警报的发送方式
6. **警报响应计划**：为每种警报类型制定行动计划
7. **警报历史记录**：记录警报的演变过程

## 使用方法

### 设置警报

```
Set up SEO monitoring alerts for [domain]
```

```
Create ranking drop alerts for my top 20 keywords
```

### 配置特定警报

```
Alert me when [specific condition]
```

```
Set up competitor monitoring for [competitor domains]
```

### 查看警报系统

```
Review and optimize my current SEO alerts
```

## 数据来源

> 请参阅[CONNECTORS.md](../../CONNECTORS.md)以了解工具类别的相关信息。

**当连接到 ~~SEO工具 + ~~搜索控制台 + ~~网络爬虫时：**
- 通过 ~~SEO工具API** 自动监控排名变化的实时数据；通过 ~~搜索控制台** 获取索引和覆盖范围警报；通过 ~~网络爬虫** 获取技术健康状况警报。并设置基于阈值的自动警报，实现通知功能。

**仅使用手动数据时：**
- 要求用户提供：
  - 警报阈值的当前基准数据（排名、流量、反向链接）
  - 需要监控的关键关键词或页面
  - 警报的优先级和通知偏好
  - 历史数据，以便了解正常波动范围
  - 在用户检查工具时，手动报告指标变化情况

根据提供的参数进行警报配置。用户需要手动检查指标并报告变化情况以触发警报。

## 操作步骤

当用户请求设置警报时：

1. **定义警报类别**

   ```markdown
   ## SEO Alert System Configuration
   
   **Domain**: [domain]
   **Configured Date**: [date]
   
   ### Alert Categories
   
   | Category | Description | Typical Urgency |
   |----------|-------------|-----------------|
   | Ranking Alerts | Keyword position changes | Medium-High |
   | Traffic Alerts | Organic traffic fluctuations | High |
   | Technical Alerts | Site health issues | Critical |
   | Backlink Alerts | Link profile changes | Medium |
   | Competitor Alerts | Competitor movements | Low-Medium |
   | GEO Alerts | AI visibility changes | Medium |
   | Brand Alerts | Brand mentions and reputation | Medium |
   ```

2. **配置排名警报**

   ```markdown
   ## Ranking Alerts
   
   ### Position Drop Alerts
   
   | Alert Name | Condition | Threshold | Priority | Action |
   |------------|-----------|-----------|----------|--------|
   | Critical Drop | Any top 3 keyword drops 5+ positions | Position change ≥5 | 🔴 Critical | Immediate investigation |
   | Major Drop | Top 10 keyword drops out of top 10 | Position >10 | 🔴 High | Same-day review |
   | Moderate Drop | Any keyword drops 10+ positions | Position change ≥10 | 🟡 Medium | Weekly review |
   | Competitor Overtake | Competitor passes you for key term | Comp position < yours | 🟡 Medium | Analysis needed |
   
   ### Position Improvement Alerts
   
   | Alert Name | Condition | Threshold | Priority |
   |------------|-----------|-----------|----------|
   | New Top 3 | Keyword enters top 3 | Position ≤3 | 🟢 Positive |
   | Page 1 Entry | Keyword enters top 10 | Position ≤10 | 🟢 Positive |
   | Significant Climb | Keyword improves 10+ positions | Change ≥+10 | 🟢 Positive |
   
   ### SERP Feature Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Snippet Lost | Lost featured snippet ownership | 🔴 High |
   | Snippet Won | Won new featured snippet | 🟢 Positive |
   | AI Overview Change | Appeared/disappeared in AI Overview | 🟡 Medium |
   
   ### Keywords to Monitor
   
   | Keyword | Current Rank | Alert Threshold | Priority |
   |---------|--------------|-----------------|----------|
   | [keyword 1] | [X] | Drop ≥3 | 🔴 Critical |
   | [keyword 2] | [X] | Drop ≥5 | 🔴 High |
   | [keyword 3] | [X] | Drop ≥10 | 🟡 Medium |
   ```

3. **配置流量警报**

   ```markdown
   ## Traffic Alerts
   
   ### Traffic Decline Alerts
   
   | Alert Name | Condition | Threshold | Priority |
   |------------|-----------|-----------|----------|
   | Traffic Crash | Day-over-day decline | ≥50% drop | 🔴 Critical |
   | Significant Drop | Week-over-week decline | ≥30% drop | 🔴 High |
   | Moderate Decline | Month-over-month decline | ≥20% drop | 🟡 Medium |
   | Trend Warning | 3 consecutive weeks decline | Any decline | 🟡 Medium |
   
   ### Traffic Anomaly Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Traffic Spike | Unusual increase | 🟢 Investigate |
   | Zero Traffic | Page receiving 0 visits | 🔴 High |
   | Bot Traffic | Unusual traffic pattern | 🟡 Medium |
   
   ### Page-Level Alerts
   
   | Page Type | Alert Condition | Priority |
   |-----------|-----------------|----------|
   | Homepage | Any 20%+ decline | 🔴 Critical |
   | Top 10 pages | Any 30%+ decline | 🔴 High |
   | Conversion pages | Any 25%+ decline | 🔴 High |
   | Blog posts | Any 40%+ decline | 🟡 Medium |
   
   ### Conversion Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Conversion Drop | Organic conversions down 30%+ | 🔴 Critical |
   | CVR Decline | Conversion rate drops 20%+ | 🔴 High |
   ```

4. **配置技术SEO警报**

   ```markdown
   ## Technical SEO Alerts
   
   ### Critical Technical Alerts
   
   | Alert Name | Condition | Priority | Response Time |
   |------------|-----------|----------|---------------|
   | Site Down | HTTP 5xx errors | 🔴 Critical | Immediate |
   | SSL Expiry | Certificate expiring in 14 days | 🔴 Critical | Same day |
   | Robots.txt Block | Important pages blocked | 🔴 Critical | Same day |
   | Index Dropped | Pages dropping from index | 🔴 Critical | Same day |
   
   ### Crawl & Index Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Crawl Errors Spike | Errors increase 50%+ | 🔴 High |
   | New 404 Pages | 404 errors on important pages | 🟡 Medium |
   | Redirect Chains | 3+ redirect hops detected | 🟡 Medium |
   | Duplicate Content | New duplicates detected | 🟡 Medium |
   | Index Coverage Drop | Indexed pages decline 10%+ | 🔴 High |
   
   ### Performance Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Core Web Vitals Fail | CWV drops to "Poor" | 🔴 High |
   | Page Speed Drop | Load time increases 50%+ | 🟡 Medium |
   | Mobile Issues | Mobile usability errors | 🔴 High |
   
   ### Security Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Security Issue | GSC security warning | 🔴 Critical |
   | Manual Action | Google manual action | 🔴 Critical |
   | Malware Detected | Site flagged for malware | 🔴 Critical |
   ```

5. **配置反向链接警报**

   ```markdown
   ## Backlink Alerts
   
   ### Link Loss Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | High-Value Link Lost | DA 70+ link removed | 🔴 High |
   | Multiple Links Lost | 10+ links lost in a day | 🟡 Medium |
   | Referring Domain Lost | Lost entire domain's links | 🟡 Medium |
   
   ### Link Gain Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | High-Value Link | New DA 70+ link | 🟢 Positive |
   | Suspicious Links | Many low-quality links | 🟡 Review |
   | Negative SEO | Spam link attack pattern | 🔴 High |
   
   ### Link Profile Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Toxic Score Increase | Toxic score up 20%+ | 🔴 High |
   | Anchor Over-Optimization | Exact match anchors >30% | 🟡 Medium |
   ```

6. **配置竞争对手警报**

   ```markdown
   ## Competitor Monitoring Alerts
   
   ### Ranking Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Competitor Overtake | Competitor passes you | 🟡 Medium |
   | Competitor Top 3 | Competitor enters top 3 on key term | 🟡 Medium |
   | Competitor Content | Competitor publishes on your topic | 🟢 Info |
   
   ### Activity Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | New Backlinks | Competitor gains high-DA link | 🟢 Info |
   | Content Update | Competitor updates ranking content | 🟢 Info |
   | New Content | Competitor publishes new content | 🟢 Info |
   
   ### Competitors to Monitor
   
   | Competitor | Domain | Monitor Keywords | Alert Priority |
   |------------|--------|------------------|----------------|
   | [Competitor 1] | [domain] | [X] keywords | High |
   | [Competitor 2] | [domain] | [X] keywords | Medium |
   | [Competitor 3] | [domain] | [X] keywords | Low |
   ```

7. **配置地理定位/AI警报**

   ```markdown
   ## GEO (AI Visibility) Alerts
   
   ### AI Citation Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Citation Lost | Lost AI Overview citation | 🟡 Medium |
   | Citation Won | New AI Overview citation | 🟢 Positive |
   | Citation Position Drop | Dropped from 1st to 3rd+ source | 🟡 Medium |
   | New AI Overview | AI Overview appears for tracked keyword | 🟢 Info |
   
   ### GEO Trend Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Citation Rate Drop | AI citation rate drops 20%+ | 🔴 High |
   | GEO Competitor | Competitor cited where you're not | 🟡 Medium |
   ```

8. **配置品牌警报**

   ```markdown
   ## Brand Monitoring Alerts
   
   ### Mention Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Brand Mention | New brand mention online | 🟢 Info |
   | Negative Mention | Negative sentiment mention | 🔴 High |
   | Review Alert | New review on key platforms | 🟡 Medium |
   | Unlinked Mention | Brand mention without link | 🟢 Opportunity |
   
   ### Reputation Alerts
   
   | Alert Name | Condition | Priority |
   |------------|-----------|----------|
   | Review Rating Drop | Average rating drops | 🔴 High |
   | Negative Press | Negative news article | 🔴 High |
   | Competitor Comparison | Named in competitor comparison | 🟡 Medium |
   ```

9. **定义警报响应计划**

   ```markdown
   ## Alert Response Plans
   
   ### Critical Alert Response (🔴)
   
   **Response Time**: Immediate (within 1 hour)
   
   | Alert Type | Immediate Actions |
   |------------|-------------------|
   | Site Down | 1. Check server status 2. Contact hosting 3. Check DNS |
   | Traffic Crash | 1. Check for algorithm update 2. Review GSC errors 3. Check competitors |
   | Manual Action | 1. Review GSC message 2. Identify issue 3. Begin remediation |
   | Critical Rank Drop | 1. Check if page indexed 2. Review SERP 3. Analyze competitors |
   
   ### High Priority Response (🔴/🟡)
   
   **Response Time**: Same day
   
   | Alert Type | Actions |
   |------------|---------|
   | Major Rank Drops | Analyze cause, create recovery plan |
   | Traffic Decline | Investigate source, check technical issues |
   | Backlink Loss | Attempt recovery outreach |
   | CWV Failure | Diagnose and fix performance issues |
   
   ### Medium Priority Response (🟡)
   
   **Response Time**: Within 48 hours
   
   | Alert Type | Actions |
   |------------|---------|
   | Moderate Rank Changes | Monitor trend, plan content updates |
   | Competitor Movement | Analyze competitor changes |
   | New 404s | Set up redirects, update internal links |
   
   ### Low Priority (🟢)
   
   **Response Time**: Weekly review
   
   | Alert Type | Actions |
   |------------|---------|
   | Positive Changes | Document wins, understand cause |
   | Info Alerts | Log for trend analysis |
   ```

10. **设置警报通知方式**

    ```markdown
    ## Alert Notification Setup
    
    ### Notification Channels
    
    | Priority | Channels | Frequency |
    |----------|----------|-----------|
    | 🔴 Critical | Email + SMS + Slack | Immediate |
    | 🔴 High | Email + Slack | Immediate |
    | 🟡 Medium | Email + Slack | Daily digest |
    | 🟢 Low | Email | Weekly digest |
    
    ### Alert Recipients
    
    | Role | Critical | High | Medium | Low |
    |------|----------|------|--------|-----|
    | SEO Manager | ✅ | ✅ | ✅ | ✅ |
    | Dev Team | ✅ | ✅ (tech only) | ❌ | ❌ |
    | Marketing Lead | ✅ | ✅ | ❌ | ❌ |
    | Executive | ✅ | ❌ | ❌ | ❌ |
    
    ### Alert Suppression
    
    - Suppress duplicate alerts for 24 hours
    - Don't alert on known issues (maintenance windows)
    - Batch low-priority alerts into digests
    
    ### Alert Escalation
    
    | If No Response In | Escalate To |
    |-------------------|-------------|
    | 1 hour (Critical) | SEO Manager → Director |
    | 4 hours (High) | Team Lead → Manager |
    | 24 hours (Medium) | Team → Lead |
    ```

11. **创建警报摘要**

    ```markdown
    # SEO Alert System Summary
    
    **Domain**: [domain]
    **Configured**: [date]
    **Total Active Alerts**: [X]
    
    ## Alert Count by Category
    
    | Category | Critical | High | Medium | Low | Total |
    |----------|----------|------|--------|-----|-------|
    | Rankings | [X] | [X] | [X] | [X] | [X] |
    | Traffic | [X] | [X] | [X] | [X] | [X] |
    | Technical | [X] | [X] | [X] | [X] | [X] |
    | Backlinks | [X] | [X] | [X] | [X] | [X] |
    | Competitors | [X] | [X] | [X] | [X] | [X] |
    | GEO | [X] | [X] | [X] | [X] | [X] |
    | **Total** | **[X]** | **[X]** | **[X]** | **[X]** | **[X]** |
    
    ## Quick Reference
    
    ### If You Get a Critical Alert
    
    1. Don't panic
    2. Check alert details
    3. Follow response plan
    4. Document actions taken
    5. Update stakeholders
    
    ### Weekly Alert Review Checklist
    
    - [ ] Review all alerts triggered
    - [ ] Identify patterns
    - [ ] Adjust thresholds if needed
    - [ ] Update response plans
    - [ ] Clean up false positives
    ```

## 验证要点

### 输入验证
- [ ] 警报阈值基于实际的基准数据
- [ ] 关键关键词和页面已明确指定
- [ ] 为每个警报优先级定义了响应计划
- [ ] 通知渠道已配置正确的接收者

### 输出验证
- [ ] 每个指标都标明了数据来源和收集日期
- [ ] 警报阈值考虑到了指标的正常波动范围
- [ ] 响应计划具体且具有时间限制
- [ ] 明确了每个警报的触发来源（~~SEO工具API警报、~~搜索控制台通知、~~网络爬虫警报或手动检查）

## 示例

**用户**：“为我最重要的关键词设置排名下降警报”

**输出结果：**

```markdown
## Ranking Alert Configuration

### Critical Keywords (Immediate Alert)

| Keyword | Current | Alert If | Priority |
|---------|---------|----------|----------|
| best project management software | 2 | Drops to 5+ | 🔴 Critical |
| project management tools | 4 | Drops to 8+ | 🔴 Critical |
| team collaboration software | 1 | Any drop | 🔴 Critical |

### Important Keywords (Same-Day Alert)

| Keyword | Current | Alert If | Priority |
|---------|---------|----------|----------|
| agile project management | 7 | Drops out of top 10 | 🔴 High |
| kanban software | 9 | Drops out of top 10 | 🔴 High |

### Alert Response Plan

**If Critical Keyword Drops**:
1. Check if page is still indexed (site:url)
2. Look for algorithm update announcements
3. Analyze what changed in SERP
4. Review competitor ranking changes
5. Check for technical issues on page
6. Create recovery action plan within 24 hours

**Notification**: Email + Slack to SEO team immediately
```

## 成功技巧

1. **从简单开始** — 初始阶段不要设置过多警报
2. **调整阈值** — 根据数据波动情况进行调整
3. **避免警报疲劳** — 警报过多可能导致警报被忽略
4. **记录响应计划** — 明确知道收到警报时应采取的措施
5. **定期审查** — 随着SEO工作的进展，需要定期维护警报系统
6. **包括正面警报** — 不仅关注问题，也要跟踪成功案例

## 警报阈值建议

### 按指标推荐的警报阈值

| 指标 | 警报阈值 | 临界阈值 | 检查频率 |
|--------|------------------|-------------------|-----------------|
| 自然流量 | -15%（每周环比） | -30%（每周环比） | 每日 |
| 平均排名位置（监控关键词） | 排名下降超过3位 | 排名下降超过5位 | 每日 |
| 被索引的页面数量 | 变化超过5% | 变化超过20% | 每周 |
| 爬取错误 | 新错误超过10个 | 新错误超过50个 | 每日 |
| 核心网站健康指标 | 任何指标降至“需要改进” | 任何指标降至“较差” | 每周 |
| 失去的反向链接 | 一周内超过总链接的5% | 一周内超过15% | 每周 |
| AI引用丢失 | 任何关键查询的引用丢失 | 超过20%的查询引用丢失 | 每周 |
| 服务器错误（5xx代码） | 超过1%的页面出现此类错误 | 超过5%的页面出现此类错误 | 每日 |
| 安全问题 | 任何问题被检测到 | 任何问题被检测到 | 每日 |
| 手动处罚 | 无 | 任何通知 | 每日 |

## 避免警报疲劳的策略

### 警报管理的最佳实践

| 实践 | 原因 | 方法 |
|----------|-----|-----|
| **分级处理** | 并非所有警报都需要立即处理 | 临界警报：立即处理；警告级警报：每日查看；信息级警报：每周汇总 |
| **调整阈值** | 减少误报 | 初始时设置保守的阈值，一个月后根据数据调整 |
| **分组处理** | 避免同一问题重复触发警报 | 将相关警报归为一类（例如，多次排名下降归为“排名警报” |
| **冷却期** | 避免同一指标连续触发警报 | 同一指标24-48小时内不再重复警报 |
| **定期汇总** | 减少通知量 | 将非紧急警报汇总到每日或每周的邮件中 |
| **自动解决** | 当指标恢复时关闭警报 | 监测指标恢复情况，若阈值恢复正常则自动关闭警报 |

### 警报优先级分类

| 优先级 | 响应时间 | 通知渠道 | 示例 |
|----------|-------------|---------------------|---------|
| P0 — 紧急 | 1小时内 | SMS + Slack + 电子邮件 | 网站瘫痪、手动处罚、安全漏洞 |
| P1 — 紧急 | 当天 | Slack + 电子邮件 | 流量大幅下降、爬取受阻、索引问题 |
| P2 — 重要 | 48小时内 | 电子邮件 + 每周汇总 | 排名下降、网站健康指标下降、反向链接丢失 |
| P3 — 监控 | 下周审查 | 仅每周汇总 | 轻微波动、竞争对手发布新内容 |

## 升级流程模板

### 标准升级流程

```
Alert Triggers -> Automated Classification -> Route by Priority

P0: Notify SEO Lead + Dev Team immediately
    -> If not acknowledged in 30 min -> Notify Engineering Manager
        -> If not resolved in 2 hours -> Notify VP/Director

P1: Notify SEO Lead
    -> If not acknowledged in 4 hours -> Notify Marketing Manager
        -> Add to next standup agenda

P2: Add to daily digest
    -> If persists >1 week -> Escalate to P1

P3: Add to weekly digest
    -> If persists >1 month -> Escalate to P2
```

## 警报响应方案

### 流量下降警报

| 步骤 | 操作 | 如果情况属实 | 如果情况不属实 |
|------|--------|---------|----------|
| 1 | 检查是整个网站还是特定页面的问题 | 进入步骤2a | 进入步骤2b |
| 2a | 查看Google搜索状态仪表板，确认是否有算法更新 | 记录情况并等待 | 进入步骤3 |
| 2b | 检查特定页面是否存在技术问题（如404错误、页面无法被索引、页面加载缓慢） | 解决技术问题 | 进入步骤3 |
| 3 | 检查搜索控制台中的爬取错误或索引问题 | 解决爬取/索引问题 | 进入步骤4 |
| 4 | 检查竞争对手是否发布了新内容 | 分析并制定内容应对策略 | 进入步骤5 |
| 5 | 检查排名页面的反向链接是否丢失 | 尝试恢复丢失的链接 | 如需进一步分析，则升级处理 |

### 排名下降警报

| 步骤 | 操作 | 如果情况属实 | 如果情况不属实 |
|------|--------|---------|----------|
| 1 | 确认排名下降是否真实（通过多个工具验证，等待24-48小时） | 确认下降情况，进入步骤2 | 警报误报，关闭警报 |
| 2 | 检查是否有算法更新 | 记录情况，监控网站表现，提升内容质量 | 进入步骤3 |
| 3 | 检查页面是否最近发生了变化 | 恢复或修正页面设置 | 进入步骤4 |
| 4 | 分析SERP情况——是否有新竞争对手出现 | 分析竞争对手情况，制定应对策略 | 进入步骤5 |
| 5 | 检查排名页面的反向链接是否丢失 | 恢复丢失的链接或建立新的链接 | 如需进一步分析，则升级处理 |

### 技术警报（网站瘫痪/5xx错误）

| 步骤 | 操作 | 如果情况属实 | 如果情况不属实 |
|------|--------|---------|----------|
| 1 | 确认网站确实瘫痪（从多个位置验证） | 关闭误报警报 | |
| 2 | 检查服务器/托管服务状态 | 如果是服务提供商的问题，请联系支持团队 | 进入步骤3 |
| 3 | 检查最近的部署或配置更改 | 撤销更改 | 进入步骤4 |
| 4 | 检查服务器资源使用情况（CPU、内存、磁盘） | 调整资源或优化配置 | 如需进一步处理，则升级至工程团队 |

## 参考资料

- [警报阈值指南](./references/alert-threshold-guide.md) — 按指标推荐的阈值、避免警报疲劳的策略以及升级流程模板

## 相关技能

- [排名追踪器](../rank-tracker/) — 提供用于警报的排名数据
- [反向链接分析器](../backlink-analyzer/) — 监控反向链接情况
- [技术SEO检查器](../../optimize/technical-seo-checker/) — 进行技术监控
- [性能报告器](../performance-reporter/) — 在报告中生成警报摘要
- [内存管理](../../cross-cutting/memory-management/) — 将警报历史和阈值存储在项目内存中
- [内容更新器](../../optimize/content-refresher/) — 在内容发生变化时触发警报，以便及时更新处理流程