---
name: intent-guardian
version: 1.0.0
description: 它监视您的桌面活动，维护一个实时的任务栈，能够检测到您在被打断后忘记了正在做什么，并会温和地提醒您。它是您随时相伴的专注助手。
author: huiling-one2x
tags: [productivity, focus, memory, awareness, context-switch]
tools: [shell, filesystem, memory, chat]
trigger: "intent guardian|task stack|what was I doing|focus guard|track my tasks"
config:
  poll_interval_seconds: 5
  interruption_threshold_minutes: 5
  reminder_cooldown_minutes: 3
  max_stack_depth: 20
  screen_capture_enabled: false
  screen_capture_interval_seconds: 30
  vision_model: ""
  activitywatch_enabled: true
  activitywatch_url: "http://localhost:5600"
  notification_channel: "system"
  working_hours_start: "09:00"
  working_hours_end: "18:00"
  excluded_apps: ["Finder", "SystemPreferences", "loginwindow"]
---
# Intent Guardian

**再也不用丢失思路了。**

Intent Guardian 会持续监控您的桌面活动，实时了解您正在处理的任务，并在您因干扰而分心、忘记最初任务时及时提醒您。

## 问题所在

知识工作者平均每 3 分钟就会受到一次干扰。受到干扰后，他们需要大约 23 分钟才能重新回到原来的任务上——而很多时候，他们根本无法回到原来的任务。这并非因为任务不重要，而是因为他们只是**忘记了**。

Intent Guardian 通过维护一个**任务栈**来解决这个问题——这个任务栈记录了您正在做什么、之前在做什么以及被什么打断了，这样您就无需再费心去回忆了。

## 适用场景

- 您是一个经常在多个应用程序和任务之间切换的多任务处理者
- 您经常在回复消息后突然想：“等等，我刚才在做什么来着？”
- 您希望有一个能够理解您工作节奏的 AI 助手，而不仅仅是执行您的命令
- 您希望长期了解自己的注意力集中模式

## 核心功能

### 1. 实时活动检测

通过查询活动窗口的标题和应用程序名称来构建连续的活动流。

**macOS:**
```bash
bash command:"scripts/sense_activity.sh"
```

**使用 ActivityWatch（提供更详细的数据）:**
```bash
bash command:"scripts/sense_activitywatch.sh"
```

**使用屏幕截图（可选，需要视觉模型）:**
```bash
bash command:"scripts/sense_screen.sh"
```

### 2. 任务栈维护

该插件在 `memory/skills/intent-guardian/task_stack.json` 文件中维护一个任务栈：

```json
{
  "stack": [
    {
      "id": "task_001",
      "intent": "Writing product requirements doc, section 3",
      "app": "Google Docs",
      "window_title": "Product Requirements v2 - Google Docs",
      "started_at": "2026-02-26T14:28:00",
      "status": "suspended",
      "suspended_at": "2026-02-26T14:31:00",
      "suspended_by": "Slack notification from Li Si",
      "completion_estimate": 0.6
    },
    {
      "id": "task_002",
      "intent": "Replying to Li Si about the API bug",
      "app": "Slack",
      "window_title": "Slack - #engineering",
      "started_at": "2026-02-26T14:31:00",
      "status": "completed",
      "completed_at": "2026-02-26T14:35:00"
    },
    {
      "id": "task_003",
      "intent": "Looking up React useEffect cleanup pattern",
      "app": "Chrome",
      "window_title": "Stack Overflow - React useEffect cleanup",
      "started_at": "2026-02-26T14:35:00",
      "status": "active"
    }
  ],
  "current_focus": "task_003",
  "forgotten_candidates": ["task_001"]
}
```

### 3. 干扰与遗忘检测

该插件会分析任务栈以检测可能的遗忘情况：

**表明遗忘的信号：**
- 被暂停的任务已经暂停超过 `interruption_threshold_minutes` 分钟
- 用户在暂停后切换了 2 个以上不相关的任务或上下文
- 用户表现出“注意力分散”的行为：快速切换应用程序且无法持续集中注意力
- 被暂停的任务完成度较低（例如，还在处理某个任务的过程中）

**表明用户故意放弃任务的信号（此时不会提醒）:**
- 用户明确关闭了与该任务相关的应用程序
- 任务已经到达自然完成点（例如，发送完邮件）
- 用户开始了一个新的、有目的的深度工作会话

### 4. 温和的提醒

当检测到遗忘时，该插件会发送一个不打扰用户的提醒：

