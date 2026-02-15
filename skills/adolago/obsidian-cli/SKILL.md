---
name: obsidian-cli
description: Obsidian 官方 CLI（v1.12 及以上版本）的实用技巧：实现全面的文件管理自动化功能，包括文件操作、每日笔记记录、搜索、任务管理、标签设置、属性编辑、链接添加、书签创建、模板应用、主题切换、插件管理、数据同步、内容发布、工作区设置以及开发者工具的使用。
version: 2.0.0
author: adolago
tags:
  - obsidian
  - cli
  - notes
  - automation
  - vault
triggers:
  - obsidian
  - vault
  - daily note
  - obsidian cli
---
# Obsidian CLI（官方版，v1.12及以上）

官方的Obsidian CLI通过IPC（Inter-Process Communication）连接到正在运行的Obsidian实例。  
需要使用Obsidian 1.12及以上版本，并在“设置”>“常规”中启用CLI功能。  

## 先决条件  

- 安装并运行了Obsidian 1.12及以上版本。  
- 在“设置”>“常规”中启用了CLI功能。  
- `obsidian`二进制文件必须位于系统的`PATH`环境变量中。  

**重要提示**：必须确保Obsidian正在运行，CLI命令才能正常使用。CLI通过IPC与正在运行的实例进行通信。  

### 平台说明  

- **macOS/Windows**：Obsidian安装程序通常会自动将CLI二进制文件添加到`PATH`中。  
- **Linux**：可能需要使用一个包装脚本来避免Electron相关配置问题（这些配置可能会影响CLI参数的解析。请确保包装脚本位于`PATH`中，并且位于系统`obsidian`二进制文件之前。如果以服务形式运行Obsidian，请确保`PrivateTmp`设置为`false`，以便IPC能够正常工作。  

## 完整命令参考  

### 基础命令  

```bash
obsidian version                            # Show Obsidian version
obsidian help                               # List all available commands
obsidian vault                              # Show vault info (name, path, files, size)
obsidian vault info=name                    # Just vault name
obsidian vault info=path                    # Just vault path
obsidian reload                             # Reload the vault
obsidian restart                            # Restart the app
```  

### 日常操作  

```bash
obsidian daily                              # Open today's daily note
obsidian daily silent                       # Open without focusing
obsidian daily:read                         # Read daily note contents
obsidian daily:append content="- [ ] Task"  # Append to daily note
obsidian daily:prepend content="# Header"   # Prepend to daily note
obsidian daily paneType=tab                 # Open in new tab (tab|split|window)
```  

### 文件操作  

```bash
obsidian read file=Recipe                   # Read by name (wikilink resolution)
obsidian read path="Work/notes.md"          # Read by exact path
obsidian file file=Recipe                   # Show file info (path, size, dates)
obsidian create name=Note content="Hello"   # Create a new note
obsidian create name=Note template=Travel   # Create from template
obsidian create path="Work/note.md" content="text"  # Create at exact path
obsidian create name=Note overwrite         # Overwrite if exists
obsidian create name=Note silent newtab     # Create silently in new tab
obsidian open file=Recipe                   # Open in Obsidian
obsidian open file=Recipe newtab            # Open in new tab
obsidian delete file=Old                    # Delete (to trash)
obsidian delete file=Old permanent          # Delete permanently
obsidian move file=Old to="Archive/Old.md"  # Move/rename (include .md in target)
obsidian append file=Log content="Entry"    # Append to file
obsidian append file=Log content="text" inline  # Append inline (no newline)
obsidian prepend file=Log content="Header"  # Prepend to file
obsidian unique name="Meeting" content="notes"  # Create note with unique timestamp
obsidian wordcount file=Note                # Word and character count
obsidian wordcount file=Note words          # Words only
obsidian wordcount file=Note characters     # Characters only
obsidian random                             # Open a random note
obsidian random:read                        # Read a random note
obsidian random folder="Work"               # Random note from folder
obsidian recents                            # List recently opened files
obsidian recents total                      # Count of recent files
```  

### 搜索  

```bash
obsidian search query="meeting notes"               # Search vault
obsidian search query="TODO" matches                 # Show match context
obsidian search query="project" path="Work" limit=10 # Scoped search
obsidian search query="test" format=json             # JSON output
obsidian search query="Bug" case                     # Case-sensitive search
obsidian search query="error" total                  # Count matches only
obsidian search:open query="TODO"                    # Open search view in Obsidian
```  

### 任务管理  

