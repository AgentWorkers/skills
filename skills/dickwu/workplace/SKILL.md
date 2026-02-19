---
name: workplace
description: 通过多代理编排、隔离的内存以及代理间的通信来管理多个工作区（项目目录）。当用户执行以下操作时，该功能会被触发：初始化/列出/切换/扫描/查看工作区状态、管理代理、在代码库之间切换、执行多代理工作流程、代理交接、配置内核代理、调整工作区结构、部署环境，或使用任何与“工作区”相关的命令。该功能也会响应 `/workplace` 命令的调用。系统会自动识别 `.git` 文件夹作为工作区。每个工作区都有自己的代理、内存配置以及部署设置，这些信息存储在 `.workplace/` 目录中。系统会将工作区的上下文信息同步到 Cursor、Claude Code 和 OpenCode 等工具中。同时，还提供了交互式的 Telegram/Discord 用户界面，用户可以通过界面中的按钮来切换工作区、启动代理或进行部署操作。
user-invocable: true
---
# 工作场所技能

支持管理多个项目工作场所，每个工作场所都有独立的代理、隔离的内存以及基于Swarm架构的代理编排机制。

## `/workplace` 命令（Telegram / 斜杠）

提供层次化的导航功能，支持从父工作场所向下钻取子工作场所：

- **`/workplace`** 或 **`/workplace list`**：显示顶级视图，包括父工作场所和独立工作场所（以按钮形式呈现）。父工作场所会显示其拥有的子工作场所数量（用`(N)`表示）。当前工作场所会标记为✓。
- **点击父工作场所按钮**：可以查看其子工作场所，并提供“使用父工作场所”和“← 返回”选项。
- **`/workplace <名称>`**：可以直接切换到指定的工作场所。如果是父工作场所且包含子工作场所，则会显示子工作场所的详细信息。
- **`/workplace parent:child`**：使用冒号语法（例如`log-stream:logstream`）直接切换工作场所。
- **`/workplace status`**：显示当前工作场所的信息，包括父工作场所、关联的工作场所以及代理状态。
- **`/workplace agents`**：列出当前工作场所中的代理，并提供启动/停止代理的按钮。

### 冒号语法

`/workplace log-stream:logstream` 会根据名称查找对应的父工作场所，然后显示该父工作场所下的所有子工作场所。这种语法允许快速切换工作场所，而无需通过菜单进行导航。

### 上下文切换

当用户切换工作场所时（无论是通过按钮点击、名称输入还是冒号语法）：

1. 会更新 `~/.openclaw/workspace/.workplaces/current.json` 文件，其中记录了当前选定的工作场所的UUID和路径。
2. 会更新 `registry.json` 文件中的 `lastActive` 字段。
3. 会加载新工作场所的 `.workplace/config.json` 文件以获取上下文信息。
4. 会发送确认信息，内容包括工作场所的名称、路径、父工作场所（如果有的话）、关联的工作场所以及代理列表。
5. 会检查 `sessions.json` 文件以确定目标工作场所的UUID：
   - 如果目标工作场所存在会话记录，则会显示“继续”和“新建聊天会话”按钮；
   - 如果没有会话记录，则会自动创建一个新的会话，并在切换提示中请求用户确认。
6. 之后的所有操作都会基于当前工作场所的上下文进行。

在执行任何工作场所相关操作之前，请先读取 `current.json` 文件，以了解当前激活的工作场所是什么。

有关完整的按钮布局、回调路由和平台兼容性信息，请参阅 [telegram-ui.md](references/telegram-ui.md)。

## 快速参考

