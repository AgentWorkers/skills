---
name: coding-lead
description: 这是一种智能编码技巧，能够根据任务的复杂程度来分配处理任务的方式：简单任务直接由系统处理；中等或复杂任务则通过ACP（Automated Code Processing）机制进行处理，并具备自动回退功能。当qmd和smart-agent-memory可用时，该技巧会与这些工具进行集成。在基础配置中，系统仅使用纯代理工具（pure agent tools）来完成任务。
---
# 编码负责人

> 本技能优先于代理 SOUL.md 文件中的内联编码规则。

根据任务的复杂性来选择执行路径。如果 ACP 失败，则自动回退到直接执行。

## 任务分类

| 级别 | 判断标准 | 操作 |
|-------|----------|--------|
| **简单** | 单个文件，少于 60 行 | 直接执行：读取/写入/编辑/执行 |
| **中等** | 2-5 个文件，范围明确 | 使用 ACP → 回退到直接执行 |
| **复杂** | 涉及架构或多个模块 | 先制定计划 → 使用 ACP → 回退到分块直接执行 |

如有疑问，选择更高级别的执行方式。

## 技术栈（新项目）

| 层次 | 首选技术 | 备选技术 |
|-------|-----------|----------|
| 后端 | PHP (Laravel/ThinkPHP) | Python |
| 前端 | Vue.js | React |
| 移动端 | Flutter | UniApp-X |
| CSS | Tailwind | - |
| 数据库 | MySQL | PostgreSQL |

现有项目：遵循当前的技术栈。新项目：先提出建议，等待确认。

## 工具检测与回退策略

所有工具均为**可选**。每个会话仅检测一次：

| 工具 | 是否可用？ | 备选方案 |
|------|-----------|----------|
| **smart-agent-memory** | `node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js stats` 的结果是否正常？ | 使用 `memory_search` 并手动写入 `.md` 文件 |
| **qmd** | `qmd --version` 的结果是否正常？ | 在 Linux/macOS 上使用 `grep`；在 Windows 上使用 `Select-String` 或 `find` |
| **ACP** | `sessions_spawn` 是否成功执行？ | 直接执行读取/写入/编辑/执行 |

注释说明：`[memory]` `[qmd]` `[acp]` 表示如果工具可用则使用该工具，否则使用备选方案。

## ACP 代理路由

**ACP 访问**：`sessions_spawn(runtime="acp")` 可能因平台限制而不可用。在这种情况下，请使用 **acpx CLI** 作为可靠的执行路径：

```bash
# One-shot execution via acpx (works from any session type)
cmd /c "C:\Users\beyou\AppData\Roaming\npm\node_modules\openclaw\extensions\acpx\node_modules\.bin\acpx.cmd --verbose --agent \"node C:/Users/beyou/AppData/Roaming/npm/node_modules/@zed-industries/claude-agent-acp/dist/index.js\" exec \"<your prompt>\" 2>&1"
```

如果当前会话中 `sessions_spawn(runtime="acp")` 可用，请使用它；否则通过 `exec` 命令回退到 acpx CLI。

请查看 `openclaw.json` 中的 `acp.allowedAgents` 以确定可用的代理：

| 任务类型 | 最佳代理 | 原因 |
|-----------|-----------|-----|
| 复杂的后端开发、多文件重构、深度推理 | **claude** | 具备出色的跨文件推理能力，能处理大量上下文信息 |
| 快速迭代、自主探索、沙箱任务 | **codex** | 执行速度快，具备自主处理能力，适合迭代性任务 |
| 代码审查 | 使用与编写代码的代理不同的代理 | 可避免因使用相同代理而产生的偏见 |

### 如何进行任务路由

```
# Default (uses acp.defaultAgent, typically "claude"):
sessions_spawn(runtime: "acp", task: <prompt>, cwd: <dir>)

# Explicit agent:
sessions_spawn(runtime: "acp", agentId: "claude", task: <prompt>, cwd: <dir>)
sessions_spawn(runtime: "acp", agentId: "codex", task: <prompt>, cwd: <dir>)
```

