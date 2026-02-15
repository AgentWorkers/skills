---
name: casual-cron
description: "**使用自然语言创建具有严格运行规则的Clawdbot定时任务**  
适用场景：当用户请求安排提醒或消息（无论是定期还是一次性）时，尤其是通过Telegram发送请求，或者当用户使用`/at`或`/every`等指令时。  
示例：  
- “创建一个每天早上8点的提醒”  
- “20分钟后提醒我”  
- “下午3点给我发送一条Telegram消息”  
- “每2小时发送一次消息”"
---

# Casual Cron

该功能可自动根据自然语言请求创建Clawdbot的Cron作业，并通过安全运行规则确保任务可靠执行。

## Cron作业运行规则（硬性规定）：

- 在Cron作业执行期间：严禁进行故障排查、重启网关或检查时间。
- 严禁发送确认信息或解释性内容。
- 作业执行完成后，仅输出指定的消息内容，然后立即停止。

## 调度规则：

- 如果命令以`/at`或`/every`开头，需通过CLI（而非Cron工具API）进行调度。
- 使用命令：`openclaw cron add`

### Telegram示例（支持夏令时）

- 默认时区：America/New_York（考虑夏令时）。
- 必须包含以下参数：
  - `--deliver`：执行任务后发送通知至指定频道。
  - `--channel telegram`：通知目标频道（例如：`--channel telegram --to <TELEGRAMCHAT_ID>`）

#### `/at`（一次性任务）：
- 如果用户提供了具体时间（例如：“3pm”），系统会将其转换为America/New_York时区的ISO格式。
- 对于短期提醒，建议使用相对时间（例如：“--at "20m”）。
- 使用`--session isolated`选项以确保任务独立运行。
- 必须包含`--message`参数以指定输出内容。

#### `/every`（重复性任务）：
- 如果需要设定间隔时间，使用`--every "<duration>"`（无需指定时区）。
- 如果需要指定具体时间，使用`--cron "<expr>" --tz "America/New_York"`。
- 同样需要使用`--session isolated`选项。

#### 确认信息：
- 系统会显示解析后的时间、任务名称和任务ID。

### 示例（支持夏令时）：

**一次性任务（考虑夏令时）：**
```bash
openclaw cron add \
  --name "提醒示例" \
  --at "2026-01-28T15:00:00-05:00" \
  --session isolated \
  --message "输出内容：<TASK>" \
  --deliver \
  --channel telegram \
  --to <TELEGRAMCHAT_ID> \
  --delete-after-run
```

**一次性任务（使用相对时间）：**
```bash
openclaw cron add \
  --name "20分钟后提醒" \
  --at "20m" \
  --session isolated \
  --message "输出内容：<TASK>" \
  --deliver \
  --channel telegram \
  --to <TELEGRAMCHAT_ID> \
  --delete-after-run
```

**重复性任务（考虑夏令时）：**
```bash
openclaw cron add \
  --name "每天下午3点提醒" \
  --cron "0 15 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "输出内容：<TASK>" \
  --deliver \
  --channel telegram \
  --to <TELEGRAMCHAT_ID>
```

**重复性任务（设定间隔时间）：**
```bash
openclaw cron add \
  --name "每两小时提醒" \
  --every "2h" \
  --session isolated \
  --message "输出内容：<TASK>" \
  --deliver \
  --channel telegram \
  --to <TELEGRAMCHAT_ID>
```

## 常用指令示例：
- “为……创建一个Cron作业”
- “设置一个提醒”
- “安排一次……”
- “提醒我……”
- “创建一个每日/每周的检查任务”
- “添加一个定期执行的任务”

## 示例说明：

| 指令内容 | 执行结果 |
|-------------|-------------------|
| “创建一个每天早上8:45的提醒” | 创建每天早上8:45的提醒任务 |
| “每两小时提醒我喝水” | 设置每小时一次的喝水提醒 |
| “每周一上午9点安排一次检查” | 创建每周一的定期检查任务 |
| “每天早上7点提醒我起床” | 设置每天早上7点的闹钟/提醒 |
| “每天早上6:30发送一条励志语” | 每天早上6:30发送励志语 |

## 支持的时间格式：**
- `8am` → `0 8 * * *`
- `8:45am` → `45 8 * * *`
- `9pm` → `0 21 * * *`
- `noon` → `0 12 * * *`
- `midnight` → `0 0 * * *`

## 支持的频率：**
- `daily` / `every day`：每天指定时间执行
- `weekdays`：周一至周五指定时间执行
- `mondays` / `every monday`：每周一执行
- `hourly` / `every hour`：每小时执行
- `every 2 hours`：每两小时执行
- `weekly`：每周执行（默认为周一）
- `monthly`：每月的第一天执行

## 通知渠道：
- 只需在请求中指定渠道（例如：“在WhatsApp上发送”）：
  - `on WhatsApp`
  - `on Telegram`
  - `on Slack`
  - `on Discord`
- 默认通知渠道：WhatsApp

## 默认消息内容：
- 该功能会自动生成合适的提醒消息：
  - **Ikigai**：每日早晨的励志提醒（包含目标、饮食、运动、社交和感恩内容）
  - **Water**：“💧 该喝水了！保持水分！🚰”
  - **Morning**：“🌅 早上好！是时候进行每日检查了。”
  - **Evening**：**🌙 晚上好！今天过得怎么样？**
  - **Weekly**：每周目标回顾
  - **Default**：“⏰ 你的提醒已发送！”