---
slug: "n8n-project-management"
display_name: "N8N Project Management"
description: "使用 n8n 构建一个完整的项目管理系统，该系统包括 Telegram 聊天机器人、任务分配以及基于照片的报告功能。该系统基于 DDC 项目管理仓库进行开发。"
---

# n8n 建筑项目管理系统

使用 n8n 自动化工具、Telegram 机器人和 Google Sheets 构建一个通用的建筑项目任务管理和报告系统。

## 商业案例

**问题**：建筑经理每天需要花费 2-3 小时的时间来：
- 向工头和工人分配任务
- 通过电话/消息收集进度更新
- 编辑照片文档
- 跟踪任务完成状态

**解决方案**：自动化系统能够：
- 在预定时间通过 Telegram 发送任务提醒
- 收集状态报告（文本 + 照片 + GPS 数据）
- 自动将所有数据保存到 Google Sheets
- 为经理提供实时信息

**投资回报率 (ROI)**：任务管理方面的行政时间减少了 70%

## 源代码仓库

```
https://github.com/datadrivenconstruction/Project-management-n8n-with-task-management-and-photo-reports
```

## 系统架构

```
┌──────────────────────────────────────────────────────────────────────┐
│                    PROJECT MANAGEMENT SYSTEM                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   MANAGER                          WORKER                            │
│   ┌─────────────┐                  ┌─────────────┐                   │
│   │ Google      │                  │ Telegram    │                   │
│   │ Sheets      │                  │ Bot         │                   │
│   │             │                  │             │                   │
│   │ • Tasks     │    n8n           │ • /start    │                   │
│   │ • Schedule  │◄──Workflow──────►│ • Tasks     │                   │
│   │ • Reports   │                  │ • Photos    │                   │
│   │ • Photos    │                  │ • GPS       │                   │
│   └─────────────┘                  └─────────────┘                   │
│         │                                │                           │
│         ▼                                ▼                           │
│   ┌─────────────┐                  ┌─────────────┐                   │
│   │ Dashboard   │                  │ Google      │                   │
│   │ View        │                  │ Drive       │                   │
│   │             │                  │ (Photos)    │                   │
│   └─────────────┘                  └─────────────┘                   │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## 实施指南

### 第一步：创建 Telegram 机器人

```python
# 1. Open @BotFather in Telegram
# 2. Send /newbot
# 3. Name: "YourProject Tasks Bot"
# 4. Username: "YourProjectTasks_bot"
# 5. Save the token: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Test bot connection
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"
response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe")
print(response.json())
# Expected: {"ok": true, "result": {"id": ..., "first_name": "YourProject Tasks Bot"}}
```

### 第二步：设置 Google Sheets

创建以下表格：

**表格 1：任务**
| 列       | 类型    | 描述                |
|---------|-------|-------------------|
| Task_ID   | 文本    | 唯一标识符（例如：TASK-001）     |
| Project   | 文本    | 项目名称             |
| Object    | 文本    | 建筑物/区域            |
| Section   | 文本    | 楼层/区域             |
| Task     | 文本    | 任务描述             |
| Executor  | 文本    | 被分配的工人名称         |
| Executor_ID | 数字    | Telegram 用户 ID         |
| Date     | 文本    | 截止日期（格式：DD.MM.YYYY）     |
| Send_Time | 文本    | 提醒时间             |
| Priority  | 文本    | 🔴高 / 🟡中 / 🟢低          |
| Status    | 文本    | 待处理/已发送/已完成/部分完成   |
| Response  | 文本    | 工人的回复           |
| Response_Time | 时间    | 回复时间             |
| Photo_Link | URL     | Google Drive 文件链接       |
| GPS_Lat   | 数字    | 纬度               |
| GPS_Lon    | 数字    | 经度               |

**表格 2：工人**
| 列       | 类型    | 描述                |
|---------|-------|-------------------|
| Name     | 文本    | 工人全名             |
| Role     | 文本    | 工头/工人/承包商           |
| Telegram_ID | 数字    | 用户 ID             |
| Phone     | 文本    | 电话号码             |
| Registered | 时间    | 注册日期             |

**表格 3：照片报告**
| 列       | 类型    | 描述                |
|---------|-------|-------------------|
| Report_ID | 文本    | 唯一 ID             |
| Report_Type | 文本    | 日报/安全/质量报告        |
| Executor  | 文本    | 应由谁提交           |
| Date     | 文本    | 报告日期             |
| Time     | 文本    | 截止时间             |
| Status    | 文本    | 待处理/已提交           |
| Photo_Link | URL     | Google Drive 文件链接       |
| Comment  | 文本    | 工人备注             |

### 第三步：导入 n8n 工作流

```json
// Core workflow structure (simplified)
{
  "nodes": [
    {
      "name": "Telegram Trigger",
      "type": "n8n-nodes-base.telegramTrigger",
      "parameters": {
        "updates": ["message", "callback_query"]
      }
    },
    {
      "name": "Route Messages",
      "type": "n8n-nodes-base.switch",
      "parameters": {
        "rules": [
          {"value": "/start"},
          {"value": "/status"},
          {"value": "/help"},
          {"value": "text_reply"},
          {"value": "photo"},
          {"value": "location"}
        ]
      }
    },
    {
      "name": "Check Tasks Schedule",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "cronExpression": "* * * * *"
      }
    },
    {
      "name": "Get Pending Tasks",
      "type": "n8n-nodes-base.googleSheets",
      "parameters": {
        "operation": "readRows",
        "sheetName": "Tasks",
        "filters": {
          "Status": "Pending",
          "Send_Time": "now"
        }
      }
    },
    {
      "name": "Send Task Reminder",
      "type": "n8n-nodes-base.telegram",
      "parameters": {
        "operation": "sendMessage",
        "chatId": "={{$json.Executor_ID}}",
        "text": "📋 *Задача: {{$json.Task}}*\n📍 Объект: {{$json.Object}}\n⏰ Срок: {{$json.Date}}\n{{$json.Priority}}"
      }
    }
  ]
}
```

### 第四步：配置 Webhook

```bash
# Set Telegram webhook to n8n
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
  -d "url=https://your-n8n-instance.com/webhook/telegram-project-manager"

