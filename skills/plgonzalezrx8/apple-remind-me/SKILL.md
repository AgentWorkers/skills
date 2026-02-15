---
name: apple-remind-me
description: 能够创建实际 Apple Reminders.app 条目的自然语言提醒功能（适用于 macOS 系统）
metadata: {"openclaw":{"emoji":"⏰","os":["darwin"],"requires":{"bins":["remindctl","date"]}}}
---

# Apple Remind Me（macOS原生工具）

使用自然语言创建、管理和组织Apple提醒事项。该工具可原生与Reminders.app配合使用，并能同步到iPhone、iPad和Apple Watch。

## 快速参考

| 操作          | 命令                | 示例                |
|------------------|------------------|-------------------|
| 创建提醒事项     | `create-reminder.sh "内容" "时间"` | `create-reminder.sh "明天下午2点给妈妈打电话"` |
| 查看提醒事项     | `list-reminders.sh [筛选条件]` | `list-reminders.sh today`       |
| 完成提醒事项     | `complete-reminder.sh ID`      | `complete-reminder.sh XXXX-XXXX`     |
| 删除提醒事项     | `delete-reminder.sh ID`      | `delete-reminder.sh XXXX-XXXX`     |
| 修改提醒内容     | `edit-reminder-message.sh ID "内容"` | `edit-reminder-message.sh XXXX "新文本"` |
| 修改提醒时间     | `edit-reminder-time.sh ID "时间"` | `edit-reminder-time.sh 明天下午3点`   |

## 可用命令

### 1. 创建提醒事项
使用自然语言创建新的提醒事项，系统会自动解析时间。

**使用方法：**
```bash
./create-reminder.sh "message" "when"
```

**示例：**
```bash
./create-reminder.sh "Pay bills" "later today"
./create-reminder.sh "Call dentist" "tomorrow at 3pm"
./create-reminder.sh "Check email" "in 2 hours"
./create-reminder.sh "Team meeting" "next monday at 10am"
```

### 2. 查看提醒事项
显示所有未完成的提醒事项，包括ID、标题、截止日期等信息。

**使用方法：**
```bash
./list-reminders.sh
```

**输出格式：**
```
⏳ ID: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
   Title: Reminder text
   Due: 2026-01-27 14:00
   List: Reminders
```

### 3. 完成提醒事项
将提醒事项标记为已完成（该事项会自动移至Reminders.app的“已完成”列表中）。

**使用方法：**
```bash
./complete-reminder.sh "REMINDER-ID"
```

**示例：**
```bash
./complete-reminder.sh "CDCBCB94-1215-494E-9F12-471AFEF25C09"
```

### 4. 删除提醒事项
永久删除某个提醒事项。

**使用方法：**
```bash
./delete-reminder.sh "REMINDER-ID"
```

**示例：**
```bash
./delete-reminder.sh "7C403BC5-6016-410A-810D-9A0F924682F9"
```

### 5. 修改提醒内容
更新现有提醒事项的文本或标题。

**使用方法：**
```bash
./edit-reminder-message.sh "REMINDER-ID" "new message"
```

**示例：**
```bash
./edit-reminder-message.sh "CDCBCB94-1215-494E-9F12-471AFEF25C09" "Updated reminder text"
```

### 6. 修改提醒时间
使用自然语言重新安排提醒事项的时间。

**使用方法：**
```bash
./edit-reminder-time.sh "REMINDER-ID" "new time"
```

**示例：**
```bash
./edit-reminder-time.sh "CDCBCB94-1215-494E-9F12-471AFEF25C09" "tomorrow at 2pm"
./edit-reminder-time.sh "CDCBCB94-1215-494E-9F12-471AFEF25C09" "in 3 hours"
./edit-reminder-time.sh "CDCBCB94-1215-494E-9F12-471AFEF25C09" "next friday"
```

## 时间解析说明

