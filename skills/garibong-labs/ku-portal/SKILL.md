---
name: ku-portal
description: 高丽大学KUPID门户查询功能：包括公告信息、本科课程安排、奖学金通知、图书馆座位信息、课程时间表以及与LMS（学习管理系统）的集成。该系统基于SonAIengine/ku-portal-mcp技术架构开发。
metadata:
  openclaw:
    min: "2026.2.0"
    requires:
      bins: ["python3"]
      config:
        - "~/.config/ku-portal/credentials.json"
        - "~/.cache/ku-portal-mcp/session.json"
        - "~/.cache/ku-portal-mcp/lms_session.json"
        - "~/.cache/ku-portal-mcp/server.log"
        - "~/Downloads/ku_timetable.ics"
---
# KU Portal – 高丽大学 KUPID 门户技能

这是一个用于查询高丽大学 KUPID 门户、图书馆及 LMS（学习管理系统）信息的 OpenClaw 技能。

## 本地文件访问

由于该技能涉及登录、缓存和导出功能，因此会使用以下路径：

- 读取：`~/.config/ku-portal/credentials.json` — KUPID 凭据文件
- 写入/读取：`~/.cache/ku-portal-mcp/session.json` — 门户会话缓存
- 写入/读取：`~/.cache/ku-portal-mcp/lms_session.json` — LMS 会话缓存
- 写入：`~/.cache/ku-portal-mcp/server.log` — MCP 服务器日志
- 写入：`~/Downloads/ku_timetable.ics` — 课程时间表（使用 `timetable --ics` 命令生成）

KUPID 凭据文件存储在技能目录之外（`~/.config` 目录中），不会被包含在 git/ClawHub 的部署包中。

## 使用方法

所有命令均应在技能目录下执行，或使用 OpenClaw 提供的 `{baseDir}` 目录作为基准。

```bash
source {baseDir}/.venv/bin/activate
python3 {baseDir}/ku_query.py <command> [options]
```

或者：

```bash
cd <skill-dir>
source .venv/bin/activate
python3 ku_query.py <command> [options]
```

## 命令列表

### 无需登录
- `library` — 查看所有图书馆的座位情况
- `library --name 中央图书馆` — 查看特定图书馆的座位情况
- `menu` — 查看今日的所有餐饮菜单（基于 koreapas.com）
- `menu --restaurant 教职员工餐厅` — 仅显示特定餐厅的菜单
- `menu --date 2026-03-10` — 查看特定日期的菜单

### 需要登录（使用 KUPID SSO）
KUPID 凭据文件：`~/.config/ku-portal/credentials.json`
```json
{"id": "your-kupid-id", "pw": "your-kupid-password"}
```

- `notices [--limit 10]` — 查看公告列表
- `notices --detail <message_id>` — 查看公告详情
- `schedules [--limit 10]` — 查看课程安排
- `scholarships [--limit 10]` — 查看奖学金信息
- `search <keyword>` — 综合搜索公告、课程安排和奖学金信息
- `timetable [--day 월]` — 查看课程时间表（可指定日期）
- `timetable --ics` — 生成 ICS 文件
- `courses --college 信息大学 --dept 计算机科学系` — 查找开设的课程
- `syllabus <course_id>` — 查看课程大纲
- `mycourses` — 查看个人选课记录

### LMS（Canvas）
- `lms courses` — 查看 LMS 中的课程
- `lms assignments <course_id>` — 查看课程作业
- `lms modules <course_id>` — 查看课程资料
- `lms todo` — 查看待办事项
- `lms dashboard` — 查看仪表板
- `lms grades <course_id>` — 查看课程成绩
- `lms submissions <course_id>` — 查看作业提交情况
- `lms quizzes <course_id>` — 查看测验列表

## 来源
- 原始代码：https://github.com/SonAIengine/ku-portal-mcp
- 分支代码：https://github.com/garibong-labs/ku-portal-mcp