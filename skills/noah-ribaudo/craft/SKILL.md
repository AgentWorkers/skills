---
name: craft
description: 通过 CLI（命令行界面）来管理 Craft 的笔记、文档和任务。当用户需要添加笔记、创建文档、管理任务、搜索 Craft 文档或处理日常笔记时，可以使用该功能。Craft 是一款专为 macOS/iOS 设计的笔记应用程序。
metadata: {"clawdbot":{"install":[{"id":"craft-cli","kind":"script","path":"scripts/craft","dest":"~/bin/craft","label":"Install Craft CLI"}]}}
---

# Craft CLI

用于与 Craft.do 文档、模块（blocks）和任务（tasks）进行交互。

## 设置（Setup）

1. 安装：将 `scripts/craft` 文件复制到 `~/bin/craft` 目录，并使其可执行。
2. 获取 Craft 的 API URL：在设置（Settings）> 集成（Integrations）> Craft Connect 中创建链接（Create Link）。
3. 设置环境变量：`export CRAFT_API_URL='https://connect.craft.do/links/YOUR LINK/api/v1'`。
   将此变量添加到 shell 配置文件中以实现持久化。

## 命令（Commands）

### 文档（Documents）

```bash
craft folders                    # List all folders
craft docs [location]            # List documents (unsorted, trash, templates, daily_notes)
craft doc <id>                   # Get document content by ID
craft daily [date]               # Get daily note (today, yesterday, YYYY-MM-DD)
craft search <term>              # Search across documents
craft create-doc "Title" [folderId]  # Create new document
```

### 模块（Blocks）

```bash
craft add-block <docId> "markdown"      # Add block to document
craft add-to-daily "markdown" [date]    # Add to daily note (default: today)
craft update-block <blockId> "markdown" # Update existing block
craft delete-block <blockId>...         # Delete block(s)
```

### 任务（Tasks）

```bash
craft tasks [scope]              # List tasks (inbox, active, upcoming, logbook)
craft add-task "text" [scheduleDate]  # Add task to inbox
craft complete-task <id>         # Mark task as done
craft delete-task <id>           # Delete task
```

### 集合（Collections）

```bash
craft collections                # List all collections
craft collection-items <id>      # Get items from collection
```

## 注意事项（Notes）

- 参数以 Markdown 格式传递；如有需要，请对引号进行转义。
- 日期格式：`today`、`yesterday` 或 `YYYY-MM-DD`。
- 任务范围：`inbox`（默认）、`active`、`upcoming`、`logbook`。
- 文档存储位置：`unsorted`、`trash`、`templates`、`daily_notes`。