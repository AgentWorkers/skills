---
name: Price
slug: price
version: 1.0.0
description: 作为消费者或企业采购人员，您可以跟踪商品价格、识别促销活动及价格操纵行为、记录购买时间，并据此做出明智的购买决策。
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## 使用场景

用户可能会提出以下问题：“这个价格合理吗？”，“我现在应该购买还是等待？”，“关注这个价格的变化”，“查看价格历史”，“这次促销是真的吗？”，“是否存在隐藏费用？”，“比较不同平台的价格”，“设置价格提醒”，“了解‘缩水通胀’（shrinkflation）现象”，“确定产品的公平市场价值”。

**不适用的场景**：作为卖家设置价格（请使用 `pricing` 文档），一般的购买流程（请使用 `buy` 文档），谈判策略（请使用相关谈判策略文档）。

## 快速参考

| 分类 | 对应文档 |
|------|------|
| 零售与电子产品 | `retail.md` |
| 旅行与酒店服务 | `travel.md` |
| B2B 与企业服务 | `b2b.md` |
| 收藏品与投资 | `collectibles.md` |
| 检测价格操纵行为 | `manipulation.md` |
| 设置价格跟踪功能 | `tracking.md` |

## 工作区结构

所有数据都存储在 `~/price/` 目录下：

```
~/price/
├── config.md           # Preferred retailers, alert thresholds
├── watchlist.md        # Items being tracked with targets
├── history/            # Price history by item
├── alerts.md           # Active price alerts
└── purchases.md        # Past decisions for learning
```

## 核心操作

**评估价格**：
- 当前价格 + 商品信息 → 查看历史价格范围 → 与 90 天内的最低价格进行比较 → 考虑总成本 → 根据置信度得出判断。

**设置价格提醒**：
- 商品信息 + 目标价格 → 添加到关注列表 → 监控多个销售平台的价格变化 → 价格达到目标时发送通知。

**跟踪商品价格**：
- 商品的 URL 或名称 → 定期查询价格 → 记录价格变化情况 → 发现价格波动时及时通知。

**决定购买时机**：
- 商品所属类别 + 时间范围 → 分析季节性价格走势 → 建议购买或等待购买 → 阐明推荐购买的理由。

## 价格评估框架

对于每一次价格评估，都需要考虑以下因素：
1. **历史价格背景**：当前价格与 90 天内的最低价格、历史最低价格以及正常价格范围的对比。
2. **总成本**：包括运费、税费、附加费用和保修费用等。
3. **时间因素**：考虑季节性价格波动、即将到来的促销活动或特殊事件可能导致的价格波动。
4. **价格操纵检测**：识别是否存在价格被人为抬高的情况（如虚假的促销信息或动态定价策略）。

## 输出格式

```
## Price Assessment: [Item]

**Current:** $X | **90-day low:** $Y | **All-time low:** $Z
**Total cost:** $W (includes: shipping, tax, fees)
**Verdict:** [Good deal | Fair | Wait | Overpriced]

**Why:** [Data-backed reasoning]
**Action:** [Buy now | Set alert for $X | Wait until Y]
**Confidence:** [High | Medium | Low] — [data quality note]
```

## 重要规则（必须遵守）

- **明确数据来源**：在引用价格历史数据时，务必注明数据来源。
- **包含总成本**：标明的价格并非最终价格，务必加上所有相关费用。
- **说明置信度**：诚实地说明数据的质量和局限性。
- **解释购买时机**：如果建议购买，需说明选择当前时机的理由。
- **警惕价格操纵**：始终检查是否存在虚假的促销信息或动态定价行为。

## 首次使用时的操作步骤：
1. 询问用户经常购买的商品类别。
2. 设置喜欢的销售平台列表。
3. 配置价格提醒的通知偏好。
4. 向用户解释可用的价格历史数据来源。
5. 将用户感兴趣的商品添加到关注列表中。