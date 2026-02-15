---
name: ralph-loop
description: 本指南旨在指导 OpenClaw 代理使用 `exec` 和 `process` 工具来执行 Ralph Wiggum 循环（Ralph Wiggum 是一种特定的编程框架或任务类型）。代理通过 `pty:true` 配置实现与编码代理（如 Codex、Claude Code、OpenCode、Goose）的协同工作，并提供适当的 TTY（终端）支持。代码的规划与构建过程依据 `PROMPT.md`、`AGENTS.md`、`SPECS` 和 `IMPLEMENTATION_PLAN.md` 文件进行。系统支持“规划”（PLANNING）与“构建”（BUILDING）两种模式，同时具备背压（backpressure）控制机制、沙箱环境（sandboxing）以及任务完成条件（completion conditions）等功能。用户可以提交循环任务，代理会使用相应工具来执行这些任务。
version: 1.1.0
author: OpenClaw Community
keywords: [ralph-loop, ai-agent, coding-agent, pty, tty, automation, loop, opencode, codex, claude, goose, exec-tool, process-tool]
license: MIT
---

# Ralph Loop

## 概述
本技能指导**OpenClaw代理**使用`exec`和`process`工具执行Ralph Loop工作流程。代理按照Ralph Playbook的流程来协调AI编码代理会话：

1) **定义需求** → 制定待办事项（JTBD） → 确定关注主题 → 创建`specs/*.md`文件
2) **规划阶段** → 创建/更新`IMPLEMENTATION_PLAN.md`文件（暂不执行实际操作）
3) **构建阶段** → 执行任务、运行测试（使用backpressure机制）、更新计划并提交结果

该流程通过`PROMPT.md`和`AGENTS.md`文件（每次迭代时都会被加载）以及磁盘上的计划和规范文件来保持上下文的一致性。

## 工作原理
本技能为**OpenClaw代理**生成指令，使其使用`exec`和`process`工具来执行Ralph Loop流程：
- 代理使用`exec`工具调用编码代理命令
- 通过设置`pty: true`来为交互式CLI提供TTY（终端）支持
- 使用`background: true`来实现监控功能
- 使用`process`工具来监控进程进度并检测任务完成情况

**重要提示**：用户无需直接运行这些脚本——OpenClaw代理会利用其工具功能来执行它们。

---

## TTY要求
某些编码代理需要**真实的终端（TTY）**才能正常工作，否则可能会出现卡顿或错误：

**需要TTY支持的交互式CLI**：
- OpenCode、Codex、Claude Code、Pi、Goose

**非交互式CLI（基于文件的）**：
- aider、自定义脚本

**解决方案**：对于交互式CLI，使用`exec + process`模式；对于基于文件的工具，则使用简单的循环处理方式。

---

## 代理工具使用模式

### 交互式CLI（推荐模式）
对于OpenCode、Codex、Claude Code、Pi和Goose，它们都需要TTY支持：
- 当我（代理）收到Ralph Loop请求时，我将：
  1. 使用`exec`工具启动编码代理：
    ```
   exec tool with parameters:
   - command: "opencode run --model <MODEL> \"$(cat PROMPT.md)\""
   - workdir: <project_path>
   - background: true
   - pty: true
   - yieldMs: 60000
   - timeout: 3600
   ```
  2. 从`exec`工具的响应中获取会话ID
  3. 使用`process`工具进行监控：
    ```
   process tool with:
   - action: "poll"
   - sessionId: <captured_session_id>
   
   process tool with:
   - action: "log"
   - sessionId: <captured_session_id>
   - offset: -30  (for recent output)
   ```
  4. 通过读取`IMPLEMENTATION_PLAN.md`中的特定文本来检查任务完成情况
  5. 如有必要，使用`process`工具终止会话：
    ```
   process tool with:
   - action: "kill"
   - sessionId: <session_id>
   ```

**优势**：支持TTY、实时日志记录、超时处理、支持并行会话、工作目录隔离

---

## 代理工作流程

### 1) 收集输入信息
**必填**：
- 目标/待办事项（JTBD）
- 使用的CLI工具（`opencode`、`codex`、`claude`、`goose`、`pi`等）
- 工作阶段（规划阶段（PLANNING）、构建阶段（BUILDING）或同时进行（BOTH）
- 最大迭代次数（默认：规划阶段5次，构建阶段10次）

**可选**：
- 任务完成标志（默认：`IMPLEMENTATION_PLAN.md`中的`STATUS: COMPLETE`）
- 工作目录（默认：`$PWD`）
- 每次迭代的超时时间（默认：3600秒）
- 沙箱环境选择
- 自动批准标志（`--full-auto`、`--yolo`、`--dangerously-skip-permissions`）

**自动检测**：
- 如果使用的CLI工具属于交互式类型，则使用`exec`工具并设置`pty: true`
- 从CLI参数中提取相关设置

### 2) 根据需求生成规范文件（可选）
如果需求不明确，可以将待办事项分解为具体的关注主题，并为每个主题创建`specs/<topic>.md`文件。确保规范文件简洁且易于测试。

### 3) PROMPT.md和AGENTS.md文件
- `PROMPT.md`文件会引用`specs/*.md`和`IMPLEMENTATION_PLAN.md`文件，以及相关的项目文件。
- `AGENTS.md`文件包含测试命令、构建/运行指令以及操作过程中的经验总结。

