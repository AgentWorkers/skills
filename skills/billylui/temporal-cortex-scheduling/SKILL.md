---
name: temporal-cortex-scheduling
description: 在 Google 日历、Outlook 和 CalDAV 中列出事件、查找空闲时间并预订会议。支持多日历的日程安排合并、重复事件的扩展功能，以及采用“两阶段提交”（Two-Phase Commit）机制来防止预订冲突。
  List events, find free slots, and book meetings across Google Calendar, Outlook, and CalDAV. Multi-calendar availability merging, recurring event expansion, and atomic booking with Two-Phase Commit conflict prevention.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.7.8"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
  openclaw:
    install:
      - kind: node
        package: "@temporal-cortex/cortex-mcp@0.7.8"
        bins: [cortex-mcp]
    requires:
      bins:
        - npx
      config:
        - ~/.config/temporal-cortex/credentials.json
        - ~/.config/temporal-cortex/config.json
---
# 日历调度与预订

共有11个工具（分为0层至4层），用于日历查询、事件查找、空闲时间段的查找、可用性检查、RRULE规则的扩展、原子级预订以及开放式调度功能。其中包括9个只读工具和2个可写工具（`book_slot`和`request_booking`）。

## 来源与开发历程

- **官方网站：** [temporal-cortex.com](https://temporal-cortex.com)
- **源代码：** [github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（开源Rust项目）
- **npm包：** [@temporal-cortex/cortex-mcp](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp)
- **Skills仓库：** [github.com/temporal-cortex/skills](https://github.com/temporal-cortex/skills)

## 运行环境

这些工具运行在[Temporal Cortex MCP服务器](https://github.com/temporal-cortex/mcp)（`@temporal-cortex/cortex-mcp`）内部，该服务器是一个编译后的Rust二进制文件，通过npm包进行分发。

**安装与启动流程：**
1. 使用`npx`从npm仓库下载`@temporal-cortex/cortex-mcp`（首次下载后会缓存到本地）。
2. 安装后的脚本会从[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.7.8)下载特定平台的二进制文件，并通过`checksums.json`文件验证其SHA256校验和；如果校验不匹配，安装将停止。
3. MCP服务器作为本地进程启动，通过标准输入输出（STDIO）进行通信（不绑定任何监听端口）。
4. 日历工具会通过认证后的API调用与您配置的日历服务（如Google Calendar API、Microsoft Graph API或CalDAV端点）进行交互。

**凭证存储：** OAuth令牌存储在本地文件`~/.config/temporal-cortex/credentials.json`中，仅由MCP服务器进程读取。凭证数据不会传输到Temporal Cortex服务器。二进制文件的文件系统访问权限仅限于`~/.config/temporal-cortex/`目录（可通过查看开源Rust代码或Docker容器中的挂载目录来验证）。

**文件访问权限：** 二进制文件仅读写`~/.config/temporal-cortex/`目录（包含凭证和配置信息），不会访问其他文件系统目录。

**网络范围：** 日历工具仅连接到您配置的日历服务，不会与Temporal Cortex服务器进行交互。默认情况下，系统不发送任何遥测数据。

**使用前的验证建议：**
1. 在实际使用前，先执行`npm pack @temporal-cortex/cortex-mcp --dry-run`命令进行测试。
2. 独立验证`SHA256SUMS.txt`文件（位于[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.7.8/SHA256SUMS.txt)中）与二进制文件的校验结果。
3. 为确保安全性，建议在Docker容器中运行该工具（而非使用`npx`命令）。

**验证机制：** 每个GitHub发布版本都会附带`SHA256SUMS.txt`文件，用于验证二进制文件的完整性。此外，npm包中还嵌入了`checksums.json`文件，安装过程中会自动比较校验和；如果校验不匹配，安装将停止（此时二进制文件会被删除而不会被执行）。

**构建过程：** 二进制文件是通过[GitHub Actions](https://github.com/temporal-cortex/mcp/actions)在5个平台上（darwin-arm64、darwin-x64、linux-x64、linux-arm64、win32-x64）交叉编译生成的。源代码托管在[github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（采用MIT许可证）。构建过程、构建结果和发布时的校验信息均公开可见。

**Docker容器安全措施：** 容器内不安装Node.js，通过卷挂载实现凭证隔离。

## 工具列表

### 第0层——日历发现（平台模式）

| 工具 | 使用场景 |
|------|------------|
| `resolve_identity` | 通过DNS将人类可读的时间标识（如电子邮件、电话号码或代理ID）转换为Temporal Cortex的统一格式。在调用`query_public_availability`之前使用。 |

### 第2层——日历操作

| 工具 | 使用场景 |
|------|------------|
| `list_calendars` | 当日历信息未知时首次调用。返回所有连接的日历信息，包括提供商前缀的ID、名称、标签、状态和访问权限。 |
| `list_events` | 在指定时间范围内列出事件。默认使用TOON格式（相比JSON格式节省约40%的传输数据量）。多日历使用时使用提供商前缀的ID（例如`"google/primary"`、`"outlook/work"`）。 |
| `find_free_slots` | 查找日历中的空闲时间段。可设置`min_duration_minutes`参数指定最小时间段长度。 |
| `expand_rrule` | 将RRULE规则（RFC 5545标准）转换为具体的事件实例。支持夏令时、BYSETPOS、EXDATE和闰年处理。使用`dtstart`参数指定本地时间（不包含时区信息）。 |
| `check_availability` | 检查指定时间段的可用性，同时考虑现有事件和预订情况。 |

### 第3层——可用性检查

| 工具 | 使用场景 |
|------|------------|
| `get_availability` | 合并多个日历的可用性信息（空闲/忙碌状态）。需要传递`calendar_ids`数组。隐私设置：`"opaque"`（默认值，隐藏来源日历信息）或`"full"`（显示所有日历的可用性）。 |
| `query_public_availability` | 通过Temporal Link标识查询其他用户的公开可用时间。需提供链接和日期信息。仅适用于平台模式。 |

### 第4层——预订功能

| 工具 | 使用场景 |
|------|------------|
| `book_slot` | 原子级预订时间段。流程包括检查可用性、锁定资源、确认预订和释放资源。**必须先调用`check_availability`。** |
| `request_booking` | 通过Temporal Link标识在他人日历上预订时间段。需要启用平台模式。 |

## 重要规则：

1. **先发现日历**：在不知道哪些日历可用时，先调用`list_calendars`函数。后续所有调用均应使用返回的提供商前缀ID。
2. **多日历环境下的ID使用规则**：使用`"google/primary"`、`"outlook/work"`、`"caldav/personal"`等前缀标识日历。使用纯ID（如`"primary"`）时，系统会自动使用默认提供商。
3. **默认输出格式为TOON**：TOON格式更节省数据传输量（相比JSON格式减少约40%的传输数据量）。如需结构化数据解析，可指定`format: "json"`。
4. **预订前必先检查**：在调用`book_slot`之前，务必先调用`check_availability`函数，避免预订冲突。
5. **内容安全**：事件摘要和描述在发送到日历API之前会经过安全过滤处理。
6. **时区处理**：所有工具都支持包含时区偏移量的RFC 3339格式。禁止使用纯日期格式。

## 完整的预订流程（如果步骤4中指定时间段已被预订，可使用`find_free_slots`寻找替代时间段）

## 开放式调度流程（平台模式）

## 两阶段提交协议

## 如果任何步骤失败，系统会释放已锁定的资源并取消预订。不允许部分操作。

## 常用操作模式：

- **列出本周事件**
- **查找多个日历中的空闲时间**
- **检查并预订时间段**
- **扩展重复事件**

## 日历ID的格式规范

所有日历ID均采用以下格式：

| 格式 | 例子 | 对应的API路径 |
|--------|---------|-----------|
| `google/<id>` | `"google/primary"` | Google Calendar |
| `outlook/<id>` | `"outlook/work"` | Microsoft Outlook |
| `caldav/<id>` | `"caldav/personal"` | CalDAV（iCloud、Fastmail） |
| `<id>`（纯ID） | `"primary"` | 默认提供商 |

## 隐私设置

| 隐私模式 | `source_count` | 使用场景 |
|------|---------------|----------|
| `"opaque"`（默认） | 始终显示`0` | 用于外部共享日历可用性 |
| `"full"` | 显示实际可用日历数量 | 仅用于内部查看 |

## 工具参数说明

| 参数 | 值 | 含义 |
|----------|-------|---------|
| `readOnlyHint` | `false` | 允许创建新的日历事件 |
| `destructiveHint` | `false` | 禁止删除或覆盖现有事件 |
| `idempotentHint` | `false` | 同一操作不会重复创建事件 |
| `openWorldHint` | `true` | 允许调用外部API |

## 错误处理

| 错误类型 | 处理方式 |
|-------|--------|
| “未找到凭证” | 运行`npx @temporal-cortex/cortex-mcp auth google`（或`outlook`/`caldav`）命令进行身份验证。 |
| “时区未配置” | 提示用户输入IANA时区信息，或手动配置时区。 |
| 时间段已预订/存在冲突 | 使用`find_free_slots`寻找替代时间段，并向用户提供选择。 |
| 预订失败 | 可能有其他用户正在预订同一时间段，建议用户重新选择时间或稍后尝试。 |
| 内容被拒绝 | 重新生成事件摘要/描述。系统会阻止恶意内容注入。 |

## 开放式调度与Temporal Links

当用户启用开放式调度功能后，他们的Temporal Link（格式为`book.temporal-cortex.com/{slug}`）允许其他人执行以下操作：

1. **查询可用性**：`GET /public/{slug}/availability?date=YYYY-MM-DD`
2. **预订会议**：`POST /public/{slug}/book`，传入`{start, end, title, attendee_email}`参数 |
3. **通过代理卡片查看日历信息**：`GET /public/{slug}/.well-known/agent-card.json`

### 预订流程：
1. 用户分享他们的Temporal Link。
2. 代理通过链接查询可用时间段。
3. 代理使用选定的时间段发起预订请求。
4. 会议会在用户的默认日历上创建。

详细API文档请参阅[Temporal Links参考文档](references/TEMPORAL-LINKS.md)。

## 其他参考资料：
- [日历工具参考](references/CALENDAR-TOOLS.md)：所有11个工具的输入/输出格式说明。
- [多日历使用指南](references/MULTI-CALENDAR.md)：提供商路由、标签设置、隐私模式及跨日历操作。
- [RRULE规则指南](references/RRULE-GUIDE.md)：RRULE规则的使用规范、夏令时处理及异常情况。
- [预订安全指南](references/BOOKING-SAFETY.md)：双向认证机制、并发预订处理、预订锁定的有效期及内容安全措施。
- [Temporal Links参考](references/TEMPORAL-LINKS.md)：开放式调度API、代理卡片集成及日历路由规则。
- [开放式调度指南](references/OPEN-SCHEDULING.md)：用户身份验证、公开日历信息的共享方式及外部预订流程。