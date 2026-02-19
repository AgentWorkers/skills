---
name: workplace
description: **使用多代理编排、隔离内存和代理间通信来管理多个工作区（项目目录）**。当用户执行以下操作时，该功能会被触发：初始化/列出/切换/扫描/查看工作区状态、管理代理、在代码库之间切换、执行多代理工作流程、进行代理交接、配置内核代理、调整工作区结构、部署环境，或使用任何与“工作区”相关的命令。该功能也会通过 `/workplace/` 命令被触发。系统会自动识别 `.git` 文件夹作为工作区。每个工作区都有自己独立的代理、内存配置以及存储在 `.workplace/` 目录中的技能和部署设置。系统会将工作区的相关信息同步到 Cursor、Claude Code 和 OpenCode 等工具中。同时，提供交互式的 Telegram/Discord 用户界面，用户可以通过界面中的内联按钮来切换工作区、启动代理或执行部署操作。
user-invocable: true
---
# 工作场所技能

支持管理多个项目工作场所，每个工作场所都配有专属的代理（agent）、独立的内存空间，并采用Swarm风格的代理编排机制。

## `/workplace` 命令（Telegram / 斜杠）

提供层次化的导航功能，支持从父工作场所逐级深入子工作场所：

- **`/workplace`** 或 **`/workplace list`**：显示顶层视图，其中父工作场所和独立工作场所以按钮形式呈现；父工作场所会显示其拥有的子工作场所数量（用 `(N)` 表示）。当前工作场所会用 ✓ 标记。
- **点击父工作场所按钮**：可以进入该子工作场所，页面会显示子工作场所的按钮以及“使用父工作场所”和“← 返回”选项。
- **`/workplace <名称>`**：可以直接切换到指定的工作场所；如果是父工作场所，则会显示其子工作场所的列表。
- **`/workplace parent:child`**：使用冒号语法（例如 `log-stream:logstream`）直接切换工作场所。
- **`/workplace status`**：显示当前工作场所的详细信息，包括父工作场所、关联的工作场所以及代理状态。
- **`/workplace agents`**：列出当前工作场所中的代理，并提供启动/停止代理的按钮。

### 冒号语法

`/workplace log-stream:logstream` 会根据名称查找对应的父工作场所，然后在该父工作场所下查找子工作场所。这种语法支持快速切换工作场所，无需通过菜单进行导航。

### 上下文切换

当用户切换工作场所时（无论是通过按钮点击、名称输入还是冒号语法）：

1. 系统会更新 `~/.openclaw/workspace/.workplaces/current.json` 文件，记录当前选择的UUID和工作场所路径。
2. 更新 `registry.json` 文件中的 `lastActive` 字段。
3. 加载新工作场所的 `.workplace/config.json` 文件以获取上下文信息。
4. 系统会发送确认信息，包括工作场所的名称、路径、父工作场所（如果有的话）、关联的工作场所列表以及代理列表。
5. 会话中的后续消息都会基于当前激活的工作场所上下文进行显示。

在执行任何与工作场所相关的操作之前，请先读取 `current.json` 文件，以确定当前激活的工作场所是什么。

有关完整的按钮布局、回调路由和平台兼容性信息，请参阅 [telegram-ui.md](references/telegram-ui.md)。

## 快速参考

| 命令 | 功能 |
|---------|--------|
| `workplace init [路径]` | 初始化工作场所（扫描现有工作场所或创建新的工作场所） |
| `workplace list` | 列出所有工作场所（提供切换按钮） |
| `workplace switch <名称\|UUID>` | 切换到指定的工作场所 |
| `workplace scan [路径]` | 在子目录中查找包含 `.git` 文件的工作场所 |
| `workplace link <路径>` | 关联一个工作场所 |
| `workplace unlink <路径\|UUID>` | 取消关联一个工作场所 |
| `workplace status` | 显示当前工作场所的详细信息及代理状态 |
| `workplace agents` | 列出当前工作场所中的代理 |
| `workplace agent start <名称>` | 启动一个代理（该代理将以子代理的形式运行） |
| `workplace agent stop <名称>` | 停止正在运行的代理 |
| `workplace kernel start` | 启动持久化的内核代理 |
| `workplace kernel stop` | 停止内核代理 |
| `workplace export [zip\|json]` | 导出工作场所配置 |
| `workplace import <文件>` | 从导出的文件中导入工作场所配置 |
| `workplace delete <名称\|UUID>` | 从注册表中删除工作场所 |
| `workplace deploy <环境>` | 显示/运行部署指令 |
| `workplace sync <IDE>` | 为 Cursor、Claude 或 OpenCode 等工具生成上下文信息 |

## 架构

### 注册表

中央注册表位于 `~/.openclaw/workspace/.workplaces/` 目录下：
- `registry.json`：记录所有已知工作场所的 UUID、路径、主机名和关联关系。
- `current.json`：记录当前激活的工作场所。

