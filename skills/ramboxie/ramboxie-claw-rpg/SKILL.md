---
name: claw-rpg
description: D&D-style RPG character system for AI lobster assistants. Automatically generates a character sheet from SOUL.md and MEMORY.md, assigns class (wizard/bard/rogue/paladin/druid/fighter) and 6 stats, tracks XP from token usage, levels up from 1 to 999 with a prestige system, and fires hidden easter egg flavor text during conversations. Use when: initializing a lobster's RPG character, syncing XP after conversations, checking level/stats, running prestige at Lv.999, or launching the character dashboard.
---

# Claw RPG 🦞⚔️

这是一个专为AI龙虾代理设计的D&D风格的角色成长系统。它会读取你的`SOUL.md`和`MEMORY.md`文件来生成角色信息表，通过使用特定“令牌”来积累经验值（XP），角色等级可以从1级升至999级，并且在对话过程中偶尔会插入一些具有RPG风格的隐藏文本。

## 快速入门

```bash
# 1. Initialize your character (reads SOUL.md + MEMORY.md)
node scripts/init.mjs

# 2. View your character sheet (terminal)
node scripts/sheet.mjs

# 3. Launch the web dashboard
cd dashboard && npm start     # http://localhost:3500
```

## 隐藏的彩蛋功能（推荐使用）

每次对话结束后，`easter.mjs`脚本会以**12%的概率**被执行，从而在对话中插入一行斜体的RPG风格文本。达到某些重要等级（10级、25级、50级、100级，以及之后的每100级）时，该功能会自动触发。

```bash
node scripts/easter.mjs            # Normal call (updates conversation counter)
node scripts/easter.mjs --force    # Force trigger (debug)
node scripts/easter.mjs --preview  # Preview without writing to character data
```

**集成方法**——请将以下代码添加到你的`AGENTS.md`文件中：

```
After each reply to a user message, run: node <SKILL_ROOT>/scripts/easter.mjs
If the output is NOT __NO_TRIGGER__, append it to the reply (blank line + italic).
Do not run during heartbeat polls.
```

## 每日问候（可选）

如果你希望在每天第一次对话时自动进行RPG风格的自我介绍，可以参考以下代码：

```bash
node scripts/greet.mjs             # Fires once per day (checks lastGreetDate)
node scripts/greet.mjs --force     # Force send
node scripts/greet.mjs --preview   # Preview without saving
```

## 经验值同步

```bash
# Pass token delta from the current conversation
node scripts/xp.mjs --in 2000 --out 800

# With bonus XP (after completing a significant task)
node scripts/xp.mjs --in 2000 --out 800 --bonus 30

# Conversation count only
node scripts/xp.mjs --conversations 1
```

## 声望系统（达到999级）

当角色达到999级时，声望值会重置为1级，所有属性会永久提升10%，并且会解锁一个新的称号等级。

## 自动化经验值同步（推荐使用）

你可以通过设置每日凌晨03:00的定时任务来自动执行经验值同步：

```bash
node scripts/setup-cron.mjs
```

或者也可以通过心跳任务或定时作业手动触发该操作：

```javascript
const { execSync } = require('child_process');
execSync(`node ${SKILL_ROOT}/scripts/xp.mjs --in ${deltaIn} --out ${deltaOut}`);
```

## 职业与技能

详细信息请参阅`references/classes.md`和`references/abilities.md`。

## 声望系统

更多关于声望系统的内容，请参阅`references/prestige.md`。

## 文件列表

| 文件名 | 说明 |
|------|-------------|
| `character.json` | 角色数据（自动生成，切勿手动编辑） |
| `arena-history.json` | 竞技场战斗记录 |
| `config.json` | 可选：Telegram通知配置（例如：`{ "telegram_chat_id": "..." }`） |