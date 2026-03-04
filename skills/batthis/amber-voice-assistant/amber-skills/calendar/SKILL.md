---
name: calendar
version: 1.2.0
description: "查询和管理操作员的日历——查看可用时间并创建新的日程条目"
metadata: {"amber": {"capabilities": ["read", "act"], "confirmation_required": false, "timeout_ms": 5000, "permissions": {"local_binaries": ["ical-query"], "telegram": false, "openclaw_action": false, "network": false}, "function_schema": {"name": "calendar_query", "description": "Check the operator's calendar availability or create a new entry. PRIVACY RULE: When reporting availability to callers, NEVER disclose event titles, names, locations, or any details about what the operator is doing. Only share whether they are free or busy at a given time (e.g. 'free from 2pm to 4pm', 'busy until 3pm'). Treat all calendar event details as private and confidential.", "parameters": {"type": "object", "properties": {"action": {"type": "string", "enum": ["lookup", "create"], "description": "Whether to look up availability or create a new event"}, "range": {"type": "string", "description": "For lookup: today, tomorrow, week, or a specific date like 2026-02-23", "pattern": "^(today|tomorrow|week|\\d{4}-\\d{2}-\\d{2})$"}, "title": {"type": "string", "description": "For create: the event title", "maxLength": 200}, "start": {"type": "string", "description": "For create: start date-time like 2026-02-23T15:00", "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}$"}, "end": {"type": "string", "description": "For create: end date-time like 2026-02-23T16:00", "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}$"}, "calendar": {"type": "string", "description": "Optional: specific calendar name", "maxLength": 100}, "notes": {"type": "string", "description": "For create: event notes", "maxLength": 500}, "location": {"type": "string", "description": "For create: event location", "maxLength": 200}}, "required": ["action"]}}}}
---
# 日历功能

通过 `ical-query` 查询操作员的日历可用性，并创建新的日历条目。

## 功能

- **读取**：查询今天、明天、本周或特定日期的可用时间。
- **创建**：创建新的日历条目。

## 隐私规则

**事件详情绝不会向呼叫者透露。** 这一规则通过两个层面来执行：

1. **处理程序层面**：处理程序在返回结果之前，会从 `ical-query` 的输出中删除所有事件标题、名称、地点和备注信息，仅返回空闲/忙碌的时间段（开始/结束时间）。
2. **模型层面**：函数描述指示 Amber 仅提供可用时间信息（例如：“今天下午2点到4点有空”），而不会透露具体是哪些事件。

Amber 应该这样回答：
- ✅ “今天下午2点到4点操作员有空。”
- ✅ “他们下午3点之前很忙，之后全天都有空。”
- ❌ “他们下午2点有与John的会议。” ← 绝不这样回答。
- ❌ “他们上午10点到11点在看牙医。” ← 绝不这样回答。

## 安全性（三层防护）

输入验证在三个独立层面进行：

1. **模式层面**：`range` 的格式为 `^(today|tomorrow|week|\d{4}-\d{2}-\d{2})$`；`start`/`end` 的格式为 `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$`；自由文本字段有长度限制。大型语言模型（LLM）无法生成不符合格式的输入。
2. **处理程序层面**：在执行任何操作之前会进行显式验证；即使绕过了模式验证，也会拒绝不符合预期格式的输入。
3. **执行层面**：`context.exec()` 接受一个 `string[]` 类型的参数，并使用 `execFileSync`（不启动shell）进行执行；参数以离散的字符串形式传递，而不是通过shell进行解析。

## 其他说明

- 使用 `/usr/local/bin/ical-query` 进行查询；不涉及网络访问或网关中转。
- 执行速度快：直接调用本地二进制文件（约100毫秒）。
- 日历名称是可选的；默认使用操作员的主要日历。