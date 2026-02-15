---
name: obsidian-official-cli
description: 使用官方的 Obsidian CLI（v1.12 及以上版本）来操作 Obsidian 文档库。您可以通过终端打开、搜索、创建、移动和管理笔记。无论您是需要进行笔记管理、文件操作、内容搜索、任务管理、属性设置、插件管理、主题调整，还是执行任何与 Obsidian 相关的命令行操作，都可以使用该工具。
---

# Obsidian CLI

Obsidian 的官方命令行界面。在 Obsidian 中可以执行的任何操作都可以通过命令行完成——包括用于调试的开发命令、截图以及插件重新加载等。

## 先决条件

- 需要 **Obsidian 1.12+** 及 **Catalyst 许可证**  
- 在 **设置 → 通用 → 命令行界面** 中启用该功能  
- 按照提示注册 `obsidian` 命令  
- 重新启动终端或执行 `source ~/.zprofile`（macOS）  
- **注意：** 必须确保 Obsidian 正在运行，CLI 才能正常使用  

测试设置：`obsidian version`

## 核心模式

### 命令结构
```bash
# Single commands
obsidian <command> [parameters] [flags]

# TUI mode (interactive)
obsidian  # Enter TUI with autocomplete and history

# Vault targeting
obsidian vault=Notes <command>
obsidian vault="My Vault" <command>
```

### 参数类型
- **参数：** `name=value`（用空格分隔参数值）  
- **标志（Flags）：** 布尔值开关（仅用于启用相应功能）  
- **多行输入：** 使用 ` ` 表示换行，`\t` 表示制表符  
- **复制输出：** 添加 `--copy` 以将输出复制到剪贴板  

## 文件操作

### 基本文件管理
```bash
# Info and listing
obsidian file                          # Active file info
obsidian file file=Recipe              # Specific file info
obsidian files                         # List all files
obsidian files folder=Projects/        # Filter by folder
obsidian folders                       # List folders

# Open and read
obsidian open file=Recipe              # Open file
obsidian open path="Inbox/Note.md" newtab
obsidian read                          # Read active file
obsidian read file=Recipe --copy       # Read and copy to clipboard

# Create new notes
obsidian create name="New Note"
obsidian create name="Note" content="# Title Body"
obsidian create path="Inbox/Idea.md" template=Daily
obsidian create name="Note" silent overwrite

# Modify content
obsidian append file=Note content="New line"
obsidian append file=Note content="Same line" inline
obsidian prepend file=Note content="After frontmatter"

# Move and delete
obsidian move file=Note to=Archive/
obsidian move path="Inbox/Old.md" to="Projects/New.md"
obsidian delete file=Note              # To trash
obsidian delete file=Note permanent
```

### 文件定位
- `file=<name>` — 根据名称查找文件  
- `path=<path>` — 从 vault 根目录开始查找指定路径的文件  

## 搜索与发现

### 文本搜索
```bash
obsidian search query="meeting notes"
obsidian search query="TODO" matches    # Show context
obsidian search query="project" path=Projects/
obsidian search query="urgent" limit=10 case
obsidian search query="API" format=json
obsidian search:open query="search term"  # Open in Obsidian
```

### 标签与属性
```bash
# Tags
obsidian tags                          # Active file tags
obsidian tags all                      # All vault tags
obsidian tags all counts sort=count    # By frequency
obsidian tag name=project              # Tag info

# Properties (frontmatter)
obsidian properties file=Note
obsidian property:read name=status file=Note
obsidian property:set name=status value=done file=Note
obsidian property:set name=tags value="a,b,c" type=list file=Note
obsidian property:remove name=draft file=Note
```

### 链接与结构
```bash
# Backlinks and outgoing links
obsidian backlinks file=Note           # What links to this
obsidian links file=Note               # Outgoing links

# Vault analysis
obsidian orphans                       # No incoming links
obsidian deadends                      # No outgoing links
obsidian unresolved                    # Broken links
obsidian unresolved verbose counts
```

## 日记与任务管理

### 日记
```bash
obsidian daily                         # Open today's note
obsidian daily paneType=split          # Open in split
obsidian daily:read                    # Print contents
obsidian daily:append content="- [ ] New task"
obsidian daily:prepend content="## Morning"
```

### 任务管理
```bash
# List tasks
obsidian tasks                         # Active file
obsidian tasks all                     # All vault tasks
obsidian tasks all todo                # Incomplete only
obsidian tasks file=Recipe             # Specific file
obsidian tasks daily                   # Daily note tasks

# Update tasks
obsidian task ref="Recipe.md:8" toggle
obsidian task file=Recipe line=8 done
obsidian task file=Recipe line=8 todo
obsidian task file=Note line=5 status="-"  # Custom [-]
```

