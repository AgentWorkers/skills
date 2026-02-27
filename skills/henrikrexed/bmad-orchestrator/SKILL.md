---
name: bmad-orchestrator
description: 在 OpenClaw 和 Claude Code 之间协调完整的 BMAD（Brainstorming, Requirements Documenting, Architecture, Implementation）方法工作流程。适用于使用 BMAD 方法论启动新项目、执行 BMAD 各阶段（头脑风暴、需求文档编写、架构设计、实施），或通过 BMAD 工作流程管理 Claude Code 代理。该流程负责与用户交互的阶段（1-3），并将实施阶段（4）通过 tmux 任务管理器委托给 Claude Code 完成。
---
# BMAD Orchestration Tool

该工具用于在 OpenClaw 与 Claude Code 之间协调执行 BMAD（敏捷 AI 驱动开发的突破性方法）的四个阶段流程。

## 架构

- **第 1-3 阶段（交互式）**：通过 OpenClaw 聊天与用户进行交流，协助进行头脑风暴、完善产品需求文档（PRD），并讨论系统架构。此阶段用户的想法最为关键。
- **团队协作模式（Party Mode）**：在关键决策节点，建议使用 Claude Code 的团队协作模式——多个 BMAD 代理会共同讨论问题并产生更丰富的输出结果。
- **第 4 阶段（自动化）**：通过开发虚拟机上的 tmux 将任务委托给 Claude Code，监控进度并向用户汇报结果。

## 先决条件

- 开发虚拟机上已安装 Claude Code（可通过 SSH 访问）。
- 项目中已安装 BMAD 框架（位于 `_bmad/` 目录中，包含代理、工作流程和命令）。
- 开发虚拟机上支持 tmux。

## 状态跟踪

工作流程状态记录在 `_bmad-output/orchestrator-state.yaml` 文件中：

```yaml
project: <name>
vm_host: <ip>
vm_user: <user>
project_path: <path>
tmux_socket: /tmp/openclaw-tmux-sockets/openclaw.sock
tmux_session: bmad-<project>
current_phase: 1|2|3|4
current_workflow: <workflow-name>
artifacts:
  brainstorming_report: null|path
  product_brief: null|path  
  prd: null|path
  ux_spec: null|path
  architecture: null|path
  epics: null|path
  sprint_status: null|path
  project_context: null|path
```

## 第 1 阶段：分析与用户互动

### 1.1 头脑风暴 (`bmad-brainstorming`)

在 OpenClaw 聊天中与用户进行以下对话：
1. 询问：“我们正在开发什么项目？请简要介绍一下项目背景。”
2. 探讨问题领域——了解用户需求、痛点及现有解决方案。
3. 对假设提出质疑。
4. **建议使用团队协作模式**：“需要我在 Claude Code 中启动团队协作模式吗？BMAD 代理（分析师、架构师、项目经理）会讨论你的想法，并发现可能被忽略的问题。”
5. 如果选择团队协作模式，向 Claude Code 发送 `/bmad-brainstorming` 命令，捕获讨论结果并分享要点。
6. 将讨论内容整理成关键决策和主题。
7. 生成文档：`brainstorming-report.md`。

### 1.2 研究 (`bmad-bmm-research`) — 可选

如果项目需要市场/技术/领域方面的验证：
1. 与用户讨论需要验证的内容。
2. 将研究工作流程提交给 Claude Code 处理。
3. 共同审查研究结果。

### 1.3 产品概述 (`bmad-bmm-create-product-brief`)

1. 以头脑风暴的结果为基础，与用户一起明确项目愿景、目标用户群和成功指标。
2. **建议使用团队协作模式**：“项目经理和分析师可以共同审查这份产品概述。”
3. 如果选择团队协作模式，发送相应命令，捕获讨论要点。
4. 重复此过程直至用户批准。
5. 生成文档：`product-brief.md`。

## 第 2 阶段：规划与用户互动

### 2.1 产品需求文档（PRD） (`bmad-bmm-create-prd`)

1. 以产品概述为依据，与用户逐项讨论需求：
   - 功能性需求（FRs）
   - 非功能性需求（NFRs）
   - 用户使用流程
   - 成功指标
2. **建议使用团队协作模式**：“项目经理、架构师和质量保证人员可以一起审查这些需求。”
3. 如果选择团队协作模式，发送命令并分享讨论结果。
4. 重复此过程直至用户确认。
5. 生成文档：`prd.md`。

### 2.2 用户体验设计（UX Design） (`bmad-bmm-create-ux-design`) — 仅适用于有用户界面的项目

#### 仅适用于需要设计用户界面的项目，后端/基础设施工具可跳过此步骤。

## 第 3 阶段：解决方案设计与用户互动

