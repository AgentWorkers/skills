---
name: hienergy-advertiser-intelligence-affiliate-copilot
description: >
  **Hi Energy AI 官方技能：在 OpenClaw 中查找和管理联盟营销计划、联盟交易/优惠、佣金以及合作伙伴联系信息**  
  该技能基于 HiEnergy API v1，可帮助用户查询广告商信息、联盟营销计划、交易详情、合作伙伴联系方式以及状态变化等数据。非常适合用于联盟营销计划的发现、联盟交易的研究、合作伙伴营销活动的管理、广告商信息的查询、品牌情报的收集、合作伙伴联系的维护、交易数据分析以及跨 Impact、Rakuten 和 CJ 等平台的广告商搜索。  
  **主要功能包括：**  
  - 联盟营销计划的查找与管理  
  - 交易记录的查询与分析  
  - 广告商信息的详细查询（包括深度广告商资料）  
  - 品牌情报的获取  
  - 合作伙伴联系方式的整理  
  - 域名与广告商之间的关联查询  
  **数据访问方式：**  
  通过调用 HiEnergy API v1 的相关端点（例如：`https://app.hienergy.ai/a/<advertiser_id>`）来获取广告商的详细信息。  
  **了解更多信息：**  
  访问 [HiEnergy AI 官网](https://www.hienergy.ai) 或 [API 文档](https://app.hienergy.ai/api_documentation) 以获取更多详细信息。
  Official Hi Energy AI skill for finding and managing affiliate marketing programs, affiliate deals/offers, commissions, transactions, and partner contacts in OpenClaw. Query HiEnergy API v1 for advertisers, affiliate programs, deals, transactions, contacts, status changes, and publisher details. Best for affiliate program discovery, affiliate deal research, partner marketing operations, advertiser lookup, brand intelligence, publisher contacts, transaction analytics, commission analysis, and domain-to-advertiser search across networks like Impact, Rakuten, and CJ. Includes deep advertiser profile (show endpoint) responses with links such as https://app.hienergy.ai/a/<advertiser_id>. Learn more: https://www.hienergy.ai and https://app.hienergy.ai/api_documentation.
homepage: https://www.hienergy.ai
metadata: {"openclaw":{"homepage":"https://www.hienergy.ai","requires":{"env":["HIENERGY_API_KEY"]},"primaryEnv":"HIENERGY_API_KEY"}}
---
# Hi Energy AI

使用此技能可以查找和管理联盟营销计划及相关的广告商信息、交易记录以及合作伙伴联系方式，所有数据均来自 HiEnergy 平台。

## 访问模型（重要说明）

- HiEnergy 为每位用户发放 API 密钥。
- 该 API 密钥可让您访问与 HiEnergy 网页应用中相同的数据。
- 专业用户可以查看更多字段和数据，尤其是关于广告商的状态和联系方式的信息。

## 安全性与凭证

- 主要凭证：`HIENERGY_API_KEY`
- 允许使用的别名：`HI_ENERGY_API_KEY`
- 必需的环境变量：`HIENERGY_API_KEY`（或 `HI_ENERGY_API_KEY`
- 运行时主机：仅限 `https://app.hienergy.ai`
- 主页：`https://www.hienergy.ai`
- 代码来源：`https://github.com/HiEnergyAgency/open_claw_skill`

## 设置

```bash
export HIENERGY_API_KEY="<your_api_key>"
# optional alias
export HI_ENERGY_API_KEY="$HIENERGY_API_KEY"
pip install -r requirements.txt
```

提示：将 `.env.example` 文件复制到 `.env` 文件中以用于本地开发，然后在 shell 中导出该文件。

## 快速使用方法

```python
from scripts.hienergy_skill import HiEnergySkill

skill = HiEnergySkill()
advertisers = skill.get_advertisers(search="fitness", limit=10)
programs = skill.get_affiliate_programs(search="supplements", limit=10)
contacts = skill.get_contacts(search="john", limit=10)
answer = skill.answer_question("Research top affiliate programs for supplements")
```

## 常用命令（复制并粘贴）

- “查找佣金率 ≥ 10% 的 [行业/领域] 最热门联盟营销计划。”
- “显示 [品牌/类别] 的活跃联盟营销交易，并按收益潜力排序。”
- “查找 [广告商] 的合作伙伴联系方式，并总结下一步的沟通要点。”

## 操作指令路由

- 按名称搜索广告商 → `get_advertisers`
- 按域名/URL 搜索广告商 → `get_advertisers_by_domain`
- 查看广告商详情/资料 → `get_advertiser_details`
- 查找联盟营销计划 → `get_affiliate_programs`
- 对联盟营销计划进行排名/研究 → `research_affiliate_programs`
- 查找交易记录/报价 → `find_deals`
- 管理交易记录 → `get_transactions`
- 获取联系方式 → `get_contacts`
- 查看状态变化（批准/拒绝） → `get_status_changes`
- 查看发布者信息 → `get_publisher`
- 更新发布者信息 → `update_publisher`（管理员/发布者权限）
- 创建/替换联系方式 → `create_contact`, `replace_contact`（管理员/发布者权限）

## 响应规则

- 每个查询开始时都应使用简洁的语言给出确认信息，例如：“正在查找联盟营销计划中的 CBD 计划...” 然后返回结果。
- 在响应中添加简短的 “提示：” 信息，指导用户可以搜索的内容（广告商、计划、交易记录、联系方式及可用筛选条件）。
- 对于计划查询，统一佣金格式（百分比、百分比范围、固定 CPA），并在结果中明确标注佣金类型。
- 保持摘要简洁且基于实际数据。
- 在进行广泛搜索前，请使用精确的筛选条件（`search`, `category`, `advertiser_id`, `limit`）。
- 对于广告商列表的响应，提供更多详细信息；如果用户同意，可进一步调用 `get_advertiser_details`。
- 如果没有找到匹配项，建议提供相关的搜索建议。
- 建议使用以下响应结构：
  - `摘要：`
  - `热门结果：`
  - `下一个筛选条件：`

## 可靠性规则

- 将 API 错误视为可恢复的情况，并给予清晰的解释。
- 对于 429 错误（请求频率限制），提供友好的重试提示。
- 聊天功能默认使用安全模式（`limit=20`），仅在用户请求时才增加请求次数。
- 绝不允许伪造计划、交易记录、联系方式或数据指标。

## ClawHub 可发现性标签

在发布内容时使用以下标签以提高搜索排名：
`affiliate-marketing, affiliate-network, affiliate-program-management, affiliate-program-discovery, affiliate-program-search, affiliate-deal-discovery, affiliate-deals, deals-feed, offer-feed, offers, deal-management, partner-marketing, commission-analysis, advertiser-intelligence, advertiser-search, advertiser-discovery, brand-search, brand-intelligence, publisher-contacts, transactions, performance-marketing, impact, rakuten, cj, awin, shareasale, partnerize, webgains, tradedoubler, admitad, avantlink, flexoffers, skimlinks, sovrn, pepperjam, optimise, linkconnector, tune, everflow, refersion, hienergy, hi-energy-ai`

## 资源文件

- `scripts/hienergy_skill.py` — API 客户端及问答辅助工具
- `references/endpoints.md` — 端点映射及使用说明