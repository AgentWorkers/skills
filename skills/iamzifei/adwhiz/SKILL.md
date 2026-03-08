---
name: adwhiz
description: 通过您的人工智能编程工具，您可以管理 Google 广告和 Meta（Facebook）广告。该工具提供了 99 种用于审计、创建和优化广告账户的功能，全部通过自然语言界面实现。
metadata:
  openclaw:
    primaryEnv: "ADWHIZ_API_KEY"
    requires:
      env:
        - "ADWHIZ_API_KEY"
    homepage: "https://adwhiz.ai"
    source: "https://github.com/iamzifei/adwhiz"
    license: "MIT"
---
# AdWhiz — Google Ads 与 Meta Ads 的 MCP 服务器

AdWhiz 是一个托管式的 MCP（广告管理平台）服务器，它通过安全的、经过身份验证的代理将您的 AI 编码工具连接到 Google Ads API 和 Meta (Facebook) Graph API。该服务器提供了 **99 种工具**，涵盖 7 个类别，使您能够使用简单的英语语法来审计、创建和管理两个平台上的广告活动。

所有 API 调用都通过您的个人 `ADWHIZ_API_KEY` 进行身份验证，并通过位于 `mcp.adwhiz.ai` 的 AdWhiz 服务器进行路由。AdWhiz 服务器不会存储任何 Google 或 Meta 的凭证——身份验证过程完全在服务器端完成，您需要在 https://adwhiz.ai/connect 链接您的广告账户后完成身份验证。

## 安全性与权限模型

- **OAuth 2.0**：用户通过 AdWhiz 的网页界面使用 Google 和/或 Meta 进行身份验证。刷新令牌（Google）和长期有效的访问令牌（Meta）在存储时会被加密（使用 AES-256-GCM 算法），并且永远不会暴露给代理程序。
- **API 密钥范围**：每个 `ADWHIZ_API_KEY` 仅绑定到单个用户的已连接账户。跨用户访问是不允许的。
- **写入安全**：所有 Google Ads 的写入工具默认会将创建的实体设置为 **暂停**（PAUSED）状态。Meta 的写入工具需要明确指定状态参数。
- **变更记录**：每次变更都会被记录在 `get_operation_log` 工具中，以便进行全面审计。
- **默认为只读**：99 种工具中有 36 种是严格只读的，无法修改您的账户信息。
- **需要用户确认**：写入工具在执行前需要用户通过代理程序的标准权限流程进行确认。
- **禁止任意代码执行**：MCP 服务器是一个托管的 HTTP 服务。除了薄层的 MCP 客户端封装外，不会在用户的机器上下载或执行任何代码。

## Google Ads 工具（70 种）

### 账户相关工具（2 种）——只读
| 工具 | 描述 |
|------|-------------|
| `list_accounts` | 列出所有可访问的 Google Ads 账户（自动展开 MCC 子账户） |
| `get_account_info` | 获取账户详情（货币、时区、优化得分） |

### 读取相关工具（20 种）——只读
| 工具 | 描述 |
|------|-------------|
| `list_campaigns` | 列出广告活动的状态、类型、预算和出价策略 |
| `get_campaign_performance` | 广告活动指标：成本、点击量、转化率、每次点击成本（CPA）、投资回报率（ROAS） |
| `list_ad_groups` | 列出广告组及其出价（可按广告活动过滤） |
| `list_ads` | 列出广告及其标题、描述和最终链接 |
| `list_keywords` | 列出关键词及其匹配类型、出价和质量得分 |
| `get_search_terms` | 搜索词报告（实际触发广告的查询词） |
| `list_negative_keywords` | 在广告活动、广告组或账户级别添加否定关键词 |
| `list_assets` | 网站链接、呼叫-out（callouts）和结构化片段（structured snippets） |
| `list_conversion_actions` | 转化动作及其状态和类型 |
| `list_budgets` | 与广告活动关联的预算 |
| `list_bidding_strategies` | 投标策略组合 |
| `list_audience_segments` | 目标受众段 |
| `list_user_lists` | 用于定向的再营销/受众列表 |
| `get_operation_log` | 通过 AdWhiz 执行的最新变更记录 |
| `list_recommendations` | Google Ads 建议（添加关键词、提高出价、调整广告强度） |
| `get_change_history` | 变更审计日志：谁在何时更改了什么 |
| `list_geo_targets` | 广告活动的地理位置定位 |
| `list_ad_schedules` | 广告活动的日程安排（按时间段划分） |
| `list_labels` | 用于组织广告活动、广告组和关键词的标签 |
| `generate_keyword_ideas` | 根据搜索量、竞争情况和出价范围生成关键词建议 |

