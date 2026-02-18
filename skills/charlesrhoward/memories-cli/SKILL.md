---
name: memories-cli
description: "`memories.sh` 的命令行界面（CLI）参考及工作流程——这是专为 AI 代理设计的持久化存储层。使用场景包括：  
1. 运行 `memories` CLI 命令以添加、搜索、编辑或管理存储数据；  
2. 在新项目中配置 `memories.sh`（执行 `memories init` 命令）；  
3. 生成 AI 工具配置文件（如 `CLAUDE.md`、`.cursor/rules` 等）；  
4. 从其他 AI 工具导入现有规则（使用 `memories ingest` 命令）；  
5. 管理云同步、嵌入数据或 Git 钩子（git hooks）；  
6. 使用 `memories doctor` 工具进行故障排查；  
7. 操作存储模板、链接、历史记录或标签。"
---
# memories-cli

`@memories.sh/cli` 的命令行接口（CLI）用于管理记忆（memories），生成配置文件，并在不同工具之间进行数据同步。

> **CLI 是与 `memories.sh` 交互的主要方式。** 你可以使用它来存储记忆内容、生成相应的配置文件以及管理你的记忆存储系统。在无法使用 CLI 的环境中（例如 v0 版本、bolt.new、Lovable 或其他基于浏览器的代理），请使用 [MCP 服务器](../memories-mcp/SKILL.md) 作为备用方案。

## 安装与初始化

```bash
npm install -g @memories.sh/cli   # or: npx @memories.sh/cli
memories init                      # Initialize in current project
```

`memories init` 会自动检测可用的 AI 工具（如 Claude Code、Cursor、Windsurf、VS Code），并配置 MCP 服务，同时生成相应的指令文件。

## 命令快速参考

| 命令 | 功能 |
|---------|---------|
| `memories add <内容>` | 存储一条记忆内容 |
| `memories recall` | 召回与当前项目相关的记忆内容 |
| `memories search <查询>` | 进行全文搜索 |
| `memories list` | 列出带有过滤条件的记忆内容 |
| `memories edit <id>` | 编辑记忆内容的类型或标签 |
| `memories forget <id>` | 软删除一条记忆 |
| `memories generate` | 生成 AI 工具的配置文件 |
| `memories prompt` | 生成系统提示信息 |
| `memories serve` | 启动 MCP 服务器 |

## 核心工作流程

### 1. 新项目设置

```bash
cd my-project
memories init              # Detect tools, configure MCP, generate files
memories add "Use pnpm" --type rule
memories add "Chose Supabase for auth" --type decision
memories generate          # Update all AI tool configs
```

### 2. 导入现有规则

```bash
memories ingest claude     # Import from CLAUDE.md
memories ingest cursor     # Import from .cursorrules / .cursor/rules/
memories ingest copilot    # Import from copilot-instructions.md
```

### 3. 搜索与召回

```bash
memories search "auth"                    # Full-text search
memories search "auth" --semantic         # Vector similarity (requires embeddings)
memories recall                           # Context for current project
memories list --type rule                 # Filter by type
memories list --tags api,auth             # Filter by tags
```

### 4. 生成配置文件

```bash
memories generate                         # All detected tools
memories generate claude                  # Only CLAUDE.md
memories generate cursor                  # Only .cursor/rules/memories.mdc
memories diff                             # Preview changes before generating
```

支持的目标工具：`claude`、`cursor`、`copilot`、`windsurf`、`cline`、`roo`、`gemini`

### 5. 云同步

```bash
memories login                            # Device code auth flow
memories sync                             # Sync local DB to cloud
memories files ingest                     # Upload config files
memories files apply --global --force     # Restore configs on new machine
```

### 6. 嵌入功能

```bash
memories embed                            # Generate embeddings for all memories
memories embed --dry-run                  # Preview what would be embedded
memories config model <model-name>        # Change embedding model
```

### 7. 维护

```bash
memories doctor                           # Diagnose issues
memories stats                            # Memory statistics
memories stale --days 90                  # Find stale memories
memories review                           # Interactive cleanup
memories validate                         # Check memory integrity
```

## 记忆类型

使用 `--type` 标志来指定记忆的类型：
- **rule** — `memories add "始终使用严格模式" --type rule`  
- **decision** — `memories add "使用 JWT 进行身份验证" --type decision`  
- **fact** — `memories add "每分钟请求限制为 100 次" --type fact`  
- **note** — （默认）`memories add "重构身份验证模块"`  

## 作用域

- **project** （默认） — 仅适用于当前 Git 仓库  
- **global** — `memories add "使用 TypeScript" --type rule --global`  

当使用 MCP 而非 CLI 命令时（例如在浏览器工具或仓库外运行的代理中），请使用 `add_memory` 命令并指定 `project_id` 以强制应用项目级作用域。

## 高级功能

- **模板**：`memories add --template decision` — 为常见场景提供结构化的提示模板  
- **链接**：`memories link <id1> <id2> --type supports` — 关联多条记忆内容  
- **历史记录**：`memories history <id>` / `memories revert <id> --to <版本>`  
- **标签**：`memories tag <id> add api,auth`  
- **导出/导入**：`memories export > backup.yaml` / `memories import backup.yaml`  
- **Git 钩子**：`memories hook install` — 在每次提交时自动执行相关操作  

## 参考文件

- **完整命令参考**：请参阅 [references/commands.md](references/commands.md)，了解所有命令的详细选项和参数  
- **工作流程指南**：请参阅 [references/workflows.md](references/workflows.md)，了解多步骤操作和自动化方案