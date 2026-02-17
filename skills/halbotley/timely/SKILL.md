---
name: timely
description: 通过命令行管理 Apple 提醒事项，并支持地理围栏功能。适用于在 macOS 上创建提醒事项时，可设置基于位置的触发条件（如到达/离开某个地点）、截止日期或基于时间的提醒。该工具支持与 iCloud 同步的提醒列表。
metadata:
  openclaw:
    emoji: "⏰"
    os: ["darwin"]
    requires:
      bins: ["timely"]
    install:
      - id: brew
        kind: brew
        formula: halbotley/tap/timely
        bins: ["timely"]
        label: "Install timely (brew)"
---
# timely

这是一个支持地理围栏功能的Apple Reminders命令行工具（CLI），无需用户界面即可创建基于位置和时间触发的提醒。

## 为什么选择“timely”？

- **位置触发**：在到达或离开某个地点时提醒用户
- **无需用户界面提示**：通过EventKit在后台默默运行
- **iCloud同步**：提醒会显示在所有设备上

## 安装

```bash
brew tap halbotley/tap
brew install timely
```

首次使用时，需要授权访问Reminders功能（系统设置 → 隐私 → Reminders），此操作仅需执行一次。

## 命令

### 列出提醒列表

```bash
timely lists
```

### 查看提醒

```bash
timely show Reminders        # Show all in list
timely show Reminders 10     # Show last 10
```

### 创建基于时间的提醒

```bash
timely add Reminders "Call mom" --due "tomorrow 3pm"
timely add Reminders "Submit report" --due "friday 5pm"
```

### 创建基于位置的提醒（到达）

```bash
timely add Reminders "Buy milk" \
  --location "Trader Joe's" \
  --address "123 Main St, Santa Barbara, CA" \
  --arrive
```

### 创建基于位置的提醒（离开）

```bash
timely add Reminders "Text wife leaving" \
  --location "Office" \
  --address "456 Work Ave" \
  --depart
```

### 结合时间和位置触发

```bash
timely add Reminders "Pick up prescription" \
  --due "today" \
  --location "CVS" \
  --address "789 Pharmacy Rd" \
  --arrive
```

## 到期日期格式

支持以下自然语言格式：

- `"today"`（今天）
- `"tomorrow"`（明天）
- `"monday"`（星期一）
- `"next friday"`（下周五）
- `"tomorrow 3pm"`（明天下午3点）
- `"friday 5pm"`（周五下午5点）
- `"2025-03-15"`（2025年3月15日）
- `"2025-03-15 14:30"`（2025年3月15日14:30）

## 地理围栏设置说明

- `--location`：用于设置提醒的显示名称（在Reminders应用中显示的名称）
- `--address`：用于地理编码（必须是一个真实的地址）
- `--arrive`：在进入该地点时触发提醒
- `--depart`：在离开该地点时触发提醒
- 默认的地理围栏半径约为100米

## 共享提醒列表

对于共享的iCloud提醒列表，请使用在Reminders应用中显示的列表名称。这些列表会在所有家庭成员的设备上同步。

## 示例

```bash
# Simple reminder
timely add Reminders "Water plants" --due "saturday 9am"

# Reminder when getting home
timely add Reminders "Take out trash" \
  --location "Home" \
  --address "123 My Street, My City, CA" \
  --arrive

# Reminder when leaving work
timely add Reminders "Pick up kids" \
  --location "Office" \
  --address "456 Work Blvd" \
  --depart
```