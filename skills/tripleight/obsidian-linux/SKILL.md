---
name: obsidian
description: 使用 Obsidian 文档管理系统（基于纯 Markdown 的笔记格式），并通过 `notesmd-cli` 工具实现自动化操作。
homepage: https://help.obsidian.md
metadata: {"clawdbot":{"emoji":"💎","requires":{"bins":["notesmd-cli"]},"install":[{"id":"brew","kind":"brew","formula":"yakitrak/yakitrak/notesmd-cli","bins":["notesmd-cli"],"label":"Install notesmd-cli (brew, macOS)"},{"id":"aur","kind":"aur","package":"notesmd-cli-bin","bins":["notesmd-cli"],"label":"Install notesmd-cli (AUR, Arch/Manjaro Linux)"}]}}
---
# Obsidian

Obsidian 的“vault”实际上只是一个普通的文件夹，其中存储着 Markdown 文件。

**典型的 vault 结构：**
- **笔记（Notes）**：`.md` 文件（纯文本 Markdown 格式；可以使用任何文本编辑器进行编辑）
- **配置（Config）**：`.obsidian/` 文件夹（包含工作区设置和插件配置；请勿通过脚本直接修改）
- **画布（Canvases）**：`.canvas` 文件（JSON 格式）
- **附件（Attachments）**：您在 Obsidian 设置中指定的任何文件夹（例如图片、PDF 等）

## 设置（Setup）

### 查找当前使用的 vault

Obsidian 桌面应用程序会从配置文件中记录所有使用的 vault 信息：
- **macOS**：`~/Library/Application Support/obsidian/obsidian.json`
- **Linux**：`~/.config/obsidian/obsidian.json`

`notesmd-cli` 会从该配置文件中读取 vault 的信息；vault 的名称就是文件夹的名称（包括路径后缀）。

### 验证默认的 vault

在运行任何命令之前，请务必检查默认的 vault 设置：
```bash
notesmd-cli print-default --path-only 2>/dev/null && echo "OK" || echo "NOT_SET"
```

如果默认 vault 未设置，请进行相应的配置：
```bash
notesmd-cli set-default "VAULT_NAME"
```

**不要猜测 vault 的路径**——请直接查看配置文件或使用 `print-default` 命令来获取路径。

## notesmd-cli 快速参考

### 查看 vault 信息
```bash
notesmd-cli print-default              # show default vault name + path
notesmd-cli print-default --path-only  # path only
notesmd-cli list                       # list notes and folders in vault
notesmd-cli list "Folder"              # list inside a folder
```

### 搜索（Search）
```bash
notesmd-cli search "query"             # fuzzy search note names
notesmd-cli search-content "query"     # search inside notes (shows snippets + lines)
```

### 读取（Read）
```bash
notesmd-cli print "path/note"          # print note contents
notesmd-cli frontmatter "path/note"    # view or modify note frontmatter
```

### 创建和编辑（Create & Edit）
```bash
notesmd-cli create "Folder/Note" --content "..." --open    # create note
notesmd-cli create "Folder/Note" --content "..." --append  # append to existing note
notesmd-cli create "Folder/Note" --content "..." --overwrite  # overwrite note
```

**注意：** 使用 `create` 命令创建新笔记时，需要确保系统中安装了 Obsidian 的相关插件（Obsidian URI 处理器）。请避免使用包含隐藏点（`.`）的文件夹路径。

### 移动或删除文件（Move / Delete）
```bash
notesmd-cli move "old/path/note" "new/path/note"  # rename/move (updates [[wikilinks]])
notesmd-cli delete "path/note"
```

### 多个 vault 的使用

在命令中添加 `--vault "Name"` 参数，即可指定要操作的 vault：
```bash
notesmd-cli print "2025-01-10" --vault "Work"
notesmd-cli search "meeting" --vault "Personal"
```

## 每日笔记（Daily Notes）
```bash
notesmd-cli daily                      # open/create today's daily note
notesmd-cli daily --vault "Work"       # for a specific vault
```

### 获取当前日期（跨平台）
```bash
date +%Y-%m-%d                         # today
# Yesterday (GNU first, BSD fallback):
date -d yesterday +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d
# Last Friday:
date -d "last friday" +%Y-%m-%d 2>/dev/null || date -v-friday +%Y-%m-%d
# N days ago:
date -d "3 days ago" +%Y-%m-%d 2>/dev/null || date -v-3d +%Y-%m-%d
```

### 将内容追加到每日笔记中
```bash
# Journal entry
notesmd-cli create "$(date +%Y-%m-%d)" --content "- Did the thing" --append

# Task
notesmd-cli create "$(date +%Y-%m-%d)" --content "- [ ] Buy groceries" --append

# Timestamped log
notesmd-cli create "$(date +%Y-%m-%d)" --content "- $(date +%H:%M) Meeting notes here" --append

# With custom folder (e.g. Daily Notes plugin folder)
notesmd-cli create "Daily Notes/$(date +%Y-%m-%d)" --content "- Entry" --append
```

### 读取每日笔记的内容
```bash
notesmd-cli print "$(date +%Y-%m-%d)"  # today
notesmd-cli print "$(date -d yesterday +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)"  # yesterday
notesmd-cli print "2025-01-10"         # specific date
```

## 常用操作模式

- **创建包含特定内容的新笔记：**
  ```bash
notesmd-cli create "Projects/My Project" --content "# My Project\n\nNotes here." --open
```

- **查找并读取笔记：**
  ```bash
notesmd-cli search "meeting"
notesmd-cli print "path/from/search/result"
```

- **安全地重命名笔记同时保留链接：**
  ```bash
notesmd-cli move "old/note name" "new/folder/note name"
```

- **在笔记内容中搜索：**
  ```bash
notesmd-cli search-content "TODO"
notesmd-cli search-content "project alpha"
```

**在适当的情况下，建议直接编辑 Markdown 文件**——Obsidian 会自动识别这些更改。