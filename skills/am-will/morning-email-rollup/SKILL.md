---
name: morning-email-rollup
description: 每天早上8点，会通过AI生成摘要的方式汇总重要的电子邮件和日历事件。
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["gog","gemini","jq","date"]}}}
---

# 早晨邮件汇总

该脚本会自动生成每日重要邮件的摘要，并在丹佛时间上午8点通过Telegram发送给用户。

## 设置

**必需步骤：** 设置您的Gmail账户邮箱地址：
```bash
export GOG_ACCOUNT="your-email@gmail.com"
```

或者直接编辑脚本以设置默认值。

## 功能介绍

- 每天上午8点（可配置时区）自动运行
- 显示来自Google Calendar的当天日程事件
- 搜索过去24小时内被标记为**重要**或**星标**的邮件
- 使用AI（Gemini CLI）为每封邮件生成自然语言摘要
- 显示最多20封最重要的邮件，包括：
  - 🔴 未读标记（红色）
  - 已读标记（绿色）
  - 发件人名称/邮箱
  - 主题行
  - **AI生成的1句话摘要**（自然语言生成，非爬取内容）
- 将格式化的摘要发送到Telegram

## 使用方法

### 手动运行
```bash
# Default (10 emails)
bash skills/morning-email-rollup/rollup.sh

# Custom number of emails
MAX_EMAILS=20 bash skills/morning-email-rollup/rollup.sh
MAX_EMAILS=5 bash skills/morning-email-rollup/rollup.sh
```

### 查看日志
```bash
cat $HOME/clawd/morning-email-rollup-log.md
```

## 工作原理

1. **检查日历**：通过`gog`命令从Google Calendar获取当天的日程事件
2. **搜索Gmail**：查询条件：`is:important OR is:starred newer_than:1d`
3. **获取邮件详情**：获取每封邮件的发件人、主题、日期和正文
4. **AI生成摘要**：使用Gemini CLI生成自然语言摘要
5. **格式化输出**：创建包含已读/未读标记的易读摘要
6. **发送到Telegram**：通过Clawdbot的消息系统发送邮件

## 日历集成

该脚本会自动从您的Google Calendar中获取当天的日程事件，使用与查询Gmail相同的`gog` CLI。

**优雅的回退机制：**
- 如果未安装`gog` → 日历部分将静默跳过（不会显示错误）
- 如果当天没有日程事件 → 日历部分将静默跳过
- 如果有日程事件 → 显示带有12小时时间和标题的格式化列表

**系统要求：**
- 必须安装并验证`gog`工具
- 使用与Gmail相同的Google账户（通过`GOG_ACCOUNT`环境变量设置）

## 邮件筛选条件

符合以下任一条件的邮件将被包含在内：
- 被Gmail标记为**重要**（闪电图标）
- 被您手动标记为**星标**
- 在过去24小时内收到

## AI摘要生成

每封邮件都使用Gemini CLI (`gemini`) 进行摘要生成：
- 提取邮件正文（去除HTML/CSS格式）
- 向`gemini --model gemini-2.0-flash`发送请求，要求其生成1句话的摘要
- 摘要为中等长度的自然语言内容（非爬取内容）
- 如果Gemini不可用，则使用清理后的邮件正文作为摘要

**重要提示：** 邮件正文作为参数传递给Gemini（而非通过标准输入），因为Gemini CLI无法正确处理带有参数的标准输入。

**示例输出：**
```
🔴 **William Ryan: Invitation to team meeting**
   The email invites you to a team meeting tomorrow at 2pm to discuss the Q1 roadmap and assign tasks for the upcoming sprint.
```

## 已读/未读标记

- 🔴 红色圆点 = 未读邮件
- 🟢 绿色圆点 = 已读邮件

所有邮件都会显示相应的标记，以确保视觉一致性。

## 格式说明

