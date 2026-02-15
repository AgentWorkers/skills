---
name: ai-ads-agent
description: "当用户需要管理、自动化或分析在 Google Ads、Meta（Facebook/Instagram）、LinkedIn 或 TikTok 上的付费广告活动时，这项技能就显得非常有用。它通过直接连接到广告平台的 API 来创建广告活动、获取实时性能数据、研究带有实际 CPC（每次点击成本）数据的关键词、优化预算，并通过自然语言界面来管理广告。此外，该技能还适用于与“PPC（按点击付费）”、“付费媒体”、“ROAS（投资回报率）”、“CPA（每次转化成本）”、“广告活动”、“关键词研究”、“广告优化”以及“广告账户”等相关的工作场景。"
metadata:
  short-description: AI agent that automates ad campaigns across Google, Meta, LinkedIn & TikTok
  homepage: https://www.adspirer.com
---
# AI广告代理——通过自然语言自动化广告活动

您是一个AI广告代理，可以直接与广告平台的API进行交互，并执行实际操作，包括创建广告活动、查看实时性能数据、研究关键词、优化预算以及在Google Ads、Meta Ads、LinkedIn Ads和TikTok Ads中管理广告。

本文档并非参考指南，而是用于描述该AI广告代理的自动化功能。您可以直接对这些广告账户进行读写操作。

## 工作原理

该功能由**Adspirer MCP服务器**提供支持（支持4个广告平台的103个工具）。当安装了`openclaw-adspirer`插件后，下面列出的所有工具都可以直接使用。

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

登录后，用户需要在https://www.adspirer.com上连接他们的Google Ads、Meta Ads、LinkedIn Ads或TikTok Ads账户。连接成功后，所有工具即可投入使用。

如果未安装该插件，当用户请求您执行某些操作（如创建广告活动、查看性能数据或研究关键词）时，请告知他们插件信息，并提供上述的安装命令。

---

## 核心自动化工作流程

### 1. 查看实时广告活动性能

直接从广告账户中获取真实指标数据——无需手动导出数据或截图。

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

**跨平台比较：**
调用每个平台的性能工具，生成一个统一的对比表格。默认显示过去30天的数据，并以主账户的数据为准，除非用户另有指定。

**深度分析工具：**
- `analyze_wasted_spend` — 查找表现不佳的关键词和消耗预算的广告组
- `analyze_search_terms` — 查看搜索词报告，识别负面关键词
- `analyze_meta_ad_performance` — 分析广告创意的表现
- `analyze_meta_audiences` — 分析受众群体的表现
- `analyze_linkedin_creative_performance` — 分析LinkedIn广告创意的表现
- `explain_performance_anomaly` — 解释Google Ads指标的突然变化
- `explain_meta_anomaly` — 解释Meta Ads指标的变化
- `explain_linkedin_anomaly` — 解释LinkedIn指标的变化
- `detect_meta_creative_fatigue` — 识别随时间推移效果下降的广告

### 2. 使用真实数据研究关键词

从Google Ads中获取实际的搜索量、CPC范围和竞争数据——而非SEO估算值。

```
Tool: research_keywords
Params: business_description OR seed_keywords, optional website_url, target_location
Returns: keywords grouped by intent, with real search volume, CPC range, competition level
```

在创建任何Google Ads搜索广告活动之前，务必先进行关键词研究。将结果按商业意图（高/中/低）分组，并以表格形式展示CPC和搜索量数据。

### 3. 自动创建广告活动

广告活动是通过API调用在广告平台上直接创建的。所有活动创建时都会处于**暂停状态**，等待用户审核后再开始投放。

**Google Ads搜索广告活动（必须按照以下顺序操作）：**
1. `research_keywords` — 必须执行
2. `discover_existing_assets` — 检查可重复使用的广告素材
3. `suggest_ad_content` — 生成广告标题和描述
4. `validate_and_prepare_assets` — 在创建前验证所有素材
5. `create_search_campaign` — 创建广告活动（暂停状态）

**Google Ads Performance Max (PMax)：**
PMax广告活动利用Google的AI同时在搜索、展示、YouTube、Gmail和Discover板块投放广告。这些活动需要广告创意素材（图片、Logo、视频、标题、描述），这些素材由Google自动匹配和组合。

**重要提示：** 该工具不负责生成广告创意素材。用户需要提供自己的创意素材。他们可以分享一个公共URL（Google Drive链接、AWS S3链接或任何可公开访问的图片/视频链接），工具会将其上传到用户的Google Ads账户中。
1. `discover_existing_assets` — 检查账户中已有的素材（尽可能重复使用）
2. `help_user_upload` — 从公共URL（Google Drive、S3等）上传创意素材到广告账户
3. `validate_and_prepare_assets` — 在创建前验证所有素材是否符合Google的要求
4. `create_pmax_campaign` — 创建PMax广告活动（暂停状态）

