---
name: Home Buying
slug: home-buying
version: 1.0.0
homepage: https://clawic.com/skills/home-buying
description: 购房时，应设置明确的预算限制，使用房屋列表评估工具（listing scorecards）来辅助决策，制定合理的购房策略（offer strategy），对潜在房源进行尽职调查（due diligence），并确保所有购房流程都符合要求（triage and closing readiness checks）。
changelog: Initial release with a full home-buying decision workflow from budget setup through closing readiness.
metadata: {"clawdbot":{"emoji":"HOME","requires":{"bins":[],"config":["~/home-buying/"]},"os":["linux","darwin","win32"],"configPaths":["~/home-buying/"]}}
---
## 设置（Setup）

如果 `~/home-buying/` 不存在或为空，请阅读 `setup.md`，了解其中将存储的内容，并在创建文件之前获取确认。

## 适用场景（When to Use）

当用户购买首套住房或投资性房产时，需要在整个预算、房源搜索、报价、房屋检查以及交易结算过程中做出有条理的决策时，可以使用此技能。该技能将基于情感的决策转化为一个可重复的决策系统，同时提供明确的规则和退出标准。

## 架构（Architecture）

所有与购房相关的信息都存储在 `~/home-buying/` 目录下。具体结构及状态字段的详细信息请参阅 `memory-template.md`。

```text
~/home-buying/
|-- memory.md             # Decision defaults, status, and recurring constraints
|-- active-deals.md       # Deal pipeline with stage and risk notes
|-- offer-log.md          # Offer ladder history and outcomes
`-- closing-checks.md     # Lender, title, insurance, and final walkthrough status
```

## 快速入门（Quick Start）

请按照以下步骤操作：
1. 定义购房的基本要求（如地理位置范围、卧室数量、通勤时间限制、房屋类型等）。
2. 使用统一的评分标准对房源进行评估。
3. 在提交报价之前，制定一个分层的报价策略。
4. 进行房屋检查并记录风险转移方案。
5. 根据准备情况完成交易结算流程。

## 快速参考（Quick Reference）

根据当前需要，选择相应的文件进行操作：
| 主题 | 文件          |
|-------|--------------|
| 设置与激活流程 | `setup.md`       |
| 记忆模板       | `memory-template.md`    |
| 预算计算与规则    | `budget-guardrails.md`   |
| 房源评分标准    | `listing-scorecard.md`   |
| 报价策略与让步     | `offer-ladder.md`    |
| 房屋检查与风险处理 | `due-diligence.md`    |
| 交易结算准备    | `closing-readiness.md`   |

## 核心规则（Core Rules）

### 1. 在浏览房源前先确定购房基本要求
- 在查看房源信息之前，先明确不可协商的要素（如地理位置、卧室数量、通勤时间、房屋类型等）。
- 制定明确的“不可接受”标准，并至少保持一周不变，以减少冲动性决策。

### 2. 计算总月成本，而非房源标价
- 计算包括本金、利息、税费、保险费、业主协会费用（HOA）、公用事业费用估算以及维护储备金在内的总月成本。
- 除非用户明确同意调整上限，否则拒绝超出月成本预算的房源。

### 3. 使用统一的评分标准
- 对所有候选房源应用相同的评分标准。
- 如果选中某房源，需将其标记为例外情况并记录原因。

### 4. 制定分层的报价策略
- 在联系卖家之前，先制定A计划、B计划以及相应的退出报价。
- 每个报价层级都应包括价格、应对风险的措施、可获得的优惠以及最大让步范围。

### 5. 将房屋检查视为风险转移过程
- 将检查中发现的问题分为三种处理方式：由卖家修复、卖家提供补偿或买家自行承担风险。
- 任何未解决的高风险问题都必须在得到明确同意前得到处理。

### 6. 严格把控时间表和融资确定性
- 保留一份包含贷款文件、评估节点、产权相关事项及保险文件的日期记录清单。
- 一旦发现关键路径上的延误，立即标记并提出具体的补救措施。

### 7. 为每笔交易记录决策过程
- 将报价内容、对方的反提案、被拒绝的选项以及交易后的总结记录下来。
- 重复使用这些经验，以改进未来的报价流程，避免重复犯错。

## 购房常见陷阱（Home-Buying Traps）
- 先购物后制定预算 → 过度投入和仓促妥协。
- 仅关注低利率信息而忽略总交易成本 → 误判购房负担能力。
- 在竞争激烈的市场中盲目放弃房屋检查 → 遭受不对称的风险。
- 仅关注价格进行谈判 → 导致错过可获得的优惠、维修费用或时间延误。
- 忽视社区层面的信息（如保险趋势、业主协会状况、建筑许可情况） → 隐藏未来的潜在成本。
- 将贷款或产权办理的延误视为“正常现象” → 导致交易失败。

## 数据存储（Data Storage）
- 活跃交易的相关信息（如评分表、决策记录）仅存储在 `~/home-buying/` 目录下。
- 仅存储必要的操作数据，避免泄露个人敏感信息。
- 在保存任何敏感的个人信息或财务数据之前，请先征得用户同意。

## 安全性与隐私（Security & Privacy）
- **数据传输**：
  - 默认情况下，不会将任何数据传输到外部系统。该技能仅提供工作流程指导及本地存储。

**数据存储位置**：
  - 决策背景信息、交易记录及清单状态数据存储在 `~/home-buying/` 目录下。

**注意事项**：
- 该技能不会自动提交报价。
- 不会自动调用贷款机构、房地产信息管理系统（MLS）、第三方托管平台或产权登记机构的API。
- 默认情况下，不会与外部服务共享用户数据。
- 不会修改 `~/home-buying/` 目录之外的文件。
- 绝不会修改自身的技能定义文件。

## 相关技能（Related Skills）
- 如果用户同意，可以使用以下命令安装相关技能：
  - `clawhub install real-estate-skill`：提供跨角色和阶段的全面房地产交易指导。
  - `property-valuation`：提供基于房产价值的评估服务。
  - `contract`：协助审核合同结构和条款。
  - `rental`：提供租赁相关的经济分析及房东/租客决策支持。
  - `house`：帮助用户管理购房后的房屋维护事务。

## 反馈与更新（Feedback）
- 如果觉得本技能有用，请给 `clawhub` 留下五星评价。
- 如需保持信息更新，请使用 `clawhub sync` 命令。