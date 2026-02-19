---
name: bun-do-api
description: 管理待办事项（bun-do tasks）和项目：可以添加任务、编辑任务、删除任务、标记任务为已完成状态、管理子任务以及记录项目进度。适用于用户执行以下操作时：添加待办事项、更新任务、删除任务、标记任务为已完成、添加子任务、记录进度、更新项目状态等。同时，也适用于代理完成任务后需要记录进度的情况。触发条件包括：待办事项（todo）、任务（task）、提醒我（remind me）、截止日期（due）、付款（payment）、账单（bill）、待办事项列表（backlog）、我需要做什么（what do I need to do）、过期事项（what's overdue）等。
---
# bun-do — 你的本地任务管理工具

> “添加任务：更新护照（截止日期为3月30日），每年重复一次，费用为85欧元”

bun-do 是一个以本地任务管理为核心的应用程序，它提供 REST API，地址为 `http://localhost:8000`。所有数据都以 JSON 格式存储在磁盘上，不会离开用户的设备。

**启动方式**：`bun-do start`（安装方式：`bun install -g bun-do`）
**数据存储路径**：`~/.bun-do/`（可自定义：`BUNDO_DATA_DIR`）
**端口号**：8000（可自定义：`--port=PORT`）

## 用户操作与 API 调用的对应关系

| 用户操作 | 对应的 API 调用 |
|-----------|--------|
| “添加任务：购买牛奶” | POST `/api/tasks` `{“title”: “Buy milk”}` |
| “提醒我明天去看牙医” | POST `{“title”: “Call dentist”, “date”: “TOMORROW”, “type”: “reminder”}` |
| “任务 P0 的截止日期：周五前提交提案” | POST `{“title”: “Submit proposal”, “date”: “FRIDAY”, “priority”: “P0”, “type”: “deadline”}` |
| “添加定期付款任务：每月1日支付1200欧元” | POST `{“title”: “Rent”, “type”: “payment”, “amount”: “1200”, “currency”: “EUR”, “recurrence”: {“type”: “monthly”, “day”: 1}}` |
| “有哪些任务逾期了？” | GET `/api/tasks`，筛选条件为 `done=false` 且 `date < today` |
| “将护照更新任务标记为已完成” | 根据任务标题查询后，使用 PUT 方法 `{“done”: true}` |
| “我今天应该做什么？” | GET `/api/tasks`，筛选出今天的任务并按优先级排序 |
| “将任务推迟到下周” | 使用 PUT 方法 `{“date”: “NEXT_MONDAY”}` |
| “添加子任务：预订航班” | POST `/api/tasks/{id}/subtasks` `{“title”: “Book flight”}` |
| “在 bun-do 中记录进度：版本 1.3 已发布” | POST `/api/projects/{id}/entries` `{“summary”: “Shipped v1.3”}` |

**重要提示**：在发送请求之前，务必将所有相对日期（如 “明天”、“下周一”）转换为 `YYYY-MM-DD` 格式。

## API 参考文档

| 功能 | 方法 | API 路径 |
|--------|--------|----------|
| 列出所有任务 | GET | `/api/tasks` |
| 添加任务 | POST | `/api/tasks` |
| 编辑任务 | PUT | `/api/tasks/{id}` |
| 删除任务 | DELETE | `/api/tasks/{id}` |
| 添加子任务 | POST | `/api/tasks/{id}/subtasks` |
| 编辑子任务 | PUT | `/api/tasks/{id}/subtasks/{sid}` |
| 删除子任务 | DELETE | `/api/tasks/{id}/subtasks/{sid}` |
| 重新排序任务列表 | POST | `/api/tasks/reorder` |
| 清除已完成的任务 | POST | `/api/tasks/clear-done` |
| 列出所有项目 | GET | `/api/projects` |
| 添加项目 | POST | `/api/projects` |
| 编辑项目 | PUT | `/api/projects/{id}` |
| 删除项目 | DELETE | `/api/projects/{id}` |
| 添加项目日志记录 | POST | `/api/projects/{id}/entries` |
| 删除项目日志记录 | DELETE | `/api/projects/{id}/entries/{eid}` |

