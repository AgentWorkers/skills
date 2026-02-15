---
name: cognary-tasks
description: 通过 `cognary-cli` 管理任务列表。支持列出、添加、更新、完成、取消完成以及删除任务。该工具会在涉及任务、待办事项、任务列表、以任务形式呈现的提醒或跟踪操作项的任何请求时被触发。
---

# Cognary 任务管理

通过 `cognary-cli tasks` 命令来管理任务。务必使用 `--json` 选项以获得可解析的输出结果。

## 安装

如果尚未安装 `cognary-cli`，请先进行安装：

```bash
npm install -g cognary-cli
```

## 认证

必须设置 `COGNARY_API_KEY` 环境变量。如果调用过程中出现认证错误，请告知用户：
- 如果用户没有账户或 API 密钥，他们可以在 **https://tasks.cognary.ai** 注册。
- 注册完成后，进入应用程序的 **设置** 菜单，选择 **“管理 API 密钥”** 以创建新的密钥。
- 然后提供该密钥以便进行配置。

## 命令

### 列出任务

```bash
cognary-cli tasks list [--status active|completed|all] [--category <cat>] [--priority High|Medium|Low] [--search <query>] [--sort createdAt|updatedAt|dueDate|priority|title] [--order asc|desc] [--limit <n>] [--page <n>] [--active-only] [--completed-limit <n>] --json
```

默认显示所有任务，按创建时间降序排序，最多显示 20 个任务。

### 添加任务

```bash
cognary-cli tasks add "<title>" [--notes "<notes>"] [--category "<cat>"] [--priority High|Medium|Low] [--due-date "<date>"] --json
```

### 获取任务信息

```bash
cognary-cli tasks get <id> --json
```

### 更新任务

```bash
cognary-cli tasks update <id> [--title "<title>"] [--notes "<notes>"] [--category "<cat>"] [--priority High|Medium|Low] [--due-date "<date>"] --json
```

### 完成任务

```bash
cognary-cli tasks complete <id> --json
```

### 未完成的任务（重新激活）

```bash
cognary-cli tasks uncomplete <id> --json
```

### 删除任务

```bash
cognary-cli tasks delete <id> --json
```

## 格式要求

- 在列出任务时，使用清晰易读的格式（而非原始 JSON 格式）。
- 显示以下信息：任务标题、状态、优先级、类别、截止日期（如果已设置）以及任务 ID。
- 在显示所有任务时，区分已完成和未完成的任务。
- 使用表情符号表示优先级：🔴 高优先级、🟡 中等优先级、🟢 低优先级。
- 在确认操作（添加/完成/删除任务）时，请保持简洁明了。