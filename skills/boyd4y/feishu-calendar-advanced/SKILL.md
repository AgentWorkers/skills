---
name: feishu-calendar-advanced
description: 通过 feishu-agent 进行 Feishu 日历管理：可以查看日历、列出事件，以及创建和删除事件（同时支持冲突检测功能）。
compatibility: darwin,linux
metadata:
  version: 1.0.0
  requires:
    bins:
      - bun
---
# Feishu Calendar 高级功能

使用 `feishu-agent` CLI 工具来管理您的 Feishu（Lark）日历。

## 依赖项

| 依赖项 | 是否必需 | 说明 |
|------------|----------|-------------|
| `bun` | 是 | Bun 运行时环境（用于执行 bunx 命令） |
| `@teamclaw/feishu-agent` | 是 | 通过 bunx 自动安装 |

### 检查依赖项

```bash
# Check bun availability
bun --version
```

## 设置

### 首次设置

1. **安装并配置 feishu-agent**：

```bash
# Interactive setup wizard (recommended)
bunx @teamclaw/feishu-agent setup

# Or manual configuration
bunx @teamclaw/feishu-agent config set appId <your_app_id>
bunx @teamclaw/feishu-agent config set appSecret <your_app_secret>
```

2. **OAuth 授权**：

```bash
bunx @teamclaw/feishu-agent auth
```

3. **验证设置**：

```bash
bunx @teamclaw/feishu-agent whoami
```

## 使用方法

```bash
/feishu-calendar-advanced [command] [options]
```

## 命令

| 命令 | 说明 |
|---------|-------------|
| `calendars` | 列出所有日历（主日历和订阅的日历） |
| `events` | 列出主日历中的事件 |
| `create --summary "会议" --start "2026-03-05 14:00" --end "2026-03-05 15:00"` | 创建新事件 |
| `create --summary "会议" --start "..." --end "..." --attendee user_id` | 创建包含参与者的事件 |
| `delete --event-id <event_id>` | 通过事件 ID 删除事件 |

## 选项

| 选项 | 说明 |
|--------|-------------|
| `--summary` | 事件标题/摘要（创建事件时必需） |
| `--start` | 开始时间，格式为 "YYYY-MM-DD HH:MM"（创建事件时必需） |
| `--end` | 结束时间，格式为 "YYYY-MM-DD HH:MM"（创建事件时必需） |
| `--attendee` | 通过用户 ID 添加参与者（可多次使用） |
| `--event-id` | 事件 ID（删除事件时必需） |

## 示例

```bash
# List all calendars
/feishu-calendar-advanced calendars

# List events in primary calendar
/feishu-calendar-advanced events

# Create a simple event
/feishu-calendar-advanced create --summary "Team Standup" --start "2026-03-05 10:00" --end "2026-03-05 10:30"

# Create event with attendees
/feishu-calendar-advanced create --summary "Project Review" --start "2026-03-05 14:00" --end "2026-03-05 15:00" --attendee user_id_1 --attendee user_id_2

# Delete an event
/feishu-calendar-advanced delete --event-id evt_xxxxxxxxxxxxx
```

## 故障排除

**“需要用户授权”**
- 运行 `bunx @teamclaw/feishu-agent auth` 进行授权

**“令牌过期”**
- 再次运行 `bunx @teamclaw/feishu-agent auth` 以刷新令牌

**“检测到时间冲突”**
- 所请求的时间段已被占用
- 选择其他时间，或使用 `bunx @teamclaw/feishu-agent calendar events` 查看日历

**“权限被拒绝”**
- 在 Feishu 开发者控制台中检查应用权限
- 必需的权限：`calendar:calendar`、`calendar:event`