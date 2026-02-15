---
name: calendar
description: "使用 `gcalcli` 管理 Google 日历事件。可以通过命令行界面（CLI）创建、列出和删除日历事件。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📅",
        "requires": { "bins": ["gcalcli"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "gcalcli",
              "bins": ["gcalcli"],
              "label": "Install gcalcli (pip)",
            },
          ],
      },
  }
---

# 日历功能

使用 `gcalcli` 与 Google 日历进行交互。需要 `GOOGLE_CALENDAR_API_KEY`（或使用 CalDAV 协议的 `CALDAV_URL`/`CALDAV_USER`/`CALDAV_PASS`）。

## 列出事件

列出指定日期范围内的即将发生的事件：

```bash
gcalcli agenda "2026-02-03" "2026-02-10"
```

## 创建事件

添加一个新的日历事件：

```bash
gcalcli add --title "Team sync" --when "2026-02-04 10:00" --duration 30
```

## 删除事件

通过搜索关键词删除事件：

```bash
gcalcli delete "Team sync"
```

## 安装

```bash
pip install gcalcli
```