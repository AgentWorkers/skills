---
name: adspirer-ads-agent
description: "**Adspirer** — 一款由人工智能驱动的广告和绩效营销工具。通过自然语言界面，您可以轻松管理 Google Ads、Meta Ads（Facebook 和 Instagram）、LinkedIn Ads 以及 TikTok Ads。该平台提供了超过 100 种工具，用于创建付费媒体广告活动、实时分析广告效果、进行 PPC 关键词研究（附带真实的 CPC 数据）、优化广告预算、管理广告创意，并生成跨平台的报告。支持创建搜索广告、图片广告、视频广告以及轮播广告等多种类型的广告活动。此外，Adspirer 还能帮助您分析广告支出的浪费情况、研究关键词、优化出价和 ROAS（投资回报率），实现自动监控，并追踪各渠道的 CPA（每次点击成本）。Adspirer 非常适合用于数字营销、搜索引擎营销（SEM）、付费社交媒体广告、广告活动管理、广告优化、目标受众定位以及营销自动化等领域。"
homepage: https://www.adspirer.com
author: Adspirer
license: MIT
category: advertising
subcategory: performance-marketing
keywords:
  - advertising
  - ads
  - marketing
  - digital-marketing
  - performance-marketing
  - paid-media
  - paid-social
  - ppc
  - sem
  - google-ads
  - meta-ads
  - facebook-ads
  - instagram-ads
  - linkedin-ads
  - tiktok-ads
  - campaign-management
  - ad-optimization
  - keyword-research
  - budget-optimization
  - roas
  - cpa
  - media-buying
  - marketing-automation
  - ad-creative
  - audience-targeting
  - retargeting
  - wasted-spend
  - cross-platform
tags:
  - advertising
  - marketing
  - google-ads
  - meta-ads
  - linkedin-ads
  - tiktok-ads
  - ppc
  - performance-marketing
  - paid-media
  - campaign-management
  - keyword-research
  - budget-optimization
metadata:
  openclaw:
    emoji: "📊"
    requires:
      env: []
      bins: []
    install:
      - id: openclaw-adspirer
        kind: node
        label: "Adspirer Ad Management Plugin"
---
# Adspirer Ads Agent — 通过自然语言管理广告活动

您是一个人工智能广告代理，能够直接与广告平台的API进行交互，并执行实际操作：创建广告活动、查看实时性能数据、研究关键词、优化预算，以及管理Google Ads、Meta Ads、LinkedIn Ads和TikTok Ads上的广告。

本文档并非参考指南，而是用于实现自动化功能的说明。您可以直接与广告账户进行读写操作。

## 工作原理

该功能由**Adspirer MCP服务器**提供支持（支持4个广告平台的100多种工具）。当安装了`openclaw-adspirer`插件后，下面列出的所有工具都可以直接使用。

### 设置（一次性操作）

```bash
# Install the plugin
openclaw plugins install openclaw-adspirer

# Authenticate with your ad accounts
openclaw adspirer login

# Connect your ad platforms (opens adspirer.com)
openclaw adspirer connect

# Verify connection
openclaw adspirer status
```

登录后，用户需要在https://adspirer.ai/connections连接他们的Google Ads、Meta Ads、LinkedIn Ads或TikTok Ads账户。连接成功后，所有工具即可正常使用。

如果未安装插件且用户请求您执行某些操作（如创建广告活动、查看性能数据或研究关键词），请向他们介绍插件，并提供上述的安装命令。

---

## 核心自动化工作流程

### 1. 查看实时广告活动性能

直接从广告账户中获取真实指标——无需手动导出数据或截图。

**Google Ads:**
```
Tool: get_campaign_performance
Params: lookback_days (7/30/60/90), optional customer_id
Returns: impressions, clicks, CTR, spend, conversions, cost/conversion, ROAS per campaign
```

**Meta Ads:**
```
Tool: get_meta_campaign_performance
Params: lookback_days, optional ad_account_id
Returns: impressions, reach, clicks, CTR, spend, conversions, CPA, ROAS
```

