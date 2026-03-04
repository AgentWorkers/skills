---
name: temporal-cortex
description: 安排会议、检查可用性，并在 Google、Outlook 和 CalDAV 之间管理日历。相关子技能用于处理日期时间的解析和日历安排。
  Schedule meetings, check availability, and manage calendars across Google, Outlook, and CalDAV. Routes to focused sub-skills for datetime resolution and calendar scheduling.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker to install the MCP server binary. python3 optional (configure/status scripts). Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.7.3"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
  openclaw:
    install:
      - kind: node
        package: "@temporal-cortex/cortex-mcp@0.7.3"
        bins: [cortex-mcp]
    requires:
      bins:
        - npx
      config:
        - ~/.config/temporal-cortex/credentials.json
        - ~/.config/temporal-cortex/config.json
---
# Temporal Cortex — 日历调度路由器

这是一个用于 Temporal Cortex 日历操作的路由器技能，它根据用户意图将任务路由到相应的子技能。

## 子技能

| 子技能 | 使用场景 | 所需工具 |
|-----------|------------|-------|
| [temporal-cortex-datetime](https://github.com/temporal-cortex/skills/blob/main/skills/temporal-cortex-datetime/SKILL.md) | 时间解析、时区转换、时长计算。无需凭证——可立即使用。 | 5 个工具（第 1 层） |
| [temporal-cortex-scheduling](https://github.com/temporal-cortex/skills/blob/main/skills/temporal-cortex-scheduling/SKILL.md) | 列出日历、事件、空闲时间、可用性、重复规则扩展以及预订功能。需要 OAuth 凭证。 | 8 个工具（第 0-4 层） |

## 路由表

| 用户意图 | 路由到 |
|------------|----------|
| “现在几点了？”，“转换时区”，“还有多久...” | **temporal-cortex-datetime** |
| “显示我的日历”，“查找空闲时间”，“检查可用性”，“扩展重复规则” | **temporal-cortex-scheduling** |
| “预订会议”，“安排约会” | **temporal-cortex-scheduling** |
| “安排下周二下午 2 点的会议”（完整工作流程） | **temporal-cortex-datetime** → **temporal-cortex-scheduling** |

## 核心工作流程

所有日历交互都遵循以下 5 个步骤：

**在日历信息未知的情况下，始终从第一步开始**。切勿假设当前时间；在预订前务必进行冲突检查。

## 安全规则

1. **先发现日历**——当不知道哪些日历已连接时，调用 `list_calendars` 函数。
2. **预订前先检查**——在调用 `book_slot` 之前，务必先调用 `check_availability` 函数。切勿跳过冲突检查。
3. **内容安全**——所有事件摘要和描述在传递给日历 API 之前，都会经过提示注入防火墙的过滤。
4. **时区意识**——切勿假设当前时间；请先使用 `get_temporal_context` 函数获取时区信息。

## 所有 12 个工具（5 个层级）

| 层级 | 所需工具 | 子技能 |
|-------|-------|-----------|
| 0 — 发现日历 | `list_calendars` | 日历操作 |
| 1 — 时间上下文 | `get_temporal_context`、`resolve_datetime`、`convert_timezone`、`compute_duration`、`adjust_timestamp` | 时间处理 |
| 2 — 日历操作 | `list_events`、`find_free_slots`、`expand_rrule`、`check_availability` | 日历操作 |
| 3 — 可用性检查 | `get_availability` | 可用性检查 |
| 4 — 预订 | `book_slot` | 预订功能 |

## MCP 服务器连接

所有子技能都依赖于 [Temporal Cortex MCP 服务器](https://github.com/temporal-cortex/mcp)（`@temporal-cortex/cortex-mcp`），这是一个通过 npm 包分发的 Rust 编译二进制文件。

**安装和启动流程：**
1. 使用 `npx` 从 npm 仓库下载 `@temporal-cortex/cortex-mcp`（首次下载后会在本地缓存）。
2. 安装后的脚本会从 [GitHub 发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.7.3) 下载特定平台的二进制文件，并验证其 SHA256 校验和是否与 `checksums.json` 文件中的值匹配；如果不匹配，安装将停止。
3. MCP 服务器作为本地进程运行，通过标准输入输出（stdio）进行通信（不监听任何端口）。
4. 第 1 层工具（时间处理工具）仅进行本地计算，不涉及网络访问。
5. 第 2-4 层工具（日历操作工具）会向配置的日历提供者（如 Google、Outlook、CalDAV）发起认证后的 API 请求。

**凭证存储：** OAuth 令牌存储在本地文件 `~/.config/temporal-cortex/credentials.json` 中，仅由本地 MCP 服务器进程读取。任何凭证数据都不会传输到 Temporal Cortex 服务器。二进制文件的文件系统访问权限仅限于 `~/.config/temporal-cortex/` 目录（可通过查看 [开源 Rust 代码](https://github.com/temporal-cortex/mcp) 或在 Docker 中运行进行验证，其中 `/tmp` 目录是唯一可写目录）。

**文件访问权限：** 二进制文件仅读取和写入 `~/.config/temporal-cortex/` 目录中的数据（包括凭证和配置信息）。不会访问其他文件系统。

**网络范围：** 在首次通过 npm 下载后，第 1 层工具不会发起任何网络请求；第 2-4 层工具仅连接到配置的日历提供者（如 `googleapis.com`、`graph.microsoft.com` 或 CalDAV 服务器）。默认情况下，不会向 Temporal Cortex 服务器发送回调数据。默认关闭遥测功能。

**使用前的验证建议：**
1. 在执行之前，先查看 npm 包的内容：`npm pack @temporal-cortex/cortex-mcp --dry-run`
2. 独立验证 SHA256 校验和是否与 [GitHub 发布版本](https://github.com/temporal-cortex/mcp/releases/download/mcp-v0.7.3/SHA256SUMS.txt) 中的值匹配（详见下面的验证流程）。
3. 为了确保完全隔离，建议在 Docker 中运行程序（而非使用 `npx`）。

**验证流程：** 每次 [GitHub 发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.7.3) 都会附带 `SHA256SUMS.txt` 文件，用于验证二进制文件的完整性（详见下面的验证流程）：

作为额外的安全措施，npm 包中还嵌入了 `checksums.json` 文件，安装脚本会在安装过程中比较 SHA256 哈希值；如果哈希值不匹配，安装将停止（此时二进制文件会被删除而不会被执行）。这种自动化验证是对上述独立验证的补充，但不会替代它。

**构建过程的可追溯性：** 二进制文件是通过 [GitHub Actions](https://github.com/temporal-cortex/mcp/actions) 在多个平台（darwin-arm64、darwin-x64、linux-x64、linux-arm64、win32-x64）上交叉编译的，源代码托管在 [github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（采用 MIT 许可协议）。CI 工作流程、构建结果和发布时的校验和信息都是公开可查的。

**Docker 隔离机制**（确保主机上不安装 Node.js，并通过卷挂载实现凭证隔离）：

**构建命令：** `docker build -t cortex-mcp https://github.com/temporal-cortex/mcp.git`

**默认配置**（使用 `npx` 的情况）：请参考 `[.mcp.json](https://github.com/temporal-cortex/skills/blob/main/.mcp.json)` 了解标准的 `npx @temporal-cortex/cortex-mcp` 配置方式。关于托管环境，请参阅 MCP 仓库中的 [平台模式](https://github.com/temporal-cortex/mcp#local-mode-vs-platform-mode)。

第 1 层工具无需任何配置即可立即使用；日历工具需要一次性设置 OAuth 凭证——请运行 [设置脚本](https://github.com/temporal-cortex/skills/blob/main/scripts/setup.sh) 或使用 `npx @temporal-cortex/cortex-mcp auth google` 命令进行设置。

## 其他参考资料

- [安全模型](references/SECURITY-MODEL.md) — 内容清洗、文件系统隔离、网络访问范围、工具说明