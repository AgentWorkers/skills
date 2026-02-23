---
name: taskflow
description: OpenClaw代理的结构化项目/任务管理工具：支持Markdown格式的编写，基于SQLite的查询功能，具备双向同步能力，提供命令行界面（CLI），同时支持与Apple Notes的集成。
metadata:
  {
    "openclaw":
      {
        "emoji": "📋",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["node"], "env": ["OPENCLAW_WORKSPACE"] },
      },
  }
---
# TaskFlow — 代理技能参考

TaskFlow 为任何 OpenClaw 代理提供了一个 **结构化的项目/任务/计划系统**，支持使用 Markdown 进行内容编写，通过 SQLite 进行数据查询，并支持双向数据同步。

**工作原理：** Markdown 是主要的编写格式。直接编辑 `tasks/*.md` 文件即可。SQLite 数据库是一个索引文件，而非数据的原始存储来源。

---

## 安全性

### OPENCLAW_WORKSPACE 的信任边界

`OPENCLAW_WORKSPACE` 是一个 **高信任级别的值**。所有 TaskFlow 脚本都会从该值中解析文件路径，CLI 和同步守护进程也会使用它来定位 SQLite 数据库、Markdown 任务文件以及日志目录。

**安全使用规则：**

1. **仅从受信任的、受控制的来源设置该值。** 该值必须来自：
   - 你的 shell 配置文件（`.zshrc`、`.bashrc`、`/etc/environment`）
   - 你控制的模板中的 systemd 用户单元 `Environment=` 指令
   - 你安装的 macOS LaunchAgent 的 `EnvironmentVariables` 字典

   **绝对** 不要从以下来源接受 `OPENCLAW_WORKSPACE`：
   - 用户提供的 CLI 参数或 HTTP 请求参数
   - 运行时读取的不可信配置文件
   - 任何未经明确验证的外部输入

2. **在使用前验证路径是否存在。** 任何读取 `OPENCLAW_WORKSPACE` 的脚本都应在继续执行前确认该目录确实存在：

--- 

3. **不要从不受信任的输入中构建路径。** 即使 `OPENCLAW_WORKSPACE` 是有效的，也绝不要将未经验证的用户输入拼接到路径中（例如 `path.join(workspace, userSlug, '`etc/passwd')`）。应使用 `path.resolve()` 并检查解析后的路径是否以工作空间根目录开头：

--- 

4. **仅将 `OPENCLAW_WORKSPACE` 视为本地系统路径。** 它必须指向本地文件系统中的一个目录。虽然远程路径（NFS 挂载、网络共享）可能也可以使用，但它们不在测试范围内，且可能会引入时间检查（TOCTOU）相关的问题。

---

## 设置

### 1. 设置环境变量

将以下内容添加到你的 shell 配置文件（`.zshrc`、`.bashrc` 等）中：

--- 

所有 TaskFlow 脚本和 CLI 都会从这个变量中解析路径。如果没有这个变量，它们会回退到使用 `process.cwd()`，而这几乎不是你想要的结果。