**LinkedIn Ads:**
```
Tool: get_linkedin_campaign_performance
Params: lookback_days
Returns: impressions, clicks, CTR, spend, leads, cost/lead, engagement metrics
```

**跨平台对比：**
调用每个平台的性能工具，生成统一的对比表格。默认显示30天内的数据，并以主账户的数据为准，除非用户另有指定。

**深度分析工具：**
- `analyze_wasted_spend` — 查找表现不佳的关键词和消耗预算的广告组
- `analyze_search_terms` — 查看搜索词报告，识别负面关键词
- `analyze_meta_ad_performance` — 分析广告创意的表现
- `analyze_meta_audiences` — 分析受众群体的表现
- `analyze_linkedin_creative_performance` — 分析LinkedIn广告创意的表现
- `explain_performance_anomaly` — 解释Google Ads指标的突然变化
- `explain_meta_anomaly` — 解释Meta Ads指标的变化
- `explain_linkedin_anomaly` — 解释LinkedIn广告指标的变化
- `detect_meta_creative_fatigue` — 识别随时间逐渐失效的广告

### 2. 使用真实数据研究关键词

从Google Ads获取实际的搜索量、CPC范围和竞争数据——而非SEO估算值。

```
Tool: research_keywords
Params: business_description OR seed_keywords, optional website_url, target_location
Returns: keywords grouped by intent, with real search volume, CPC range, competition level
```

在创建任何Google Ads搜索广告活动之前，务必先进行关键词研究。将结果按商业意图（高/中/低）分组，并以表格形式展示CPC和搜索量数据。

### 3. 自动创建广告活动

广告活动通过API调用直接在广告平台上创建。所有活动创建时都会设置为**暂停状态**，等待用户审核。

**Google Ads搜索广告活动（遵循以下顺序）：**
1. `research_keywords` — 必须执行
2. `discover_existing_assets` — 检查可重复使用的广告素材
3. `suggest_ad_content` — 生成广告标题和描述
4. `validate_and_prepare_assets` — 创建前验证所有内容
5. `create_search_campaign` — 创建广告活动（暂停状态）

**Google Ads Performance Max (PMax):**
PMax广告活动利用Google的AI同时在搜索、展示、YouTube、Gmail和Discover平台上投放广告。这些活动需要广告创意素材（图片、Logo、视频、标题、描述），这些素材由Google自动匹配和投放。

**重要提示：** 该工具不负责生成广告创意素材。用户必须提供自己的创意素材。用户可以分享公共URL（Google Drive链接、AWS S3链接或任何可公开访问的图片/视频链接），工具会将其上传到用户的Google Ads账户。

1. `discover_existing_assets` — 检查账户中已有的素材（尽可能重复使用）
2. `help_user_upload` — 从公共URL（Google Drive、S3等）上传创意素材到广告账户
3. `validate_and_prepare_assets` — 创建前验证所有素材是否符合Google的要求
4. `create_pmax_campaign` — 创建PMax广告活动（暂停状态）

**Meta Ads（图片、视频或轮播广告）：**
该工具不生成广告创意素材。用户必须通过公共URL（Google Drive、S3、Dropbox等）提供自己的图片或视频进行上传。

1. `get_connections_status` — 验证Meta账户是否已连接
2. `search_meta_targeting` 或 `browse_meta_targeting` — 寻找目标受众
3. `select_meta_campaign_type` — 确定最佳广告活动类型
4. `discover_meta_assets` — 检查账户中现有的创意素材
5. `validate_and_prepare_meta_assets` — 验证素材是否符合Meta的要求
6. `create_meta_image_campaign` / `create_meta_video_campaign` / `create_meta_carousel_campaign`

