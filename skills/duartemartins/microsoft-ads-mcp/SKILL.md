---
name: microsoft-ads-mcp
description: 通过 MCP 服务器创建和管理 Microsoft Advertising 广告活动（Bing Ads / DuckDuckGo Ads），包括活动、广告组、关键词、广告内容以及广告报告功能。
metadata: {"clawdbot":{"emoji":"📢","requires":{"commands":["mcporter"]},"homepage":"https://github.com/Duartemartins/microsoft-ads-mcp-server"}}
---

# Microsoft Ads MCP 服务器

该服务器支持通过编程方式创建和管理 Microsoft Advertising 广告活动，可全面管理 Bing 和 DuckDuckGo 搜索广告。

## 为何选择 Microsoft Advertising？

- **DuckDuckGo 集成**：Microsoft Advertising 支持 DuckDuckGo 的搜索广告服务，能够触达注重隐私的用户。
- **更低的点击成本（CPC）**：通常比 Google Ads 便宜 30-50%。
- **覆盖范围广泛**：整合了 Bing、Yahoo 和 AOL 的搜索资源。
- **从 Google 广告迁移**：可轻松迁移现有的广告活动。

## 设置步骤

### 1. 安装 MCP 服务器

```bash
git clone https://github.com/Duartemartins/microsoft-ads-mcp-server.git
cd microsoft-ads-mcp-server
pip install -r requirements.txt
```

### 2. 获取凭证

