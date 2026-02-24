---
name: rollhub-bot-builder
description: "使用 Agent Casino API 为 Telegram、Discord 和 Twitter 构建并部署自主赌博机器人。这些机器人支持加密货币赌场功能、骰子游戏以及具有可证明公平性的硬币投掷游戏。提供适用于 python-telegram-bot、Discord.js 和 Twitter API 的机器人模板，支持自动投注、斜杠命令（slash commands）、内联键盘（inline keyboards）以及实时投注结果展示。支持部署赌博机器人、赌场机器人构建工具、Telegram 骰子游戏机器人、Discord 赌场机器人、Twitter 投注机器人以及自主交易机器人。集成 Agent.Rollhub.com API，实现实时投注通知功能，确保所有游戏过程的公平性。"
metadata:
  { "openclaw": { "emoji": "🤖" } }
---# 赌场机器人构建器

使用 Agent Casino API 为 Telegram、Discord 和 Twitter 构建并部署自主赌博机器人。可以创建加密货币赌场机器人、掷骰子机器人以及具有可证明公平性的硬币翻转机器人。提供适用于 python-telegram-bot、Discord.js 和 Twitter API 的机器人模板。支持自动投注、斜杠命令（slash commands）、内联键盘（inline keyboards）以及实时结果推送。

## 概述

本技能可帮助您为 **Telegram**、**Discord** 和 **Twitter** 创建并部署赌博机器人，这些机器人能够与 [Agent Casino API](https://agent.rollhub.com/api/v1) 进行交互。所有机器人均支持推荐跟踪（referral tracking）功能，并且投注过程具有可证明的公平性（provably fair）。

## API 基础知识

```
https://agent.rollhub.com/api/v1
```

## 第 1 步：注册 Agent 账户

每个机器人必须先在 Agent Casino 上注册：

```bash
curl -X POST https://agent.rollhub.com/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"name": "my-bot", "ref": "ref_27fcab61"}'
```

保存返回的 `agent_id` 和 `api_key`。

## 第 2 步：选择平台

### Telegram 机器人
完整模板：[references/telegram-bot.md](references/telegram-bot.md)

功能：
- `/bet <金额> <游戏>` — 下注
- `/coinflip <金额>` — 快速掷硬币
- `/dice <金额>` — 掷骰子
- `/balance` — 查看余额
- `/history` — 下注历史记录
- `/autoplay <游戏> <轮数>` — 自动播放模式
- 内联键盘（inline keyboards）用于快速投注
- 实时结果通知

### Discord 机器人
完整模板：[references/discord-bot.md](references/discord-bot.md)

功能：
- `/bet amount:100 game:coinflip` — 通过斜杠命令进行投注
- `/leaderboard` — 服务器排行榜
- `/autoplay` — 自动进行投注轮次
- 可嵌入包含投注结果的消息
- 基于角色的访问控制（role-based access control）

### Twitter 机器人
完整模板：[references/twitter-bot.md](references/twitter-bot.md)

功能：
- 自动发布投注结果推文
- 通过回复进行投注（@机器人 + 金额）
- 每日汇总推文
- 基于线程的投注会话

## 第 3 步：通过 API 下注

```bash
# Coinflip
curl -X POST https://agent.rollhub.com/api/v1/bet \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"game": "coinflip", "amount": 100, "choice": "heads"}'

# Dice
curl -X POST https://agent.rollhub.com/api/v1/bet \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"game": "dice", "amount": 100, "target": 50, "over": true}'
```

## 第 4 步：验证结果（可证明的公平性）

每次投注都会返回 `server_seed_hash`、`client_seed` 和 `nonce`。请进行验证：

```bash
curl https://agent.rollhub.com/api/v1/verify/<bet_id>
```

## 第 5 步：自动播放模式

所有机器人模板均支持自动播放功能：
1. 设置游戏、投注金额和轮数
2. 机器人会自动进行投注，并可配置延迟时间
3. 停止条件：最大损失、目标利润或轮数限制
4. 结果会被记录并报告

## 快速设置

运行设置辅助工具：

```bash
bash scripts/setup-bot.sh telegram  # or discord, twitter
```

## 关键词

赌场机器人构建器（Casino Bot Builder）、Telegram 掷骰子机器人（Telegram Dice Bot）、Discord 赌场机器人（Discord Casino Bot）、Twitter 投注机器人（Twitter Betting Bot）、加密货币赌博机器人（Crypto Gambling Bot）、自动投注（Autonomous Betting）、可证明公平性机器人（Provably Fair Bot）、Agent Casino API（Agent Casino API）、硬币翻转机器人（Coinflip Bot）、掷骰子机器人（Dice Bot）、赌博自动化（Gambling Automation）、机器人部署（Bot Deployment）、斜杠命令（Slash Commands）、内联键盘（Inline Keyboards）、自动播放机器人（Auto-Play Bot）、实时通知（Real-Time Notifications）、agent.rollhub.com（agent.rollhub.com）。