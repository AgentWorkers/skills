---
name: codex-orchestrator
description: **Codex CLI 的系统化端到端软件交付工具**  
该工具支持两种项目模式：**绿色场模式（用于新项目的构建）** 和 **棕地场模式（用于现有系统的升级）**，以及两种执行模式：**自主执行模式** 和 **受控执行模式**。  

**主要特点：**  
- **全面的生命周期管理**：支持严格的开发阶段控制，确保项目按计划进行。  
- **进度追踪**：实时监控项目进度，便于团队成员了解项目进展。  
- **逐步测试**：提供手动和自动化测试选项，确保代码质量。  
- **持续文档更新**：自动更新项目文档，保持信息的最新性。  
- **变更影响管理**：有效管理代码变更对系统的影响。  
- **通用工作流程**：提供可复用的 `AGENTS.md` 工作流程模板，适用于任何编码工具或代理。  

**适用场景：**  
适用于需要系统化、高效软件交付流程的场景，尤其是那些对项目质量、进度和文档管理有严格要求的项目。
---

# Codex Orchestrator

将 Codex 视为一个规范、有序的交付系统，而不仅仅是一个一次性生成的工具。

## 核心模式

请同时选择以下两种模式：

- `project_mode`：
  - `greenfield`：从零开始构建
  - `brownfield`：整合并现代化现有系统
- `execution_mode`：
  - `autonomous`：在满足所有条件后自动执行
  - `gated`：在每个执行阶段暂停，等待用户批准

## 指导原则：规范驱动开发（Spec-Driven Development）

**没有规范的代码是不被允许的。** 这是一条不可商量的原则。

在任何实施之前，必须先编写一份书面规范，其中应包含：
- 要构建的内容
- 为什么需要它
- 可接受的测试标准
- 限制条件以及超出范围的内容

编码人员绝对不能：
- 对需求进行猜测
- 对系统行为做出假设
- 添加未被请求的功能
- 创建规范中未规定的抽象概念

如果规范不明确，请立即停止并寻求澄清。切勿猜测。

有关完整的规范模板和执行规则，请参阅 `references/spec-driven-development.md`。

## 不可跳过的流程步骤：

1. 收集信息 + 填写计划问卷
2. **创建规范 + 获得批准**（规范必须在编写代码之前完成）
3. 创建文档框架 + 确认 `AGENTS.md` 合同
4. 根据模式进行预架构设计
5. 设计架构并制定 ADR 基线（参考规范）
6. 按照垂直切片的方式逐步构建（每个任务都应参照规范）
7. 根据规范的可接受标准进行验证
8. 通过安全/质量检查
9. 确认是否可以发布 + 完成任务交接

切勿跳过任何检查步骤，也绝不要在没有规范的情况下开始实施。

## 必需的资源

在开始之前，请阅读以下参考资料：

- `references/spec-driven-development.md`（必读——指导所有工作流程）
- `references/planning-questionnaire.md`
- `references/modes.md`
- `references/gate-checklists.md`
- `references/testing-matrix.md`
- `references/manual-test-templates.md`
- `references/codex-runbook.md`
- `references/gate-prompts.md`
- `scripts/agent_exec.py`
- `references/research-playbook.md`（如果 `research_mode=true`）

## 文档框架的初始化

```bash
python scripts/init_project_docs.py --root <project-path> --mode <greenfield|brownfield>
```

此步骤会创建/更新以下文件：
- `AGENTS.md`（项目工作流程合同）
- `docs/*.md`（包含计划、架构、测试和进度信息的文档）
- 适用于 `brownfield` 模式的文档
- `.orchestrator/status.json`（机器可读的状态信息）
- `.orchestrator/context.json`（项目/执行/研究模式的上下文信息）

## 计划规则

在开始之前，首先询问用户需要使用哪种编码工具（`codex` | `claude` | `opencode` | `pi`），并确定备用工具。然后根据 `references/planning-questionnaire.md` 中的问题进行详细询问。

至少需要回答以下问题：
- 项目目标
- 主要用户使用流程
- 第一阶段的任务范围
- 托管目标
- 技术栈偏好（或请求推荐）
- `project_mode`
- `execution_mode`
- 对“完成”的定义
- 可接受的测试标准

如果 `research_mode=true`，则在 G2 阶段之前生成 `docs/research-notes.md` 和架构建议。

## 各模式的具体要求

### Greenfield（从零开始构建）

在 G2 阶段之前必须完成以下内容：
- 明确的需求和完成标准
- 架构基线
- 包含多种方案的 ADR-0001 文档
- 持续集成/测试的基线计划

### Brownfield（整合现有系统）

在 G2 阶段之前必须完成以下内容（这些内容应由编码人员编写，而非协调者）：
- 系统的当前架构和组件清单
- 依赖关系图及风险登记册
- 特性测试的基线
- 迁移策略及回滚方案
- 明确的兼容性边界

## 关卡管理系统（Gate Engine）

使用 `references/gate-checklists.md` 中定义的 `G0` 至 `G7` 等关卡。

通过脚本更新关卡状态：

```bash
python scripts/gate_status.py set --root <project-path> --gate G3 --state PASS --note "slice-1 verified"
```

验证状态信息：

```bash
python scripts/gate_status.py validate --root <project-path>
```

允许的状态：`PENDING | IN_PROGRESS | PASS | FAIL | BLOCKED`。
默认情况下，会强制执行关卡的前置条件（包括流程顺序和模式相关的文档检查）。

