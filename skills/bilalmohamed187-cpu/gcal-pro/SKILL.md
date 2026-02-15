---
name: gcal-pro
description: **Google Calendar集成**  
用于查看、创建和管理日历事件。当用户询问自己的日程安排、需要添加/编辑/删除事件、查看可用时间，或希望接收每日晨报时，可以使用该功能。支持自然语言指令，例如：“我明天有什么安排？”或“周五中午和Alex安排一次午餐会面”。免费版本仅提供读取日历事件的功能；专业版（12美元）则新增了创建/编辑/删除事件以及每日晨报的功能。
---

# gcal-pro

通过自然语言对话来管理 Google 日历。

## 快速参考

| 功能 | 命令 | 订阅等级 |
|--------|---------|------|
| 查看今日日程 | `python scripts/gcal_core.py today` | 免费 |
| 查看明日日程 | `python scripts/gcal_core.py tomorrow` | 免费 |
| 查看本周日程 | `python scripts/gcal_core.py week` | 免费 |
| 搜索事件 | `python scripts/gcal_core.py search -q "会议"` | 免费 |
| 列出日历 | `python scripts/gcal_core.py calendars` | 免费 |
| 查找空闲时间 | `python scripts/gcal_core.py free` | 免费 |
| 快速添加事件 | `python scripts/gcal_core.py quick -q "周五中午午餐"` | 专业级 |
| 删除事件 | `python scripts/gcal_core.py delete --id EVENT_ID -y` | 专业级 |
| 早晨简报 | `python scripts/gcal_core.py brief` | 专业级 |

## 设置

**首次使用需要完成以下步骤：**

1. 用户必须创建 Google Cloud 项目并获取 OAuth 凭据。
2. 将 `client_secret.json` 文件保存到 `~/.config/gcal-pro/` 目录下。
3. 运行身份验证：
   ```bash
   python scripts/gcal_auth.py auth
   ```
4. 浏览器打开 → 用户授权日历访问权限 → 设置完成。

**检查身份验证状态：**
```bash
python scripts/gcal_auth.py status
```

## 订阅等级

### 免费等级
- 查看事件（今日、明日、本周、本月）
- 搜索事件
- 列出日历
- 查找空闲时间

### 专业级（一次性费用 $12）

- 免费等级的所有功能外，还支持：
- 创建事件
- 通过自然语言快速添加事件
- 更新/重新安排事件
- 删除事件
- 通过 cron 服务发送早晨简报

## 使用示例

### 查看日程

当用户询问“我的日历上有什么安排？”或“我今天有什么事情？”时：

```bash
cd /path/to/gcal-pro
python scripts/gcal_core.py today
```

对于特定时间范围：
- “明天” → `python scripts/gcal_core.py tomorrow`
- “本周” → `python scripts/gcal_core.py week`
- “与 Alex 的会议” → `python scripts/gcal_core.py search -q "Alex"`

### 创建事件（专业级）

当用户说“在我的日历上添加某个事件”或“安排某个活动”时：

**选项 1：通过自然语言快速添加事件**
```bash
python scripts/gcal_core.py quick -q "Lunch with Alex Friday at noon"
```

**选项 2：通过 Python 结构化创建事件**
```python
from scripts.gcal_core import create_event, parse_datetime

create_event(
    summary="Lunch with Alex",
    start=parse_datetime("Friday noon"),
    location="Cafe Roma",
    confirmed=True  # Set False to show confirmation prompt
)
```

### 修改事件（专业级）

**⚠️ 执行删除或重大修改操作前必须确认！**

在删除或大幅修改事件之前，务必先与用户确认：
1. 显示事件详情
2. 询问“我是否要删除/重新安排这个事件？”
3. 仅在使用用户确认（`confirmed=True` 或 `-y` 参数）后才能继续操作

**删除事件：**
```bash
# First, find the event
python scripts/gcal_core.py search -q "dentist"
# Shows event ID

# Then delete (with user confirmation)
python scripts/gcal_core.py delete --id abc123xyz -y
```

### 查找空闲时间

当用户询问“我什么时候有空？”或“安排一个小时的会议”时：

```bash
python scripts/gcal_core.py free
```

### 早晨简报（专业级 + Cron）

通过 Clawdbot 的 cron 服务每天发送早晨简报：

```python
from scripts.gcal_core import generate_morning_brief
print(generate_morning_brief())
```

**Cron 设置示例：**
- 时间：每天上午 8:00
- 操作：运行 `python scripts/gcal_core.py brief`
- 通知方式：将结果发送到用户的消息频道

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| “client_secret.json 未找到” | 设置未完成 | 完成 Google Cloud 的设置 |
| “令牌更新失败” | 令牌过期/被撤销 | 运行 `python scripts/gcal_auth.py auth --force` |
| “需要专业级权限” | 免费用户尝试执行写入操作 | 提示用户升级或说明权限限制 |
| “事件未找到” | 事件 ID 无效 | 先搜索正确的事件 |

## 时区处理

- 所有时间均按照用户的本地时区显示（默认：America/New_York）
- 如果用户指定了时区（例如 “下午 2 点 EST”），则按该时区显示
- 时间以 ISO 8601 格式存储，并包含时区信息

## 响应格式

**事件列表的显示格式：**

```
📅 **Monday, January 27**
  • 9:00 AM — Team standup
  • 12:00 PM — Lunch with Alex 📍 Cafe Roma
  • 3:00 PM — Client call

📅 **Tuesday, January 28**
  • 10:00 AM — Dentist appointment 📍 123 Main St
```

**确认信息的格式：**

```
✓ Event created: "Lunch with Alex"
  📅 Friday, Jan 31 at 12:00 PM
  📍 Cafe Roma
```

**早晨简报的格式：**

```
☀️ Good morning! Here's your day:
📆 Monday, January 27, 2026

You have 3 events today:
  • 9:00 AM — Team standup
  • 12:00 PM — Lunch with Alex
  • 3:00 PM — Client call

👀 Tomorrow: 2 events
```

## 文件位置

```
~/.config/gcal-pro/
├── client_secret.json   # OAuth app credentials (user provides)
├── token.json           # User's access token (auto-generated)
└── license.json         # Pro license (if purchased)
```

## 与 Clawdbot 的集成

此功能支持与以下服务集成：
- **Cron**：用于安排早晨简报
- **Memory**：存储用户的日历偏好设置
- **Messaging**：通过 Telegram/WhatsApp 等工具发送简报

## 升级提示

当免费用户尝试执行专业级操作时，回复：

> ⚠️ 创建事件需要购买 **gcal-pro Pro**（一次性费用 $12）。
> 
> 专业级功能包括：创建、编辑、删除事件以及发送早晨简报。
> 
> 👉 升级链接：[gumroad-link]
> 
> 目前，我可以为您显示今天的日程（免费）——您想查看今天的事件吗？