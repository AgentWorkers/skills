---
name: luma
description: 从 Luma (lu.ma) 网站获取任意城市的即将举行的活动信息。当用户询问有关技术活动、创业聚会、社交活动、会议或班加罗尔、孟买、德里、旧金山、纽约等城市的最新动态时，可以使用此功能。
version: 1.0.0
author: Clawd
---

# Luma Events Skill

该技能用于从 Luma (lu.ma) 平台获取结构化的事件数据，无需进行身份验证。Luma 是一个专注于技术交流会、创业活动、会议和社区聚会的热门平台。

## 工作原理

Luma 是一个基于 Next.js 的服务器端渲染（SSR）应用程序。所有事件数据都以 JSON 格式嵌入在 HTML 中，位于 `<script id "__NEXT_DATA__">` 标签内。该 Python 脚本可以直接提取这些数据，无需使用 API 密钥。

## 快速入门

```bash
python3 scripts/fetch_events.py bengaluru mumbai --days 14
```

## 使用方法

```bash
python3 scripts/fetch_events.py <city> [cities...] [--days N] [--max N] [--json]
```

### 参数

- **`city`**：城市名称（例如：bengaluru、mumbai、delhi、san-francisco、new-york、london 等）
- **`--days N`**：仅显示过去 N 天内的事件（默认值：30 天）
- **`--max N`**：每个城市显示的事件数量上限（默认值：20 个）
- **`--json`**：以原始 JSON 格式输出数据，而非格式化后的文本

### 常见的城市名称

- **印度**：bengaluru、mumbai、delhi、hyderabad、pune
- **美国**：san-francisco、new-york、austin、seattle、boston
- **全球**：london、singapore、dubai、toronto、sydney

## 输出格式

### 人类可读格式（默认）

```
============================================================
📍 BENGALURU — 5 events
============================================================

🎯 AI Engineers Day with OpenAI
📍 Whitefield, Bengaluru
📅 Jan 31, 2026 10:30 AM IST
👥 OpenAI, Google AI
👤 1411 going
🎫 Available (150 spots)
🔗 https://lu.ma/57tarlkp

🎯 Startup Fundraising Masterclass
📍 Koramangala, Bengaluru
📅 Feb 02, 2026 06:00 PM IST
🟢 Free (50 spots)
🔗 https://lu.ma/startup-funding
```

### JSON 格式输出（使用 `--json` 参数）

```json
[
  {
    "city": "bengaluru",
    "count": 5,
    "events": [
      {
        "event": {
          "name": "AI Engineers Day",
          "start_at": "2026-01-31T05:00:00.000Z",
          "end_at": "2026-01-31T12:30:00.000Z",
          "url": "57tarlkp",
          "geo_address_info": {
            "city": "Bengaluru",
            "address": "Whitefield",
            "full_address": "..."
          }
        },
        "hosts": [{"name": "OpenAI", "linkedin_handle": "/company/openai"}],
        "guest_count": 1411,
        "ticket_info": {
          "is_free": false,
          "is_sold_out": false,
          "spots_remaining": 150
        }
      }
    ]
  }
]
```

## 事件数据持久化

**请将获取到的事件数据保存到 `~/clawd/memory/luma-events.json` 文件中，以便后续使用。**这样您可以：

- 在不重复请求的情况下回答关于事件的问题
- 跟踪用户感兴趣的事件
- 比较不同城市之间的事件
- 了解即将举行的活动安排

**保存数据的时间点**：
- 在获取某个城市的事件数据后
- 将数据与现有数据合并（通过事件 URL 进行匹配）
- 仅保留过去 60 天内的事件
- 为数据添加 `lastFetched` 时间戳

**数据保存格式**：

```json
[
  {
    "city": "bengaluru",
    "name": "AI Engineers Day",
    "start": "2026-01-31T05:00:00.000Z",
    "end": "2026-01-31T12:30:00.000Z",
    "url": "https://lu.ma/57tarlkp",
    "venue": "Whitefield, Bengaluru",
    "hosts": ["OpenAI", "Google AI"],
    "guestCount": 1411,
    "ticketStatus": "available",
    "spotsRemaining": 150,
    "isFree": false,
    "lastFetched": "2026-01-29T12:54:00Z"
  }
]
```

## 常见使用场景

- **查找本周的技术活动**  
- **查询多个城市的 AI 相关活动**  
- **获取某个城市的未来 5 个事件**

## 示例查询

**用户**：“本周末班加罗尔有哪些技术活动？”  
→ 获取班加罗尔未来 7 天内的事件数据，并保存到内存中。

**用户**：“下个月孟买有哪些 AI 相关的交流会？”  
→ 获取孟买未来 30 天内的事件数据，筛选出 AI 相关的活动，并保存到内存中。

**用户**：“比较旧金山和纽约的创业活动。”  
→ 获取这两个城市的相关事件数据，进行对比，并将结果保存到内存中。

## 注意事项

- **无需身份验证**：Luma 的事件页面是公开的。
- **城市名称**：使用小写字母并使用连字符分隔（例如：san-francisco，而非 San Francisco）。
- **限制请求频率**：请合理使用该工具，避免对服务器造成负担。
- **数据更新**：事件数据直接从 HTML 中获取，因此始终是最新的。
- **时区**：事件时间采用事件的本地时区（从 `start_at` 字段中提取）。

## 故障排除

- **“无法找到 __NEXT_DATA__”**：可能是 Luma 的 HTML 结构发生了变化，需要更新脚本。
- **“数据结构异常”**：可能是 JSON 数据的路径发生了变化，请查看最新的 HTML 文件。
- **没有返回事件数据**：可能是输入的城市名称错误，或者该城市没有即将举行的活动。
- **超时错误**：可能是网络问题，请尝试重新连接或检查网络连接。

## 所需依赖库

- Python 3.6 及以上版本（仅需要标准库，无需额外安装第三方包）
- `urllib`、`json`、`re`、`argparse`、`datetime`（均为内置库）

## 更新日志

### v1.0.0（2026-01-29）
- 首次发布
- 支持多个城市
- 提供人类可读格式和 JSON 格式的输出
- 支持按日期筛选事件（`--days` 参数）
- 支持限制每个城市显示的事件数量（`--max` 参数）
- 支持将事件数据保存到内存文件中