## 模板与书签

### 模板
```bash
obsidian templates                     # List all templates
obsidian template:read name=Daily
obsidian template:read name=Daily resolve title="My Note"
obsidian template:insert name=Daily    # Insert into active file
obsidian create name="Meeting Notes" template=Meeting
```

### 书签
```bash
obsidian bookmarks                     # List all
obsidian bookmark file="Important.md"
obsidian bookmark file=Note subpath="#Section"
obsidian bookmark folder="Projects/"
obsidian bookmark search="TODO"
obsidian bookmark url="https://..." title="Reference"
```

## 插件与主题管理

### 插件
```bash
# List and info
obsidian plugins                       # All installed
obsidian plugins:enabled               # Only enabled
obsidian plugin id=dataview            # Plugin info

# Manage plugins
obsidian plugin:enable id=dataview
obsidian plugin:disable id=dataview
obsidian plugin:install id=dataview enable
obsidian plugin:uninstall id=dataview
obsidian plugin:reload id=my-plugin    # Development
```

### 主题与 CSS
```bash
# Themes
obsidian themes                        # List installed
obsidian theme                         # Active theme
obsidian theme:set name=Minimal
obsidian theme:install name="Theme Name" enable

# CSS Snippets
obsidian snippets                      # List all
obsidian snippet:enable name=my-snippet
obsidian snippet:disable name=my-snippet
```

## 高级功能

### Obsidian 同步
```bash
obsidian sync:status                   # Status and usage
obsidian sync on/off                   # Resume/pause
obsidian sync:history file=Note
obsidian sync:restore file=Note version=2
obsidian sync:deleted                  # Deleted files
```

### 文件历史记录
```bash
obsidian history file=Note             # List versions
obsidian history:read file=Note version=1
obsidian history:restore file=Note version=2
obsidian diff file=Note from=2 to=1   # Compare versions
```

### 开发者工具
```bash
# Console and debugging
obsidian devtools                      # Toggle dev tools
obsidian dev:console                   # Show console
obsidian dev:errors                    # JS errors
obsidian eval code="app.vault.getFiles().length"

# Screenshots and DOM
obsidian dev:screenshot path=screenshot.png
obsidian dev:dom selector=".workspace-leaf"
obsidian dev:css selector=".mod-active" prop=background

# Mobile and debugging
obsidian dev:mobile on/off
obsidian dev:debug on/off
```

## 实用命令

### 工作区与导航
```bash
# Workspace management
obsidian workspace                     # Current layout
obsidian workspace:save name="coding"
obsidian workspace:load name="coding"
obsidian tabs                          # Open tabs
obsidian tab:open file=Note

# Random and unique
obsidian random                        # Open random note
obsidian random folder=Inbox newtab
obsidian unique                        # Create unique name
obsidian wordcount file=Note           # Word count
```

### 命令面板
```bash
obsidian commands                      # List all command IDs
obsidian commands filter=editor        # Filter commands
obsidian command id=editor:toggle-bold
obsidian hotkeys                       # List hotkeys
```

## TUI 模式

交互式终端用户界面，具备增强功能：  
```bash
obsidian                               # Enter TUI mode
```

**TUI 快捷键：**  
- **导航：** ←/→（Ctrl+B/F），Home/End（Ctrl+A/E）  
- **编辑：** Ctrl+U（删除开始部分），Ctrl+K（删除结束部分）  
- **自动完成：** Tab/↓（回车），Shift+Tab/Esc（退出）  
- **历史记录：** ↑/↓（Ctrl+P/N），Ctrl+R（反向搜索）  
- **其他：** Enter（执行），Ctrl+L（清除），Ctrl+C/D（退出）  

## 故障排除

### 设置问题  
- 使用最新版本的安装程序（1.11.7+）及早期访问版本（1.12.x）  
- 注册 CLI 后重新启动终端  
- 使用 CLI 之前确保 Obsidian 正在运行  

### 平台特定设置  

**macOS：** 将路径添加到 `~/.zprofile` 文件中  
```bash
# For other shells, add manually:
export PATH="$PATH:/Applications/Obsidian.app/Contents/MacOS"
```

**Linux：** 在 `/usr/local/bin/obsidian` 创建符号链接  
```bash
# Manual creation if needed:
sudo ln -s /path/to/obsidian /usr/local/bin/obsidian
```

**Windows：** 需要使用 `Obsidian.com` 提供的终端重定向器（通过 Catalyst Discord 连接）