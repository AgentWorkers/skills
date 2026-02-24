---
name: calendar-scheduling
description: AI代理的日历调度功能：能够解析自然语言中的时间信息，整合Google、Outlook和CalDAV日历中的可用时间，检测时间冲突，扩展重复规则（RRULE），并采用两阶段提交（Two-Phase Commit）机制确保操作的原子性（即操作的各个步骤要么全部成功完成，要么全部失败）。适用于安排会议、查询可用时间、解析日期时间表达式或管理日历事件等场景。
  Calendar scheduling for AI agents. Resolves natural language times, merges availability across Google, Outlook, and CalDAV calendars, detects conflicts, expands recurrence rules (RRULE), and books slots atomically with Two-Phase Commit safety. Use when scheduling meetings, checking availability, resolving datetime expressions, or managing calendar events.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. python3 optional (configure/status scripts). Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: billylui
  version: "0.4.1"
  mcp-server: "@temporal-cortex/cortex-mcp"
  requires: '{"bins":["npx"],"optional_bins":["python3","docker"],"env":["TIMEZONE","WEEK_START"],"optional_env":["HTTP_PORT","GOOGLE_CLIENT_ID","GOOGLE_CLIENT_SECRET","MICROSOFT_CLIENT_ID","MICROSOFT_CLIENT_SECRET","GOOGLE_OAUTH_CREDENTIALS","TEMPORAL_CORTEX_TELEMETRY"],"credentials":["~/.config/temporal-cortex/credentials.json","~/.config/temporal-cortex/config.json"]}'
  openclaw:
    requires:
      bins:
        - npx
      anyBins:
        - python3
        - docker
      env:
        - TIMEZONE
        - WEEK_START
      config:
        - ~/.config/temporal-cortex/credentials.json
        - ~/.config/temporal-cortex/config.json
    primaryEnv: TIMEZONE
---
# 日历调度

本技能涵盖了使用 Temporal Cortex MCP 服务器的 AI 代理应掌握的程序性知识，主要介绍了正确的日历操作工作流程，包括时间定位以及无冲突的预订流程。

## 核心工作流程

所有的日历交互都遵循以下 4 个步骤：

**始终从第一步开始。** 不要假设当前时间；在预订之前务必进行冲突检查。

## 工具参考（11 个工具，4 个层级）

### 第一层——时间上下文（纯计算，无需调用 API）

| 工具 | 使用场景 |
|------|------------|
| `get_temporal_context` | 每个会话开始时调用。返回当前时间、时区、UTC 偏移量、夏令时状态和星期几。 |
| `resolve_datetime` | 将人类可读的时间表达式转换为 RFC 3339 格式。支持多种表达方式，例如：“下周二下午 2 点”、“明天早上”、“+2 小时”、“下周开始”等。 |
| `convert_timezone` | 在 IANA 时区之间转换 RFC 3339 格式的日期时间。 |
| `compute_duration` | 计算两个时间戳之间的时长（以天、小时、分钟为单位）。 |
| `adjust_timestamp` | 考虑夏令时的时间戳调整。例如，“+1d”表示跨过夏令时调整后的实际时间。 |

### 第二层——日历操作（需要日历提供者支持）

| 工具 | 使用场景 |
|------|------------|
| `list_events` | 列出指定时间范围内的事件。支持 TOON 格式（可节省约 40% 的输入字符数量）。对于多日历环境，使用带有提供者前缀的 ID，例如：“google/primary”、“outlook/work”。 |
| `find_free_slots` | 查找日历中的空闲时间段。需要设置 `min_duration_minutes` 以指定最小时间段长度。 |
| `expand_rrule` | 将 RFC 5545 格式的重复规则解析为具体的事件实例。支持夏令时、BYSETPOS、EXDATE 等规则。使用 `dtstart` 作为本地日期时间（不包含时区后缀）。 |
| `check_availability` | 检查特定时间段是否可用。同时会检查已有事件和预订情况。 |

### 第三层——跨日历的可用性检查

| 工具 | 使用场景 |
|------|------------|
| `get_availability` | 合并多个日历的可用/忙碌状态信息。需要传入 `calendar_ids` 数组。隐私设置：默认为 “opaque”（隐藏来源信息），也可设置为 “full”。 |

### 第四层——预订（唯一的写入操作）

| 工具 | 使用场景 |
|------|------------|
| `book_slot` | �原子的地长时间段预订流程：锁定 → 验证 → 写入 → 释放。这是唯一一个具有写入权限的工具。务必先调用 `check_availability`。 |

## 重要规则

1. **务必先调用 `get_temporal_context`**——不要随意假设时间或时区信息。
2. **查询前先进行转换**——在将时间表达式传递给日历工具之前，使用 `resolve_datetime` 将其转换为 RFC 3339 格式。
3. **预订前务必检查**——在调用 `book_slot` 之前，务必先调用 `check_availability`。
4. **多日历环境使用提供者前缀的 ID**：例如 “google/primary”、“outlook/work”、“caldav/personal”。使用纯 ID（如 “primary”）时，系统会使用默认提供者。
5. **提高效率**——使用 `format: "toon"` 格式调用 `list_events` 可节省输入字符数量。
6. **时区处理**——所有日历工具都支持带有时区偏移量的 RFC 3339 格式；切勿使用纯日期格式。
7. **内容安全**——事件摘要和描述在传递给日历 API 之前会经过安全过滤处理。

## 常见操作模式

- **安排会议**  
- **跨日历查找空闲时间**  
- **检查跨日历的可用性**  
- **扩展重复事件**  
- **跨时区转换时间**  

## 错误处理

| 错误类型 | 处理方式 |
|-------|--------|
| 时间段已被占用/检测到冲突 | 使用 `find_free_slots` 提供替代方案，并向用户展示选项。 |
| 未找到凭证 | 告知用户运行命令：`npx @temporal-cortex/cortex-mcp auth google`（或 `outlook`/`caldav`）。请参考 [设置脚本](scripts/setup.sh)。 |
| 时区未配置 | 提示用户输入其 IANA 时区信息；或运行 `npx @temporal-cortex/cortex-mcp auth google` 进行时区配置。 |
| 预订失败 | 可能有其他代理正在预订同一时间段，请稍后重试或建议其他时间。 |
| 内容被安全过滤器拒绝 | 重新编写事件摘要/描述；系统会阻止恶意内容的插入。 |

## MCP 服务器连接

本技能依赖于 Temporal Cortex MCP 服务器。请参阅 `.mcp.json` 文件以获取默认配置信息。

**本地模式**（默认推荐）：
第 1 层工具（时间上下文处理、日期时间转换、时区转换）无需任何配置即可立即使用。日历工具需要一次性完成 OAuth 设置——运行 [设置脚本](scripts/setup.sh) 或使用命令 `npx @temporal-cortex/cortex-mcp auth google`。

**托管云模式**（无需本地设置）：
在 https://app.temporal-cortex.com 注册以获取托管的 MCP 端点，并使用Bearer 令牌进行身份验证。配置客户端时使用云端的 URL，所有 11 个工具均可正常使用，同时支持开放调度、仪表盘界面和多代理协调功能。

## 其他参考资料

- [预订安全](references/BOOKING-SAFETY.md)——两阶段提交、冲突解决机制、预订锁的过期时间设置  
- [多日历管理](references/MULTI-CALENDAR.md)——使用提供者前缀的 ID、可用性信息合并、隐私设置  
- [重复规则指南](references/RRULE-GUIDE.md)——重复规则的模式及夏令时的处理方式  
- [工具参考](references/TOOL-REFERENCE.md)——所有 11 个工具的完整输入/输出格式规范