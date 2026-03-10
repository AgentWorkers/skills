---
name: kanbn-todo-api
description: 通过 API 驱动的操作在 Kan.bn 中管理个人待办事项。适用于需要在 Kan.bn 上实现单用户任务管理的工作流程，包括待办事项的创建（CREATE）、读取（READ）、更新（UPDATE）和删除（DELETE）操作，以及在不同状态列表之间移动待办事项、完成清单项、搜索以及更新个人资料等操作；不包括多用户协作、邀请功能、集成/导入以及附件功能。
---
# Kan.bn TODO API

使用此技能可通过 `scripts/kanbn_todo.py` 执行 Kan.bn 的 TODO 操作。

## 配置

在运行命令之前，请设置认证信息：

- 使用 `KANBN_TOKEN` 进行承载式认证，或
- 使用 `KANBN_API_KEY` 进行 API 密钥认证。

`kanbn_todo.py` 中的认证信息查找顺序如下：
1. 命令行参数（`--token`、`--api-key`、`--base-url`）
2. 环境变量（`KANBN_TOKEN`、`KANBN_API_KEY`、`KANBN_BASE_URL`）
3. `~/.bashrc` 文件中的 `export` 语句（用于非交互式运行）

可选参数：
- `KANBN_BASE_URL`（默认值为 `https://kan.bn/api/v1`）

## 优先级标签规则

当请求涉及设置、标记、排序或批量分配优先级时，请以标签（`P0`-`P4`）作为优先级依据。

- 通过修改标签来设置优先级。
- 对于已存在的任务，使用以下命令：`python3 scripts/kanbn_todo.py todo-label-toggle --card-id <cardPublicId> --label-id <labelPublicId>`。
- 请勿在任务标题中编码优先级（例如，不要在任务标题前添加 `[P0]`/`[P1]`）。
- 任务标题应仅包含实际的工作内容。
- 注意：Kan.bn 的官方文档将标签更改操作放在专门的接口上，而非 `todo-update` 接口中。

## 执行核心 TODO 流程

使用以下命令执行相应操作：`python3 scripts/kanbn_todo.py <command> ...`

### 1) 查找工作空间和看板

```bash
python3 scripts/kanbn_todo.py me
python3 scripts/kanbn_todo.py workspaces
python3 scripts/kanbn_todo.py boards --workspace-id <workspacePublicId>
```

### 2) 创建 TODO 并读取其内容

```bash
python3 scripts/kanbn_todo.py todo-create \
  --list-id <todoListPublicId> \
  --title "Pay electricity bill" \
  --description "Before Friday" \
  --due-date "2026-03-06T09:00:00.000Z"

python3 scripts/kanbn_todo.py todo-get --card-id <cardPublicId>
```

### 3) 更新 TODO 或更改状态

- 编辑任务字段：

```bash
python3 scripts/kanbn_todo.py todo-update \
  --card-id <cardPublicId> \
  --title "Pay electricity + water bill" \
  --description "Do both tonight"
```

- 通过移动任务状态来更改任务状态（例如：TODO -> DOING -> DONE）：

```bash
python3 scripts/kanbn_todo.py todo-move \
  --card-id <cardPublicId> \
  --to-list-id <doingListPublicId>
```

- 为现有任务添加或删除优先级标签：

```bash
python3 scripts/kanbn_todo.py todo-label-toggle \
  --card-id <cardPublicId> \
  --label-id <p1LabelPublicId>
```

### 4) 删除 TODO

```bash
python3 scripts/kanbn_todo.py todo-delete --card-id <cardPublicId>
```

## 使用仅限个人的增强功能

- 在工作空间中搜索任务：

```bash
python3 scripts/kanbn_todo.py search --workspace-id <workspacePublicId> --query "bill"
```

- 添加个人备注/评论：

```bash
python3 scripts/kanbn_todo.py comment-add --card-id <cardPublicId> --comment "Waiting for invoice"
```

- 使用检查列表来跟踪子任务：

```bash
python3 scripts/kanbn_todo.py checklist-add --card-id <cardPublicId> --name "Prep"
python3 scripts/kanbn_todo.py checkitem-add --checklist-id <checklistPublicId> --title "Download invoice"
python3 scripts/kanbn_todo.py checkitem-update --item-id <checklistItemPublicId> --completed true
```

## 注意使用范围

此技能仅支持单用户使用的 TODO 接口。请勿在此处执行协作、邀请、导入、集成或附加文件等操作。

如需了解接口详情，请参阅 `references/api-scope.md`。