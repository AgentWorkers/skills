---
name: topydo
description: 使用 `topydo CLI` 管理 `todo.txt` 任务。可以执行添加、列出、完成、设置优先级、添加标签等操作，并能处理具有依赖关系、截止日期、重复周期以及关联项目的任务。适用于各种任务管理场景，无论是简单的待办事项列表，还是用户直接提及的“任务”或“todo.txt”文件。需要 Python 3 和 `pip` 的支持。支持在 macOS、Linux 和 Windows 系统上运行。
license: MIT
metadata:
  author: github.com/bastos
  version: "2.0"
---

# topydo - Todo.txt 任务管理器

topydo 是一个功能强大的命令行工具（CLI），用于管理以 `todo.txt` 格式存储的任务。它支持任务之间的依赖关系、截止日期、开始日期、重复规则、优先级、项目以及任务所属的上下文等信息。

## 任务格式参考

```
(A) 2025-01-11 Task text +Project @Context due:2025-01-15 t:2025-01-10 rec:1w star:1
│   │          │         │        │        │             │            │      │
│   │          │         │        │        │             │            │      └─ Star marker
│   │          │         │        │        │             │            └─ Recurrence
│   │          │         │        │        │             └─ Start/threshold date
│   │          │         │        │        └─ Due date
│   │          │         │        └─ Context
│   │          │         └─ Project
│   │          └─ Task description
│   └─ Creation date
└─ Priority (A-Z)
```

## 安装

### Homebrew（macOS，推荐使用）
```bash
brew install topydo
```

### pip（所有平台）
```bash
pip3 install topydo
```

### apt（Ubuntu/Debian）
```bash
sudo apt install python3-pip && pip3 install topydo
```

## 配置

配置文件的位置（优先级顺序）：
- `topydo.conf` 或 `.topydo`（当前目录）
- `~/.topydo` 或 `~/.config/topydo/config`
- `/etc/topydo.conf`

示例 `~/.topydo` 配置文件：
```ini
[topydo]
filename = ~/todo.txt
archive_filename = ~/done.txt
colors = 1
identifiers = text

[add]
auto_creation_date = 1

[sort]
sort_string = desc:importance,due,desc:priority
ignore_weekends = 1
```

## 添加任务

基本任务：
```bash
topydo add "Buy groceries"
```

设置优先级（A 为最高优先级）：
```bash
topydo add "(A) Urgent task"
```

为任务指定项目及上下文：
```bash
topydo add "Write report +ProjectX @office"
```

设置绝对截止日期：
```bash
topydo add "Submit proposal due:2025-01-15"
```

设置相对截止日期：
```bash
topydo add "Call mom due:tomorrow"
```

设置基于工作日的截止日期：
```bash
topydo add "Weekly review due:fri"
```

设置开始/截止日期：
```bash
topydo add "Future task t:2025-02-01"
```

设置每周重复规则：
```bash
topydo add "Water plants due:sat rec:1w"
```

设置严格的重复规则（每月1日执行）：
```bash
topydo add "Pay rent due:2025-02-01 rec:+1m"
```

设置任务之间的依赖关系（任务2依赖于任务1）：
```bash
topydo add "Write tests before:1"
```

将任务1设置为任务2的子任务：
```bash
topydo add "Review code partof:1"
```

## 列出任务

列出所有相关任务：
```bash
topydo ls
```

列出隐藏/被屏蔽的任务：
```bash
topydo ls -x
```

按项目筛选任务：
```bash
topydo ls +ProjectX
```

按上下文筛选任务：
```bash
topydo ls @office
```

按优先级筛选任务：
```bash
topydo ls "(A)"
```

按优先级范围筛选任务：
```bash
topydo ls "(>C)"
```

筛选今日到期的任务：
```bash
topydo ls due:today
```

筛选逾期未完成的任务：
```bash
topydo ls "due:<today"
```

筛选周五到期的任务：
```bash
topydo ls "due:<=fri"
```

组合多个筛选条件：
```bash
topydo ls +ProjectX @office due:today
```

排除特定上下文的任务：
```bash
topydo ls -- -@waiting
```

按优先级排序：
```bash
topydo ls -s priority
```

按截止日期降序排序，再按优先级排序：
```bash
topydo ls -s desc:due,priority
```

