---
name: icloud-caldav
description: 通过 CalDAV 协议直接集成 iCloud 日历功能。用户可以无需借助第三方服务即可创建、读取、更新和删除日历事件。适用于需要管理 iCloud 日历、查看日程安排、创建事件或查找空闲时间的场景。使用该功能需具备 Apple ID 以及应用程序指定的密码。
---
# iCloud CalDAV — 直接访问日历

您可以通过CalDAV协议直接管理iCloud日历。无需使用任何第三方服务，数据只会传输到Apple的服务器，而不会离开您的设备。

## 使用场景

**在用户需要以下操作时激活此技能：**
- 查看日历或即将发生的事件
- 创建新的日历事件
- 删除现有的事件
- 列出可用的日历

**不适用于以下场景：**
- 设置提醒（如可用，请使用`apple-reminders`技能）
- 管理联系人（CalDAV仅支持日历数据）
- 非iCloud日历（如Google、Outlook等）

## 先决条件

**所需凭证：**
- `APPLE_ID` — 您的Apple ID邮箱地址
- `APPLE_APP_PASSWORD` — [特定于应用的密码](https://appleid.apple.com)（并非您的常规Apple ID密码）

**生成特定于应用的密码：**
1. 访问[appleid.apple.com](https://appleid.apple.com)
2. 登录 → 点击“登录与安全” → “应用专用密码”
3. 生成新密码
4. 使用此密码（而非您的常规密码）

## 快速入门

```bash
# Set credentials
export APPLE_ID="your.email@icloud.com"
export APPLE_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"

# List calendars
./scripts/caldav.py list-calendars

# List events for next 7 days
./scripts/caldav.py list-events --days 7

# Create an event
./scripts/caldav.py create-event \
  --title "Team Meeting" \
  --start "2025-07-23T14:00:00" \
  --duration 60 \
  --calendar "Work"
```

## 可用的操作

| 操作          | 命令                | 描述                                      |
|------------------|------------------|-----------------------------------------|
| 列出日历        | `list-calendars`       | 显示所有iCloud日历                          |
| 列出事件        | `list-events`        | 在指定日期范围内列出事件                        |
| 创建事件        | `create-event`       | 添加新的日历事件                         |
| 删除事件        | `delete-event`       | 根据文件名或UID删除事件                         |

## 工作流程示例

### 创建事件

```bash
# Basic event
./scripts/caldav.py create-event \
  --title "Dentist Appointment" \
  --start "2025-07-25T09:30:00" \
  --duration 30

# With location and description
./scripts/caldav.py create-event \
  --title "Project Review" \
  --start "2025-07-26T14:00:00" \
  --duration 60 \
  --location "Conference Room B" \
  --description "Q3 planning review" \
  --calendar "Work"

# All-day event
./scripts/caldav.py create-event \
  --title "Vacation" \
  --start "2025-08-01" \
  --all-day
```

### 批量操作

**注意：** CalDAV不支持原生的批量操作。若需创建多个事件，请多次运行相应命令。

```bash
# Create multiple events by running the command multiple times
./scripts/caldav.py create-event --title "Meeting 1" --start "2025-07-26T10:00:00" --duration 60
./scripts/caldav.py create-event --title "Meeting 2" --start "2025-07-26T14:00:00" --duration 60
./scripts/caldav.py create-event --title "Meeting 3" --start "2025-07-27T09:00:00" --duration 60
```

iCloud能够很好地处理大量的连续请求，但无法通过单次API调用同时创建多个事件。

### 删除事件

```bash
# Delete by filename
./scripts/caldav.py delete-event \
  --file "event-name.ics" \
  --calendar "Calendar"

# Delete by UID (searches calendar for matching event)
./scripts/caldav.py delete-event \
  --uid "openclaw-xxx@openclaw.local" \
  --calendar "Calendar"
```

**警告：** 删除操作是不可逆的。虽然iCloud可能具有备份机制，但标准的CalDAV DELETE命令会立即删除事件。

## 日期/时间格式

- **ISO 8601**：`2025-07-23T14:00:00`（若未指定时区，则使用本地时区）
- **带时区**：`2025-07-23T14:00:00+08:00`
- **全天事件**：`2025-07-23`（仅显示日期）

## 安全注意事项

- 凭证仅从环境变量中读取，不会被记录或存储
- 所有通信均通过HTTPS与`caldav.icloud.com`进行
- 特定于应用的密码可以在appleid.apple.com随时撤销

## 错误处理

| 错误代码 | 原因                | 解决方案                                      |
|---------|------------------|-----------------------------------------|
| 401 未经授权 | 凭证错误             | 检查APPLE_ID和APPLE_APP_PASSWORD是否正确             |
| 404 未找到       | 日历/事件不存在           | 先尝试列出日历/事件                        |
| 403 禁止访问     | 仅允许读取日历           | 尝试其他日历                         |
| 超时        | 网络问题             | 重试请求                         |

## 参考资料

- 有关CalDAV实现的详细信息，请参阅`references/caldav-protocol.md`
- 有关iCloud特定端点的详细信息，请参阅`references/icloud-endpoints.md`