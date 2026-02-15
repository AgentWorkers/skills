---
name: technical-seo-checker
description: '**使用场景：**  
当用户请求进行“技术性SEO审计”、“检查页面速度”、“解决爬虫问题”、“评估Core Web Vitals指标”、“排查网站索引问题”、“网站加载缓慢”、“Google无法抓取我的网站”、“存在移动端兼容性问题”或“索引问题”时，可以使用该工具。该工具会执行涵盖网站速度、可爬取性、可索引性、移动设备友好性、安全性以及结构化数据等方面的技术性SEO审计，识别阻碍网站搜索性能优化的技术问题。  
- 对于内容或标题元素相关的问题，请参考**on-page-seo-auditor**；  
- 对于链接结构相关的问题，请参考**internal-linking-optimizer**。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
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

> **[SEO与地理定位技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理定位相关技能 · 全部技能的安装命令：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [结构化数据标记生成器](../../build/schema-markup-generator/)

**优化** · [页面SEO审核器](../on-page-seo-auditor/) · **技术性SEO检查工具** · [内部链接优化器](../internal-linking-optimizer/) · [内容更新工具](../content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域技能** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威性审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)

</details>

该工具可执行全面的技术性SEO审计，以识别可能阻碍搜索引擎正确爬取、索引和排名您网站的问题。

## 适用场景

- 新网站上线时
- 诊断排名下降的原因
- 迁站前的SEO审计
- 定期进行技术健康检查
- 识别爬取和索引问题
- 提升网站性能
- 修复Core Web Vitals相关问题

## 功能概述

1. **可爬取性审计**：检查robots.txt文件、站点地图（sitemaps）以及爬取过程中存在的问题。
2. **可索引性审核**：分析索引状态及潜在的阻碍因素。
3. **网站速度分析**：评估Core Web Vitals指标及网站性能。
4. **移动设备友好性**：检查网站的移动优化情况。
5. **安全性检查**：审查HTTPS设置和安全头部信息。
6. **结构化数据审计**：验证网站的结构化数据标记是否正确。
7. **URL结构分析**：检查URL格式和重定向规则。
8. **国际SEO**：检查网站的国际化设置（如hreflang和本地化内容）。

## 使用方法

### 全面技术性审计

```
Perform a technical SEO audit for [URL/domain]
```

### 针对特定问题的审计

```
Check Core Web Vitals for [URL]
```

### 迁站前的审计

```
Technical SEO checklist for migrating [old domain] to [new domain]
```

## 数据来源

> 有关工具类别的更多信息，请参阅[CONNECTORS.md](../../CONNECTORS.md)。

**当连接了[网络爬虫 + 页面速度工具 + CDN]时：**
Claude能够自动爬取整个网站结构，从页面速度工具中获取Core Web Vitals指标和性能数据，从CDN中获取缓存信息，并分析网站的移动设备友好性。这实现了全面的自动化技术审计。

**仅使用手动数据时：**
用户需要提供以下信息：
1. 需要审计的网站URL。
2. PageSpeed Insights的截图或报告。
3. robots.txt文件的内容。
4. sitemap.xml文件的URL或文件路径。

使用提供的数据开始全面审计。在审计结果中明确标注哪些发现是通过自动化爬取得出的，哪些是通过手动审核得出的。

## 使用说明

当用户请求进行技术性SEO审计时，请按照以下步骤操作：

1. **可爬取性审计**
   ```markdown
   ## Crawlability Analysis
   
   ### Robots.txt Review
   
   **URL**: [domain]/robots.txt
   **Status**: [Found/Not Found/Error]
   
   **Current Content**:
   ```
   [robots.txt文件内容]
   ```
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | File exists | ✅/❌ | [notes] |
   | Valid syntax | ✅/⚠️/❌ | [errors found] |
   | Sitemap declared | ✅/❌ | [sitemap URL] |
   | Important pages blocked | ✅/⚠️/❌ | [blocked paths] |
   | Assets blocked | ✅/⚠️/❌ | [CSS/JS blocked?] |
   | Correct user-agents | ✅/⚠️/❌ | [notes] |
   
   **Issues Found**:
   - [Issue 1]
   - [Issue 2]
   
   **Recommended robots.txt**:
   ```
   User-agent: *
   Allow: /
   Disallow: /admin/
   Disallow: /private/
   
   Sitemap: https://example.com/sitemap.xml
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

2. **可索引性审计**
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

3. **网站速度与Core Web Vitals审计**
   ```markdown
   ## Performance Analysis
   
   ### Core Web Vitals
   
   | Metric | Mobile | Desktop | Target | Status |
   |--------|--------|---------|--------|--------|
   | LCP (Largest Contentful Paint) | [X]s | [X]s | <2.5s | ✅/⚠️/❌ |
   | FID (First Input Delay) | [X]ms | [X]ms | <100ms | ✅/⚠️/❌ |
   | CLS (Cumulative Layout Shift) | [X] | [X] | <0.1 | ✅/⚠️/❌ |
   | INP (Interaction to Next Paint) | [X]ms | [X]ms | <200ms | ✅/⚠️/❌ |
   
   ### Additional Performance Metrics
   
   | Metric | Value | Status |
   |--------|-------|--------|
   | Time to First Byte (TTFB) | [X]ms | ✅/⚠️/❌ |
   | First Contentful Paint (FCP) | [X]s | ✅/⚠️/❌ |
   | Speed Index | [X] | ✅/⚠️/❌ |
   | Total Blocking Time | [X]ms | ✅/⚠️/❌ |
   | Page Size | [X]MB | ✅/⚠️/❌ |
   | Requests | [X] | ✅/⚠️/❌ |
   
   ### Performance Issues
   
   **LCP Issues**:
   - [Issue]: [Impact] - [Solution]
   - [Issue]: [Impact] - [Solution]
   
   **CLS Issues**:
   - [Issue]: [Impact] - [Solution]
   
   **Resource Loading**:
   | Resource Type | Count | Size | Issues |
   |---------------|-------|------|--------|
   | Images | [X] | [X]MB | [notes] |
   | JavaScript | [X] | [X]MB | [notes] |
   | CSS | [X] | [X]KB | [notes] |
   | Fonts | [X] | [X]KB | [notes] |
   
   ### Optimization Recommendations
   
   **High Impact**:
   1. [Recommendation] - Est. improvement: [X]s
   2. [Recommendation] - Est. improvement: [X]s
   
   **Medium Impact**:
   1. [Recommendation]
   2. [Recommendation]
   
   **Performance Score**: [X]/10
   ```

4. **移动设备友好性审计**
   ```markdown
   ## Mobile Optimization Analysis
   
   ### Mobile-Friendly Test
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Mobile-friendly overall | ✅/❌ | [notes] |
   | Viewport configured | ✅/❌ | [viewport tag] |
   | Text readable | ✅/⚠️/❌ | Font size: [X]px |
   | Tap targets sized | ✅/⚠️/❌ | [notes] |
   | Content fits viewport | ✅/❌ | [notes] |
   | No horizontal scroll | ✅/❌ | [notes] |
   
   ### Responsive Design Check
   
   | Element | Desktop | Mobile | Issues |
   |---------|---------|--------|--------|
   | Navigation | [status] | [status] | [notes] |
   | Images | [status] | [status] | [notes] |
   | Forms | [status] | [status] | [notes] |
   | Tables | [status] | [status] | [notes] |
   | Videos | [status] | [status] | [notes] |
   
   ### Mobile-First Indexing
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Mobile version has all content | ✅/⚠️/❌ | [notes] |
   | Mobile has same structured data | ✅/⚠️/❌ | [notes] |
   | Mobile has same meta tags | ✅/⚠️/❌ | [notes] |
   | Mobile images have alt text | ✅/⚠️/❌ | [notes] |
   
   **Mobile Score**: [X]/10
   ```

5. **安全性与HTTPS审计**
   ```markdown
   ## Security Analysis
   
   ### HTTPS Status
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | SSL certificate valid | ✅/❌ | Expires: [date] |
   | HTTPS enforced | ✅/❌ | [redirects properly?] |
   | Mixed content | ✅/⚠️/❌ | [X] issues |
   | HSTS enabled | ✅/⚠️ | [notes] |
   | Certificate chain | ✅/⚠️/❌ | [notes] |
   
   ### Security Headers
   
   | Header | Present | Value | Recommended |
   |--------|---------|-------|-------------|
   | Content-Security-Policy | ✅/❌ | [value] | [recommendation] |
   | X-Frame-Options | ✅/❌ | [value] | DENY or SAMEORIGIN |
   | X-Content-Type-Options | ✅/❌ | [value] | nosniff |
   | X-XSS-Protection | ✅/❌ | [value] | 1; mode=block |
   | Referrer-Policy | ✅/❌ | [value] | [recommendation] |
   
   **Security Score**: [X]/10
   ```

6. **URL结构审计**
   ```markdown
   ## URL Structure Analysis
   
   ### URL Pattern Review
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | HTTPS URLs | ✅/⚠️/❌ | [X]% HTTPS |
   | Lowercase URLs | ✅/⚠️/❌ | [notes] |
   | No special characters | ✅/⚠️/❌ | [notes] |
   | Readable/descriptive | ✅/⚠️/❌ | [notes] |
   | Appropriate length | ✅/⚠️/❌ | Avg: [X] chars |
   | Keywords in URLs | ✅/⚠️/❌ | [notes] |
   | Consistent structure | ✅/⚠️/❌ | [notes] |
   
   ### URL Issues Found
   
   | Issue Type | Count | Examples |
   |------------|-------|----------|
   | Dynamic parameters | [X] | [URLs] |
   | Session IDs in URLs | [X] | [URLs] |
   | Uppercase characters | [X] | [URLs] |
   | Special characters | [X] | [URLs] |
   | Very long URLs (>100) | [X] | [URLs] |
   
   ### Redirect Analysis
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Redirect chains | [X] found | [max chain length] |
   | Redirect loops | [X] found | [URLs] |
   | 302 → 301 needed | [X] found | [URLs] |
   | Broken redirects | [X] found | [URLs] |
   
   **URL Score**: [X]/10
   ```

7. **结构化数据审计**
   > **CORE-EEAT对齐性**：检查网站的结构化数据标记是否符合CORE-EEAT基准中的O05标准。有关全面的内容质量审计，请参阅[content-quality-auditor](../../cross-cutting/content-quality-auditor/)。

8. **国际SEO审计（如适用）**
   ```markdown
   ## International SEO Analysis
   
   ### Hreflang Implementation
   
   | Check | Status | Notes |
   |-------|--------|-------|
   | Hreflang tags present | ✅/❌ | [notes] |
   | Self-referencing | ✅/⚠️/❌ | [notes] |
   | Return tags present | ✅/⚠️/❌ | [notes] |
   | Valid language codes | ✅/⚠️/❌ | [notes] |
   | x-default tag | ✅/⚠️ | [notes] |
   
   ### Language/Region Targeting
   
   | Language | URL | Hreflang | Status |
   |----------|-----|----------|--------|
   | [en-US] | [URL] | [tag] | ✅/⚠️/❌ |
   | [es-ES] | [URL] | [tag] | ✅/⚠️/❌ |
   
   **International Score**: [X]/10
   ```

9. **生成技术性审计报告**
   ```markdown
   # Technical SEO Audit Report
   
   **Domain**: [domain]
   **Audit Date**: [date]
   **Pages Analyzed**: [X]
   
   ## Overall Technical Health: [X]/100
   
   ```
   评分详情：
   ████████░░ 可爬取性：8/10
   ███████░░░ 可索引性：7/10
   █████░░░░░ 网站性能：5/10
   ████████░░ 移动设备友好性：8/10
   █████████░ 安全性：9/10
   ██████░░░░ URL结构：6/10
   █████░░░░░ 结构化数据：5/10
   ```
   
   ## Critical Issues (Fix Immediately)
   
   1. **[Issue]**: [Impact] 
      - Affected: [pages/scope]
      - Solution: [specific fix]
      - Priority: 🔴 Critical
   
   2. **[Issue]**: [Impact]
      - Affected: [pages/scope]
      - Solution: [specific fix]
      - Priority: 🔴 Critical
   
   ## High Priority Issues
   
   1. **[Issue]**: [Solution]
   2. **[Issue]**: [Solution]
   
   ## Medium Priority Issues
   
   1. **[Issue]**: [Solution]
   2. **[Issue]**: [Solution]
   
   ## Quick Wins
   
   These can be fixed quickly for immediate improvement:
   
   1. [Quick fix 1]
   2. [Quick fix 2]
   3. [Quick fix 3]
   
   ## Implementation Roadmap
   
   ### Week 1: Critical Fixes
   - [ ] [Task 1]
   - [ ] [Task 2]
   
   ### Week 2-3: High Priority
   - [ ] [Task 1]
   - [ ] [Task 2]
   
   ### Week 4+: Optimization
   - [ ] [Task 1]
   - [ ] [Task 2]
   
   ## Monitoring Recommendations

   Set up alerts for:
   - Core Web Vitals drops
   - Crawl error spikes
   - Index coverage changes
   - Security issues
   ```

## 验证要求

### 输入验证
- 必须明确提供网站URL或域名。
- 必须能够访问技术性数据（如robots.txt文件、站点地图或爬取结果）。
- 必须提供性能指标数据（通过页面速度工具或截图获取）。

### 输出验证
- 每条建议都必须引用具体的数据来源。
- 所有问题都应包含受影响的URL或页面数量。
- 性能指标必须包含具体的数值（如秒数、KB等）。
- 必须明确说明数据来源（网络爬虫数据、页面速度工具数据、用户提供的数据或估算值）。

## 示例

**用户**：“检查cloudhosting.com的技术性SEO情况”

**审计结果：**
```markdown
# Technical SEO Audit Report

**Domain**: cloudhosting.com
**Audit Date**: 2024-09-15
**Pages Analyzed**: 312

## Crawlability Analysis

### Robots.txt Review

**URL**: cloudhosting.com/robots.txt
**Status**: Found

| Check | Status | Notes |
|-------|--------|-------|
| File exists | ✅ | 200 response |
| Valid syntax | ⚠️ | Wildcard pattern `Disallow: /*?` too aggressive — blocks faceted pages |
| Sitemap declared | ❌ | No Sitemap directive in robots.txt |
| Important pages blocked | ⚠️ | /pricing/ blocked by `Disallow: /pricing` rule |
| Assets blocked | ✅ | CSS/JS accessible |

**Issues Found**:
- Sitemap URL not declared in robots.txt
- `/pricing/` inadvertently blocked — high-value commercial page

### XML Sitemap Review

**Sitemap URL**: cloudhosting.com/sitemap.xml
**Status**: Found (not referenced in robots.txt)

| Check | Status | Notes |
|-------|--------|-------|
| Sitemap exists | ✅ | Valid XML, 287 URLs |
| Only indexable URLs | ❌ | 23 noindex URLs included |
| Includes lastmod | ⚠️ | All dates set to 2023-01-01 — not accurate |

**Crawlability Score**: 5/10

## Performance Analysis

### Core Web Vitals

| Metric | Mobile | Desktop | Target | Status |
|--------|--------|---------|--------|--------|
| LCP (Largest Contentful Paint) | 4.8s | 2.1s | <2.5s | ❌ Mobile / ✅ Desktop |
| FID (First Input Delay) | 45ms | 12ms | <100ms | ✅ / ✅ |
| CLS (Cumulative Layout Shift) | 0.24 | 0.08 | <0.1 | ❌ Mobile / ✅ Desktop |
| INP (Interaction to Next Paint) | 380ms | 140ms | <200ms | ❌ Mobile / ✅ Desktop |

### Additional Performance Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Time to First Byte (TTFB) | 1,240ms | ❌ |
| Page Size | 3.8MB | ❌ |
| Requests | 94 | ⚠️ |

**LCP Issues**:
- Uncompressed hero image (2.4MB PNG): Convert to WebP, est. save 1.9MB
- No CDN detected: TTFB 1,240ms from origin server

**CLS Issues**:
- Ad banner at top of page injects without reserved height (0.18 shift contribution)

**Performance Score**: 3/10

## Security Analysis

### HTTPS Status

| Check | Status | Notes |
|-------|--------|-------|
| SSL certificate valid | ✅ | Expires: 2025-03-22 |
| HTTPS enforced | ⚠️ | http://cloudhosting.com returns 200 instead of 301 redirect |
| Mixed content | ❌ | 7 images loaded over HTTP on /features/ page |
| HSTS enabled | ❌ | Header not present |

**Security Score**: 5/10

## Structured Data Analysis

### Schema Markup Found

| Schema Type | Pages | Valid | Errors |
|-------------|-------|-------|--------|
| Organization | 1 (homepage) | ✅ | None |
| Article | 0 | — | Missing on 48 blog posts |
| Product | 0 | — | Missing on 5 plan pages |
| FAQ | 0 | — | Missing on 12 pages with FAQ content |

**Structured Data Score**: 3/10

## Overall Technical Health: 42/100

```
评分详情：
█████░░░░░ 可爬取性：5/10
██████░░░░ 可索引性：6/10
███░░░░░░ 页面性能：3/10
██████░░░░░ 移动设备友好性：6/10
█████░░░░░ 安全性：5/10
██████░░░░ URL结构：6/10
███░░░░░ 结构化数据：3/10
```

## Priority Issues

### 🔴 Critical (Fix Immediately)
1. **Mobile LCP 4.8s (target <2.5s)** — Compress hero image to WebP (est. save 1.9MB) and implement a CDN to reduce TTFB from 1,240ms to <400ms.

### 🟡 Important (Fix Soon)
2. **HTTP not redirecting to HTTPS** — Add 301 redirect from http:// to https:// and enable HSTS header. 7 mixed-content images on /features/ need URL updates.

### 🟢 Minor (Optimize)
3. **No Article/FAQ schema on blog posts** — Add Article schema to 48 blog posts and FAQ schema to 12 FAQ pages for rich result eligibility.
```

## 技术性SEO检查清单

```markdown
### Crawlability
- [ ] robots.txt is valid and not blocking important content
- [ ] XML sitemap exists and is submitted to ~~search console
- [ ] No crawl errors in ~~search console
- [ ] No redirect chains or loops

### Indexability  
- [ ] Important pages are indexable
- [ ] Canonical tags are correct
- [ ] No duplicate content issues
- [ ] Pagination is handled correctly

### Performance
- [ ] Core Web Vitals pass
- [ ] Page speed under 3 seconds
- [ ] Images are optimized
- [ ] JS/CSS are minified

### Mobile
- [ ] Mobile-friendly test passes
- [ ] Viewport is configured
- [ ] Touch elements are properly sized

### Security
- [ ] HTTPS is enforced
- [ ] SSL certificate is valid
- [ ] No mixed content
- [ ] Security headers present

### Structure
- [ ] URLs are clean and descriptive
- [ ] Site architecture is logical
- [ ] Internal linking is strong
```

## 成功技巧

1. **按问题影响程度优先处理**——先修复关键问题。
2. **持续监控**——利用搜索控制台（search console）的警报功能。
3. **测试修改效果**——在广泛部署之前验证修复措施是否有效。
4. **详细记录所有操作**——便于后续问题排查。
5. **定期进行审计**——每季度安排一次技术性审查。

## 技术性SEO问题严重性分级

| 问题严重性 | 影响描述 | 例子 | 处理时间 |
|----------|-------------------|---------|---------------|
| **严重** | 阻止网站被索引或导致全局性问题** | robots.txt文件设置错误、关键页面被禁止索引、全站出现500错误 | 当天处理 |
| **较高** | 显著影响排名或用户体验** | 网页加载速度慢、缺少hreflang标签、重复内容、重定向链问题 | 1周内处理 |
| **中等** | 影响特定页面或造成中等程度的影响** | 缺少结构化数据标记、默认链接设置不当、内容页面质量较低 | 1个月内处理 |
| **较低** | 存在较小的优化空间** | 图像压缩、轻微的CLS（Cumulative Layout Shift）问题、非必要的结构化数据缺失 | 下一季度处理 |

## Core Web Vitals优化快速参考

### LCP（Largest Contentful Paint，最大内容绘制时间）优化

| 原因 | 检测方法 | 解决方案 |
|-----------|-----------|-----|
| 大尺寸的标题图片** | PageSpeed Insights工具 | 使用WebP格式、调整图片大小、添加`loading="lazy"`属性 |
| 阻碍页面渲染的CSS/JavaScript** | 开发工具（DevTools） | 延迟加载非关键代码、将关键代码内联 |
| 服务器响应缓慢** | 网页加载时间超过800毫秒 | 使用CDN、服务器端缓存、升级托管服务 |
| 第三方脚本** | 开发工具（DevTools Network） | 延迟加载或异步加载这些脚本 |

### CLS（Cumulative Layout Shift，累积布局偏移）优化

| 原因 | 检测方法 | 解决方案 |
|-----------|-----------|-----|
| 图片没有尺寸信息** | 开发工具（DevTools） | 为图片添加明确的宽度/高度属性 |
| 广告或嵌入内容没有预留显示空间** | 直观检查页面布局 | 为相关元素设置最小高度 |
| 导致页面布局混乱的Web字体** | 开发工具（DevTools） | 设置字体显示方式（font-display: swap）并预加载字体 |
| 动态内容插入** | 直观检查页面布局 | 使用CSS为动态内容预留显示空间 |

### INP（Interaction to Next Paint，交互到下一次绘制时间）优化

| 原因 | 检测方法 | 解决方案 |
|-----------|-----------|-----|
| JavaScript任务执行时间过长** | 开发工具（DevTools） | 将复杂任务分解为更小的部分、使用`requestIdleCallback` |
| 事件处理程序占用过多线程** | 开发工具（DevTools） | 使用节流（debounce/throttle）或被动事件监听器 |
| 主线程被阻塞** | 开发工具（DevTools） | 使用Web Workers处理耗时任务 |

## 参考资料

- [robots.txt文件参考](./references/robots-txt-reference.md) — robots.txt文件的语法指南、模板示例和常见配置。
- [HTTP状态码](./references/http-status-codes.md) — 各HTTP状态码对SEO的影响及重定向的最佳实践。

## 相关技能

- [页面SEO审核器](../on-page-seo-auditor/) — 用于检查页面SEO问题。
- [结构化数据标记生成器](../../build/schema-markup-generator/) — 用于修复结构化数据标记问题。
- [性能报告器](../../monitor/performance-reporter/) — 用于监控网站性能改进情况。
- [内部链接优化器](../internal-linking-optimizer/) — 用于修复链接问题。
- [警报管理器](../../monitor/alert-manager/) — 用于生成技术问题的警报通知。
- [内容质量审核器](../../cross-cutting/content-quality-auditor/) — 提供全面的80项核心评估（CORE-EEAT）。