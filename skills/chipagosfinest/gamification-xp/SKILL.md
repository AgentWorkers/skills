---
name: gamification
version: 1.1.0
description: 通过ClawdBot实现生产力游戏化的XP系统——记录等级、徽章、连续使用时长以及各种成就
author: ClawdBot
category: productivity
tags:
  - gamification
  - xp
  - levels
  - badges
  - streaks
  - habits
  - productivity
  - motivation
  - achievements
  - goals
env:
  - name: SUPABASE_URL
    description: Supabase project URL for gamification data storage
    required: true
  - name: SUPABASE_SERVICE_KEY
    description: Supabase service role key for database access
    required: true
keywords:
  - earn xp
  - level up
  - streak bonus
  - habit tracking
  - goal milestones
  - leaderboard
  - accountability
triggers:
  - my xp
  - what level am I
  - my badges
  - leaderboard
  - xp stats
  - gamification stats
---

# 游戏化与经验值（XP）系统

通过经验值（XP）、等级、徽章、连续完成任务的天数（连击）和成就，将工作效率转化为一种游戏体验。每完成一项任务、养成一个习惯或达到一个目标里程碑，你都会获得经验值，从而提升等级。

## 与 ClawdBot 的集成

此功能专为 **ClawdBot** 设计，它为 ClawdBot 的游戏化 API 服务器提供提示界面，并将数据存储在 Supabase 数据库中。

**架构：**
```
User → ClawdBot Gateway → ClawdBot API Server → Supabase (Postgres)
                         (Railway)              (user_gamification, xp_transactions tables)
```

后端实现代码位于 `api-server/src/routes/gamification.ts` 和 `api-server/src/lib/xp-engine.ts` 文件中。

## 主要功能

- **经验值系统**：通过养成习惯、完成任务或达成目标来获取经验值。
- **等级提升**：等级提升的计算公式为 `XP = 50 * (level^2)`。
- **连击奖励**：持续养成某个习惯可享受最高 2.0 倍的经验值加成。
- **徽章**：通过达成成就或完成特定目标来获得徽章。
- **排行榜**：支持多用户查看进度。
- **问责机制**：跟踪用户的表现并给予相应的奖励或惩罚。

## 环境变量

| 变量          | 是否必需 | 说明                          |
|---------------|---------|-------------------------------------------|
| `SUPABASE_URL`     | 是       | Supabase 项目的 URL                          |
| `SUPABASE_SERVICE_KEY` | 是       | Supabase 服务的访问密钥                        |

## API 端点

所有 API 端点都以 ClawdBot API 服务器的路径 `{CLAWDBOT_API_URL}/api/gamification/` 为基准。

### 获取用户统计信息
```
GET /api/gamification/stats/:userId
```

响应数据：
```json
{
  "totalXp": 2450,
  "currentLevel": 7,
  "weeklyXp": 350,
  "monthlyXp": 1200,
  "progress": {
    "xpInLevel": 150,
    "xpNeeded": 450,
    "percent": 33
  },
  "accountability": {
    "balance": 50,
    "totalSlashed": 10,
    "totalEarnedBack": 60
  }
}
```

### 获取最近的操作记录
```
GET /api/gamification/transactions/:userId?limit=20
```

### 获取用户获得的徽章
```
GET /api/gamification/badges/:userId
```

### 内部奖励：分配经验值
```
POST /api/gamification/award
{
  "userId": "302137836",
  "amount": 50,
  "source": "habit",
  "sourceId": "morning-routine",
  "note": "Completed morning routine"
}
```

### 完成习惯（包含连击奖励）
```
POST /api/gamification/habit-complete
{
  "userId": "302137836",
  "habitId": "workout",
  "currentStreak": 7
}
```

### 完成任务
```
POST /api/gamification/task-complete
{
  "userId": "302137836",
  "taskId": "task-123",
  "priority": 8
}
```

### 达成目标里程碑
```
POST /api/gamification/goal-milestone
{
  "userId": "302137836",
  "goalId": "goal-456",
  "milestonePercent": 50
}
```

### 颁发徽章
```
POST /api/gamification/badge
{
  "userId": "302137836",
  "badgeType": "early_bird",
  "metadata": { "streak": 30 }
}
```

### 查看排行榜
```
GET /api/gamification/leaderboard
```

### 获取经验值配置
```
GET /api/gamification/config
```

## 数据库表

此功能需要使用以下 Supabase 数据表：
- `user_gamification`：存储用户的总经验值、当前等级和连击天数。
- `xp_transactions`：记录经验值的分配历史。
- `user_badges`：存储用户获得的徽章信息。

## 经验值奖励规则

| 操作            | 基础经验值 | 备注                          |
|-----------------|---------|-------------------------------------------|
| 完成习惯          | 10–50       | 可获得最高 2 倍的连击奖励                 |
| 完成任务          | 5–50       | 根据任务优先级（1–10）分配经验值                 |
| 达成 25% 的目标    | 100       | 第一季度的目标完成                   |
| 达成 50% 的目标    | 200       | 目标完成一半                     |
| 达成 75% 的目标    | 300       | 目标完成三分之二                     |
| 完成 100% 的目标    | 500       | 目标完全完成                     |

## 示例用法

### 检查用户进度
```
"What's my XP level?"
"How close am I to leveling up?"
"Show my gamification stats"
```

### 查看用户成就
```
"What badges do I have?"
"Show my recent XP transactions"
"What's my current streak?"
```

### 查看排行榜
```
"Show the leaderboard"
"Who has the most XP?"
```

## 相关功能

- `goals`：用于设置和跟踪目标。
- `habits`：习惯养成管理系统。
- `remind`：提醒系统。
- `daily-briefing`：每日进度总结。