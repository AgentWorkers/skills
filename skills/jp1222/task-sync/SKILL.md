---
name: task-sync
description: 实现TickTick（Dida）与Google Tasks之间的双向同步，包括列表/项目的映射、任务内容的同步、任务完成状态的同步，以及智能列表的导出（分为“今日”、“未来7天”和“全部”三类）。此功能适用于用户需要设置OAuth认证、运行或安排同步操作、修复任务信息不匹配/被删除/已完成的情况，或解决因截止日期处理方式导致的Google Calendar重复显示问题时。
---

# 任务同步

操作并排查 TickTick 与 Google Tasks 之间的双向任务同步问题。

## 运行方式

```bash
python {baseDir}/sync.py
```

## 设置检查清单

1. 安装 Python 3.10 及以下依赖库：`google-auth`, `google-auth-oauthlib`, `google-api-python-client`, `requests`。
2. 启用 Google Tasks API 并执行以下命令：
   ```bash
   python {baseDir}/scripts/setup_google_tasks.py
   ```
3. 创建 TickTick 开发者应用并运行相关命令：
   ```bash
   python {baseDir}/scripts/setup_ticktick.py
   ```
4. 配置 `{baseDir}/config.json` 文件中的令牌文件路径和数据存储路径。

## 预期行为

- 将 Google 任务列表与 TickTick 项目（具有相同名称的项）进行双向同步。
- 任务标题、完成状态以及备注/内容能够实现双向同步。
- 将 TickTick 的优先级映射到 Google 任务标题的前缀：`[★]` 表示高优先级，`[!]` 表示中等优先级。
- 能够将 TickTick 的智能列表（今日、未来 7 天、全部）单向导出到 Google Tasks。

## 截止日期规则（日历重复项）

- 截止日期仅保留于“全部”智能列表中。
- 对于其他已同步的列表，将日期信息转发到 TickTick 后，清除 Google 任务中的截止日期。
- 在调试日历重复项时，以 TickTick 的数据为准。

## 自动化方案

如果可用，请使用 OpenClaw 的 cron 任务来定时执行同步操作。

## 故障排除流程

1. 如果出现认证错误，请重新运行两次 OAuth 设置脚本。
2. 确认 `config.json` 文件中指定的路径指向有效的令牌文件。
3. 运行 `python {baseDir}/sync.py`，并查看 `{baseDir}/data/sync_log.json` 和 `{baseDir}/data/sync_db.json` 文件。
4. 检查相关的 API 封装脚本：
   - `{baseDir}/utils/google_api.py`
   - `{baseDir}/utils/ticktick_api.py`