1. **Microsoft Advertising 账户**：在 [ads.microsoft.com](https://ads.microsoft.com) 注册账户。
2. **开发者令牌（Developer Token）**：在 [developers.ads.microsoft.com](https://developers.ads.microsoft.com) 申请。
3. **Azure AD 应用程序（Azure AD App）**：在 [portal.azure.com](https://portal.azure.com) 创建应用程序，并设置重定向 URI 为 `https://login.microsoftonline.com/common/oauth2/nativeclient`。

### 3. 配置 `mcporter`

将以下配置添加到 `~/.mcporter/mcporter.json` 文件中：

```json
{
  "mcpServers": {
    "microsoft-ads": {
      "command": "python3",
      "args": ["/path/to/microsoft-ads-mcp-server/server.py"],
      "type": "stdio",
      "env": {
        "MICROSOFT_ADS_DEVELOPER_TOKEN": "your_token",
        "MICROSOFT_ADS_CLIENT_ID": "your_azure_app_client_id"
      }
    }
  }
}
```

### 4. 进行身份验证

```bash
mcporter call microsoft-ads.get_auth_url
# Open URL in browser, sign in, copy redirect URL
mcporter call microsoft-ads.complete_auth '{"redirect_url": "https://login.microsoftonline.com/common/oauth2/nativeclient?code=..."}'
```

## 可用工具

### 账户管理
```bash
mcporter call microsoft-ads.search_accounts
```

### 广告活动操作
```bash
# List campaigns
mcporter call microsoft-ads.get_campaigns

# Create campaign (starts paused for safety)
mcporter call microsoft-ads.create_campaign '{"name": "My Campaign", "daily_budget": 20}'

# Activate or pause
mcporter call microsoft-ads.update_campaign_status '{"campaign_id": 123456, "status": "Active"}'
```

### 广告组
```bash
# List ad groups
mcporter call microsoft-ads.get_ad_groups '{"campaign_id": 123456}'

# Create ad group
mcporter call microsoft-ads.create_ad_group '{"campaign_id": 123456, "name": "Product Keywords", "cpc_bid": 1.50}'
```

### 关键词
```bash
# List keywords
mcporter call microsoft-ads.get_keywords '{"ad_group_id": 789012}'

# Add keywords (Broad, Phrase, or Exact match)
mcporter call microsoft-ads.add_keywords '{"ad_group_id": 789012, "keywords": "buy widgets, widget store", "match_type": "Phrase", "default_bid": 1.25}'
```

### 广告内容
```bash
# List ads
mcporter call microsoft-ads.get_ads '{"ad_group_id": 789012}'

# Create Responsive Search Ad
mcporter call microsoft-ads.create_responsive_search_ad '{
  "ad_group_id": 789012,
  "final_url": "https://example.com/widgets",
  "headlines": "Buy Widgets Online|Best Widget Store|Free Shipping",
  "descriptions": "Shop our selection. Free shipping over $50.|Quality widgets at great prices."
}'
```

### 报告功能
```bash
# Submit report request
mcporter call microsoft-ads.submit_campaign_performance_report '{"date_range": "LastWeek"}'
mcporter call microsoft-ads.submit_keyword_performance_report '{"date_range": "LastMonth"}'
mcporter call microsoft-ads.submit_search_query_report '{"date_range": "LastWeek"}'
mcporter call microsoft-ads.submit_geographic_report '{"date_range": "LastMonth"}'

# Check status and get download URL
mcporter call microsoft-ads.poll_report_status
```

### 其他功能
```bash
mcporter call microsoft-ads.get_budgets
mcporter call microsoft-ads.get_labels
```

## 完整的工作流程示例

```bash
# 1. Check account
mcporter call microsoft-ads.search_accounts

# 2. Create campaign
mcporter call microsoft-ads.create_campaign '{"name": "PopaDex - DDG Search", "daily_budget": 15}'
# Returns: Campaign ID 123456

# 3. Create ad group
mcporter call microsoft-ads.create_ad_group '{"campaign_id": 123456, "name": "Privacy Keywords", "cpc_bid": 0.75}'
# Returns: Ad Group ID 789012

# 4. Add keywords
mcporter call microsoft-ads.add_keywords '{
  "ad_group_id": 789012,
  "keywords": "privacy search engine, private browsing, anonymous search",
  "match_type": "Phrase",
  "default_bid": 0.60
}'

# 5. Create ad
mcporter call microsoft-ads.create_responsive_search_ad '{
  "ad_group_id": 789012,
  "final_url": "https://popadex.com",
  "headlines": "PopaDex Private Search|Search Without Tracking|Privacy-First Search Engine",
  "descriptions": "Search the web without being tracked. No ads, no profiling.|Your searches stay private. Try PopaDex today."
}'

# 6. Activate campaign
mcporter call microsoft-ads.update_campaign_status '{"campaign_id": 123456, "status": "Active"}'

# 7. Check performance after a few days
mcporter call microsoft-ads.submit_campaign_performance_report '{"date_range": "LastWeek"}'
mcporter call microsoft-ads.poll_report_status
```

## 匹配类型

| 匹配类型 | 语法 | 触发条件 |
|------|--------|----------|
| 广义匹配（Broad） | `keyword` | 相关搜索词、同义词 |
| 短语匹配（Phrase） | `"keyword"` | 必须按顺序包含该短语 |
| 精确匹配（Exact） | `[keyword]` | 仅精确匹配该关键词 |

## 报告列

**广告活动报告**：CampaignName（广告活动名称）、Impressions（展示次数）、Clicks（点击次数）、Ctr（点击率）、AverageCpc（平均点击成本）、Spend（花费）、Conversions（转化次数）、Revenue（收入）

**关键词报告**：Keyword（关键词）、AdGroupName（广告组名称）、CampaignName（广告活动名称）、Impressions（展示次数）、Clicks（点击次数）、Ctr（点击率）、AverageCpc（平均点击成本）、Spend（花费）、Conversions（转化次数）、QualityScore（质量得分）

**搜索查询报告**：SearchQuery（搜索查询）、Keyword（关键词）、CampaignName（广告活动名称）、Impressions（展示次数）、Clicks（点击次数）、Spend（花费）、Conversions（转化次数）

**地理位置报告**：Country（国家）、State（州）、City（城市）、CampaignName（广告活动名称）、Impressions（展示次数）、Clicks（点击次数）、Spend（花费）、Conversions（转化次数）

## 使用技巧

1. **广告活动默认为暂停状态**：新创建的广告活动默认处于暂停状态，请在启用前仔细检查。
2. **使用短语匹配**：对于大多数关键词来说，短语匹配能在覆盖范围和相关性之间取得良好的平衡。
3. **设置多个广告标题**：对于某些广告类型（如 RSAs），建议设置 3-15 个标题（每个标题不超过 30 个字符）和 2-4 个描述（每个描述不超过 90 个字符）。
4. **检查搜索查询**：仔细审查实际搜索词，以识别可能引起负面效果的关键词。
5. **地理位置定位**：利用地理位置报告来优化广告投放。

## 致谢

MCP 服务器的源代码托管在 [github.com/Duartemartins/microsoft-ads-mcp-server](https://github.com/Duartemartins/microsoft-ads-mcp-server)。

该服务器基于 [FastMCP](https://github.com/jlowin/fastmcp) 和 [Bing Ads Python SDK](https://github.com/BingAds/BingAds-Python-SDK) 开发。