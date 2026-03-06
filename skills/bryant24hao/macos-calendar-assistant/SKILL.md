---
name: macos-calendar-assistant
description: 在以即时通讯（如 Telegram/Discord/Feishu/iMessage/Slack）为主的工作流程中，使用 OpenClaw 管理 macOS 日历。支持的功能包括：从截图中提取事件信息、执行创建/更新/移动/延长/重新安排事件的操作（这些操作具有幂等性）、设置提醒、检查事件冲突、每日同步日历内容以及清理重复事件。当用户需要添加/编辑/移动/推迟事件、解析日历截图或聊天消息、将每周计划调整为每日执行任务，或者希望保持日历内容与备注同步时，可以使用该工具。
---
# macOS-calendar-assistant

使用内置的脚本来可靠地操作 Calendar.app。

## 工作流程

1. 提取事件的标题、开始时间/结束时间、时区、日历、地点、备注以及闹钟信息。
2. 在写入数据之前检查是否存在冲突：
   - `scripts/list_events.swift <start_iso> <end_iso>`
3. 优先使用幂等性的写入操作（即多次执行不会产生不同结果）：
   - `scripts/upsert_event.py`（用于创建、更新或跳过事件）
4. 如果需要设置闹钟，请执行以下操作：
   - `scripts/set_alarm.py --uid <event_uid> --alarm-minutes <n>`
5. 为确保数据一致性，执行重复扫描：
   - `scripts/calender_clean.py --start <iso> --end <iso>`

## 日历分类规则

- 锻炼/跑步/训练 → `Training`
- 工作/会议/客户 → `Work`
- 产品/开发/构建 → `Product`
- 个人/社交/旅行 → `Life`
- 如果未指定类别：优先使用可写入的 iCloud/CalDAV 日历，而非本地日历。

> 注意：日历的名称可能因用户设置而有所不同。在写入数据之前，请将用户意图映射到最匹配的本地日历名称。

## 命令

### 列出所有日历
```bash
swift scripts/list_calendars.swift
```

### 列出指定时间范围内的事件
```bash
swift scripts/list_events.swift "2026-03-06T00:00:00+08:00" "2026-03-06T23:59:59+08:00"
```

输出结果中会包含事件的 `uid`，以便后续进行闹钟设置或编辑操作。

### 创建/更新事件（推荐使用幂等性操作）
```bash
python3 scripts/upsert_event.py \
  --title "Team sync" \
  --start "2026-03-06T19:00:00+08:00" \
  --end "2026-03-06T20:00:00+08:00" \
  --calendar "Work" \
  --notes "Agenda" \
  --location "Online" \
  --alarm-minutes 15
```

操作结果可能是 `CREATED`、`UPDATED` 或 `SKIPPED`。
可以使用 `--dry-run` 选项进行预览。

### 传统方式直接添加事件（会创建新事件）
```bash
python3 scripts/add_event.py --title "..." --start "..." --end "..."
```

### 根据 `uid` 设置闹钟
```bash
python3 scripts/set_alarm.py --uid "EVENT_UID" --alarm-minutes 15
```

### 移动事件（传统工具）
```bash
swift scripts/move_event.swift "Team sync" "Work" "2026-03-07T10:00:00+08:00" 60 --search-days 7
# optional precise match:
# --original-start "2026-03-06T10:00:00+08:00"
```
对于大多数重新安排事件的操作，建议使用 `upsert_event.py`；在需要基于事件标题直接移动事件时，可以使用 `move_event.swift`。

### 执行重复扫描/清理操作
```bash
python3 scripts/calendar_clean.py --start "2026-03-01T00:00:00+08:00" --end "2026-03-08T23:59:59+08:00"
python3 scripts/calendar_clean.py --start "..." --end "..." --apply --confirm yes --snapshot-out ./delete-plan.json
```

### 查看未来 2 小时内的事件
```bash
python3 scripts/within_2h.py
```

### 环境配置与测试
```bash
python3 scripts/env_check.py
python3 scripts/regression_test.py
scripts/smoke_test.sh
```

### 每日自动检查通知功能
```bash
scripts/install.sh     # run env check + install cron from config.json
scripts/uninstall.sh   # remove cron
```

## 数据提取与调度策略（基于实际使用情况）

1. **从聊天截图中判断事件所有者**
   - 将用户的消息气泡视为主要意图。
   - 将对方的消息气泡视为约束条件（如可用时间或旅行安排），而不是自动创建任务的依据。

2. **冲突处理规则**
   - 如果用户明确表示“覆盖”某个事件（例如“替换这个时间安排”），则允许替换现有事件并重新安排。
   - 如果用户没有明确表示，系统会发出警告并询问用户的确认。

3. **时间窗口的解析**
   - 如“下午 4–6 点”这样的表述应首先被理解为用户的可用时间窗口。
   - 只有在用户确认后，才会将其转换为正式的事件记录。

4. **事件重新安排的优先级**
   - 优先安排灵活性的事件（如锻炼或非强制性的任务），然后再安排重要的工作任务。
   - 除非用户明确要求，否则不要自动移动重要任务。

5. **确认提示模板**
   - 使用以下提示：“我理解您的意图是 X，对方的约束条件是 Y。我将按照 Z 来操作。您确认吗？”
   - 保持提示简洁；当用户的意图已经明确时，避免重复确认。

## 系统要求与限制

- 仅支持 macOS 系统（需要 EventKit 和 Calendar 权限）。
- 当用户未指定时，系统使用 `config.json.timezone` 中设置的默认时区（默认为 Asia/Shanghai）。
- 请在查看预览结果（`--dry-run`）后，再使用 `--apply` 选项来应用更改。