---
name: clawvault
version: 2.4.2
description: "**Agent内存系统**  
该系统具备以下功能：  
- 内存图谱（Memory Graph）  
- 上下文信息分析（Context Profiles）  
- 检点/恢复机制（Checkpoint/Recovery）  
- 结构化存储（Structured Storage）  
- 语义搜索（Semantic Search）  
- 观测性内存管理（Observational Memory）  
- 任务跟踪（Task Tracking）  
- 画布式仪表板（Canvas Dashboards）  
- 与Obsidian平台的集成（Integration with Obsidian）  
- Tailscale网络支持（Tailscale Networking）  

**适用场景：**  
- 存储/搜索内存数据  
- 防止上下文信息丢失（Preventing context loss）  
- 基于内存图谱的上下文数据检索  
- 修复损坏的会话（Recovering broken sessions）  
- 任务跟踪与管理  
- 生成可视化仪表板（Generating dashboards）  

**不适用场景：**  
- 通用文件输入/输出操作（General file I/O operations）"
author: Versatly
repository: https://github.com/Versatly/clawvault
homepage: https://clawvault.dev
docs: https://docs.clawvault.dev
metadata:
  {
    "openclaw":
      {
        "emoji": "🐘",
        "kind": "cli",
        "requires":
          {
            "bins": ["clawvault"],
            "env_optional": ["CLAWVAULT_PATH", "GEMINI_API_KEY", "OPENCLAW_HOME", "OPENCLAW_STATE_DIR"]
          },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "clawvault",
              "bins": ["clawvault"],
              "label": "Install ClawVault CLI (npm)"
            }
          ],
        "hooks":
          {
            "clawvault":
              {
                "events": ["gateway:startup", "command:new"],
                "capabilities":
                  [
                    "auto-checkpoint before session reset (/new)",
                    "context death detection and alert injection on startup"
                  ],
                "does_not":
                  [
                    "make network calls (except optional GEMINI_API_KEY for observe/reflect, Tailscale for serve/peers)",
                    "access external APIs or cloud services (except optional Tailscale mesh)",
                    "send telemetry or analytics",
                    "modify files outside vault directory and OpenClaw session transcripts"
                  ]
              }
          },
        "capabilities":
          [
            "reads/writes markdown files in vault directory",
            "reads/modifies OpenClaw session transcripts (repair-session, with backup)",
            "builds memory graph index (.clawvault/graph-index.json)",
            "runs qmd for semantic search (optional, graceful fallback)",
            "LLM API calls for observe/reflect (optional, requires GEMINI_API_KEY)",
            "task tracking with status, priority, and blocking relationships",
            "Obsidian JSON Canvas dashboard generation (4 templates: default, brain, project-board, sprint)",
            "Obsidian Bases view generation (5 .base files for task management)",
            "Neural graph theme with colored nodes by category",
            "Tailscale-based vault networking, cross-vault search, observation forwarding"
          ]
      }
  }
---

# ClawVault 🐘

大象永远不会忘记。专为AI代理设计的结构化记忆系统。

