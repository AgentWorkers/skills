---
name: osori
description: "Osori v1.6.1 — 支持 Telegram 斜杠命令的本地项目注册表与上下文加载器。具备版本控制功能、自动迁移机制、根目录过滤、根目录管理、项目状态检查（预览优先、风险控制）、安全移除项目、多条件匹配切换、GitHub 项目计数缓存、别名/收藏功能，以及完整的项目集成命令集。支持查找、切换、列出、添加/删除项目以及检查项目状态。主要功能包括：在特定目录下工作、查找特定项目、列出所有项目、查看项目状态以及切换项目。"
homepage: https://github.com/oozoofrog/osori
metadata: { "openclaw": { "emoji": "🦦", "requires": { "bins": ["python3", "git", "gh"] }, "os": ["darwin", "linux"] } }
---
# Osori（오소리）

这是一个用于AI代理的本地项目注册表和上下文加载器。

## 先决条件

- **macOS**：需要`mdfind`（内置的Spotlight工具）、`python3`、`git`以及`gh` CLI。
- **Linux**：由于`mdfind`不可用，系统会自动使用`find`作为替代工具。同样需要`python3`、`git`以及`gh` CLI。
- **完整集成（可选）**：需要安装`entire` CLI（用于执行`/entire-*`命令）。

## 依赖项

- **python3**：必需。用于处理JSON数据。
- **git**：用于检测项目及检查项目状态。
- **entire**：可选。仅在执行`/entire-status`、`/entire-enable`、`/entire-rewind-list`命令时需要。

## Telegram机器人命令（v1.6.1版本更新）

Osori现在支持通过Telegram的斜杠命令来快速管理项目：

```
/list [root] — Show registered projects (optional root filter)
/status [root] — Check status of projects (optional root filter)
/find <name> [root|--root <root>] — Find a project by name (optional root scope)
/switch <name> [root|--root <root>] [--index <n>] — Switch to project and load context (multi-match selection)
/fingerprints [name] [--root <root>] — Show repo remote + last commit + open PR/issue counts
/doctor [--fix] [--dry-run] [--yes] [--json] — Registry health check (preview-first, risk-gated)
/list-roots — List roots, labels, paths, and project counts
/root-add <key> [label] — Add root (or update label)
/root-path-add <key> <path> — Add discovery path to root
/root-path-remove <key> <path> — Remove discovery path from root
/root-set-label <key> <label> — Update root label
/root-remove <key> [--reassign <target>] [--force] — Safely remove root
/alias-add <alias> <project> — Add alias for project
/alias-remove <alias> — Remove alias
/favorites — Show favorite projects
/favorite-add <project> — Mark project as favorite
/favorite-remove <project> — Unmark favorite
/entire-status <project> [root|--root <root>] — Show Entire status in a project
/entire-enable <project> [root|--root <root>] [--agent <name>] [--strategy <name>] — Enable Entire in a project
/entire-rewind-list <project> [root|--root <root>] — List rewind points in a project
/add <path> — Add project to registry
/remove <name> — Remove project from registry
/scan <path> [root] — Scan directory for git projects, optional root key
/help — Show command help
```

### 设置

将以下配置添加到您的OpenClaw代理的`TOOLS.md`文件或Telegram机器人配置文件中：

```bash
# In Telegram bot commands (BotFather)
list - Show all projects (or by root)
status - Check project statuses (or by root)
find - Find project by name
switch - Switch to project
fingerprints - Show repo/commit/PR/issue fingerprint
doctor - Health check (preview-first, risk-gated fix)
list-roots - Show roots and discovery paths
root-add - Add root
root-path-add - Add path to root
root-path-remove - Remove path from root
root-set-label - Rename root label
root-remove - Safely remove root (with reassign/force options)
alias-add - Add alias for a project
alias-remove - Remove alias
favorites - Show favorite projects
favorite-add - Mark favorite project
favorite-remove - Unmark favorite project
entire-status - Show Entire status for a project
entire-enable - Enable Entire for a project
entire-rewind-list - List rewind points for a project
add - Add project to registry
remove - Remove project
scan - Scan directory (optional root)
help - Show help
```

### 使用示例

```
/list work
/status personal
/find agent-avengers work
/switch Tesella --root personal
/switch Tesella --root personal --index 1
/fingerprints Tesella --root personal
/doctor --fix
/list-roots
/root-add work Work
/root-path-add work /path/to/workspace
/root-remove work --reassign default
/alias-add rh RunnersHeart
/favorite-add RunnersHeart
/favorites
/entire-status osori
/entire-enable osori --agent claude-code --strategy manual-commit
/add /Volumes/disk/MyProject
/scan /path/to/workspace work
```

## 注册表

注册表的路径为：`${OSORI_REGISTRY:-$HOME/.openclaw/osori.json}`

