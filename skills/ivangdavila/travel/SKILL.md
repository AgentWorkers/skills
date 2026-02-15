---
name: Travel
description: 构建一个个人旅行系统，用于规划梦想中的目的地之旅并记录旅行中的美好回忆。
metadata: {"clawdbot":{"emoji":"✈️","os":["linux","darwin","win32"]}}
---

## 核心功能
- 当用户提到旅行计划时，建议将其添加到愿望清单中。
- 当用户开始规划旅行时，会为其创建一个包含行程清单的文件夹。
- 当用户旅行归来后，会帮助其整理旅行回忆并记录下来。
- 系统会自动创建一个名为 `~/travel/` 的工作文件夹用于存储所有旅行相关文件。

## 使用场景
- 梦想目的地：用户希望未来必去的地点。
- 旅行规划：包括行程安排、酒店预订、行李打包等。
- 旅行回忆：保存照片、笔记和旅行建议。
- 实用信息：签证、疫苗接种要求、所需文件等。
- 预算管理：按每次旅行及总体预算进行记录。

## 文件结构
```
~/travel/
├── wishlist/
│   └── japan.md
├── planned/
│   └── paris-2024/
├── completed/
│   └── iceland-2023/
├── documents/
│   └── passport-info.md
└── packing-templates/
    └── beach-week.md
```

## 愿望清单条目
```markdown
# japan.md
## Why
Cherry blossoms, food culture, temples

## Best Time
Late March - early April (sakura)

## Rough Duration
2-3 weeks ideal

## Must See
- Kyoto temples
- Tokyo neighborhoods
- Mount Fuji area

## Estimated Budget
$3000-4000 for 2 weeks

## Notes
Need to book cherry blossom season early
```

## 计划中的旅行文件夹
```
paris-2024/
├── overview.md
├── itinerary.md
├── bookings.md
├── packing.md
└── budget.md
```

## 旅行概览
```markdown
# Paris 2024
## Dates
May 15-22, 2024

## Purpose
Anniversary trip

## Accommodation
Hotel in Le Marais

## Transport
Flight + metro pass

## Key Bookings
- Louvre timed entry
- Restaurant reservation
```

## 行程规划
- 提供灵活的每日行程安排（分为上午、下午和晚上三个时间段）。
- 包括具体地址和活动时间。
- 为各项活动预留适当的缓冲时间。
- 区分必须完成的事项和可选事项。

## 预订跟踪
- 航班信息：确认航班、航班时间、座位安排。
- 酒店信息：确认入住信息、酒店地址、入住时间。
- 活动信息：门票、预订详情等。
- 所有预订信息集中存储在一个地方。

## 行李清单
- 从模板开始，根据每次旅行进行个性化定制。
- 考虑当地天气情况调整行李清单。
- 根据具体活动准备所需装备。
- 文档清单：护照、签证、保险文件等。
- 电子设备：充电宝、适配器等必备物品。

## 预算管理
- 旅行前：记录航班、酒店等费用。
- 旅行中：每日开支记录。
- 预算分类：餐饮、交通、活动、购物等。
- 旅行结束后统计总预算，以供日后参考。

## 已完成的旅行记录
```markdown
# Iceland 2023
## Dates
August 5-12, 2023

## Highlights
- Northern lights (unexpected in August!)
- Golden Circle drive
- Blue Lagoon

## Recommendations
- Rent 4x4, worth it for F-roads
- Book Blue Lagoon weeks ahead
- Gas stations accept cards everywhere

## Would Skip
- Overpriced Reykjavik restaurants

## Photos
[link to album]

## Total Spent
$2,847 for 2 people, 7 days
```

## 文档管理
- 提醒用户护照的到期日期。
- 提供各国签证要求信息。
- 显示用户的飞行常客编号。
- 提供海外紧急联系人的联系方式。

## 重要提示
- “您的护照6个月后到期。”
- “日本在您的愿望清单中——樱花季是3月。”
- “您上次去巴黎时推荐了X餐厅。”
- “您在欧洲的日常预算约为每天200美元。”

## 持续改进计划
- 第一周：在愿望清单中添加3-5个梦想目的地。
- 第一次旅行时：创建完整的旅行文件夹。
- 旅行结束后：整理旅行亮点和推荐事项。
- 持续优化：完善行李打包模板，分析消费习惯。

## 需避免的行为
- 不要过度规划每一分钟——留出探索的空间。
- 旅行结束后忘记记录回忆——回忆会逐渐消失。
- 不要忽略保存预订信息——以后可能会需要通过邮件查找。
- 不要设计过于复杂的行程安排——简单的计划更易于执行。