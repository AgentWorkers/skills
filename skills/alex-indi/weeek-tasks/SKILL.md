---
name: weeek-tasks
description: "通过 Public API（任务管理器）管理 WEEEK 任务：获取任务列表、创建/更新/完成任务、在任务板/列之间切换任务，以及获取任务板与列的列表。该功能适用于与 WEEEK API 的集成，以及处理任务、任务板及相关列的操作。"
---

# WEEEK 任务管理

## 快速入门

1. 设置环境变量：
   - `WEEEK_TOKEN`：授权令牌
   - `WEEEK_USER_ID`：您的 WEEEK 用户 ID（可选）
2. 使用 `scripts/weeek_api.py` 进行相关操作。
3. 如需了解端点详情，请参阅 `references/api.md`。

## 脚本

### 获取任务

```bash
python scripts/weeek_api.py list-tasks --day DD.MM.YYYY --board-id ID_доски --board-column-id ID_колонки
```

### 创建任务

```bash
python scripts/weeek_api.py create-task --title "Задача" --day DD.MM.YYYY --no-locations
```

如果需要将任务关联到特定项目或看板，请提供 `project_id`、`board_id` 或 `board_column_id`，或使用 JSON 格式传递相关信息：

```bash
python scripts/weeek_api.py create-task --title "Задача" --locations-json '[{"boardId":ID_доски,"boardColumnId":ID_колонки}]'
```

### 更新任务

```bash
python scripts/weeek_api.py update-task ID_задачи --title "Новый заголовок" --priority 2
```

### 完成任务或返回任务状态

```bash
python scripts/weeek_api.py complete-task ID_задачи
python scripts/weeek_api.py uncomplete-task ID_задачи
```

### 移动任务

```bash
python scripts/weeek_api.py move-board ID_задачи --board-id ID_доски
python scripts/weeek_api.py move-board-column ID_задачи --board-column-id ID_колонки
```

### 项目/看板/列列表

```bash
python scripts/weeek_api.py list-projects
python scripts/weeek_api.py list-boards --project-id ID_проекта
python scripts/weeek_api.py list-board-columns --board-id ID_доски
```

您可以通过 `list-projects`、`list-boards` 和 `list-board-columns` 命令获取项目/看板/列的列表。

## 限制与注意事项

- 文档中提到的 `day` 格式为字符串类型；具体格式请咨询用户。
- 默认情况下，创建的任务不关联任何项目或看板（使用 `--no-locations` 选项）。
- 如果指定了 `WEEEK_USER_ID`，该 ID 会自动填充到 `userId` 和 `assignees` 字段中。