---
name: prose
description: OpenProse 虚拟机技能包：可以通过任何 `prose` 命令、`.prose` 文件或 OpenProse 相关的引用进行激活；该技能包能够协调和管理多代理（multi-agent）的工作流程。
metadata: {"moltbot":{"emoji":"🪶","homepage":"https://www.prose.md"}}
---

# OpenProse 技能

OpenProse 是一种用于 AI 会话的编程语言。大型语言模型（LLMs）本质上是模拟器——当给定详细的系统描述时，它们不仅仅是描述系统，而是真正地模拟系统。`prose.md` 规范描述了一台虚拟机，其细节足够真实，以至于读取该规范的 Prose Complete 系统会“变成”这台虚拟机。具有足够真实性的模拟就等同于实现了该系统。**你本身就是 Prose Complete 系统。**

## Moltbot 运行时映射

- **上游规范中的任务工具** 对应 Moltbot 的 `sessions_spawn` 功能
- **文件 I/O** 对应 Moltbot 的 `read`/`write` 操作
- **远程获取数据** 对应 Moltbot 的 `web_fetch` 方法（或在需要 POST 请求时使用 `exec` 和 curl）

## 何时激活此技能

在以下情况下激活此技能：

- 用户使用任何 `prose` 命令（例如：`prose boot`、`prose run`、`prose compile`、`prose update`、`prose help` 等）
- 用户请求运行一个 `.prose` 文件
- 用户提到“OpenProse”或“prose program”
- 用户希望从脚本中协调多个 AI 代理
- 用户拥有格式为 `session "..."` 或 `agent name:` 的文件
- 用户希望创建可重用的工作流程

## 命令路由

当用户调用 `prose <command>` 时，系统会根据用户的意图智能地路由命令：

| 命令 | 操作 |
|---------|--------|
| `prose help` | 加载 `help.md`，指导用户所需操作 |
| `prose run <file>` | 加载虚拟机配置（`prose.md` 和状态后端数据），然后执行程序 |
| `prose run handle/slug` | 从注册表中获取相关信息，然后执行（详见“远程程序”部分） |
| `prose compile <file>` | 加载 `compiler.md`，验证程序代码 |
| `prose update` | 运行迁移操作（详见“迁移”部分） |
| `prose examples` | 显示或运行 `examples/` 目录中的示例程序 |
| 其他命令 | 根据上下文智能解析命令 |

### 重要提示：**只有一个技能**

系统中只有一个技能，即 `open-prose`。不存在 `prose-run`、`prose-compile` 或 `prose-boot` 等独立技能。所有 `prose` 命令都通过这个单一技能来处理。

### 解析示例引用

示例程序存储在 `examples/` 目录中（与当前文件位于同一目录）。当用户通过名称引用示例程序时（例如：“运行 gastown 示例”）：

1. 读取 `examples/` 目录以列出可用文件
2. 根据文件名的一部分、关键词或编号来匹配文件
3. 使用命令 `prose run examples/28-gas-town.prose` 来运行相应的程序

**常见示例关键词：**
| 关键词 | 对应文件 |
|---------|------|
| hello, hello world | `examples/01-hello-world.prose` |
| gas town, gastown | `examples/28-gas-town.prose` |
| captain, chair | `examples/29-captains-chair.prose` |
| forge, browser | `examples/37-the-forge.prose` |
| parallel | `examples/16-parallel-reviews.prose` |
| pipeline | `examples/21-pipeline-operations.prose` |
| error, retry | `examples/22-error-handling.prose` |

### 远程程序

你可以通过 URL 或注册表引用来运行任何 `.prose` 程序：

```bash
# Direct URL — any fetchable URL works
prose run https://raw.githubusercontent.com/openprose/prose/main/skills/open-prose/examples/48-habit-miner.prose

# Registry shorthand — handle/slug resolves to p.prose.md
prose run irl-danb/habit-miner
prose run alice/code-review
```

**解析规则：**

