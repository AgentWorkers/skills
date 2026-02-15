---
name: Wishlist
description: 构建一个个人愿望清单系统，用于记录需求、跟踪商品价格，并辅助做出明智的购买决策。
metadata: {"clawdbot":{"emoji":"⭐","os":["linux","darwin","win32"]}}
---

## 核心功能
- 用户分享他们想要购买的商品，并提供详细信息。
- 系统会根据商品优先级和价格将推荐商品展示给用户。
- 定期检查已跟踪商品的价格变化。
- 创建 `~/wishlist/` 文件夹作为用户购物清单的工作区。

## 文件结构
```
~/wishlist/
├── items/
│   └── sony-headphones.md
├── by-priority/
│   ├── must-have.md
│   ├── want.md
│   └── someday.md
├── by-category/
│   ├── tech.md
│   ├── home.md
│   └── clothing.md
├── purchased.md
├── price-alerts.md
└── settings.md
```

## 商品信息记录
```markdown
# sony-headphones.md
## Item
Sony WH-1000XM5 Headphones

## Why I Want It
Best noise cancelling, work from cafes

## Priority
Must-have

## Category
Tech

## Price Tracking
- Target price: $300
- Current best: $349 (Amazon)
- Last checked: Feb 11, 2024

## Links
- Amazon: [url]
- Best Buy: [url]

## Price History
- Feb 1: $379
- Feb 10: $349 (dropped!)

## Notes
Wait for Prime Day or Black Friday
Consider refurbished

## Added
January 15, 2024
```

## 快速记录功能
为了方便快速保存商品信息：
```markdown
User: "I want those Sony headphones"
→ Create item with name
→ Ask: priority? budget? link?
→ Start tracking
```

## 优先级设置
```markdown
# by-priority/must-have.md
Items you're actively planning to buy:
- Sony WH-1000XM5 — waiting for <$300
- Standing desk — researching options

# by-priority/want.md
Would buy if good deal:
- Kindle Paperwhite
- AirTag 4-pack

# by-priority/someday.md
Nice to have, no rush:
- Espresso machine
- Drone
```

## 价格提醒功能
```markdown
# price-alerts.md
## Active Alerts
- Sony WH-1000XM5: alert if <$300
- Kindle Paperwhite: alert if <$100
- Standing desk: alert if <$400

## Triggered
- Feb 10: Sony dropped to $349 (still above target)
```

## 设置选项
```markdown
# settings.md
## Price Check Frequency
Weekly on Sundays

## Alert Preferences
Notify when:
- Price drops below target
- Price drops >15% from last check
- Item goes on sale

## Preferred Stores
- Amazon
- Best Buy
- Direct from manufacturer
```

## 价格检查流程
在检查价格时：
- 在配置好的商店中搜索当前价格。
- 将当前价格与目标价格及历史价格进行比较。
- 强制显示价格大幅下降的商品。
- 更新商品的最后检查日期。

## 信息展示内容示例：
- “索尼耳机本周降价30美元。”
- “您购物清单中的3件商品在预算范围内。”
- “Kindle的价格已经两个月没有变动了。”
- “黑色星期五即将到来——请查看高优先级的商品。”

## 智能推荐功能
- “这款商品在Prime Day经常打折。”
- “有翻新版的商品，折扣高达40%。”
- “有评价更好的类似商品，价格更便宜。”
- “您已经想要这款商品6个月了——它还符合您的需求吗？”

## 购买流程
当用户决定购买时：
- 确认当前的最佳购买价格。
- 将商品信息保存到 `purchased.md` 文件中，并记录购买日期和最终价格。
- 注意：实际购买价格是否达到了目标价格？

## 购买记录
```markdown
# purchased.md
## 2024
- Sony WH-1000XM5: $299 (Feb 20) — hit target!
- Standing desk: $450 (Jan 15) — slightly over

## Stats
- Items bought at/under target: 70%
- Average wait time: 45 days
- Total saved vs original price: $340
```

## 商品分类
为了便于浏览，商品按类别进行分类：
- 科技类：小工具、电子产品
- 家居类：家具、电器
- 服装类：新增的衣物
- 休闲爱好类：与个人兴趣相关的装备
- 礼品类：适合赠送他人的物品

## 功能逐步完善计划：
- 初始阶段：仅记录商品及其优先级。
- 后续添加目标价格信息。
- 启用价格检查功能。
- 每月检查一次：用户是否仍然需要这些商品？

## 需避免的行为：
- 不要未经查看购物清单就冲动购买。
- 不要长期保留未审核的商品记录。
- 忽视商品的价格历史变化趋势。
- 忘记自己最初想要购买这些商品的原因。