### 回退策略
1. 尝试首选代理 → 2. 尝试备用代理 → 3. 直接执行

如果某个代理失败或不可用，先尝试其他代理，再回退到直接执行。

### 使用多个代理并行处理任务（最多支持 2 个并行任务）

```
Session 1: claude → backend refactor (needs deep reasoning)
Session 2: codex → frontend fixes (needs fast iteration)
```

## 编码规范 — 两级规范，避免重复

### 第一层：项目级规范（由 Claude Code 负责维护）
项目可以有自己的 `CLAUDE.md`、`.cursorrules` 和 `docs/` 文件，这些文件由 Claude Code 自动读取。**请勿将项目级规范复制到 ACP 提示中**。

### 第二层：团队级规范（由 OpenClaw 负责维护）
`shared/knowledge/tech-standards.md` 包含跨项目的规范（如安全规范、变更控制规则、技术栈偏好设置），仅适用于**无需使用 ACP 的简单任务**。

### 启动 ACP 时需要注意的事项
- **不要** 将编码规范直接嵌入到提示信息中 — Claude Code 有自己的 `CLAUE.md` 文件
- **必须** 包含：任务描述、验收标准、相关上下文信息（文件路径、决策内容）
- **如有必要**，还需包含任务特定的约束条件（例如：“不得修改 API 接口规范”）

### 直接执行任务时的注意事项
- 每个会话都会加载规范，优先使用以下规范：
  1. `shared/knowledge/tech-standards.md`（团队级规范，如果存在）
  2. 内置的默认规范（如果上述规范不存在）

### 内置的默认规范（用于直接执行时的回退依据）
- 遵循 KISS、SOLID 和 DRY 原则，在修改代码前进行充分研究
- 方法长度不超过 200 行，遵循现有的架构设计
- 不要使用硬编码的敏感信息，尽量减少代码修改范围，确保提交日志清晰明了
- 数据库修改需通过 SQL 脚本完成，引入新技术前需获得确认

## 简单任务的处理流程
1. 读取目标文件（相关规范已在上一步中加载）
2. [memory] 查阅相关的决策记录
3. 使用读取/写入/编辑/执行命令完成任务
4. [memory] 记录修改的内容及原因

## 中等/复杂任务的处理流程

### 第一步：创建上下文文件
将任务相关信息写入 `<project>/.openclaw/context-<task-id>.md` 文件中（ACP 会从磁盘读取该文件，而不是从提示信息中获取）：

```bash
# [qmd] or grep: find relevant code
# [memory] recall + lessons: find past decisions
# Standards already loaded (see "Coding Standards Loading" above)
# Write context file with 3-5 key rules from loaded standards — do NOT paste full file
```

上下文文件的基本结构如下：
```markdown
# Task Context: <id>
## Project — path, stack, architecture style
## Relevant Code — file paths + brief descriptions from qmd/grep
## History — past decisions/lessons from memory (if any)
## Constraints — task-specific rules only (NOT general coding standards — Claude Code has CLAUDE.md)
```

完整的模板及示例请参见 [references/prompt-templates.md](references/prompt-templates.md)。

### 第二步：编写简洁的提示信息

```
Project: <path> | Stack: <e.g. Laravel 10 + React 18 + TS>
Context file: .openclaw/context-<task-id>.md (read it first if it exists)

## Task
<description>

## Acceptance Criteria
- [ ] <criteria>
- [ ] Tests pass, no unrelated changes, clean code

Before finishing: run linter + tests, include results.
When done: openclaw system event --text "Done: <summary>" --mode now
```

### 第三步：启动任务执行

