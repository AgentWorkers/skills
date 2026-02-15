---
name: lattice
description: >
  Initialize and manage Lattice organizations — a file-based operating system for AI agent teams
  that enables stable, long-running iterative development through an 8-phase pipeline.
  Core strengths: (1) File-driven state keeps agents on track across sessions — no context loss,
  no drift, tasks complete reliably over hours or days. (2) Three-tier failure handling
  (model escalation → peer consult → auto-triage) automatically unblocks stuck agents without
  human intervention. (3) Per-phase model configuration — use cheap models for simple phases,
  strong models for critical ones, optimizing token cost. (4) Multi-project parallel execution
  with cron scheduling — run several projects simultaneously, each on its own cadence.
  Triggers: lattice, org framework, pipeline setup, agent team, multi-agent project, 8-phase pipeline,
  new org, new project, department setup, pipeline orchestrator, long-running tasks, model escalation,
  peer consult, auto-triage, token optimization.
---

# Lattice

Lattice 是一个专为 AI 代理团队设计的基于文件的操作系统。它用持久化的文件替代了易变的聊天窗口，使得代理能够在漫长的迭代开发周期中稳定地工作，通过一个包含 8 个阶段的执行流程来实现这一目标。

**为什么选择 Lattice？**

- **稳定的长时间运行**：基于文件的状态机确保代理在会话之间保持连贯性。不会出现上下文窗口溢出或数据漂移的问题，任务能够通过结构化的迭代过程在数小时或数天内可靠地完成。
- **三层故障处理机制**：当代理遇到问题时：
  - **模型升级**：尝试使用更强大的模型重新运行；
  - **同行咨询**：从多个模型中收集并行意见；
  - **自动分类**：做出判断（放宽限制、推迟任务或请求人工干预）。大多数问题都能自动解决。
- **阶段化模型配置**：将成本较低的模型用于简单的阶段（如研究和规划），将成本较高的模型保留用于关键阶段（如实现和评审）。这样可以大幅降低运行成本，同时不牺牲任务质量。
- **多项目并行执行**：可以同时运行多个项目，每个项目都有自己的定时调度器。结合 OpenClaw 的定时系统，项目可以按照独立的节奏自主推进。

模板文件位于 `templates/ORG/` 目录下。

## 快速参考

- 完整的设计文档：`templates/ORG/PROJECTS/pipeline-framework/DESIGN.md`
- 流程指南（适用于所有代理）：`templates/ORG/PIPELINE_GUIDE.md`
- 子代理指南：`templates/ORG/PROJECTS/pipeline-framework/templates/PIPELINE_GUIDE_FOR_SUBAGENTS.md`
- 调度器提示模板：`templates/ORG/PROJECTS/pipeline-framework/templates/ORCHESTRATOR_PROMPT.template.md`
- 阶段提示模板：`templates/ORG/PROJECTS/pipeline-framework/templates/PHASE_PROMPTS/`
- 状态机模板：`templates/ORG/PROJECTS/pipeline-framework/templates/PIPELINE_STATE.template.json`

---

## 任务：初始化一个新的组织 (`lattice init`)

### 1. 收集信息

向用户询问以下信息：
- **组织名称**（例如：“Acme Labs”）
- **目标目录**：用于创建 `ORG/` 文件夹的位置（默认为当前工作区的根目录）
- **部门列表**：部门名称（例如：研究部、工程部、可靠性部）
- **第一个项目**（可选）：项目名称及简短描述

保持对话的轻松氛围，不要一次性提出所有问题。

### 2. 构建 ORG 目录结构

将整个 `templates/ORG/` 目录复制到 `<target>/ORG/`。

然后进行以下自定义操作：
1. **ORG_README.md**：将示例组织结构中的部门名称替换为用户的实际部门名称。
2. **TASKBOARD.md**：保留模板结构（用户稍后填写优先级信息）。
3. **部门设置**：对于用户列出的每个部门：
   - 将 `DEPARTMENTS/example-dept/` 复制到 `DEPARTMENTS/<部门名称>/`；
   - 在每个复制的部门文件夹中，将 `CHARTER.md`、`RUNBOOK.md`、`HANDOFF.md` 中的 `<部门名称>` 占位符替换为实际的部门名称；
   - 将 `STATE.json` 重置为 `{"lastRun": null, "cursor": null, "notes": "初始状态"}`。
4. （创建实际部门后）删除 `DEPARTMENTS/example-dept/` 文件夹（除非用户希望保留它作为参考）。

### 3. 创建第一个项目（如果用户要求）

