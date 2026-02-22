---
name: hienergy-advertiser-intelligence-affiliate-copilot
description: 官方的 Hi Energy AI 技能，用于在 OpenClaw 中查找和管理联盟营销计划、联盟交易/优惠、佣金以及合作伙伴联系信息。该技能可通过 HiEnergy API v1 查询广告商、联盟计划、交易和联系信息。非常适合用于联盟营销计划的发现、联盟交易研究、合作伙伴营销运营、广告商信息查询、品牌情报分析、发布商联系管理、交易数据分析以及跨 Impact、Rakuten 和 CJ 等平台的广告商搜索。查询结果会包含详细的广告商资料（可通过以下链接查看：https://app.hienergy.ai/a/<advertiser_id>）。更多信息请访问：https://www.hienergy.ai 和 https://app.hienergy.ai/api_documentation。
  Official Hi Energy AI skill for finding and managing affiliate marketing programs, affiliate deals/offers, commissions, transactions, and partner contacts in OpenClaw. Query HiEnergy API v1 for advertisers, affiliate programs, deals, transactions, and contacts. Best for affiliate program discovery, affiliate deal research, partner marketing operations, advertiser lookup, brand intelligence, publisher contacts, transaction analytics, commission analysis, and domain-to-advertiser search across networks like Impact, Rakuten, and CJ. Includes deep advertiser profile (show endpoint) responses with links such as https://app.hienergy.ai/a/<advertiser_id>. Learn more: https://www.hienergy.ai and https://app.hienergy.ai/api_documentation.
homepage: https://www.hienergy.ai
metadata: {"openclaw":{"homepage":"https://www.hienergy.ai","requires":{"env":["HIENERGY_API_KEY"]},"primaryEnv":"HIENERGY_API_KEY"}}
---
# Hi Energy AI

使用此技能可以查找和管理联盟营销计划及相关的广告商、交易和合作伙伴联系方式，所有数据均来自 HiEnergy。

## 访问模型（重要）

- HiEnergy 为每位用户发放 API 密钥。
- 您的 API 密钥可让您访问与 HiEnergy 网页应用中相同的数据。
- 专业用户可以查看更多字段/数据，尤其是关于广告商状态和联系方式的信息。

## 安全性与凭证

- 主要凭证：`HIENERGY_API_KEY`
- 允许的别名：`HI_ENERGY_API_KEY`
- 必需的环境变量：`HIENERGY_API_KEY`（或 `HI_ENERGY_API_KEY`
- 运行时主机：仅限 `https://app.hienergy.ai`
- 主页：`https://www.hienergy.ai`
- 来源：`https://github.com/HiEnergyAgency/open_claw_skill`

## 设置

```bash
export HIENERGY_API_KEY="<your_api_key>"
# optional alias
export HI_ENERGY_API_KEY="$HIENERGY_API_KEY"
pip install -r requirements.txt
```

提示：将 `.env.example` 复制到 `.env` 文件以用于本地开发，然后在 shell 中导入该文件。

## 快速使用方法

```python
from scripts.hienergy_skill import HiEnergySkill

skill = HiEnergySkill()
advertisers = skill.get_advertisers(search="fitness", limit=10)
programs = skill.get_affiliate_programs(search="supplements", limit=10)
contacts = skill.get_contacts(search="john", limit=10)
answer = skill.answer_question("Research top affiliate programs for supplements")
```

## 命令示例（复制/粘贴）

- “查找佣金率 ≥ 10% 的 [行业/领域] 顶级联盟营销计划。”
- “显示 [品牌/类别] 的活跃联盟营销交易，并按收益潜力排序。”
- “查找 [广告商] 的合作伙伴联系方式，并总结下一步的沟通要点。”

## 操作路径

- 按名称搜索广告商 → `get_advertisers`
- 按域名/URL 搜索广告商 → `get_advertisers_by_domain`
- 查看广告商详情/资料 → `get_advertiser_details`
- 查找联盟营销计划 → `get_affiliate_programs`
- 对联盟营销计划进行排名/研究 → `research_affiliate_programs`
- 查找交易/优惠信息 → `find_deals`
- 查看交易记录/生成报告 → `get_transactions`
- 查看联系方式 → `get_contacts`

## 响应规则

- 每个查询开始时都应使用简洁的语言给出确认信息，例如：“正在查找联盟营销计划中的 CBD 计划...” 然后返回结果。
- 在响应中添加简短的 “提示：” 信息，指导用户可以搜索的内容（广告商、计划、交易、联系方式及可用筛选条件）。
- 对于计划的研究，统一佣金格式（百分比、百分比范围、固定 CPA），并在结果中明确标注佣金类型。
- 保持摘要简洁且基于实际数据。
- 在进行广泛搜索前使用精确的筛选条件（`search`、`category`、`advertiser_id`、`limit`）。
- 对于广告商列表的响应，提供更多详细信息；如果用户同意，可调用 `get_advertiser_details`。
- 如果没有匹配结果，建议提供相关的搜索关键词。
- 建议使用以下响应结构：
  - `摘要：`
  - `顶级结果：`
  - `下一个筛选条件：`

## 可靠性规则

- 将 API 错误视为可恢复的情况，并给予清晰的解释。
- 对于 429 错误（请求速率限制），提供友好的重试提示。
- 聊天功能默认使用安全模式（`limit=20`），仅在用户请求时才增加请求次数。
- 绝不虚构任何计划、交易、联系方式或指标数据。

## ClawHub 可发现性标签

在发布内容时使用以下标签以提高搜索排名：
`affiliate-marketing, affiliate-network, affiliate-program-management, affiliate-program-discovery, affiliate-program-search, affiliate-deal-discovery, affiliate-deals, deals-feed, offer-feed, offers, deal-management, partner-marketing, commission-analysis, advertiser-intelligence, advertiser-search, advertiser-discovery, brand-search, brand-intelligence, publisher-contacts, transactions, performance-marketing, impact, rakuten, cj, awin, shareasale, partnerize, webgains, tradedoubler, admitad, avantlink, flexoffers, skimlinks, sovrn, pepperjam, optimise, linkconnector, tune, everflow, refersion, hienergy, hi-energy-ai`

## 资源

- `scripts/hienergy_skill.py` — API 客户端及问答辅助工具
- `references/endpoints.md` — 端点映射及使用说明