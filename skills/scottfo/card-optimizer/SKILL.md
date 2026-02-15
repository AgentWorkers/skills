---
name: card-optimizer
description: "信用卡奖励优化工具——通过为每个购物类别推荐最适合的信用卡，帮助用户最大化返现、积分和里程的收益。该工具会监控年度消费限额，计算年费的投入回报率（ROI），管理每季度轮换的购物类别，并根据用户的消费习惯建议更换新的信用卡。"
homepage: https://github.com/ScotTFO/card-optimizer-skill
metadata: {"clawdbot":{"emoji":"💳"}}
---

# 信用卡优化器

通过为每次购物选择最合适的信用卡，最大限度地提高信用卡奖励收益。

## 数据存储位置

- **技能逻辑文件：** `skills/card-optimizer/`
- **用户数据文件：** `data/card-optimizer/`
  - `cards.json` — 信用卡信息、奖励费率、消费估算、类别映射

## 信用卡数据库架构

`cards.json` 中的每张信用卡都遵循以下结构：

```json
{
  "id": "unique_id",
  "name": "Card Name",
  "issuer": "Issuer Name",
  "network": "visa|mastercard|amex|discover",
  "annual_fee": 95,
  "reward_type": "cashback|points|miles",
  "point_valuation_cpp": null,
  "transfer_partners": [],
  "notes": "Optional notes",
  "signup_bonus": {
    "amount": 200,
    "type": "cashback",
    "spend_requirement": 3000,
    "timeframe_months": 3,
    "earned": false
  },
  "categories": [
    {
      "category": "groceries",
      "rate": 6.0,
      "cap_amount": 6000,
      "cap_period": "yearly",
      "rate_after_cap": 1.0
    },
    {
      "category": "rotating",
      "rate": 5.0,
      "cap_amount": 1500,
      "cap_period": "quarterly",
      "rate_after_cap": 1.0,
      "quarterly_categories": {
        "Q1": ["gas", "ev_charging"],
        "Q2": ["groceries", "home_improvement"],
        "Q3": ["restaurants", "paypal"],
        "Q4": ["amazon", "target", "walmart"]
      },
      "activation_required": true
    },
    {
      "category": "everything_else",
      "rate": 1.0
    }
  ]
}
```

### 积分估值

对于积分/里程信用卡，存储 `point_valuation.cpp`（每点的价值，单位：美分）：
- Chase Ultimate Rewards：基础值为 1.0 美分；Sapphire Preferred 为 1.25 美分；Sapphire Reserve 为 1.5 美分
- Amex Membership Rewards：基础值为 1.0 美分；具体费率因转账合作伙伴而异
- 在比较信用卡时，将费率乘以 `point_valuation.cpp` 以获得等值的现金返还

### 类别映射

`cards.json` 中的 `category_map` 将每个消费类别映射到最适合的信用卡。这是预先计算出的最优分配结果——当信用卡添加或删除时需要重新计算。

### 消费估算

为了进行投资回报率（ROI）计算、差距分析和新信用卡推荐，用户可以在 `cards.json` 中选择性地设置每个类别的月消费估算：

```json
{
  "estimated_monthly_spending": {
    "groceries": 600,
    "gas": 200,
    "restaurants": 300,
    "amazon": 150,
    "streaming": 50,
    "everything_else": 500
  }
}
```

如果没有提供估算数据，该技能仍然可以针对每次购物推荐信用卡——但无法进行 ROI 或差距分析。请用户在首次设置时提供估算数据。

**注意：** 该技能不跟踪用户的单次消费记录。如果用户需要详细的消费数据，应通过预算工具连接银行账户。这些估算数据仅用于优化计算。

## 购物优化器

### 如何推荐信用卡

当用户询问“[类别] 应该使用哪种信用卡？”或“我要购买 [商品]”时：

1. **从购物信息中识别类别**（详见下面的“类别匹配”部分）
2. **检查所有适用于该类别的信用卡的奖励费率**
3. **考虑消费限额**：如果某张信用卡有消费限额，且用户在该类别的年消费额超过限额，请注明限额以及何时可能达到限额
4. **考虑网络受理情况**：如果最佳信用卡是 Amex，请说明某些商家不接受 Amex，并提供 Visa/MC 作为备用选项
5. **比较实际回报率**：对于积分信用卡，使用 `point_valuation.cpp` 将费率转换为等值的现金返还
6. **给出推荐理由**

### 建议格式

```
💳 Use: [Card Name] ([Issuer])
💰 Reward: [X]% [cashback/points/miles] on [category]
⚠️ Note: [any caps, network warnings, or caveats]
🔄 Fallback: [Next best card if merchant doesn't accept primary]
```

### 有消费限额的信用卡推荐

当某张信用卡有消费限额时：
- **远低于限额**：正常推荐该信用卡
- **可能达到限额**（根据估算的消费额）：说明何时会达到限额以及之后应更换为哪种信用卡
- **存在限额**：始终告知用户限额的存在

