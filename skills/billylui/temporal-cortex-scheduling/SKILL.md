---
name: temporal-cortex-scheduling
description: 在 Google Calendar、Outlook 和 CalDAV 中列出事件、查找空闲时间并预订会议。支持多日历的可用性合并、重复事件的扩展功能，以及采用两阶段提交（Two-Phase Commit）机制来防止冲突。
  List events, find free slots, and book meetings across Google Calendar, Outlook, and CalDAV. Multi-calendar availability merging, recurring event expansion, and atomic booking with Two-Phase Commit conflict prevention.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker for the MCP server. Stores OAuth credentials at ~/.config/temporal-cortex/. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.5.8"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
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
# 日历调度与预订

共有8个工具可用于日历发现、事件查询、空闲时段查找、可用性检查、RRULE规则扩展以及原子级预订操作。其中7个工具为只读模式，1个工具（`book_slot`）支持写入操作。

## 运行时环境

这些工具运行在[Temporal Cortex MCP服务器](https://github.com/temporal-cortex/mcp)（版本`@temporal-cortex/cortex-mcp@0.5.8`）内部，该服务器是一个用Rust语言编写的二进制文件，通过npm包进行分发。

**启动时的流程：**
1. `npx`命令从npm注册表下载`@temporal-cortex/cortex-mcp@0.5.8`（仅下载一次，会缓存到本地）。
2. MCP服务器作为本地进程启动，并通过标准输入输出（stdio）与客户端进行通信。
3. 日历相关工具会向您配置的日历服务提供商（如Google Calendar API、Microsoft Graph API或CalDAV端点）发送经过身份验证的API请求。

**凭证存储：** OAuth令牌存储在`~/.config/temporal-cortex/credentials.json`文件中，并仅在本地使用，不会发送到Temporal Cortex服务器。

**文件访问权限：** 该二进制文件仅读取和写入`~/.config/temporal-cortex/`目录下的文件（包括凭证和配置信息），不会访问其他文件系统。

**网络范围：** 日历工具仅连接到您配置的日历服务提供商（`googleapis.com`、`graph.microsoft.com`或您的CalDAV服务器），不会发送任何回调请求到Temporal Cortex服务器。默认情况下，这些工具不记录使用数据（即关闭了遥测功能）。

**验证机制：** 每次[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases)都会附带SHA256校验和文件（`SHA256SUMS.txt`），并嵌入到npm包中，以便在安装后自动进行验证。您也可以手动验证。

**来源与许可证：** 该项目托管在[github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)，采用MIT许可证。二进制文件是通过[GitHub Actions](https://github.com/temporal-cortex/mcp/actions)从公开的Rust源代码构建的。

**容器化部署：** 可将此工具部署在容器中以实现完全隔离。具体配置方法请参考[router skill](https://github.com/temporal-cortex/skills/blob/main/skills/temporal-cortex/SKILL.md#mcp-server-connection)。

## 工具分类

### 第0层：日历发现
| 工具 | 使用场景 |
|------|------------|
| `list_calendars` | 在不知道有哪些日历可用时首次调用。返回所有已连接的日历信息，包括日历ID、名称、标签、状态及访问权限。 |

### 第2层：日历操作
| 工具 | 使用场景 |
|------|------------|
| `list_events` | 列出指定时间范围内的事件。默认输出格式为TOON格式（相比JSON格式节省约40%的请求令牌数量）。在处理多个日历时，使用带有提供商前缀的ID（例如`"google/primary"`、`"outlook/work"`）。 |
| `find_free_slots` | 查找日历中的空闲时段。可通过`min_duration_minutes`参数设置最小时段长度。 |
| `expand_rrule` | 将RRULE规则（RFC 5545标准）解析为具体的事件实例。支持夏令时（DST）、日期范围（BYSETPOS）、日期截止（EXDATE）以及闰年处理。请使用`dtstart`参数指定本地日期时间（不包含时区信息）。 |
| `check_availability` | 检查指定时间段是否可用。会同时检查该时间段内是否有事件或预订占用。 |

### 第3层：跨日历的可用性检查
| 工具 | 使用场景 |
|------|------------|
| `get_availability` | 合并多个日历的可用性信息（空闲/忙碌状态）。需要传递`calendar_ids`数组。隐私设置选项包括`"opaque"`（默认值，隐藏日历来源信息）或`"full"`。 |

### 第4层：预订操作
| 工具 | 使用场景 |
|------|------------|
| `book_slot` | 原子级预订某个时间段。流程包括锁定、验证、写入数据以及释放预订状态。**务必先调用`check_availability`进行检查。** |

**重要规则：**
1. **先发现日历**：在不知道哪些日历可用时，必须先调用`list_calendars`。后续的所有请求都应使用返回的、带有提供商前缀的日历ID。
2. **使用带有提供商前缀的ID**：在处理多个日历时，使用`"google/primary"`、`"outlook/work"`、`"caldav/personal"`等前缀来区分不同的日历服务。
3. **默认输出格式为TOON**：输出数据采用TOON格式（更节省请求令牌）。只有在需要结构化数据解析时，才使用`format: "json"`格式。
4. **预订前必须检查**：在调用`book_slot`之前，务必先使用`check_availability`确保时间段未被占用。
5. **内容安全**：事件摘要和描述在发送到日历API之前会经过安全过滤处理。
6. **时区处理**：所有工具都支持包含时区偏移量的RFC 3339格式；切勿使用纯日期格式。

## 完整的预订流程

如果步骤4中发现时间段已被占用，可以使用`find_free_slots`来寻找其他可用选项。

## 两阶段提交协议

如果任何步骤失败，系统会立即释放预订状态并终止预订操作。不允许进行部分数据的写入。

## 常用操作模式
- **列出本周事件**  
- **查找多个日历中的空闲时间**  
- **检查并预订时间段**  
- **扩展重复事件**  

## 日历ID的格式规范

所有日历ID都采用以下格式，其中前缀表示对应的日历服务提供商：
| 格式 | 示例 | 对应的API路由 |
|--------|---------|-----------|
| `google/<id>` | `"google/primary"` | Google Calendar |
| `outlook/<id>` | `"outlook/work"` | Microsoft Outlook |
| `caldav/<id>` | `"caldav/personal"` | CalDAV（iCloud、Fastmail） |
| `<id>`（无前缀） | `"primary"` | 默认日历服务 |

## 隐私设置
| 隐私模式 | `source_count` | 使用场景 |
|------|---------------|----------|
| `"opaque"`（默认） | 始终显示`0` | 隐藏日历来源信息，适用于外部共享 |
| `"full"` | 显示实际占用日历的数量 | 仅用于内部查看 |

## `book_slot`工具的额外配置选项
| 属性 | 值 | 含义 |
|----------|-------|---------|
| `readOnlyHint` | `false` | 允许创建新的日历事件 |
| `destructiveHint` | `false` | 禁止删除或覆盖现有事件 |
| `idempotentHint` | `false` | 同一请求不会重复创建事件 |
| `openWorldHint` | `true` | 允许进行外部API调用 |

## 错误处理机制
- 如果找不到凭证，运行`npx @temporal-cortex/cortex-mcp@0.5.8 auth google`（或`outlook`/`caldav`）来获取凭证。
- 如果未配置时区，系统会提示用户输入IANA时区信息或自动配置时区。
- 如果时间段已被占用或检测到冲突，系统会使用`find_free_slots`提供替代选项。
- 如果预订请求失败（例如因其他工具正在预订同一时间段），系统会提示用户重新选择时间或稍后重试。
- 如果系统检测到不安全的内容（如恶意代码），会重新生成事件摘要/描述。

**相关参考资料：**
- [日历工具参考](references/CALENDAR-TOOLS.md)：所有8个工具的输入/输出数据格式说明。
- [多日历使用指南](references/MULTI-CALENDAR.md)：日历服务提供商的路由规则、标签设置、隐私模式及跨服务操作说明。
- [RRULE规则指南](references/RRULE-GUIDE.md)：RRULE规则的详细说明及特殊处理方式。
- [预订安全指南](references/BOOKING-SAFETY.md)：双重认证机制、并发预订处理、预订状态的有效期设置以及内容安全策略。