### 编写相关工具（45 种）——需要用户确认
| 工具 | 描述 |
|------|-------------|
| `create_campaign` | 创建搜索广告活动、展示广告活动、Performance Max（PMax）或视频广告活动（默认为暂停状态） |
| `update_campaign` | 更新广告活动名称 |
| `set_campaign_status` | 暂停、启用或删除广告活动 |
| `create_ad_group` | 在广告活动中创建广告组 |
| `update_ad_group` | 更新广告组名称或 CPC 出价 |
| `set_ad_group_status` | 暂停、启用或删除广告组 |
| `create_responsive_search_ad` | 创建响应式搜索广告（RSA），包含标题和描述（默认为暂停状态） |
| `set_ad_status` | 暂停、启用或删除广告 |
| `add_keywords` | 添加关键词及其匹配类型和出价 |
| `update_keyword_bid` | 更改关键词的 CPC 出价 |
| `set_keyword_status` | 暂停、启用或删除关键词 |
| `add_negative_keyword` | 在广告活动或广告组级别添加否定关键词 |
| `remove_negative_keyword` | 删除否定关键词 |
| `create_shared_negative_list` | 创建共享的否定关键词列表 |
| `add_to_shared_list` | 将关键词添加到共享的否定关键词列表 |
| `attach_shared_list` | 将共享列表关联到广告活动 |
| `create_sitelink` | 创建网站链接资产 |
| `create_callout` | 创建呼叫-out（callout）资产 |
| `create_structured_snippet` | 创建结构化片段资产 |
| `create_price_extension` | 创建价格扩展资产 |
| `link_asset_to_campaign` | 将资产关联到广告活动 |
| `unlink_asset_from_campaign` | 从广告活动中解除资产关联 |
| `create_conversion_action` | 创建转化跟踪动作 |
| `update_conversion_action` | 更新转化跟踪动作的名称或状态 |
| `create_budget` | 创建广告活动预算 |
| `update_budget` | 更新预算金额或名称 |
| `create_bidding_strategy` | 创建投标策略组合 |
| `add_audience_to_campaign` | 为广告活动添加目标受众 |
| `update_responsive_search_ad` | 更新响应式搜索广告的标题、描述或链接 |
| `link_asset_to_ad_group` | 将资产关联到广告组 |
| `unlink_asset_from_ad_group` | 从广告组解除资产关联 |
| `upload_click_conversions` | 上传离线点击转化数据（基于 gclid） |
| `upload_customer_list` | 上传哈希处理的 PII 数据到客户匹配用户列表 |
| `apply_recommendation` | 应用 Google Ads 建议 |
| `dismiss_recommendation` | 取消 Google Ads 建议 |
| `add_geo_targeting` | 为广告活动添加地理位置定位 |
| `remove_geo_targeting` | 从广告活动中删除地理位置定位 |
| `add_ad_schedule` | 为广告活动添加日程安排（按时间段划分） |
| `remove_ad_schedule` | 从广告活动中删除日程安排规则 |
| `set_device_bid_adjustment` | 设置设备出价调整（移动设备、桌面设备、平板电脑） |
| `set_demographic_targeting` | 设置人口统计目标（年龄、性别、收入） |
| `create_label` | 创建用于组织实体的标签 |
| `apply_label` | 将标签应用到广告活动、广告组或广告 |
| `remove_label` | 从广告活动、广告组或广告中删除标签 |
| `create_asset_group` | 为 Performance Max 广告活动创建资产组 |

### 审计相关工具（2 种）——只读分析
| 工具 | 描述 |
|------|-------------|
| `run_mini_audit` | 快速审计：浪费的支出、最佳/最差的 CPA、预计节省额 |
| `run_full_audit` | 全面审计：广告活动、关键词、搜索词、问题和建议 |

### 查询相关工具（1 种）——只读，有使用限制
| 工具 | 描述 |
|------|-------------|
| `run_gaql_query` | 对您的账户执行只读的 GAQL 查询（最多 1,000 行，仅支持 SELECT 操作）

## Meta (Facebook) Ads 工具（29 种）

### Meta 读取相关工具（13 种）——只读
| 工具 | 描述 |
|------|-------------|
| `meta_list_ad_accounts` | 列出所有连接的 Meta 广告账户 |
| `meta_list_campaigns` | 列出广告活动的状态、目标和预算 |
| `meta_get_campaign_insights` | 每个广告活动的指标：支出、点击量、转化率、每次点击成本（CPA）、频率（可选细分） |
| `meta_list_ad_sets` | 列出广告集及其定位信息、状态和预算 |
| `meta_list_ads` | 列出广告及其创意详情（标题、正文、图片链接） |
| `meta_get_account_insights` | 账户级别的汇总指标（每日细分） |
| `meta_get_ad_set_insights` | 每个广告集的绩效指标：支出、点击量、每次点击成本（CPA）、频率 |
| `meta_get_ad_insights` | 每个广告的绩效指标：支出、点击量、转化率（CPA） |
| `meta_get_ad_creatives` | 列出广告创意或获取特定广告的创意 |
| `meta_search_interests` | 根据关键词搜索可定向的兴趣受众 |
| `meta_search_geo_locations` | 搜索可用于定向的地理位置 |
| `meta_estimate_audience_size` | 估计定向目标的覆盖范围 |
| `meta_get_account_pages` | 列出可用于投放广告的 Facebook 页面 |

