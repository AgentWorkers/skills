---
name: coding-lead
description: 这是一种智能编码技术，能够根据任务的复杂程度来分配处理任务的方式：简单任务直接由系统处理；中等或复杂任务则通过ACP（Automatic Task Routing）机制进行分配，并具备自动回退功能。当qmd和smart-agent-memory工具可用时，该技术会与它们进行集成。在基础配置中，系统仅使用纯代理工具（pure agent tools）来完成任务处理。
---
# 编码负责人

> 本技能优先于代理 SOUL.md 文件中的内联编码规则。

任务路由依据复杂度进行分配。如果 ACP 失败，则自动切换为直接执行。

## 任务分类

| 级别 | 判断标准 | 操作 |
|-------|----------|--------|
| **简单** | 单个文件，少于 60 行 | 直接操作：读取/写入/编辑/执行 |
| **中等** | 2-5 个文件，范围明确 | 使用 ACP → 自动切换为直接执行 |
| **复杂** | 涉及架构或多个模块 | 先制定计划 → 使用 ACP → 如仍失败则切换为分块直接执行 |

如有疑问，应提升一个处理级别。

## 技术栈（新项目）

| 层次 | 首选技术 | 备选技术 |
|-------|-----------|----------|
| 后端 | PHP（Laravel/ThinkPHP） | Python |
| 前端 | Vue.js | React |
| 移动端 | Flutter | UniApp-X |
| CSS | Tailwind | - |
| 数据库 | MySQL | PostgreSQL |

现有项目：遵循当前的技术栈。新项目：先提出方案，等待确认。

## 工具检测与备用方案

所有工具均为**可选**。每个会话仅检测一次：

| 工具 | 是否可用？ | 备用方案 |
|------|-----------|----------|
| **smart-agent-memory** | `node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js stats` 的输出是否正常？ | 使用 `memory_search` 并手动写入 `.md` 文件 |
| **qmd** | `qmd --version` 的输出是否正常？ | 在 Linux/macOS 上使用 `grep`；在 Windows 上使用 `Select-String` 或 `find` |
| **ACP** | `sessions_spawn` 是否成功执行？ | 直接进行读取/写入/编辑/执行 |

注释说明：`[memory]` 表示“如果可用则使用该工具，否则使用备用方案”。

## ACP 代理路由

当配置了多个编码代理时（请查看 `openclaw.json` 中的 `acp.allowedAgents`）：

| 任务类型 | 最适合的代理 | 原因 |
|-----------|-----------|-----|
| 复杂的后端开发、多文件重构、深度推理 | **claude-code** | 具备出色的跨文件推理能力，能处理大量上下文信息 |
| 快速迭代、自主探索、沙箱任务 | **codex** | 执行速度快，能够自主完成任务，适合迭代性修复 |
| 代码审查 | 使用与编写代码的代理不同的代理 | 可以避免偏见导致的遗漏 |

### 路由流程

```
# Default (uses acp.defaultAgent):
sessions_spawn(runtime: "acp", task: <prompt>, cwd: <dir>)

# Explicit agent:
sessions_spawn(runtime: "acp", agentId: "claude-code", task: <prompt>, cwd: <dir>)
sessions_spawn(runtime: "acp", agentId: "codex", task: <prompt>, cwd: <dir>)
```

### 备用方案流程
1. 尝试首选代理 → 2. 尝试备用代理 → 3. 直接执行

如果某个代理失败或不可用，先尝试其他代理，再切换为直接执行。

### 使用不同代理并行处理复杂任务
对于复杂任务，可以在不同的子任务上同时启动两个代理：
```
Session 1: claude-code → backend refactor (needs deep reasoning)
Session 2: codex → frontend fixes (needs fast iteration)
```

## 简单任务

1. 读取目标文件及编码规范（CLAUDE.md、tech-standards.md、.cursorrules）
2. 从内存中检索相关决策
3. 执行读取/写入/编辑/操作
4. 记录变更内容及原因

## 中等/复杂任务

### 第一步：创建上下文文件