| 输入        | 解析方式                |
|-------------|----------------------|
| 以 `http://` 或 `https://` 开头 | 直接从 URL 获取文件内容 |
| 包含 `/` 但没有协议 | 解析为 `https://p.prose.md/{path}` |
| 其他情况     | 视为本地文件路径           |

**远程程序的执行步骤：**

1. 应用上述解析规则
2. 获取 `.prose` 文件的内容
3. 加载虚拟机配置并正常执行程序

这些规则同样适用于 `.prose` 文件中的 `use` 语句：

```prose
use "https://example.com/my-program.prose"  # Direct URL
use "alice/research" as research             # Registry shorthand
```

---

## 文件位置

**请勿在用户的工作空间中搜索 OpenProse 的文档文件。** 所有技能相关的文件都与此 `SKILL.md` 文件位于同一目录下：

| 文件名                | 所在位置                    | 用途                                   |
| ------------------------- | --------------------------- | ----------------------------------------- |
| `prose.md`                | 与当前文件位于同一目录          | 虚拟机配置文件（用于加载和执行程序）       |
| `help.md`                 | 与当前文件位于同一目录          | 帮助文档、常见问题解答、入门指南（用于 `prose help` 命令） |
| `state/filesystem.md`     | 与当前文件位于同一目录          | 基于文件的状态管理（默认配置）         |
| `state/in-context.md`     | 与当前文件位于同一目录          | 基于上下文的状态管理（按需加载）             |
| `state/sqlite.md`         | 与当前文件位于同一目录          | SQLite 数据库状态（实验性，按需加载）         |
| `state/postgres.md`       | 与当前文件位于同一目录          | PostgreSQL 数据库状态（实验性，按需加载）         |
| `compiler.md`             | 与当前文件位于同一目录          | 编译器/验证工具（仅按需加载）         |
| `guidance/patterns.md`    | 与当前文件位于同一目录          | 编写 `.prose` 文件时的最佳实践         |
| `guidance/antipatterns.md` | 与当前文件位于同一目录          | 编写 `.prose` 文件时应避免的错误         |
| `examples/`               | 与当前文件位于同一目录          | 包含 37 个示例程序                         |

**用户的工作空间文件**（这些文件位于用户的项目目录中）：

| 文件/目录           | 所在位置                 | 用途                             |
| ---------------- | ------------------------ | ----------------------------------- |
| `.prose/.env`    | 用户的工作目录             | 配置文件（键值对格式）                   |
| `.prose/runs/`   | 用户的工作目录             | 基于文件的运行时状态管理文件             |
| `.prose/agents/` | 用户的工作目录             | 项目级别的持久化代理程序                   |
| `*.prose` 文件          | 用户的项目目录             | 用户创建的程序文件                         |

**用户级别的文件**（位于用户的主目录中，可在所有项目中共享）：

| 文件/目录           | 所在位置                 | 用途                             |
| ~/.prose/agents/          | 用户的主目录             | 用户级别的持久化代理程序（跨项目使用）           |

当你需要读取 `prose.md` 或 `compiler.md` 时，请从与 `SKILL.md` 文件相同的目录中查找这些文件。切勿在用户的工作空间中搜索这些文件。

---

## 核心文档

| 文件名                | 用途                          | 何时加载                          |
| --------------------- | ------------------------------ | ---------------------------------------------- |
| `prose.md`            | 虚拟机配置文件            | 始终加载以执行程序                     |
| `state/filesystem.md`     | 基于文件的状态管理文件         | 默认情况下与虚拟机一起加载                   |
| `state/in-context.md`     | 基于上下文的状态管理文件         | 仅当用户请求 `--in-context` 时加载                 |
| `state/sqlite.md`         | SQLite 数据库状态文件         | 仅当用户请求 `--state=sqlite` 时加载（需要 sqlite3 CLI）     |
| `state/postgres.md`       | PostgreSQL 数据库状态文件         | 仅当用户请求 `--state=postgres` 时加载（需要 psql 和 PostgreSQL）     |
| `compiler.md`         | 编译器/验证工具文件         | 仅当用户请求编译或验证时加载                   |
| `guidance/patterns.md`    | 编写 `.prose` 文件时的最佳实践         | 编写新文件时加载                         |
| `guidance/antipatterns.md` | 编写 `.prose` 文件时应避免的错误         | 编写新文件时加载                         |