# Verify webhook is set
curl "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo"
```

## 工人命令

### 注册：/start

```
User: /start

Bot: 👋 Добро пожаловать в систему управления задачами!

Пожалуйста, укажите ваше имя:

User: Иван Петров

Bot: Выберите вашу роль:
[Прораб] [Рабочий] [Субподрядчик]

User: [Прораб]

Bot: ✅ Регистрация завершена!
Имя: Иван Петров
Роль: Прораб
ID: 123456789

Вы будете получать задачи автоматически.
Используйте /help для справки.
```

### 接收任务

```
Bot: 📋 *ЗАДАЧА #TASK-047*
━━━━━━━━━━━━━━━━━━━━━
📍 Объект: ЖК Солнечный, Корпус 2
🏗 Секция: 5 этаж, кв. 51-55
📝 Задача: Монтаж электропроводки
⏰ Срок: 24.01.2026
🔴 Приоритет: Высокий
━━━━━━━━━━━━━━━━━━━━━

Ответьте на это сообщение для отчета:
• Текст: статус + комментарий
• Фото: прикрепите фото работ
• GPS: отправьте геолокацию
```

### 回复任务

```
User: (reply to task message)
выполнено
Проводка смонтирована по всем квартирам, ждем приемку

Bot: ✅ Отчет принят!
━━━━━━━━━━━━━━━━━━━━━
📋 Задача: #TASK-047
📊 Статус: Выполнено
💬 Комментарий: Проводка смонтирована...
⏰ Время: 24.01.2026 14:35
━━━━━━━━━━━━━━━━━━━━━
```

### 提交照片报告

```
User: (sends photo as reply to task)
[Photo of completed electrical work]
Caption: Монтаж завершен, готово к проверке

Bot: 📷 Фото получено и сохранено!
━━━━━━━━━━━━━━━━━━━━━
📋 Задача: #TASK-047
🔗 Фото: [Ссылка на Google Drive]
💬 Комментарий: Монтаж завершен...
⏰ Время: 24.01.2026 14:38
━━━━━━━━━━━━━━━━━━━━━
```

### 提供 GPS 位置信息

```
User: (sends location)
📍 [Location: 55.7558, 37.6173]

Bot: 📍 Геолокация получена!
━━━━━━━━━━━━━━━━━━━━━
📋 Задача: #TASK-047
🗺 Координаты: 55.7558, 37.6173
🔗 Карта: [Google Maps Link]
⏰ Время: 24.01.2026 14:40
━━━━━━━━━━━━━━━━━━━━━
```

## 经理仪表盘

### 查看 Google Sheets 数据

```
┌────────────────────────────────────────────────────────────────────────┐
│ TASK DASHBOARD                                          🔄 Auto-refresh │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TODAY'S SUMMARY                                                       │
│  ┌───────────┬───────────┬───────────┬───────────┐                    │
│  │ Total: 24 │ ✅ Done:15│ ⏳ Pending:7│ ⚠️ Late:2│                    │
│  └───────────┴───────────┴───────────┴───────────┘                    │
│                                                                         │
│  TASK LIST                                             Filter: [Today ▼]│
│  ┌──────────┬────────────┬──────────┬────────┬────────┬──────────────┐│
│  │ Task ID  │ Task       │ Worker   │ Status │ Photo  │ Response     ││
│  ├──────────┼────────────┼──────────┼────────┼────────┼──────────────┤│
│  │ TASK-047 │ Электрика  │ Петров   │ ✅     │ 📷 3   │ Выполнено    ││
│  │ TASK-048 │ Сантехника │ Иванов   │ ⏳     │ -      │ -            ││
│  │ TASK-049 │ Штукатурка │ Сидоров  │ ⚠️     │ 📷 1   │ Частично     ││
│  └──────────┴────────────┴──────────┴────────┴────────┴──────────────┘│
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