**主题行和摘要的处理：**
- 主题行中的多余引号会自动去除（例如，`""Agent Skills""` → `Agent Skills`）
- Gemini生成的摘要也会去除开头/结尾的引号
- 这样可以确保在Telegram或其他渠道中显示清晰、易读的内容

## Cron作业设置

在您方便的时间设置每日Cron作业：
```bash
cron add --name "Morning Email Rollup" \
  --schedule "0 8 * * *" \
  --tz "America/Denver" \
  --session isolated \
  --message "GOG_ACCOUNT=your-email@gmail.com bash /path/to/skills/morning-email-rollup/rollup.sh"
```

请根据需要调整时间（上午8点）和时区。

## 自定义设置

### 更改显示的邮件数量

默认情况下，汇总显示**10封邮件**。如需更改：
**临时更改（仅一次）：**
```bash
MAX_EMAILS=20 bash skills/morning-email-rollup/rollup.sh
```

**永久更改：**
编辑`skills/morning-email-rollup/rollup.sh`文件：
```bash
MAX_EMAILS="${MAX_EMAILS:-20}"  # Change 10 to your preferred number
```

### 更改搜索条件

编辑`skills/morning-email-rollup/rollup.sh`文件：
```bash
# Current: important or starred from last 24h
IMPORTANT_EMAILS=$(gog gmail search 'is:important OR is:starred newer_than:1d' --max 20 ...)

# Examples of other searches:
# Unread important emails only
IMPORTANT_EMAILS=$(gog gmail search 'is:important is:unread newer_than:1d' --max 20 ...)

# Specific senders
IMPORTANT_EMAILS=$(gog gmail search 'from:boss@company.com OR from:client@example.com newer_than:1d' --max 20 ...)

# By label/category
IMPORTANT_EMAILS=$(gog gmail search 'label:work is:important newer_than:1d' --max 20 ...)
```

### 更改发送时间

更新Cron作业时间：
```bash
# List cron jobs to get the ID
cron list

# Update schedule (example: 7am instead of 8am)
cron update <job-id> --schedule "0 7 * * *" --tz "America/Denver"
```

### 更改摘要样式

编辑`rollup.sh`文件中的`summarize_email()`函数，修改摘要生成逻辑：
```bash
# Current: medium-to-long 1 sentence
"Summarize this email in exactly 1 sentence of natural language. Make it medium to long length. Don't use quotes:"

# Shorter summaries
"Summarize in 1 short sentence:"

# More detail
"Summarize in 2-3 sentences with key details:"
```

### 更改使用的AI模型

编辑`summarize_email()`函数中的Gemini命令：
```bash
# Current: gemini-2.0-flash (fast)
gemini --model gemini-2.0-flash "Summarize..."

# Use a different model
gemini --model gemini-pro "Summarize..."
```

## 故障排除

### 未收到汇总邮件
```bash
# Check if cron job is enabled
cron list

# Check last run status
cron runs <job-id>

# Test manually
bash skills/morning-email-rollup/rollup.sh
```

### 邮件未显示
- 可能是Gmail的重要性标记设置导致邮件被过滤掉
- 请检查邮件是否在Gmail中被正确标记为重要或星标
- 尝试手动搜索：`gog gmail search 'is:important newer_than:1d`

### 摘要未显示
- 请检查`gemini` CLI是否已安装：`which gemini`
- 手动测试：`echo "test" | gemini "Summarize this:"`
- 确认Gemini已正确授权（首次运行时应会提示）

### 时区错误
- Cron作业使用`America/Denver`（MST/MDT时区）
- 请使用以下命令更新时区：`cron update <job-id> --tz "Your/Timezone"`

## 日志记录

所有汇总任务的运行记录都会保存在：
```
$HOME/clawd/morning-email-rollup-log.md
```

日志格式：
```markdown
- [2026-01-15 08:00:00] 🔄 Starting morning email rollup
- [2026-01-15 08:00:02] ✅ Rollup complete: 15 emails
```