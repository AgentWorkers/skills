---
name: student-timetable
description: 学生时间表管理系统，适用于学生自行管理或家长代为管理的学生档案。系统包含初始化流程以及存储学生档案信息的数据库（位于 `schedules/profiles/` 目录下）。
---
# student-timetable

## 设计

- 支持两种操作模式：
  - **学生个人资料模式**：学生可以自行管理自己的日程安排。
  - **家长/监护人模式**：家长/监护人可以管理一个或多个孩子的日程安排。
- 采用个人资料注册表（profile registry）和每个个人资料对应的数据文件，确保查询结果在所有孩子之间保持一致，并可被其他自动化脚本重复使用。

## 初始化

- 运行交互式设置脚本：
  - `node skills/student-timetable/cli.js init`
  - 该脚本会执行以下操作：
    - 更新 `schedules/profiles/registry.json`
    - 更新 `schedules/profiles/<profile_id>/*` 文件（其中 `<profile_id>` 为个人资料ID）

## 查询

- `node skills/student-timetable/cli.js today --profile <id|name|alias>`
- `node skills/student-timetable/cli.js tomorrow --profile <id|name|alias>`
- `node skills/student-timetable/cli.js this_week --profile <id|name|alias>`
- `node skills/student-timetable/cli.js next_week --profile <id|name|alias>`

## 工具入口文件

- `tool.js`