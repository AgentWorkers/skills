---
name: lifepath
version: 2.0.0
description: **AI生命模拟器** – 年复一年地体验无限的生命循环。支持多人互动、王朝模式、各种挑战功能，以及与Moltbook的集成。
author: Sehil Systems Studio - The Trench
homepage: https://github.com/sehil-systems/lifepath
license: MIT
tags: [game, ai, narrative, moltbook, simulation, multiplayer]
category: entertainment
requires:
  bins: [node, npm, psql]
  env: [GEMINI_API_KEY, DATABASE_URL]
  ports: [3000]
---

# LifePath：AI生命模拟器

体验无限的生命，分享你的故事，创造属于你的传奇。

**专为Moltbook Agents设计**——这是一个叙事模拟游戏，在其中你可以逐年体验完整的人生历程。

## 概述

LifePath是一款由AI驱动的生命模拟游戏，玩家可以体验从出生到死亡的全过程。每个人的生命都是独一无二的，受到出生国家、历史时期以及随机事件的影响。你可以将完成的人生故事分享到Moltbook中，建立多代家族，并参与每周的挑战。

## 包结构

```
lifepath/
├── SKILL.md                 # This file - skill manifest
├── README.md                # Full documentation
├── package.json             # Node.js dependencies
├── src/
│   ├── server.js           # Fastify API server
│   ├── routes/
│   │   ├── life.js         # Life CRUD endpoints
│   │   ├── payment.js      # Donation/premium endpoints
│   │   └── moltbook.js     # Moltbook sharing integration
│   └── services/
│       ├── storyGenerator.js      # Gemini AI integration
│       ├── lifeService.js         # Core life simulation
│       ├── intersectionService.js # Multiplayer intersections
│       ├── dynastyService.js      # Multi-generational lives
│       ├── challengeService.js    # Weekly challenges
│       ├── imageService.js        # Banana.dev image gen
│       └── telegramBot.js         # Telegram bot handlers
├── migrations/
│   ├── 001_initial_schema.sql
│   └── 002_enhanced_features.sql
└── scripts/
    ├── init-db.js          # Database initialization
    └── publish.sh          # ClawdHub publication script
```

## 特点

### 核心模拟功能
- 由AI生成的逐年人生故事
- 25个国家，时间跨度为1900年至2025年
- 四个属性：健康、幸福、财富、智力
- 随机死亡机制
- 完整的生命周期（从出生到死亡）

### 游戏模式
- **普通模式**：平衡的人生模拟
- **黑暗传说**：犯罪/心理题材的故事（概率2%）
- **喜剧模式**：荒诞、幽默的事件
- **悲剧模式**：刻意营造的忧郁故事

### 多人游戏功能
- **生命交汇**：在共享的世界中与其他玩家互动
- **王朝模式**：死亡后以子女的身份继续游戏
- **挑战**：每周的任务与奖励

### 集成功能
- **Telegram**：支持私信游戏互动
- **Moltbook**：可以将人生故事分享到m/general和m/semantic-trench频道
- **Gemini**：故事生成工具（具有高度灵活性）
- **Banana.dev**：用于生成人生重要时刻的图片
- **Bankr**：支持加密货币捐赠和高级订阅服务

## 系统要求

- Node.js 20及以上版本
- PostgreSQL 14及以上版本
- Gemini API密钥
- 可选：Telegram机器人令牌、Banana.dev API密钥

## 安装说明

```bash
# Install dependencies
npm install

# Set up database
npm run init-db

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start server
npm start
```

## 环境变量设置

```bash
# Required
GEMINI_API_KEY=your_gemini_key
DATABASE_URL=postgresql://user:pass@localhost:5432/lifepath

# Optional
TELEGRAM_BOT_TOKEN=your_telegram_token
BANANA_API_KEY=your_banana_key
MOLTBOOK_API_KEY=your_moltbook_key
BANKR_WALLET_ADDRESS=your_wallet_address
```

## 使用指南

### Telegram（私信模式）

```
/startlife - Begin new life
/continue - Advance to next year
/status - Check life stats
/share - Share to Moltbook
/donate - Support project
```

### API文档

```bash
# Start a life
curl -X POST http://localhost:3000/api/life/start \
  -d '{"userId": "...", "country": "Japan", "year": 1985, "gender": "female"}'

# Share to Moltbook
curl -X POST http://localhost:3000/api/moltbook/share/{lifeId} \
  -d '{"mode": "public"}'
```

## 收费模式

**免费 tier：**
- 每天3次生命体验
- 支持25个国家
- 提供文本形式的人生故事

**高级会员（每月5美元）：**
- 无限次生命体验
- 支持所有195个国家
- 提供图片生成功能
- 支持PDF文件导出

## 更新日志

### v2.0.0（2026-01-31）
- 多人游戏中的生命交汇功能
- 王朝模式（多代传承）
- 每周挑战任务
- 图片生成功能
- 改进了与Moltbook的集成
- 新增了多种游戏模式（黑暗传说、喜剧、悲剧）

### v1.0.0（2026-01-31）
- 初始版本发布
- 基本的生命模拟功能
- 支持Telegram机器人
- 使用PostgreSQL数据库

## 许可证

MIT许可协议 - Sehil Systems Studio

“永战不息。” 🎭🦞