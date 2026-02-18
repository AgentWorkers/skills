---
name: lattice
description: >
  初始化和管理 Lattice 组织——这是一个基于文件的操作系统，专为 AI 代理团队设计，通过八阶段的流程实现稳定、持续迭代的开发。其主要优势包括：  
  1. **文件驱动的状态管理**：确保代理在会话之间保持状态的一致性，避免上下文丢失或任务执行偏差，无论任务持续多长时间都能可靠完成。  
  2. **三层故障处理机制**：通过模型升级、同行协商和自动分类（auto-triage）自动解决代理遇到的问题，无需人工干预。  
  3. **阶段化的模型配置**：在需要大量计算（如规划、评审）的阶段使用高性能模型，在需要处理大量数据（如实现、测试）的阶段使用成本效益更高的模型，从而优化资源使用。  
  4. **多项目并行执行**：支持 cron 调度，允许多个项目同时运行，每个项目按照自己的节奏进行。  
  触发事件包括：Lattice 框架的启动、组织结构的创建、流程的设置、代理团队的加入、新项目的启动、多代理项目的启动、八阶段流程的启动、新组织的创建、新项目的启动、部门设置的调整、流程协调器的激活、长时间运行的任务、模型升级、同行协商机制的触发、以及自动分类功能的启用等。
---
# Lattice

Lattice 是一个专为 AI 代理团队设计的基于文件的操作系统。它用持久化的文件替代了易变的聊天窗口，使得代理能够在漫长的迭代开发周期中稳定地工作，整个开发过程通过一个包含 8 个阶段的执行管道来完成。

**为什么选择 Lattice？**

- **稳定的长时间运行**：基于文件的状态机确保代理在各个会话之间保持连贯性，不会出现上下文丢失或数据漂移的问题。任务能够通过结构化的迭代过程在数小时或数天内可靠地完成。
- **三层故障处理机制**：当代理遇到问题时：
  - **模型升级**：尝试使用更强大的模型进行重试；
  - **同行咨询**：从多个模型中收集并行意见；
  - **自动分类**：系统会做出判断（是放宽限制、推迟任务还是等待人工干预）。大多数问题都能自动得到解决。
- **阶段特定的模型配置**：需要大量推理能力的阶段（如规划、评审、架构设计）可以使用强大的推理模型；而需要大量代码编写的阶段（如实现、测试）则可以使用成本效益更高的编码模型。这种配置方式能够在不影响关键质量的前提下显著降低整体资源消耗。

**示例模型分配（来自生产环境）：**

| 阶段 | 模型类型 | 示例模型 |
|-------|-----------|---------|
| 构建架构 | 强大推理能力 | Claude Opus |
| 研究 | 强大推理能力 | Gemini Pro |
| 规划任务 | 强大推理能力 | Claude Opus |
| 实现代码 | 成本效益高的编码模型 | GPT Codex |
| 测试代码 | 成本效益高的编码模型 | GPT Codex |
| 代码评审 | 强大推理能力 | Claude Opus |
| 差异分析 | 强大推理能力 | Gemini Pro |

关键点在于：实现和测试阶段消耗最多的资源（编写和运行代码），但并不需要最昂贵的模型；而规划和评审阶段虽然消耗的资源较少，但需要更复杂的推理能力。因此，应根据认知需求来匹配模型强度，而不是简单地根据模型使用的资源量来决定。

- **多项目并行执行**：可以同时运行多个项目，每个项目都有自己独立的调度器。结合 OpenClaw 的 cron 系统，各个项目可以按照各自的节奏自主推进。

所有模板都存储在 `templates/ORG/` 目录下。

## 快速参考

- 完整的设计文档：`templates/ORG/PROJECTS/pipeline-framework/DESIGN.md`
- 管道指南（适用于所有代理）：`templates/ORG/PIPELINE_GUIDE.md`
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
- **部门列表**：各部门的名称（例如：研究部、工程部、可靠性部）
- **第一个项目**（可选）：项目名称及简短描述

保持对话的流畅性，不要一次性提出所有问题。

### 2. 构建 ORG 目录结构

将整个 `templates/ORG/` 目录复制到 `<target>/ORG/`。

然后进行以下自定义操作：
1. **ORG_README.md**：将示例组织结构中的部门名称替换为用户的实际部门名称。
2. **TASKBOARD.md**：保持模板结构不变（用户稍后填写优先级信息）。
3. **部门设置**：对于用户列出的每个部门：
   - 将 `DEPARTMENTS/example-dept/` 复制到 `DEPARTMENTS/<部门名称>/`；
   - 在每个复制的部门目录中，将 `CHARTER.md`、`RUNBOOK.md`、`HANDOFF.md` 中的 `<部门名称>` 占位符替换为实际的部门名称；
   - 将 `STATE.json` 文件重置为 `{"lastRun": null, "cursor": null, "notes": "初始状态"}`。
