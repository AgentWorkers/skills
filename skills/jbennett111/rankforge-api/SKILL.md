---
name: rankforge-api
description: "使用 RankForge API 进行全面的 SEO 分析与优化：包括 SEO 审计、网站审计、关键词研究、关键词分析、搜索引擎优化（SEO）、竞争对手分析、搜索结果页面（SERP）分析、排名分析、反向链接分析、技术性 SEO（Technical SEO）、页面内 SEO（On-Page SEO）、页面外 SEO（Off-Page SEO）、关键词难度评估、搜索量分析、关键词建议、内容优化、元标签分析、网站性能评估、SEO 评分、搜索排名分析、自然流量分析、关键词跟踪、SEO 建议、网站健康状况检查、爬虫分析、索引问题排查、移动设备优化（Mobile SEO）、页面速度分析、结构化数据标记（Schema Markup）分析以及全面的搜索引擎可见性优化。"
---
# RankForge API 技能

使用 VCG 的 RankForge API 进行全面的 SEO 分析和优化——提供专业的 SEO 审计、关键词研究和竞争对手分析功能。

## 快速入门

1. **获取 API 密钥**：帮助用户免费注册 RankForge API 密钥。
2. **保存密钥**：安全地存储密钥。
3. **运行 SEO 分析**：审计网站、研究关键词、分析竞争对手。

## API 密钥注册

### 第 1 步：获取用户邮箱
请求用户的邮箱地址以创建一个免费的 RankForge 账户。

### 第 2 步：通过 API 注册
```bash
curl -X POST https://rankforge.vosscg.com/v1/keys \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

**预期响应：**
```json
{
  "api_key": "rf_9876543210fedcba",
  "message": "API key created successfully",
  "tier": "free",
  "daily_limit": 50
}
```

### 第 3 步：保存 API 密钥
将 API 密钥安全保存以供将来使用。提醒用户妥善保管密钥。

## 核心 SEO 分析功能

### 网站 SEO 审计
```bash
curl -X POST https://rankforge.vosscg.com/v1/audit \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "depth": "full",
    "include": ["technical", "content", "performance", "mobile"]
  }'
```

**预期响应：**
```json
{
  "audit_id": "aud_12345",
  "url": "https://example.com",
  "overall_score": 78,
  "issues": {
    "critical": 3,
    "warnings": 12,
    "recommendations": 8
  },
  "categories": {
    "technical_seo": 85,
    "on_page_seo": 72,
    "performance": 68,
    "mobile_friendly": 90
  },
  "details": "Full audit report with actionable recommendations"
}
```

### 关键词研究
```bash
curl -X POST https://rankforge.vosscg.com/v1/keywords/research \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "seed_keywords": ["digital marketing", "SEO tools"],
    "location": "US",
    "language": "en",
    "include_metrics": true
  }'
```

**预期响应：**
```json
{
  "keywords": [
    {
      "keyword": "digital marketing agency",
      "search_volume": 12000,
      "difficulty": 65,
      "cpc": 8.50,
      "competition": "high",
      "related_keywords": ["marketing agency", "digital advertising"]
    }
  ],
  "total_found": 150,
  "suggestions": 25
}
```

### 竞争对手分析
```bash
curl -X POST https://rankforge.vosscg.com/v1/competitors/analyze \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://mysite.com",
    "competitors": ["https://competitor1.com", "https://competitor2.com"],
    "metrics": ["keywords", "backlinks", "content", "technical"]
  }'
```

**预期响应：**
```json
{
  "target": {
    "url": "https://mysite.com",
    "domain_authority": 45,
    "organic_keywords": 2340,
    "total_backlinks": 1250
  },
  "competitors": [
    {
      "url": "https://competitor1.com",
      "domain_authority": 62,
      "organic_keywords": 4580,
      "total_backlinks": 3200,
      "gap_analysis": {
        "keyword_opportunities": 150,
        "content_gaps": 23,
        "backlink_opportunities": 85
      }
    }
  ]
}
```

### SERP 分析
```bash
curl -X GET "https://rankforge.vosscg.com/v1/serp?keyword=digital%20marketing&location=US" \
  -H "X-API-Key: rf_9876543210fedcba"
