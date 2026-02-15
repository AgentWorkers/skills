---
name: daily-rhythm
description: 这是一个自动化的每日计划与反思系统，包含早晨简报、睡前提醒以及每周总结功能。适用于用户希望建立结构化的日常作息、早晨简报、晚间反思环节或每周规划流程的场景。该系统可触发以下功能：每日日程安排、早晨简报、睡前放松程序、睡眠提醒、每周总结，同时支持与生产力管理系统集成以实现日常规划的自动化。
---

# 日常节奏

这是一个全面的日常规划和反思系统，可自动执行晨间简报、晚间放松提醒、睡眠提醒以及每周回顾功能，帮助用户保持专注、跟踪进度并维持工作与生活的平衡。

## 快速入门

1. **安装该工具**，并确保相关脚本可执行。
2. **配置数据源**（Google Tasks，可选：Stripe，Calendar）。
3. **设置定时任务**以实现自动化操作。
4. **自定义**你的专注领域和每日目标（祷告、积极语录或冥想主题）。
5. **享受**自动化的每日简报和提醒服务。

## 功能亮点

### 日常自动化
- **上午7:00**：后台数据同步（任务、活动安排（ARR）。
- **上午8:30**：晨间简报，包含任务优先级、日历信息及天气情况。
- **晚上10:30**：提供放松提醒，帮助规划第二天的重点任务。
- **晚上11:00**：发送鼓励性的睡眠提醒。

### 周期性自动化
- **每周日晚上8:00**：进行每周回顾，帮助用户反思和规划任务。

### 丰富的晨间简报内容
- 🙏 **每日目标**：祷告、积极语录或冥想主题。
- 日历事件。
- 专注领域。
- 活动安排（ARR）进度跟踪（可选：集成Stripe功能）。
- 当天的重点任务。
- 可操作的建议。
- 详细的行动计划。
- 来自Google Tasks的任务列表。
- 天气信息（如已配置）。
- 昨天的未完成事项。

## 设置指南

### 第一步：安装依赖项

确保已安装Python 3及所需软件包：
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client stripe
```

### 第二步：配置Google Tasks

1. 访问[Google Cloud Console](https://console.cloud.google.com/)。
2. 创建项目并启用**Tasks API**。
3. 生成OAuth 2.0认证信息（适用于桌面应用程序）。
4. 将`credentials.json`文件下载到`~/.openclaw/google-tasks/`目录。
5. 运行`python3 scripts/sync-google-tasks.py`进行一次身份验证。

详细步骤请参阅[CONFIGURATION.md](references/CONFIGURATION.md)。

### 第三步：配置Stripe（可选）

如需在晨间简报中显示活动安排（ARR），请执行以下操作：
1. 在工作区根目录下创建`.env.stripe`文件：
   ```
   STRIPE_API_KEY=sk_live_...
   ```
2. 在状态文件中设置ARR目标。

### 第四步：配置Calendar

将日历的ICS（iCal）URL添加到`TOOLS.md`文件中：
```markdown
### Calendar
- **ICS URL:** `https://calendar.google.com/calendar/ical/...`
```

### 第五步：设置定时任务

**选项A：系统定时任务（传统方式）**
```bash
crontab -e