```bash
obsidian tasks daily                        # Tasks from daily note
obsidian tasks daily todo                   # Incomplete daily tasks
obsidian tasks daily done                   # Completed daily tasks
obsidian tasks all todo                     # All incomplete tasks in vault
obsidian tasks file=Recipe done             # Completed tasks in file
obsidian tasks verbose                      # Tasks with file paths + line numbers
obsidian tasks total                        # Count of tasks
obsidian tasks status="/"                   # Tasks with custom status character
obsidian task daily line=3 toggle           # Toggle task completion
obsidian task daily line=3 done             # Mark task done
obsidian task daily line=3 todo             # Mark task incomplete
obsidian task ref="Work/todo.md:5" toggle   # Toggle by file:line reference
obsidian task daily line=3 status="/"       # Set custom status
```  

### 标签与属性  

```bash
# Tags
obsidian tags all counts                    # All tags with counts
obsidian tags all counts sort=count         # Sorted by frequency
obsidian tags file=Note                     # Tags in specific file
obsidian tags total                         # Total tag count
obsidian tag name=project verbose           # Tag details with file list
obsidian tag name=project total             # Count of files with tag

# Properties (frontmatter)
obsidian properties all counts              # All properties with counts
obsidian properties all counts sort=count   # Sorted by frequency
obsidian properties file=Note               # Properties of specific file
obsidian properties name=status             # Files with specific property
obsidian properties format=yaml             # YAML output
obsidian properties format=tsv              # TSV output
obsidian property:read name=status file=Note       # Read a property value
obsidian property:set name=status value=done file=Note  # Set a property
obsidian property:set name=due value="2026-03-01" type=date file=Note  # Set with type
obsidian property:remove name=status file=Note     # Remove a property

# Aliases
obsidian aliases                            # List all aliases in vault
obsidian aliases all                        # Include files without aliases
obsidian aliases file=Note                  # Aliases for specific file
obsidian aliases total                      # Count of aliases
obsidian aliases verbose                    # With file paths
```  

### 链接与文件结构  

```bash
obsidian backlinks file=Note                # Files linking to Note
obsidian backlinks file=Note counts         # With link counts
obsidian backlinks file=Note total          # Count of backlinks
obsidian links file=Note                    # Outgoing links from Note
obsidian links file=Note total              # Count of outgoing links
obsidian orphans                            # Files with no incoming links
obsidian orphans total                      # Count of orphans
obsidian orphans all                        # Include non-markdown files
obsidian deadends                           # Files with no outgoing links
obsidian deadends total                     # Count of deadends
obsidian unresolved                         # Broken/unresolved links
obsidian unresolved total                   # Count of unresolved
obsidian unresolved counts                  # With reference counts
obsidian unresolved verbose                 # With source file details
obsidian outline file=Note                  # Headings tree
obsidian outline file=Note format=md        # Headings as markdown
obsidian outline file=Note total            # Count of headings
```  

### 仓库信息  

```bash
obsidian files total                        # File count
obsidian files folder="Work" ext=md         # Filter by folder and extension
obsidian folders                            # List all folders
obsidian folders total                      # Folder count
obsidian folders folder="Work"              # Subfolders of path
obsidian folder path="Work" info=size       # Folder size in bytes
obsidian folder path="Work" info=files      # File count in folder
obsidian folder path="Work" info=folders    # Subfolder count
```  

### 书签  

```bash
obsidian bookmarks                          # List all bookmarks
obsidian bookmarks total                    # Count of bookmarks
obsidian bookmarks verbose                  # With details
obsidian bookmark file="Work/note.md"       # Bookmark a file
obsidian bookmark file="note.md" subpath="#heading"  # Bookmark a heading
obsidian bookmark folder="Work"             # Bookmark a folder
obsidian bookmark search="TODO"             # Bookmark a search query
obsidian bookmark url="https://example.com" title="Example"  # Bookmark a URL
```  

### 数据库视图（Bases）  

```bash
obsidian bases                              # List all base files
obsidian base:views                         # List views in current base
obsidian base:query file=MyBase             # Query base, default format
obsidian base:query file=MyBase format=json # JSON output
obsidian base:query file=MyBase format=csv  # CSV output
obsidian base:query file=MyBase format=tsv  # TSV output
obsidian base:query file=MyBase format=md   # Markdown table
obsidian base:query file=MyBase format=paths  # Just file paths
obsidian base:query file=MyBase view="View Name"  # Query specific view
obsidian base:create name="New Item"        # Create item in current base view
obsidian base:create content="text" silent  # Create silently
```  

### 模板  