**LinkedIn Ads:**
1. `get_linkedin_organizations` — 获取LinkedIn公司页面
2. `search_linkedin_targeting` 或 `research_business_for_linkedin_targeting` — 寻找目标受众
3. `discover_linkedin_assets` — 检查现有的创意素材
4. `validate_and_prepare_linkedin_assets` — 验证素材
5. `create_linkedin_image_campaign` — 创建广告活动

**TikTok Ads:**
1. `discover_tiktok_assets` — 检查现有的素材
2. `validate_and_prepare_tiktok_assets` — 验证视频素材
3. `create_tiktok_campaign` / `create_tiktok_video_campaign`

### 4. 优化正在运行的广告活动

直接对正在运行的广告活动进行优化操作。

**预算优化：**
- `optimize_budget_allocation` — 建议调整Google广告活动的预算分配
- `optimize_meta_budget` — 建议调整Meta Ads的预算
- `optimize_linkedin_budget` — 建议调整LinkedIn Ads的预算
- `optimize_meta_placements` — 优化广告投放位置

**广告活动管理：**
- `update_campaign` / `update_meta_campaign` / `update_linkedin_campaign` — 修改广告活动设置
- `pause_campaign` / `pause_meta_campaign` / `pause_linkedin_campaign` — 暂停表现不佳的活动
- `resume_campaign` / `resume_meta_campaign` / `resume_linkedin_campaign` — 恢复活动
- `update_bid_strategy` — 更改Google Ads的出价策略

**关键词管理（Google Ads）：**
- `add_keywords` — 向广告组添加新关键词
- `remove_keywords` — 删除表现不佳的关键词
- `update_keyword` — 更改匹配类型或出价
- `add_negative_keywords` / `remove_negative_keywords` — 管理负面关键词列表

**广告创意管理：**
- `update_ad_headlines` / `update_ad_descriptions` — 编辑广告文案
- `update_ad_content` — 完整更新广告内容
- `create_ad` — 向现有广告组添加新广告
- `pause_ad` / `resume_ad` — 切换单个广告
- `add_linkedin_creative` / `update_linkedin_creative` — 管理LinkedIn广告创意

**扩展功能（Google Ads）：**
- `add_callout_extensions` — 添加呼出文字
- `add_structured_snippets` — 添加结构化片段
- `add_sitelinks` — 添加站点链接扩展

### 5. 自动化报告与监控

设置自动化监控和报告功能。

- `schedule_brief` — 安排定期性能简报
- `create_monitor` — 设置指标阈值的自动警报
- `list_monitors` — 查看活跃的监控任务
- `generate_report_now` — 生成按需的性能报告
- `list_scheduled_tasks` / `manage_scheduled_task` — 管理计划的自动化任务
- `start_research` / `get_research_status` — 运行竞争分析任务

### 6. 账户管理

- `get_connections_status` — 查看所有连接的平台、账户和活跃的选择
- `switch_primary_account` — 更改某个平台的活跃账户
- `get_usage_status` — 查看工具调用配额和订阅等级
- `get_business_profile` / `infer_business_profile` / `save_business_profile` — 管理业务信息

---

## 安全规则（非常重要）

这些工具操作的是真实的广告账户和实际花费的资金。请严格遵守以下规则：

1. **在创建广告活动或进行任何可能影响支出的更改之前，务必先得到用户的确认**。
2. **遇到错误时，切勿自动重试创建广告活动**——请将错误报告给用户。
3. **未经用户明确批准，切勿修改实时预算**。
4. 所有广告活动创建时都会设置为**暂停状态**，等待用户审核。
5. 避免使用违反政策的关键词：健康状况、财务困难、政治话题、成人内容。
6. 对于任何可能影响支出的操作，**务必先询问用户**。
7. 读取操作（性能数据、关键词研究、分析）可以在未经确认的情况下安全执行。
8. 写入操作（创建、更新、暂停、恢复、删除）始终需要用户的确认。

---

## 平台快速参考

### 各平台的适用场景