> **文档：** [docs.clawvault.dev](https://docs.clawvault.dev) | **npm：** [clawvault](https://www.npmjs.com/package/clawvault)

## 安全性与透明度

**该工具的功能：**
- 读取/写入您指定的vault目录（`CLAWVAULT_PATH`或自动检测到的目录）中的markdown文件
- `repair-session` 功能可以读取和修改OpenClaw会话记录，并在写入前创建备份
- 安装一个OpenClaw **钩子**（`hooks/clawvault/handler.js`），在 `gateway:startup` 和 `command:new` 事件触发时自动执行，用于检查会话状态并检测上下文丢失情况
- `observe` 功能会调用LLM API（默认使用Gemini Flash）来压缩会话记录
- `reflect` 功能会调用LLM API生成每周的总结报告
- `serve` 功能会在您的Tailscale IP上启动一个HTTP API，实现跨vault之间的数据共享

**使用的环境变量：**
- `CLAWVAULT_PATH` — vault的位置（可选，系统会自动检测）
- `OPENCLAW_HOME` / `OPENCLAW_STATE_DIR` — `repair-session` 用于查找会话记录的目录
- `GEMINI_API_KEY` — `observe` 和 `reflect` 用于LLM数据压缩的密钥（可选）

**所有数据均存储在本地，不进行云同步。**

## 安装

```bash
npm install -g clawvault
```

## 初始化与设置

```bash
# Initialize a new vault (creates categories + ledger + templates + welcome note)
clawvault init ~/my-vault

# Minimal vault (memory categories only, no tasks/bases/graph)
clawvault init ~/my-vault --minimal

# Custom categories
clawvault init ~/my-vault --categories "notes,ideas,contacts,projects"

# Skip specific features
clawvault init ~/my-vault --no-bases --no-tasks --no-graph

# Apply neural graph theme on init
clawvault init ~/my-vault --theme neural

# Generate canvas on init
clawvault init ~/my-vault --canvas brain

# Full Obsidian setup (theme + bases + canvas on existing vault)
clawvault setup
clawvault setup --theme neural --canvas brain --bases

# Or set env var to use existing vault
export CLAWVAULT_PATH=/path/to/memory
```

### 初始化参数（v2.4.0及以上版本）

| 参数 | 说明 |
|------|-------------|
| `-n, --name <名称>` | Vault的名称（默认为目录名称） |
| `--minimal` | 仅显示内存分类信息，不显示任务、基础数据或图表 |
| `--categories <列表>` | 以逗号分隔的自定义分类 |
| `--no-bases` | 跳过Obsidian基础数据文件的生成 |
| `--no-tasks` | 跳过任务和待办事项目录的生成 |
| `--no-graph` | 跳过初始图表的生成 |
| `--canvas <模板>` | 生成相应的仪表板模板（默认为“brain”、“project-board”或“sprint”） |
| `--theme <样式>` | 图表的颜色主题（neural、minimal、none） |
| `--qmd` | 设置qmd语义搜索功能 |

### 设置参数（v2.4.0及以上版本）

| 参数 | 说明 |
|------|-------------|
| `--theme <样式>` | 图表的颜色主题（默认为“neural”、“minimal”或“none” |
| `--graph-colors` / `--no-graph-colors` | 是否启用图表颜色方案 |
| `--bases` / `--no-bases` | 是否生成Obsidian基础数据视图 |
| `--canvas <模板>` | 生成相应的仪表板模板 |
| `--force` | 覆盖现有的配置文件 |
| `-v, --vault <路径>` | 指定vault的路径 |

## 快速入门

```bash
# Start your session
clawvault wake

# Capture and checkpoint during work
clawvault capture "TODO: Review PR tomorrow"
clawvault checkpoint --working-on "PR review" --focus "type guards"

# End your session
clawvault sleep "PR review + type guards" --next "respond to CI" --blocked "waiting for CI"

# Health check
clawvault doctor
```

## 新功能

### v2.4.x 版本的新特性：
- **自定义初始化参数**：`--minimal`、`--categories`、`--no-bases`、`--no-tasks`、`--no-graph`、`--canvas`、`--theme`、`--name`
- **现有vault的处理**：在检测到现有vault时会发出错误提示，而不会直接覆盖原有数据
- **新增仪表板模板**：默认模板包括“brain”（四象限架构）、“project-board”（以负责人为中心的视图）和“sprint”模板
- **仪表板参数**：`--owner`、`--width`、`--height`、`--include-done`、`--list-templates`用于自定义仪表板显示内容
- **图表样式**：支持深色背景、按类别/标签着色的节点、绿色的神经链接以及金色的高亮显示
- **Obsidian基础数据**：自动生成5个`.base`文件（包括所有任务、待办事项、按项目分类的任务、按负责人分类的任务）
- **日期处理改进**：文档中的日期格式现在不会导致命令执行失败

### v2.3.0 版本的新特性：
- **任务跟踪**：新增`clawvault task`（添加/列出/更新/完成/显示任务）和`clawvault backlog`（添加/列出/推进待办事项）命令
- **仪表板**：`clawvault canvas`可生成Obsidian格式的JSON图表
- **待办事项视图**：`clawvault blocked`用于快速查看被阻止的任务
- **Tailscale网络支持**：新增`clawvault serve`、`clawvault peers`、`clawvault net-search`命令以实现网络通信

### v2.2.0 版本的新特性：
- **采用“账本优先”的数据结构**：`ledger/raw/`作为数据来源
- **每周生成总结报告**：`clawvault reflect`功能
- **回放/重建/归档**：新增`clawvault replay`、`clawvault rebuild`、`clawvault archive`命令

### v2.0.0 版本的新特性：
- **内存图表**：基于wiki链接、标签和文档前言生成内存图表
- **上下文检索**：支持根据上下文生成图表（默认模式包括“规划”、“事件”和“交接”）
- **兼容OpenClaw**：改进了与OpenClaw的兼容性

---

## 核心命令

### 启动/停止工具

```bash
clawvault wake
clawvault sleep "what I was working on" --next "ship v1" --blocked "waiting for API key"
```

### 按类型存储数据

```bash
clawvault remember decision "Use Postgres over SQLite" --content "Need concurrent writes"
clawvault remember lesson "Context death is survivable" --content "Checkpoint before heavy work"
clawvault remember relationship "Justin Dukes" --content "Client at Hale Pet Door"
```

### 快速捕获数据

```bash
clawvault capture "TODO: Review PR tomorrow"
```

### 搜索功能

```bash
clawvault search "client contacts"        # Keyword (fast)
clawvault vsearch "database decision"     # Semantic (slower, more accurate)
```

## 任务跟踪（v2.3.0及以上版本）

```bash
clawvault task add "Ship v2.4.0" --priority high
clawvault task list
clawvault task list --status blocked
clawvault task update <id> --status in-progress
clawvault task done <id>
clawvault blocked                          # Quick blocked view
clawvault backlog add "Voice memo capture"
clawvault backlog promote <id>
```

## 仪表板（v2.3.0及以上版本）

```bash
# Generate with default template
clawvault canvas

# Choose template
clawvault canvas --template brain           # 4-quadrant architecture view
clawvault canvas --template project-board   # Owner-centric with agent/human cards
clawvault canvas --template sprint          # Sprint-focused view

# Filter and customize
clawvault canvas --owner agent-alpha        # Filter to one owner
clawvault canvas --include-done             # Include completed tasks
clawvault canvas --width 1600 --height 1200

# List available templates
clawvault canvas --list-templates
```

## 与Obsidian的集成（v2.4.0及以上版本）

### 神经图表样式

```bash
clawvault setup --theme neural    # Dark bg, colored nodes, green links, golden glow
clawvault setup --theme minimal   # Subtle category colors
clawvault setup --theme none      # No theme changes
```

### Obsidian基础数据视图

自动生成的`.base`文件，用于Obsidian插件：
- `all-tasks.base`：按状态分组的活动任务
- `blocked.base`：被阻止的任务及其原因
- `by-project.base`：按项目分组的任务
- `by-owner.base`：按负责人分组的任务
- `backlog.base`：按来源分类的待办事项

```bash
clawvault setup --bases           # Generate bases files
```

## 观察功能（v2.1.0及以上版本）

```bash
clawvault observe                  # Watch current session
clawvault observe --compress file  # One-shot compression
```

观察结果会按照重要性进行排序：`[类型|置信度|i=重要性]`

## 账本功能（v2.2.0及以上版本）

```bash
clawvault reflect                  # Generate weekly reflection
clawvault replay --last 7d         # Replay recent events
clawvault rebuild                  # Rebuild from raw ledger
clawvault archive --before 2026-01-01
```

## 内存图表（v2.0.0及以上版本）

```bash
clawvault graph                    # View graph summary
clawvault graph --refresh          # Rebuild index
clawvault context "topic"          # Graph-aware context retrieval
clawvault context --profile planning "Q1 roadmap"
clawvault entities                 # List linkable entities
clawvault link --all               # Auto-link mentions
```

## 上下文丢失的恢复机制

```bash
clawvault wake                     # Start session (recover + recap)
clawvault checkpoint --working-on "task" --focus "details"
clawvault sleep "summary" --next "next steps" --blocked "blockers"
clawvault recover --clear          # Manual recovery check
clawvault handoff --working-on "task" --next "next" --blocked "blocker"
```

## Tailscale网络支持（v2.3.0及以上版本）

```bash
clawvault serve                    # Serve vault on Tailscale (port 7283)
clawvault peers                    # Manage vault peers
clawvault net-search "query"       # Cross-vault search
```

## 会话修复功能

```bash
clawvault repair-session --dry-run
clawvault repair-session
clawvault repair-session --list
```

修复孤立的工具结果、异常终止的工具调用以及损坏的父级数据链

## Vault结构

```
vault/
├── .clawvault.json          # Vault config
├── .clawvault/              # Internal state (graph-index, checkpoints)
├── decisions/
├── lessons/
├── people/
├── projects/
├── goals/
├── preferences/
├── patterns/
├── commitments/
├── handoffs/
├── transcripts/
├── agents/
├── research/
├── inbox/
├── tasks/                   # Task tracking
├── backlog/                 # Backlog items
├── templates/               # 7 templates (daily-note, decision, checkpoint, etc.)
├── ledger/
│   ├── raw/                 # Raw session transcripts
│   ├── observations/        # Compressed observations
│   └── reflections/         # Weekly reflections
├── *.base                   # Obsidian Bases views (5 files)
├── dashboard.canvas         # Generated canvas
└── README.md                # Auto-generated vault docs
```

**默认包含16个分类**：决策、经验教训、人员信息、项目、目标、偏好设置、模式、承诺事项、交接记录、会话记录、代理信息、研究资料、收件箱、任务列表、待办事项、模板

可以通过`--categories`参数自定义分类

## OpenClaw钩子

捆绑的钩子（`hooks/clawvault/handler.js`）提供以下功能：
- `gateway:startup`：在程序启动时执行`clawvault recover --clear`命令；如果检测到上下文丢失，则触发警报
- `command:new`：在会话重置前自动创建备份

**注意：** 该钩子还包含`session:start`处理程序，以兼容未来的OpenClaw版本

**启用方法：**
```bash
openclaw hooks enable clawvault
```

## 环境变量

| 变量 | 用途 |
|----------|---------|
| `CLAWVAULT_PATH` | 默认的vault路径（可忽略自动检测） |
| `OPENCLAW_HOME` | OpenClaw的安装目录 |
| `OPENCLAW_STATE_DIR` | OpenClaw的状态数据目录 |
| `GEMINI_API_KEY` | 用于`observe`和`reflect`功能的LLM压缩密钥（可选）

## 常见问题解决方法：
- **qmd未安装**：运行`npm install -g qmd`或`bun install -g github:tobi/qmd`
- **未找到vault**：运行`clawvault init`或设置`CLAWVAULT_PATH`
- **初始化失败（提示“already exists”）**：该路径下已经存在vault
- **出现“unexpected tool_use_id”错误**：运行`clawvault repair-session`
- **图表数据过时**：运行`clawvault graph --refresh`更新图表
- **旧版本的emoji格式问题**：运行`clawvault migrate-observations`修复问题
- **OpenClaw版本不兼容**：运行`clawvault compat`进行兼容性检查

## 链接：
- 文档：https://docs.clawvault.dev
- npm：https://www.npmjs.com/package/clawvault
- GitHub仓库：https://github.com/Versatly/clawvault