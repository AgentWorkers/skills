---
name: kanbn-todo-api
description: 通过 API 驱动的操作来管理个人在 Kan bn 中的待办事项。当用户需要创建、更新、移动、设置优先级、搜索、汇总或清理自己的 Kan bn 任务或看板数据时，都可以使用此功能——即使他们没有明确提到 API。这些操作可以响应诸如“添加一个待办事项”、“将此任务标记为优先级 1”、“将此任务标记为已完成”、“查找我的发票任务”或类似的单用户 Kan bn 任务管理请求。请注意，此功能不支持多用户协作、邀请、集成/导入以及附件功能。
---
# Kan.bn TODO API

使用此技能通过 `scripts/kanbn_todo.py` 运行 Kan.bn 的个人任务工作流。

保持交互的目标导向性：弄清楚用户想要进行的任务更改，找出任何缺失的 ID，执行最合适的 API 操作，然后清晰地报告结果。

## 配置身份验证

在运行命令之前设置身份验证：

- 使用 `KANBN_TOKEN` 进行承载式身份验证，或
- 使用 `KANBN_API_KEY` 进行 API 密钥身份验证。

`kanbn_todo.py` 中的身份验证查找顺序如下：

1. 命令行参数（`--token`、`--api-key`、`--base-url`）
2. 环境变量（`KANBN_TOKEN`、`KANBN_API_KEY`、`KANBN_BASE_URL`）
3. `~/.bashrc` 文件中的 `export` 语句（用于非交互式运行）

可选参数：

- `KANBN_BASE_URL`（默认值为 `https://kan.bn/api/v1`）

如果未设置身份验证信息，请提前停止并请求用户提供凭据或确认环境变量的来源。

## 遵循标准执行流程

### 1) 在修改数据之前先获取上下文信息

当用户未提供具体的 Kan.bn ID 时，先获取这些 ID。

```bash
python3 scripts/kanbn_todo.py me
python3 scripts/kanbn_todo.py workspaces
python3 scripts/kanbn_todo.py boards --workspace-id <workspacePublicId>
```

使用以下流程处理以下请求：
- “在 Kan.bn 中添加一个待办事项”
- “将我的任务标记为已完成”
- “查找包含发票的看板”

如果用户已经提供了具体的卡片/列表/工作空间 ID，则跳过不必要的上下文获取步骤。

### 2) 创建后读取结果

创建待办事项后，当用户需要确认待办事项、截止日期、标签或返回的 ID 时，再读取相关信息。

```bash
python3 scripts/kanbn_todo.py todo-create \
  --list-id <todoListPublicId> \
  --title "Pay electricity bill" \
  --description "Before Friday" \
  --due-date "2026-03-06T09:00:00.000Z"

python3 scripts/kanbn_todo.py todo-get --card-id <cardPublicId>
```

### 3) 选择最直接的修改方式

选择最符合用户请求的命令：
- 修改标题/描述/截止日期 -> `todo-update`
- 更改工作流状态/列表 -> `todo-move`
- 添加或删除标签 -> `todo-label-toggle`
- 删除任务 -> `todo-delete`

修改字段的具体实现：

```bash
python3 scripts/kanbn_todo.py todo-update \
  --card-id <cardPublicId> \
  --title "Pay electricity + water bill" \
  --description "Do both tonight"
```

通过更改列表来修改任务状态（例如，从待办状态改为进行中状态，再改为已完成状态）：

```bash
python3 scripts/kanbn_todo.py todo-move \
  --card-id <cardPublicId> \
  --to-list-id <doingListPublicId>
```

删除待办事项：

```bash
python3 scripts/kanbn_todo.py todo-delete --card-id <cardPublicId>
```

## 应用优先级标签规则

当请求涉及设置、标记、排序或批量分配优先级时，以标签（`P0`-`P4`）作为优先级判断的依据：
- 通过修改标签来设置优先级。
- 不要在标题中编码优先级信息。
- 保持任务标题专注于实际的工作内容。
- 如果不知道正确的优先级标签 ID，请先检查看板元数据。
- Kan.bn 的官方文档将标签修改操作放在专门的接口上，而不是 `todo-update` 接口中。

对于已存在的待办事项：

```bash
python3 scripts/kanbn_todo.py todo-label-toggle \
  --card-id <cardPublicId> \
  --label-id <p1LabelPublicId>
```

## 使用个人生产力工作流

在工作空间中搜索任务：

```bash
python3 scripts/kanbn_todo.py search --workspace-id <workspacePublicId> --query "bill"
```

添加个人备注/评论：

```bash
python3 scripts/kanbn_todo.py comment-add --card-id <cardPublicId> --comment "Waiting for invoice"
```

使用检查列表来跟踪子任务：

```bash
python3 scripts/kanbn_todo.py checklist-add --card-id <cardPublicId> --name "Prep"
python3 scripts/kanbn_todo.py checkitem-add --checklist-id <checklistPublicId> --title "Download invoice"
python3 scripts/kanbn_todo.py checkitem-update --item-id <checklistItemPublicId> --completed true
```

仅在用户明确要求时更新个人资料：

```bash
python3 scripts/kanbn_todo.py user-update --name "New Name"
```

## 小心处理缺失的信息

当用户请求执行某个操作但关键信息缺失时：
- 首先找出缺失的最基本的信息。
- 如果用户通过任务文本而不是卡片 ID 来描述任务，优先使用搜索功能。
- 如果缺失的信息与看板或列表结构相关，优先使用 “boards” 功能。
- 只有在尝试了简单的查找方法后，再进一步询问用户。

**示例**：
- 用户说 “将我的发票任务标记为已完成” -> 先搜索与发票相关的卡片，确定目标卡片，然后将其标记为已完成。
- 用户说 “将这个任务添加到我的财务看板” -> 先确定工作空间和对应的看板，然后再确认是否存在多个合适的列表。

## 仅在需要时阅读参考资料

- 阅读 `references/common-workflows.md` 以获取可复用的端到端任务处理模式。
- 当接口细节或范围边界很重要时，阅读 `references/api-scope.md`。
- 在修改脚本或验证该技能在真实 Kan.bn 账户上的表现时，阅读 `references/smoke-test.md`。

## 尊重使用范围

此技能仅使用单用户专用的待办事项接口，不支持协作、邀请、导入、集成或附件等功能。