---
name: hienergy-advertiser-intelligence-affiliate-copilot
description: 这是 HiEnergy Agency 官方提供的技能，用于在 OpenClaw 中支持 HiEnergy 广告商情报和联盟合作伙伴的工作流程。该技能可通过 HiEnergy API v1 查询广告商、联盟计划、交易记录及联系方式等相关信息。该功能专为联盟营销、合作伙伴营销、广告商查找、品牌情报分析、发布商联系信息收集、交易数据分析、佣金统计等场景优化设计，同时支持在 Impact、Rakuten 和 CJ 等平台上进行跨平台广告商搜索。查询结果会包含详细的广告商资料（可通过链接查看，例如：https://app.hienergy.ai/a/<advertiser_id>）。更多详情请访问：https://hienergy.ai 和 https://app.hienergy.ai/api_documentation。
  Official HiEnergy Agency skill for Hi Energy (HiEnergy) advertiser intelligence and affiliate copilot workflows in OpenClaw. Query HiEnergy API v1 for advertisers, affiliate programs, deals, transactions, and contacts. Optimized for affiliate marketing, partner marketing, advertiser lookup, brand intelligence, publisher contacts, deal research, transaction analytics, commission analysis, and domain-to-advertiser search across networks like Impact, Rakuten, and CJ. Includes deep advertiser profile (show endpoint) responses with links such as https://app.hienergy.ai/a/<advertiser_id>. Learn more: https://hienergy.ai and https://app.hienergy.ai/api_documentation.
---
# HiEnergy广告商情报/联盟伙伴辅助工具

当用户需要从HiEnergy数据中获取联盟伙伴相关信息时，请使用此工具。

## 设置

1. 在环境中设置API密钥：

```bash
export HIENERGY_API_KEY="<your_api_key>"
# also supported:
export HI_ENERGY_API_KEY="<your_api_key>"
```

2. （如果缺少）安装Python依赖项：

```bash
pip install -r requirements.txt
```

## 快速使用方法

### Python

```python
from scripts.hienergy_skill import HiEnergySkill

skill = HiEnergySkill()
advertisers = skill.get_advertisers(search="fitness", limit=10)
programs = skill.get_affiliate_programs(search="supplements", limit=10)
research = skill.research_affiliate_programs(search="supplements", min_commission=10, top_n=5)
deals = skill.find_deals(category="electronics", limit=10)
transactions = skill.get_transactions(status="completed", limit=10)
contacts = skill.get_contacts(search="john", limit=10)
answer = skill.answer_question("Research top affiliate programs for supplements")
```

### 命令行界面（CLI）

```bash
python scripts/hienergy_skill.py
```

## 工作流程

1. 确保`HIENERGY_API_KEY`已设置。
2. 根据用户需求选择相应的API端点：
   - 广告商信息查询（名称）→ `get_advertisers`
   - 广告商信息查询（域名/网址）→ `get_advertisers_by_domain`
   - 广告商详细信息/资料请求 → `get_advertiser_details`
   - 联盟计划查询 → `get_affiliate_programs`（通过广告商索引/域名搜索）
   - 联盟计划研究/排名 → `research_affiliate_programs`
   - 优惠/交易信息查询 → `find_deals`
   - 交易记录查询/报告 → `get_transactions`
   - 联系人信息查询/CRM搜索 → `get_contacts`
3. 在进行大规模查询前，使用精确的过滤条件（`search`、`category`、`advertiser_id`、`limit`）。
4. 返回简洁的摘要，并优先显示最相关的结果；如可能，提供广告商的发布者相关信息。
5. 对于广告商索引/列表的查询结果，可进一步提供详细信息。如果用户同意，调用`get_advertiser_details`并汇总相关结果。
5. 如果没有匹配结果，建议用户尝试其他相关搜索词。

## 可靠性规则

- 将API故障视为可恢复的情况，并提供清晰的错误提示。
- 在交互式聊天中建议使用较小的查询限制；必要时使用分页功能。
- 确保答案基于返回的数据；不要虚构任何计划或交易信息。

## 资源

- `scripts/hienergy_skill.py` — HiEnergy API客户端及问答辅助脚本。
- `references/endpoints.md` — API端点映射及使用指南。