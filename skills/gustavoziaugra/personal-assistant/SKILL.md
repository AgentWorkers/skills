---
name: personal-assistant
description: 个人每日简报与生产力辅助工具。可生成包含优先事项、日常习惯及自我护理提醒的晨间简报。适用于开始新的一天、规划任务、维护日常作息或促进个人成长时使用。这是一款以用户为中心的极简主义个人生产力工具。
---

# 个人助理

## 概述

生成个性化的每日简报，内容包括早晨的激励信息、优先事项、习惯跟踪以及晚上的反思。以最简单的方式帮助您提升工作效率和幸福感。

## 快速入门

```bash
# Generate daily briefing
python3 scripts/daily_briefing.py --location Columbus --summary

# Save to file
python3 scripts/daily_briefing.py --output daily_briefing.json
```

## 工作流程

### 早晨例行程序

以结构化的简报开始新的一天：
1. **激励**：以积极的态度和明确的目标开始一天
2. **天气**：查看当天的天气状况
3. **优先事项**：确定当天的前三项任务
4. **习惯**：记录当天的目标

### 白天工作期间

将简报作为参考：
- 查看优先事项列表
- 标记已完成的习惯
- 适当休息并保持水分摄入

### 晚上回顾

通过反思结束一天：
- 我今天完成了什么？
- 我对什么心存感激？
- 我有哪些可以改进的地方？
- 确定明天的优先事项

## 使用方法

### 生成简报

```bash
python3 scripts/daily_briefing.py --location Columbus --summary
```

### 参数

| 参数 | 描述 | 默认值 |
|-----------|-------------|-------------|
| `--location` | 你的城市 | Columbus | `--location Miami` |
| `--output` | 输出文件 | daily_briefing.json | `--output briefing.json` |
| `--summary` | 打印可读的输出 | false | `--summary` |

## 日常自动化

使用 OpenClaw 的 cron 任务设置早晨的简报：

```bash
# Every day at 7 AM
openclaw cron add \
  --schedule "0 7 * * *" \
  --tz "America/New_York" \
  --message "Generate my daily briefing"
```

或者手动设置：

```bash
# Morning (7 AM)
python3 scripts/daily_briefing.py --location Columbus --summary

# Evening (9 PM)
python3 scripts/daily_briefing.py --location Columbus --summary
```

## 输出格式

### JSON 结构

```json
{
  "generated_at": "2026-02-11T07:00:00.000Z",
  "location": "Columbus",
  "date": "2026-02-11",
  "weekday": "Wednesday",
  "sections": [
    {
      "title": "🌅 Good Morning!",
      "content": "Start your day...",
      "type": "motivation"
    }
  ]
}
```

## 主要部分

### 🌅 早晨激励
以专注和明确的目标开始新的一天。

### 🎯 今日重点
列出当天的前三项优先事项，并留出空间记录你的个人任务。

### ✅ 日常习惯
跟踪有助于个人成长的日常目标。

### 💚 自我关怀
提供关于水分摄入、休息和工作生活平衡的提醒。

### 🌙 晚上反思
通过结构化的问题进行自我反思，促进成长和感恩。

## 功能特点

- **简单快捷**：操作简单且效率高
- **人类可读的输出**：输出内容易于理解
- **带表情符号的章节**：章节中包含表情符号
- **地理位置感知**：根据用户位置调整内容
- **JSON 导出**：支持导出 JSON 文件以用于自动化
- **区分工作日**：区分工作日和周末的内容

## 工作原理

1. **获取当前日期和位置**：获取当前日期和用户位置
2. **创建主要部分**：生成五个核心部分
3. **格式化输出**：输出内容便于阅读
4. **导出为 JSON**：支持导出 JSON 文件以便集成到其他系统中

## 使用场景

### 个人效率提升

每天早晨通过结构化的简报来明确目标和优先事项。

### 个人成长

利用习惯跟踪和晚上反思来增强自我意识和促进个人成长。

### 远程工作

在家工作时，通过简报和休息时间来保持工作秩序和自我关怀。

### 心理健康

通过定期提醒保持水分摄入和休息，关注自己的身心健康。

## 设计理念

本工具遵循以下高效工作原则：
- 专注于重要的事情
- 简单胜过复杂
- 一致性比强度更重要
- 重视进步，而非完美

## 资源

### scripts/daily_briefing.py
生成包含所有部分的每日简报的主要脚本。

### references/productivity.md
关于个人效率和习惯养成的技巧与建议。

## 依赖项

**无**：仅使用 Python 标准库，无需外部依赖。

## 使用建议

### 早晨例行程序

- 喝咖啡时阅读简报
- 前一晚填写优先事项
- 保持简单——最多设置 3 个优先事项

### 晚上例行程序

- 花 5 分钟进行反思
- 记下明天的优先事项
- 每天练习感恩

### 建立习惯

- 从 1-2 个习惯开始
- 注重持续性的养成，而非一次性完成
- 使用 ☐/☑ 标记习惯的完成情况

## 自定义

### 添加新章节

编辑 `scripts/daily_briefing.py` 并将其添加到 `generate_briefing()` 函数中。

### 修改章节内容

每个章节都包含标题、内容和类型，可根据需要进行自定义。

## 许可证

MIT 许可证：可自由用于个人和商业用途。

## 致谢

本工具由 **Gustavo (GustavoZiaugra)** 使用 OpenClaw 开发。

- 一个简单的效率提升工具
- 注重个人心理健康
- 采用极简且实用的设计理念

---

**更多 OpenClaw 工具请访问 ClawHub.com**
**更多 OpenClaw 工具请访问 ClawHub.com**

⭐ **如果您觉得这个工具有用，请给它点赞！**
⭐ **如果您觉得这个工具有用，请给它点赞！**

📋 **这是专为您准备的个人助理。**
📋 **这是专为您准备的个人助理。**