---
name: osori
description: "Osori — 一个用于管理本地项目的项目注册系统及上下文加载工具。支持查找、切换项目、列出项目、添加/删除项目以及检查项目状态等功能。相关操作包括：开始在某个项目上工作、查找特定项目、列出所有项目、查看项目状态以及切换当前项目。"
---

# Osori (오소리)

这是一个用于AI代理的本地项目注册表和上下文加载工具。

## 先决条件

- **macOS**: 需要`mdfind`（内置在Spotlight中）、`python3`、`git`以及`gh`命令行工具。
- **Linux**: 由于`mdfind`不可用，系统会自动使用`find`作为替代工具。同样需要`python3`、`git`以及`gh`命令行工具。

## 依赖项

- **python3**：必需。用于处理JSON数据。
- **git**：用于检测项目及其状态。

## 注册表

注册表的路径为：`${OSORI_REGISTRY:-$HOME/.openclaw/osori.json}`

可以通过设置`OSORI_REGISTRY`环境变量来更改注册表的路径。

## 查找项目（当项目路径未知时）

当项目路径未知时，系统会按以下顺序进行查找：

1. **在注册表中查找**：在`osori.json`文件中模糊匹配项目名称。
2. **使用`mdfind`（仅限macOS）**：执行命令 `mdfind "kMDItemFSName == '<name>'" | head -5`。
3. **使用`find`命令**：如果`OSORI_SEARCH_PATHS`环境变量未设置，系统会提示用户输入搜索路径，然后使用 `find <search_paths> -maxdepth 4 -type d -name '<name>' 2>/dev/null` 命令进行搜索。
4. **询问用户**：如果以上方法都失败，系统会直接询问用户项目路径。
5. **将找到的项目添加到注册表中**。

## 命令

### 列出
显示所有已注册的项目。支持使用`--tag`和`--lang`参数进行过滤。
```
Read osori.json and display as a table.
```

### 切换操作
1. 在注册表中搜索项目（通过名称进行模糊匹配）。
2. 如果未找到项目，则执行上述的查找流程。
3. 加载项目的上下文信息：
   - `git status --short`
   - `git branch --show-current`
   - `git log --oneline -5`
   - `gh issue list -R <repo> --limit 5`（当指定了仓库时）
4. 显示项目的简要信息。

### 添加项目
```bash
bash skills/osori/scripts/add-project.sh <path> [--tag <tag>] [--name <name>]
```
系统会自动检测项目的远程仓库地址、使用的语言以及项目描述等信息。

### 扫描目录
```bash
bash skills/osori/scripts/scan-projects.sh <root-dir> [--depth 3]
```
批量扫描目录中的Git仓库，并将它们添加到注册表中。

### 删除项目
根据项目名称从`osori.json`文件中删除相应的记录。

### 查看项目状态
可以运行`git status`和`gh issue list`命令来查看单个项目或所有项目的状态。

## 数据结构（schema）

```json
{
  "name": "string",
  "path": "/absolute/path",
  "repo": "owner/repo",
  "lang": "swift|typescript|python|rust|go|ruby|unknown",
  "tags": ["personal", "ios"],
  "description": "Short description",
  "addedAt": "YYYY-MM-DD"
}
```

## 自动触发规则

- 输入“work on X”/“开始处理X项目” → 切换到对应的项目。
- 输入“find project X”/“查找X项目”/“提供X项目的路径” → 在注册表中搜索或发现该项目。
- 输入“list projects”/“显示项目列表” → 显示所有项目。
- 输入“add project”/“添加项目” → 添加新项目。
- 输入“project status”/“查看项目状态” → 查看所有项目的状态。