---
name: todoist
description: 使用 `td`（Todoist CLI）命令行工具，可以从终端读取和管理 Todoist 中的任务列表。该工具会在用户查询任务列表、日程安排、待办事项、检查清单（今日任务、即将到期的任务、逾期任务），或者希望以自然语言方式添加新任务，以及更新、完成、删除或移动任务时被触发。例如：用户可以在任务描述中添加电话号码，修改任务的截止日期、优先级或标签等操作。
---

# 通过 `td` CLI 使用 Todoist

## 安装/验证

仓库地址：https://github.com/Doist/todoist-cli

如果 `td` 未安装（例如，出现“command not found: td”错误），请从该仓库进行安装：

```bash
git clone https://github.com/Doist/todoist-cli
cd todoist-cli
npm install
npm run build
npm link
```

安装完成后，进行验证：

```bash
td --help
```

### 使用 `td` 执行所有 Todoist 操作

建议使用易于解析的输出格式：

- 使用 `--json`（或 `--ndjson`）来列出/读取任务。
- 使用 `td task update ...` 来编辑任务（内容、截止日期、描述、优先级、标签等）。

## 常用命令

- 查看今日及过期的任务：
  - `td today --json`
- 查看接下来 N 天内的任务：
  - `td upcoming 7 --json`
- 查看收件箱中的任务：
  - `td inbox --json`

### 为用户总结任务安排

- 区分**过期的任务**和**今日到期的任务**（可选地还包括**即将到期的任务**）。
- 如果有优先级信息，请一并显示（p1–p4）以及所有标签。

## 查找要编辑的任务

**推荐方法**：

1. 如果已知任务 ID，可以直接使用该 ID：
  - 格式示例：`id:6WcqCcR4wF7XW5m6`

2. 如果只知道任务标题或部分内容，可以先搜索/列出任务，然后根据具体条件筛选：
  - `td task list --json`（可选地使用 `today`、`upcoming`、`inbox` 等筛选条件）
  - 之后根据任务内容、截止日期或项目名称选择正确的任务。

### 查看单个任务

- `td task view <ref> --json`

## 常见编辑操作

- 更新任务描述：
  - `td task update <ref> --description "..."`

- 更新任务标题/内容：
  - `td task update <ref> --content "新任务标题..."`

- 更改任务截止日期：
  - `td task update <ref> --due "明天下午 3 点"`

- 设置任务优先级：
  - `td task update <ref> --priority p1`（或 p2/p3/p4）

- 更改任务标签：
  - `td task update <ref> --labels "杂务, 电话"`（替换现有标签）

- 完成/重新开启任务：
  - `td task complete <ref>`
  - `td task uncomplete id:<taskId>`

- 删除任务：
  - `td task delete <ref> --yes`（仅当用户明确表示要删除任务时使用）

## 添加任务

- 使用自然语言快速添加任务：
  - `td add "明天上午 10 点看牙医 #个人事务"`

- 或者通过结构化字段添加任务：
  - `td task add --content "..." --due "..." --priority p2 --labels "..."`

## 安全性/用户体验

- 在执行删除等破坏性操作前，请务必确认。
- 如果有多个任务符合用户的描述，在更新前请询问用户以获取确认（或展示可选的任务列表）。
- 当用户需要添加信息（例如电话号码）时，建议将其放入**描述**字段中，除非用户特别要求将其放在标题中。