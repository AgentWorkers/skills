---
name: clawflight
description: 查找支持 Starlink 卫星 WiFi 的航班。筛选条件仅限于提供 Starlink 服务的航空公司；结果按 WiFi 信号质量、价格或飞行延迟进行排序，并提供联盟预订链接。适用于需要在飞机上工作的乘客。
---
# ✈️ ClawFlight 技能

这是一个以人工智能为核心的航班搜索工具，专门用于查找提供 Starlink 互联网服务的航班。它专为需要在长途飞行中工作的商务旅客和数字游民设计。

## 功能介绍

- 🔍 **搜索航班**：可以在任意机场之间搜索航班。
- 🛜 **筛选 Starlink 服务**：仅显示提供 Starlink 服务的航空公司航班。
- ⭐ **按优先级排序**：可以根据 WiFi 质量、价格、飞行时长或减少时差的效果进行排序。
- 🔗 **直接预订链接**：提供通过 Kiwi.com 和 Skyscanner 的直接预订链接。
- 📊 **评价航班**：用户可以提交关于 WiFi 质量的评分（包括速度、稳定性、使用便捷性等）。
- ⏰ **飞行后提醒**：系统会在航班降落 6 小时后自动提醒用户评价航班的 WiFi 服务。

## 设置

```bash
# Install dependencies
cd ~/clawd/projects/clawflight/skill
npm install

# Get a FREE Amadeus API key (no credit card required):
# 1. Go to https://developers.amadeus.com/self-service
# 2. Register → Create App → copy Client ID + Secret
# 3. Set environment variables:

export AMADEUS_CLIENT_ID="your_client_id"
export AMADEUS_CLIENT_SECRET="your_client_secret"

# Optional: use production data (requires moving to production in Amadeus portal)
export AMADEUS_ENV=production
```

WiFi 评分数据库由 ClawFlight 维护，您只需提供自己的 Amadeus 密钥即可获取实时航班数据。无需其他 API 密钥。

## 命令

### 搜索航班

```
clawflight search --from BKK --to LHR --date 2026-03-14 --priority wifi
```

选项：
- `--from, -f` — 起飞机场 IATA 代码（例如：BKK、LHR、SFO）
- `--to, -t` — 目的地机场 IATA 代码
- `--date, -d` — 出发日期（格式：YYYY-MM-DD）
- `--priority, -p` — 排序方式：`wifi`（默认）、`cheap`（价格）、`fast`（速度）、`jetlag`（减少时差）
- `--adults, -a` — 乘客人数（默认：1 人）
- `--json` — 以机器可读的 JSON 格式输出结果

### 查看提供 Starlink 服务的航空公司

```
clawflight airlines
```

显示数据库中所有提供 Starlink 服务的航空公司及其航班覆盖范围。

### 保存航班信息（用于飞行后评价）

```
clawflight save --flight UA123 --arrival 2026-03-15T14:30:00Z
```

用户可以保存航班信息，系统会在航班降落 6 小时后自动提醒用户评价 WiFi 服务。

### 评价航班

```
clawflight rate --airline UA --speed 5 --reliability 4 --ease 5
```

用户可以提交关于 WiFi 质量的评分，以帮助构建社区评价数据库。

## 使用示例

### “帮我查找下周从纽约飞往伦敦的航班，且航班提供良好的 WiFi 服务”

```bash
clawflight search --from JFK --to LHR --date 2026-03-10 --priority wifi
```

输出结果：
```
🛫 ClawFlight Results

✈️ #1 — United Airlines (Starlink ⭐ 4.7)
   Mar 10 | 7h05 | $540 | New York → London
   Book: https://www.kiwi.com/deep?affilid=clawflight&booking_token=...

✈️ #2 — Air France (Starlink ⭐ 4.3)
   Mar 10 | 7h25 | $485 | New York → Paris → London
   Book: https://www.kiwi.com/deep?...
```

### “显示最便宜的航班选项”

```bash
clawflight search --from SFO --to NRT --date 2026-04-01 --priority cheap
```

### “我希望尽量减少飞行时的时差”

```bash
clawflight search --from LAX --to SYD --date 2026-05-15 --priority jetlag
```

## 航空公司数据库

该技能使用存储在 `data/airlines.json` 文件中的 Starlink 服务航空公司列表。当前支持的航空公司包括：

| 航空公司 | 代码 | 航班覆盖范围 | WiFi 服务类型 |
|---------|------|----------------|-----------|
| 联合航空公司 | UA | 85% | Starlink |
| 夏威夷航空公司 | HA | 90% | Starlink |
| JSX | JSX | 100% | Starlink |
| 卡塔尔航空公司 | QR | 40% | Starlink |
| 法国航空公司 | AF | 30% | Starlink |
| 达美航空公司 | DL | 15% | Starlink |
| 阿拉斯加航空公司 | AS | 35% | Starlink |
| 西南航空公司 | WN | 20% | Starlink |

**注意：**航班覆盖范围为大致数据，航空公司可能会更换使用的飞机，因此并非每趟航班都提供 Starlink 服务。

## 与 OpenClaw 的集成

该技能可以在 OpenClaw 的对话界面中直接调用。

## 相关文件

```
skill/
├── package.json       # Dependencies (axios, commander)
├── clawflight.js      # Main CLI script
└── SKILL.md          # This file

data/
├── airlines.json      # Starlink airline database
├── saved-flights.json # User-saved flights
└── ratings.json      # Community WiFi ratings
```

## 获取 API 密钥

1. 访问 https://tequila.kiwi.com
2. 注册账户（免费）
3. 获取 API 密钥
4. 在代码中设置：`export KIWI_API_KEY="your_key"`

## 合作计划

- **Kiwi.com**：预订成功后可获得 5% 的佣金
- **合作 ID**：`clawflight`
- 预订链接会自动添加您的合作标识

## 维护工作

- **航空公司数据**：每周更新（由 Samantha 负责）
- **用户评价**：用户通过 `rate` 命令提交评价
- **数据库位置**：`~/clawd/projects/clawflight/data/`

---

*由 Samantha 和 Antoine 开发*
*版本 1.0 — 2026 年 2 月*