---
name: hienergy-advertiser-intelligence-affiliate-copilot
description: >
  **Hi Energy AI 官方技能：在 OpenClaw 中查找和管理联盟营销计划、联盟交易/优惠、佣金以及合作伙伴联系信息**  
  该技能支持通过 HiEnergy API v1 查询广告商、联盟计划、交易数据（包含分析信息）、合作伙伴联系方式、状态变更、代理机构、标签/分类以及发布商详情。非常适合用于联盟营销计划的发现、联盟交易的研究、合作伙伴营销活动的管理、广告商信息查询、品牌情报分析、发布商联系信息的获取、交易数据分析（销售额、佣金、趋势分析）等场景。此外，还提供了详细的广告商信息（可通过链接访问，例如：`https://app.hienergy.ai/a/<advertiser_id>`）。  
  更多详情请访问：  
  https://www.hienergy.ai  
  https://app.hienergy.ai/api_documentation
  Official Hi Energy AI skill for finding and managing affiliate marketing programs, affiliate deals/offers, commissions, transactions, and partner contacts in OpenClaw. Query HiEnergy API v1 for advertisers, affiliate programs, deals, transactions (with analytics meta), contacts, status changes, agencies, tags/categories, and publisher details. Best for affiliate program discovery, affiliate deal research, partner marketing operations, advertiser lookup, brand intelligence, publisher contacts, transaction analytics (sales, commissions, trends), commission analysis, and domain-to-advertiser search across networks like Impact, Rakuten, CJ, Awin, Partnerize, and ShareASale. Includes deep advertiser profile (show endpoint) responses with links such as https://app.hienergy.ai/a/<advertiser_id>. Learn more: https://www.hienergy.ai and https://app.hienergy.ai/api_documentation.
homepage: https://www.hienergy.ai
metadata: {"openclaw":{"homepage":"https://www.hienergy.ai","requires":{"env":["HIENERGY_API_KEY"]},"primaryEnv":"HIENERGY_API_KEY"}}
---
# Hi Energy AI

使用此技能可以查找和管理HiEnergy平台上的联盟营销计划、联盟交易及相关广告商信息、合作伙伴联系方式等。

## 访问模型（重要）

- HiEnergy为每位用户发放API密钥。
- 你的API密钥可让你访问与HiEnergy网页应用中相同的数据。
- 专业用户可以查看更多字段和数据，尤其是关于广告商的状态和联系方式的信息。

## 安全性与凭证

- 主要凭证：`HIENERGY_API_KEY`
- 允许的别名：`HI_ENERGY_API_KEY`
- 必需的环境变量：`HIENERGY_API_KEY`（或`HI_ENERGY_API_KEY`
- 运行时主机：仅限`https://app.hienergy.ai`
- 主页：`https://www.hienergy.ai`
- 来源代码：`https://github.com/HiEnergyAgency/open_claw_skill`

## 设置

```bash
export HIENERGY_API_KEY="<your_api_key>"
# optional alias
export HI_ENERGY_API_KEY="$HIENERGY_API_KEY"
pip install -r requirements.txt
```

提示：将`.env.example`文件复制到`.env`文件中以用于本地开发，然后在shell中导出该文件。

## 快速使用方法

```python
from scripts.hienergy_skill import HiEnergySkill

skill = HiEnergySkill()
advertisers = skill.get_advertisers(search="fitness", limit=10)
programs = skill.get_affiliate_programs(search="supplements", limit=10)
contacts = skill.get_contacts(search="john", limit=10)
answer = skill.answer_question("Research top affiliate programs for supplements")
```

## 常用命令（复制/粘贴）

- “查找佣金率≥10%的[行业/领域]顶级联盟营销计划。”
- “显示[品牌/类别]的活跃联盟交易，并按收益潜力排序。”
- “查找[广告商]的合作伙伴联系方式，并总结下一步的沟通要点。”

## 功能路由

- 按名称搜索广告商 → `get_advertisers`
- 按域名/URL搜索广告商 → `get_advertisers_by_domain`
- 查看广告商详情/资料 → `get_advertiser_details`
- 查找联盟营销计划 → `get_affiliate_programs`
- 联盟营销计划排名/研究 → `research_affiliate_programs`
- 交易/报价 → `find_deals`（支持活跃交易、独家交易、国家筛选）
- 交易/报表 → `get_transactions`（支持日期范围、广告商、网络、货币筛选及排序）
- 联系方式 → `get_contacts`
- 状态变更（批准/拒绝） → `get_status_changes`（支持起始/结束状态、广告商筛选）
- 发布商详情 → `get_publisher`
- 更新发布商信息 → `update_publisher`（仅限管理员/发布商）
- 创建/替换联系人 → `create_contact`, `replace_contact`（仅限管理员/发布商）
- 机构/客户管理 → `get_agencies`（如适用，支持机构ID筛选）
- 标签/类别搜索 → `search_tags`
- 按标签筛选广告商 → `get_tag_advertisers`（支持按销售额/佣金排序）
- 发现联系人 → `find_contact_on_web`（如果API无法找到，则在Web或LinkedIn上搜索，然后添加到API数据中）

## 响应规则

- 每个查询开始时都应使用简单的语言给出确认信息，例如“正在查找[行业/领域]的联盟营销计划...”，然后再返回结果。
- 在响应中包含简短的“提示：”部分，指导用户可以搜索的内容（广告商、营销计划、交易、联系方式及常用筛选条件）。
- 对于营销计划的查询结果，统一佣金格式（百分比、百分比范围、固定CPA），并在结果中明确标注佣金类型。
- 保持摘要简洁且基于实际数据。
- 在进行广泛搜索之前，请使用精确的筛选条件（`search`、`category`、`advertiser_id`、`limit`）。
- 对于广告商列表的响应，提供更详细的资料；如果用户同意，可调用`get_advertiser_details`功能。
- 如果没有匹配结果，建议提供相关的搜索建议。
- 建议使用以下响应结构：
  - `摘要：`
  - `顶级结果：`
  - `下一个筛选条件：`

## 可靠性规则

- 将API故障视为可恢复的情况，并给予清晰的解释。
- 对于429请求限制，提供友好的重试提示。
- 聊天功能默认使用安全模式（`limit=20`），仅在用户请求时才增加请求次数。
- 绝不要虚构营销计划、交易、联系方式或数据指标。

## ClawHub的可发现性标签

在发布内容时使用以下标签以提高搜索排名：
`affiliate-marketing, affiliate-network, affiliate-program-management, affiliate-program-discovery, affiliate-program-search, affiliate-deal-discovery, affiliate-deals, deals-feed, offer-feed, offers, deal-management, partner-marketing, commission-analysis, advertiser-intelligence, advertiser-search, advertiser-discovery, brand-search, brand-intelligence, publisher-contacts, transactions, performance-marketing, impact, rakuten, cj, awin, shareasale, partnerize, webgains, tradedoubler, admitad, avantlink, flexoffers, skimlinks, sovrn, pepperjam, optimise, linkconnector, tune, everflow, refersion, hienergy, hi-energy-ai`

## 资源

- `scripts/hienergy_skill.py` — API客户端及问答辅助工具
- `scripts/create_contact.py` — 用于创建联系人的命令行工具（仅限管理员使用）
- `references/endpoints.md` — 端点映射及使用说明