按项目分组任务：
```bash
topydo ls -g project
```

限制显示结果数量为5条：
```bash
topydo ls -n 5
```

自定义输出格式：
```bash
topydo ls -F "%I %p %s %{due:}d"
```

将任务信息输出为 JSON 格式：
```bash
topydo ls -f json
```

## 完成任务

通过任务ID完成任务：
```bash
topydo do 1
```

一次性完成多个任务：
```bash
topydo do 1 2 3
```

完成今日到期的所有任务：
```bash
topydo do -e due:today
```

设置自定义完成日期来完成任务：
```bash
topydo do -d yesterday 1
```

## 优先级管理

设置任务的优先级为 A：
```bash
topydo pri 1 A
```

为多个任务设置优先级：
```bash
topydo pri 1 2 3 B
```

移除任务的优先级：
```bash
topydo depri 1
```

## 为任务添加标签

设置任务的截止日期：
```bash
topydo tag 1 due tomorrow
```

给任务添加星标：
```bash
topydo tag 1 star 1
```

移除任务的标签：
```bash
topydo tag 1 due
```

为任务设置带有相对日期的标签：
```bash
topydo tag -r 1 review 2w
```

## 修改任务

向任务中添加文本内容：
```bash
topydo append 1 "additional notes"
```

修改任务的截止日期：
```bash
topydo append 1 due:friday
```

使用文本编辑器编辑任务：
```bash
topydo edit 1
```

批量编辑项目中的所有任务：
```bash
topydo edit -e +ProjectX
```

## 删除任务

通过任务ID删除任务：
```bash
topydo del 1
```

批量删除多个任务：
```bash
topydo del 1 2 3
```

根据特定条件删除任务：
```bash
topydo del -e completed:today
```

## 任务依赖关系

设置任务2依赖于任务1：
```bash
topydo dep add 2 to 1
```

将任务2设置为任务1的子任务：
```bash
topydo dep add 2 partof 1
```

列出依赖于任务1的任务：
```bash
topydo dep ls 1 to
```

列出任务1依赖于哪些任务：
```bash
topydo dep ls to 1
```

移除任务之间的依赖关系：
```bash
topydo dep rm 2 to 1
```

可视化任务依赖关系（需要使用 graphviz 工具）：
```bash
topydo dep dot 1 | dot -Tpng -o deps.png
```

## 延迟任务

将任务推迟1周：
```bash
topydo postpone 1 1w
```

将任务推迟3天：
```bash
topydo postpone 1 3d
```

推迟任务的同时保留开始日期：
```bash
topydo postpone -s 1 1w
```

## 其他命令

对 `todo.txt` 文件进行排序：
```bash
topydo sort
```

撤销上一次执行的操作：
```bash
topydo revert
```

查看操作历史记录：
```bash
topydo revert ls
```

列出所有项目：
```bash
topydo lsprj
```

列出所有任务所属的上下文：
```bash
topydo lscon
```

归档已完成的任务：
```bash
topydo archive
```

## 相对日期

- `today`（今天），`tomorrow`（明天），`yesterday`（昨天）
- 工作日：`mon`（周一），`tue`（周二），`wed`（周三），`thu`（周四），`fri`（周五），`sat`（周六），`sun`（周日）
- 时间单位：`1d`（天），`2w`（周），`3m`（月），`1y`（年）
- 工作日：`5b`（不包括周末）

## 排序/分组字段

- `priority`（优先级），`due`（截止日期），`creation`（创建时间），`completed`（完成状态）
- `importance`（重要性），`importance-avg`（平均重要性）
- `project`（项目），`context`（上下文），`text`（任务描述），`length`（任务长度）

使用 `desc:` 前缀进行降序排序。例如：`desc:importance,due`（按重要性降序排序，再按截止日期排序）

## 提示

- 使用清晰、易于阅读的格式向用户展示任务信息
- 在配置文件中设置 `identifiers = text` 以使用稳定的任务ID
- 为重要任务添加星标：使用 `star:1` 标签
- 默认情况下，`id`、`p`、`ical` 标签表示任务被隐藏
- 任务的重要性 = 优先级 + 截止日期的接近程度 + 是否被标记为重要任务