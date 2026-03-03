---
name: clawevents
description: >
  **多城市活动查询功能**  
  支持查询特拉维夫（Tel Aviv）、巴塞罗那（Barcelona）和纽约（New York）的城市活动。可搜索音乐会、爵士乐演出、电影院、剧院演出、夜生活活动、家庭活动、喜剧表演、艺术展览以及各类节日活动。  
  提供按年龄组（儿童/家庭/成人）、时间段（上午/下午/晚上/深夜）、日期范围以及是否免费进行筛选的功能。  
  系统会从多个信息源中检索相关活动，并返回经过排序、去重后的结果。
version: 0.1.0
homepage: https://github.com/yhyatt/clawevents
metadata: {"kai": {"emoji": "🎉", "category": "lifestyle", "cities": ["tel-aviv", "barcelona", "new-york"]}}
---
# ClawEvents 🎉

支持多城市事件查询——特拉维夫、巴塞罗那、纽约。

## 使用场景

- “这个周末特拉维夫有什么活动？”
- “下周巴塞罗那有哪些爵士音乐会？”
- “今晚特拉维夫有哪些电影放映？”
- “本周六纽约有哪些免费的家庭活动？”
- “为团队旅行查询特拉维夫和巴塞罗那的活动”
- “Lev Cinema本周的放映安排”
- “纽约有哪些仅限成人的现场音乐活动？”

## 命令行接口（CLI）使用方法

```bash
# Basic search
python3 -m clawevents search --city tel-aviv --days 7

# Jazz in Tel Aviv this week
python3 -m clawevents search --city tel-aviv --type jazz --days 7

# Cinema tonight (Lev + others)
python3 -m clawevents search --city tel-aviv --type cinema --days 1

# Multi-city: what's on in Barcelona and NYC this weekend
python3 -m clawevents search --city barcelona new-york --days 3

# Family events, free, afternoon
python3 -m clawevents search --city tel-aviv --type family --age family --time afternoon --free

# Concert, adults, evening, specific dates
python3 -m clawevents search --city tel-aviv barcelona --type concert --age adults --time evening --from 2026-06-21 --to 2026-06-27

# JSON output (for programmatic use)
python3 -m clawevents search --city new-york --type jazz --format json --limit 10
```

## 支持的城市

| 城市 | 别名 | 数据来源 |
|------|-------|---------|
| 特拉维夫 | `tel-aviv`, `tlv` | TLV市政厅API、Eventbrite、Lev Cinema |
| 巴塞罗那 | `barcelona`, `bcn` | Ticketmaster、Eventbrite |
| 纽约 | `new-york`, `nyc` | Ticketmaster、Eventbrite、NYC开放数据 |

## 事件类型

- 爵士乐（jazz） | 音乐会（concert） | 电影（cinema） | 戏剧（theatre） | 夜生活（nightlife） | 家庭活动（family） | 儿童活动（kids） | 喜剧（comedy） | 艺术活动（art） | 体育活动（sport） | 节日活动（festival） | 社区活动（community） |

## 过滤条件

| 参数 | 可选值 | 默认值 |
|------|--------|---------|
| --type | jazz, concert, cinema, theatre, ... | 全部（all） |
| --age | kids, family, adults | 全部（all） |
| --time | morning, afternoon, evening, late-night | 全部（all） |
| --from | --to | YYYY-MM-DD | 今天（today）/ +7天（+7d） |
| --days | 整数 | 7 | |
| --free | 是否免费（flag） | 否（false） |
| --limit | 整数 | 20 | |
| --format | text | json | text |

## 配置说明

### 安装依赖项
```bash
cd skills/clawevents
pip3 install -r requirements.txt
```

### API密钥（推荐使用，但非强制）

| 密钥 | 来源 | 可查询的城市 |
|-----|--------|-----------------|
| `TICKETMASTER_API_KEY` | [developer.ticketmaster.com](https://developer.ticketmaster.com) | 免费 | 巴塞罗那、纽约 |
| `EVENTBRITE_TOKEN` | [eventbrite.com/platform/api](https://www.eventbrite.com/platform/api) | 免费 | 所有城市 |
| `TLV_API_KEY` | [apiportal.tel-aviv.gov.il](https://apiportal.tel-aviv.gov.il) | 免费 | 特拉维夫的官方活动 |

**注：** 未使用API密钥时：  
- 特拉维夫的数据来自TLV市政厅网站；  
- 巴塞罗那和纽约的数据仅使用Eventbrite的免费服务及NYC开放数据。

**将以下代码添加到`~/.zshrc`或`~/.bashrc`文件中：**  
```bash
export TICKETMASTER_API_KEY="your_key"
export EVENTBRITE_TOKEN="your_token"
export TLV_API_KEY="your_key"         # optional
```

## 数据来源

### 特拉维夫  
- **TLV市政厅API**：官方城市活动数据（来源：DigiTel）。使用API密钥可免费访问。  
- **Eventbrite**：科技、社区、文化活动数据。  
- **Lev Cinema**：Dizengoff影院的活动信息（通过网页抓取获取）。  
- **计划中**：使用Time Out Israel工具获取更多爵士乐、俱乐部和剧院活动信息。

### 巴塞罗那  
- **Ticketmaster Discovery API**：音乐会、剧院、体育活动数据（超过23万条记录）。  
- **Eventbrite**：社区和文化活动数据。  
- **计划中**：使用Fever/Xceed工具获取更多夜生活和俱乐部活动信息。

### 纽约  
- **Ticketmaster Discovery API**：音乐会、百老汇演出、体育活动数据。  
- **Eventbrite**：社区活动数据。  
- **NYC开放数据**：免费公园活动及城市活动信息。

## 系统架构

```
ClawEventsEngine
├── Fetchers (parallel, per-city)
│   ├── TLVMunicipalityFetcher  → Tel Aviv
│   ├── TicketmasterFetcher     → Barcelona, NYC
│   ├── EventbriteFetcher       → All cities
│   ├── LevCinemaFetcher        → Tel Aviv (cinema)
│   └── NYCOpenDataFetcher      → NYC (free events)
├── Filter layer  (types, age, time-of-day, date, free)
├── Dedup layer   (same title + time across sources)
└── Rank layer    (chronological, no-time events last)
```

## 扩展功能

如需添加新城市或数据来源：  
1. 创建`clawevents/fetchers/your_source.py`文件，实现`BaseFetcher`接口。  
2. 在`engine.py`文件中注册该抓取器及其对应的城市别名。  
3. 在`cli.py`文件中更新城市列表。