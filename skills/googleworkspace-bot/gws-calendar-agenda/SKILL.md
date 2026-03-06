---
name: gws-calendar-agenda
version: 1.0.0
description: "**Google 日历：** 显示所有日历中的即将发生的事件。"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws calendar +agenda --help"
---
# 日历 + 日程安排

> **前提条件：** 阅读 `../gws-shared/SKILL.md` 以了解身份验证、全局标志和安全规则。如果文件缺失，请运行 `gws generate-skills` 来生成它。

**显示所有日历中的即将发生的事件**

## 使用方法

```bash
gws calendar +agenda
```

## 标志参数

| 标志 | 是否必填 | 默认值 | 说明 |
|------|----------|---------|-------------|
| `--today` | — | — | 显示今天的事件 |
| `--tomorrow` | — | — | 显示明天的事件 |
| `--week` | — | — | 显示本周的事件 |
| `--days` | — | — | 显示未来多少天的事件 |
| `--calendar` | — | — | 按特定日历名称或 ID 过滤事件 |

## 示例

```bash
gws calendar +agenda
gws calendar +agenda --today
gws calendar +agenda --week --format table
gws calendar +agenda --days 3 --calendar 'Work'
```

## 提示：

- 该工具仅具有读取权限，不会修改任何事件。
- 默认情况下会查询所有日历；可以使用 `--calendar` 参数进行过滤。

## 参考资料：

- [gws-shared](../gws-shared/SKILL.md) — 全局标志和身份验证设置
- [gws-calendar](../gws-calendar/SKILL.md) — 所有与日历和事件相关的管理命令