将结果写入 `<project>/.openclaw/context-<task-id>.md` 文件（ACP 从磁盘读取文件，而不是从命令行读取）：

```bash
# [qmd] or grep: find relevant code
# [memory] recall + lessons: find past decisions
# Read project standards (CLAUDE.md, tech-standards.md, .cursorrules)
# Write context file with sections below
```

上下文文件的基本结构：
```markdown
# Task Context: <id>
## Project — path, stack, architecture style
## Standards — key coding rules (3-5 bullets)
## Relevant Code — file paths + brief descriptions from qmd/grep
## History — past decisions/lessons from memory (if any)
```

完整模板及示例请参见 [references/prompt-templates.md](references/prompt-templates.md)

### 第二步：生成提示信息

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

### 第三步：启动代理

```
sessions_spawn(runtime: "acp", task: <prompt>, cwd: <project-dir>, mode: "run")
```

### 第四步：检测是否需要备用方案

| 条件 | 操作 |
|-----------|--------|
| 启动代理失败/超时 | → 直接执行 |
| 输出为空/文件未发生变更 | → 直接执行 |
| 任务仅部分完成 | → 由代理完成剩余部分 |

备用方案：将失败信息记录到内存中 → 由代理直接执行任务 → 向用户报告结果。

**切勿默默失败。** 必须完成任务或说明失败原因。

### 第五步：验证与记录

1. 检查任务完成标准并运行测试
2. 记录变更内容、所做的决策及经验教训
3. 清理上下文文件

## 复杂任务

请仅针对**复杂任务** 参考 [references/complex-tasks.md]——包括角色分配、质量保证（QA）机制、并行处理策略以及任务流程（RESEARCH→PLAN→EXECUTE→REVIEW）。

## 上下文重用（节省令牌）

- **将上下文文件保存在磁盘上**，而非嵌入到提示信息中 → 每次启动任务时可节省约 90% 的令牌资源
- **并行处理**：一个上下文文件可供多个 ACP 会话使用
- **串行处理**：使用 `mode: "session"` 和 `sessions_send` 进行后续操作
- **[qmd]**：进行精确搜索，仅提取上下文文件中的相关内容

## 内存整合

- **使用 [memory] 功能**：在开始任务前检索相关信息和经验教训；任务完成后记录变更内容、决策及收获的教训。
- **跨会话存储**：代理会记住之前的上下文信息；Claude Code 无法实现这一点，这是该功能的核心优势。

## 多项目并行处理

- 每个项目都有自己的上下文文件，存储在对应的 `.openclaw/` 目录下
- 每个项目使用不同的工作目录（`cwd`），避免上下文之间的交叉污染
- 为每个项目添加标签：`--tags code,<project-name>`
- 同时运行 2-3 个 ACP 会话是安全的；使用多个提供者时最多可运行 4-5 个会话
- 当代理处理简单任务时，ACP 会在后台运行

有关多项目处理的示例，请参见 [references/prompt-templates.md](references/prompt-templates.md)。

## 智能重试机制（最多重试 3 次）

1. 分析失败原因 → 2. 调整提示信息 → 3. 重新尝试改进后的操作 → 4. 最多重试 3 次后若仍未成功则切换为备用方案/报告错误。
每次重试的内容都必须有所不同。

## 进度更新

- 开始任务时发送简短消息；遇到错误时立即报告；任务完成后发送总结信息；发生备用方案时需解释原因。

## 安全性注意事项

- **切勿在 `~/.openclaw/**` 目录中启动代理**——编码代理可能会损坏配置文件
- **务必将工作目录（`cwd`）设置为项目目录**
- **在提交代码前进行审查**——尤其是处理复杂任务时
- **终止失控的会话**——无论是由于超时还是输出结果无意义的情况

## 参考资料
- [references/complex-tasks.md](references/complex-tasks.md) —— 适用于复杂任务的角色分配、质量保证（QA）机制及并行处理策略
- [references/prompt-templates.md](references/prompt-templates.md) —— 上下文文件模板及提示信息示例