---
name: calendar-scheduling
description: >
  **AI代理的日历调度功能**  
  该功能能够处理自然语言时间表达，整合Google、Outlook及CalDAV日历中的可用时间信息，检测时间冲突，并支持递归规则（RRULE）的扩展应用。通过两阶段提交（Two-Phase Commit）机制确保操作的原子性（即操作的各个步骤要么全部成功完成，要么全部失败）。适用于安排会议、查询可用时间、解析日期时间表达式以及管理日历事件等场景。
  Calendar scheduling for AI agents. Resolves natural language times, merges availability across Google, Outlook, and CalDAV calendars, detects conflicts, expands recurrence rules (RRULE), and books slots atomically with Two-Phase Commit safety. Use when scheduling meetings, checking availability, resolving datetime expressions, or managing calendar events.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. python3 optional (configure/status scripts). Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: billylui
  version: "0.3.4"
  mcp-server: "@temporal-cortex/cortex-mcp"
  requires: '{"bins":["npx"],"optional_bins":["python3","docker"],"env":["TIMEZONE","WEEK_START"],"optional_env":["HTTP_PORT","GOOGLE_CLIENT_ID","GOOGLE_CLIENT_SECRET","MICROSOFT_CLIENT_ID","MICROSOFT_CLIENT_SECRET","GOOGLE_OAUTH_CREDENTIALS","TEMPORAL_CORTEX_TELEMETRY"],"credentials":["~/.config/temporal-cortex/credentials.json","~/.config/temporal-cortex/config.json"]}'
---
# 日历调度

本技能介绍了使用 Temporal Cortex MCP 服务器的 AI 代理应掌握的流程知识，涵盖了从时间理解到无冲突预订的正确操作流程。

## 核心工作流程

所有日历操作都遵循以下 4 个步骤：

**始终从第 1 步开始**。切勿假设当前时间，预订前务必进行冲突检查。

## 工具参考（11 个工具，4 个层级）

### 第 1 层——时间上下文（纯计算，无需调用 API）

| 工具 | 使用场景 |
|------|------------|
| `get_temporal_context` | 每次会话开始时调用。返回当前时间、时区、UTC 偏移量、夏令时状态及星期几。 |
| `resolve_datetime` | 将人类可读的时间表达式转换为 RFC 3339 格式。支持多种格式，例如：“下周二下午 2 点”、“明天早上”、“+2 小时”、“下周开始”等。 |
| `convert_timezone` | 在 IANA 时区之间转换 RFC 3339 格式的日期时间。 |
| `compute_duration` | 计算两个时间戳之间的时长（以天、小时、分钟为单位）。 |
| `adjust_timestamp` | 考虑夏令时的时间戳调整。例如，“+1d”表示进入夏令期后的同一时间。 |

### 第 2 层——日历操作（需要日历提供者支持）

| 工具 | 使用场景 |
|------|------------|
| `list_events` | 列出指定时间范围内的事件。支持 TOON 格式（可节省约 40% 的输入字符数）。对于多个日历，使用带有提供者前缀的 ID，例如：“google/primary”、“outlook/work”。 |
| `find_free_slots` | 查找日历中的空闲时间段。可设置 `min_duration_minutes` 以指定最小时间段长度。 |
| `expand_rrule` | 将 RFC 5545 格式的重复事件规则转换为具体的事件实例。支持夏令时、BYSETPOS、EXDATE 等规则。使用 `dtstart` 作为本地日期时间（不包含时区后缀）。 |
| `check_availability` | 检查特定时间段是否可用。同时会检查事件安排和现有预订情况。 |

### 第 3 层——跨日历的可用性检查

| 工具 | 使用场景 |
|------|------------|
| `get_availability` | 合并多个日历的可用/忙碌状态。传入 `calendar_ids` 数组。隐私设置：默认为 “opaque”（隐藏来源信息），也可设置为 “full”。 |

### 第 4 层——预订（唯一的写入操作）

| 工具 | 使用场景 |
|------|------------|
| `book_slot` | �原子的地时间段预订流程：锁定 → 验证 → 写入 → 释放。这是唯一一个具有写入权限的工具。预订前务必先调用 `check_availability`。 |

## 重要规则

1. **务必先调用 `get_temporal_context`**——切勿直接使用当前时间或时区信息。
2. **查询前先转换时间**——在将时间表达式传递给日历工具之前，使用 `resolve_datetime` 将其转换为 RFC 3339 格式。
3. **预订前务必检查**——在调用 `book_slot` 之前，务必先调用 `check_availability` 以确认时间段是否可用。
4. **使用带有提供者前缀的 ID**——在处理多个日历时，使用如 “google/primary”、“outlook/work”、“caldav/personal” 等前缀。使用纯 ID（如 “primary”）会默认使用默认日历提供者。
5. **提高效率**——使用 `format: "toon"` 格式调用 `list_events` 可节省输入字符数。
6. **注意时区**——所有日历工具都支持带有时区偏移量的 RFC 3339 格式。切勿使用纯日期格式。
7. **内容安全**——事件摘要和描述在传递给日历 API 之前会经过安全过滤处理。

## 常见操作模式

- **安排会议**
- **查找多个日历中的空闲时间**
- **检查跨日历的可用性**
- **扩展重复事件**
- **跨时区转换时间**

## 错误处理

| 错误类型 | 处理方式 |
|-------|--------|
| 时间段已被占用/检测到冲突 | 使用 `find_free_slots` 提供替代时间段，并向用户展示选项。 |
| “未找到凭证” | 告知用户运行命令：`npx @temporal-cortex/cortex-mcp auth google`（或 `outlook`/`caldav`）。请参阅 [设置脚本](scripts/setup.sh)。 |
| “时区未配置” | 提示用户输入他们的 IANA 时区，或运行 `npx @temporal-cortex/cortex-mcp auth google` 进行时区配置。 |
| 预订失败 | 可能有其他代理正在预订同一时间段。稍后重试或建议其他时间。 |
| 内容被安全过滤器拒绝 | 重新编写事件摘要/描述。防火墙会阻止恶意代码的插入。 |

## MCP 服务器连接

本技能需要 Temporal Cortex MCP 服务器。默认配置信息请参见 `.mcp.json` 文件。

**本地模式**（默认推荐）：
第 1 层工具（时间上下文处理、日期时间转换、时区转换）无需额外配置即可立即使用。日历工具需要一次性 OAuth 设置——请运行 [设置脚本](scripts/setup.sh) 或 `npx @temporal-cortex/cortex-mcp auth google`。

**托管云环境**（适用于开放式调度、仪表盘界面、多代理协调）：
（具体配置信息请参考相关文档。）

## 其他参考资料

- [预订安全](references/BOOKING-SAFETY.md)——两阶段提交、冲突解决机制、预订锁的过期时间设置
- [多日历管理](references/MULTI-CALENDAR.md)——使用提供者前缀的 ID、可用性合并、隐私设置
- [重复事件规则指南](references/RRULE-GUIDE.md)——重复事件规则的格式与注意事项
- [工具参考](references/TOOL-REFERENCE.md)——所有 11 个工具的完整输入/输出格式说明