```

### 外部链接分析
```bash
curl -X POST https://rankforge.vosscg.com/v1/backlinks/analyze \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "filters": {
      "domain_rating": ">30",
      "status": "active",
      "type": ["follow", "nofollow"]
    }
  }'
```

### 技术 SEO 检查
```bash
curl -X POST https://rankforge.vosscg.com/v1/technical-seo \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "checks": [
      "crawlability",
      "indexability", 
      "page_speed",
      "mobile_usability",
      "schema_markup",
      "ssl_certificate"
    ]
  }'
```

### 关键词跟踪
```bash
curl -X POST https://rankforge.vosscg.com/v1/rankings/track \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "keywords": ["seo tools", "keyword research", "rank tracking"],
    "location": "US",
    "device": "desktop"
  }'
```

## 高级功能

### 内容优化分析
```bash
curl -X POST https://rankforge.vosscg.com/v1/content/optimize \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "target_keyword": "SEO best practices",
    "analysis_type": "comprehensive"
  }'
```

### 本地 SEO 分析
```bash
curl -X POST https://rankforge.vosscg.com/v1/local-seo \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "business": {
      "name": "Local Business",
      "address": "123 Main St, City, State",
      "phone": "+1234567890"
    },
    "target_location": "City, State"
  }'
```

### 网站速度分析
```bash
curl -X POST https://rankforge.vosscg.com/v1/performance/analyze \
  -H "X-API-Key: rf_9876543210fedcba" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "device": "both",
    "metrics": ["lcp", "fid", "cls", "ttfb"]
  }'
```

## 常见用例

### 完整的 SEO 审计工作流程
```bash
# 1. Site audit
curl -X POST https://rankforge.vosscg.com/v1/audit \
  -H "X-API-Key: [API_KEY]" -d '{"url":"site.com"}'

# 2. Keyword research
curl -X POST https://rankforge.vosscg.com/v1/keywords/research \
  -H "X-API-Key: [API_KEY]" -d '{"seed_keywords":["main topic"]}'

# 3. Competitor analysis
curl -X POST https://rankforge.vosscg.com/v1/competitors/analyze \
  -H "X-API-Key: [API_KEY]" -d '{"target_url":"site.com"}'

# 4. Technical SEO check
curl -X POST https://rankforge.vosscg.com/v1/technical-seo \
  -H "X-API-Key: [API_KEY]" -d '{"url":"site.com"}'
```

## 错误处理

常见错误响应：
- `401 未授权`：API 密钥无效或缺失。
- `429 请求过多`：超出每日限制（免费用户每天 50 次请求）。
- `400 错误请求`：URL 或参数无效。
- `404 未找到`：URL 无法用于分析。
- `503 服务不可用`：分析正在进行中，请稍后再试。

## 价格与限制

**免费 tier：**
- 每天 50 次请求。
- 基本 SEO 审计。
- 关键词研究（每次查询最多 100 个关键词）。
- 竞争对手分析（最多 3 个竞争对手）。
- 技术 SEO 检查。

**付费计划：**
- 访问 [https://vosscg.com/forges](https://vosscg.com/forges) 升级以获得更多权限。
- 高级分析和历史数据。
- 白标签报告和 API 访问权限。
- 优先处理和支持。

## 最佳实践

1. **全面审计**：进行包括技术、内容和性能在内的全面审计。
2. **定期监控**：设置关键词跟踪以持续优化。
3. **竞争对手情报**：监控竞争对手的变化和机会。
4. **以行动为导向**：优先处理具有高影响力的建议。
5. **移动优先**：在审计中始终包含移动设备分析。
6. **本地优化**：针对本地业务使用本地 SEO 工具。

## 集成示例

### OpenClaw 代理工作流程
```bash
# Help user get API key
curl -X POST https://rankforge.vosscg.com/v1/keys -d '{"email":"user@domain.com"}'

# Run comprehensive SEO analysis based on user request
curl -X POST https://rankforge.vosscg.com/v1/audit \
  -H "X-API-Key: [USER_API_KEY]" \
  -d '{"url":"[USER_WEBSITE]", "depth":"full"}'

# Present actionable insights and recommendations
```

当用户需要 SEO 分析、提升搜索排名、研究关键词、审计网站性能或分析竞争对手时，可以使用此技能通过 RankForge 的全面分析工具提供专业级的 SEO 指导。