- 将 `PROJECTS/example-project/` 复制到 `PROJECTS/<项目名称>/`；
- 更新 `STATUS.md` 文件中的项目名称；
- 更新 `DECISIONS.md` 文件的头部信息；
- 配置 `PIPELINE_STATE.json`（详见下文“配置管道状态”）；
- 创建实际项目后删除 `PROJECTS/example-project/` 文件夹。

### 4. 配置管道状态

参考 `templates/ORG/PROJECTS/pipeline-framework/templates/PIPELINE_STATE.template.json` 文件。

向用户询问：
- **哪些代理将参与每个阶段的执行？**（每个角色的代理 ID，或者所有代理都由同一个代理执行）
- **每个阶段使用哪些模型？**（或者使用默认模型）
- **升级流程**：按成本从低到高的模型列表（例如：`["gflash", "gpro", "sonnet"]`）
- **同行咨询模型**：在遇到问题时需要咨询的模型
- **综合/分类模型**：通常使用最强大的可用模型
- **通知渠道**（可选）：用于发送管道状态更新的地址

使用这些信息填写项目的 `PIPELINE_STATE.json` 文件，替换所有的 `<placeholder>` 占位符。

### 5. 设置调度器 Cron 作业

阅读 `templates/ORG/PROJECTS/pipeline-framework/templates/ORCHESTRATOR_PROMPT.template.md` 文件。

使用 `cron` 工具创建一个 Cron 作业：
- **调度频率**：每 30 分钟（可调整）
- **会话目标**：隔离环境
- **作业类型**：`agentTurn`
- **使用的模型**：用户选择的调度器模型
- **消息内容**：调度器提示模板，其中所有 `<placeholder>` 占位符均已填充：
  - `<project>`：项目名称
  - `<org-root>`：ORG 目录的绝对路径
  - `<project-root>`：项目目录的绝对路径
  - `<repo-root>`：代码仓库的绝对路径（询问用户）
  - 阶段提示文件的路径：技能相关阶段提示文件的绝对路径

将 Cron 作业的 ID 告知用户，以便他们后续进行管理。

### 6. 总结

打印以下内容：
- ORG 目录的位置
- 创建的部门列表
- 创建的项目列表
- Cron 作业的 ID 及调度信息
- 提醒用户填写 `TASKBOARD.md` 中的初始优先级信息

---

## 任务：添加新项目 (`lattice new-project`)

1. 询问项目名称、简短描述以及代码仓库的路径。
2. 将 `templates/ORG/PROJECTS/example-project/` 复制到 `ORG/PROJECTS/<项目名称>/`。
3. 根据步骤 3-4 的内容自定义 `STATUS.md`、`DECISIONS.md` 和 `PIPELINE_STATE.json` 文件。
4. （可选）为该项目创建一个新的调度器 Cron 作业。

---

## 任务：添加新部门 (`lattice new-dept`)

1. 询问部门名称及部门使命（用一句话描述）。
2. 将 `templates/ORG/DEPARTMENTS/example-dept/` 复制到 `ORG/DEPARTMENTS/<部门名称>/`。
3. 在 `CHARTER.md` 文件中填写部门名称和使命。
4. 更新 `ORG_README.md` 文件中的相关内容，以包含新部门的详细信息。

---

## 任务：检查组织状态 (`lattice status`)

1. 阅读 `ORG/TASKBOARD.md` 文件，了解当前的优先级任务。
2. 对于 `ORG/PROJECTS/` 目录下的每个项目：
   - 查看 `STATUS.md` 文件，了解当前阶段和进度；
   - 查看 `PIPELINE_STATE.json` 文件，了解各阶段的执行状态和存在的障碍。
3. 对于 `ORG/DEPARTMENTS/` 目录下的每个部门：
   - 查看 `HANDOFF.md` 文件，了解当前的状态和存在的障碍。
4. 提供一个简洁的状态报告。

---

## 管道架构（供参考）

### 8 个执行阶段
```
Constitute → Research → Specify → Plan+Tasks → Implement → Test → Review → Gap Analysis
```

### 三层辅助机制（当某个阶段遇到问题时）
1. **模型升级**：尝试使用更强大的模型重新运行。
2. **同行咨询**：多个模型并行咨询并综合分析结果。
3. **自动分类**：自动化系统判断：放宽限制、推迟任务或请求人工干预。

### 每个项目的关键文件
```
ORG/PROJECTS/<project>/
├── STATUS.md              # Human-readable status
├── DECISIONS.md           # Key decisions + rationale
├── PIPELINE_STATE.json    # Phase state machine
├── PIPELINE_LOG.jsonl     # Append-only history
├── pipeline/              # Current run artifacts
└── pipeline_archive/      # Historical runs
```