## Python 集成

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime, timedelta

class ProjectTaskManager:
    """Integration with n8n Project Management System"""

    def __init__(self, credentials_path: str, spreadsheet_id: str):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_path, scope
        )
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open_by_key(spreadsheet_id)

    def create_task(self, task: dict) -> str:
        """Create new task in system"""
        tasks_sheet = self.spreadsheet.worksheet('Tasks')

        # Generate task ID
        all_tasks = tasks_sheet.get_all_records()
        task_num = len(all_tasks) + 1
        task_id = f"TASK-{task_num:04d}"

        # Prepare row
        row = [
            task_id,
            task.get('project', ''),
            task.get('object', ''),
            task.get('section', ''),
            task.get('description', ''),
            task.get('executor_name', ''),
            task.get('executor_id', ''),
            task.get('date', datetime.now().strftime('%d.%m.%Y')),
            task.get('send_time', '09:00'),
            task.get('priority', '🟡Medium'),
            'Pending',  # Status
            '',  # Response
            '',  # Response_Time
            '',  # Photo_Link
            '',  # GPS_Lat
            ''   # GPS_Lon
        ]

        tasks_sheet.append_row(row)
        return task_id

    def create_bulk_tasks(self, tasks: list) -> list:
        """Create multiple tasks at once"""
        task_ids = []
        for task in tasks:
            task_id = self.create_task(task)
            task_ids.append(task_id)
        return task_ids

    def get_today_summary(self) -> dict:
        """Get summary of today's tasks"""
        tasks_sheet = self.spreadsheet.worksheet('Tasks')
        all_tasks = tasks_sheet.get_all_records()

        today = datetime.now().strftime('%d.%m.%Y')
        today_tasks = [t for t in all_tasks if t['Date'] == today]

        return {
            'total': len(today_tasks),
            'completed': len([t for t in today_tasks if t['Status'] == 'Completed']),
            'pending': len([t for t in today_tasks if t['Status'] == 'Pending']),
            'partial': len([t for t in today_tasks if t['Status'] == 'Partial']),
            'with_photos': len([t for t in today_tasks if t['Photo_Link']])
        }

    def get_worker_performance(self, worker_name: str, days: int = 30) -> dict:
        """Analyze worker performance over period"""
        tasks_sheet = self.spreadsheet.worksheet('Tasks')
        all_tasks = tasks_sheet.get_all_records()

        cutoff_date = datetime.now() - timedelta(days=days)

        worker_tasks = [
            t for t in all_tasks
            if t['Executor'] == worker_name
            and datetime.strptime(t['Date'], '%d.%m.%Y') >= cutoff_date
        ]

        if not worker_tasks:
            return {'error': 'No tasks found'}

        completed = len([t for t in worker_tasks if t['Status'] == 'Completed'])
        total = len(worker_tasks)

        return {
            'worker': worker_name,
            'period_days': days,
            'total_tasks': total,
            'completed': completed,
            'completion_rate': round(completed / total * 100, 1),
            'with_photos': len([t for t in worker_tasks if t['Photo_Link']]),
            'with_gps': len([t for t in worker_tasks if t['GPS_Lat']])
        }


# Usage Example
if __name__ == "__main__":
    manager = ProjectTaskManager(
        'credentials.json',
        'your-spreadsheet-id'
    )

    # Create tasks for the week
    weekly_tasks = [
        {
            'project': 'ЖК Солнечный',
            'object': 'Корпус 2',
            'section': '5 этаж',
            'description': 'Монтаж электропроводки кв. 51-55',
            'executor_name': 'Петров И.И.',
            'executor_id': '123456789',
            'date': '24.01.2026',
            'send_time': '08:00',
            'priority': '🔴High'
        },
        {
            'project': 'ЖК Солнечный',
            'object': 'Корпус 2',
            'section': '5 этаж',
            'description': 'Монтаж сантехники кв. 51-55',
            'executor_name': 'Иванов А.П.',
            'executor_id': '987654321',
            'date': '25.01.2026',
            'send_time': '08:00',
            'priority': '🟡Medium'
        }
    ]

    task_ids = manager.create_bulk_tasks(weekly_tasks)
    print(f"Created tasks: {task_ids}")

    # Get summary
    summary = manager.get_today_summary()
    print(f"Today's summary: {summary}")
