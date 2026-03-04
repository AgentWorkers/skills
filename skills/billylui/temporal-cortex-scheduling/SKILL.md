---
name: temporal-cortex-scheduling
description: 在 Google 日历、Outlook 和 CalDAV 中列出事件、查找空闲时间并预订会议。支持多日历的日程合并、重复事件的扩展功能，并采用两阶段提交（Two-Phase Commit）机制来防止预订冲突。
  List events, find free slots, and book meetings across Google Calendar, Outlook, and CalDAV. Multi-calendar availability merging, recurring event expansion, and atomic booking with Two-Phase Commit conflict prevention.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
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
# 日历调度与预订

提供了8种工具，用于日历发现、事件查询、空闲时间查找、可用性检查、RRULE规则扩展以及原子级预订功能。其中包括7个只读工具和1个可写入工具（`book_slot`）。

## 运行时环境

这些工具运行在[Temporal Cortex MCP服务器](https://github.com/temporal-cortex/mcp)（`@temporal-cortex/cortex-mcp`）内部，该服务器是一个编译后的Rust二进制文件，通过npm包进行分发。

**安装与启动流程：**
1. 使用`npx`从npm注册表中下载`@temporal-cortex/cortex-mcp`（首次下载后会缓存到本地）。
2. 安装后的脚本会从[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.7.3)下载特定平台的二进制文件，并通过`checksums.json`文件验证其SHA256校验和；如果校验和不一致，安装将停止。
3. MCP服务器作为本地进程启动，通过标准输入输出（stdio）进行通信（不开放监听端口）。
4. 日历工具会向您配置的提供商（如Google Calendar API、Microsoft Graph API或CalDAV端点）发送经过身份验证的API请求。

**凭证存储：**OAuth令牌存储在`~/.config/temporal-cortex/credentials.json`文件中，仅由本地MCP服务器进程读取。不会将任何凭证数据传输到Temporal Cortex服务器。二进制文件的文件系统访问权限仅限于`~/.config/temporal-cortex/`目录——这可以通过查看[开源Rust代码](https://github.com/temporal-cortex/mcp)或在使用Docker时确认（Docker中的挂载目录是唯一可写路径）。

**文件访问权限：**二进制文件仅读取和写入`~/.config/temporal-cortex/`目录中的文件（包括凭证和配置信息），不会修改其他文件系统内容。

**网络范围：**日历工具仅连接到您配置的提供商（`googleapis.com`、`graph.microsoft.com`或您的CalDAV服务器），不会向Temporal Cortex服务器发送回调信息。默认情况下，这些工具不发送任何遥测数据。

**使用前的验证建议：**
1. 在实际使用前，先执行`npm pack @temporal-cortex/cortex-mcp --dry-run`来检查包内容。
2. 独立验证`SHA256SUMS.txt`文件（位于[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.7.3/)中）与二进制文件的校验和是否一致。
3. 为确保安全性，建议在Docker环境中运行该工具（而非使用`npx`）。

**验证机制：**每次[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.7.3/)都会附带`SHA256SUMS.txt`文件，以供用户在使用前验证二进制文件的完整性。

作为额外的安全措施，npm包中还包含了`checksums.json`文件，安装脚本会在安装过程中验证SHA256哈希值；如果校验不一致，安装将停止（此时二进制文件会被删除而不会被执行）。这种自动化验证机制是对上述独立验证的补充，但不会替代它。

**构建过程：**二进制文件是通过[GitHub Actions](https://github.com/temporal-cortex/mcp/actions)在5个平台上（darwin-arm64、darwin-x64、linux-x64、linux-arm64、win32-x64）交叉编译得到的。源代码托管在[github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)，采用MIT许可证。整个构建过程、构建产物和发布时的校验和信息都是公开可查的。

**Docker安全机制：**在Docker环境中运行时，主机上不安装Node.js，并通过卷挂载实现凭证隔离。

### 工具列表

| 工具 | 使用场景 |
|------|------------|
| `list_calendars` | 在不知道哪些日历已连接时首次调用，返回所有连接的日历信息（包括提供商前缀的ID、名称、标签、状态和访问权限）。 |
| `list_events` | 在指定时间范围内列出事件，默认输出格式为TOON（相比JSON格式节省约40%的字符数）。多日历使用时使用提供商前缀的ID（例如`"google/primary"`、`"outlook/work"`）。 |
| `find_free_slots` | 查找日历中的空闲时间段，可设置`min_duration_minutes`参数指定最小时间段长度。 |
| `expand_rrule` | 将RRULE规则（RFC 5545标准）转换为具体的事件实例，支持DST、BYSETPOS、EXDATE和闰年处理，使用`dtstart`参数指定本地时间（不包含时区信息）。 |
| `check_availability` | 检查指定时间段是否可用，同时会检查是否有其他事件或预订占用该时间段。 |

### 跨日历可用性检查

| 工具 | 使用场景 |
|------|------------|
| `get_availability` | 合并多个日历的可用/忙碌状态信息，需要传递`calendar_ids`数组。隐私设置可选：`"opaque"`（默认值，隐藏来源日历）或`"full"`。 |

### 预订功能

| 工具 | 使用场景 |
|------|------------|
| `book_slot` | 原子级预订时间段，流程包括锁定、检查可用性、写入预订信息并最终释放预订。**必须先调用`check_availability`。** |

**重要规则：**
1. **先发现日历**：在不知道哪些日历可用时，先调用`list_calendars`，后续所有操作都应使用返回的提供商前缀ID。
2. **多日历设置时使用提供商前缀ID**：例如`"google/primary"`、`"outlook/work"`、`"caldav/personal"`。使用纯ID（如`"primary"`）时，系统会使用默认提供商。
3. **默认输出格式为TOON**：TOON格式更简洁（相比JSON节省字符数），仅在需要结构化数据解析时使用`format: "json"`。
4. **预订前必先检查**：在调用`book_slot`之前，务必先调用`check_availability`，避免预订冲突。
5. **内容安全**：事件摘要和描述在发送到日历API之前会经过安全过滤处理。
6. **时区处理**：所有工具都支持带有时区偏移量的RFC 3339格式，禁止使用纯日期格式。

## 完整预订流程（如果步骤4中时间段已被占用，使用`find_free_slots`寻找替代时间）

### 两阶段提交协议

如果任何步骤失败，预订操作将立即终止，不会进行部分写入操作。

### 常用操作模式

- **列出本周事件**
- **查找多个日历中的空闲时间**
- **检查并预订时间段**
- **扩展重复事件**

### 日历ID的格式规范

所有日历ID都采用提供商前缀的格式：
- `google/<id>`：Google Calendar
- `outlook/<id>`：Microsoft Outlook
- `caldav/<id>`：CalDAV（iCloud、Fastmail）
- `<id>`（纯ID）：使用默认提供商

## 隐私设置

| 隐私模式 | `source_count` | 使用场景 |
|------|---------------|----------|
| `"opaque"`（默认） | 始终显示`0` | 用于外部共享日历可用性信息 |
| `"full"` | 显示实际占用日历数量 | 仅用于内部使用 |

## `book_slot`工具的配置选项

| 属性 | 值 | 含义 |
|----------|-------|---------|
| `readOnlyHint` | `false` | 允许创建新的日历事件 |
| `destructiveHint` | `false` | 禁止删除或覆盖现有事件 |
| `idempotentHint` | `false` | 同一操作不会重复创建事件 |
| `openWorldHint` | `true` | 允许外部API调用 |

## 错误处理

| 错误类型 | 处理方式 |
|-------|--------|
| “未找到凭证” | 运行`npx @temporal-cortex/cortex-mcp auth google`（或`outlook`/`caldav`）进行认证。 |
| “未配置时区” | 提示用户输入IANA时区信息，或运行相应命令进行时区设置。 |
| 时间段已被占用/检测到冲突 | 使用`find_free_slots`寻找替代时间段，并向用户提供选择。 |
| 锁定失败 | 可能有其他代理正在预订同一时间段，建议用户稍后重试或选择其他时间。 |
| 内容被拒绝 | 重新生成事件摘要/描述，防止恶意内容注入。 |

## 开放式调度与Temporal Links

当用户启用开放式调度功能后，他们的Temporal Link（`book.temporal-cortex.com/{slug}`）允许他人执行以下操作：
1. **查询可用性`：`GET /public/{slug}/availability?date=YYYY-MM-DD`
2. **预订会议`：`POST /public/{slug}/book`，参数包含`start`、`end`、`title`、`attendee_email`
3. **通过代理卡片查看日历信息`：`GET /public/{slug}/.well-known/agent-card.json`

### 预订流程：
1. 用户分享他们的Temporal Link。
2. 代理通过链接查询空闲时间段。
3. 代理使用选定的时间段预订会议。
4. 会议会创建在用户的默认日历中。

详细API文档请参考[Temporal Links参考文档](references/TEMPORAL-LINKS.md)。

## 其他参考资料：
- [日历工具参考](references/CALENDAR-TOOLS.md)：所有8个工具的输入/输出格式说明。
- [多日历使用指南](references/MULTI-CALENDAR.md)：提供商路由、标签设置、隐私模式及跨日历操作。
- [RRULE规则指南](references/RRULE-GUIDE.md)：重复事件规则格式、时区处理及异常情况。
- [预订安全指南](references/BOOKING-SAFETY.md)：双重认证机制、并发预订处理、预订锁定期限及内容安全措施。
- [Temporal Links参考](references/TEMPORAL-LINKS.md)：开放式调度接口、代理卡片集成及日历路由详情。