---
name: technical-seo-checker
version: "3.0.0"
description: '当用户请求进行“技术性SEO审计”、“检查页面速度”、“核心网页指标（Core Web Vitals）”、“LCP（页面加载时间）过慢”、“CLS（内容可读性）问题”、“INP（初始页面延迟）问题”、“爬取错误”、“索引问题”、“robots.txt文件检查”、“XML站点地图错误”、“hreflang（语言标签）问题”、“规范标签（canonical tags）问题”、“HTTPS无法正常工作”、“移动端SEO优化”或“JavaScript渲染问题”时，应使用此技能。该技能会执行全面的技术性SEO审计，涵盖核心网页指标（LCP/CLS/INP/TTFB）、页面的可爬取性、可索引性、移动友好性、HTTPS/HSTS安全性、URL结构、重定向链、robots.txt文件、XML站点地图、hreflang标签以及结构化数据的验证。审计结果会生成一份评分报告（0–100分），其中会区分问题的严重程度（关键/高/中等），并提供优先级的实施计划。该服务可通过Google PageSpeed Insights、Google Search Console或手动审计工具来完成。对于内容元素相关的问题，请参考“on-page-seo-auditor”；对于链接架构相关的问题，请参考“internal-linking-optimizer”。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
allowed-tools: WebFetch
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
  geo-relevance: "low"
  tags:
    - seo
    - technical seo
    - page speed
    - core web vitals
    - crawlability
    - indexability
    - mobile-friendly
    - site speed
    - security audit
    - core-web-vitals
    - page-speed
    - lcp
    - cls
    - inp
    - ttfb
    - crawl-errors
    - robots-txt
    - xml-sitemap
    - hreflang
    - canonicalization
    - https
    - mobile-seo
    - redirect-chains
    - javascript-rendering
    - site-health
  triggers:
    - "technical SEO audit"
    - "check page speed"
    - "crawl issues"
    - "Core Web Vitals"
    - "site indexing problems"
    - "mobile-friendly check"
    - "site speed"
    - "my site is slow"
    - "Google can't crawl my site"
    - "mobile issues"
    - "indexing problems"
---
# 技术性SEO检查工具