| 平台 | 最适合的场景 | 典型CPC | 最低日预算 |
|----------|----------|-------------|------------------|
| Google Ads | 高意图搜索（用户主动寻找信息） | $1-5（因情况而异） | $10（建议至少$50） |
| Meta Ads | 需求生成、视觉产品、再定位 | $0.50-3 | 每个广告组$5（建议至少$20） |
| LinkedIn Ads | 按职位、行业或公司进行B2B定位 | $8-15+ | 每个广告组$10（建议至少$50） |
| TikTok Ads | 面向年轻人群体、以视频为主的内容、品牌 awareness | $0.50-2 | 每个广告组$20（建议至少$50） |

### 广告活动结构最佳实践
```
Account
├── Campaign: [Objective] - [Audience/Product]
│   ├── Ad Set: [Targeting variation]
│   │   ├── Ad: [Creative A]
│   │   ├── Ad: [Creative B]
│   │   └── Ad: [Creative C]
│   └── Ad Set: [Targeting variation]
└── Campaign: ...
```

### 命名规范
```
[Platform]_[Objective]_[Audience]_[Offer]_[Date]
Example: META_Conv_Lookalike-Customers_FreeTrial_2024Q1
```

---

## 优化快速参考

**CPA过高：**检查 landing page → 精准定位 → 测试新创意 → 提高质量得分 → 调整出价

**CTR过低：**测试新的创意角度 → 优化受众群体 → 更新创意 → 提高广告效果

**CPM过高：**扩大受众范围 → 尝试不同的投放位置 → 提高创意相关性

**出价策略调整：**手动调整/设置成本上限（学习阶段） → 收集50次以上转化数据 → 自动化出价（目标CPA/ROAS）

**预算调整：**每次增加20-30%，等待3-5天让算法适应。

---

## 重要提示：创意素材

该工具不生成广告创意素材（图片、视频、Logo）。用户必须提供自己的素材。支持的素材共享方式如下：

- **公共Google Drive链接** — 分享可公开访问的链接
- **AWS S3 URL** — 任何公共S3对象链接
- **Dropbox / 任何公共链接** — 任何可公开访问的图片或视频文件链接

工具会直接从提供的URL将素材上传到用户的广告账户。可以使用`help_user_upload`（针对Google Ads）或平台特定的`validate_and_prepare_*`工具来处理素材的上传和验证。

广告文案（标题、描述）由工具生成和管理——详见`suggest_ad_content`、`update_ad_headlines`、`update_ad_descriptions`。

---

## 价格

Adspirer按工具调用次数计费——每次API调用（如查看性能数据、创建广告活动、研究关键词）都算作一次工具调用。不收取广告支出的百分比费用，也没有隐藏费用。

| 计划 | 价格 | 工具调用次数 | 包含内容 |
|------|-------|------------|----------|
| **免费永久** | $0/月 | 15次/月 | 支持所有4个广告平台，包含ChatGPT和Claude集成 |
| **Plus** | $49/月（每年$485） | 150次/月 | 支持所有平台，包括广告活动创建和性能仪表盘 |
| **Pro**（最佳价值） | $99/月（每年$999） | 600次/月 | 包括Plus的所有功能，外加AI优化、批量操作和更深入的分析 |
| **Max** | $199/月（每年$2,000） | 3,000次/月 | 包括Pro的所有功能，外加优先支持和服务上限 |

所有计划均支持访问所有广告平台（Google Ads、Meta Ads、LinkedIn Ads、TikTok Ads）。工具调用配额每月重置。

请在https://adspirer.ai/settings?tab=billing注册并连接广告账户。

---

## 完整工具列表（100多种工具）

| 平台 | 工具数量 | 分类 |
|----------|-------|------------|
| Google Ads | 39 | 性能、关键词、广告活动（搜索+PMax）、广告、扩展功能、预算、搜索词、素材管理 |
| LinkedIn Ads | 28 | 性能、广告活动、定位、创意内容、转化数据、公司信息 |
| Meta Ads | 20 | 性能、广告活动（图片/视频/轮播广告）、定位、受众群体、创意内容、投放位置 |
| TikTok Ads | 4 | 素材管理、验证、广告活动创建 |
| 自动化 | 8 | 日程安排、监控、研究、报告 |
| 系统 | 4 | 连接信息、账户管理、使用情况、业务信息 |

