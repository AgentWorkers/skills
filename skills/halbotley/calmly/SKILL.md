---
name: calmly
description: 使用 EventKit 通过命令行管理 macOS 日历事件。适用于在 macOS 上创建、列出或查看日历事件时，无需使用 AppleScript 对话框或用户界面提示。支持全天事件、多日事件和定时事件。兼容 iCloud、本地日历以及 CalDAV 日历。
metadata:
  openclaw:
    emoji: "📅"
    os: ["darwin"]
    requires:
      bins: ["calmly"]
    install:
      - id: brew
        kind: brew
        formula: halbotley/tap/calmly
        bins: ["calmly"]
        label: "Install calmly (brew)"
---
# calmly

这是一个专为 macOS 日历设计的简洁、高效的命令行工具（CLI），无需对话框、提示信息或用户界面干扰，即可轻松管理 iCloud 和本地日历。

## 为什么选择 calmly？

- **AppleScript 会卡顿**：日历脚本在请求权限时经常会导致程序冻结。
- **ICS 导入时会弹出对话框**：这会妨碍自动化操作，需要用户手动干预。
- **icalBuddy 只能读取日历数据**：无法创建新的事件。

calmly 直接使用 EventKit 进行操作，因此运行时完全静默无声。

## 安装

```bash
brew tap halbotley/tap
brew install calmly
```

首次使用时，系统会提示您授权 calmly 访问日历（系统设置 → 隐私 → 日历）。此授权过程只需执行一次。

## 命令

### 列出所有日历

```bash
calmly list
```

### 查看即将发生的事件

```bash
calmly events Work           # Next 30 days
calmly events Family 14      # Next 14 days
```

### 创建全天事件

```bash
calmly add Work "Day Off" 2025-03-15
```

### 创建多日事件

```bash
calmly add Family "Vacation" 2025-07-01 2025-07-14
```

### 创建定时事件

```bash
calmly addtimed Work "Meeting" 2025-03-15 09:00 10:30
calmly addtimed Kids "Swim Practice" 2025-02-03 07:00 08:30
```

## 批量创建事件

对于重复性事件，可以使用 bash 脚本进行批量操作：

```bash
# Morning practice every Tuesday/Thursday for 6 weeks
for d in 2025-02-04 2025-02-06 2025-02-11 2025-02-13; do
  calmly addtimed Kids "🏊 AM Practice" "$d" 07:00 08:30
done
```

## 日期验证

在创建事件之前，请确保日期格式正确（格式为 `YYYY-MM-DD`）。

## 注意事项

- 日期使用 `YYYY-MM-DD` 格式。
- 时间使用 24 小时制格式（`HH:MM`）。
- 日历名称不区分大小写。
- 事件会自动同步到 iCloud。
- 目前 calmly 还不提供直接删除事件的命令，需通过日历应用程序或 iCloud 网页进行删除操作。