### 每个工作场所的结构

每个项目都有一个 `.workplace/` 目录。

```
.workplace/
├── config.json          # UUID, name, path, hostname, linked, parent
├── agents/*.md          # Agent role definitions (kernel.md always present)
├── memory/              # Isolated daily logs (YYYY-MM-DD.md)
├── skills/              # Workplace-specific skills (user-managed via git)
├── chat.md              # Inter-agent communication
├── structure.json       # Auto-scanned file tree
├── full-tree.md         # Full tree with parent + linked workplaces (by hostname)
├── process-status.json  # Agent runtime states and errors
└── deploy/              # Deployment docs: dev.md, main.md, pre.md
```

### 工作场所的检测

- 任何包含 `.git/` 目录的文件夹都可能是一个工作场所。
- 子模块会被视为嵌套的工作场所。
- 父工作场所会自动从父目录中被检测出来。
- 用户也可以通过 `workplace link` 命令手动关联工作场所。

## 工作流程

### 初始化工作场所

1. 运行 `scripts/init_workplace.sh <路径> [--name <名称>] [--desc <描述>]` 命令。
2. 对于现有项目：扫描文件结构，读取 `.md` 文件，分析项目类型，并推荐合适的代理。
3. 对于空文件夹：询问项目名称、描述、所需的语言/框架和角色。
4. 创建 `.workplace/` 目录结构，并将其注册到中央注册表中，然后设置为当前工作场所。
有关完整的初始化流程，请参阅 [init-guide.md](references/init-guide.md)。

### 代理系统

代理信息存储在 `.workplace/agents/` 目录下的 `.md` 文件中，这些文件使用 YAML 格式定义代理的详细信息（如名称、角色、触发条件等）。代理通过 `sessions_spawn` 命令启动，系统会根据代理的定义和工作场所的上下文生成相应的提示。

- 有关代理的创建、Swarm 机制以及运行时细节，请参阅 [agent-system.md](references/agent-system.md)。

### 代理间的通信

代理之间通过 `chat.md` 文件使用结构化的消息协议进行通信。Rust 文件监控器服务器会监测文件变化，并将解析后的消息以 JSON 格式输出。

- 有关消息格式的详细信息，请参阅 [chat-protocol.md](references/chat-protocol.md)。

### Rust 文件监控器服务器

该服务器的二进制文件位于 `assets/bin/workplace-server-{os}-{arch}` 目录下，可以通过 `scripts/build.sh` 脚本从源代码构建。

```bash
# Start server for a workplace
workplace-server /path/to/project

# Server outputs JSON lines to stdout for each new chat.md message
{"timestamp":"...","sender":"coder","recipient":"reviewer","broadcast":[],"message":"...","line_number":1}
```

### 导出/导入

- **ZIP 格式**：导出整个 `.workplace/` 目录（默认不包含内存数据）。
- **JSON 格式**：导出配置文件、代理定义以及部署文档，形成可移植的配置文件。
- 导入新工作场所时，系统会生成一个新的 UUID 以避免冲突。

## 聊天界面（Telegram / Discord）

在支持内联按钮的平台上，`workplace list` 会提供一个可点击的切换器；`workplace agents` 会显示每个代理的启动/停止按钮；`workplace deploy` 会显示与部署相关的按钮。

有关消息格式、按钮组件和回调处理的详细信息，请参阅 [telegram-ui.md](references/telegram-ui.md)。

在不支持内联按钮的平台上（如 WhatsApp、Signal），系统会使用编号文本列表来显示工作场所信息。

## 集成到 IDE 中

系统会将工作场所的上下文信息同步到外部编码工具中：
- **Cursor**：通过 `.cursor/rules/workplace.mdc` 文件进行同步（该文件使用 MDC 格式）。
- **Claude Code**：通过 `CLAUDE.md` 文件进行同步（基于标记的更新）。
- **OpenCode**：通过 `opencode.jsonc` 文件中的指令字段进行同步。

运行 `workplace sync all` 命令可以同步所有已检测到的 IDE；也可以针对特定 IDE 运行 `workplace sync cursor` 命令。

有关集成细节，请参阅 [ide-sync.md](references/ide-sync.md)。

## 脚本

| 脚本 | 功能 |
|--------|---------|
| `scripts/init_workplace.sh` | 初始化指定目录下的工作场所配置 |
| `scripts/scan_workplaces.sh` | 在指定路径下查找包含 `.git` 文件的工作场所 |
| `scripts/build.sh` | 为当前平台构建 Rust 服务器 |

## 超级内存集成

每个工作场所都会使用其唯一的 UUID 作为超级内存操作的标识符：
- 内核代理会保存工作场所的结构摘要和项目相关信息。
- 所有工作场所的内存空间都是相互隔离的。
- 这种机制支持跨会话的工作状态共享。

## 命令详情

有关所有命令的详细信息（包括使用示例），请参阅 [commands.md](references/commands.md)。