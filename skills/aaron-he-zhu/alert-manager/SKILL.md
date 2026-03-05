---
name: alert-manager
version: "3.0.0"
description: '此技能适用于用户需要执行以下操作的情况：设置SEO警报、监控排名变化、在排名下降时接收通知、接收流量变化警报、关注竞争对手动态、在排名下降或流量变化时收到提醒，以及监控关键词的变化。该功能用于设置和管理与SEO及地理位置（GEO）相关的关键指标的警报，包括排名下降、流量变化、技术问题以及竞争对手的动向。通过该功能，可以实现主动监控并对问题迅速作出响应。如需详细的排名分析，请使用rank-tracker工具；如需全面的报告，请使用performance-reporter工具。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: AMPLITUDE_API_KEY
  author: aaron-he-zhu
  version: "3.0.0"
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
    - seo-monitoring
    - ranking-drop-alert
    - traffic-drop-alert
    - technical-monitoring
    - seo-alerts
    - automated-monitoring
    - threshold-alerts
    - anomaly-detection
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
# 警报管理系统

> **[SEO与地理策略技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含20项SEO与地理策略相关技能 · 全部技能可通过以下命令安装：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [搜索引擎排名分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写工具](../../build/seo-content-writer/) · [地理内容优化工具](../../build/geo-content-optimizer/) · [元标签优化工具](../../build/meta-tags-optimizer/) · [结构化标记生成工具](../../build/schema-markup-generator/)

**优化** · [页面SEO审核工具](../../optimize/on-page-seo-auditor/) · [技术SEO检查工具](../../optimize/technical-seo-checker/) · [内部链接优化工具](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名跟踪工具](../rank-tracker/) · [反向链接分析工具](../backlink-analyzer/) · [性能报告工具](../performance-reporter/) · **警报管理系统**

**跨领域工具** · [内容质量审核工具](../../cross-cutting/content-quality-auditor/) · [域名权威度审核工具](../../cross-cutting/domain-authority-auditor/) · [实体信息优化工具](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该系统可设置针对关键SEO和地理策略指标的主动监控警报。当排名下降、流量发生显著变化、出现技术问题或竞争对手有动作时，系统会触发通知。

## 适用场景

- 设置SEO监控系统
- 创建排名下降警报
- 监控技术SEO的健康状况
- 跟踪竞争对手的动态
- 在内容表现发生变化时发出警报
- 监控地理策略/AI相关指标的变化
- 设置品牌提及警报

## 功能概述

1. **警报配置**：设置自定义警报阈值
2. **多指标监控**：跟踪排名、流量和技术问题
3. **阈值管理**：定义警报触发条件
4. **优先级分类**：根据严重程度对警报进行分类
5. **通知设置**：配置警报的发送方式
6. **警报响应计划**：为每种警报类型制定行动计划
7. **警报历史记录**：记录警报的发生情况

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

> 有关工具类别的详细信息，请参阅 [CONNECTORS.md](../../CONNECTORS.md)。

**当连接了以下工具时：**
- **SEO工具** + **搜索控制台** + **网络爬虫**：通过SEO工具的API实时监控排名变化；通过搜索控制台获取索引和覆盖情况警报；通过网络爬虫获取技术健康状况警报。可设置基于阈值的自动警报，并配置通知方式。
**仅使用手动数据时：**
- 需要用户提供：
  - 警报阈值的当前基准数据（排名、流量、反向链接）
  - 需要监控的关键关键词或页面
  - 警报的优先级和通知偏好
  - 用于了解正常波动范围的历史数据
  - 用户在检查工具时需要手动报告指标变化情况

根据提供的参数进行警报配置。用户需要手动检查指标并报告变化情况以触发警报。

## 使用说明

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

2. **按类别配置警报规则**
   为每个相关类别（排名、流量、技术问题、反向链接、竞争对手、地理策略/AI、品牌）定义警报名称、触发条件、阈值和优先级。
   > **参考**：请参阅 [references/alert-configuration-templates.md](./references/alert-configuration-templates.md)，其中包含所有7个类别的完整警报表格、阈值示例和响应计划模板。

3. **定义警报响应计划**
   将每个优先级（紧急、高、中、低）映射到相应的响应时间和立即行动步骤。

4. **设置警报通知**
   配置通知渠道（电子邮件、短信、Slack），按角色分配接收者，设置抑制规则（避免重复通知、维护窗口），以及升级路径。

5. **创建警报摘要**
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
- [ ] 关键关键词和页面已明确识别
- [ ] 为每个警报优先级定义了响应计划
- [ ] 通知渠道已配置正确的接收者

### 输出验证
- [ ] 每个指标都标明了数据来源和收集日期
- [ ] 警报阈值考虑了指标的正常波动范围
- [ ] 响应计划具体且具有时间限制
- [ ] 明确说明了每个警报的触发来源（SEO工具API警报、搜索控制台通知、网络爬虫警报或手动检查）

## 示例

**用户**：“为我的热门关键词设置排名下降警报”

**输出**：
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
2. **调整阈值** — 根据数据波动情况适时调整
3. **避免警报疲劳** — 警报过多可能导致用户忽略警报
4. **记录响应计划** — 明确知道收到警报时应采取的措施
5. **定期审查** — 随着SEO工作的进展，需要定期维护警报系统
6. **包括正面警报** — 不仅记录问题，也要跟踪成功案例

## 警报阈值快速参考

| 指标 | 警报级别 | 紧急程度 | 报警频率 |
|--------|---------|----------|-----------|
| 自然流量 | 比上周下降15% | 比上周下降30% | 每日 |
| 关键词排名 | 排名下降超过3位 | 排名下降超过5位 | 每日 |
| 被索引的页面数量 | 变化幅度超过5% | 变化幅度超过20% | 每周 |
| 爬取错误 | 每日新增错误超过10个 | 每日新增错误超过50个 | 每日 |
| 核心网站健康状况 | “需要改进” | “较差” | 每周 |
| 失去的反向链接 | 一周内减少超过5个 | 一周内减少超过15个 | 每周 |
| AI引用数量 | 任何关键查询出现变化 | 超过20%的查询出现变化 | 每周 |
| 安全问题 | 任何问题被检测到 | 任何问题被检测到 | 每日 |

> **参考**：请参阅 [references/alert-threshold-guide.md](./references/alert-threshold-guide.md)，了解基准值的设定方法、阈值设置策略、避免疲劳的技巧、升级路径和响应方案。

## 参考资料

- [警报阈值指南](./references/alert-threshold-guide.md) — 提供按指标推荐的阈值、疲劳预防策略和升级路径模板

## 相关技能

- [rank-tracker](../rank-tracker/) — 用于获取排名数据以生成警报
- [backlink-analyzer](../backlink-analyzer/) — 用于监控反向链接
- [technical-seo-checker](../../optimize/technical-seo-checker/) — 用于进行技术监控
- [performance-reporter](../performance-reporter/) — 在报告中生成警报摘要
- [memory-management](../../cross-cutting/memory-management/) — 用于存储警报历史记录和阈值
- [content-refresher](../../optimize/content-refresher/) — 用于在内容更新时触发警报并更新相关工作流程