### 编写指南

当用户要求你**编写或创建**新的 `.prose` 文件时，请参考以下指导文件：
- `guidance/patterns.md` — 提供编写健壮、高效程序的实用模式
- `guidance/antipatterns.md` — 列出常见的错误和避免方式

**注意：** 在运行或编译程序时** **不要** 加载这些指导文件，因为它们仅用于编写过程。

### 状态管理方式

OpenProse 支持三种状态管理方式：

| 状态管理方式 | 使用场景                | 状态存储位置                         |
|------------|------------------|--------------------------------------|
| **filesystem**（默认） | 复杂程序、需要恢复状态、调试时使用       | `.prose/runs/{id}/` 文件           |
| **in-context** | 简单程序（少于 30 条指令）、无需持久化状态时使用 | 对话历史记录                         |
| **sqlite**（实验性） | 支持查询、原子事务和灵活的数据库结构       | `.prose/runs/{id}/state.db`                 |
| **postgres**（实验性） | 支持并发写入、外部集成和团队协作       | PostgreSQL 数据库                         |

**默认行为：** 在加载 `prose.md` 时，同时加载 `state/filesystem.md`。这对大多数程序来说是推荐的方式。

**切换状态管理方式：** 如果用户请求使用基于上下文的状态管理（`--in-context`），则加载 `state/in-context.md`。

**实验性的 SQLite 模式：** 如果用户指定 `--state=sqlite` 或请求使用 SQLite 状态管理方式，则加载 `state/sqlite.md`。此模式需要安装 `sqlite3` CLI（macOS 上已预装，Linux/Windows 上可通过包管理器安装）。如果 `sqlite3` 无法使用，需警告用户并切换回基于文件系统的状态管理方式。

**实验性的 PostgreSQL 模式：** 如果用户指定 `--state=postgres` 或请求使用 PostgreSQL 状态管理方式：

**⚠️ 安全提示：** `OPENPROSE_POSTGRES_URL` 中的数据库凭据会传递给子代理会话，并会显示在日志中。建议用户使用权限受限的专用数据库。请参阅 `state/postgres.md` 以获取安全配置指南。**

1. **首先检查连接配置：**
   ```bash
   # Check .prose/.env for OPENPROSE_POSTGRES_URL
   cat .prose/.env 2>/dev/null | grep OPENPROSE_POSTGRES_URL
   # Or check environment variable
   echo $OPENPROSE_POSTGRES_URL
   ```

2. **如果连接字符串存在，验证连接是否成功：**
   ```bash
   psql "$OPENPROSE_POSTGRES_URL" -c "SELECT 1" 2>&1
   ```

3. **如果配置缺失或连接失败，提醒用户：**
   ```
   ⚠️  PostgreSQL state requires a connection URL.

   To configure:
   1. Set up a PostgreSQL database (Docker, local, or cloud)
   2. Add connection string to .prose/.env:

      echo "OPENPROSE_POSTGRES_URL=postgresql://user:pass@localhost:5432/prose" >> .prose/.env

   Quick Docker setup:
      docker run -d --name prose-pg -e POSTGRES_DB=prose -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 postgres:16
      echo "OPENPROSE_POSTGRES_URL=postgresql://postgres@localhost:5432/prose" >> .prose/.env

   See state/postgres.md for detailed setup options.
   ```

4. **只有在连接成功后，才加载 `state/postgres.md`**

此模式需要 `psql` CLI 和运行中的 PostgreSQL 服务器。如果其中任何一个不可用，需警告用户并建议切换回基于文件系统的状态管理方式。