4. （创建实际部门后）删除 `DEPARTMENTS/example-dept/` 文件夹（除非用户希望保留它作为参考）。

### 3. 创建第一个项目（如果用户需要）

- 将 `PROJECTS/example-project/` 复制到 `PROJECTS/<项目名称>/`；
- 更新 `STATUS.md` 文件中的项目名称；
- 更新 `DECISIONS.md` 文件的头部信息；
- 配置 `PIPELINE_STATE.json` 文件（具体配置方法见下文）；
- 创建项目完成后删除 `PROJECTS/example-project/` 文件夹。

### 4. 配置管道状态

参考 `templates/ORG/PROJECTS/pipeline-framework/templates/PIPELINE_STATE.template.json` 文件。

向用户询问：
- **每个阶段由哪些代理执行？**（每个角色对应的代理 ID，或者所有阶段都由同一个代理执行）；
- **每个阶段使用哪些模型？**（或者使用默认模型）；
- **模型升级顺序**：从成本最低的模型开始，逐步尝试更强大的模型（例如：`["gflash", "gpro", "sonnet"]`）；
- **同行咨询模型**：在遇到问题时需要咨询的模型；
- **综合/分类模型**：通常使用最强大的模型；
- **通知渠道**（可选）：用于发送管道状态更新的地址。

根据这些信息填写项目的 `PIPELINE_STATE.json` 文件，替换所有 `<placeholder>` 占位符。

### 5. 设置调度器 Cron 作业

阅读 `templates/ORG/PROJECTS/pipeline-framework/templates/ORCHESTRATOR_PROMPT.template.md` 文件。

使用 `cron` 工具创建一个 Cron 作业：
- **调度频率**：每 30 分钟（可调整）；
- **会话执行模式**：独立执行；
- **作业类型**：`agentTurn`；
- **使用的模型**：用户选择的调度器模型；
- **消息内容**：调度器提示模板，其中的所有 `<placeholder>` 占位符都需要填写：
  - `<project>`：项目名称；
  - `<org-root>`：ORG 目录的绝对路径；
  - `<project-root>`：项目目录的绝对路径；
  - `<repo-root>`：代码仓库的绝对路径（询问用户）；
  - 阶段提示文件的绝对路径：技能相关模板文件的绝对路径。

告知用户 Cron 作业的 ID，以便他们后续可以管理该作业。

### 6. 总结

打印以下内容：
- ORG 目录的位置；
- 创建的部门列表；
- 创建的项目列表；
- Cron 作业的 ID 及调度信息；
- 提醒用户填写 `TASKBOARD.md` 文件中的初始优先级信息。

---

## 任务：添加新项目 (`lattice new-project`)

1. 询问项目名称、简短描述以及代码仓库的路径；
2. 将 `templates/ORG/PROJECTS/example-project/` 复制到 `ORG/PROJECTS/<项目名称>/`；
3. 根据步骤 3-4 的内容自定义 `STATUS.md`、`DECISIONS.md` 和 `PIPELINE_STATE.json` 文件；
- （可选）为该项目创建一个新的调度器 Cron 作业。

---

## 任务：添加新部门 (`lattice new-dept`)

1. 询问部门名称及部门使命（用一句话描述）；
2. 将 `templates/ORG/DEPARTMENTS/example-dept/` 复制到 `ORG/DEPARTMENTS/<部门名称>/`；
3. 在 `CHARTER.md` 文件中填写部门名称和使命；
4. 更新 `ORG_README.md` 文件中的相应内容，以包含新部门的详细信息。

---

## 任务：检查组织状态 (`lattice status`)

1. 阅读 `ORG/TASKBOARD.md` 文件，汇总当前的优先级信息；
2. 遍历 `ORG/PROJECTS/` 目录下的所有项目：
   - 查看 `STATUS.md` 文件，了解每个项目的当前阶段和进度；
   - 查看 `PIPELINE_STATE.json` 文件，了解各阶段的执行状态和存在的障碍；
3. 遍历 `ORG/DEPARTMENTS/` 目录下的所有部门：
   - 查看 `HANDOFF.md` 文件，了解每个部门的当前状态和存在的障碍；
4. 提供一个简洁的状态报告。

---

## 管道架构（供参考）

### 8 个执行阶段
```
Constitute → Research → Specify → Plan+Tasks → Implement → Test → Review → Gap Analysis
```

### 三层辅助机制（当某个阶段遇到问题时）
1. **模型升级**：尝试使用更强大的模型进行重试；
2. **同行咨询**：多个模型并行协商并综合分析结果；
3. **自动分类**：系统自动判断：是放宽限制、推迟任务还是等待人工干预。

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