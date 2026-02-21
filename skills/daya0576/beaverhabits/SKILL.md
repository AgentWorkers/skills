---
name: beaverhabits
description: 使用 Beaver Habit Tracker API 来跟踪和管理您的习惯。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - BEAVERHABITS_API_KEY
        - SERVER_URL (optional, defaults to https://beaverhabits.com)
      bins:
        - curl
    primaryEnv: BEAVERHABITS_API_KEY
    emoji: "\U0001F9AB"
    homepage: https://github.com/daya0576/beaverhabits
---
# Beaver 习惯追踪器

使用 [Beaver 习惯追踪器](https://beaverhabits.com) 的 API 来跟踪和管理您的日常习惯。

API 文档：[https://beaverhabits.com/docs](https://beaverhabits.com/docs)

## 设置

### 环境变量

| 变量 | 是否必需 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `BEAVERHABITS_API_KEY` | 是 | — | 从 Beaver Habits 设置页面获取的永久 API 令牌 |
| `SERVER_URL` | 否 | `https://beaverhabits.com` | 您的 Beaver Habits 服务器地址（用于自托管实例） |

### 获取 API 令牌

1. 登录到您的 Beaver Habits 实例
2. 打开菜单 → 工具 → API 令牌
3. 点击“生成 API 令牌”
4. 复制令牌，并将其设置为 `BEAVERHABITS_API_KEY`

## 工具

### `list_habits`（概览）

列出所有习惯，并显示每周的 ASCII 概览。这是任何与习惯相关的查询的 **默认响应**。

**步骤 1** — 获取所有习惯：

```bash
curl -s -H "Authorization: Bearer $BEAVERHABITS_API_KEY" \
  "${SERVER_URL:-https://beaverhabits.com}/api/v1/habits"
```

**步骤 2** — 对于每个习惯，获取过去 5 天内的完成情况：

```bash
curl -s -H "Authorization: Bearer $BEAVERHABITS_API_KEY" \
  "${SERVER_URL:-https://beaverhabits.com}/api/v1/habits/{habit_id}/completions?date_fmt=%25d-%25m-%25Y&date_start={start}&date_end={end}&limit=100&sort=asc"
```

响应格式：`["16-02-2026", "18-02-2026"]`（完成的日期字符串数组）

**步骤 3** — 以 ASCII 表格的形式显示结果：

示例输出：
```
              Mon   Tue   Wed   Thu   Fri   
Exercise       ✗     ✗     ✗     ✗     ✗     
English        ✓     ✗     ✗     ✗     ✗     
paipai         ✗     ✗     ✗     ✗     ✓     
Reading        ✗     ✗     ✗     ✗     ✗     
Table Tennis   ✗     ✗     ✗     ✗     ✗     
```

使用 `✓` 表示已完成，`✗` 表示未完成。默认时间范围为截至今天的 5 天。为了对齐，习惯名称中的表情符号会被删除。

### `complete_habit`

将某个习惯标记为在特定日期已完成（或未完成）。

参数：
- `habit_id`（必填）：通过调用 `list_habits` 并匹配用户的习惯名称来自动获取。切勿向用户询问此值。
- `date`（必填）：日期格式为 DD-MM-YYYY
- `done`（可选）：`true` 表示已完成，`false` 表示未完成（默认值：`true`）

```bash
curl -s -X POST \
  -H "Authorization: Bearer $BEAVERHABITS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"date": "20-02-2026", "done": true, "date_fmt": "%d-%m-%Y"}' \
  "${SERVER_URL:-https://beaverhabits.com}/api/v1/habits/{habit_id}/completions"
```

响应：`{"day": "20-02-2026", "done": true}`

## 使用说明

- 当用户请求列出、查看或检查习惯时，始终以 ASCII 表格的形式返回结果（而不是简单的列表）。
- 完成或未完成一个习惯后，务必重新生成概览表格以显示更新后的状态。
- 通过 `list_habits` 功能获取习惯名称对应的 ID。切勿向用户询问习惯 ID。
- 除非另有指定，否则默认使用今天的日期。可以使用 `date_fmt=%d-%m-%Y` 格式。