### 4) 提示模板
- **规划阶段提示**（不涉及实际执行）：
    ```
You are running a Ralph PLANNING loop for this goal: <goal>.

Read specs/* and the current codebase. Only update IMPLEMENTATION_PLAN.md.

Rules:
- Do not implement
- Do not commit
- Create a prioritized task list
- Write down questions if unclear

Completion:
When plan is ready, add: STATUS: PLANNING_COMPLETE
```
- **构建阶段提示**：
    ```
You are running a Ralph BUILDING loop for this goal: <goal>.

Context: specs/*, IMPLEMENTATION_PLAN.md, AGENTS.md

Tasks:
1) Pick the most important task
2) Investigate code
3) Implement
4) Run backpressure commands from AGENTS.md
5) Update IMPLEMENTATION_PLAN.md
6) Update AGENTS.md with learnings
7) Commit with clear message

Completion:
When all done, add: STATUS: COMPLETE
```

### 5) CLI命令参考
代理根据以下模式构建命令字符串：
| CLI工具 | 命令字符串格式 |
|---------|----------------------|
| OpenCode | `opencode run --model <模型> "$(cat PROMPT.md)"` |
| Codex | `codex exec <参数> "$(cat PROMPT.md)"` （需要git支持） |
| Claude Code | `claude <参数> "$(cat PROMPT.md)"` |
| Pi | `pi --provider <提供者> --model <模型> -p "$(cat PROMPT.md)"` |
| Goose | `goose run "$(cat PROMPT.md)"` |

**常用参数**：
- Codex：`--full-auto`、`--yolo`、`--model <模型>`
- Claude：`--dangerously-skip-permissions`

---

## 代理工具使用示例

### 示例1：OpenCode Ralph Loop
代理执行的步骤如下：
```
Step 1: Launch OpenCode with exec tool
{
  command: "opencode run --model github-copilot/claude-opus-4.5 \"$(cat PROMPT.md)\"",
  workdir: "/path/to/project",
  background: true,
  pty: true,
  timeout: 3600,
  yieldMs: 60000
}

Step 2: Capture session ID from response
sessionId: "abc123"

Step 3: Monitor with process tool every 10-30 seconds
{
  action: "poll",
  sessionId: "abc123"
}

Step 4: Check recent logs
{
  action: "log",
  sessionId: "abc123",
  offset: -30
}

Step 5: Read IMPLEMENTATION_PLAN.md to check for completion
- Look for: "STATUS: COMPLETE" or "STATUS: PLANNING_COMPLETE"

Step 6: If complete or timeout, cleanup
{
  action: "kill",
  sessionId: "abc123"
}
```

### 示例2：使用`--full-auto`模式的Codex
代理使用的命令如下：
```
exec tool:
{
  command: "codex exec --full-auto --model anthropic/claude-opus-4 \"$(cat PROMPT.md)\"",
  workdir: "/path/to/project",
  background: true,
  pty: true,
  timeout: 3600
}

# Then monitor with process tool as above
```

---

## 完成检测
使用灵活的正则表达式来匹配不同的完成状态：
```bash
grep -Eq "STATUS:?\s*(PLANNING_)?COMPLETE" IMPLEMENTATION_PLAN.md
```

**匹配的完成状态**：
- `STATUS: COMPLETE`
- `STATUS: COMPLETE`
- `STATUS: PLANNING_COMPLETE`
- `## Status: PLANNING_COMPLETE`

---

## 安全性与防护措施
### 自动批准标志（请谨慎使用！**
- `Codex`：`--full-auto`（在沙箱环境中自动批准）或`--yolo`（不使用沙箱）
- `Claude`：`--dangerously-skip-permissions`
**建议**：使用沙箱环境（如docker、e2b或fly）并限制代理的权限。

### 应急处理措施
- 停止执行：使用`Ctrl+C`
- 终止会话：使用`process`工具执行`kill`命令
- 回滚操作：使用`git reset --hard HEAD~N`

### 最佳实践
1. **从小规模开始测试**：先进行1-2次迭代
2. **工作目录隔离**：防止读取无关文件
3. **设置超时**：默认的1小时时间可能不足以完成所有任务
4. **积极监控**：定期检查日志，避免过早终止进程
5. **先明确需求**：在开始构建之前先整理好规范文件
6. **尽早添加测试**：从一开始就加入测试步骤

---

## 故障排除
| 问题 | 解决方案 |
|---------|----------|
| OpenCode卡顿 | 确保代理使用`exec`工具并设置`pty: true` |
| 会话无法启动 | 检查CLI路径、git仓库和命令语法 |
| 无法检测到任务完成 | 验证`IMPLEMENTATION_PLAN.md`中的完成状态标识 |
- 进程超时 | 代理应增加超时时间或简化任务流程 |
- 并发任务冲突 | 代理应使用git工作目录来隔离不同任务 |
- 无法查看进度 | 代理应使用`process`工具并设置`log`选项以记录日志

---

## 许可证
本技能基于以下人员的贡献开发：
- **@jordyvandomselaar**：提出了Ralph Loop的概念和工作流程设计
- **@steipete**：设计了编码代理的运行模式以及支持TTY的`exec`和`process`工具的使用方式

**关键改进**：通过使用`exec`工具并设置`pty: true`为交互式CLI提供TTY支持，解决了在简单后台bash执行过程中可能出现的卡顿问题。