**简单提醒：**
> “25 分钟前，您正在 Google Docs 中编写产品需求文档的第 3 节内容，然后被 Slack 干扰了。想要继续吗？”

**智能提醒（包含上下文信息）:**
> “您暂停编写产品需求文档去查找 Li Si 的 bug 相关的 useEffect 清理代码。答案是：在 useEffect 中返回一个清理函数。准备好继续处理这个任务了吗？”

第二种提醒方式更为高效——它不仅会提醒您忘记了什么，还会**补充您暂停的原因**，让您能够带着答案回到原来的任务上。

### 5. 长期模式学习

随着时间的推移，该插件会在 `memory/skills/intent-guardian/focus_profile.json` 文件中构建一个注意力集中模式：

```json
{
  "user_id": "default",
  "updated_at": "2026-02-26",
  "patterns": {
    "avg_focus_duration_minutes": 12,
    "interruption_sources": {
      "Slack": { "count": 45, "forget_rate": 0.78 },
      "Mail": { "count": 22, "forget_rate": 0.18 },
      "Chrome": { "count": 31, "forget_rate": 0.42 }
    },
    "peak_focus_hours": ["09:00-11:00", "14:00-16:00"],
    "high_risk_transitions": [
      { "from": "VSCode", "to": "Slack", "forget_rate": 0.82 },
      { "from": "Google Docs", "to": "Chrome", "forget_rate": 0.55 }
    ],
    "reminder_effectiveness": {
      "accepted": 34,
      "dismissed": 8,
      "ignored": 5
    }
  }
}
```

该模式用于个性化设置检测阈值和提醒时机。

## 架构

```
 Your Desktop
      |
      v
 [Sensing Layer]  ---- scripts/sense_activity.sh (window title, every N sec)
      |                 scripts/sense_activitywatch.sh (ActivityWatch API)
      |                 scripts/sense_screen.sh (optional screenshot + vision)
      v
 [Activity Log]   ---- memory/skills/intent-guardian/activity_log.jsonl
      |
      v
 [Understanding]  ---- LLM analyzes activity stream on each Heartbeat:
      |                 - Segments activities into logical tasks
      |                 - Infers intent for each task
      |                 - Detects interruptions and context switches
      v
 [Task Stack]     ---- memory/skills/intent-guardian/task_stack.json
      |
      v
 [Detection]      ---- Compares stack state against forgetting heuristics
      |                 Consults focus_profile.json for personalized thresholds
      v
 [Reminder]       ---- Sends reminder via configured notification channel
      |                 Logs user response for feedback loop
      v
 [Learning]       ---- Updates focus_profile.json with new patterns
```

## 与 Heartbeat 的集成

请将以下内容添加到您的 `HEARTBEAT.md` 文件中：

```markdown
## Intent Guardian Check
Every heartbeat, run the intent guardian cycle:
1. Read latest activity from memory/skills/intent-guardian/activity_log.jsonl
2. Update task_stack.json with new activities
3. Check for forgotten tasks (suspended > threshold, not resumed)
4. If forgotten task detected, send reminder
5. Log any reminder responses to focus_profile.json
```

## Cron 定时任务

添加每日注意力报告：

```bash
openclaw cron add --name "intent-guardian-daily" --schedule "0 18 * * *" \
  --prompt "Generate my daily focus report using intent-guardian data"
```

## 设置

### 最小化设置（macOS，无需额外依赖）

1. 安装该插件：
```bash
npx playbooks add skill openclaw/skills --skill intent-guardian
```

2. 该插件使用 macOS 的原生命令 (`osascript`) 来获取活动窗口。
无需安装其他软件。

3. 将上述 Heartbeat 集成内容添加到您的 `HEARTBEAT.md` 文件中。

### 扩展设置（使用 ActivityWatch）