**注意事项：** `compiler.md` 文件体积较大。仅在用户明确请求编译或验证时才加载它。编译完成后，建议用户使用 `/compact` 命令或创建新会话后再执行程序——避免同时加载这两个文档。

## 示例程序

`examples/` 目录包含 37 个示例程序：

- **01-08**：基础示例（hello world、研究、代码审查、调试）
- **09-12**：代理和技能相关示例
- **13-15**：变量和组合逻辑示例
- **16-19**：并行执行示例
- **20-21**：循环和管道处理示例
- **22-23**：错误处理示例
- **24-27**：高级功能示例（条件判断、代码块、插值操作）
- **28**：Gas Town（多代理协调示例）
- **29-31**：Captain’s Chair 模式（持久化代理协调器）
- **33-36**：生产流程示例（自动修复代码、内容推送、特性生成、错误排查）
- **37**：The Forge（从零开始构建浏览器）

可以从 `01-hello-world.prose` 开始学习，或尝试 `37-the-forge.prose` 来观看 AI 如何构建一个网页浏览器。

## 执行流程

首次在会话中调用 OpenProse 虚拟机时，会显示以下提示信息：

```
┌─────────────────────────────────────┐
│         ◇ OpenProse VM ◇            │
│       A new kind of computer        │
└─────────────────────────────────────┘
```

要执行一个 `.prose` 文件，你需要成为 OpenProse 虚拟机：

1. **读取 `prose.md` 文件** — 该文件定义了虚拟机的运行规则
2. **你本身就是虚拟机** — 你的对话内容构成了虚拟机的内存，你的操作指令决定了虚拟机的行为
3. **创建会话** — 每条 `session` 语句都会触发相应的任务执行
4. **记录执行过程** — 使用特定的协议来跟踪程序的执行状态（如 [Position]、[Binding]、[Success] 等）
5. **智能判断执行结果** — 文件中的 `**...** 标记需要你根据实际情况进行判断

## 帮助与常见问题解答

有关语法参考、常见问题解答以及使用指南，请加载 `help.md` 文件。

---

## 迁移（`prose update`）

当用户执行 `prose update` 命令时，系统会检查旧版本的文件结构，并将其迁移到当前格式：

### 需要检查的旧文件路径

| 旧文件路径         | 新文件路径                | 备注                                      |
|-----------------|------------------|-----------------------------------------|
| `.prose/state.json`    | `.prose/.env`            | 将 JSON 格式转换为键值对格式                   |
| `.prose/execution/`    | `.prose/runs/`            | 重命名目录                              |

### 迁移步骤

1. **检查 `.prose/state.json` 文件**：
   - 如果存在，读取其内容并将其转换为 `.env` 格式
   - 将转换后的内容写入 `.prose/.env` 文件
   - 删除 `.prose/state.json` 文件

2. **检查 `.prose/execution/` 目录**：
   - 如果存在，将其重命名为 `.prose/runs/`
   - 注意：运行目录的内部结构可能已发生变化，因此需要手动迁移每个运行时的状态数据

3. **如果缺少 `.prose/agents/` 目录**，则创建该目录
   - 该目录用于存储项目级别的持久化代理程序

### 迁移结果

```
🔄 Migrating OpenProse workspace...
  ✓ Converted .prose/state.json → .prose/.env
  ✓ Renamed .prose/execution/ → .prose/runs/
  ✓ Created .prose/agents/
✅ Migration complete. Your workspace is up to date.
```

如果未找到旧版本文件：
```
✅ Workspace already up to date. No migration needed.
```

### 技能文件名称的变更（供维护人员参考）

这些文档文件的名称在技能文件本身中已更新（用户的工作空间中无需更改）：

| 旧文件名       | 新文件名                   |
|--------------|------------------|-----------------------------------------|
| `docs.md`      | `compiler.md`                |                          |
| `patterns.md`      | `guidance/patterns.md`                |                          |
| `antipatterns.md`      | `guidance/antipatterns.md`                |                          |

如果在用户提示或外部文档中遇到旧文件名，请将其映射到新的文件路径。