# Add these lines:
0 7 * * * cd /path/to/workspace && python3 skills/daily-rhythm/scripts/sync-stripe-arr.py
30 8 * * * cd /path/to/workspace && python3 skills/daily-rhythm/scripts/morning-brief.sh
0 20 * * 0 cd /path/to/workspace && echo "Weekly review time"
30 22 * * * cd /path/to/workspace && echo "Wind-down time"
0 23 * * * cd /path/to/workspace && echo "Sleep nudge"
```

**选项B：OpenClaw定时任务（如可用）**
使用`cron`工具创建定时任务，以生成并发送简报。

### 第六步：创建HEARTBEAT.md文件

将`assets/HEARTBEAT TEMPLATE.md`中的模板复制到工作区根目录，并进行自定义：
- 修改每日目标的文本内容（祷告、积极语录或冥想主题）。
- 更新专注领域。
- 设置活动安排（ARR）目标（如使用Stripe功能）。

## 工作流程详情

### 晨间简报生成流程

简报的生成步骤包括：
1. 同步最新数据（任务、活动安排）。
2. 从`memory/YYYY-MM-DD.md`文件中读取当天的重点任务。
3. 从日历URL获取日历信息。
4. （如已配置）获取天气信息。
5. 将所有内容整合成格式化的简报内容。

### 晚间放松提醒流程

当用户回复晚上10:30的提醒时：
1. 解析用户指定的第二天重点任务。
2. 生成可操作的建议。
3. 将任务分解为具体步骤。
4. 提供相关资源信息。
5. 请求用户确认。
6. 将信息保存到`memory/YYYY-MM-DD.md`文件中。
7. 将这些信息包含在次日的晨间简报中。

### 周期性回顾流程

每周日晚上8:00的提醒会引导用户进行反思。用户回复后：
1. 总结本周的工作情况。
2. 确定关键任务。
3. 在Google Tasks中创建新任务。
4. 预览下一天的简报内容。

## 自定义设置

### 更改每日目标

你可以自定义晨间简报的开场内容：
- **宗教相关**：祷告、圣经经文、灵修思考。
- **世俗相关**：积极语录、目标设定、感恩练习。
- **名言**：励志语录、哲学思考或诗歌。
- **目标相关**：每日使命宣言或价值观提醒。

请在HEARTBEAT.md文件中进行修改，或直接调整晨间简报的生成逻辑。

### 更改专注领域

在HEARTBEAT.md文件中更新默认的专注领域设置：
```markdown
### Focus
Your primary focus (e.g., "Product growth and customer acquisition")
```

### 调整时间

修改定时任务的设置：
- `30 8 * * *`：每天上午8:30。
- `30 22 * * *`：每天晚上10:30。
- `0 23 * * *`：每天晚上11:00。
- `0 20 * * 0`：每周日晚上8:00。

### 添加自定义内容

通过修改`scripts/morning-brief.sh`脚本，可以添加额外的数据源。

## 文件结构

```
workspace/
├── memory/
│   ├── YYYY-MM-DD.md          # Wind-down responses
│   ├── google-tasks.json      # Synced tasks
│   ├── stripe-data.json       # ARR data
│   └── heartbeat-state.json   # State tracking
├── skills/daily-rhythm/
│   ├── scripts/
│   │   ├── sync-google-tasks.py
│   │   ├── sync-stripe-arr.py
│   │   └── morning-brief.sh
│   ├── references/
│   │   └── CONFIGURATION.md
│   └── assets/
│       └── HEARTBEAT_TEMPLATE.md
└── HEARTBEAT.md               # Your custom schedule
```

## 脚本参考

### sync-google-tasks.py
将Google Tasks的数据同步到本地JSON文件。需要`credentials.json`文件。

### sync-stripe-arr.py
根据用户激活的Stripe订阅信息计算活动安排（ARR）。需要`.env.stripe`文件。

### morning-brief.sh
负责协调数据同步和简报的生成工作。

## 故障排除

**Google Tasks无法同步？**
- 确认`credentials.json`文件存在。
- 检查是否已启用Tasks API。
- 手动运行脚本以查看错误信息。

**Stripe的活动安排（ARR）未显示？**
- 确认`.env.stripe`文件中的API密钥有效。
- 检查是否有激活的订阅服务。
- 手动运行同步脚本。

**定时任务未执行？**
- 确认定时任务已正确安装：`crontab -l`。
- 检查脚本路径是否正确。
- 查看系统日志。

详细故障排除方法请参阅[CONFIGURATION.md](references/CONFIGURATION.md)。

## 最佳实践

1. **务必回复晚间放松提醒**，以获得最佳的晨间简报体验。
2. **定期更新Google Tasks中的任务信息**。
3. **定期进行每周回顾**，以确保目标与实际进度保持一致。
4. **根据需要调整专注领域**。
5. **根据个人作息时间调整定时任务的时间设置**。

## 系统要求

- Python 3.7及以上版本。
- Google Tasks API认证信息（用于任务同步）。
- Stripe API密钥（可选，用于活动安排跟踪）。
- 日历的ICS URL（可选，用于显示日历事件）。
- 安装并配置定时任务系统（Cron或OpenClaw）。