1. 安装 [ActivityWatch](https://activitywatch.net/) 以获得更详细的窗口级跟踪信息。
2. 在插件配置中设置 `activitywatch_enabled: true`。
3. ActivityWatch 可提供包含 URL 和文档标题的详细窗口时间线。

### 完整设置（使用屏幕截图）

1. 设置 `screen_capture_enabled: true` 并配置 `vision_model`。
2. 需要一个具备视觉分析能力的模型（如 Claude、Gemini、Qwen3-VL）。
3. 屏幕截图会在本地捕获、分析，**不会永久保存**。

## 隐私与安全

- **所有数据都保存在本地**。活动日志、任务栈和注意力集中模式都作为本地文件存储在您的 OpenClaw 内存目录中。
- **不会保存原始截图**。如果启用了屏幕截图功能，只会分析截图内容并立即丢弃，仅保留语义摘要。
- **排除特定应用程序**。通过配置 `excluded_apps` 来阻止跟踪某些应用程序。
- **限制工作时间**。检测仅在配置的 `working_hours_start` 到 `working_hours_end` 期间进行。
- **数据归您所有**。所有文件均为人类可读的 JSON/JSONL 格式，您可以随时查看、编辑或删除。

## 配置参考

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|---------|-------------|
| `poll_interval_seconds` | int | 5 | 检查活动窗口的频率 |
| `interruption_threshold_minutes` | int | 被暂停的任务被标记为可能遗忘前的等待时间（分钟） |
| `reminder_cooldown_minutes` | int | 提醒之间的最小间隔时间（分钟），以避免频繁提醒 |
| `max_stack_depth` | int | 任务栈中允许的最大任务数量 |
| `screen_capture_enabled` | bool | 是否启用定期屏幕截图分析 |
| `screen_capture_interval_seconds` | int | 如果启用屏幕截图功能的间隔时间（秒） |
| `vision_model` | string | 用于屏幕截图分析的模型（例如 "gemini", "claude"） |
| `activitywatch_enabled` | bool | 是否使用 ActivityWatch 提供更详细的活动数据 |
| `activitywatch_url` | string | ActivityWatch 服务器的 URL |
| `notification_channel` | string | 提醒信息的发送方式（例如 "system", "telegram", "slack" 等） |
| `working_hours_start` | string | 活动跟踪的开始时间 |
| `working_hours_end` | string | 活动跟踪的结束时间 |
| `excluded_apps` | list | 需要排除的应用程序列表（例如 "Finder", "SystemPreferences", "loginwindow"） |

## 示例交互

**用户：**“我在分心之前在做什么？”
**插件读取任务栈并回答：**
> “在 14:31 被 Slack 干扰之前，您正在 Google Docs 中编写产品需求文档的第 3 节内容，已经完成了大约 60%。想要继续吗？”

**用户：**“显示我的任务栈”
**插件显示当前的任务栈：**
> ```
> Task Stack (3 items):
> [ACTIVE]     Looking up React useEffect cleanup (Chrome) - 17 min
> [COMPLETED]  Replying to Li Si about API bug (Slack) - 4 min
> [SUSPENDED]  Writing product requirements doc, section 3 (Google Docs) - 25 min ago  !!
> ```

**用户：**“我今天的注意力集中情况如何？”
**插件读取活动日志和注意力集中模式：**
> “今天您进行了 6 次深度工作会话，每次平均持续 18 分钟。您被干扰了 11 次，其中 7 次来自 Slack。您有 4 次忘记返回原来的任务——其中 3 次被我发现了。您的最佳注意力集中时间为 09:30-10:45。”

**主动提醒（通过 Heartbeat）:**
> “注意——自从那个电话会议后，您已经离开了季度报告（Excel）40 分钟了。报告明天就要提交了。想要完成当前任务并继续处理它吗？”

## 与其他插件的集成

Intent Guardian 可以与以下插件很好地配合使用：

| 插件 | 集成方式 |
|-------|-------------|
| `personal-analytics` | 将注意力集中模式数据提供给分析工具，生成更详细的每周报告 |
| `daily-review` | 在每日报告中包含任务完成情况和干扰次数 |
| `deepwork-tracker` | 在检测到持续专注时自动启动深度工作计时器 |
| `screen-monitor` | 如果配置了视觉模型，可以使用 `screen_analyze` 提供更详细的上下文信息 |
| `rememberall` | 将被暂停的任务转换为基于时间的提醒 |
| `get-focus-mode` | 当 macOS 的专注模式激活时，抑制提醒 |

## 发展计划

- [ ] 跨设备同步（在手机上提醒笔记本电脑上未完成的任务）
- [ ] 团队协作模式（经用户同意后显示提醒，例如：“Zhang San 等待您的审核，已经等了 2 天”）
- [ ] 主动任务分配（“您可以在您专注于文档时帮我起草邮件回复”）
- [ ] 日历提醒功能（“季度报告会议还有 2 小时，而您只完成了 60%”）
- [ ] 目标层次管理（跟踪 L1-L4 级别的任务，而不仅仅是即时任务）

## 许可证

MIT