您可以通过设置`OSORI_REGISTRY`环境变量来更改这个路径。

### 版本控制与迁移（v1.6.1）

- 当前注册表格式：`osoriregistry`
- 当前版本：`2`
- 每次加载时，Osori会自动迁移旧版本的注册表数据：
  - 旧版本的数组格式（`[]`） → 新版本的规范化对象格式
  - 未包含`schema/version`字段的对象 → 也会被转换为规范化版本
- 规范化的注册表字段包括：
  - 最顶层的`roots[]`
  - 最顶层的`aliases{}`（别名对应项目名称）
  - 每个`projects[]`条目中包含`favorite: bool`字段
- 迁移过程中的安全措施：
  - 会创建备份文件：`osori.json.bak-<timestamp>`
  - 故障的JSON文件会被保存为：`osori.json.broken-<timestamp>`
  - 写入注册表时使用原子替换操作，并提供回滚机制

## 查找项目（当项目路径未知时）

当项目路径未知时，系统会按以下顺序进行查找：
1. **在注册表中查找**：在`osori.json`中模糊匹配项目名称。
2. **使用`mdfind`（仅限macOS）**：执行`mdfind "kMDItemFSName == '<name>'" | head -5`。
3. **使用`find`作为备用方法**：查找优先级如下：
   1) 从注册表中的`roots[]`中查找（如果指定了项目根目录，则优先查找该目录下的项目）
   2) 从`OSORI SEARCH_PATHS`中查找路径
   命令格式：`find <search_paths> -maxdepth 4 -type d -name '<name>' 2>/dev/null`
4. **询问用户**：如果以上方法都失败，则直接询问用户项目路径。
5. 提供将找到的项目添加到注册表的功能。

## 命令

### 列出所有注册的项目

可以列出所有注册的项目。在Telegram命令中支持指定项目根目录：

```bash
/list [root]
```

（示例：`/list work`）

### 切换项目

支持指定项目根目录和选择特定项目：

```bash
/switch <name> [root|--root <root>] [--index <n>]
```

操作流程：
1. 在注册表中查找项目（进行模糊匹配，如果指定了根目录，则在指定范围内查找）。
2. 如果找到多个匹配项：
   - 显示候选项目列表（包括项目名称、根目录、路径、最近一次提交时间、项目状态等信息）
   - 可以使用`--index <n>`来指定要选择的项目
   - 如果未指定索引，则自动选择得分最高的项目
3. 如果未找到项目，则执行上述查找流程，并提示用户输入项目路径。
4. 加载项目的相关信息：
   - `git status --short`
   - `git branch --show-current`
   - `git log --oneline -5`
   - `gh issue list -R <repo> --limit 5`（如果指定了仓库）
5. 显示项目概要信息

### 项目评分规则：
- 如果指定了项目根目录，则得分为+50分。
- 如果项目名称完全匹配，则得分为+30分。
- 如果项目名称包含指定前缀，则得分为+20分。
- 最近提交的记录得分+10分。
- 如果项目路径缺失，则得分为-10分。
- 如果仓库缺失，则得分为-5分。
- 在得分相同的情况下，优先选择最近提交的记录。

### 项目信息查看

显示项目的详细信息：
- 项目的GitHub远程仓库URL
- 最近一次提交的哈希值/日期
- 开启的Pull Request（PR）数量
- 开启的Issue数量

```bash
bash {baseDir}/scripts/project-fingerprints.sh [project-name]
bash {baseDir}/scripts/project-fingerprints.sh --root <root-key> [project-name]
```

GitHub上的PR和Issue数量缓存：
- 缓存文件默认路径：`$HOME/.openclaw/osori-cache.json`
- 缓存有效期：600秒
- 可通过环境变量覆盖缓存设置：
  - `OSORI_CACHE_FILE`
  - `OSORI_CACHE_TTL`

### 添加项目

```bash
bash {baseDir}/scripts/add-project.sh <path> [--tag <tag>] [--name <name>]
```
系统会自动检测项目的Git远程仓库地址、编程语言和项目描述。

### 扫描目录

```bash
bash {baseDir}/scripts/scan-projects.sh <root-dir> [--depth 3]
OSORI_ROOT_KEY=work bash {baseDir}/scripts/scan-projects.sh <root-dir> [--depth 3]
```
可以批量扫描目录中的Git仓库，并将其添加到注册表中。
在Telegram命令中也可以指定项目根目录。

### 删除项目

可以通过项目名称从`osori.json`中删除项目。

### 查看项目状态

可以通过`git status`和`gh issue list`命令查看单个或多个项目的状态。
在Telegram命令中可以指定项目根目录。

### 项目健康检查

**Doctor**功能用于检查注册表的健康状况，并提供修复建议。

