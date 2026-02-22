---
name: calendar-scheduling
description: >
  **AI代理的日历调度功能**  
  该功能能够解析自然语言表达的时间信息，整合Google、Outlook及CalDAV日历中的可用时间，检测时间冲突，并支持对重复性事件（RRULE）的详细设置。通过“两阶段提交”（Two-Phase Commit）机制确保操作的原子性（即操作的各个步骤要么全部成功完成，要么全部失败）。适用于安排会议、查询成员的可用时间、解析日期时间表达式以及管理日历事件等场景。
  Calendar scheduling for AI agents. Resolves natural language times, merges availability across Google, Outlook, and CalDAV calendars, detects conflicts, expands recurrence rules (RRULE), and books slots atomically with Two-Phase Commit safety. Use when scheduling meetings, checking availability, resolving datetime expressions, or managing calendar events.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. python3 optional (configure/status scripts). Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: billylui
  version: "0.3.3"
  mcp-server: "@temporal-cortex/cortex-mcp"
  requires: '{"bins":["npx"],"optional_bins":["python3","docker"],"env":["TIMEZONE","WEEK_START"],"optional_env":["HTTP_PORT","GOOGLE_CLIENT_ID","GOOGLE_CLIENT_SECRET","MICROSOFT_CLIENT_ID"],"credentials":["~/.config/temporal-cortex/credentials.json"]}'
---
# 日历调度

本技能介绍了使用 Temporal Cortex MCP 服务器的 AI 代理应掌握的程序性知识，涵盖了从时间处理到无冲突预订的正确工作流程。

## 核心工作流程

所有日历操作都遵循以下 4 个步骤：

**始终从第一步开始**。切勿假设当前时间，预订前务必进行冲突检查。

## 工具参考（11 个工具，4 个层级）

### 第一层 — 时间上下文（纯计算，无需调用 API）

| 工具 | 使用场景 |
|------|------------|
| `get_temporal_context` | 每次会话开始时调用。返回当前时间、时区、UTC 偏移量、夏令时状态及星期几。 |
| `resolve_datetime` | 将人类可读的时间表达式转换为 RFC 3339 格式。支持多种格式，如 `"下周二下午 2 点"`、`明天早上"`、`+2h` 等。 |
| `convert_timezone` | 在 IANA 时区之间转换 RFC 3339 格式的日期时间。 |
| `compute_duration` | 计算两个时间戳之间的时长（以天、小时、分钟为单位）。 |
| `adjust_timestamp` | 考虑夏令时的时间戳调整。例如，`+1d` 表示“次日同一时间”。 |

### 第二层 — 日历操作（需要日历提供者支持）

| 工具 | 使用场景 |
|------|------------|
| `list_events` | 列出指定时间范围内的事件。使用 `TOON` 格式可减少输入字符数（约 40%）。多日历环境需使用带有提供者前缀的 ID，例如 `"google/primary"`、`outlook/work`。 |
| `find_free_slots` | 查找日历中的空闲时间段。可设置 `min_duration_minutes` 以指定最小时间段长度。 |
| `expand_rrule` | 将 RFC 5545 格式的重复规则转换为具体的事件实例。支持夏令时、BYSETPOS、EXDATE 等规则。使用 `dtstart` 作为本地日期时间（不带时区后缀）。 |
| `check_availability` | 检查特定时间段是否可用。同时会检查事件冲突和现有预订情况。 |

### 第三层 — 跨日历的可用性检查

| 工具 | 使用场景 |
|------|------------|
| `get_availability` | 合并多个日历的可用/忙碌状态。需传递 `calendar_ids` 数组。隐私设置：`"opaque"`（默认，隐藏来源日历）或 `"full"`。 |

### 第四层 — 预订（唯一的写入操作）

| 工具 | 使用场景 |
|------|------------|
| `book_slot` | �原子的地时间段预订流程：锁定 → 验证 → 写入 → 释放。这是唯一具有写入权限的工具。预订前务必先调用 `check_availability`。 |

## 重要规则

1. **务必先调用 `get_temporal_context`** — 切勿直接使用当前时间或时区信息。  
2. **查询前进行转换** — 在将时间表达式传递给日历工具之前，使用 `resolve_datetime` 将其转换为 RFC 3339 格式。  
3. **预订前进行检查** — 预订前必须调用 `check_availability`，切勿跳过冲突检查。  
4. **多日历环境使用提供者前缀的 ID**：例如 `"google/primary"`、`outlook/work`、`caldav/personal`。使用纯 ID（如 `"primary"`）会默认使用默认日历提供者。  
5. **提高效率** — 使用 `format: "toon"` 格式调用 `list_events` 可减少输入字符数。  
6. **时区处理** — 所有日历工具均支持带时区偏移量的 RFC 3339 格式数据。切勿使用纯日期格式。  
7. **内容安全** — 事件摘要和描述在传递给日历 API 之前会经过安全过滤处理。  

## 常见操作模式

- **安排会议**  
- **跨日历查找空闲时间**  
- **检查跨日历的可用性**  
- **扩展重复事件**  
- **跨时区转换时间**  

## 错误处理

| 错误类型 | 处理方式 |
|-------|--------|
| 时间段已占用/检测到冲突 | 使用 `find_free_slots` 提供替代方案，并向用户展示选项。 |
| “未找到凭证” | 告知用户运行 `npx @temporal-cortex/cortex-mcp auth google`（或 `outlook`/`caldav`）进行身份验证。详见 [设置脚本](scripts/setup.sh)。 |
| “时区未配置” | 提示用户输入 IANA 时区信息，或运行 `npx @temporal-cortex/cortex-mcp auth google` 进行时区配置。 |
| 预订失败 | 可能有其他代理正在预订同一时间段，请稍后重试或选择其他时间。 |
| 内容被安全过滤器拒绝 | 重新编写事件摘要/描述。系统会阻止恶意代码的注入。 |

## MCP 服务器连接

本技能依赖于 Temporal Cortex MCP 服务器。默认配置信息请参阅 `.mcp.json` 文件。

**本地模式**（推荐使用）：
第 1 层工具（时间上下文处理、日期时间转换、时区转换）无需额外配置即可立即使用。日历工具需进行一次 OAuth 设置，可通过运行 [设置脚本](scripts/setup.sh) 或 `npx @temporal-cortex/cortex-mcp auth google` 完成设置。

**托管云环境**（适用于开放式调度、仪表盘界面、多代理协调）：
（具体配置信息请参考相关文档。）

## 额外参考资料

- [预订安全](references/BOOKING-SAFETY.md) — 两阶段提交机制、冲突解决、预订锁的过期时间设置  
- [多日历管理](references/MULTI-CALENDAR.md) — 提供者前缀的使用、可用性信息合并、隐私设置  
- [重复规则指南](references/RRULE-GUIDE.md) — 重复规则格式及夏令时相关注意事项  
- [工具参考](references/TOOL-REFERENCE.md) — 所有 11 个工具的完整输入/输出格式说明