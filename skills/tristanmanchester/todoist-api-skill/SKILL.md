---
name: todoist-api
description: 通过 Todoist API v1 管理 Todoist 任务、项目、分类、标签、评论、已完成任务的报告、活动日志、ID 迁移、项目模板以及同步工作流程。适用于用户需要记录任务、快速添加工作内容、整理收件箱中的待办事项、将 Todoist 任务名称转换为对应的 ID、批量关闭或移动任务、添加重复的评论、审核已完成的工作内容、管理项目结构、导出项目模板或自动化 Todoist 工作流程的场景。
  Manages Todoist tasks, projects, sections, labels, comments, completed-task reports,
  activity logs, ID migration, project templates, and sync workflows through Todoist API v1.
  Use when the user asks to capture tasks, quick-add work, triage an inbox, resolve Todoist
  names to IDs, bulk-close or move tasks, add repeated comments, review completed work,
  manage project structure, export templates, or automate Todoist workflows.
license: MIT. See LICENSE.txt
compatibility: Requires HTTPS access to api.todoist.com plus Python 3.9+ or curl. Write operations require a Todoist API token or OAuth access token.
metadata:
  author: OpenAI
  version: "2.0.0"
  todoist_api: "v1"
  last_reviewed: "2026-03-05"
---
# Todoist API

## 何时使用此技能

当工作涉及 **Todoist 数据或自动化** 时，请使用此技能，例如：
- 捕获或快速添加新任务
- 检查、筛选、移动、完成、重新打开或删除任务
- 管理项目、分类、标签或评论
- 在写入之前将人名解析为 Todoist ID
- 使用 **dry-run** 功能执行更安全的大批量编辑操作
- 查看已完成的工作或最近的活动
- 基于公共 API 构建 Todoist 脚本、代理或集成

## 何时不使用此技能

**请勿** 使用此技能进行以下操作：
- 直接编辑用户的本地 Todoist 应用程序界面
- 与日历相关的工作流程（应使用专门的日历技能）
- 需要处理多部分数据的附件上传流程（除非您准备使用 `curl` 或 `raw` 选项）
- 非 Todoist 任务系统

## 安全默认设置

- 如果用户的意图不明确，以 **只读** 模式开始操作。
- 在任何写入操作之前，先将名称解析为 ID。
- 除非用户明确要求永久删除，否则优先选择 **关闭** 而不是 **删除**。
- 对于批量或破坏性操作，请先运行 `--dry-run`。
- 对于批量关闭、移动、重复评论或删除操作，请使用 `--confirm`。
- 如果命令可能返回大量数据，请设置 `--output FILE` 以保持 stdout 的大小可控且易于预测。

## 选择合适的接口

- **单个对象**：使用低级别的 REST 接口，如 `get-task`、`update-project` 或 `get-comment`。
- **自然语言输入**：使用 `quick-add-task`。
- **安全地解析名称**：使用 `resolve-project`、`resolve-section`、`resolve-label`。
- **创建缺失的对象**：使用 `ensure-project`、`ensure-section`、`ensure-label`。
- **处理多个匹配的任务**：使用 `bulk-close-tasks`、`bulk-move-tasks`、`bulk-comment-tasks`。
- **查看已完成的工作**：使用 `report-completed` 或 `get-completed-tasks`。
- **全量或增量同步/批量写入**：使用 `sync`。
- **未封装的特殊接口**：使用 `raw`。

## 输出格式

默认情况下，主脚本会将结构化输出打印到 stdout：
- `--format json` 会返回一个包含 `action`、`ok`、`count`、`next_cursor`、`matched_count`、`changed_count` 和 `resolved` 等字段的 JSON 数据。
- `--format summary` 会返回一个更简洁、易于阅读的摘要。
- `--output FILE` 会将完整输出写入文件，并在 stdout 上显示一条简短的 JSON 通知。

## 脚本示例

- **`scripts/todoist_api.py`**：主要的非交互式 Todoist CLI 脚本
- **`scripts/smoke_test.py`：用于检查连接是否正常的只读测试脚本

**请先查看帮助文档：**

```bash
python3 scripts/todoist_api.py --help
python3 scripts/todoist_api.py get-tasks-by-filter --help
python3 scripts/todoist_api.py bulk-move-tasks --help
python3 scripts/smoke_test.py --help
```

## 快速入门

设置一个 Todoist API 令牌：

```bash
export TODOIST_API_TOKEN="YOUR_TODOIST_TOKEN"
```

**只读测试：**

```bash
python3 scripts/smoke_test.py
```

**访问权限检查：**

```bash
python3 scripts/todoist_api.py get-projects --limit 5
python3 scripts/todoist_api.py get-labels --limit 10
```

**在写入之前解析名称：**

```bash
python3 scripts/todoist_api.py resolve-project --name "Inbox"
python3 scripts/todoist_api.py resolve-section --project-name "Client Alpha" --name "Next Actions"
python3 scripts/todoist_api.py resolve-label --name "waiting-on"
```

## 高价值代理工作流程

### 快速添加任务

```bash
python3 scripts/todoist_api.py quick-add-task \
  --text "Email Chris tomorrow at 09:00 #Work @follow-up p2"
```

### 如果分类不存在则创建

```bash
python3 scripts/todoist_api.py ensure-section \
  --project-name "Client Alpha" \
  --name "Next Actions"
```

### 预览批量关闭操作

```bash
python3 scripts/todoist_api.py bulk-close-tasks \
  --filter "overdue & @errands" \
  --dry-run
```

### 执行批量关闭操作

```bash
python3 scripts/todoist_api.py bulk-close-tasks \
  --filter "overdue & @errands" \
  --confirm
```

### 将匹配的任务移动到指定的分类中

```bash
python3 scripts/todoist_api.py bulk-move-tasks \
  --filter "#Inbox & !recurring" \
  --target-project-name "Work" \
  --target-section-name "Next Actions" \
  --dry-run
```

### 报告已完成的任务

```bash
python3 scripts/todoist_api.py report-completed \
  --since "2026-03-01T00:00:00Z" \
  --until "2026-03-31T23:59:59Z" \
  --by completion \
  --output reports/march-completed.json
```

## 推荐的操作流程

1. **解析或列出** 目标对象。
2. 使用低级别接口读取当前状态。
3. 使用 `--dry-run` 预览写入操作的结果。
4. 如有需要，使用 `--confirm` 执行操作。
5. 通过重新读取数据或运行报告命令来验证操作结果。

## 功能索引

- **命令目录和接口覆盖范围**：[references/REFERENCE.md](references/REFERENCE.md)
- **基于任务的操作指南**：[references/RECIPES.md](references/RECIPES.md)
- **Todoist 特有的注意事项**：[references/GOTCHAS.md](references/GOTCHAS.md)

## 临时解决方案

- 当公共 CLI 接口尚未提供所需的功能时，可以使用 `raw` 选项：
```bash
python3 scripts/todoist_api.py raw \
  --method GET \
  --path /projects/PROJECT_ID/full
```

- 当需要增量同步或批量执行命令时，使用 `sync`：
```bash
python3 scripts/todoist_api.py sync \
  --sync-token '*' \
  --resource-types '["all"]'
```