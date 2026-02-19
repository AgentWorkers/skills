---
name: Gym
slug: gym
version: 1.0.1
description: 记录锻炼情况、规划训练计划、跟踪进度，并获得适合任何健身水平的智能指导。
changelog: "Preferences now persist across skill updates"
metadata: {"clawdbot":{"emoji":"🏋️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 快速参考

| 主题 | 文件 |
|-------|------|
| 练习、训练计划、模板 | `workouts.md` |
| 进度跟踪、训练量、个人请求（PRs） | `progress.md` |
| 伤势适应与训练调整 | `adaptation.md` |
| 健身房营养、宏量营养素、训练时间安排 | `nutrition.md` |

## 用户资料

用户的偏好设置保存在 `~/gym/memory.md` 文件中。首次使用时需要创建该文件：

```markdown
## Level
<!-- beginner | intermediate | advanced -->

## Goals
<!-- strength | hypertrophy | fat-loss | general-fitness | powerlifting -->

## Schedule
<!-- Days available. Format: "days | frequency" -->
<!-- Examples: Mon/Wed/Fri, 3x/week, daily -->

## Session Duration
<!-- 45min | 60min | 90min -->

## Restrictions
<!-- Injuries, equipment limits, mobility issues -->
<!-- Examples: Lower back injury (no deadlifts), Home gym (no cable machine) -->
```

*首次使用时填写相关信息。随着目标的变化，请随时更新。*

## 数据存储

训练日志和各项数据存储在 `~/gym/` 目录下：
- `workouts`：训练记录（日期、练习项目、组数、次数、重量）
- `prs`：按练习项目划分的个人最佳成绩
- `measurements`：身体各项数据、体重变化趋势

## 核心训练规则

- 在推荐练习前，请务必确认用户是否有相关禁忌或限制。
- 每次训练应优先进行复合动作（深蹲、硬拉、推举、划船、引体向上）。
- 采用渐进式增负荷原则：如果上一次训练完成得不错，建议增加2.5公斤的重量或增加1-2次重复次数。
- 休息时间：力量训练时休息2-3分钟，增肌训练时休息60-90秒，有氧训练时休息30-45秒。
- 每周的负荷增幅不要超过10%，以避免受伤风险。
- 每4-6周安排一次减负荷周，或当用户表示持续疲劳时也应进行减负荷调整。
- 如果用户错过训练日，无需自责，只需重新计算训练计划即可。
- 当需要记录RPE（相对强度感知）时，请务必记录下来，以便进行自动调整。
- 如果用户连续48小时内未休息就训练同一肌肉群，请发出警告，建议采取适当的恢复措施。