### 3.1 系统架构 (`bmad-bmm-create-architecture`)

1. 以产品需求文档为依据，与用户讨论技术决策：
   - 选择编程语言/框架
   - 部署模式
   - 关键设计模式及权衡因素
   - 架构决策记录（ADRs）
2. **建议使用团队协作模式**：“架构师、开发人员和质量保证人员共同讨论架构，有助于提前发现实施风险。”
3. 如果选择团队协作模式，发送命令并分享讨论结果。
4. 与用户共同完善方案。
5. 生成文档：`architecture.md`，其中包含架构决策记录（ADRs）。

### 3.2 项目任务与故事分解 (`bmad-bmm-create-epics-and-stories`)

1. 以系统架构和产品需求文档为基础，向用户展示任务分解结果。
2. 讨论每个任务的大小、优先级和依赖关系。
3. 生成文档：`epics.md`，其中包含所有任务列表。

### 3.3 实施准备检查 (`bmad-bmm-check-implementation-readiness`)

1. 将相关数据提交给 Claude Code 进行自动化检查。
2. 分享检查结果：通过 /PASS/CONCERNS/FAIL。
3. 如果存在问题，与用户讨论并解决问题。
4. 生成报告：`readiness-report.md`。

### 3.4 项目背景信息 (`bmad-bmm-generate-project-context`)

1. 在系统架构确定后，将相关信息提交给 Claude Code。
2. 与用户一起审查结果。
3. 生成文档：`project-context.md`。

## 第 4 阶段：通过 Claude Code 自动化执行

### 4.0 设置

有关 tmux 会话初始化的详细信息，请参阅 [references/tmux-setup.md](references/tmux-setup.md)。

### 4.1 斯普林特计划（Sprint Planning）

将相关数据提交给 Claude Code：
```
/bmad-bmm-sprint-planning
```
捕获并保存 `sprint-status.yaml` 文件。

### 4.2 任务执行循环（针对每个任务）

对于每个任务：
1. **创建任务**：发送 `/bmad-bmm-create-story` 命令，生成 `story-[slug].md` 文件。
2. **开发任务**：发送 `/bmad-bmm-dev-story` 命令，实现代码并进行测试。
3. **代码审查**：发送 `/bmad-bmm-code-review` 命令，验证代码质量。
4. 如果审查失败，返回修改后的代码并重新审查。
5. 更新任务状态。
6. 完成每个任务后提交代码。

### 4.3 任务完成

所有任务完成后：
1. 发送 `/bmad-bmm-retrospective` 命令，总结经验教训。
2. （可选）运行 `/bmad-bmm-automate` 命令生成端到端测试脚本。
3. 提交代码并更新 sprint 状态。

### 4.4 监控

设置定时任务，每 15 分钟监控 Claude Code 的执行进度，并通过聊天向用户报告进度。

## 团队协作模式（Team Collaboration Mode）集成

团队协作模式可在以下情况下使用，模拟 Claude Code 中的多代理讨论：
| 使用场景 | 目的 | 命令 |
|------|-----|---------|
| 头脑风暴后 | 发现潜在问题 | `/bmad-party-mode` 并提供头脑风暴的上下文信息 |
| 产品概述后 | 验证项目愿景 | `/bmad-party-mode` 并提供产品概述文件 |
| 产品需求文档审查期间 | 发现需求漏洞 | `/bmad-party-mode` 并提供需求文档草稿 |
| 架构决策时 | 讨论权衡因素 | `/bmad-party-mode` 并提供架构设计信息 |

**如何触发 Claude Code 的团队协作模式**：
```bash
tmux send-keys -l -- "/bmad-party-mode" && sleep 0.3 && tmux send-keys Enter
```
捕获讨论结果，提取关键见解并向用户展示。

## Claude Code 命令参考

完整的命令列表请参阅 [references/bmad-commands.md](references/bmad-commands.md)。

## 快速流程（跳过第 1-3 阶段）

对于简单且需求明确的项目：
1. 使用 `/bmad-bmm-quick-spec` 命令生成技术规范文档（`tech-spec.md`）。
2. 使用 `/bmad-bmm-quick-dev` 命令直接开始开发。

**仅当用户明确表示项目简单且需求清晰时使用此流程。**

## 向 Claude Code 发送命令

有关 tmux 的交互方式，请参阅 [references/tmux-setup.md](references/tmux-setup.md)。

**重要规则**：
- 分段输入文本，并在每次输入后稍作延迟（符合 Claude Code 的用户界面交互逻辑）。
- 使用 `capture-pane -S -200` 命令读取输出内容。
- 在发送下一个命令前等待界面提示符出现。
- 如果遇到问题，可以使用 `C-c` 键中断当前操作。