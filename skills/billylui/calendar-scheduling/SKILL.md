---
name: calendar-scheduling
description: 安排会议、查看他人日程安排，并在 Google、Outlook 和 CalDAV 之间管理日历事件。能够自动处理自然语言表达的时间和时区信息，找到空闲时间、检测时间冲突，支持重复事件的设置，并在安排会议时避免时间冲突。适用于寻找空闲时间、预约会议、查看他人忙碌情况或在不同时区之间转换时间时使用。
  Schedule meetings, check availability, and manage calendar events across Google, Outlook, and CalDAV. Resolves natural language times and timezones, finds free slots, detects conflicts, expands recurring events, and books with conflict prevention. Use when finding free time, scheduling appointments, checking who is busy, or converting between timezones.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. python3 optional (configure/status scripts). Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: billylui
  version: "0.5.0"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/billylui/temporal-cortex-skill"
  requires: '{"bins":["npx"],"optional_bins":["python3","docker"],"optional_env":["TIMEZONE","WEEK_START","HTTP_PORT","GOOGLE_CLIENT_ID","GOOGLE_CLIENT_SECRET","MICROSOFT_CLIENT_ID","MICROSOFT_CLIENT_SECRET","GOOGLE_OAUTH_CREDENTIALS","TEMPORAL_CORTEX_TELEMETRY"],"credentials":["~/.config/temporal-cortex/credentials.json","~/.config/temporal-cortex/config.json"]}'
  openclaw:
    requires:
      bins:
        - npx
      anyBins:
        - python3
        - docker
      config:
        - ~/.config/temporal-cortex/credentials.json
        - ~/.config/temporal-cortex/config.json
---
# 日历调度

本技能介绍了使用 Temporal Cortex MCP 服务器的 AI 代理应掌握的程序性知识，涵盖了从时间定位到无冲突预订的整个日历操作工作流程。

## 核心工作流程

所有日历交互都遵循以下 5 个步骤：

**在不知道哪些日历可用时，务必从第一步开始操作**。切勿假设当前时间，也绝不要在预订前跳过冲突检查。

## 工具参考（12 个工具，5 个层级）

### 第 0 层 — 发现（查找连接的日历）

| 工具 | 使用场景 |
|------|------------|
| `list_calendars` | 在不知道日历信息时首次调用。返回所有连接的日历，包括提供商前缀的 ID、名称、标签、主要状态和访问权限。 |

### 第 1 层 — 时间上下文（纯计算，无需调用 API）

| 工具 | 使用场景 |
|------|------------|
| `get_temporal_context` | 每次会话开始时首次调用。返回当前时间、时区、UTC 偏移量、夏令时状态及夏令时预测信息。 |
| `resolve_datetime` | 将人类可读的时间表达式转换为 RFC 3339 格式。支持多种格式，例如：“下周二下午 2 点”、“明天早上”、“+2 小时”、“下周开始”等。 |
| `convert_timezone` | 在不同的 IANA 时区之间转换 RFC 3339 格式的日期时间。 |
| `compute_duration` | 计算两个时间戳之间的时长（以天、小时、分钟为单位）。 |
| `adjust_timestamp` | 考虑夏令时的时间戳调整。例如，“+1d”表示进入夏令时后的时间。 |

### 第 2 层 — 日历操作（需要日历提供商的支持）

| 工具 | 使用场景 |
|------|------------|
| `list_events` | 列出指定时间范围内的事件。默认使用 TOON 格式（相比 JSON 格式节省约 40% 的数据量）。在处理多个日历时，使用提供商前缀的 ID，例如：“google/primary”、“outlook/work”。 |
| `find_free_slots` | 查找日历中的可用时间段。可设置 `min_duration_minutes` 参数来指定最小时间段长度。支持 `format` 参数。 |
| `expand_rrule` | 将 RFC 5545 格式的重复规则解析为具体的事件实例。支持处理夏令时、BYSETPOS、EXDATE 等特殊情况。使用 `dtstart` 参数指定事件开始时间（不包含时区后缀）。支持 `format` 参数。 |
| `check_availability` | 检查特定时间段是否可用。会同时检查事件安排和现有的预订情况。 |