| 命令 | 功能 |
|---------|--------|
| `workplace init [路径]` | 初始化工作场所（扫描现有工作场所或创建新的工作场所） |
| `workplace list` | 列出所有工作场所（提供切换按钮） |
| `workplace switch <名称\|uuid>` | 切换到指定的工作场所 |
| `workplace scan [路径]` | 在子目录中查找 `.git` 格式的工作场所 |
| `workplace link <路径>` | 关联一个工作场所 |
| `workplace unlink <路径\|uuid>` | 取消关联一个工作场所 |
| `workplace status` | 显示当前工作场所的信息及代理状态 |
| `workplace agents` | 列出当前工作场所中的代理 |
| `workplace agent start <名称>` | 启动一个代理（该代理将以子代理的形式运行） |
| `workplace agent stop <名称>` | 停止正在运行的代理 |
| `workplace kernel start` | 启动持久化的内核代理 |
| `workplace kernel stop` | 停止内核代理 |
| `workplace export [zip\|json]` | 导出工作场所配置 |
| `workplace import <文件>` | 从导出的文件中导入工作场所配置 |
| `workplace load <路径\|名称\|uuid>` | 加载并打开已注册的工作场所 |
| `workplace unload <名称\|uuid>` | 从已加载的工作场所列表中移除该工作场所 |
| `workplace loaded` | 列出所有已加载的工作场所 |
| `workplace delete <名称\|uuid>` | 从注册表中删除该工作场所 |
| `workplace deploy <环境>` | 显示/运行部署指令 |
| `workplace sync <IDE>` | 为 cursor/claude/opencode/all 生成上下文信息 |
| `workplace sessions` | 列出当前工作场所的聊天会话 |
| `workplace session new [标签]` | 创建一个新的聊天会话 |
| `workplace session continue [标签]` | 恢复已保存的会话 |
| `workplace session delete <标签>` | 删除已保存的会话 |
| `workplace session rename <旧标签> <新标签>` | 重命名会话 |

## 架构

### 注册表

注册表位于 `~/.openclaw/workspace/.workplaces/` 目录下：
- `registry.json`：包含所有已知工作场所的 UUID、路径、主机名和关联信息。
- `current.json`：记录当前激活的工作场所。
- `loaded.json`：记录当前正在“打开/加载”中的工作场所，便于快速访问和跨工作场所操作。

### 每个工作场所的结构

每个项目都有一个 `.workplace/` 目录：

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

### 已加载的工作场所

`loaded.json` 文件记录了当前正在“打开”的工作场所。这与注册表（包含所有已知工作场所）和当前激活的工作场所是不同的。已加载的工作场所是指用户正在实际操作的工作场所，这对于跨工作场所的代理编排、快速切换和上下文感知非常有用。

```json
[
  {
    "uuid": "74cdd6fd-...",
    "name": "log-stream",
    "path": "/Users/dev/opensource/log-stream",
    "loadedAt": "2026-02-17T22:05:00Z",
    "source": "manual"
  }
]
```

字段说明：
- `uuid`：工作场所的 UUID（与注册表中的信息匹配）。
- `name`：工作场所的显示名称。
- `path`：工作场所的绝对文件系统路径。
- `loadedAt`：工作场所被加载的时间戳（ISO 格式）。
- `source`：工作场所的加载方式（手动、自动或关联）。

可以通过 `scripts/loaded_workplaces.sh` 脚本来管理已加载的工作场所（列出、加载、卸载或查看状态）。

### 会话管理

每个工作场所的聊天会话信息存储在 `~/.openclaw/workspace/.workplaces/sessions.json` 文件中。每个工作场所的 UUID 都对应一个会话数组（包含会话 ID、标签和时间戳），以及一个 `activeSession` 指针。

切换工作场所时：
- 如果目标工作场所有已保存的会话记录，会显示“继续”和“新建聊天”按钮。
- 如果没有已保存的会话记录，系统会自动创建一个新的会话。
- 会话记录会以 `.jsonl` 文件的形式保存在 OpenClaw 系统中。

点击“继续”按钮时，系统会从会话记录中加载最新的上下文信息；点击“新建聊天”按钮时，系统会提示用户输入会话标签。

有关完整的按钮布局和回调路由信息，请参阅 [telegram-ui.md](references/telegram-ui.md)。

### 工作场所的检测

- 任何包含 `.git/` 目录的目录都可能是一个工作场所。
- 子模块会被视为嵌套的工作场所。
- 父工作场所会自动从父目录中被检测出来。
- 用户也可以通过 `workplace link` 命令手动关联工作场所。

## 工作流程

### 初始化工作场所