## 任务字段说明

```json
{
  "title": "string (required)",
  "date": "YYYY-MM-DD (default: today)",
  "priority": "P0 | P1 | P2 | P3 (default: P2)",
  "type": "task | deadline | reminder | payment (default: task)",
  "notes": "string",
  "done": false,
  "amount": "string (for payments)",
  "currency": "CHF | USD | EUR | BRL (default: CHF)",
  "recurrence": null | {"type": "weekly", "dow": 0-6} | {"type": "monthly", "day": 1-31} | {"type": "yearly", "month": 1-12, "day": 1-31}
}
```

**优先级**：
- P0：紧急任务，必须立即处理
- P1：高优先级任务，今天必须完成
- P2：普通任务
- P3：待处理任务（不显示在日历中）

**任务类型**：
- `task`：可执行的任务
- `deadline`：有固定截止日期的任务
- `reminder`：用于提醒的任务
- `payment`：用于跟踪账单/发票的任务

**重复性设置**：
- 当重复性任务被标记为已完成时，系统会自动创建下一次任务的记录。

## Curl 命令示例

### 在执行任何操作之前，请先检查服务器是否运行中

```bash
curl -sf http://localhost:8000/api/tasks > /dev/null && echo "OK" || echo "Server not running — run: bun-do start"
```

### 添加新任务

```bash
curl -s -X POST http://localhost:8000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title": "Buy milk", "date": "2026-03-01", "priority": "P2"}'
```

### 添加定期付款任务

```bash
curl -s -X POST http://localhost:8000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title": "Server hosting", "date": "2026-03-01", "priority": "P1", "type": "payment", "amount": "29", "currency": "USD", "recurrence": {"type": "monthly", "day": 1}}'
```

### 根据任务标题查找任务并获取其 ID

```bash
curl -s http://localhost:8000/api/tasks | python3 -c "
import sys, json
for t in json.load(sys.stdin)['tasks']:
    if 'SEARCH' in t['title'].lower(): print(t['id'], t['title'])
"
```

### 编辑任务（仅发送需要修改的字段）

```bash
curl -s -X PUT http://localhost:8000/api/tasks/TASK_ID \
  -H 'Content-Type: application/json' \
  -d '{"priority": "P0", "date": "2026-03-15"}'
```

### 将任务标记为已完成

```bash
curl -s -X PUT http://localhost:8000/api/tasks/TASK_ID \
  -H 'Content-Type: application/json' \
  -d '{"done": true}'
```

### 删除任务

```bash
curl -s -X DELETE http://localhost:8000/api/tasks/TASK_ID
```

### 添加子任务

```bash
curl -s -X POST http://localhost:8000/api/tasks/TASK_ID/subtasks \
  -H 'Content-Type: application/json' \
  -d '{"title": "Step one"}'
```

### 记录项目进度

```bash
curl -s -X POST http://localhost:8000/api/projects/PROJECT_ID/entries \
  -H 'Content-Type: application/json' \
  -d '{"summary": "Shipped v1.3 with MCP server and OpenClaw skill"}'
```

## 自动化操作模式

- **每日晨会**：获取今日及逾期的任务列表，并按优先级排序。
- **每日结束时**：将已完成的任务标记为已完成，并为活跃项目添加新的日志记录。
- **每周回顾**：列出所有任务，突出显示逾期未完成或优先级为 P0/P1 的任务。
- **付款预测**：列出所有类型为 “payment”的任务，按月份分组并计算总金额。

## 使用注意事项：
- 在发送任何 API 请求之前，请务必确认服务器正在运行。
- 绝不要猜测任务 ID，应先通过标题查询任务，再使用 UUID。
- 日期必须使用 `YYYY-MM-DD` 格式。在发送请求前，请将 “明天”、“下周一” 等相对日期转换为具体的日期。
- 在使用 PUT 请求时，仅发送需要修改的字段。
- API 会在操作成功后返回创建或更新后的任务信息。
- 调用 `GET /api/tasks` 时，系统会自动将逾期未支付的任务更新为今天的状态。