```bash
obsidian templates                          # List available templates
obsidian templates total                    # Count of templates
obsidian template:read name=Daily           # Read template content
obsidian template:read name=Daily resolve   # Read with variables resolved
obsidian template:read name=Daily resolve title="My Note"  # Resolve with title
obsidian template:insert name=Daily         # Insert template into active file
```  

### 命令与快捷键  

```bash
obsidian commands                           # List all command IDs
obsidian commands filter="editor"           # Filter by prefix
obsidian command id=app:open-settings       # Execute a command
obsidian hotkeys                            # List assigned hotkeys
obsidian hotkeys all                        # Include unassigned
obsidian hotkeys total                      # Count of hotkeys
obsidian hotkeys verbose                    # With command details
obsidian hotkey id=app:open-settings        # Hotkey for specific command
obsidian hotkey id=app:open-settings verbose # With full details
```  

### 标签页与工作区  

```bash
# Tabs
obsidian tabs                               # List open tabs
obsidian tabs ids                           # With tab IDs
obsidian tab:open                           # Open new empty tab
obsidian tab:open file="Work/note.md"       # Open file in new tab
obsidian tab:open group=2                   # Open in specific tab group

# Workspaces
obsidian workspaces                         # List saved workspaces
obsidian workspaces total                   # Count of workspaces
obsidian workspace                          # Show current workspace tree
obsidian workspace ids                      # With element IDs
obsidian workspace:save name="coding"       # Save current layout
obsidian workspace:load name="coding"       # Load saved workspace
obsidian workspace:delete name="old"        # Delete saved workspace
```  

### 历史记录与文件差异（文件恢复）  

```bash
obsidian history file=Note                  # List version history for file
obsidian history:list                       # List all files with history
obsidian history:read file=Note             # Read latest history version
obsidian history:read file=Note version=3   # Read specific version
obsidian history:restore file=Note version=3  # Restore a version
obsidian history:open file=Note             # Open file recovery UI
obsidian diff file=Note                     # List/diff local versions
obsidian diff file=Note from=1 to=3         # Diff between versions
obsidian diff file=Note filter=local        # Local versions only
obsidian diff file=Note filter=sync         # Sync versions only
```  

### 同步（Obsidian同步）  

```bash
obsidian sync:status                        # Show sync status
obsidian sync on                            # Resume sync
obsidian sync off                           # Pause sync
obsidian sync:history file=Note             # Sync version history
obsidian sync:history file=Note total       # Count of sync versions
obsidian sync:read file=Note version=2      # Read a sync version
obsidian sync:restore file=Note version=2   # Restore a sync version
obsidian sync:deleted                       # List files deleted in sync
obsidian sync:deleted total                 # Count of deleted files
obsidian sync:open file=Note               # Open sync history UI
```  

### 发布（Obsidian发布功能）  

```bash
obsidian publish:site                       # Show publish site info
obsidian publish:status                     # List all publish changes
obsidian publish:status new                 # New files to publish
obsidian publish:status changed             # Changed files
obsidian publish:status deleted             # Deleted files
obsidian publish:status total               # Count of changes
obsidian publish:list                       # List published files
obsidian publish:list total                 # Count of published files
obsidian publish:add file=Note              # Publish a file
obsidian publish:add changed                # Publish all changed files
obsidian publish:remove file=Note           # Unpublish a file
obsidian publish:open file=Note             # Open on published site
```  

### 主题与CSS样式  

```bash
# Themes
obsidian theme                              # Show active theme
obsidian theme name="Minimal"               # Get theme info
obsidian themes                             # List installed themes
obsidian themes versions                    # With version numbers
obsidian theme:set name="Minimal"           # Set active theme
obsidian theme:install name="Minimal"       # Install community theme
obsidian theme:install name="Minimal" enable  # Install and activate
obsidian theme:uninstall name="Minimal"     # Uninstall theme

# CSS Snippets
obsidian snippets                           # List installed snippets
obsidian snippets:enabled                   # List enabled snippets
obsidian snippet:enable name="custom"       # Enable a snippet
obsidian snippet:disable name="custom"      # Disable a snippet
```  

### 插件  

```bash
obsidian plugins                            # List all installed
obsidian plugins filter=core                # Core plugins only
obsidian plugins filter=community           # Community plugins only
obsidian plugins versions                   # With version numbers
obsidian plugins:enabled                    # List enabled plugins
obsidian plugins:enabled filter=community versions  # Enabled community with versions
obsidian plugins:restrict                   # Check restricted mode status
obsidian plugins:restrict on                # Enable restricted mode
obsidian plugins:restrict off               # Disable restricted mode
obsidian plugin id=dataview                 # Get plugin info
obsidian plugin:enable id=dataview          # Enable plugin
obsidian plugin:disable id=dataview         # Disable plugin
obsidian plugin:install id=dataview         # Install community plugin
obsidian plugin:install id=dataview enable  # Install and enable
obsidian plugin:uninstall id=dataview       # Uninstall community plugin
obsidian plugin:reload id=my-plugin         # Reload plugin (dev)
```  