**默认操作**（不使用任何参数）：仅进行分析并提供修复建议，不会实际修改注册表数据。

```bash
/doctor                     # preview only (default)
/doctor --fix               # preview + apply (high-risk blocked)
/doctor --fix --yes         # preview + apply all (including high-risk)
/doctor --dry-run           # explicit preview only (never applies)
/doctor --json              # machine-readable JSON output
```

项目健康风险等级：
- 🟢 **低风险**：需要规范注册表结构、迁移数据或修复缺失的字段。
- 🟡 **中等风险**：需要删除重复项目或修复根目录引用问题。
- 🔴 **高风险**：需要从损坏的状态中重新初始化注册表。

**对应的Shell命令**：

```bash
bash {baseDir}/scripts/doctor.sh [--fix] [--dry-run] [--yes] [--json]
```

更多信息请参阅：[Doctor安全修复指南](docs/examples/doctor-safe-fix.md)

### 根目录管理

```bash
/list-roots
/root-add <key> [label]
/root-path-add <key> <path>
/root-path-remove <key> <path>
/root-set-label <key> <label>
/root-remove <key> [--reassign <target>] [--force]
```

**对应的Shell命令**：

```bash
bash {baseDir}/scripts/root-manager.sh list
bash {baseDir}/scripts/root-manager.sh add <key> [label]
bash {baseDir}/scripts/root-manager.sh path-add <key> <path>
bash {baseDir}/scripts/root-manager.sh path-remove <key> <path>
bash {baseDir}/scripts/root-manager.sh set-label <key> <label>
bash {baseDir}/scripts/root-manager.sh remove <key> [--reassign <target>] [--force]
```

**删除项目的安全规则**：
- **默认情况下**，根目录不能被删除。
- 如果根目录下有项目存在：
  - 可以使用`--reassign <target>`将项目移动到其他目录后再删除
  - 或者使用`--force`将项目移动到默认目录后再删除

### 别名与收藏项目

```bash
/alias-add <alias> <project>
/alias-remove <alias>
/favorites
/favorite-add <project>
/favorite-remove <project>
```

**对应的Shell命令**：

```bash
bash {baseDir}/scripts/alias-favorite-manager.sh alias-add <alias> <project>
bash {baseDir}/scripts/alias-favorite-manager.sh alias-remove <alias>
bash {baseDir}/scripts/alias-favorite-manager.sh aliases
bash {baseDir}/scripts/alias-favorite-manager.sh favorite-add <project>
bash {baseDir}/scripts/alias-favorite-manager.sh favorite-remove <project>
bash {baseDir}/scripts/alias-favorite-manager.sh favorites
```

别名不区分大小写，可以通过`/find`、`/switch`以及`project-fingerprints.sh`命令来查询项目。

### 完整集成

可以在已注册的项目上下文中执行`entire` CLI命令：

```bash
/entire-status <project> [root|--root <root>]
/entire-enable <project> [root|--root <root>] [--agent <name>] [--strategy <name>]
/entire-rewind-list <project> [root|--root <root>]
```

**对应的Shell命令**：

```bash
bash {baseDir}/scripts/entire-manager.sh status <project> [root|--root <root>]
bash {baseDir}/scripts/entire-manager.sh enable <project> [root|--root <root>] [entire enable flags...]
bash {baseDir}/scripts/entire-manager.sh rewind-list <project> [root|--root <root>]
```

**默认设置**：
- 如果未指定参数，`entire enable`的默认值为`--agent claude-code --strategy manual-commit`。
- `/entire-rewind-list`命令使用非破坏性的JSON列表显示方式（`entire rewind --list`）。

## 注册表结构

```json
{
  "schema": "osori.registry",
  "version": 2,
  "updatedAt": "2026-02-16T00:00:00Z",
  "roots": [
    {
      "key": "default",
      "label": "Default",
      "paths": []
    }
  ],
  "aliases": {
    "rh": "RunnersHeart"
  },
  "projects": [
    {
      "name": "string",
      "path": "/absolute/path",
      "repo": "owner/repo",
      "lang": "swift|typescript|python|rust|go|ruby|unknown",
      "tags": ["personal", "ios"],
      "description": "Short description",
      "addedAt": "YYYY-MM-DD",
      "root": "default",
      "favorite": false
    }
  ]
}
```

## 自动触发规则

- 输入“work on X”或“X 프로젝트 작업하자”等命令时，会切换到对应的项目。
- 输入“find project X”或“X 찾아줘”等命令时，会在注册表中搜索或发现该项目。
- 输入“list projects”或“프로젝트 목록”时，会列出所有项目。
- 输入“add project”或“프로젝트 추가”时，会添加新项目。
- 输入“project status”或“프로젝트 상태”时，会显示所有项目的状态。