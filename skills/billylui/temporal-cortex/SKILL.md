---
name: temporal-cortex
description: 安排会议、检查可用性，并在 Google、Outlook 和 CalDAV 之间管理日历。这些功能指向相关的子技能，用于处理日期时间的解析和日历安排。
  Schedule meetings, check availability, and manage calendars across Google, Outlook, and CalDAV. Routes to focused sub-skills for datetime resolution and calendar scheduling.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. python3 optional (configure/status scripts). Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.5.8"
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
| [temporal-cortex-datetime](https://github.com/temporal-cortex/skills/blob/main/skills/temporal-cortex-datetime/SKILL.md) | 时间解析、时区转换、时长计算。无需凭证——可立即使用。 | 5 个工具（第 1 层） |
| [temporal-cortex-scheduling](https://github.com/temporal-cortex/skills/blob/main/skills/temporal-cortex-scheduling/SKILL.md) | 列出日历、事件、空闲时间、可用性、RRULE 规则的扩展以及预订功能。需要 OAuth 凭证。 | 8 个工具（第 0-4 层） |

## 路由表

| 用户意图 | 路由目标 |
|------------|----------|
| “现在几点了？”，“转换时区”，“还有多久...” | **temporal-cortex-datetime** |
| “显示我的日历”，“查找空闲时间”，“检查可用性”，“扩展重复规则” | **temporal-cortex-scheduling** |
| “预订会议”，“安排约会” | **temporal-cortex-scheduling** |
| “安排下周二下午 2 点的会议”（完整工作流程） | **temporal-cortex-datetime** → **temporal-cortex-scheduling** |

## 核心工作流程

所有日历交互都遵循以下 5 个步骤：

**在日历信息未知的情况下，始终从第 1 步开始。**切勿假设当前时间。在预订之前，务必进行冲突检查。

## 所有 12 个工具（5 个层级）

| 层级 | 工具 | 子技能 |
|-------|-------|-----------|
| 0 — 发现层 | `list_calendars` | scheduling |
| 1 — 时间上下文层 | `get_temporal_context`，`resolve_datetime`，`convert_timezone`，`compute_duration`，`adjust_timestamp` | datetime |
| 2 — 日历操作层 | `list_events`，`find_free_slots`，`expand_rrule`，`check_availability` | scheduling |
| 3 — 可用性层 | `get_availability` | scheduling |
| 4 — 预订层 | `book_slot` | scheduling |

## MCP 服务器连接

所有子技能都依赖于 [Temporal Cortex MCP 服务器](https://github.com/temporal-cortex/mcp)（版本 `@temporal-cortex/cortex-mcp@0.5.8`），这是一个用 Rust 编写的二进制文件，通过 npm 包进行分发。

**启动时的流程：**
1. `npx` 从 npm 注册表下载 `@temporal-cortex/cortex-mcp@0.5.8`（仅下载一次，缓存到本地）。
2. MCP 服务器作为本地进程启动，并通过标准输入/输出（stdio）进行通信。
3. 第 1 层工具（日期时间相关功能）仅进行本地计算，不涉及任何网络请求。
4. 第 2-4 层工具会向您配置的日历服务提供商（如 Google、Outlook、CalDAV）发送经过身份验证的 API 请求。

**凭证存储：** OAuth 令牌存储在 `~/.config/temporal-cortex/credentials.json` 文件中，并在本地使用，不会发送到 Temporal Cortex 服务器。

**文件访问权限：** 该二进制文件仅读取和写入 `~/.config/temporal-cortex/` 目录下的文件（包括凭证和配置信息），不会访问其他文件系统。

**网络范围：** 在初次通过 npm 下载后，第 1 层工具不再发送任何网络请求。第 2-4 层工具仅连接到您配置的日历服务提供商（`googleapis.com`、`graph.microsoft.com` 或 CalDAV 服务器）。默认情况下，不发送任何回传数据到 Temporal Cortex 服务器。此外，系统默认关闭了遥测功能。

**验证机制：** 每次发布新版本时，都会附带 SHA256 校验和（文件名：`SHA256SUMS.txt`），并嵌入到 npm 包中，以便在安装后进行自动验证。您也可以手动进行验证：

**来源：** [github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（采用 MIT 许可协议）。二进制文件通过在 [GitHub Actions](https://github.com/temporal-cortex/mcp/actions) 中使用可审计的 Rust 代码生成。

**Docker 隔离环境：** 如果需要在主机上不使用 Node.js 的环境中运行该服务，可以将 MCP 服务器部署在容器中。具体步骤请参见 [Docker 配置指南](https://github.com/temporal-cortex/mcp#how-do-i-verify-the-installation)。

有关默认配置信息，请参阅 `[.mcp.json](https://github.com/temporal-cortex/skills/blob/main/.mcp.json)`：

**对于托管环境（无需本地配置）：** 请参考 MCP 仓库中的 [平台模式说明](https://github.com/temporal-cortex/mcp#local-mode-vs-platform-mode)。

第 1 层工具无需任何配置即可立即使用。日历相关工具需要完成一次 OAuth 设置：请运行 [设置脚本](https://github.com/temporal-cortex/skills/blob/main/scripts/setup.sh) 或使用 `npx @temporal-cortex/cortex-mcp@0.5.8 auth google` 命令进行设置。