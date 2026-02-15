---
name: Gifts
description: 构建一个个人礼物系统，用于记录各种想法、送礼场合以及送礼的历史记录。
metadata: {"clawdbot":{"emoji":"🎁","os":["linux","darwin","win32"]}}
---

## 核心功能
- 当用户提到礼物建议时，将其保存到该用户的文件中。
- 当用户询问应该送什么礼物时，首先查看已保存的建议。
- 当用户赠送或收到礼物时，记录下来以供将来参考。
- 创建一个名为 `~/gifts/` 的文件夹作为礼物存储空间。

## 文件结构
```
~/gifts/
├── people/
│   ├── mom.md
│   └── sarah.md
├── occasions/
│   └── birthdays.md
├── given/
│   └── 2024.md
├── ideas/
│   └── generic.md
└── my-wishlist.md
```

## 用户文件
```markdown
# sarah.md
## Basics
Birthday: March 15

## Interests
Cooking (Italian), yoga, true crime podcasts

## Sizes
Clothing: M, Shoes: 38 EU

## Ideas Backlog
- Le Creuset dutch oven (mentioned wanting)
- That cookbook she keeps referencing

## Given History
- 2024: Knife set — loved it
- 2023: Cooking class — went together

## Avoid
Candles (has too many)
```

## 捕获礼物建议
当用户提到某人想要某样东西时：
- 立即保存相关信息，并注明上下文（例如：“在做饭时提到的”或“看到她在看那个东西”）。
- 非正式的提及可以作为后续选择礼物的参考。

## 派对/活动日历
```markdown
# birthdays.md
## March
- Sarah: 15th
- Mom: 22nd
```

## 礼物赠送记录
```markdown
# given/2024.md
## Sarah — Birthday
Knife set, $120 — loved it, uses daily

## Mom — Mother's Day
Spa day — went together
```

## 通用礼物建议库
```markdown
# generic.md
## Safe Options
Nice candle, quality chocolates, gift card

## Experiences
Concert tickets, cooking class, spa day
```

## 我的愿望清单
```markdown
# my-wishlist.md
## Want
- AirPods Max
- Leather weekender bag

## Sizes & Notes
L shirts, 10 US shoes
Avoid: cologne, novelty items
```

## 需要展示的信息
- “Sarah 的生日还有两周。”
- “你上个月为她保存了一个礼物建议。”
- “去年你送了她 X，效果很好。”

## 持续改进计划
- 初始阶段：优先记录生日临近的亲朋好友的礼物建议。
- 进行中：每当有人提到礼物建议时立即记录下来。
- 礼物赠送后：记录对方的反应。

## 不应做的事情
- 未经查看用户文件就推荐通用礼物。
- 忘记记录礼物赠送情况（避免重复赠送相同的礼物）。
- 错过用户表达“我想要那个礼物”的时刻。