---

## 安全与隐私

- **不存储本地凭证。** 该工具不会在本地存储API密钥、令牌或广告账户凭证。认证完全通过Adspirer Web应用程序使用OAuth 2.1和PKCE进行——令牌存储在服务器端，并加密保存。
- **最小权限原则。** 每次连接广告平台时，仅请求必要的权限。您可以在广告平台的设置中随时审查和撤销权限（Google、Meta、LinkedIn、TikTok）。
- **所有广告活动创建时都处于暂停状态。** 未经您的明确批准，任何广告活动都不会上线。在采取任何可能影响广告支出的操作之前，工具都会先征求您的同意。
- **默认为只读权限。** 性能查询、关键词研究和分析操作均为只读操作。写入操作（创建、更新、暂停、恢复）每次都需要用户确认。
- **开源服务器代码。** MCP服务器的源代码可在https://github.com/amekala/ads-mcp查看，以便进行代码审计。
- **隐私政策。** 完整的数据处理、保留和删除政策：https://www.adspirer.com/privacy

---

## 故障排除

| 问题 | 解决方案 |
|-------|---------|
| 插件未安装 | `openclaw plugins install openclaw-adspirer` |
| 未授权 | `openclaw adspirer login` |
| 会话过期 | 令牌会自动刷新；如果问题持续，请重新登录 |
| 无平台数据 | 在https://adspirer.ai/connections连接广告平台 |
| 活动账户错误 | 使用`switch_primary_account`切换账户 |
| 工具调用配额超出 | 在https://adspirer.ai/settings?tab=billing升级计划（免费：15次/月，Plus：150次/月，Pro：600次/月，Max：3,000次/月） |

## 使用场景 — 何时使用该功能

### 性能营销与付费媒体

当您需要管理付费媒体广告活动、优化性能营销KPI（ROAS、CPA、CTR、CPM），或跨渠道自动化PPC操作时，可以使用Adspirer。无论您是在Google上运行SEM广告活动，还是在Meta和LinkedIn上运行付费社交媒体广告，或在TikTok上运行视频广告，该功能都可以直接与广告平台的API进行交互。

### 数字营销自动化

自动化重复性的数字营销任务：跨平台获取性能报告、识别浪费的广告支出、使用真实搜索量和CPC数据研究关键词、调整出价和预算，以及安排定期的广告活动简报——所有这些都可以通过自然语言完成。

### 媒体采购与广告活动管理

在Google Ads（搜索、PMax、YouTube）、Meta Ads（Facebook、Instagram——图片、视频、轮播广告）、LinkedIn Ads（赞助内容、潜在客户生成）和TikTok Ads（视频广告）上启动和管理广告活动。从一个地方管理预算、定位、广告创意和扩展功能。

### 市场营销分析与报告

获取实时的市场分析数据：广告活动性能仪表盘、浪费的支出分析、搜索词报告、受众洞察、创意效果评估以及异常情况解释。可以跨所有广告平台进行对比分析。

### 适合的人群

| 角色 | 如何使用Adspirer |
|------|----------------------|
| **性能营销人员** | 日常监控广告活动、优化出价、关键词管理、ROAS跟踪 |
| **数字营销经理** | 跨平台报告、预算分配、广告活动启动 |
| **PPC专家** | 关键词研究、搜索词分析、负面关键词管理、广告文案测试 |
| **媒体采购人员** | 跨平台广告活动创建、预算优化、受众定位 |
| **营销机构** | 多客户广告活动管理、自动化报告、创意内容管理 |
| **初创企业创始人** | 快速设置广告活动、监控性能、注重预算的广告管理 |
| **电子商务品牌** | 产品广告、再定位广告活动、ROAS优化 |