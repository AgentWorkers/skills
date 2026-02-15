# exchange2010

Exchange 2010 提供了对电子邮件、日历、联系人和任务的集成支持。

## 设置

需要 `.env.credentials` 文件中的凭据：
```
EXCHANGE_SERVER=mail.company.com
EXCHANGE_DOMAIN=company
EXCHANGE_EMAIL=user@company.com
EXCHANGE_PASSWORD=your_password
```

## 功能

- ✅ **电子邮件**：查看未读邮件、发送邮件、搜索邮件、将邮件标记为已读
- ✅ **电子邮件附件**：下载附件、提取附件文本（PDF、TXT格式）
- ✅ **电子邮件文件夹**：浏览已发送邮件、草稿邮件、垃圾邮件文件夹
- ✅ **日历**：查看、创建、更新、删除日历事件
- ✅ **重复事件**：检测和管理重复事件
- ✅ **共享日历**：访问其他 Exchange 邮箱的日历
- ✅ **联系人**：搜索联系人信息、解析联系人名称（GAL 数据库）
- ✅ **任务/待办事项**：管理、创建和完成任务
- ✅ **外出办公**：查看和设置外出办公状态
- ✅ **EWS 过滤器**：使用 `subject__contains`、`start__gte` 等条件进行快速搜索
- ✅ **日历文件夹列表**：显示所有日历文件夹

## 示例

### 查看电子邮件

```python
from skills.exchange2010 import get_account, get_unread_emails

account = get_account()
emails = get_unread_emails(account, limit=10)
for email in emails:
    print(f"{email['subject']} from {email['sender']}")
```

### 查看今日事件

```python
from skills.exchange2010 import get_today_events

# Your own events
today = get_today_events()

# Events from shared calendar
today = get_today_events('shared@company.com')
```

### 搜索日历事件

```python
from skills.exchange2010 import search_calendar_by_subject
from datetime import date

# Fast search for Ekadashi
ekadashi = search_calendar_by_subject(
    email_address='shared@company.com',
    search_term='Ekadashi',
    start_date=date(2025, 1, 1),
    end_date=date(2026, 12, 31)
)
print(f"Found: {len(ekadashi)} events")
```

### 创建日历事件

```python
from skills.exchange2010 import create_calendar_event
from datetime import datetime

create_calendar_event(
    subject="Team Meeting",
    start=datetime(2026, 2, 7, 14, 0),
    end=datetime(2026, 2, 7, 15, 0),
    body="Project discussion",
    location="Conference Room A"
)
```

### 更新日历事件

```python
from skills.exchange2010 import update_calendar_event
from datetime import datetime

# Reschedule
update_calendar_event(
    event_id='AAQkAG...',
    start=datetime(2026, 2, 10, 14, 0),
    end=datetime(2026, 2, 10, 15, 0),
    location="New Room B"
)
```

### 浏览电子邮件文件夹

```python
from skills.exchange2010 import get_folder_emails, list_email_folders

# List all folders
folders = list_email_folders(account)
for f in folders:
    print(f"{f['name']}: {f['unread_count']} unread")

# Sent Items
sent = get_folder_emails('sent', limit=10)

# Drafts
drafts = get_folder_emails('drafts')

# Trash
trash = get_folder_emails('trash')
```

### 搜索电子邮件

```python
from skills.exchange2010 import search_emails

# By sender
emails = search_emails(sender='boss@company.com', limit=10)

# By subject
emails = search_emails(subject='Invoice', folder='inbox')

# Unread only
emails = search_emails(is_unread=True, limit=20)
```

### 将电子邮件标记为已读

```python
from skills.exchange2010 import mark_email_as_read

mark_email_as_read(email_id='AAQkAG...')
```

### 下载附件

```python
from skills.exchange2010 import get_email_attachments

# Show info
attachments = get_email_attachments(email_id='AAQkAG...')
for att in attachments:
    print(f"{att['name']}: {att['size']} bytes")

# Download
attachments = get_email_attachments(
    email_id='AAQkAG...',
    download_path='/tmp/email_attachments'
)
```

### 从附件中提取文本

**前提条件**：需要安装 `pip install PyPDF2` 以支持 PDF 文本提取

```python
from skills.exchange2010 import process_attachment_content

results = process_attachment_content(email_id='AAQkAG...')
for result in results:
    print(f"File: {result['name']}")
    if 'extracted_text' in result:
        print(f"Content: {result['extracted_text'][:500]}...")
```

### 搜索联系人

```python
from skills.exchange2010 import search_contacts, resolve_name

# Search contacts
contacts = search_contacts('John Doe')
for c in contacts:
    print(f"{c['name']}: {c['email']}")

# Resolve name (GAL)
result = resolve_name('john.doe@company.com')
if result:
    print(f"Found: {result['name']} - {result['email']}")
```