> **[SEO与地理定位技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含20项SEO与地理定位相关技能 · 全部技能的安装命令：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [搜索引擎排名分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [结构化数据生成器](../../build/schema-markup-generator/)

**优化** · [页面SEO审核器](../on-page-seo-auditor/) · **技术性SEO检查工具** · [内部链接优化器](../internal-linking-optimizer/) · [内容更新工具](../content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威性审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该工具可进行全面的技术性SEO审计，以识别可能阻碍搜索引擎正确爬取、索引和排名您网站的问题。

## 适用场景

- 新网站上线时
- 诊断排名下降的原因
- 迁移前的SEO审计
- 定期进行技术健康检查
- 识别爬取和索引问题
- 提升网站性能
- 修复Core Web Vitals相关问题

## 功能介绍

1. **可爬取性审计**：检查`robots.txt`文件、站点地图（sitemaps）以及爬取过程中存在的问题。
2. **可索引性审查**：分析索引状态及潜在的阻碍因素。
3. **网站速度分析**：评估Core Web Vitals指标及网站性能。
4. **移动友好性检查**：检测网站的移动优化情况。
5. **安全性检查**：审核HTTPS设置和安全头部信息。
6. **结构化数据验证**：验证网站的结构化数据标记（schema markup）。
7. **URL结构分析**：检查URL模式和重定向规则。
8. **国际SEO优化**：检查`hreflang`设置及本地化策略。

## 使用方法

### 全面技术审计

```
Perform a technical SEO audit for [URL/domain]
```

### 特定问题检测

```
Check Core Web Vitals for [URL]
```

```
Audit crawlability and indexability for [domain]
```

### 迁移前审计

```
Technical SEO checklist for migrating [old domain] to [new domain]
```

## 数据来源

> 有关工具类别的更多信息，请参阅[CONNECTORS.md](../../CONNECTORS.md)。

**当连接了[网络爬虫 + 页面速度工具 + CDN]时：**
Claude能够自动爬取整个网站结构，从[网络爬虫]获取Core Web Vitals指标和性能数据，从[页面速度工具]获取缓存头部信息，并从[CDN]获取移动友好性数据，从而实现全面自动化的技术审计。

**仅使用手动数据时：**
用户需要提供以下信息：
1. 需要审计的网站URL。
2. `PageSpeed Insights`的截图或报告。
3. `robots.txt`文件的内容。
4. `sitemap.xml`文件的URL或文件路径。

使用提供的数据进行全面审计。在审计结果中明确标注哪些发现来自自动爬取，哪些来自手动审核。

## 使用说明

当用户请求技术性SEO审计时，请按照以下步骤操作：

1. **进行可爬取性审计**

   ```markdown
   ## Crawlability Analysis
   
   ### Robots.txt Review
   
   **URL**: [domain]/robots.txt
   **Status**: [Found/Not Found/Error]
   
   **Current Content**:
   ```
   `robots.txt`文件内容：
   ```
   User-agent: *
   Allow: /
   Disallow: /admin/
   Disallow: /private/
   Sitemap: https://example.com/sitemap.xml
   ```
   ```
   
   ---
   
   ### XML Sitemap Review
   
   **Sitemap URL**: [URL]
   **Status**: [Found/Not Found/Error]
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Sitemap exists | ✅/❌ | [notes] |
   | Valid XML format | ✅/⚠️/❌ | [errors] |
   | In robots.txt | ✅/❌ | [notes] |
   | Submitted to ~~search console | ✅/⚠️/❌ | [notes] |
   | URLs count | [X] | [appropriate?] |
   | Only indexable URLs | ✅/⚠️/❌ | [notes] |
   | Includes priority | ✅/⚠️ | [notes] |
   | Includes lastmod | ✅/⚠️ | [accurate?] |
   
   **Issues Found**:
   - [Issue 1]
   
   ---
   
   ### Crawl Budget Analysis
   
   | Factor | Status | Impact |
   |--------|--------|--------|
   | Crawl errors | [X] errors | [Low/Med/High] |
   | Duplicate content | [X] pages | [Low/Med/High] |
   | Thin content | [X] pages | [Low/Med/High] |
   | Redirect chains | [X] found | [Low/Med/High] |
   | Orphan pages | [X] found | [Low/Med/High] |
   
   **Crawlability Score**: [X]/10
   ```

2. **进行可索引性审计**

   ```markdown
   ## Indexability Analysis
   
   ### Index Status Overview
   
   | Metric | Count | Notes |
   |--------|-------|-------|
   | Pages in sitemap | [X] | |
   | Pages indexed | [X] | [source: site: search] |
   | Index coverage ratio | [X]% | [good if >90%] |
   
   ### Index Blockers Check
   
   | Blocker Type | Found | Pages Affected |
   |--------------|-------|----------------|
   | noindex meta tag | [X] | [list or "none"] |
   | noindex X-Robots | [X] | [list or "none"] |
   | Robots.txt blocked | [X] | [list or "none"] |
   | Canonical to other | [X] | [list or "none"] |
   | 4xx/5xx errors | [X] | [list or "none"] |
   | Redirect loops | [X] | [list or "none"] |
   
   ### Canonical Tags Audit
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Canonicals present | ✅/⚠️/❌ | [X]% of pages |
   | Self-referencing | ✅/⚠️/❌ | [notes] |
   | Consistent (HTTP/HTTPS) | ✅/⚠️/❌ | [notes] |
   | Consistent (www/non-www) | ✅/⚠️/❌ | [notes] |
   | No conflicting signals | ✅/⚠️/❌ | [notes] |
   
   ### Duplicate Content Issues
   
   | Issue Type | Count | Examples |
   |------------|-------|----------|
   | Exact duplicates | [X] | [URLs] |
   | Near duplicates | [X] | [URLs] |
   | Parameter duplicates | [X] | [URLs] |
   | WWW/non-WWW | [X] | [notes] |
   | HTTP/HTTPS | [X] | [notes] |
   
   **Indexability Score**: [X]/10
   ```

3. **进行网站速度及Core Web Vitals审计** — 包括LCP/FID/CLS/INP等Core Web Vitals指标，以及TTFB/FCP/Speed Index/TBT等性能指标，还包括资源加载情况分析及优化建议。
   > **参考资料**：性能分析模板详见[references/technical-audit-templates.md](./references/technical-audit-templates.md)（第3步）。

4. **进行移动友好性审计** — 检测网站的移动优化情况，验证响应式设计及是否优先考虑移动用户。
   > **参考资料**：移动优化模板详见[references/technical-audit-templates.md](./references/technical-audit-templates.md)（第4步）。

5. **进行安全性与HTTPS审计** — 检查SSL证书、HTTPS实施情况、混合内容问题、HSTS设置以及安全头部信息（如CSP、X-Frame-Options等）。
   > **参考资料**：安全分析模板详见[references/technical-audit-templates.md](./references/technical-audit-templates.md)（第5步）。

6. **进行URL结构审计** — 检查URL模式及存在的问题（如动态参数、大写字符的使用、重定向链等）。
   > **参考资料**：URL结构审计模板详见[references/technical-audit-templates.md](./references/technical-audit-templates.md)（第6步）。

7. **进行结构化数据审计** — 验证网站的结构化数据标记是否正确，检查是否存在结构化数据缺失的情况。
   > **参考资料**：结构化数据审计模板详见[references/technical-audit-templates.md](./references/technical-audit-templates.md)（第7步）。

8. **进行国际SEO审计（如适用）** — 检查`hreflang`设置及语言/地区定位策略。
   > **参考资料**：国际SEO审计模板详见[references/technical-audit-templates.md](./references/technical-audit-templates.md)（第8步）。

9. **生成技术审计报告** — 提供包含整体健康状况的可视化报告，列出关键问题、高/中等风险问题、可快速解决的优化点以及实施计划（1-4周内需完成的任务），并提供监控建议。
   > **参考资料**：审计报告模板详见[references/technical-audit-templates.md](./references/technical-audit-templates.md)（第9步）。

## 验证要求

### 输入验证
- 必须明确提供网站URL或域名。
- 必须能够访问技术相关数据（`robots.txt`文件、站点地图或爬取结果）。
- 必须提供性能指标数据（通过[页面速度工具或截图获取）。

### 输出验证
- 每条建议都必须引用具体的数据来源。
- 所有问题都必须包含受影响的URL或页面数量。
- 性能指标必须包含具体的数值及单位（如秒数、KB等）。
- 必须明确说明每个数据来源（来自网络爬虫、页面速度工具、用户提供的数据或估算值）。

## 示例

> 完整的技术审计示例及详细检查清单详见[references/technical-audit-example.md](./references/technical-audit-example.md)（以cloudhosting.com为例）。

## 成功技巧

1. **按问题影响程度优先处理** — 先解决关键问题。
2. **持续监控** — 使用[搜索控制台]接收警报信息。
3. **测试修改效果** — 在广泛部署之前验证修改是否有效。
4. **详细记录所有操作** — 以便后续问题排查。
5. **定期进行审计** — 定期进行技术审查。

> **技术参考**：关于问题严重程度分级、优先级排序以及Core Web Vitals优化方法的详细信息，请参阅[references/http-status-codes.md](./references/http-status-codes.md)。

## 参考资料

- [robots.txt文件参考](./references/robots-txt-reference.md) — 语法指南、模板及常见配置示例。
- [HTTP状态码](./references/http-status-codes.md) — 各HTTP状态码对SEO的影响及重定向的最佳实践。
- [技术审计模板](./references/technical-audit-templates.md) — 第3-9步的详细输出模板（包括Core Web Vitals、移动优化、安全性、URL结构、结构化数据、国际SEO审计及审计报告）。
- [技术审计示例及检查清单](./references/technical-audit-example.md) — 完整的审计示例及详细的技术SEO检查清单。

## 相关技能

- [页面SEO审核器](../on-page-seo-auditor/) — 用于进行页面SEO审计。
- [结构化数据生成器](../../build/schema-markup-generator/) — 用于修复结构化数据问题。
- [性能报告工具](../../monitor/performance-reporter/) — 用于监控网站性能改进情况。
- [内部链接优化器](../internal-linking-optimizer/) — 用于修复链接问题。
- [警报管理器](../../monitor/alert-manager/) — 用于设置技术问题的警报通知。
- [内容质量审核器](../../cross-cutting/content-quality-auditor/) — 用于进行全面的80项核心指标审计。