> **另请参阅：** 上面的 [OPENCLAW_WORKSPACE 信任边界](#openclaw_workspace-trust-boundary) 以了解安全要求。

### 2. 链接 CLI

--- 

### 3. 运行设置向导

--- 

设置向导会处理其余的工作：创建工作空间目录，指导你添加第一个项目，初始化数据库，并可选地安装 macOS LaunchAgent 以实现定期同步。

**替代方案 — 手动设置：**

<details>
<summary>如果你希望有更明确的控制权，可以参考手动步骤</summary>

--- 

---

## 首次运行

### 对于代理（OpenClaw / AI）

当用户要求你设置 TaskFlow 或检测到它尚未初始化时：

1. **检测状态。** 检查 `$OPENCLAW_WORKSPACE/PROJECTS.md` 和 `$OPENCLAW_WORKSPACE/memory/taskflow.sqlite` 的存在。
2. **如果是全新的环境：** 询问用户第一个项目的名称和描述，然后运行：
   --- 
   接着运行 `taskflow status` 来确认设置是否完成。
3. **如果 `PROJECTS.md` 存在但数据库不存在：** 运行 `taskflow setup`（它会自动检测状态并提示是否需要初始化和同步）。
4. **如果两者都存在：** 运行 `taskflow status` — 表明已经设置完成。
5. 设置完成后，更新 `AGENTS.md` 文件，添加新的项目标识符，以便后续会话可以通过 `cat PROJECTS.md` 发现该项目。

### 对于人类用户（通过 CLI）

--- 

交互式向导会：
- 检测你现有的工作空间状态
- 指导你为第一个项目命名
- 根据模板创建 `PROJECTS.md` 和 `tasks/<slug>-tasks.md` 文件
- 初始化 SQLite 数据库并执行同步
- 提供安装定期同步守护进程的选项（在 macOS 上使用 LaunchAgent，在 Linux 上使用 systemd 定时器）

**非交互式（脚本安装）：**

--- 

--- 

## 目录结构

--- 

## 创建项目

创建新项目时，请遵循以下完整步骤：

### 1. 在 `PROJECTS.md` 中添加一个条目

--- 

- `slug` 应该是小写且用连字符分隔的（例如 `my-project`）。它将成为项目的唯一标识符。
- 可能的状态值有：`active`（活动）、`paused`（暂停）、`done`（已完成）。

### 2. 创建任务文件

将 `taskflow/templates/tasks-template.md` 复制到 `tasks/<slug>-tasks.md`，并在文件标题中更新项目名称。

该文件 **必须** 按以下顺序包含以下五个部分标题：

--- 

### 3. （可选）创建计划文件

将 `taskflow/templates/plan-template.md` 复制到 `plans/<slug>-plan.md`，用于存储架构文档、设计决策和分阶段路线图。计划文件 **不会** 被同步到 SQLite 中 — 它们仅用于代理参考。

### 4. 数据库记录（首次同步时自动创建）

你 **不需要** 手动将项目信息插入 `projects` 表中。同步引擎会在下一次执行 `files-to-db` 时根据 `PROJECTS.md` 自动创建项目记录。如果你想通过 Node.js 显式操作，可以使用参数化语句：

--- 

## 任务行格式

每条任务行都必须遵循以下格式：

| 字段 | 说明 |
|---|---|
| `[ ]` / `[x]` | 表示任务处于活动/已完成状态。同步状态由部分标题决定，而不是由这个复选框决定。 |
| `(task:<id>)` | 任务 ID。格式为 `<slug>-NNN`（前三位用零填充）。每个项目中的任务 ID 是唯一的。 |
| `[<priority>]` | **必填**。必须放在所有者标签之前。请参见下面的优先级表。 |
| `[<owner>]` | 可选。代理/模型标签（例如 `codex`、`sonnet`、`claude`）。 |
| `<title>` | 人类可读的任务标题。 |

### ⚠️ 标签顺序规则

**优先级标签必须放在所有者标签之前。** 同步解析器会按顺序读取第一个 `[Px]` 标签作为优先级，然后是 `[tag]` 标签。如果顺序颠倒，会导致解析错误。**

### ⚠️ 标题清理规则

任务标题只能是 **纯文本**。在将用户提供的字符串作为任务标题之前，请遵循以下规则：

1. **拒绝看起来像部分标题的行。** 标题不能以一个或多个 `#` 字符开头，后面跟着空格（例如 `# My heading`、`## Done`）。这些会导致同步解析器无法正确识别部分内容。
2. **拒绝那些本身就是部分标题的字符串**：
   - `In Progress`、`Pending Validation`、`Backlog`、`Blocked`、`Done`
   - 注意比较时不需要区分大小写。
3. **转义或删除任务文件中具有结构意义的 Markdown 特殊字符**：

   | 字符 | 风险 | 安全处理方式 |
|-----------|------|-------------|
| `#`       | 看起来像部分标题 | 删除或忽略 |
| `- ` （行首的连字符 + 空格）` | 看起来像列表项或任务 | 删除前面的连字符 |
| `[ ]` / `[x]` | 看起来像复选框 | 转义括号：`\[` `\]` |
| `]` / `[` 单独出现 | 可能会破坏 `(task:id)` 的解析 | 转义：`\[` `\]` |
| 新行（`\n`、`\r`）` | 会导致多行标题 | 删除或忽略 |

**示例清理（使用 Node.js）：**

--- 

这些规则适用于 **任何外部或用户提供的任务标题来源**（CLI 参数、API 数据、文件导入）。代理在自身会话中硬编码的标题风险较低，但仍应避免使用这些特殊字符。

✅ 正确格式：`- [ ] (task:myproject-007) [P1] [codex] Implement search`
❌ 错误格式：`- [ ] (task:myproject-007) [codex] [P1] Implement search`

### 优先级级别（可配置）

| 标签 | 默认含义 |
|---|---|
| `P0` | 关键任务 — 需立即完成，会阻塞其他所有任务 |
| `P1` | 重要任务 — 应尽快完成 |
| `P2` | 普通任务 — 默认优先级 |
| `P3` | 较低优先级 — 可以稍后处理 |
| `P9` | 未来可能需要的任务 — 没有紧迫性 |

优先级可以在安装时进行配置，但标签本身（`P0`–`P3`、`P9`）是由同步引擎验证的。

### 可选的注释行

可以在任务行后添加缩进的 `- note:` 行来添加注释：

--- 

> **已知限制（版本 1）：** 注释是单向的。在 Markdown 中删除或编辑注释不会同步到数据库中。这将在后续版本中修复。

### 示例任务文件内容

--- 

## 添加新任务

1. **确定下一个任务 ID。** 遍历任务文件中的最高编号的 `<slug>-NNN`，然后加 1。或者使用 **参数化语句** 从 SQLite 中查询（**切勿在 SQL 语句中插入 `slug`）：

--- 

> ⚠️ **切勿通过字符串插值来构建 SQL 语句。** 对于来自外部输入的所有值，都应使用 `db.prepare()` 和命名参数或位置参数（`?` 或 `:name`）。即使是对只读查询也是如此。

2. **将任务行** 添加到正确的部分（新任务添加到 `## Backlog`，立即开始的任务添加到 `## In Progress`）。

3. **使用上述格式格式化任务行。** 任务行末尾不应有空格。优先级标签必须放在所有者标签之前。

---

## 更新任务状态

**将任务行** 从当前部分移动到 markdown 文件中的目标部分。

| 目标状态 | 移动到的部分 |
|---|---|
| Started / picked up | `## In Progress` |
| Needs human review | `## Pending Validation` |
| Not started yet | `## Backlog` |
| Waiting on dependency | `## Blocked` |
| Finished | `## Done` |

同时更新复选框的状态：活动状态显示为 `[ ]`，已完成状态显示为 `[x]`（`Pending Validation` 也可以这样显示）。

定期同步（每 60 秒）会自动检测到这些变化并更新 SQLite。如果需要立即同步，可以执行以下操作：

--- 

## 查询任务

### 简单方法：直接读取 markdown 文件

--- 

对于快速查看任务状态，只需读取相关部分即可。

### 高级方法：查询 SQLite

> ⚠️ **SQL 安全规则：** 任何包含变量值（项目标识符、任务 ID、状态字符串等）的查询 **必须** 使用参数化语句 — **不能使用字符串插值**。下面的 `sqlite3` CLI 示例仅用于诊断/检查目的，实际编程时应使用 Node.js 的 `db.prepare()` API 和参数。

#### sqlite3 CLI（仅用于手动检查）

--- 

> **不要** 直接在 SQL 语句中嵌入 shell 变量（例如 `WHERE project_id = '$SLUG'`）。这种写法容易导致 SQL 注入攻击。应使用 Node.js API 和参数。

#### Node.js API — 参数化查询（编程使用时必需）

--- 

### CLI 快速参考

--- 

### Apple 注释导出（可选 — 仅限 macOS）

TaskFlow 可以根据当前项目状态维护一个实时的 Apple 注释。注释会以富格式 HTML 的形式显示，并通过 AppleScript 生成。

--- 

在首次运行时（或在 `taskflow setup` 期间），系统会在配置的文件夹中创建一个新的注释，并将其 Core Data ID 保存到：

--- 

配置文件结构：

--- 

**重要提示 — **切勿删除共享的注释。** 注释总是就地编辑的。删除并重新创建注释会导致 Core Data ID 更改，从而破坏现有的共享链接。如果注释被意外删除，`taskflow notes` 会自动创建一个新的注释并更新配置。

为了实现每小时自动更新，可以添加一个 cron 任务：

--- 

或者安装一个专门的 LaunchAgent（macOS），设置 `apple-notes-export.mjs` 的 `StartInterval` 为 3600 秒。

此功能完全是可选的，且仅适用于 macOS。在其他平台上，`taskflow notes` 会优雅地退出并显示相应的提示信息。

---

## 内存集成规则

这些规则有助于保持每日内存日志的整洁，并防止数据重复。

### ✅ 应该做的操作

- 在完成或推进工作时，在每日内存日志中引用任务 ID：
  --- 

- 保留内存记录的详细内容 — 包括发生了什么、你的决策以及下一步计划。

### 不应该做的操作

- **切勿在每日内存文件中重复记录待办任务。** `tasks/<slug>-tasks.md` 是所有待办任务的唯一来源。内存文件不应列出尚未完成的任务。
- 不要在内存中记录任务状态的变化（例如，“Task 007 现在正在进行中”）。只需记录有意义的进度事件或决策。
- 不要在内存文件中创建新的任务。应直接将任务添加到任务文件中。

### 加载项目上下文的步骤

在开始涉及某个项目的会话时：

1. `cat PROJECTS.md` — 确定项目标识符和状态
2. `cat tasks/<slug>-tasks.md` — 加载当前任务的状态
3. `cat plans/<slug>-plan.md` — 加载项目架构信息（如果存在）
4. 开始工作。在会话结束时将任务 ID 信息记录在内存中。

---

## 定期同步守护进程

同步守护进程会每 **60 秒** 在后台运行 `task-sync.mjs files-to-db` 命令。这意味着 markdown 的更改会在一分钟内自动反映到 SQLite 中。

- 日志：`logs/taskflow-sync.stdout.log` 和 `logs/taskflow-sync.stderr.log`（相对于工作空间路径）
- 锁定：`sync_state` 表中的 Advisory TTL 锁防止同时进行同步
- 冲突解决：按照最后写入的时间顺序来确定同步结果

### 最快的安装方式（自动检测操作系统）

--- 

系统会自动检测你的操作系统并安装相应的组件。在 macOS 上，它会安装并启动 LaunchAgent；在 Linux 上，它会配置 systemd 用户单元并启用定时器。

### macOS — LaunchAgent（手动步骤）

模板文件：`taskflow/system/com.taskflow.sync.plist.xml`

1. 将 `taskflow/system/com.taskflow.sync.plist.xml` 复制到 `~/Library/LaunchAgents/com.taskflow.sync.plist`
2. 将 `{{workspace}}` 替换为你的工作空间的绝对路径（不要在路径末尾加斜杠）
3. 将 `{{node}}` 替换为你的 `node` 可执行文件的路径（使用 `which node` 命令找到）
4. 启动守护进程：`launchctl load ~/Library/LaunchAgents/com.taskflow.sync.plist`
5. 验证安装结果：`launchctl list | grep taskflow`

### Linux — systemd 用户定时器（手动步骤）

模板文件：`taskflow/system/taskflow-sync.service` 和 `taskflow/system/taskflow-sync.timer`

--- 

验证安装结果：
--- 

卸载程序：
--- 

> **注意：** systemd 用户单元需要登录会话才能运行。如果需要在没有交互式会话的环境中运行它们（例如在服务器上），可以使用 `loginctl enable-linger $USER` 来启用定时器。

---

## 部分标题与数据库状态的对应关系

| Markdown 标题 | 数据库中的状态值 |
|---|---|
| `## In Progress` | `in_progress` |
| `## Pending Validation` | `pending_validation` |
| `## Backlog` | `backlog` |
| `## Blocked` | `blocked` |
| `## Done` | `done` |

**部分标题是固定的。** 不要更改它们的名称。同步解析器会严格按照这些字符串进行匹配。**

---

## 已知的特殊行为

- **`MAX(id)` 是按字典顺序处理的。** 由于任务 ID 是文本格式的，`SELECT MAX(id)` 只能正常工作是因为 ID 会被自动填充为三位数（例如 `-001`、`-002`）。如果使用 `-1` 代替 `-001`，顺序会混乱。请始终将 ID 填充为三位数。
- **复选框的状态只是为了美观。** 任务的状态由它所在的 `##` 部分决定，而不是由复选框的状态（`[x]` 或 `[ ]`）决定。同步引擎在读取时不会考虑复选框的状态。在写入时，已完成的任务会被标记为 `[x]`，其他状态则标记为 `[ ]`。
- **注释在删除后仍然保留。** 如果从 Markdown 中删除 `- note:` 行，注释仍然会保留在数据库中（因为 COALESCE 规则）。这是版本 1 的设计意图——注释是单向显示的。如果要彻底删除注释，需要直接更新数据库。
- **锁的过期时间为 60 秒。** 如果同步过程中出现错误导致锁未释放，下一次同步会被延迟最多 60 秒。`SIGTERM/SIGINT` 信号可以尝试清除锁，但 `kill -9` 命令可能无法立即解除锁定。**
- **自动创建项目名称时使用 `slug`。** 如果同步过程中找不到匹配的 `projects` 行，系统会使用 `slug` 生成一个默认名称（例如 “My Project”）。如果你需要自定义项目名称，请在 `PROJECTS.md` 中进行修改并重新同步。
- **标签顺序必须正确。** `[P1] [codex]` 的顺序是正确的。`[codex] [P1]` 会导致优先级标签被错误地解析为 `codex`。**

## 已知的限制（版本 1）

- 注释是单向的（从 Markdown 到数据库）。在 Markdown 中删除注释不会自动清除数据库中的记录。
- `db-to-files` 命令会重写所有项目任务文件，即使文件内容没有变化。
- 每个项目只对应一个任务文件（1:1 的映射关系）。多任务文件的功能将在后续版本中实现。
- 支持 macOS（LaunchAgent）和 Linux（systemd 定时器）的定期同步。可以使用 `taskflow install-daemon` 命令来安装相关组件。
- 需要 Node.js 22.5 或更高版本（`node:sqlite`）。版本 1 不支持使用 Python。

---

## 快速参考

---