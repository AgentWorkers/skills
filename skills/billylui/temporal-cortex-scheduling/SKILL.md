---
name: temporal-cortex-scheduling
description: 在 Google 日历、Outlook 和 CalDAV 中列出事件、查找空闲时间并预订会议。支持多日历的可用性合并、重复事件的扩展功能，以及采用两阶段提交（Two-Phase Commit）机制来防止冲突。
  List events, find free slots, and book meetings across Google Calendar, Outlook, and CalDAV. Multi-calendar availability merging, recurring event expansion, and atomic booking with Two-Phase Commit conflict prevention.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.6.2"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
  openclaw:
    install:
      - kind: node
        package: "@temporal-cortex/cortex-mcp@0.6.2"
        bins: [cortex-mcp]
    requires:
      bins:
        - npx
      config:
        - ~/.config/temporal-cortex/credentials.json
        - ~/.config/temporal-cortex/config.json
---
# 日历调度与预订

共有8个工具可用于日历查询、事件查找、空闲时间段的查找、可用性检查、RRULE规则的扩展以及原子级的预订操作。其中包括7个只读工具和1个可写工具（`book_slot`）。

## 运行时环境

这些工具运行在[Temporal Cortex MCP服务器](https://github.com/temporal-cortex/mcp)（版本`@temporal-cortex/cortex-mcp@0.6.2`）内部，该服务器是一个编译后的Rust二进制文件，通过npm包进行分发。

**安装与启动流程：**
1. 使用`npx`从npm仓库下载`@temporal-cortex/cortex-mcp@0.6.2`（首次下载后会在本地缓存）。
2. 安装后的脚本会从[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.6.2)下载特定平台的二进制文件，并通过`checksums.json`文件验证其SHA256校验和；如果校验和不一致，则安装过程将停止。
3. MCP服务器作为本地进程启动，通过标准输入输出（stdio）与外部服务通信（不开放监听端口）。
4. 日历工具会向您配置的提供者（如Google Calendar API、Microsoft Graph API或CalDAV端点）发送经过身份验证的API请求。

**凭证存储：**OAuth令牌存储在`~/.config/temporal-cortex/credentials.json`文件中，仅由本地MCP服务器进程读取。任何凭证数据都不会传输到Temporal Cortex服务器。二进制文件的文件系统访问权限仅限于`~/.config/temporal-cortex/`目录——这一点可以通过查看[开源Rust代码](https://github.com/temporal-cortex/mcp)或在使用Docker时确认（Docker中的挂载目录是唯一可写路径）。

**文件访问权限：**该二进制文件仅读写`~/.config/temporal-cortex/`目录中的凭证和配置文件，不会修改其他文件系统内容。

**网络范围：**日历工具仅连接到您配置的提供者服务器（`googleapis.com`、`graph.microsoft.com`或CalDAV服务器），不会向Temporal Cortex服务器发送回调数据。默认情况下，这些工具不启用数据监控功能。

**使用前的验证建议：**
1. 在实际使用前，先执行`npm pack @temporal-cortex/cortex-mcp@0.6.2 --dry-run`命令来检查包内容。
2. 独立验证[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/download/mcp-v0.6.2/SHA256SUMS.txt)中的校验和值。
3. 为了确保安全性，建议在Docker环境中运行该工具（而非使用`npx`）。

**验证机制：**每次[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.6.2)都会附带`SHA256SUMS.txt`文件，以供用户在使用前验证二进制文件的完整性。

**安全性措施：**npm包中嵌入了`checksums.json`文件，安装脚本会在安装过程中验证SHA256哈希值；如果哈希值不一致，安装过程将停止（此时二进制文件会被删除而不会被执行）。这种自动化验证机制是对上述独立验证的补充，但并不能完全替代它。

**构建过程：**二进制文件是通过[GitHub Actions](https://github.com/temporal-cortex/mcp/actions)在5个平台上（darwin-arm64、darwin-x64、linux-x64、linux-arm64、win32-x64）交叉编译得到的。源代码托管在[github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（采用MIT许可证）。整个构建流程、构建结果和发布时的校验和信息都是公开可查的。

**Docker安全机制：**在Docker环境中运行时，主机上不安装Node.js，并通过卷挂载实现凭证隔离。

### 工具列表

| 工具 | 使用场景 |
|------|------------|
| `list_calendars` | 在不知道有哪些日历可用时首次调用。返回所有已连接的日历信息，包括提供者前缀、日历名称、标签、状态及访问权限。 |
| `list_events` | 在指定时间范围内列出事件。默认输出格式为TOON格式（相比JSON格式节省约40%的字符数量）。对于多个日历的情况，使用提供者前缀来区分日历（例如：`"google/primary"`、`"outlook/work"`）。 |
| `find_free_slots` | 查找日历中的空闲时间段。可以通过`min_duration_minutes`参数设置最小时间段长度。 |
| `expand_rrule` | 将RRULE规则（RFC 5545标准）解析为具体的事件实例。支持夏令时、BYSETPOS、EXDATE以及闰年处理。使用`dtstart`参数指定本地时间（不包含时区信息）。 |
| `check_availability` | 检查指定时间段是否可用。同时会检查该时间段内是否有事件或预订冲突。 |
| `get_availability` | 合并多个日历的空闲/忙碌状态信息。可以通过`calendar_ids`参数传递多个日历的ID。隐私设置选项包括`"opaque"`（默认值，隐藏日历来源）和`"full"`。 |
| `book_slot` | 原子级预订某个时间段。操作流程包括锁定、检查可用性、写入预订信息并最终释放预订状态。**务必先调用`check_availability`。** |

**重要规则：**
1. **先获取日历列表**：在不知道哪些日历可用时，先调用`list_calendars`函数。后续的所有操作都应使用该函数返回的提供者前缀标识符。
2. **多日历环境下的标识符使用规则**：使用`"google/primary"`、`"outlook/work"`、`"caldav/personal"`等前缀来区分不同的日历提供者。如果仅提供日历ID（如`"primary"`），系统会使用默认提供者。
3. **默认输出格式为TOON**：输出采用TOON格式（更简洁）。只有在需要结构化数据解析时才使用`format: "json"`格式。
4. **预订前必须检查可用性**：在调用`book_slot`之前，务必先执行`check_availability`函数，以避免预订冲突。
5. **内容安全**：事件摘要和描述在传递给日历API之前会经过安全过滤处理。
6. **时区处理**：所有工具都支持包含时区偏移量的RFC 3339格式；禁止使用纯日期格式。

## 完整的预订流程（如果步骤4中时间段已被预订，则使用`find_free_slots`寻找替代时间）

### 两阶段提交协议

如果任何步骤失败，系统会立即释放已预订的状态并终止预订操作，不会进行部分性的数据写入。

### 常用操作模式：

- **列出本周事件**
- **查找多个日历中的空闲时间**
- **检查并预订时间段**
- **扩展重复事件**

### 日历ID的命名规则

所有日历ID都采用以下格式：
| 格式 | 例子 | 对应的API路径 |
|--------|---------|-----------|
| `google/<id>` | `"google/primary"` | Google Calendar |
| `outlook/<id>` | `"outlook/work"` | Microsoft Outlook |
| `caldav/<id>` | `"caldav/personal"` | CalDAV（iCloud、Fastmail） |
| `<id>`（无前缀） | `"primary"` | 默认提供者 |

## 隐私设置

| 隐私模式 | `source_count` | 使用场景 |
|------|---------------|----------|
| `"opaque"`（默认） | 始终显示`0` | 隐藏日历来源信息 |
| `"full"` | 显示实际占用情况 | 仅用于内部查看 |

### `book_slot`工具的配置选项

| 参数 | 值 | 含义 |
|----------|-------|---------|
| `readOnlyHint` | `false` | 允许创建新的日历事件 |
| `destructiveHint` | `false` | 禁止删除或覆盖现有事件 |
| `idempotentHint` | `false` | 同一请求不会重复创建事件 |
| `openWorldHint` | `true` | 允许进行外部API调用 |

## 错误处理机制

| 错误类型 | 处理方式 |
|-------|--------|
| “未找到凭证” | 运行`npx @temporal-cortex/cortex-mcp@0.6.2 auth google`（或`outlook` / `caldav`）命令进行认证。 |
| “时区未配置” | 提示用户输入IANA时区信息，或手动运行认证命令进行配置。 |
| 时间段已被预订/存在冲突 | 使用`find_free_slots`寻找其他可用时间段，并向用户展示可选选项。 |
| 锁定失败 | 可能有其他进程正在预订同一时间段，建议用户稍后重试或选择其他时间。 |
| 内容被安全过滤系统拒绝 | 重新生成事件摘要/描述。系统会阻止恶意代码的注入。 |

**附加参考资料：**
- [日历工具参考文档](references/CALENDAR-TOOLS.md)：包含所有8个工具的输入/输出格式规范。
- [多日历使用指南](references/MULTI-CALENDAR.md)：介绍日历提供者路由、标签设置、隐私模式及跨提供者操作。
- [RRULE规则指南](references/RRULE-GUIDE.md)：解释RRULE规则的格式及处理特殊情况。
- [预订安全指南](references/BOOKING-SAFETY.md)：详细介绍双向认证机制、并发预订处理、预订状态的过期时间以及内容安全措施。