### Meta 编写相关工具（15 种）——需要用户确认
| 工具 | 描述 |
|------|-------------|
| `meta_set_campaign_status` | 暂停或启用 Meta 广告活动 |
| `meta_update_campaign_budget` | 更新 Meta 广告活动的每日或生命周期预算 |
| `meta_set_ad_set_status` | 暂停或启用 Meta 广告集 |
| `meta_set_ad_status` | 暂停或启用 Meta 广告 |
| `meta_create_campaign` | 创建新的 Meta 广告活动，指定目标和预算 |
| `meta_create_ad_set` | 创建广告集，指定定位信息、预算和优化目标 |
| `meta_create_ad_creative` | 创建广告创意（包含图片/视频、链接、呼叫动作 CTA） |
| `meta_create_ad` | 创建广告，将广告集与创意关联 |
| `meta_update_campaign` | 更新广告活动名称、预算、结束时间、支出上限 |
| `meta_update_ad_set` | 更新广告集名称、预算、定位信息和日程安排 |
| `meta_update_ad` | 更新广告名称、创意或状态 |
| `meta_create_custom_audience` | 根据客户列表或网站访问者创建自定义受众 |
| `meta_create_lookalike_audience` | 根据源受众创建相似受众 |
| `meta_upload_ad_image` | 从 URL 上传广告创意的图片 |
| `meta_duplicate_campaign` | 复制包含所有广告集和广告的广告活动 |

### Meta 审计相关工具（1 种）——只读分析
| 工具 | 描述 |
|------|-------------|
| `meta_run_mini_audit` | 快速健康状况审计：根据浪费的支出、CPA 效率、预算利用率和创意使用情况打分（0-100 分）

## MCP 服务器配置

AdWhiz 使用 **HTTP 传输** 与托管的 MCP 服务器进行连接。在运行时不会下载或执行任何 npm 包。

```json
{
  "mcpServers": {
    "adwhiz": {
      "transport": "http",
      "url": "https://mcp.adwhiz.ai/mcp",
      "headers": {
        "Authorization": "Bearer ${ADWHIZ_API_KEY}"
      }
    }
  }
}
```

## REST API（MCP 的替代方案）

对于无法使用 MCP 协议的平台（如 GPT Actions、Dify、Coze 或任何基于 HTTP 的工作流），AdWhiz 还提供了所有 99 种工具作为标准 REST API，遵循 OpenAPI 3.1.0 规范：

- **OpenAPI 规范**：https://mcp.adwhiz.ai/api/v1/openapi.json |
- **工具列表**：https://mcp.adwhiz.ai/api/v1/tools |
- **工具执行**：`POST https://mcp.adwhiz.ai/api/v1/tools/{tool_name}`

将 OpenAPI 规范 URL 导入支持 OpenAPI 功能的任何平台，以便自动发现所有 99 种工具。

## 快速安装

```bash
clawhub install adwhiz
```

这将上述 MCP 服务器配置添加到您的设置中。系统会提示您提供您的 `ADWHIZ_API_KEY`。

## 获取 API 密钥

1. 在 https://adwhiz.ai 注册账号。
2. 通过 OAuth 将您的 Google Ads 和/或 Meta Ads 账户连接到 AdWhiz。
3. 从仪表板设置页面复制您的 API 密钥。

## 示例命令

### Google Ads
- “审计我的 Google Ads 账户，并显示支出最高的 5 个领域”
- “暂停所有 CPA 超过 150 美元的广告活动”
- “将这些否定关键词添加到我的搜索广告活动中：[列表]”
- “创建一个新的搜索广告活动，目标受众为纽约的律师，预算为每天 100 美元”
- “显示浪费资金的搜索词，并建议添加否定关键词”
- “我这个月的平均质量得分是多少？”

### Meta Ads
- “审计我的 Meta Ads 账户，并显示健康状况得分”
- “列出所有活跃的 Meta 广告活动及其支出和转化率”
- “暂停频率最高的 Meta 广告活动”
- “显示我账户过去 30 天的每日支出趋势”
- “哪些 Meta 广告集的 CPA 最低？”

## 数据处理

- AdWhiz 仅访问您明确连接的广告账户。
- 每个 API 请求结束后，广告活动数据不会被保存。
- 变更日志会保留 30 天，以便进行审计。
- 您可以随时通过 https://adwhiz.ai/connect 撤销访问权限。

## 文档

完整文档：https://adwhiz.ai/docs