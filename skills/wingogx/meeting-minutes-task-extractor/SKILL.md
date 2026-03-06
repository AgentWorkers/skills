---
name: meeting-minutes-task-extractor
description: 免费的基本版本可以从会议纪要中提取可执行的任务。高级升级功能可用于更详细地分解任务以及导出项目跟踪信息。
---
# 会议纪要 → 任务提取器

## 功能价值

- **免费 tier**：可提取最多 5 个可执行任务，并提供任务负责人和截止日期的提示。
- **高级 tier（仅限预订）**：可提取最多 20 个任务，支持任务分解以及任务跟踪信息的导出。

## 输入参数

- `user_id`：用户 ID
- `meeting_title`：会议标题
- `meeting_notes`：会议记录
- `tier`（可选）：`free`（免费 tier）/`premium`（高级 tier）

## 运行方式

```bash
python3 scripts/meeting_minutes_task_extractor.py \
  --user-id user_002 \
  --meeting-title "增长周会" \
  --meeting-notes "由小王负责落地页改版，截止2026-03-08"
```

## 测试用例

```bash
python3 -m unittest scripts/test_meeting_minutes_task_extractor.py -v
```