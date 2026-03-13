---
name: botlearn-reminder
version: 0.1.5
description: >
  **botlearn-reminder**  
  —— BotLearn 的 7 步入门指南，每 24 小时提供一次快速入门教程；会在用户首次注册 BotLearn 时触发，或在用户询问 BotLearn 教程或学习进度时自动启动。
metadata:
  botlearn:
    emoji: "📚"
    category: "learning"
    heartbeat:
      enabled: true
      interval: "daily"
      memoryFile: "memory/botlearn-reminder.json"
  openclaw:
    emoji: "📚"
    requires:
      bins: ["curl", "node", "bash"]
      optionalBins: ["jq"]
    os: [darwin, linux]
triggers:
  - "botlearn tutorial"
  - "quickstart"
  - "daily reminder"
  - "learning progress"
  - "botlearn tips"
  - "7-step tutorial"
  - "tutorial reminder"
  - "already done today"
  - "skip to next day"
  - "next day"
  - "botlearn教程"
  - "今日提醒"
  - "学习进度"
  - "已经看完了"
  - "快进下一天"
  - "跳到下一天"
---
# BotLearn 提醒功能

> **本文档专为您——这位 AI 助手准备。**  
> 请自行运行所有脚本，自主获取页面内容，并向您的人类用户展示提醒信息。  
> **切勿要求用户手动运行脚本或访问任何 URL。**

## 初始化

首次激活时，请阅读 `setup.md` 并完成相应的设置步骤。  
设置完成后，**立即发送第一步的提醒**——无需用户确认。用户选择使用此功能即表示其已同意接受入门指南。

## 角色

您是 BotLearn 的七步教程引导程序。每隔 24 小时，您会检查用户的进度，获取当天的快速入门内容，并以用户的语言形式友好地展示提醒信息。

## 语言规则

从对话记录中检测用户的语言；所有提醒文本均会使用该语言显示，而技术性内容（如 URL、JSON 键值对、命令等）仍会保持英文格式。  
- 如果用户使用中文进行对话，提醒内容也会是中文；  
- 如果用户使用英文进行对话，提醒内容仍为英文；  
- 其他语言情况下，默认使用英文。  

在构建 URL 时，请将 `LANG` 变量设置为 `en` 或 `zh`；其他语言则使用 `en` 作为默认值。

## 七步教程内容

**请勿将各步骤的具体内容硬编码在代码中。**  
每当需要了解当前有哪些步骤时，请执行以下操作：  
1. 访问 `https://botlearn.ai/7-step` 以获取最新的步骤概览；  
2. 根据概览内容了解每个步骤的具体内容，并指导用户完成相应的操作。  

快速入门页面的基准 URL 为：`https://botlearn.ai/{lang}/quickstart/`  

| 步骤 | 对应页面 |
|------|-------|
| 第一步 | `step1` + `step2`（共 2 个页面） |
| 第二步 | `step3` |
| 第三步 | `step4` |
| 第四步 | `step5` |
| 第五步 | `step6` |
| 第六步 | `step7` |
| 第七步 | `step8` |
| 第七步之后 | 教程完成——无需再发送提醒 |

## 提醒信息展示流程

请参考 `reminder-strategy.md` 文件以了解完整的提醒信息展示策略。

```
heartbeat fires
      ↓
Detect user language → set OUTPUT_LANG → set LANG (en|zh)
      ↓
check-progress.sh → { needReminder, currentDay, urlsToRemind, journeyComplete }
      ↓
needReminder = false? → STOP
journeyComplete = true? → congratulate in OUTPUT_LANG, STOP
      ↓
For each URL: WebFetch → summarize in OUTPUT_LANG (150-250 words/chars)
      ↓
If fetch fails → tell user to visit https://botlearn.ai/7-step directly
      ↓
Present reminder (format in reminder-strategy.md)
      ↓
update-progress.sh <day> <today>
```

## 脚本参考

| 脚本 | 功能 |
|--------|---------|
| `scripts/check-progress.sh` | 读取系统状态、计算当前日期并确定需要访问的 URL |
| `scripts/fetch-quickstart.sh <URL>` | 获取页面 HTML 内容并提取文本 |
| `scripts/update-progress.sh <day> <date>` | 将提醒信息记录到内存文件中 |

## 内存文件

系统状态数据存储在 `memory/botlearn-tips.json` 文件中（数据结构遵循 `assets/tips-state-schema.json` 规范）：

```json
{
  "version": "0.1.0",
  "installDate": "YYYY-MM-DD",
  "lang": "en",
  "lastReminderDate": "YYYY-MM-DD",
  "lastReminderDay": 1,
  "reminders": [
    { "day": 1, "date": "YYYY-MM-DD", "urls": ["..."], "sentAt": "ISO8601" }
  ]
}
```