```
# Option A: sessions_spawn (if available in your session)
sessions_spawn(runtime: "acp", task: <prompt>, cwd: <project-dir>, mode: "run")

# Option B: acpx CLI (always works)
exec: acpx --agent "node C:/Users/beyou/AppData/Roaming/npm/node_modules/@zed-industries/claude-agent-acp/dist/index.js" exec "<prompt>"
# Set cwd to project dir in exec command
```

### 回退策略
- 如果任务启动失败或超时 → 直接执行任务
- 如果输出为空或文件内容没有变化 → 直接执行任务
- 如果任务仅部分完成 → 由代理完成剩余的工作

回退策略：[memory] 记录失败原因 → 由代理直接执行任务 → 向用户报告失败情况。

**切勿默默失败。** 必须完成任务或说明失败原因。

### 第四步：验证与记录
1. 检查任务是否达到验收标准，并运行相应的测试
2. [memory] 记录修改的内容、所做的决策以及经验教训
3. 清理上下文文件

## 复杂任务的处理流程
请参考 [references/complex-tasks.md](references/complex-tasks.md)（仅适用于复杂任务）——包括角色分配、质量保证流程、并行处理策略以及任务执行的整个流程（RESEARCH→PLAN→EXECUTE→REVIEW）。

## 提高效率的技巧（节省代码执行所需的令牌）
- **将上下文信息存储在磁盘上的文件中**，而非嵌入到提示信息中 → 每次执行任务时可节省约 90% 的令牌资源
- **并行处理**：使用一个上下文文件，多个 ACP 会话可以共享该文件
- **串行处理**：使用 `mode: "session"` 和 `sessions_send` 命令进行后续操作
- **使用 [qmd]** 进行精确搜索 → 只提取上下文文件中的相关内容
- **不要在 ACP 提示中包含通用规范**：Claude Code 会读取自己的 `CLAUE.md` 和 `.cursorrules` 文件，避免重复规定
- **ACP 提示信息应保持简洁**：仅包含任务内容、验收标准和上下文文件路径
- **直接执行任务时**：每个会话都加载团队规定的规范，而不是针对每个任务单独加载

## 内存管理机制
- **执行任务前**：从内存中检索相关的任务信息和经验教训
- **执行任务后**：记录修改的内容、所做的决策以及获得的经验教训
- **跨会话数据共享**：代理会在不同会话间保留这些信息；Claude Code 无法实现这一点，这是该机制的核心优势

## 多项目并行处理
- 每个项目都有自己的上下文文件（存储在 `.openclaw/` 目录下）
- 每个项目使用不同的工作目录（`cwd`）以避免数据混淆
- 为每个项目的上下文文件添加标签：`--tags code,<project-name>`
- **最多支持 2 个并行 ACP 会话**，以确保令牌和资源的使用更加合理
- ACP 会在后台运行，而代理则直接执行简单任务

有关多项目并行处理的详细示例，请参见 [references/prompt-templates.md](references/prompt-templates.md)。

## 智能重试机制（最多尝试 3 次）
1. 分析失败原因 → 2. 调整提示信息 → 3. 优化重试策略 → 4. 最多尝试 3 次，若仍失败则报告失败原因

## 进度更新
- 任务开始时发送一条简短的消息
- 出现错误时立即报告
- 任务完成后发送总结信息
- 如果需要回退，需说明原因

## 安全注意事项
- **切勿在 `~/.openclaw/**` 目录中启动任务执行** — 避免代码代理损坏配置文件
- **始终将工作目录（`cwd`）设置为项目目录**
- 在提交代码前进行仔细检查，尤其是处理复杂任务时
- 如果会话运行异常（如超时或输出结果无意义），请及时终止该会话

## 相关参考资料
- [references/complex-tasks.md](references/complex-tasks.md) — 适用于复杂任务的详细处理流程，包括角色分配、质量保证机制和并行处理策略
- [references/prompt-templates.md](references/prompt-templates.md) — 提示信息的模板和示例