示例：“您的 Amex BCP 在每年 6,000 美元的食品杂货消费上可享受 6% 的返现。如果您每月消费约 600 美元，大约在 10 月就会达到限额。之后返现率会降至 1%——此时可以更换为 Wells Fargo Active Cash，返现率为 2%。”

## 季度类别管理

### 旋转类别

部分信用卡（如 Chase Freedom Flex、Discover It）的优惠类别每季度会发生变化，并需要用户手动激活。

### 季度提醒

每个季度开始时（1 月 1 日、4 月 1 日、7 月 1 日、10 月 1 日）：
- 检查哪些信用卡的 `activation_required` 属性为 `true`
- 如果信用卡尚未在当前季度激活，提醒用户
- 列出当前季度的优惠类别
- **提示：** 可以通过设置季度定时任务或将其纳入里程检查流程来实现自动化

存储每张信用卡的激活状态：
```json
{
  "quarterly_activations": {
    "chase_freedom_flex": {
      "2026-Q1": {"activated": true, "date": "2026-01-02"}
    }
  }
}
```

## 年费 ROI 分析

对于每张收取年费的信用卡，根据用户的 `estimated_monthly_spending`（月消费估算）来评估是否值得继续使用：

1. **计算奖励收益**：计算每个优惠类别的年奖励金额
2. **计算基准收益**：无年费的 2% 固定返现信用卡在同一消费额下的收益
3. **奖励价值**：`bonus_rewards` - `baseline_rewards`
4. **净 ROI**：`bonus_value` - `annual_fee`
5. **判断**：如果净 ROI 大于 0，则值得继续使用

### 报告格式

```
💳 [Card Name] — Annual Fee: $[fee]

Bonus rewards earned:     $[amount]
vs. 2% flat card:         $[amount]
Bonus value:              $[amount]
Annual fee:              -$[fee]
━━━━━━━━━━━━━━━━━━━━━━━━
Net value:                $[amount] ✅ Worth it / ❌ Consider downgrading

Break-even: Need $[X]/yr in bonus categories to justify the fee
```

## 优化与差距分析

### 消费差距分析

利用 `estimated_monthly_spending`，识别以下情况：
1. **薄弱消费类别**：用户在该类别的消费额很高，但当前使用的信用卡返现率仅为 1-2%
2. **表现不佳的年费信用卡**：年费过高，导致的奖励不足以覆盖年费
3. **可能达到消费限额的类别**：用户在该类别的年消费额超过信用卡的返现限额，可能需要额外添加一张信用卡
4. **缺乏覆盖的类别**：用户在该类别没有适用的信用卡

### 报告格式

```
📊 Card Optimization Report

✅ Well covered:
- Groceries → Amex BCP (6%) — earning ~$360/yr
- Amazon → Chase Prime (5%) — earning ~$90/yr

⚠️ Gaps identified:
- Dining: $300/mo at 2% (Chase Prime) — a 4% dining card would save $72/yr
- Travel: $200/mo at 1% — a 3x travel card would earn $48 more/yr

❌ Fee card alert:
- [Card] costs $95/yr but only generates $60 in bonus rewards — net loss of $35

💡 Recommendations:
- Adding [Card Name] would earn ~$[X] more per year on [categories]
- Consider downgrading [Card] to the no-fee version
```

### 新信用卡推荐

根据用户的消费估算，推荐能够带来额外收益的信用卡：

1. 确定用户消费最多的薄弱类别
2. 从这些类别中选择返现率较高的热门信用卡
3. 计算新信用卡的预计年奖励金额
4. 考虑年费因素
5. 提及注册奖励（作为第一年的优惠）

**请勿推荐具体的联盟链接**——只需提及信用卡名称并说明推荐理由。

**按类别推荐的热门信用卡：**

| 类别 | 信用卡 | 备注 |
|----------|-------|-------|
| 餐饮 | Chase Sapphire Preferred（3x）、Amex Gold（4x）、Capital One SavorOne（3%） | Sapphire 和 Gold 需支付年费 |
| 食品杂货 | Amex BCP（6%）、Amex Gold（4x MR） | BCP 有 6,000 美元的消费限额 |
| 旅行 | Chase Sapphire Reserve（3x）、Amex Platinum（5x 飞行里程）、Capital One Venture X（2x） | 所有这些信用卡都需支付年费 |
| 加油 | Citi Custom Cash（5%）、PenFed Platinum Rewards（5% 加油返现） | Citi Custom Cash 使用灵活 |
| 固定返现率信用卡 | Citi Double Cash（2%）、Wells Fargo Active Cash（2%）、Fidelity Visa（2%） | 无年费的备用选项 |
| 旋转优惠类别信用卡 | Chase Freedom Flex（每季度 5%）、Discover It（每季度 5% + 第一年额外返现） | 需要用户手动激活 |

## 类别匹配

### 商家 → 类别映射

当用户提到特定商家时，将其映射到正确的信用卡类别：