1. 运行 `scripts/init_workplace.sh <路径> [--名称 <名称>] [--描述 <描述>]` 命令来初始化一个工作场所。
2. 对于现有的项目，系统会扫描目录结构，读取 `.md` 文件，分析项目类型，并推荐合适的代理。
3. 对于空文件夹，系统会询问用户项目的名称、描述、所需的语言/框架和角色。
4. 系统会创建相应的 `.workplace/` 目录结构，并将其注册到中央注册表中，然后设置为当前工作场所。
有关完整的初始化流程，请参阅 [init-guide.md](references/init-guide.md)。

### 代理系统

代理配置文件位于 `.workplace/agents/` 目录下，采用 YAML 格式编写（包含代理的名称、角色、触发条件等信息）。可以通过 `sessionsspawn` 命令来启动代理，系统会根据代理的配置和工作场所的上下文来执行相应的操作。

有关代理的创建、Swarm 集群机制和运行时细节，请参阅 [agent-system.md](references/agent-system.md)。

### 代理间的通信

代理之间通过 `chat.md` 文件进行通信，使用结构化的消息协议。Rust 文件监控器服务器会监视文件的变化，并将解析后的消息以 JSON 格式输出。

有关消息格式的详细信息，请参阅 [chat-protocol.md](references/chat-protocol.md)。

### Rust 文件监控器服务器

该服务器的二进制文件位于 `assets/bin/workplace-server-{os}-{arch}` 目录下，可以通过 `scripts/build.sh` 脚本从源代码构建。

```bash
# Start server for a workplace
workplace-server /path/to/project

# Server outputs JSON lines to stdout for each new chat.md message
{"timestamp":"...","sender":"coder","recipient":"reviewer","broadcast":[],"message":"...","line_number":1}
```

### 导出/导入

- **ZIP 格式**：导出整个 `.workplace/` 目录（默认情况下不包含内存数据）。
- **JSON 格式**：导出工作场所的配置信息、代理定义和部署文档，形成可移植的配置文件。
- 在导入时，系统会生成一个新的 UUID 以避免冲突。

## 聊天界面（Telegram / Discord）

在支持内联按钮的平台上，`workplace list` 会显示一个可点击的切换器；`workplace agents` 会显示每个代理的启动/停止按钮；`workplace deploy` 会显示与部署相关的按钮。

有关消息格式、按钮组件和回调处理方式的详细信息，请参阅 [telegram-ui.md](references/telegram-ui.md)。

在不支持内联按钮的平台上（如 WhatsApp、Signal），系统会使用编号列表来显示工作场所信息。

## 集成到 IDE 中

系统会将工作场所的上下文信息同步到外部编码工具中：
- **Cursor**：通过 `.cursor/rules/workplace.mdc` 文件进行同步（使用 Markdown 格式）。
- **Claude Code**：通过 `CLAUDE.md` 文件进行同步（基于标记的更新）。
- **OpenCode**：通过 `opencode.jsonc` 文件中的指令进行同步。

可以通过运行 `workplace sync all` 命令来更新所有已检测到的 IDE；也可以针对特定的 IDE 运行 `workplace sync cursor` 命令。

有关集成细节，请参阅 [ide-sync.md](references/ide-sync.md)。

## 脚本

| 脚本 | 功能 |
|--------|---------|
| `scripts/init_workplace.sh` | 初始化指定目录下的工作场所配置 |
| `scripts/scan_workplaces.sh` | 在指定路径下查找 `.git` 格式的工作场所 |
| `scripts/loaded_workplaces.sh` | 管理已加载的工作场所（列出、加载、卸载或查看状态） |
| `scripts/build.sh` | 为当前平台构建 Rust 服务器。 |

## 超级内存集成

每个工作场所都会使用自己的 UUID 作为超级内存操作的 `containerTag`：
- 内核代理会保存工作场所的结构摘要和项目相关信息。
- 所有工作场所的内存都是隔离的，每个工作场所的内存都通过 `containerTag` 进行区分。
- 这种机制支持跨会话的工作状态感知。

## 命令详情

有关所有命令的详细信息（包括使用示例），请参阅 [commands.md](references/commands.md)。