---
name: mac-reminder-bridge
description: "通过 HTTP 桥接在 Docker 中管理 macOS 的 Reminders.app 应用程序。适用于以下操作：设置/添加/创建提醒、设置提醒在特定时间执行、取消/删除提醒、标记提醒为已完成、更新/编辑提醒以及查看/列出所有提醒。需要确保在 Mac 上的 `listener.py` 脚本运行在 5000 端口上。"
metadata:
  {
    "openclaw": {
      "emoji": "🔔",
      "requires": { "bins": ["curl"] }
    }
  }
---
# 技能：Mac 提醒事项管理工具（Mac Reminder Bridge）

通过 HTTP 在 Docker 内部控制 macOS 的 Reminders.app 应用程序。
基础 URL：`http://host.docker.internal:5000`

---

## 使用场景

| 用户操作 | 对应的 API 端点 |
|-------------|----------|
| “设置提醒” | POST `/add_reminder` |
| “取消/删除某个提醒” | POST `/delete_reminder` |
| “标记某项任务为已完成” | POST `/complete_reminder` |
| “取消标记/重新打开提醒” | 使用 `completed=false` 发送 POST 请求到 `/complete_reminder` |
| “更新/修改某个提醒” | POST `/update/reminder` |
| “查看所有提醒” | GET `/list_reminders` |
| “查看我拥有的所有提醒列表” | GET `/list_lists` |

---

## POST /add_reminder

```json
{
  "task":      "Buy groceries",
  "list":      "Shopping",
  "due":       "2025-12-31 09:00",
  "remind_at": "2025-12-31 08:50",
  "notes":     "Get milk and eggs",
  "priority":  "high"
}
```

- 必需字段：`task`；其他字段为可选
- `due` / `remind_at` 格式：`YYYY-MM-DD HH:MM`
- `priority`：`none` | `low` | `medium` | `high`
- `list`：留空则使用默认列表

---

## POST /update_reminder

```json
{
  "task":         "Buy groceries",
  "fuzzy":        false,
  "new_task":     "Buy organic groceries",
  "new_due":      "2025-12-31 10:00",
  "new_notes":    "Also get juice",
  "new_priority": "medium"
}
```

- `task`：用于指定要更新的提醒
- 将 `new_due` 设置为 `""` 以清除到期日期
- 仅提交需要修改的字段

---

## POST /delete/reminder

```json
{ "task": "Buy groceries", "fuzzy": false, "list": "" }
```

- `fuzzy`: 如果不确定确切的提醒内容，可设置为 `true`（通过包含关系进行匹配）
- `list`：留空则搜索所有列表

---

## POST /complete/reminder

```json
{ "task": "Buy groceries", "completed": true, "fuzzy": false }
```

- `completed`: 如果设置为 `false`，则表示取消标记或重新打开提醒

---

## GET /list_reminders

```
GET /list_reminders
GET /list_reminders?list=Shopping
GET /list_reminders?completed=true
GET /list_reminders?completed=all
```

返回包含任务内容、到期时间、备注、优先级、完成状态以及所属列表的结构化 JSON 数据

---

## GET /list_lists

返回所有提醒列表，包括每个列表中的未完成提醒数量及列表名称

---

## GET /health

检查监听器是否正在运行，并确认是否具有管理提醒事项的权限

---

## 代理操作步骤

### 添加提醒
1. 提取所需信息：`task`（必填）、`due`、`remind_at`、`notes`、`priority`、`list`
2. 发送 POST 请求到 `/add_reminder`
3. 确认操作结果：显示 “✅ 提醒已设置：<task>” 以及到期时间（如适用）

### 删除提醒
1. 提取提醒的名称；如果不确定确切内容，可使用 `fuzzy: true`
2. 发送 POST 请求到 `/delete/reminder`
3. 检查返回的计数：如果计数为 0，则显示 “⚠️ 未找到与 '<task>' 匹配的提醒”

### 更新提醒
1. 提取当前提醒的名称及需要修改的内容
2. 仅提交需要修改的字段，发送 POST 请求到 `/update/reminder`
3. 确认修改的内容

### 查看提醒列表
1. 发送 GET 请求到 `/list_reminders`（如果用户指定了特定列表，可添加 `?list=X` 参数）
2. 如果存在多个列表，结果应按列表进行分组显示

### 重要操作前的健康检查
```bash
curl http://host.docker.internal:5000/health
```

### 认证请求头（如果设置了 BRIDGE_SECRET）
```
X-Bridge-Secret: <secret>
```