| 商家/关键词 | 类别 | 备注 |
|---|---|---|
| Kroger、Publix、Safeway、HEB、Aldi、Trader Joe’s | 食品杂货 | 超市 |
| Costco、Sam’s Club | 食品杂货或仓储商品 | Costco 在店内仅接受 Visa；在 Sam’s Club 可使用 Amex |
| Target、Walmart | 类别可能不同 | 根据发卡机构不同，可能被归类为“超级市场”或“食品杂货” |
| Amazon、amazon.com | Amazon | 部分信用卡有专门的 Amazon 类别 |
| Whole Foods | Whole Foods 或食品杂货 | Chase Prime 有专门的 Whole Foods 类别 |
| Shell、Exxon、BP、Chevron | 加油 | 加油站 |
| Uber、Lyft、Subway、Bus | 公共交通/打车服务 | 公共交通和打车服务 |
| Netflix、Hulu、Spotify、Disney+、HBO Max、YouTube TV | 流媒体服务 | 流媒体订阅服务 |
| Chipotle、McDonald’s、DoorDash、Grubhub | 餐厅/外卖服务 | 餐厅和外卖服务 |
| CVS、Walgreens、Rite Aid | 药房 | 药房 |
| Hilton、Marriott、Airbnb | 酒店/旅行 | 酒店和住宿 |
| United、Delta、Southwest | 航空公司 | 航班旅行 |

### 模糊类别匹配

当用户使用非正式表达时：
- “food” / “eating out” / “dinner” → **餐厅**
- “grocery run” / “supermarket” → **食品杂货**
- “gas” / “fuel” / “fill up” → **加油**
- “uber” / “lyft” / “ride” → **公共交通**
- “stuff on amazon” / “prime order” → **Amazon**
- “pharmacy” / “meds” / “prescription” → **药房**
- “subscription” / “monthly streaming” → **流媒体服务**
- “general” / “random purchase” → **其他所有类别**

如果表达模糊，可以询问：“这是食品杂货店还是餐厅？”

## 网络受理警告

### Amex 的受理情况

American Express 的商户受理范围低于 Visa/Mastercard：
- 小型/本地商家
- 部分国际商家
- Costco（在美国的门店仅接受 Visa）
- 部分政府支付场景

**在推荐 Amex 信用卡时，务必提供 Visa/MC 作为备用选项。**

### Costco 的特殊情况

Costco 的美国门店仅接受 **Visa** 信用卡（店内支付）：
- 在店内：必须使用 Visa
- 在线（costco.com）：接受 Visa、Mastercard、Discover（不接受 Amex）

## 添加新信用卡

当用户想要添加新信用卡时：

1. **收集信息**：
   - 信用卡名称和发卡机构
   - 支付网络（Visa/Mastercard/Amex/Discover）
   - 年费
   - 奖励类型（现金返还/积分/里程）及相应的积分估值（如适用）
   - 各类别的奖励费率
   - 是否有消费限额或限制
   - 信用卡是否有旋转优惠类别？哪些季度需要激活？
   - 注册奖励详情（可选）

2. **如果用户仅提供信用卡名称**，请通过网络搜索获取当前的奖励费率、年费和类别信息

3. 在 `cards.json` 中创建新的信用卡条目

4. **重新计算 `category_map`，确定新的最佳信用卡类别

5. **确认并显示更新后的推荐结果**

## 删除信用卡

1. 从 `cards.json` 中删除该信用卡条目
2. 重新计算 `category_map`
3. 确认并显示哪些类别的信用卡覆盖范围变弱

## 首次设置

如果 `data/card-optimizer/cards.json` 不存在：

1. 询问用户目前拥有的信用卡
2. 对于每张信用卡：
   - 通过网络搜索查询当前的奖励信息，或
   - 如果是特殊或地区性的信用卡，询问用户具体的费率信息
3. 使用这些信息创建 `cards.json` 文件，包含所有信用卡及预先计算好的类别映射
4. 询问用户每个主要类别（食品杂货、加油、餐饮、Amazon 等）的月消费估算——解释这些数据用于 ROI 和差距分析（但为可选信息）
5. 生成初始优化报告，显示用户每个类别的最佳信用卡及存在的差距

## 快速参考

| 用户输入 | 操作建议 |
|---|---|
| “购买食品杂货应该用哪种信用卡？” | 推荐该类别的最佳信用卡 |
| “我要加油” | 推荐适合加油的信用卡 |
| “Amazon 适合用哪种信用卡？” | 推荐适合 Amazon 消费的信用卡 |
| “年费是否值得？” | 对所有年费信用卡进行 ROI 分析 |
| “添加新信用卡” | 指导用户如何添加新信用卡 |
| “删除信用卡” | 删除信用卡并重新计算推荐结果 |
| “信用卡优化报告” | 提供全面的差距分析和推荐建议 |
| “我应该购买哪些信用卡？” | 提供新的信用卡推荐 |
| “激活第二季度的优惠类别” | 更新信用卡的激活状态 |
| “Costco 接受 Amex 吗？” | 提供信用卡的受理情况 |
| “我有哪些信用卡？” | 列出所有信用卡及其费率信息 |
| “更新我的消费估算” | 修订用户的月消费估算数据 |