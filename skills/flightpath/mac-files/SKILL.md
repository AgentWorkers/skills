---
name: mac-files
description: 通过 SSH 在 Guy 的 Mac（Mac Mini 或 MacBook）上搜索、阅读、创建、编辑和管理文件。当用户需要查找文件、阅读文档、创建或编辑文件、整理文件夹或管理文件时，可以使用此功能。其中包括通过 mdfind 进行的 Spotlight 搜索。
---
# 通过 SSH 操作 Mac 上的文件

您可以通过 SSH 管理远程 Mac 上的文件。为确保安全，访问权限仅限于允许的目录。

## 目标主机

- `mini`（默认）—— guym@doclib
- `macbook`—— guymackenzie@guy-mac-m1

## 允许的目录

- `~/Documents`
- `~/Desktop`
- `~/Downloads`
- `~/Projects`

所有路径必须位于这些目录内。超出这些范围的路径将被拒绝。

## 脚本

`scripts/mac-files.sh <操作> <目标主机> [参数...]`

### 操作类型

**查找文件：**
- `search <查询> [文件夹]` — 在允许的目录中或特定文件夹内使用 macOS 的 Spotlight 功能（mdfind）进行搜索
- `grep <模式> <文件夹>` — 在文件内容中搜索指定文本

**读取文件：**
- `ls <路径>` — 列出目录内容
- `tree <路径> [深度]` — 以树形结构显示目录结构（默认深度为 2 层）
- `read <路径>` — 读取整个文件的内容
- `head <路径> [行数>` — 显示文件的前 N 行（默认 20 行）
- `tail <路径> [行数>` — 显示文件的后 N 行（默认 20 行）
- `info <路径>` — 显示文件的大小、类型和修改日期
- `du <路径>` — 显示目录内容的磁盘使用情况

**创建和编辑文件：**
- `create <路径> <内容>` — 创建新文件（会自动创建父目录）
- `write <路径> <内容>` — 覆盖现有文件
- `append <路径> <文本>` — 在文件末尾追加文本
- `mkdir <路径>` — 创建新目录

**移动和整理文件：**
- `mv <源路径> <目标路径>` — 移动或重命名文件（源路径和目标路径都必须位于允许的目录内）
- `cp <源路径> <目标路径>` — 复制文件（源路径和目标路径都必须位于允许的目录内）
- `trash <路径>` — 将文件移至“废纸篓”（比直接删除更安全）
- `open <路径>` — 用默认的 macOS 应用程序打开文件

### 示例

```bash
# Spotlight search for tax docs
bash scripts/mac-files.sh search mini "tax 2025"

# List Documents folder
bash scripts/mac-files.sh ls mini ~/Documents

# Read a file
bash scripts/mac-files.sh read mini ~/Documents/notes.txt

# Create a file
bash scripts/mac-files.sh create mini ~/Projects/ideas.md "# Ideas"

# Search file contents
bash scripts/mac-files.sh grep mini "password" ~/Documents
```

## 注意事项：

- 始终使用“trash”功能而不是直接删除文件——请先确认用户操作。
- `search`命令使用 macOS 的 Spotlight 功能（mdfind），搜索速度非常快，可以同时搜索文件名和文件内容。
- 使用`open`命令时，需要先解锁 Mac 才能打开相应的应用程序窗口。
- 路径中可以使用 `~` 符号，它表示目标用户的 home 目录。