```

## n8n 工作流模板

### 模板 1：早晨任务分配

```yaml
name: Morning Task Distribution
trigger:
  type: cron
  expression: "0 8 * * 1-6"  # 8:00 AM, Mon-Sat

steps:
  - get_today_tasks:
      node: Google Sheets
      operation: readRows
      sheet: Tasks
      filter: Date = TODAY(), Status = Pending

  - group_by_worker:
      node: Code
      code: |
        const grouped = {};
        items.forEach(item => {
          const worker = item.json.Executor_ID;
          if (!grouped[worker]) grouped[worker] = [];
          grouped[worker].push(item.json);
        });
        return Object.entries(grouped).map(([id, tasks]) => ({
          worker_id: id,
          tasks: tasks
        }));

  - send_task_list:
      node: Telegram
      operation: sendMessage
      chatId: "={{$json.worker_id}}"
      text: |
        🌅 *Доброе утро! Ваши задачи на сегодня:*

        {{#each tasks}}
        ━━━━━━━━━━━━━━━━━━━━━
        {{priority}} *{{Task}}*
        📍 {{Object}} / {{Section}}
        ⏰ Срок: {{Date}}
        {{/each}}

        Ответьте на каждую задачу по мере выполнения.
```

### 模板 2：收集照片报告

```yaml
name: Scheduled Photo Reports
trigger:
  type: cron
  expression: "0 12,17 * * 1-6"  # 12:00 and 17:00

steps:
  - get_photo_reports:
      node: Google Sheets
      operation: readRows
      sheet: Photo Reports
      filter: Date = TODAY(), Status = Pending

  - send_photo_request:
      node: Telegram
      operation: sendMessage
      chatId: "={{$json.Executor_ID}}"
      text: |
        📷 *Требуется фото-отчет*
        ━━━━━━━━━━━━━━━━━━━━━
        📋 Тип: {{$json.Report_Type}}
        📍 Объект: {{$json.Object}}
        ⏰ Срок: {{$json.Time}}

        Пожалуйста, отправьте фото с комментарием.
      replyMarkup:
        inline_keyboard:
          - [{text: "📷 Отправить фото", callback_data: "photo_{{$json.Report_ID}}"}]
```

### 模板 3：每日总结

```yaml
name: End of Day Report
trigger:
  type: cron
  expression: "0 18 * * 1-6"  # 18:00

steps:
  - get_day_stats:
      node: Google Sheets
      operation: readRows
      sheet: Tasks
      filter: Date = TODAY()

  - calculate_stats:
      node: Code
      code: |
        const stats = {
          total: items.length,
          completed: items.filter(i => i.json.Status === 'Completed').length,
          partial: items.filter(i => i.json.Status === 'Partial').length,
          pending: items.filter(i => i.json.Status === 'Pending').length,
          photos: items.filter(i => i.json.Photo_Link).length
        };
        stats.completion_rate = Math.round(stats.completed / stats.total * 100);
        return [{ json: stats }];

  - send_to_manager:
      node: Telegram
      operation: sendMessage
      chatId: "MANAGER_CHAT_ID"
      text: |
        📊 *Итоги дня: {{$now.format('DD.MM.YYYY')}}*
        ━━━━━━━━━━━━━━━━━━━━━

        📋 Всего задач: {{$json.total}}
        ✅ Выполнено: {{$json.completed}}
        ⏳ Частично: {{$json.partial}}
        ❌ Не выполнено: {{$json.pending}}

        📷 Фото-отчетов: {{$json.photos}}
        📈 Выполнение: {{$json.completion_rate}}%

        [Открыть таблицу]({{SPREADSHEET_URL}})
```

## 最佳实践

### 任务设计
1. 保持任务的原子性（每个任务对应一个具体的行动）
2. 明确指定任务地点（建筑物/区域）
3. 设定合理的截止日期
4. 合理设置任务优先级（并非所有任务都需立即处理）

### 照片报告
1. 在关键节点要求提交照片
2. 按项目和日期创建不同的 Google Drive 文件夹
3. 确保照片中包含位置信息（GPS 数据）
4. 明确提交照片的要求

### 工人参与
1. 及时回复所有消息
2. 提供每日反馈
3. 表扬表现优秀的工人
4. 保持机器人消息的简洁性

## 资源

- **代码仓库**：https://github.com/datadrivenconstruction/Project-management-n8n-with-task-management-and-photo-reports
- **演示机器人**：@ProjectManagementTasks_Bot
- **演示表格**：[Google Sheets 演示](https://docs.google.com/spreadsheets/d/1fWi_0W_jqKa61h2oB3zZLdTDBK8_cQ123RtF70X1rwc)
- **n8n 文档**：https://docs.n8n.io

---

*“自动化并非是为了取代人类，而是为了让他们能够去做那些只有人类才能做的事情。”*