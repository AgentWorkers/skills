---
name: openclaw-tour-planner
description: "OpenClaw代理的通用旅行规划工具：通过自然语言对话即可制定行程计划、查询天气信息、查找景点以及估算旅行预算。该工具使用免费的API，核心功能无需API密钥即可使用。"
version: 1.0.2
author: Asif2BD
license: MIT
tags: [travel, itinerary, weather, tourism, planning]
website: https://openclaw.tours
repository: https://github.com/Asif2BD/openclaw.tours
---
# OpenCLAW 旅行规划工具

> **专为 OpenClaw 代理设计的通用旅行规划工具**

> 通过自然语言对话，您可以规划行程、查询天气、探索景点并估算预算。

---

## 快速入门

### 安装

```bash
# Install via ClawHub
clawhub install Asif2BD/openclaw-tour-planner

# Or via OpenClaw CLI
openclaw skills install openclaw-tour-planner

# Or clone manually
git clone https://github.com/Asif2BD/openclaw.tours.git
cd openclaw.tours
npm install
```

### 使用方法

```
User: Plan a 5-day trip to Tokyo in April
Agent: I'll create a personalized itinerary for Tokyo. Let me gather the latest information...

[Agent generates day-by-day plan with weather, attractions, and budget estimates]
```

---

## 功能

### 核心功能

| 功能 | 描述 | 数据来源 |
|---------|-------------|-------------|
| **行程规划** | 提供每日行程安排 | Wikivoyage + OSM |
| **天气预报** | 提供15天天气预测 | Visual Crossing |
| **地理编码** | 查找地点信息 | Nominatim |
| **预算估算** | 按类别分解旅行费用 | 当地数据 + API |
| **景点发现** | 推荐热门景点及隐藏宝藏 | Wikivoyage |
| **文化提示** | 提供当地风俗和礼仪信息 | Wikivoyage |

### 命令

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `plan` | 生成完整行程 | `/tour plan Tokyo 5 days in April` |
| `weather` | 查询目的地天气 | `/tour weather Tokyo next week` |
| `budget` | 估算旅行费用 | `/tour budget Tokyo 5 days mid-range` |
| `attractions` | 查找适合家庭的活动 | `/tour attractions Tokyo family-friendly` |
| `guide` | 获取目的地指南 | `/tour guide Tokyo` |

---

## 架构

### 数据流

```
User Request
    │
    ▼
┌─────────────────┐
│  Input Parser   │ ──→ Extract: destination, dates, budget, interests
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│Geocode │ │Weather │
│Nominatim│ │Visual  │
└───┬────┘ │Crossing│
    │      └───┬────┘
    │          │
    └────┬─────┘
         ▼
┌─────────────────┐
│ Wikivoyage API  │ ──→ Travel guide, attractions, tips
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Itinerary Engine│ ──→ Build day-by-day plan
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Output Formatter│ ──→ Markdown / JSON / Text
└─────────────────┘
```

### API 集成

#### 免费 tier 的 API（无需付费）

| 服务 | 功能 | 使用限制 |
|---------|---------|--------|
| **Nominatim** | 地理编码 | 每秒 1 次请求 |
| **Visual Crossing** | 天气数据 | 每天 1000 条记录 |
| **Wikivoyage** | 旅行指南 | 无限制 |
| **RestCountries** | 国家信息 | 无限制 |
| **ExchangeRate-API** | 货币汇率 | 每月 1500 次请求 |

---

## 配置

### 环境变量

```bash
# Optional — improves weather accuracy (free tier available at visualcrossing.com)
# Core features work without any keys using Open-Meteo (free, keyless)
VISUAL_CROSSING_API_KEY=your_key_here

# Optional — alternative weather source
OPENWEATHER_API_KEY=backup_weather_key

# Optional — flight search (Phase 2, not yet implemented in current release)
AMADEUS_API_KEY=flight_search_key
AMADEUS_API_SECRET=flight_search_secret

# Optional — redirect the local SQLite response cache (default: ~/.openclaw/cache/tour-planner.db)
TOUR_PLANNER_CACHE_PATH=/custom/path/tour-planner.db
```

### 技能配置（openclaw.json）

```json
{
  "skills": {
    "tour-planner": {
      "enabled": true,
      "config": {
        "defaultBudget": "mid-range",
        "cacheEnabled": true,
        "cachePath": "./cache/tour-planner.db"
      }
    }
  }
}
```

---

## 输出格式

### Markdown 格式的行程信息（默认）

```markdown
# 5-Day Tokyo Adventure

## Overview
- **Dates:** April 15-19, 2025
- **Weather:** 18-22°C, partly cloudy
- **Budget:** $1,200-1,800 (excl. flights)

## Day 1: Arrival & Shibuya
### Morning
- **10:00** Arrive at Narita/Haneda
- **12:00** Airport Express to Shibuya
- **Activity:** Shibuya Crossing + Hachiko

### Afternoon
- **14:00** Lunch at Genki Sushi
- **16:00** Meiji Shrine walk

### Evening
- **19:00** Dinner in Nonbei Yokocho
```

### JSON 格式（供代理处理）

```json
{
  "destination": "Tokyo",
  "duration_days": 5,
  "weather_summary": {...},
  "days": [...],
  "budget_breakdown": {...},
  "packing_list": [...]
}
```

---

## 开发

### 开发环境设置

```bash
# Clone repository
git clone https://github.com/Asif2BD/openclaw.tours.git
cd tour-planner

# Install dependencies
npm install

# Run tests
npm test

# Build
npm run build
```

### 项目结构

```
tour-planner/
├── src/
│   ├── apis/           # API clients
│   │   ├── nominatim.ts
│   │   ├── weather.ts
│   │   └── wikivoyage.ts
│   ├── planners/       # Planning engines
│   │   ├── itinerary.ts
│   │   └── budget.ts
│   ├── utils/          # Utilities
│   │   ├── cache.ts
│   │   └── formatter.ts
│   └── data/           # Static data
│       └── countries.json
├── tests/
├── docs/
└── package.json
```

---

## 制定计划

### 第一阶段：MVP（已完成）

- [x] 基本行程生成 |
- [x] 天气信息集成 |
- [x] Wikivoyage 指南整合 |
- [x] Markdown 格式输出

### 第二阶段：功能增强（进行中）

- [ ] 航班搜索（使用 Amadeus API） |
- [ ] 酒店价格估算 |
- [ ] 多城市行程优化 |
- [ ] PDF 文件导出

### 第三阶段：高级功能（计划中）

- [ ] 实时事件更新 |
- [ ] 餐厅预订 |
- [ ] 协作式行程规划 |
- [ ] 移动应用适配

---

## 贡献方式

我们欢迎您的贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 以获取详细指南。

### 添加新目的地

1. 检查 Wikivoyage 是否提供了该目的地的信息 |
2. 将目的地信息添加到 `data/destinations.json` 文件中 |
3. 测试行程生成功能 |
4. 提交代码更改请求（PR） |

---

## 许可证

本项目采用 MIT 许可证——详情请参阅 [LICENSE](LICENSE)。

---

## 链接

- **官方网站：** https://openclaw.tours |
- **GitHub 仓库：** https://github.com/Asif2BD/openclaw.tours |
- **文档：** https://openclaw.tours/docs |
- **问题反馈：** https://github.com/Asif2BD/openclaw.tours/issues |

---

本项目专为 OpenClaw 社区精心开发。