### Web浏览器查看器  

```bash
obsidian web url="https://example.com"      # Open URL in web viewer
obsidian web url="https://example.com" newtab  # Open in new tab
```  

### 开发者工具  

```bash
# JavaScript evaluation
obsidian eval code="app.vault.getFiles().length"  # Run JS in Obsidian context

# Screenshots
obsidian dev:screenshot                     # Screenshot to default path
obsidian dev:screenshot path=screenshot.png # Screenshot to file

# DevTools
obsidian devtools                           # Toggle Electron devtools

# Console & Errors (requires dev:debug on)
obsidian dev:debug on                       # Attach CDP debugger (required for console)
obsidian dev:debug off                      # Detach debugger
obsidian dev:console                        # Show captured console messages
obsidian dev:console limit=10               # Last 10 messages
obsidian dev:console level=error            # Filter by level (log|warn|error|info|debug)
obsidian dev:console clear                  # Clear captured messages
obsidian dev:errors                         # Show captured JS errors
obsidian dev:errors clear                   # Clear errors

# DOM inspection
obsidian dev:dom selector=".workspace"      # Query DOM elements
obsidian dev:dom selector=".nav-file" total # Count matching elements
obsidian dev:dom selector=".nav-file" text  # Get text content
obsidian dev:dom selector=".nav-file" inner # Get innerHTML
obsidian dev:dom selector=".nav-file" all   # All matches
obsidian dev:dom selector="h1" attr=class   # Get attribute
obsidian dev:dom selector="h1" css=color    # Get CSS property

# CSS inspection
obsidian dev:css selector=".workspace"      # Inspect CSS with source locations
obsidian dev:css selector=".workspace" prop=background  # Specific property

# Chrome DevTools Protocol
obsidian dev:cdp method="Page.getLayoutMetrics"  # Raw CDP command
obsidian dev:cdp method="Runtime.evaluate" params='{"expression":"1+1"}'

# Mobile emulation
obsidian dev:mobile on                      # Enable mobile emulation
obsidian dev:mobile off                     # Disable mobile emulation
```  

### 多个仓库管理  

```bash
obsidian vaults                             # List known vaults
obsidian vaults verbose                     # With paths
obsidian vaults total                       # Count of vaults
obsidian vault=Notes daily                  # Target specific vault
obsidian vault=Notes search query="test"    # Search in specific vault
```  

## 参数语法  

- 参数格式：`param=value`（使用空格分隔）：例如 `content="Hello world"`  
- 命令标志：直接使用单词形式，例如 `obsidian tasks daily todo verbose`  
- 多行输入：使用`\n`表示换行，`\t`表示制表符  
- `file=<名称>`：会解析为Wiki链接（仅需要文件名，无需路径或扩展名）  
- `path=<路径>`：需要提供从仓库根目录开始的完整路径  
- `vault=<名称>`：必须作为第一个参数来指定目标仓库  

## 仓库选择  

- 如果当前工作目录（CWD）位于某个仓库内，将使用该仓库；  
- 否则，将使用默认的活跃仓库。  
- 可以通过`vault=<名称>`作为第一个参数来指定目标仓库。  

## 故障排除  

- **“无法连接”**：请确认Obsidian正在运行，并且在“设置”>“常规”中启用了CLI功能。  
- **“命令未找到”**：请检查`obsidian`二进制文件是否在`PATH`中。  
- **Linux系统下的IPC问题**：如果以无界面模式或服务形式运行Obsidian，请确保IPC套接字可访问（关闭`PrivateTmp`选项），并确保使用正确的用户权限。  
- **Electron配置冲突（Linux系统）**：在调用CLI时，使用不包含`electron-flags.conf`文件的包装脚本。  

## 其他说明  

- CLI通过IPC与正在运行的Obsidian实例建立连接。  
- 对于非交互式使用（如脚本或定时任务），请确保Obsidian已经启动。  
- `move`命令需要提供包含`.md`扩展名的完整目标文件路径。  
- 在包含大量文件（超过19,000个文件）的仓库中，`folders`命令可能会执行较慢。  
- 使用`dev:console`命令时，需要先启用`dev:debug`模式。