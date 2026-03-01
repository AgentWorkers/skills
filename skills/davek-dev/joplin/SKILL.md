---
name: joplin
description: 通过 CLI 与 Joplin 笔记本进行交互。支持读取、创建、编辑笔记以及管理待办事项。同时支持 WebDAV 同步和 Kanban 格式的笔记。
---
# Joplin CLI 使用指南

使用 `joplin` CLI 来操作 Joplin 笔记。

## ⚠️ 重要提示：请使用 CLI，而非 SQL

**请始终使用 `joplin` CLI 来编辑笔记。** 除非万不得已，否则不要直接修改 SQLite 数据库。直接修改数据库可能会导致同步冲突和数据丢失。

## 设置

如果 Joplin 未配置 WebDAV，请进行配置：

```bash
joplin config sync.target 6
joplin config sync.6.path "https://your-webdav-server/path"
joplin config sync.6.username "your-username"
joplin config sync.6.password "your-password"
joplin sync
```

## 常用命令

### 列出笔记本和笔记
```bash
joplin ls                          # List notebooks
joplin ls "Notebook Name"          # List notes in a notebook
joplin status                      # Show sync status and note counts
joplin ls -l                       # List with IDs
```

### 阅读笔记
```bash
joplin cat <note-id>               # Display note content
joplin cat "Note Title"            # Also works with title
joplin note <note-id>              # Open note in editor
```

### 创建笔记
```bash
joplin mknote "Note Title"         # Create note in default notebook
joplin mknote "Note Title" --notebook "Notebook Name"
joplin mkbook "New Notebook"       # Create new notebook
```

**提示：** 在执行任何操作前，请务必询问用户要使用哪个笔记本。可以使用以下命令：
- `joplin use` — 显示当前使用的笔记本
- `joplin use "笔记本名称"` — 切换到指定笔记本
- `joplin ls` — 查看所有笔记本

### 编辑笔记
```bash
joplin edit --note <note-id>       # Edit note in editor
joplin set <note-id> title "New title"  # Change note title
```

### 删除笔记
```bash
joplin rmnote <note-id>            # Delete note
joplin rmbook "Notebook Name"      # Delete notebook
```

### 在笔记本之间移动笔记
```bash
joplin mv "Note Title" "Target Notebook"
```

### 待办事项
```bash
joplin todos                       # List all todos
joplin todo <note-id>              # Toggle todo status
joplin done <note-id>              # Mark as done
joplin undone <note-id>            # Mark as not done
```

### 同步
```bash
joplin sync                        # Sync with WebDAV server
```

### 导出
```bash
joplin export <note-id> --format md
joplin export <note-id> --format html
joplin export <note-id> --format pdf
```

### 导入
```bash
joplin import /path/to/note.md --notebook "Notebook Name"
```

### 搜索

**注意：`joplin search` 仅在图形界面模式下可用。** 可以使用 `joplin ls` 并通过管道（`|`）与 `grep` 命令结合使用进行搜索。

## 所有 Joplin 命令列表
```
attach, batch, cat, config, cp, done, e2ee, edit, export, geoloc, help, 
import, ls, mkbook, mknote, mktodo, mv, ren, restore, rmbook, rmnote, 
server, set, share, status, sync, tag, todo, undone, use, version
```

### 引用笔记和笔记本

笔记或笔记本可以通过以下方式引用：
- **标题**：`“笔记标题”`
- **ID**：`fe889`（通过 `joplin ls -l` 获取）
- **快捷键**：
  - `$n` — 当前选中的笔记
  - `$b` — 当前选中的笔记本
  - `$c` — 当前选中的项目

## 交互式 shell 模式

Joplin 可以以交互式的方式运行（类似于 shell）。只需输入 `joplin` 即可开始使用：

```bash
joplin                          # Start interactive mode
```

### Shell 命令（前缀为 `:`）

| 命令 | 描述 |
|---------|-------------|
| `:sync` | 与 WebDAV 服务器同步 |
| `:quit` 或 `:q` | 退出 Joplin |
| `:help` | 显示帮助信息 |
| `:open <笔记ID>` | 打开指定笔记 |

### Shell 模式快捷键
- `e` — 编辑当前笔记
- `i` — 插入新笔记
- `空格` — 选择项目
- `Enter` — 打开笔记

### 示例工作流程
```bash
# Create a notebook
joplin mkbook "My notebook"

# Switch to it
joplin use "My notebook"

# Create a note
joplin mknote "My note"

# View notes with IDs
joplin ls -l

# Edit a note's title
joplin set <note-id> title "New title"
```

## Kanban 笔记（YesYouKan 插件）

某些笔记本使用了 YesYouKan kanban 插件来创建可视化的看板。这些笔记具有特定的格式，在编辑时必须保持该格式：

### Kanban 格式

```markdown
# Notebook Name

# Backlog

## Task 1

Description here

## Task 2



# In progress

## Another Task

Details



# Done

## Completed Task

Result

```kanban-settings
# 请勿删除此部分
```
```

### ⚠️ Kanban 格式规则

1. **务必在笔记末尾添加 `kanban-settings` 块，并确保格式正确**：
   ```
   ```kanban-settings
   # 请勿删除此部分
   ```
   ```

2. **使用 `##` 作为任务标题**（而不是 `#`）

3. **列标题应保持为 `# 待办事项`、`# 进行中`、`# 完成`**

4. **任务之间请保留空行**——这些空行会在看板视图中显示

5. **编辑 Kanban 笔记后，务必运行 `joplin sync` 以上传更改**

6. **使用 `joplin cat <笔记ID>` 验证格式是否正确**

### 在不同列之间移动任务

移动任务时，只需将包含任务信息的 `##` 标签从一列移动到另一列即可。