---
name: temporal-cortex-datetime
description: >
  **功能说明：**  
  - **时区转换**：能够将时间从一种时区转换为另一种时区。  
  - **自然语言时间解析**：能够解析类似“下周二下午2点”这样的自然语言时间表达，并将其转换为标准的时间格式。  
  - **时长计算**：能够计算两个时间点之间的时长。  
  - **夏令时（DST）处理**：在处理时间时，系统会自动考虑夏令时的影响。  
  - **零配置使用**：无需任何额外的设置，无需调用API或提供任何凭证即可直接使用该工具。  
  **特点：**  
  - **无需额外配置**：无需进行任何复杂的设置或安装过程，即可立即开始使用。  
  - **无需API调用**：完全依赖内置的功能来实现所有功能，无需与外部服务进行交互。  
  - **安全性**：无需输入任何敏感信息（如API密钥或凭证），确保数据安全。  
  **适用场景：**  
  - **项目管理**：用于协调不同地区团队之间的时间安排。  
  - **日常办公**：帮助用户更准确地理解全球各地的时间差异。  
  - **软件开发**：在处理跨时区的数据时非常有用。  
  **示例：**  
  - 将“New York, USA”时区的“2023-03-15 14:00”转换为“北京, China”时区的对应时间。  
  - 解析“Next Tuesday at 2pm”并计算从今天到下周二下午2点的时长。  
  - 计算两个日期之间的工作日时长（考虑夏令时）。
  Convert timezones, resolve natural language times ("next Tuesday at 2pm"), compute durations, and adjust timestamps with DST awareness. Zero-setup — no API calls or credentials needed.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) for the MCP server. No OAuth or credentials needed — all tools are pure computation. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.5.2"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
  openclaw:
    requires:
      bins:
        - npx
---
# 时间上下文与日期时间解析

提供了5种用于时间定位和日期时间计算的工具。这些工具仅执行纯计算操作（不调用任何外部API），均为只读功能，并且具有幂等性（多次调用结果相同）。使用这些工具无需OAuth认证或日历凭证。

## 工具列表

| 工具 | 使用场景 |
|------|------------|
| `get_temporal_context` | 在任何会话中首次调用时使用。返回当前时间、时区、UTC偏移量、夏令时状态以及夏令时的预测信息。 |
| `resolve_datetime` | 将人类可读的时间表达式转换为RFC 3339格式。支持60多种时间表达式模式，例如：“下周二下午2点”、“明天早上”、“+2小时”、“下周开始”等。 |
| `convert_timezone` | 在IANA时区之间转换RFC 3339格式的日期时间。 |
| `compute_duration` | 计算两个时间戳之间的时间间隔（以天、小时、分钟为单位）。 |
| `adjust_timestamp` | 考虑夏令时的时间戳调整。例如，“+1d”表示将时间向前推进1天（保持时钟显示的时间不变）。 |

## 重要规则

1. **在进行任何依赖时间的信息处理之前，务必先调用`get_temporal_context`**——切勿直接使用默认的时间或时区设置。 |
2. **在查询之前进行转换**——在将时间表达式传递给日历相关工具之前，使用`resolve_datetime`将其转换为RFC 3339格式。 |
3. **时区意识**——所有日期时间处理工具都会返回包含时区偏移量的RFC 3339格式的结果。 |

## `resolve_datetime`的时间表达式模式

该工具支持60多种时间表达式模式，分为10个类别：

| 类别 | 示例 |
|----------|---------|
| 相对时间 | `now`（现在）、`today`（今天）、`tomorrow`（明天）、`yesterday`（昨天） |
| 命名日期 | `next Monday`（下周一）、`this Friday`（本周五）、`last Wednesday`（上周三） |
| 一天中的时间 | `morning`（09:00）、`noon`（12:00）、`evening`（18:00）、`eob`（17:00） |
| 时钟时间 | `2pm`（下午2点）、`14:00`（14:00）、`3:30pm`（下午3:30） |
| 时间偏移量 | `+2h`（提前2小时）、`-30m`（延迟30分钟）、`in 2 hours`（2小时后） |
| 复合时间表达式 | `next Tuesday at 2pm`（下周二下午2点）、`tomorrow morning`（明天早上）、`this Friday at noon`（本周五中午） |
| 时间段边界 | `start of week`（一周的开始）、`end of month`（月底）、`start of next week`（下周开始）、`end of last month`（上个月底） |
| 周几的顺序表示 | `first Monday of March`（三月的第一个周一）、`third Friday of next month`（下个月的第三个周五） |
| 直接使用RFC 3339格式 | `2026-03-15T14:00:00-04:00`（原样返回） |
| 考虑周起始日 | 使用配置的`WEEK_START`参数（默认为周一，也可设置为周日） |

## 常见使用场景

### 获取当前时间上下文
```
get_temporal_context()
→ utc, local, timezone, utc_offset, dst_active, dst_next_transition,
  day_of_week, iso_week, is_weekday, day_of_year, week_start
```

### 解析会议时间
```
resolve_datetime("next Tuesday at 2pm")
→ resolved_utc, resolved_local, timezone, interpretation
```

### 在不同时区之间进行转换
```
1. get_temporal_context → user's timezone
2. convert_timezone(datetime: "2026-03-15T14:00:00-04:00", target_timezone: "Asia/Tokyo")
   → same moment in Tokyo time with DST and offset info
```

### 计算时间间隔
```
compute_duration(start: "2026-03-15T09:00:00-04:00", end: "2026-03-15T17:30:00-04:00")
→ total_seconds: 30600, hours: 8, minutes: 30, human_readable: "8 hours 30 minutes"
```

### 考虑夏令时的时间调整
```
adjust_timestamp(
  datetime: "2026-03-07T23:00:00-05:00",
  adjustment: "+1d",
  timezone: "America/New_York"
) → same wall-clock time (23:00) on March 8, even though DST spring-forward occurs
```

## 额外参考资料

- [日期时间工具参考](references/DATETIME-TOOLS.md) — 提供了这5个工具的完整输入/输出格式说明。