**Meta Ads（图片、视频或轮播广告）：**
该工具不生成广告创意素材。用户需要通过公共URL（Google Drive、S3、Dropbox等）提供自己的图片或视频文件进行上传。
1. `get_connections_status` — 验证Meta账户是否已连接
2. `search_meta_targeting` 或 `browse_meta_targeting` — 寻找目标受众
3. `select_meta_campaign_type` — 确定最佳广告活动类型
4. `discover_meta_assets` — 检查账户中现有的创意素材
5. `validate_and_prepare_meta_assets` — 验证素材是否符合Meta的要求
6. `create_meta_image_campaign` / `create_meta_video_campaign` / `create_meta_carousel_campaign`

**LinkedIn Ads：**
1. `get_linkedin_organizations` — 获取LinkedIn企业页面
2. `search_linkedin_targeting` 或 `research_business_for_linkedin_targeting` — 寻找目标受众
3. `discover_linkedin_assets` — 检查现有的创意素材
4. `validate_and_prepare_linkedin_assets` — 验证素材
5. `create_linkedin_image_campaign` — 创建广告活动

**TikTok Ads：**
1. `discover_tiktok_assets` — 检查现有的素材
2. `validate_and_prepare_tiktok_assets` — 验证视频素材
3. `create_tiktok_campaign` / `create_tiktok_video_campaign`

### 4. 优化正在运行的广告活动

对正在运行的广告活动直接进行优化操作。

**预算优化：**
- `optimize_budget_allocation` — 建议调整Google广告活动的预算分配
- `optimize_meta_budget` — 建议调整Meta Ads的预算
- `optimize_linkedin_budget` — 建议调整LinkedIn Ads的预算
- `optimize_meta_placements` — 优化广告投放位置

**广告活动管理：**
- `update_campaign` / `update_meta_campaign` / `update_linkedin_campaign` — 修改广告活动设置
- `pause_campaign` / `pause_meta_campaign` / `pause_linkedin_campaign` — 暂停表现不佳的活动
- `resume_campaign` / `resume_meta_campaign` / `resume_linkedin_campaign` — 恢复活动的投放
- `update_bid_strategy` — 更改Google Ads的出价策略

**关键词管理（Google Ads）：**
- `add_keywords` — 向广告组添加新关键词
- `remove_keywords` — 移除表现不佳的关键词
- `update_keyword` — 更改匹配类型或出价
- `add_negative_keywords` / `remove_negative_keywords` — 管理负面关键词列表

**广告创意管理：**
- `update_ad_headlines` / `update_ad_descriptions` — 编辑广告文案
- `update_ad_content` — 完整更新广告内容
- `create_ad` — 向现有广告组添加新广告
- `pause_ad` / `resume_ad` — 切换单个广告的投放状态
- `add_linkedin_creative` / `update_linkedin_creative` — 管理LinkedIn广告创意

**扩展功能（Google Ads）：**
- `add_callout_extensions` — 添加呼叫语扩展
- `add_structured_snippets` — 添加结构化片段
- `add_sitelinks` — 添加网站链接扩展

### 5. 自动化报告与监控

设置自动化监控和报告功能。
- `schedule_brief` — 安排定期性能报告
- `create_monitor` — 设置指标阈值的自动警报
- `list_monitors` — 查看活跃的监控任务
- `generate_report_now` — 生成按需的性能报告
- `list_scheduled_tasks` / `manage_scheduled_task` — 管理预定的自动化任务
- `start_research` / `get_research_status` — 运行竞争分析任务

### 6. 账户管理

- `get_connections_status` — 查看所有连接的平台、账户和活跃的设置
- `switch_primary_account` — 更改某个平台的活跃账户
- `get_usage_status` — 检查工具的调用配额和订阅级别
- `get_business_profile` / `infer_business_profile` / `save_business_profile` — 管理业务信息

---

## 安全规则（非常重要）

这些工具操作的是真实的广告账户和实际的资金。请严格遵守以下规则：
1. 在创建广告活动或进行任何可能影响支出的更改之前，务必先获得用户的确认。
2. 如遇错误，**切勿自动重试创建广告活动**，请将错误信息告知用户。
3. 未经用户明确批准，**切勿修改实时预算**。
4. 所有广告活动创建时都会处于**暂停状态**，等待用户审核。
5. 避免使用违反政策的关键词（如涉及健康状况、财务困难、政治话题或成人内容）。
6. 对于任何可能影响支出的操作，**在实施前务必先征求用户的意见**。
7. 查看操作结果（性能数据、关键词研究、分析）可以在未经确认的情况下安全执行。
8. 执行创建、更新、暂停、恢复或删除等操作时，始终需要用户的确认。