## 验证规则

请使用 `references/testing-matrix.md` 中的规定进行验证。

每个执行阶段都必须执行的强制检查包括：
- 代码格式检查、类型检查、构建验证
- 单元测试/集成测试/端到端测试（如适用）
- API 合规性检查（如果使用了 API）
- 安全性基线检查
- 文档同步验证

此外，还需要执行 `references/manual-test-templates.md` 中提供的手动测试脚本。

## 文档编写规则

对于每个重要的步骤，必须执行以下操作：
- 更新 `docs/tasks.md`
- 更新 `docs/progress.md`
- 添加到 `docs/change-log.md`
- 更新 `docs/traceability.md`
- 将测试结果记录在 `docs/test-results.md` 中

对于用户请求的变更，需要执行以下操作：

```bash
python scripts/change_impact.py --root <project-path> --request "<change request>"
```

完成后，需要更新受影响的文档中的所有待办事项。

## Codex 的执行流程

对于长时间运行的任务，建议使用 PTY（并行任务执行）或后台任务执行方式。请遵循 `references/codex-runbook.md` 中提供的命令模式。

重要规则：每次运行只执行一个任务，不能在一次操作中完成整个项目。
对于 G4 阶段，需要维护 `docs/g4-task-plan.md` 中的待办事项列表，并逐一处理任务。

使用 ````bash
python scripts/generate_gate_prompt.py --gate <G1..G7> --agent <codex|claude|opencode|pi> --project-mode <greenfield|brownfield> --execution-mode <autonomous|gated> --research-mode <true|false> --task "<single task summary>" --spec-ref "<spec ref when applicable>"
```` 生成与具体关卡相关的提示信息。

`update_docs_step.py` 现在仅用于恢复或手动记录操作。主要要求是：编码人员应在执行每个任务时直接更新文档。

必须执行的循环步骤包括：
1. 确认该任务有相应的规范（没有规范则不允许执行）
2. 使用规范驱动的提示模板启动相应的编码工具
3. 任务完成后，编码人员立即更新文档（包括交接清单）
4. 编码人员通过终端工具启动 OpenClaw 进行验证
5. OpenClaw 代理执行验证：
   - 使用终端工具进行 CLI 验证
   - 对于 Web 流程，使用浏览器工具进行手动验证
6. 确认验证结果是否符合规范的可接受标准
7. 如果验证失败，OpenClaw 会将失败原因反馈给编码人员，并重新启动修复流程
8. 仅在验证通过后才能将状态设置为 `PASS` 或 `BLOCKED`

执行规则：
- 对于 G3/G4 阶段的关卡，`run_gate.py` 需要 `--spec-ref` 参数
- `run_gate.py` 需要编码人员和备用工具的上下文信息
- 每个任务都需要验证结果（`--validate-cmd` 和/或 `--ui-review-note` 参数）
- 被标记为 `--requires-browser-check` 的任务必须包含 `--ui-review-note`
- 当状态设置为 `PASS` 时，如果使用了 `--agent-dry-run`，则不允许继续执行下一步
- 对于 G4 阶段，只有当 `docs/g4-task-plan.md` 中的所有任务都已完成时，状态才能设置为 `PASS`
- 验证结果会记录在 `docs/validation-log.md` 中
- 编码人员必须在每次任务完成后更新文档，包括 `docs/agent-handoff.md`
- 在 `brownfield` 模式下，如果编码人员未更新相关文档，G1/G2 阶段的关卡将标记为 `FAIL`
- 编码人员生成的提示信息必须包含 `references/spec-driven-development.md` 中规定的规范内容
- 任何没有规范参考的实现都将被视为失败
- 在自动执行模式下，如果验证失败，系统会自动尝试多次修复（默认尝试次数为 2 次），并将失败详情反馈给编码人员
- 可选的高级模式：`--auto-block-on-retry-exhaust` 会在尝试次数用尽后自动将关卡状态设置为 `BLOCKED`

## 进度可视化

生成一个快速的状态显示板：

```bash
python scripts/progress_dashboard.py --root <project-path>
```

该显示板会汇总当前关卡的进度、完成百分比、存在的障碍以及最近的活动情况。

可以通过一个命令执行单个任务的关卡验证：

```bash
python scripts/run_gate.py --root <project-path> --gate G2 --agent codex --fallback-agent claude --project-mode brownfield --execution-mode gated --research-mode true --task "architecture baseline refined for API routing" --status IN_PROGRESS --validate-cmd "npm run -s typecheck" --ui-review-note "N/A for architecture-only task"
```

只有在所有关卡检查项都完成后，才能将状态设置为 `PASS`：

```bash
python scripts/run_gate.py --root <project-path> --gate G2 --agent codex --task "architecture gate complete" --status PASS --validate-cmd "npm run -s typecheck"
```

对于涉及 Web 或 UI 的任务，需要 OpenClaw 代理进行浏览器验证：

```bash
python scripts/run_gate.py ... --requires-browser-check --ui-review-note "Verified login + CRUD manually in browser via OpenClaw browser tools"
```

## 打包可发布的技能成果

最终交付物包括：
- `docs/progress.md`（显示 100% 的完成进度）
- 从 `.orchestrator/status.json` 中获取的最终关卡总结
- 测试结果总结及未解决的风险
- 部署相关信息和回滚方案
- 下一次迭代的待办事项列表

如果仍有障碍存在，应将项目状态标记为 `PARTIAL_COMPLETE`，并明确列出障碍及其负责人。