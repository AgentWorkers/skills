---
name: macos-reminders
description: 通过 AppleScript 创建、列出和管理 macOS 的提醒事项。适用于用户需要创建提醒、添加待办事项、设置提醒，或执行任何与 macOS 上的 Apple Reminders 相关的操作的场景。例如：请求“提醒我买牛奶”、“添加一个去看牙医的待办事项”、“为周五设置提醒”、“将某项任务添加到购物清单中”或“将此事项标记为重要”。仅适用于 macOS 系统。
license: MIT
compatibility: Requires macOS with Reminders.app. Uses osascript (AppleScript) and python3 for JSON parsing.
metadata:
  author: lucaperret
  version: "1.0.0"
  openclaw:
    os: macos
    emoji: "\U00002705"
    homepage: https://github.com/lucaperret/agent-skills
    requires:
      bins:
        - osascript
        - python3
---
# macOS 提醒事项管理

通过 `$SKILL_DIR/scripts/reminders.sh` 命令来管理 Apple 的提醒事项。所有日期处理都使用相对时间计算（`当前日期 + N * 天`），以避免因地区设置（如法语/英语/德语的日期格式）而产生的问题。

## 快速入门

### 列出提醒事项列表

首先列出所有提醒事项列表，以便找到正确的列表名称：

```bash
"$SKILL_DIR/scripts/reminders.sh" list-lists
```

### 创建提醒事项

```bash
echo '<json>' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
```

**提醒事项的 JSON 格式：**

| 字段 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|
| `name` | 是 | - | 提醒事项的标题 |
| `list` | 否 | 默认列表 | 提醒事项所属的列表名称（来自 `list-lists`） |
| `body` | 否 | "" | 备注/详细信息 |
| `offset_days` | 否 | - | 到期的天数（0 表示今天，1 表示明天） |
| `iso_date` | 否 | - | 绝对到期日期（格式为 `YYYY-MM-DD`，会覆盖 `offset_days`） |
| `hour` | 否 | 9 | 到期时间（0-23 小时） |
| `minute` | 否 | 0 | 到期时间（0-59 分钟） |
| `priority` | 否 | 0 | 优先级：0=无，1=高，5=中，9=低 |
| `flagged` | 否 | false | 标记为已标记 |

### 列出所有提醒事项

```bash
echo '<json>' | "$SKILL_DIR/scripts/reminders.sh" list-reminders
```

**查询提醒事项的 JSON 格式：**

| 字段 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|
| `list` | 否 | 所有列表 | 按列表名称过滤 |
| `include_completed` | 否 | false | 包括已完成的提醒事项 |

## 理解用户指令

将用户的自然语言指令转换为 JSON 格式：

| 用户指令 | 对应的 JSON 数据 |
|---|---|
| “明天下午 2 点提醒我” | `offset_days: 1, hour: 14` |
| “3 天后提醒我” | `offset_days: 3` |
| “添加到购物清单中” | `list: "Shopping"` （匹配最接近的列表名称） |
| “高优先级”或“重要” | `priority: 1, flagged: true` |
| “2 月 25 日下午 3:30 提醒我” | `iso_date: "2026-02-25", hour: 15, minute: 30` |
| “下周一提醒我” | 根据当前日期计算到下周一的 `offset_days` |
| “标记这个提醒” | `flagged: true` |

对于 “下周一”、“下周五” 等指令，需要使用 `date` 命令来计算日期偏移量：

```bash
# Days until next Monday (1=Monday)
target=1; today=$(date +%u); echo $(( (target - today + 7) % 7 ))
```

## 示例指令及对应的操作：

**“提醒我买牛奶”**  
```bash
"$SKILL_DIR/scripts/reminders.sh" list-lists
```  
执行后：  
```bash
echo '{"name":"Buy milk","list":"Reminders"}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
```

**“添加一个待办事项：明天上午 10 点打电话给牙医”**  
```bash
echo '{"name":"Call the dentist","offset_days":1,"hour":10}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
```

**“提醒我在 2 月 28 日提交报告——高优先级”**  
```bash
echo '{"name":"Submit the report","iso_date":"2026-02-28","hour":9,"priority":1,"flagged":true}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
```

**“将鸡蛋、面包和黄油添加到购物清单中”**  
```bash
echo '{"name":"Eggs","list":"Shopping"}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
echo '{"name":"Bread","list":"Shopping"}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
echo '{"name":"Butter","list":"Shopping"}' | "$SKILL_DIR/scripts/reminders.sh" create-reminder
```

**“我的提醒事项有哪些？”**  
```bash
echo '{}' | "$SKILL_DIR/scripts/reminders.sh" list-reminders
```

**“显示我的待办事项”**  
```bash
echo '{"list":"Work"}' | "$SKILL_DIR/scripts/reminders.sh" list-reminders
```

## 重要规则：

1. **如果用户没有指定具体的列表名称，** 一定要先列出所有提醒事项列表，并使用最匹配的列表名称。
2. **在 AppleScript 中绝对不要使用硬编码的日期字符串**，始终使用 `offset_days` 或 `iso_date`。
3. **如果列表名称不明确，** 要与用户确认正确的列表名称。
4. **通过标准输入（stdin）传递 JSON 数据**，**切勿通过命令行参数传递，以避免数据泄露**。
5. **脚本会验证所有输入**（包括类型转换、范围检查、格式验证）；无效输入会显示错误信息。
6. **所有操作都会被记录到 `logs/reminders.log` 文件中**，记录包括时间戳、命令、列表名称和具体操作内容。
7. **到期日期是可选的**；没有到期日期的提醒事项也是有效的（即未设置日期的任务）。
8. **如果用户列出了多个事项**，**系统会为每个事项创建一个单独的提醒事项。