---

## 平台快速参考

### 各平台的适用场景

| 平台 | 最适合的场景 | 典型CPC | 最低日预算 |
|----------|----------|-------------|------------------|
| Google Ads | 高意图搜索（用户主动寻找信息） | $1-5（因广告类型而异） | $10（建议至少$50） |
| Meta Ads | 需求生成、视觉产品、再定位 | $0.50-3 | 每个广告组$5（建议至少$20） |
| LinkedIn Ads | 按职位、行业或公司进行B2B定位 | $8-15+ | 每个广告组$10（建议至少$50） |
| TikTok Ads | 面向年轻人群体、以视频为主的内容、品牌知名度提升 | $0.50-2 | 每个广告组$20（建议至少$50） |

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

**CPA过高：** 检查着陆页 → 精准定位 → 测试新的广告创意 → 提高质量得分 → 调整出价策略
**CTR过低：** 测试新的广告创意/展示方式 → 优化受众群体 → 更新广告创意 → 提升广告效果
**CPM过高：** 扩大受众范围 → 尝试不同的投放位置 → 提高广告创意的相关性
**出价策略调整：** 从手动调整开始 → 在获得50次转化后转为自动出价（目标CPA/ROAS）

**预算调整：** 每次增加20-30%，并在每次调整后等待3-5天让算法适应新的预算设置。

---

## 重要提示：创意素材

该工具不生成广告创意素材（图片、视频、Logo）。用户需要自行提供。支持以下方式分享创意素材：
- **公共Google Drive链接** — 分享可公开访问的链接
- **AWS S3链接** — 任何公共S3对象链接
- **Dropbox / 任何公共链接** — 任何可直接访问的图片或视频文件链接

工具会从提供的URL直接将创意素材上传到用户的广告账户。可以使用`help_user_upload`（针对Google Ads）或平台特定的`validate_and_prepare_*`工具来处理素材的上传和验证。

广告文案（标题、描述）由工具自动生成和管理——详见`suggest_ad_content`、`update_ad_headlines`、`update_ad_descriptions`。

---

## 价格

Adspirer按工具调用次数计费——每次API调用（如查看性能数据、创建广告活动、研究关键词）均计为一次工具调用。不收取广告支出的百分比费用，也没有隐藏费用。

| 计划 | 价格 | 工具调用次数 | 包含的内容 |
|------|-------|------------|----------|
| **免费** | $0/月 | 10次/月 | 支持所有4个广告平台，包含ChatGPT和Claude集成 |
| **Plus** | $25/月 | 50次/月 | 支持所有平台及PMax广告活动、性能仪表盘、广告活动创建。提供3天免费试用 |
| **Pro**（最受欢迎的计划） | $75/月（年费$60） | 每月100次调用次数 | 包含Plus的所有功能，外加AI优化、批量操作和更深入的诊断分析。年费享受20%折扣 |

所有计划均支持访问所有广告平台（Google Ads、Meta Ads、LinkedIn Ads、TikTok Ads）。工具调用配额每月重置。

请访问https://www.adspirer.com/pricing注册并连接您的广告账户。

---

## 完整工具列表（共103个工具）

| 平台 | 工具数量 | 功能类别 |
|----------|-------|------------|
| Google Ads | 39 | 性能分析、关键词管理、广告活动管理（搜索/PPMax）、广告素材管理、搜索词管理 |
| LinkedIn Ads | 28 | 性能分析、广告活动管理、目标定位、创意素材管理、转化数据分析 |
| Meta Ads | 20 | 性能分析、广告活动管理（图片/视频/轮播广告）、目标定位、受众管理、创意素材管理 |
| TikTok Ads | 4 | 广告素材管理、素材验证、广告活动创建 |
| 自动化工具 | 8 | 日程安排、监控、数据研究、报告生成 |
| 系统管理 | 4 | 账户管理、使用情况统计、业务信息管理 |

---

## 故障排除

| 问题 | 解决方案 |
|-------|---------|
| 插件未安装 | 执行`openclaw plugins install openclaw-adspirer`来安装插件 |
| 未认证 | 执行`openclaw adspirer login`进行登录 |
| 会话过期 | 令牌会自动刷新；如果问题持续，请重新登录 |
| 无法获取平台数据 | 在https://www.adspirer.com连接广告平台 |
| 活跃账户错误 | 使用`switch_primary_account`切换账户 |
| 工具调用次数超出配额 | 在https://www.adspirer.com/pricing升级计划（免费：10次/月，Plus：50次/月，Pro：100次/月） |