### 相对时间表达方式
格式：`in [数字] [单位]`
- `in 5 minutes` → 5分钟后
- `in 2 hours` → 2小时后
- `in 3 days` → 3天后（从当前时间算起）

### 时间快捷方式
- `later today` / `later` / `this afternoon` → 今天下午
- `tonight` → 今晚
- `tomorrow` → 明天

### 明天具体时间
格式：`tomorrow at [时间]`
- `tomorrow at 3pm` → 明天下午3点
- `tomorrow at 10:30am` → 明天上午10:30
- `tomorrow at 8pm` → 明天晚上8点

### 星期几
格式：`next [星期几]`（必须使用小写）
- `next monday` → 下周一上午9点
- `next friday` → 下周五上午9点
- `next sunday` → 下周日上午9点

**注意：** 星期几必须使用小写（如“monday”而非“Monday”）

### 备用格式（ISO格式）
- `2026-01-27 14:00` → 精确的日期和时间

## 代理实现指南

### 创建提醒事项
当用户说：“在[时间]提醒我做某事”时，系统会执行以下操作：
```bash
./create-reminder.sh "X" "Y"
```

### 查看提醒事项
当用户询问“我的提醒事项有哪些？”或“显示我的提醒事项”时，系统会执行以下操作：
```bash
./list-reminders.sh
```

### 完成提醒事项
当用户说“将[提醒事项]标记为已完成”或“完成[提醒事项]”时，系统会执行以下操作：
1. 列出所有提醒事项以找到对应的ID；
2. 使用该ID完成提醒事项：
```bash
./complete-reminder.sh "REMINDER-ID"
```

### 修改提醒事项
当用户说“将[提醒事项]的内容修改为[新内容]”或“将[提醒事项]的时间改到[新时间]”时，系统会执行以下操作：
1. 列出所有提醒事项以找到对应的ID；
2. 修改提醒事项的内容或时间：
```bash
./edit-reminder-message.sh "REMINDER-ID" "new message"
./edit-reminder-time.sh "REMINDER-ID" "new time"
```

### 删除提醒事项
当用户说“删除[提醒事项]”或“移除[提醒事项]”时，系统会执行以下操作：
1. 列出所有提醒事项以找到对应的ID；
2. 删除该提醒事项：
```bash
./delete-reminder.sh "REMINDER-ID"
```

## 工作流程示例

### 完整工作流程：查找并完成提醒事项
```bash
# 1. List all reminders
./list-reminders.sh | grep "Pay bills"

# 2. Get the ID from output
# Output shows: ID: CDCBCB94-1215-494E-9F12-471AFEF25C09

# 3. Mark as complete
./complete-reminder.sh "CDCBCB94-1215-494E-9F12-471AFEF25C09"
```

### 完整工作流程：重新安排提醒事项
```bash
# 1. List reminders and find the one to reschedule
./list-reminders.sh | grep "Team meeting"

# 2. Reschedule to new time
./edit-reminder-time.sh "REMINDER-ID" "next friday at 2pm"
```

## 技术细节

- **后端支持：** 使用`remindctl`命令行工具（macOS原生工具）
- **日期解析：** 使用BSD日期处理函数（兼容macOS）
- **时间格式：** 使用ISO 8601时间戳格式
- **列表筛选：** 默认仅显示未完成的提醒事项
- **同步功能：** 所有更改会立即同步到iCloud及所有设备

## 系统要求

- macOS（darwin系统）
- 安装了`remindctl`工具（位于`/usr/local/bin/remindctl`）
- 安装了`date`命令（BSD版本，macOS系统默认提供）
- 安装了`python3`（用于`list-reminders.sh`脚本中的JSON解析）
- 安装了Apple Reminders.app

## 限制事项

- 星期几的名称必须使用小写（例如“monday”而非“Monday”）
- 使用“next [星期几]”时，系统会添加7天（不计算下一个确切的提醒时间）
- 不支持重复提醒
- 不支持自定义提醒列表（使用系统默认的“Reminders”列表）
- 不支持基于位置的提醒功能