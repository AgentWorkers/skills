---
name: Games
description: 构建一个个人游戏系统，用于玩电子游戏、棋盘游戏、聚会游戏以及进行家庭活动。
metadata: {"clawdbot":{"emoji":"🎮","os":["linux","darwin","win32"]}}
---

## 核心行为
- 当用户提到某款游戏时，主动提出为其记录游戏信息。
- 当用户询问想玩什么游戏时，首先了解游戏的相关背景信息。
- 当用户完成或玩完游戏后，帮助用户记录游戏体验和感受。
- 创建一个名为 `~/games/` 的文件夹作为游戏资料存储空间。

## 文件结构
```
~/games/
├── video/
│   ├── backlog.md
│   ├── playing.md
│   └── completed/
├── board/
│   ├── collection.md
│   └── wishlist.md
├── party/
│   └── ideas.md
├── kids/
│   └── activities.md
├── favorites.md
└── game-nights.md
```

## 视频游戏
```markdown
# video/playing.md
## Elden Ring
Platform: PS5
Hours: ~30
Where I Left Off: Just beat Margit

# video/backlog.md
## High Priority
- Baldur's Gate 3 — need 100 hours clear

## On Sale Watch
- Disco Elysium — wait for 50% off
```

## 桌游集合
```markdown
# board/collection.md
## Own
- Catan — classic, good for newbies
- Wingspan — beautiful, medium complexity
- Codenames — perfect party game
- Ticket to Ride — family friendly

## By Player Count
### 2 Players
- 7 Wonders Duel
- Patchwork

### 5+ Players
- Codenames
- Wavelength
- Deception: Murder in Hong Kong
```

## 团体游戏
```markdown
# party/ideas.md
## No Equipment Needed
- Charades
- 20 Questions
- Two Truths and a Lie
- Mafia/Werewolf

## With Cards/Board
- Codenames
- Wavelength
- Just One

## Drinking Games (adults)
- Kings Cup
- Beer Pong
```

## 儿童活动
```markdown
# kids/activities.md
## By Age
### Toddlers (2-4)
- Hide and seek
- Simon says
- Duck duck goose

### Kids (5-10)
- Uno
- Candy Land
- Scavenger hunts
- Freeze dance

### Tweens
- Exploding Kittens
- Ticket to Ride
- Minecraft together
```

## 游戏之夜记录
```markdown
# game-nights.md
## Feb 10, 2024
Group: Jake, Sarah, Mike
Played: Catan, Codenames
Winner: Sarah dominated Catan
Notes: Need 5-player game next time

## What Worked
Codenames teams were balanced
```

## 最爱游戏
```markdown
# favorites.md
## Video Games
1. Breath of the Wild
2. Hades

## Board Games
- Wingspan (2 player)
- Codenames (groups)

## Party
- Wavelength — always a hit

## With Kids
- Uno — easy, quick
```

## 建议内容
- “你有《卡坦岛》这款游戏，非常适合这个团队规模。”
- “上次游戏之夜，大家希望玩一款5人游戏。”
- “推荐一些你评价很高的、类似桌游的游戏。”
- “选择适合儿童参与的游戏。”

## 推荐策略
当用户询问想玩什么游戏时：
- 询问游戏类型（单人游戏、多人游戏、适合特定日期或群体的游戏）以及是否有儿童参与。
- 根据玩家人数选择合适的游戏。
- 考虑玩家的游戏经验及游戏难度。
- 查看用户已拥有的游戏，以便推荐适合他们的游戏。

## 需要记录的信息
- 视频游戏：平台、游戏时长、游戏进度、用户评分。
- 桌游：参与玩家人数、游戏难度、游戏时长。
- 对于同时涉及视频游戏和桌游的情况，还需记录哪些玩家喜欢这些游戏，以及它们在什么情况下最适合玩。

## 持续改进的步骤
- 初始阶段：列出用户已拥有的游戏（视频游戏和桌游）。
- 添加用户喜欢的游戏，并附上相关背景信息。
- 记录每次游戏之夜的详细情况，以便发现游戏使用规律。
- 逐步丰富适合团体或儿童的游戏推荐库。

## 不应做的事情
- 未经询问就推荐用户没有的游戏。
- 为休闲团队推荐难度过高的游戏。
- 忽视玩家人数限制。
- 忽视游戏的年龄适宜性。