### 管理任务

```python
from skills.exchange2010 import get_tasks, create_task, complete_task, delete_task
from datetime import datetime, timedelta

# Show open tasks
tasks = get_tasks()
for task in tasks:
    status = '✅' if task['is_complete'] else '⏳'
    print(f"{status} {task['subject']}")

# Create new task
task_id = create_task(
    subject="Finish report",
    body="Q1 report due Friday",
    due_date=datetime.now() + timedelta(days=3),
    importance="High"
)

# Mark as complete
complete_task(task_id)

# Delete
delete_task(task_id)
```

### 查找重复事件

```python
from skills.exchange2010 import get_recurring_events

recurring = get_recurring_events(
    email_address='shared@company.com',
    days=30
)
for r in recurring:
    print(f"{r['subject']}: {r['recurrence']}")
```

### 设置外出办公状态

```python
from skills.exchange2010 import get_out_of_office, set_out_of_office
from datetime import datetime, timedelta

# Check status
oof = get_out_of_office()
print(f"Out of office active: {oof['enabled']}")

# Enable
set_out_of_office(
    enabled=True,
    internal_reply="I am on vacation until Feb 15th.",
    external_reply="I am on vacation until Feb 15th.",
    start=datetime.now(),
    end=datetime.now() + timedelta(days=7),
    external_audience='All'  # 'All', 'Known', 'None'
)

# Disable
set_out_of_office(enabled=False, internal_reply="")
```

### 发送电子邮件

```python
from skills.exchange2010 import send_email

send_email(
    to=["recipient@example.com"],
    subject="Test",
    body="Hello!",
    cc=["cc@example.com"]
)
```

## API 参考

### 电子邮件

| 函数 | 描述 |
|----------|-------------|
| `get_account()` | 连接到 Exchange 服务器 |
| `get_unread_emails(account, limit=50)` | 获取未读邮件 |
| `search_emails(search_term, sender, subject, is_unread, folder, limit)` | 搜索电子邮件 |
| `send_email(to, subject, body, cc, bcc)` | 发送电子邮件 |
| `mark_email_as_read(email_id)` | 将邮件标记为已读 |
| `get_emailattachments(email_id, download_path)` | 下载附件 |
| `process_attachment_content(email_id, attachment_name)` | 提取附件内容 |

### 电子邮件文件夹

| 函数 | 描述 |
| ----------|-------------|
| `get_folder_emails(folder_name, limit, is_unread)` | 获取文件夹中的电子邮件 |
| `list_email_folders(account)` | 列出所有文件夹 |

### 日历

| 函数 | 描述 |
| ----------|-------------|
| `get_today_events(email_address)` | 获取今日事件 |
| `get_upcoming_events(email_address, days)` | 获取未来 N 天内的事件 |
| `get_calendar_events(account, start, end)` | 获取指定时间范围内的事件 |
| `get_shared_calendar_events(email, start, end)` | 获取共享日历的事件 |
| `search_calendar_by_subject(email, term, start, end)` | 快速搜索日历事件 |
| `create_calendar_event(subject, start, end, body, location)` | 创建日历事件 |
| `update_calendar_event(event_id, ...)` | 更新日历事件 |
| `get_event_details(event_id)` | 查看事件详情 |
| `delete_calendar_event(event_id)` | 删除日历事件 |
| `get_recurring_events(email, start, end)` | 获取重复事件 |
| `list_available_calendars(account)` | 列出可用的日历 |
| `count_ekadashi_events(email, start_year)` | 统计特定日期的 Ekadashi 事件数量 |

### 联系人

| 函数 | 描述 |
| ----------|-------------|
| `search_contacts(search_term, limit)` | 搜索联系人 |
| `resolve_name(name)` | 解析联系人名称（GAL 数据库） |

### 任务

| 函数 | 描述 |
| ----------|-------------|
| `get_tasks(status, folder)` | 获取任务列表 |
| `create_task(subject, body, due_date, importance, categories)` | 创建任务 |
| `complete_task(task_id)` | 完成任务 |
| `delete_task(task_id)` | 删除任务 |

### 外出办公状态

| 函数 | 描述 |
| ----------|-------------|
| `get_out_of_office(email_address)` | 查看外出办公状态 |
| `set_out_of_office.enabled, internal_reply, ...)` | 设置外出办公状态 |

## 注意事项

- 明确使用 Exchange 2010 SP2 版本
- 对于自己的邮箱和共享邮箱，使用 `DELEGATE` 访问权限类型
- **EWS 过滤器**（如 `subject__contains`、`start__gte`）比传统遍历方式更高效
- 时间区自动转换为 UTC 格式
- 共提供 27 个相关函数