### 第 3 层 — 跨日历的可用性检查

| 工具 | 使用场景 |
|------|------------|
| `get_availability` | 合并多个日历的可用/忙碌状态信息。需要传递 `calendar_ids` 数组。隐私设置：默认为 “opaque”（隐藏来源日历），也可设置为 “full”。支持 `format` 参数。 |

### 第 4 层 — 预订（唯一的写入操作）

| 工具 | 使用场景 |
|------|------------|
| `book_slot` | 原子级地预订一个时间段。操作流程包括锁定、验证、写入和释放。这是唯一一个具有写入权限的工具。在预订前务必先调用 `check_availability`。 |

## 重要规则

1. **先发现日历**：在不知道哪些日历可用时，先调用 `list_calendars`，并使用返回的提供商前缀 ID 进行后续操作。
2. **在涉及时间依赖的操作前，务必调用 `get_temporal_context`**：切勿假设当前时间或时区。
3. **查询前进行转换**：在将时间表达式传递给日历工具之前，使用 `resolve_datetime` 将其转换为 RFC 3339 格式。
4. **预订前务必检查**：在调用 `book_slot` 之前，务必先调用 `check_availability`，切勿跳过冲突检查。
5. **在处理多个日历时，使用提供商前缀的 ID**：例如 “google/primary”、“outlook/work”、“caldav/personal”。使用纯 ID（如 “primary”）时，系统会使用默认的日历提供商。
6. **默认使用 TOON 格式**：输出结果采用 TOON 格式（相比 JSON 更节省数据量）。只有在需要结构化解析时才使用 `format: "json"`。
7. **注意时区设置**：所有日历工具都支持带有时区偏移量的 RFC 3339 格式的数据。切勿使用纯日期格式。
8. **内容安全**：事件摘要和描述在传递给日历 API 之前会经过安全过滤处理。

## 常见操作模式

- **安排会议**  
- **查找多个日历中的空闲时间**  
- **检查跨日历的可用性**  
- **扩展重复事件**  
- **在不同时区之间转换时间**  

## 错误处理

| 错误类型 | 处理方式 |
|--------|--------|
| 时间段已被占用或存在冲突 | 使用 `find_free_slots` 提供替代方案，并向用户展示选项。 |
| 未找到凭证 | 告知用户执行命令：`npx @temporal-cortex/cortex-mcp auth google`（或 `outlook`/`caldav`）。请参考 [设置脚本](scripts/setup.sh)。 |
| 时区未配置 | 提示用户输入他们的 IANA 时区信息，或执行 `npx @temporal-cortex/cortex-mcp auth google` 进行时区配置。 |
| 预订失败 | 可能有其他代理正在预订同一时间段。稍后重试或建议其他时间。 |
| 内容被安全过滤器拒绝 | 重新编写事件摘要或描述。系统会阻止恶意内容的插入。 |

## MCP 服务器连接

本技能需要 Temporal Cortex MCP 服务器的配合。默认配置信息请参见 `.mcp.json` 文件。

**本地模式**（推荐使用）：
第 1 层工具（时间上下文处理、日期时间转换、时区转换）无需额外配置即可立即使用。日历工具需要一次性完成 OAuth 设置——运行 [设置脚本](scripts/setup.sh) 或执行 `npx @temporal-cortex/cortex-mcp auth google`。

**托管云模式**（无需本地设置）：
在 https://app.temporal-cortex.com 注册，以获取带有承载令牌认证功能的托管 MCP 端点。使用云端的 URL 配置客户端，所有 12 个工具均可正常使用，同时支持开放调度、仪表盘界面和多代理协调功能。

## 其他参考资料

- [预订安全](references/BOOKING-SAFETY.md)：两阶段提交机制、冲突解决、预订锁定的有效期  
- [多日历管理](references/MULTI-CALENDAR.md)：提供商前缀 ID 的使用、可用性信息的合并、隐私设置  
- [重复规则指南](references/RRULE-GUIDE.md)：重复规则的模式及夏令时的特殊处理  
- [工具参考](references/TOOL-REFERENCE.md)：所有 12 个工具的完整输入/输出格式规范