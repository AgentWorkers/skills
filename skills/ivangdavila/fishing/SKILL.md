---
name: Fishing
slug: fishing
version: 1.0.0
homepage: https://clawic.com/skills/fishing
description: 跟踪钓鱼地点、使用的装备、捕获的鱼类以及当天的钓鱼条件，并提供个性化的建议。
metadata: {"clawdbot":{"emoji":"🎣","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户希望记录自己的钓鱼活动、记住喜欢的钓鱼地点、记录捕获的鱼类信息，或者根据自己的钓鱼历史获得个性化的装备和技术建议。

## 架构

所有数据存储在 `~/fishing/` 目录下。具体设置方法请参考 `memory-template.md` 文件。

```
~/fishing/
├── memory.md          # HOT: preferences, gear, active spots
├── catches.md         # WARM: catch log with dates, species, conditions
├── spots.md           # WARM: saved locations with notes
└── archive/           # COLD: past seasons
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 数据库设置 | `memory-template.md` |
| 鱼类信息 | `species.md` |
| 钓具指南 | `tackle.md` |

## 核心规则

### 1. 先查看数据库信息
在给出任何建议之前，请先阅读 `~/fishing/memory.md`，以了解以下内容：
- 用户的钓鱼装备清单
- 偏好的钓鱼物种
- 技能水平
- 用户遵守的当地钓鱼规定

### 2. 主动记录捕获信息
当用户报告捕获情况后，请更新 `~/fishing/catches.md` 文件，内容如下：
| 日期 | 鱼类 | 重量 | 钓鱼地点 | 钓鱼环境 | 使用的钓鱼技巧 |
|------|---------|--------|------|------------|-----------|
| YYYY-MM-DD | 鲈鱼 | 3.5磅 | X湖 | 多云，气温65华氏度 | 使用德州式钓具（Texas rig） |

### 3. 分析钓鱼地点的规律
在 `~/fishing/spots.md` 文件中记录每个地点的钓鱼规律：
- 最佳钓鱼时间（黎明、黄昏、潮汐）
- 有效的钓鱼技巧
- 季节性钓鱼建议

### 4. 提供个性化建议
根据用户的捕获记录，给出以下建议：
- “最近在X湖捕获的3条鲈鱼都是在多云的早晨，使用塑料饵料时捕获的”
- “您自春季以来还没有去Y地点钓鱼——现在是繁殖季节”

### 5. 确保推荐的装备用户已拥有
只推荐用户实际拥有的装备（信息来源于 `memory.md`）。如果建议购买新装备，请明确标注为购买建议。

## 常见问题

- 如果建议用户购买其未拥有的装备，请先检查用户的装备清单。
- 提供的通用建议应忽略用户的实际钓鱼历史。
- 如果忘记考虑季节性因素，请按月查看 `catches.md` 文件。
- 如果不更新 `spots.md` 文件，建议将会过时。

## 相关工具
如果用户需要，可以使用以下工具进行扩展：
- `clawhub install <slug>`：用于安装相关工具（如 `plan`（行程规划工具）和 `remind`（行程提醒工具）。

## 反馈方式
- 如果对服务有用，请使用 `clawhub star fishing` 给予评价。
- 为了保持信息更新，请使用 `clawhub sync` 功能。