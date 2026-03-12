---
name: calendar-scheduling
description: >
  安排会议、检查可用性，并在 Google、Outlook 和 CalDAV 之间管理日历。这些功能指向用于处理日期和时间以及日历安排的具体子模块。  
  该工具还提供名为 “temporal-cortex” 的版本。无论是哪个版本，它们都安装相同的 MCP 服务器并共享相同的源代码。
  Schedule meetings, check availability, and manage calendars across Google, Outlook, and CalDAV. Routes to focused sub-skills for datetime resolution and calendar scheduling.
  Also available as temporal-cortex. Both listings install the same MCP server and share the same source code.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker to install the MCP server binary. python3 optional (configure/status scripts). Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.9.1"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
  openclaw:
    install:
      - kind: node
        package: "@temporal-cortex/cortex-mcp@0.9.1"
        bins: [cortex-mcp]
    requires:
      bins:
        - npx
      config:
        - ~/.config/temporal-cortex/credentials.json
        - ~/.config/temporal-cortex/config.json
---
# Temporal Cortex — 日历调度路由器

这是一个用于 Temporal Cortex 日历操作的路由技能。它根据用户意图将任务路由到相应的子技能。

## 适用对象：

**如果您是个人用户**（使用 Claude Desktop、Cursor、OpenClaw 或 Manus）——请安装此技能，让您的 AI 代理管理您的日历。连接您的 Google、Outlook 或 CalDAV 日历，代理将负责处理日程安排、可用性检查及预订，避免重复预订。

