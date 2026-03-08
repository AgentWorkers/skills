---
name: temporal-cortex-scheduling
description: 在 Google 日历、Outlook 和 CalDAV 中列出事件、查找空闲时间并预订会议。支持多日历的可用时间合并、重复事件的扩展功能，以及采用两阶段提交（Two-Phase Commit）机制来防止预订冲突。
  List events, find free slots, and book meetings across Google Calendar, Outlook, and CalDAV. Multi-calendar availability merging, recurring event expansion, and atomic booking with Two-Phase Commit conflict prevention.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.8.1"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
  openclaw:
    install:
      - kind: node
        package: "@temporal-cortex/cortex-mcp@0.8.1"
        bins: [cortex-mcp]
    requires:
      bins:
        - npx
      config:
        - ~/.config/temporal-cortex/credentials.json
        - ~/.config/temporal-cortex/config.json
---
# 日历调度与预订

共有11个工具（分为0层、2-4层），用于日历发现、事件查询、空闲时段查找、可用性检查、RRULE规则扩展、原子级预订以及开放式调度功能。其中包括9个只读工具和2个可写工具（`book_slot`、`request_booking`）。

## 来源与出处

- **官方网站：** [temporal-cortex.com](https://temporal-cortex.com)
- **源代码：** [github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（开源Rust项目）
- **npm包：** [@temporal-cortex/cortex-mcp](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp)
- **Skills仓库：** [github.com/temporal-cortex/skills](https://github.com/temporal-cortex/skills)

## 运行时环境

这些工具运行在[Temporal Cortex MCP服务器](https://github.com/temporal-cortex/mcp)（`@temporal-cortex/cortex-mcp`）内部，该服务器是一个编译后的Rust二进制文件，通过npm包进行分发。

**安装与启动流程：**
1. 使用`npx`从npm仓库中下载`@temporal-cortex/cortex-mcp`（首次下载后会缓存到本地）。
2. 安装后的脚本会从[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.8.1)下载特定平台的二进制文件，并通过`checksums.json`文件验证其SHA256校验和；如果校验不匹配，安装将停止。
3. MCP服务器作为本地进程启动，通过标准输入输出（stdio）进行通信（不开放监听端口）。
4. 日历工具会通过认证后的API调用与您配置的日历服务（如Google Calendar API、Microsoft Graph API、CalDAV端点）进行交互。

**凭证存储：** OAuth令牌存储在`~/.config/temporal-cortex/credentials.json`文件中，仅由本地MCP服务器进程读取。任何凭证数据都不会传输到Temporal Cortex服务器。二进制文件的文件系统访问权限仅限于`~/.config/temporal-cortex/`目录（可通过查看开源Rust代码或在使用Docker时确认）。

**文件访问权限：** 该二进制文件仅读取和写入`~/.config/temporal-cortex/`目录中的数据（包括凭证和配置信息），不会修改其他文件系统内容。

**网络范围：** 日历工具仅连接到您配置的日历服务。在本地模式下（默认设置），不会向Temporal Cortex服务器发送请求，也不会收集任何数据。在平台模式下，有三个工具（`resolve_identity`、`query_public_availability`、`request_booking`）会通过`api.temporal-cortex.com`进行跨用户调度，但这些请求中不包含任何凭证信息。

**使用前的验证建议：**
1. 在执行安装前，先查看npm包的详细信息：`npm pack @temporal-cortex/cortex-mcp --dry-run`
2. 独立验证`SHA256SUMS.txt`文件（位于[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.8.1/SHA256SUMS.txt)中）
3. 为确保安全性，建议在Docker环境中运行该工具（详见Docker相关内容）。

**验证机制：** 每次发布新版本时，都会在`SHA256SUMS.txt`文件中发布校验和值。此自动化检查是对上述独立验证的补充，但不会替代它。

**构建过程：** 二进制文件是通过[GitHub Actions](https://github.com/temporal-cortex/mcp/actions)在5个平台上（darwin-arm64、darwin-x64、linux-x64、linux-arm64、win32-x64）交叉编译得到的。源代码托管在[github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（采用MIT许可证）。持续集成（CI）流程、构建结果和发布时的校验和信息均可公开查看。

**Docker安全机制：** 在Docker环境中运行时，主机上不安装Node.js，并通过卷挂载实现凭证隔离。

## 工具列表

### 第0层——日历发现（平台模式）

| 工具 | 使用场景 |
|------|------------|
| `resolve_identity` | 通过DNS将电子邮件地址、电话号码或代理ID转换为Temporal Cortex的标识符。在调用`query_public_availability`之前使用。 |

### 第2层——日历操作

| 工具 | 使用场景 |
|------|------------|
| `list_calendars` | 当日历信息未知时首次调用。返回所有连接的日历列表，包括提供者前缀的ID、名称、标签、状态和访问权限。 |
| `list_events` | 在指定时间范围内列出事件。默认使用TOON格式（相比JSON格式节省约40%的传输数据量）。多日历情况下使用提供者前缀的ID（例如：`"google/primary"`、`"outlook/work"`）。 |
| `find_free_slots` | 查找日历中的空闲时段。可通过`min_duration_minutes`参数设置最小时段长度。 |
| `expand_rrule` | 将RRULE规则（RFC 5545标准）转换为具体的事件实例。支持夏令时、BYSETPOS、EXDATE和闰年处理。使用`dtstart`参数指定本地日期时间（不包含时区信息）。 |
| `check_availability` | 检查指定时间段是否可用。同时考虑事件和已有的预订情况。 |

### 第3层——可用性检查

| 工具 | 使用场景 |
|------|------------|
| `get_availability` | 合并多个日历的可用性信息。需要传入`calendar_ids`数组。隐私设置：`"opaque"`（默认值，隐藏来源日历信息）或`"full"`。 |
| `query_public_availability` | 通过Temporal Link标识符查询其他用户的公开可用时间。传入标识符和日期以获取其可用时段。仅适用于平台模式。 |

### 第4层——预订功能

| 工具 | 使用场景 |
|------|------------|
| `book_slot` | 原子级预订某个时间段。流程包括锁定、验证、写入和释放。**必须先调用`check_availability`。** |
| `request_booking` | 通过Temporal Link标识符在他人日历上预订时间。需要处于平台模式下。 |

## 重要规则：

1. **先发现日历**：在不知道哪些日历可用时，先调用`list_calendars`。后续调用时使用返回的提供者前缀ID。
2. **多日历设置时使用提供者前缀ID**：例如`"google/primary"`、`"outlook/work"`、`"caldav/personal"`。使用裸ID（如`"primary"`）会自动使用默认提供者。
3. **默认使用TOON格式**：输出采用TOON格式（相比JSON格式节省数据量）。只有在需要结构化解析时才使用`format: "json"`。
4. **预订前必查可用性**：在调用`book_slot`之前，务必先调用`check_availability`。切勿跳过冲突检查。
5. **内容安全**：事件摘要和描述在传递给日历API之前会经过安全过滤处理。
6. **时区处理**：所有工具都支持带有时区偏移的RFC 3339格式。严禁使用纯日期格式。
7. **预订前确认**：自动运行时，务必向用户展示预订详情（时间、日历、摘要），并在调用`book_slot`或`request_booking`前等待用户确认。

## 完整的预订流程

如果步骤4中发现时段已被预订，可使用`find_free_slots`寻找替代时段。

## 开放式调度流程（平台模式）

## 两阶段提交协议

如果任何步骤失败，预订操作将中止，不会进行部分性的数据写入。

## 常用操作模式：

- **列出本周事件**
- **查找多个日历中的空闲时间**
- **检查并预订时段**
- **扩展重复事件**

## 日历ID的格式规范

所有日历ID都采用提供者前缀的格式：

| 格式 | 例 | 对应的日历服务 |
|--------|---------|-----------|
| `google/<id>` | `"google/primary"` | Google Calendar |
| `outlook/<id>` | `"outlook/work"` | Microsoft Outlook |
| `caldav/<id>` | `"caldav/personal"` | CalDAV（iCloud、Fastmail） |
| `<id>`（裸ID） | `"primary"` | 默认提供者 |

## 隐私设置

| 设置 | 含义 | 使用场景 |
|------|---------------|----------|
| `"opaque"`（默认） | 始终显示为`0` | 隐藏日历的可用性信息 |
| `"full"` | 显示实际占用日历的数量 | 仅用于内部查看 |

## 工具参数说明

| 参数 | 值 | 含义 |
|----------|-------|---------|
| `readOnlyHint` | `false` | 允许创建日历事件 |
| `destructiveHint` | `false` | 禁止删除或覆盖现有事件 |
| `idempotentHint` | `false` | 同一操作不会重复创建事件 |
| `openWorldHint` | `true` | 允许调用外部API |

## 错误处理

| 错误类型 | 处理方式 |
|-------|--------|
| “未找到凭证” | 运行`npx @temporal-cortex/cortex auth google`（或`outlook` / `caldav`）进行认证。 |
| “时区未配置” | 提示用户输入IANA时区信息，或运行认证命令进行配置。 |
| 时段已预订/存在冲突 | 使用`find_free_slots`寻找替代时段，并向用户提供选项。 |
| 预订失败 | 可能有其他用户正在预订同一时段，建议用户选择其他时间。 |
| 内容被拒绝 | 重新生成事件摘要/描述。防火墙会阻止恶意代码的注入。 |

## 开放式调度与Temporal Links

当用户启用开放式调度功能后，他们的Temporal Link（`book.temporal-cortex.com/{slug}`）允许他人执行以下操作：

1. **查询可用性**：`GET /public/{slug}/availability?date=YYYY-MM-DD`
2. **预订会议**：`POST /public/{slug}/book`，参数包含`start`、`end`、`title`、`attendee_email`
3. **通过代理卡片查看日历信息**：`GET /public/{slug}/.well-known/agent-card.json`

### 通过Temporal Link预订的流程：
1. 用户分享他们的Temporal Link。
2. 代理通过可用性接口查询空闲时段。
3. 代理使用选定的时段通过预订接口进行预订。
4. 会议将在用户的默认日历上创建。

详细API文档请参阅[Temporal Links参考文档](references/TEMPORAL-LINKS.md)。

## 其他参考资料：
- [日历工具参考](references/CALENDAR-TOOLS.md)：所有11个工具的输入/输出格式说明
- [多日历使用指南](references/MULTI-CALENDAR.md)：提供者路由、标签设置、隐私模式、跨日历操作
- [RRULE规则指南](references/RRULE-GUIDE.md)：重复规则格式、夏令时处理、异常情况处理
- [预订安全指南](references/BOOKING-SAFETY.md)：双向认证（2PC）机制、并发预订、预订锁定期限、内容安全处理
- [Temporal Links参考](references/TEMPORAL-LINKS.md)：开放式调度接口、代理卡片集成、日历路由
- [开放式调度指南](references/OPEN-SCHEDULING.md)：身份验证、公开可用性、通过MCP工具进行外部预订