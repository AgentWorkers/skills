---
name: tripit_calendar
description: 从 TripIt 的 iCal 数据源中读取即将发生的旅行计划。
metadata: {"openclaw":{"os":["linux","darwin"],"requires":{"bins":["python"],"env":["TRIPIT_ICAL_URL"]}}}
---
# TripIt 日历

当用户询问以下内容时，可以使用此技能：
- 下一次旅行
- 即将到来的旅行
- 旅行行程
- TripIt 的旅行计划
- 即将出发的航班或酒店信息
- 本月的旅行安排

## 所需条件

使用此技能需要以下工具或环境：
- Python
- 环境变量 `TRIPIT_ICAL_URL`
- Python 包 `requests` 和 `icalendar`

## 设置

在 OpenClaw 虚拟环境中安装所需的 Python 包：

```bash
source ~/.openclaw/workspace/openclaw_venv/bin/activate
pip install requests icalendar
```