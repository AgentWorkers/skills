---
name: agent-conductor
description: "协调各种编码工具（如 Claude Code、Codex、Cursor、Gemini Code 或任何基于 CLI 的编码工具），以实现实施任务的最大吞吐量。适用场景包括：(1) 编写或修改代码文件；(2) 运行脚本或数据管道；(3) 批量处理大型数据集；(4) 需要并行执行的多阶段工作流程。该方案涵盖了与具体工具无关的调度模板、任务分解、并行协调以及任务完成标准。不适用场景包括：简单的文件读取操作、仅涉及配置的修改，或发送消息。核心原则是：编排器负责规划任务，编码工具负责执行具体操作。"
---
# Agent Conductor 🎼

**您负责指挥，代理执行任务。**

将所有实现工作（文件修改、脚本执行、数据处理等）分配给相应的代理程序。协调会话本身保持简洁：它负责规划、决策和验证；具体执行工作由代理程序完成。

## 支持的代理程序

系统对代理程序类型没有限制。只需设置一次调用命令即可：

| 代理程序 | 调用命令 |
|-------|---------------|
| Claude Code | `claude '<任务>'` |
| OpenAI Codex | `codex '<任务>'` |
| Cursor Agent | `cursor-agent '<任务>'` |
| Gemini Code | `gemini-code '<任务>'` |
| 其他代理程序 | `your-agent-cmd '<任务>'` |

在以下示例中，请使用 `AGENT_CMD` 作为占位符。

## 何时触发任务执行

当任务涉及以下任何一项时，应触发任务执行：
- 编写或修改文件（哪怕只修改一行）
- 运行脚本或处理数据
- 执行时间超过 10 秒
- 需要对多个项目进行批量操作

*如果任务会导致文件修改，**必须**触发任务执行。*

## 任务调度模板

```
## Task: [name]

### Requirement
[One sentence: what to produce and where]

### Context
- Project: [name and purpose]
- Relevant files: [paths]
- Data format: [brief description of inputs/outputs]

### Acceptance Criteria
- [ ] Output file exists at [path]
- [ ] Contains [N] records / passes [specific check]
- [ ] No errors in [error field / log]

### Gotchas
- [Known pitfall 1]
- [Known pitfall 2]

### Environment
- Language/runtime: [python3 / node / go / etc.]
- Working directory: [path]
- Special config: [proxy, auth, env vars if needed]

When done, notify with:
[your completion notification command]
```

## 执行机制

| 执行时间 | 执行方式 |
|----------|-----------|
| < 5 分钟 | 前台执行：`exec pty:true command:"AGENT_CMD '...'"` |
| 5–30 分钟 | 后台执行：`exec pty:true background:true timeout:1800 command:"AGENT_CMD '...'"` |
| > 30 分钟 | 代理程序会生成脚本并直接在 `screen` 或 `tmux` 环境中执行 |

> 如果您的平台有特殊要求（例如 Claude Code 需要 `pty:true`），请确保使用该选项；其他代理程序的配置请参考其官方文档。

## 任务分解

将大型项目按**阶段**进行分解，而非按功能划分。每个阶段都必须能够独立验证。

**在以下情况下需要拆分任务：**
- 执行时间超过 30 分钟
- 需要运行多个脚本
- 需要处理超过 100 个项目
- 一个阶段的输出结果会作为下一个阶段的输入

```
Stage 1: Prepare data  →  clean_data.csv        (< 2 min)
Stage 2: Process       →  results.json           (needs Stage 1)
Stage 3: Report        →  report.md              (needs Stage 2)
```

有关并行协调、检查点设置、任务恢复以及具体应用场景的详细信息，请参阅 [references/patterns.md](references/patterns.md)。

## 验收标准

在收到任务完成信号后，务必进行以下验证：
1. **文件是否存在** — 确认输出路径是否正确
2. **记录数量是否正确** — 实际记录数是否与预期相符
3. **输出结果是否非空** — 随机检查 2–3 个输出结果
4. **是否存在隐藏错误** — 检查错误信息及空值情况

*任务完成信号并不意味着任务已经通过验收。必须完成上述所有验证步骤。*

## 错误处理

| 错误类型 | 处理方式 |
|---------|--------|
| 超时且无输出 | 查看进程日志 → 结束任务并重新调度，同时提供更多相关信息 |
| 任务完成后文件缺失 | 读取执行日志 → 添加相关信息后重新调度 |
| 任务部分完成 | 检查 `progress.json` 文件 → 从检查点继续执行 |
| 任务连续失败两次 | 停止重新调度 → 在协调会话中调试问题 |

## 不应触发任务执行的情况

- 简单的读取操作 → 直接使用相应的读取工具
- 协调器配置的修改 → 仅在协调器会话中进行
- 消息/通知的发送 → 直接使用相应的消息传递工具
- 设计决策 → 需要先由协调器确定方案，再由代理程序执行