**如果您正在开发具有调度功能的产品**——请使用与您的调度后端相同的 MCP 服务器。该系统支持 18 种工具，通过两阶段提交（Two-Phase Commit）实现原子级预订功能，并能合并不同提供者的日程信息。有关开发者集成的详细信息，请参阅 [REST API 参考文档](https://temporal-cortex.com/docs/rest-api) 和 [平台文档](https://app.temporal-cortex.com)。

## 来源与开发历程：

- **官方网站：** [temporal-cortex.com](https://temporal-cortex.com)
- **源代码：** [github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（开源 Rust 项目）
- **npm 包：** [@temporal-cortex/cortex-mcp](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp)
- **技能仓库：** [github.com/temporal-cortex/skills](https://github.com/temporal-cortex/skills)

## 子技能

| 子技能 | 使用场景 | 所需工具 |
|-----------|------------|-------|
| [temporal-cortex-datetime](https://github.com/temporal-cortex/skills/blob/main/skills/temporal-cortex-datetime/SKILL.md) | 时间解析、时区转换、时长计算。无需凭证即可立即使用。 | 5 种工具（第 1 层） |
| [temporal-cortex-scheduling](https://github.com/temporal-cortex/skills/blob/main/skills/temporal-cortex-scheduling/SKILL.md) | 列出日历、事件、空闲时间、可用性检查、重复规则扩展、预订、联系人搜索及会议提案生成。需要 OAuth 凭证。 | 14 种工具（第 0-4 层） |

## 路由表

| 用户意图 | 路由目标 |
|------------|----------|
| “现在几点了？”，“转换时区”，“还有多久...” | **temporal-cortex-datetime** |
| “显示我的日历”，“查找空闲时间”，“检查可用性”，“扩展重复规则” | **temporal-cortex-scheduling** |
| “预订会议”，“安排约会” | **temporal-cortex-scheduling** |
| “查找某人的预订页面”，“查询电子邮件地址” | **temporal-cortex-scheduling** |
| “在我的联系人中搜索 Jane”，“查找某人的电子邮件” | **temporal-cortex-scheduling** |
| “我应该如何与这个人安排会议？” | **temporal-cortex-scheduling** |
| “检查他人的可用性”，“查询公共可用性” | **temporal-cortex-scheduling** |
| “与外部人员预订会议”，“通过 Temporal Link 请求预订” | **temporal-cortex-scheduling** |
| “发送会议提案”，“编写会议邀请” | **temporal-cortex-scheduling** |
| “安排下周二下午 2 点的会议”（完整工作流程） | **temporal-cortex-datetime** → **temporal-cortex-scheduling** |
| “与 Jane 安排会议”（端到端流程） | **temporal-cortex-scheduling**（联系人搜索 → 日程解析 → 提案/预订） |

## 核心工作流程

所有日历操作都遵循以下 7 个步骤：

```
0. Resolve Contact  →  search_contacts → resolve_contact   (find the person, determine scheduling path)
1. Discover         →  list_calendars                       (know which calendars are available)
2. Orient           →  get_temporal_context                  (know the current time)
3. Resolve Time     →  resolve_datetime                     (turn human language into timestamps)
4. Route            →  If open_scheduling: fast path. If email: backward-compat path.
5. Query            →  list_events / find_free_slots / get_availability / query_public_availability
6. Act              →  Fast: check_availability → book_slot / request_booking
                       Backward-compat: compose_proposal → agent sends via channel MCP
```

步骤 0 是可选的——如果用户直接提供了电子邮件地址，则可以跳过。当不知道使用哪些日历时，**必须从步骤 1 开始**。切勿假设当前时间是正确的，且在预订前务必进行冲突检查。

## 安全规则：

1. **先发现日历**——在不知道连接了哪些日历时，调用 `list_calendars` 函数。
2. **预订前先检查**——在调用 `book_slot` 之前，务必先调用 `check_availability` 函数。切勿跳过冲突检查。
3. **内容安全**——所有事件摘要和描述在传递给日历 API 之前都会经过安全检查。
4. **时区处理**——切勿假设当前时间是正确的，务必先使用 `get_temporal_context` 函数获取时区信息。
5. **预订前确认**——在自动运行时，必须在调用 `book_slot` 或 `request_booking` 之前向用户展示预订详情以获取确认。
6. **确认联系人选择**——当 `search_contacts` 返回多个匹配结果时，务必向用户展示所有候选联系人，并确认正确的联系人后再继续操作。
7. **发送提案前确认**——在使用 `compose_proposal` 时，必须在通过任何渠道发送提案之前向用户展示提案内容。切勿自动发送联系信息。
8. **联系人搜索是可选的**——如果用户直接提供了电子邮件地址，整个工作流程也可以不使用联系人搜索功能。如果未配置联系人权限，需向用户请求电子邮件地址。

## 所有 18 种工具（共 5 层）

| 层次 | 所需工具 | 子技能 |
|-------|-------|-----------|
| 0 — 发现日历 | `resolve_identity`，`search_contacts`，`resolve_contact` | 日程调度相关 |
| 1 — 时间处理 | `get_temporal_context`，`resolve_datetime`，`convert_timezone`，`compute_duration`，`adjust_timestamp` | 时间处理相关 |
| 2 — 日历操作 | `list_calendars`，`list_events`，`find_free_slots`，`expand_rrule`，`check_availability` | 日程调度相关 |
| 3 — 可用性检查 | `get_availability`，`query_public_availability` | 日程调度相关 |
| 4 — 预订 | `book_slot`，`request_booking`，`compose_proposal` | 日程调度相关 |

## MCP 服务器连接

所有子技能都依赖于 [Temporal Cortex MCP 服务器](https://github.com/temporal-cortex/mcp)（`@temporal-cortex/cortex-mcp`），这是一个作为 npm 包分发的编译后的 Rust 二进制文件。

**安装与启动流程：**
1. 使用 `npx` 从 npm 仓库安装 `@temporal-cortex/cortex-mcp`（首次安装后会缓存到本地）。
2. 安装后的脚本会从 [GitHub 发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.9.1) 下载特定平台的二进制文件，并验证其 SHA256 校验和是否与 `checksums.json` 文件中的值一致——如果不一致，安装将停止。
3. MCP 服务器作为本地进程运行，通过标准输入输出（stdio）进行通信（不开启监听端口）。
4. 第 1 层工具（时间处理相关工具）仅进行本地计算，不涉及网络访问。
5. 第 2-4 层工具（日历相关工具）会向您配置的日历提供者（Google、Outlook、CalDAV）发送经过身份验证的 API 请求。

**凭证存储：** OAuth 令牌存储在本地文件 `~/.config/temporal-cortex/credentials.json` 中，仅由本地 MCP 服务器进程读取。不会将任何凭证数据传输到 Temporal Cortex 服务器。二进制文件的文件系统访问权限仅限于 `~/.config/temporal-cortex/` 目录——可以通过查看 [开源 Rust 代码](https://github.com/temporal-cortex/mcp) 或在 Docker 中运行来验证这一点（在 Docker 中，`~/.config/temporal-cortex/` 目录是唯一可写入的目录）。

**文件访问权限：** 二进制文件仅读取和写入 `~/.config/temporal-cortex/` 目录中的数据（包括凭证和配置信息）。不会访问其他文件系统目录。

**网络访问范围：** 在首次通过 npm 安装后，第 1 层工具不会发起任何网络请求。第 2-4 层工具仅连接到您配置的日历提供者（`googleapis.com`、`graph.microsoft.com` 或 CalDAV 服务器）。在本地模式下（默认设置），不会向 Temporal Cortex 服务器发送请求，也不会收集任何遥测数据。在平台模式下，第 3-4 层工具会通过 `api.temporal-cortex.com` 进行跨用户日程安排，但这些请求不包含任何凭证信息。

**使用前的验证建议：**
1. 在实际使用前，先检查 npm 包：`npm pack @temporal-cortex/cortex-mcp --dry-run`
2. 独立验证 checksum：将本地生成的 checksum 与 [GitHub 发布版本](https://github.com/temporal-cortex/mcp/releases/download/mcp-v0.9.1/SHA256SUMS.txt) 进行比对（详见下面的验证流程）。
3. 为了确保安全性，建议在 Docker 中运行程序（而非使用 `npx`）。

**验证流程：** 每次 [GitHub 发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.9.1) 都会附带 `SHA256SUMS.txt` 文件，用于验证二进制文件的完整性：

```bash
# 1. Fetch checksums from GitHub (independent of the npm package)
curl -sL https://github.com/temporal-cortex/mcp/releases/download/mcp-v0.9.1/SHA256SUMS.txt

# 2. Compare against the npm-installed binary
shasum -a 256 "$(npm root -g)/@temporal-cortex/cortex-mcp/bin/cortex-mcp"
```

作为额外的安全措施，npm 包中嵌入了 `checksums.json` 文件，安装脚本会在安装过程中比较 SHA256 哈希值——如果哈希值不一致，安装将停止（此时二进制文件会被删除，而不会被执行）。这种自动化检查是对上述独立验证的补充，但不会替代它。

**构建过程：** 二进制文件是通过 [GitHub Actions](https://github.com/temporal-cortex/mcp/actions) 在多个平台上（darwin-arm64、darwin-x64、linux-x64、linux-arm64、win32-x64）交叉编译的。源代码托管在 [github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（采用 MIT 许可协议）。CI 工作流程、构建结果和发布时的 checksum 都可公开查看。

**Docker 安全措施**（确保主机上不安装 Node.js，通过卷挂载实现凭证隔离）：

```json
{
  "mcpServers": {
    "temporal-cortex": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "-v", "~/.config/temporal-cortex:/root/.config/temporal-cortex", "cortex-mcp"]
    }
  }
}
```

构建命令：`docker build -t cortex-mcp https://github.com/temporal-cortex/mcp.git`

**默认配置**（使用 `npx` 的情况）：请参阅 `.mcp.json` 文件（位于 `https://github.com/temporal-cortex/skills/blob/main/.mcp.json`）中的 `npx @temporal-cortex/cortex-mcp` 配置信息。有关托管环境的配置，请参阅 MCP 仓库中的 [平台模式](https://github.com/temporal-cortex/mcp#local-mode-vs-platform-mode) 文档。

第 1 层工具无需任何配置即可立即使用。日历相关工具需要一次性设置 OAuth 凭证——请运行 [设置脚本](https://github.com/temporal-cortex/skills/blob/main/scripts/setup.sh) 或使用 `npx @temporal-cortex/cortex-mcp auth google` 命令进行设置。

## 其他参考资料：

- [安全模型](references/SECURITY-MODEL.md)——内容清理、文件系统安全、网络访问范围及工具功能说明