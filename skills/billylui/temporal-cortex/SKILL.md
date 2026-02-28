---
name: temporal-cortex
description: 安排会议、检查他人时间是否可用，并在 Google、Outlook 和 CalDAV 之间管理日历。相关子技能可用于处理日期时间的解析和日历安排。
  Schedule meetings, check availability, and manage calendars across Google, Outlook, and CalDAV. Routes to focused sub-skills for datetime resolution and calendar scheduling.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. python3 optional (configure/status scripts). Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.5.6"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
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
# Temporal Cortex — 日历调度路由器

这是一个用于 Temporal Cortex 日历操作的路由技能。它根据用户的意图将任务路由到相应的子技能。

## 子技能

| 子技能 | 使用场景 | 所需工具 |
|-----------|------------|-------|
| [temporal-cortex-datetime](https://github.com/temporal-cortex/skills/blob/main/skills/temporal-cortex-datetime/SKILL.md) | 时间解析、时区转换、时长计算。无需凭证，可立即使用。 | 5 个工具（第 1 层） |
| [temporal-cortex-scheduling](https://github.com/temporal-cortex/skills/blob/main/skills/temporal-cortex-scheduling/SKILL.md) | 列出日历、事件、空闲时段、可用性、RRULE 规则的扩展以及预订功能。需要 OAuth 凭证。 | 8 个工具（第 0-4 层） |

## 路由表

| 用户意图 | 路由目标 |
|------------|----------|
| “现在几点了？”，“转换时区”，“还有多久……” | **temporal-cortex-datetime** |
| “显示我的日历”，“查找空闲时间”，“检查可用性”，“扩展重复规则” | **temporal-cortex-scheduling** |
| “预订会议”，“安排约会” | **temporal-cortex-scheduling** |
| “安排下周二下午 2 点的会议”（完整工作流程） | **temporal-cortex-datetime** → **temporal-cortex-scheduling** |

## 核心工作流程

所有日历操作都遵循以下 5 个步骤：

**在不知道日历信息时，始终从第 1 步开始。**切勿假设当前时间；在预订前务必进行冲突检查。

## 所有 12 个工具（5 个层级）

| 层级 | 工具 | 子技能 |
|-------|-------|-----------|
| 0 — 发现层 | `list_calendars` | scheduling |
| 1 — 时间上下文层 | `get_temporal_context`, `resolve_datetime`, `convert_timezone`, `compute_duration`, `adjust_timestamp` | datetime |
| 2 — 日历操作层 | `list_events`, `find_free_slots`, `expand_rrule`, `check_availability` | scheduling |
| 3 — 可用性层 | `get_availability` | scheduling |
| 4 — 预订层 | `book_slot` | scheduling |

## MCP 服务器连接

所有子技能都依赖于 [Temporal Cortex MCP 服务器](https://github.com/temporal-cortex/mcp)（`@temporal-cortex/cortex-mcp@0.5.6`），这是一个作为 npm 包分发的 Rust 编译二进制文件。

**启动时会发生以下操作：**
1. `npx` 从 npm 注册表下载 `@temporal-cortex/cortex-mcp@0.5.6`（仅下载一次，会缓存到本地）。
2. MCP 服务器作为本地进程启动，并通过标准输入/输出（stdio）进行通信。
3. 第 1 层工具（时间处理工具）仅进行本地计算，不涉及网络访问。
4. 第 2-4 层工具（日历处理工具）会向您配置的提供者（如 Google、Outlook、CalDAV）发起经过身份验证的 API 请求。

**凭证存储：** OAuth 令牌存储在本地文件 `~/.config/temporal-cortex/credentials.json` 中，永远不会发送到 Temporal Cortex 服务器。

**验证：** 每次 [GitHub 发布版本](https://github.com/temporal-cortex/mcp/releases) 都会附带 SHA256 校验和，并将其嵌入到 npm 包中，以便在安装后自动进行验证。来源：[github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（采用 MIT 许可协议）。

有关默认配置，请参阅 [`.mcp.json` 文件（https://github.com/temporal-cortex/skills/blob/main/.mcp.json）：

```json
{
  "mcpServers": {
    "temporal-cortex": {
      "command": "npx",
      "args": ["-y", "@temporal-cortex/cortex-mcp@0.5.6"]
    }
  }
}
```

对于托管环境（无需本地设置），请参阅 MCP 仓库中的 [平台模式](https://github.com/temporal-cortex/mcp#local-mode-vs-platform-mode)。

第 1 层工具无需任何配置即可立即使用。日历工具需要一次性设置 OAuth 凭证——请运行 [设置脚本](https://github.com/temporal-cortex/skills/blob/main/scripts/setup.sh) 或使用 `npx @temporal-cortex/cortex-mcp@0.5.6 auth google` 进行设置。