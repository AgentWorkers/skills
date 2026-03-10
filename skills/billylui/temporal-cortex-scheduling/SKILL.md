---
name: temporal-cortex-scheduling
description: 在 Google 日历、Outlook 和 CalDAV 中列出事件、查找空闲时间并预订会议。支持多日历的可用时间合并、重复事件的扩展功能，以及采用“两阶段提交”（Two-Phase Commit）机制来防止预订冲突。
  List events, find free slots, and book meetings across Google Calendar, Outlook, and CalDAV. Multi-calendar availability merging, recurring event expansion, and atomic booking with Two-Phase Commit conflict prevention.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
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
# 日历调度与预订

共有14个工具（分为0层、2-4层），用于解决联系人问题、发现日历、查询事件、查找空闲时间、检查可用性、扩展重复规则（RRULEs）、进行原子级预订、开放式调度（Open Scheduling）以及生成预订提案。其中12个工具为只读模式，另外2个工具（`book_slot`和`request_booking`）支持写入操作。

## 来源与开发历程

- **官方网站：** [temporal-cortex.com](https://temporal-cortex.com)
- **源代码：** [github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（开源Rust项目）
- **npm包：** [@temporal-cortex/cortex-mcp](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp)
- **Skills仓库：** [github.com/temporal-cortex/skills](https://github.com/temporal-cortex/skills)

## 运行环境

这些工具运行在[Temporal Cortex MCP服务器](https://github.com/temporal-cortex/mcp)（`@temporal-cortex/cortex-mcp`）内部，该服务器是一个编译后的Rust二进制文件，通过npm包进行分发。

**安装与启动流程：**
1. 使用`npx`从npm仓库中下载`@temporal-cortex/cortex-mcp`（首次下载后会缓存到本地）。
2. 安装后的脚本会从[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.9.1)下载特定平台的二进制文件，并通过`checksums.json`文件验证其SHA256校验和；如果校验不匹配，安装将停止。
3. MCP服务器作为本地进程启动，通过标准输入输出（stdio）进行通信（不监听任何端口）。
4. 日历相关工具会通过认证后的API调用你的配置提供商（如Google日历API、Microsoft Graph API或CalDAV端点）。

**凭证存储：** OAuth令牌存储在本地文件`~/.config/temporal-cortex/credentials.json`中，仅由本地MCP服务器进程读取。不会将任何凭证数据传输到Temporal Cortex服务器。二进制文件的文件系统访问权限仅限于`~/.config/temporal-cortex/`目录（可通过查看[开源Rust代码](https://github.com/temporal-cortex/mcp)或在使用Docker时确认）。

**文件访问权限：** 二进制文件仅读取和写入`~/.config/temporal-cortex/`目录中的数据（包括凭证和配置信息），不会修改其他文件系统内容。

**网络范围：** 日历工具仅连接到你配置的提供商（`googleapis.com`、`graph.microsoft.com`或CalDAV服务器）。在本地模式下（默认设置），不会向Temporal Cortex服务器发送请求，也不会收集任何数据。在平台模式下，`resolve_identity`、`query_public_availability`和`request_booking`这三个工具会通过`api.temporal-cortex.com`进行跨用户调度，但这些请求中不包含任何凭证信息。

**使用前的验证建议：**
1. 在首次使用前，先查看npm包的详细信息（不执行实际安装）：`npm pack @temporal-cortex/cortex-mcp --dry-run`
2. 独立验证`SHA256校验和（参考[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.9.1/SHA256SUMS.txt)）
3. 为确保安全性，建议在Docker环境中运行该工具（详见Docker相关内容）。

**验证机制：** 每次[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.9.1)都会附带`SHA256SUMS.txt`文件，用于验证二进制文件的完整性。此外，npm包中还嵌入了`checksums.json`文件，安装脚本会在安装过程中对比SHA256哈希值；如果校验不匹配，安装将停止（此时二进制文件会被删除，而不会被执行）。

**构建流程：** 二进制文件是通过[GitHub Actions](https://github.com/temporal-cortex/mcp/actions)在5个平台上（darwin-arm64、darwin-x64、linux-x64、linux-arm64、win32-x64）交叉编译的。源代码位于[github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)，采用MIT许可证。整个构建流程、构建结果和发布时的校验和数据都是公开可查看的。

**Docker安全机制：** 在Docker环境中运行时，主机上不安装Node.js；通过卷挂载实现凭证隔离。

## 工具列表

### 第0层 — 日历发现

| 工具 | 使用场景 |
|------|------------|
| `resolve_identity` | 通过DNS将电子邮件、电话号码或代理ID解析为Temporal Cortex的标识符。仅在平台模式下使用，用于`query_public_availability`之前。|
| `search_contacts` | 根据名称在用户的联系人簿中搜索联系人（使用Google People API或Microsoft Graph）。返回包含电子邮件、电话号码、组织信息和职位的匹配联系人（需用户授权）。|
| `resolve_contact` | 给定已确认的联系人信息后，确定最佳的调度方式（原子级预订、电子邮件或电话）。在支持平台API的情况下，可与`resolve_identity`联合使用。|

### 第2层 — 日历操作

| 工具 | 使用场景 |
|------|------------|
| `list_calendars` | 在不知道有哪些日历可用时首次调用。返回所有连接的日历信息，包括提供商前缀的ID、名称、标签、状态和访问权限。|
| `list_events` | 在指定时间范围内列出事件。默认使用TOON格式（相比JSON格式节省约40%的传输数据量）。对于多个日历，使用提供商前缀的ID（例如`"google/primary"`、`"outlook/work"`）。|
| `find_free_slots` | 查找日历中的空闲时间段。可设置`min_duration_minutes`参数指定最小时间段长度。|
| `expand_rrule` | 将重复规则（RFC 5545）转换为具体的事件实例。支持夏令时调整（DST）、BYSETPOS、EXDATE和闰年处理。使用`dtstart`参数指定本地时间（不包含时区后缀）。|
| `check_availability` | 检查指定时间段是否可用。同时检查该时间段内是否有事件或预订。|

### 第3层 — 可用性检查

| 工具 | 使用场景 |
|------|------------|
| `get_availability` | 合并多个日历的可用性信息（空闲/忙碌状态）。需要传递`calendar_ids`数组。隐私设置：`"opaque"`（默认，隐藏来源日历）或`"full"`（显示所有日历）。|
| `query_public_availability` | 通过Temporal Link标识符查询其他用户的公开可用时间。传递标识符和日期以获取他们的空闲时间段。仅在平台模式下使用。|

### 第4层 — 预订

| 工具 | 使用场景 |
|------|------------|
| `book_slot` | 原子级预订时间段。流程包括锁定、检查可用性、写入预订信息并最终释放预订。**必须先调用`check_availability`。**|
| `request_booking` | 通过Temporal Link标识符在另一个用户的日历上预订时间段。需要处于平台模式下。|
| `compose_proposal` | 生成预订提案信息，可用于发送电子邮件、Slack或短信。提案中的时间会按照接收者的时区进行格式化，并附带一个可供代理使用的预订链接。**不会直接发送提案内容，而是返回格式化后的文本供代理通过其内部系统发送。|

## 重要规则

1. **先发现日历**：在不知道哪些日历可用时，先调用`list_calendars`。后续所有调用都应使用返回的提供商前缀ID。|
2. **使用提供商前缀的ID**：对于多个日历的设置，使用`"google/primary"`、`"outlook/work"`、`"caldav/personal"`等前缀。使用纯ID（如`"primary"`时，系统会使用默认提供商。|
3. **默认使用TOON格式**：输出采用TOON格式（相比JSON格式节省数据量）。只有在需要结构化数据解析时才使用`format: "json"`。|
4. **预订前必检查**：在调用`book_slot`之前，务必先调用`check_availability`。切勿跳过冲突检查。|
5. **内容安全**：事件摘要和描述在发送前会经过安全过滤处理。|
6. **时区处理**：所有工具都支持带有时区偏移的RFC 3339格式。切勿使用纯日期格式。|
7. **预订前确认**：在自动执行预订时，务必向用户展示预订详情（时间、日历、事件摘要），并在调用`book_slot`或`request_booking`前等待用户确认。|
8. **确认联系人选择**：当`search_contacts`返回多个匹配结果时，需向用户确认正确的联系人。切勿自动选择联系人。|
9. **发送提案前确认**：在使用`compose_proposal`时，发送提案前务必向用户展示提案内容。切勿自动发送预订请求。|
10. **联系人搜索可选**：如果未配置联系人权限，可直接询问用户的电子邮件地址。即使没有联系人搜索功能，系统也能正常工作。|

## 完整的预订流程（见**CODE_BLOCK_2___）

如果步骤5中指定的时间段已被预订，可使用`find_free_slots`寻找其他可用选项。

## 开放式调度流程（平台模式）（见**CODE_BLOCK_3___）

## 两阶段提交协议（见**CODE_BLOCK_4___）

如果任何步骤失败，预订操作将被取消，不会进行部分性的数据写入。

## 常见操作模式

- **与联系人一起安排日程**（见**CODE_BLOCK_5___）
- **列出本周事件**（见**CODE_BLOCK_6___）
- **跨日历查找空闲时间**（见**CODE_BLOCK_7___）
- **检查并预订时间段**（见**CODE_BLOCK_8___）
- **扩展重复事件**（见**CODE_BLOCK_9___）

## 日历ID的格式规范

所有日历ID都采用以下格式：

| 格式 | 例子 | 对应的API路径 |
|--------|---------|-----------|
| `google/<id>` | `"google/primary"` | Google日历 |
| `outlook/<id>` | `"outlook/work"` | Microsoft Outlook |
| `caldav/<id>` | `"caldav/personal"` | CalDAV（iCloud、Fastmail） |
| `<id>`（纯ID） | `"primary"` | 默认提供商 |

## 隐私设置

| 模式 | `source_count` | 使用场景 |
|------|---------------|----------|
| `"opaque"`（默认） | 始终显示为`0` | 用于外部共享可用性信息 |
| `"full"` | 显示实际可用日历数量 | 仅用于内部使用 |

## 工具参数说明

| 参数 | 值 | 含义 |
|----------|-------|---------|
| `readOnlyHint` | `false` | 允许创建日历事件 |
| `destructiveHint` | `false` | 禁止删除或修改现有事件 |
| `idempotentHint` | `false` | 同一调用可能生成多个事件 |
| `openWorldHint` | `true` | 允许调用外部API |

## 工具参数说明（`book_slot`）

| 参数 | 值 | 含义 |
|----------|-------|---------|
| `readOnlyHint` | `false` | 允许创建日历事件 |
| `destructiveHint` | `false` | 禁止删除或修改现有事件 |
| `idempotentHint` | `false` | 同一调用可能生成多个预订记录 |
| `openWorldHint` | `true` | 允许调用外部API |

## 工具参数说明（`request_booking`）

| 参数 | 值 | 含义 |
|----------|-------|---------|
| `readOnlyHint` | `false` | 允许在他人日历上创建事件 |
| `destructiveHint` | `false` | 禁止删除或修改现有事件 |
| `idempotentHint` | `false` | 同一调用可能生成多个预订记录 |
| `openWorldHint` | `true` | 允许调用外部API |

## 工具参数说明（`compose_proposal`）

| 参数 | 值 | 含义 |
|----------|-------|---------|
| `readOnlyHint` | `true` | 仅进行格式化处理，不修改数据 |
| `destructiveHint` | `false` | 禁止删除数据 |
| `idempotentHint` | `true` | 同一输入始终返回相同结果 |
| `openWorldHint` | `false` | 不会调用外部API |

## 工具参数说明（`search_contacts`）

| 参数 | 值 | 含义 |
|----------|-------|---------|
| `readOnlyHint` | `true` | 仅读取联系人信息，不进行任何修改 |
| `destructiveHint` | `false` | 禁止删除联系人信息 |
| `idempotentHint` | `true` | 同一查询始终返回相同结果 |
| `openWorldHint` | `true` | 会调用外部联系人API（Google People或Microsoft Graph） |

## 错误处理

| 错误类型 | 处理方式 |
|-------|--------|
| “未找到凭证” | 运行`npx @temporal-cortex/cortex-mcp auth google`（或`outlook` / `caldav`）进行认证。|
| “时区未配置” | 提示用户输入IANA时区信息，或运行认证命令进行配置。|
| 时间段已预订/存在冲突 | 使用`find_free_slots`寻找其他可用时间段，并向用户提供选择选项。|
| 预订失败 | 另有代理正在预订同一时间段。稍后重试或提供其他选项。|
| 内容被拒绝 | 重新编写事件摘要/描述。系统会阻止恶意代码的注入。|

## 开放式调度与Temporal Links

当用户启用开放式调度功能后，他们的Temporal Link（`book.temporal-cortex.com/{slug}`）允许他人执行以下操作：

1. **查询可用性**：`GET /public/{slug}/availability?date=YYYY-MM-DD`
2. **预订会议**：`POST /public/{slug}/book`，参数包括`start`、`end`、`title`和`attendee_email`
3. **通过代理卡片查看日历信息**：`GET /public/{slug}/.well-known/agent-card.json`

### 使用流程：通过Temporal Link进行预订
1. 用户分享他们的Temporal Link。
2. 代理调用可用性接口查询空闲时间段。
3. 代理使用选定的时间段调用预订接口。
4. 会议将在用户的默认日历上创建。

详细API文档请参考[Temporal Links参考文档](references/TEMPORAL-LINKS.md)。

## 其他参考资料

- [日历工具参考](references/CALENDAR-TOOLS.md)：所有14个工具的完整输入/输出格式规范。
- [多日历使用指南](references/MULTI-CALENDAR.md)：提供商路由、标签设置、隐私模式及跨日历操作。
- [重复规则指南](references/RRULE-GUIDE.md)：重复规则的使用方式、夏令时处理规则及异常情况处理。
- [预订安全指南](references/BOOKING-SAFETY.md)：双向认证（2PC）机制、并发预订处理、预订锁定的有效期以及内容安全措施。
- [Temporal Links参考](references/TEMPORAL-LINKS.md)：开放式调度接口、代理卡片集成及日历路由方式。
- [开放式调度指南](references/OPEN-SCHEDULING.md)：身份验证流程、公开可用性信息以及通过MCP工具进行外部预订的详细说明。