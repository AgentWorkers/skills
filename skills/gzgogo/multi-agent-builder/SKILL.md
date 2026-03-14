---
name: multi-agent-builder
description: 在 OpenClaw 中，根据用户的需求（例如“创建一个产品工程团队”或“组建一个市场运营团队”）来构建一个可重用的多代理团队。当用户需要进行角色分析、角色确认、为每个代理制定创建计划、制定协作协议、设计交接流程以及准备渠道绑定清单时，可以使用此功能。在整个交互过程中以及输出结果中，都会保持与用户使用的语言（英语/中文/其他语言）一致。
---
# 团队构建器（Team Builder）

## 概述  
设计并组建一个多智能体团队，明确各成员的职责、具备依赖关系感知的工作流程以及可靠的协作规则。首先进行角色识别，与用户确认团队范围，然后生成一份可立即实施的团队计划。

## 工作流程  

### 1) 识别用户语言并捕获任务需求  
- 检测并识别用户使用的语言。  
- 遵循 `references/dialog-flow.md` 中提供的“最小化问题数量”的策略。  
- 仅询问缺失的信息：团队目标、预期成果、约束条件（时间线、工具、合规性要求）以及偏好的沟通渠道。  
- 如果用户的需求较为模糊，先提出一个默认的运作模式，再进一步细化。  
- 重用 `references/language-templates.md` 中的语言提示模板。  

### 2) 提出完整的角色列表（让用户进行筛选）  
- 为任务生成一份全面且实用的角色目录。  
- 确保包含 `team-leader`（团队领导者）这一核心角色。  
- 应用 `references/dialog-flow.md` 中提供的自动补全功能及避免过度设计的规则。  
- 根据 `references/splitting-principles.md` 中的准则来决定角色是否需要拆分或合并。  
- 将角色标记为：  
  - **核心角色**（必需）  
  - **可选角色**（取决于具体情境）  
  - **当前不需要**（待后续处理）  
- 在确认角色时，仅显示角色名称和职责（此时不显示智能体ID）。  
- 在执行任何构建步骤之前，请求用户确认角色的增减。  
- 角色建议可参考 `references/role-catalog.md` 中的模板。  
- 最终创建报告中才会显示：角色名称 + 智能体ID + 职责内容。  

### 3) 定义每个智能体的职责  
对于每个已确认的角色，需定义以下内容：  
- 智能体ID（稳定、简短、使用小写字母和下划线连接）  
- 团队领导者的ID必须以 `<team>` 为前缀（例如：`<team>-team-leader`）  
- 角色的具体任务  
- 所需输入的数据  
- 产生的输出结果  
- 决策权限  
- 上游/下游的依赖关系  
- 升级处理的目标对象  

使用 `references/output-templates.md` 中的表格格式进行记录。  

### 4) 明确协作协议  
不要依赖模糊的“共同协作”指令，而应具体规定：  
- 任务分配的详细信息（目标、背景、交付物、截止日期）  
- 状态标识（`accepted`、`blocked`、`done`）  
- 完成后的反馈机制（必须明确告知任务分配者）  
- 长期任务的更新频率  
- 超时/重试/升级策略  
- 输出格式要求（仅提供摘要和文件路径）  
- 进程中的透明度：显示每个阶段正在处理的任务内容  

参考 `references/collaboration-protocol.md` 来制定详细的协作规则。  

### 5) 生成执行所需的包  
返回一个可用于实际操作的完整包，包括：  
1. 团队成员名单及职责分配  
2. 智能体之间的交互流程（按顺序排列的步骤）  
3. 协作协议的详细说明  
4. 需要创建/更新的文件（包括SOUL/AGENTS/IDENTITY相关的指导信息）  
5. 资源配置计划（每个角色所需的工具/权限）  
6. 团队创建报告（必填项；包含各阶段的交付物、路径及安全检查总结）  
7. 通道绑定方案（报告生成后自动提供）  
8. 简单的端到端验证脚本  

**强制执行的步骤（通过程序方式，而非仅依赖提示）：**  
- 运行入口脚本：`scripts/create_team.mjs`  
- 该脚本必须依次执行以下步骤：`materialize` → `validate` → `emit_report`  
- 如果验证结果为“未准备好”，则返回“部分准备好”或“阻塞”状态，并停止后续流程。  
**必须执行**：使用 `references/materialization-checklist.md` 进行创建后的检查。  
**注意**：如果角色相关的文件仍为占位符，切勿将团队标记为“已准备好”。  

参考使用的文档包括：  
- `references/capability-matrix.md`  
- `references/permission-profiles.md`  
- `references/provisioning-playbook.md`  
- `references/final-deliverable-sample.md`  
- `references/channel-binding-blueprints.md`  
- `references/materialization-checklist.md`  

### 6) 确保安全执行  
在采取任何可能产生外部影响的操作之前，需遵循以下确认流程：  
- 对于内部设置（如更新 `openclaw.json` 中的智能体信息），无需额外确认；  
- 设置智能体之间的权限（A2A/子智能体权限）无需确认；  
- 但对于通道绑定或机器人凭证等具有不可逆影响的操作，则必须获得用户确认。  
在安装技能之前，先进行安全检查，并阻止高风险操作。  
**创建过程中严禁自动重启系统**；如需重启，请先征求用户同意或提供手动重启指导。  
如果存在任何不确定之处，暂停操作并询问用户。  

### 7) 故障处理与恢复  
当设置或协作过程中出现问题时，参照 `references/failure-modes.md` 进行处理。  
优先选择快速恢复方案，以尽量减少影响范围：  
- 保留已完成的工作  
- 从上一个检查点恢复  
- 保持用户状态的准确性（标记为“已准备好”或“部分准备好”）  
- 绝不自动安装未通过安全检查的技能。  

## 质量标准：  
- 优先选择职责边界清晰的角色，而非职责重叠的角色过多。  
- 每个角色都应具有可衡量的输出结果。  
- 每个依赖关系都应有明确的处理路径。  
- 交付物必须能够被操作者立即执行。  
- 角色文档应足够详细，能够准确描述专家级别的操作内容（而非简化的占位符）。  
- 团队领导者仅负责协调工作，不应直接生成专业性的成果。  
- 所有专业性成果必须保存在团队共享目录中。  
当用户需求与已知团队模板匹配时，可重用 `references/examples.md` 中的模板。  

## 创建阶段的详细步骤  
在确认角色信息后，严格按照 `references/create-playbook.md` 的步骤进行操作。  
使用 `references/snippet-templates.md` 生成可重复使用的代码片段。  
最终的用户交付文档格式参考 `references/final-deliverable-sample.md`。  

## 参考资源：  
- `references/role-catalog.md`：跨领域的角色模板集。  
- `references/role-display-mapping.json`：根据用户语言显示角色的名称。  
- `references/dialog-flow.md`：用于角色识别的最小化问题策略及自动补全功能。  
- `references/language-templates.md`：支持多语言的提示模板。  
- `references/splitting-principles.md`：判断何时需要拆分或合并角色的准则。  
- `references/examples.md`：常见团队架构的端到端示例。  
- `references/channel-binding-blueprints.md`：单机器人团队与多机器人团队的绑定方案及配置指南。  
- `references/capability-matrix.md`：角色与工具/技能之间的映射关系。  
- `references/permission-profiles.md`：最小权限配置方案。  
- `references/provisioning-playbook.md`：自动安装及权限设置流程（包含安全扫描功能）。  
- `references/security-report-schema.md`：机器可读的安全报告及安装决策模板。  
- `references/collaboration-protocol.md`：明确的多智能体协作协议。  
- `references/output-templates.md`：最终输出的格式模板及检查清单。  
- `references/create-playbook.md`：完整的创建流程指南。  
- `references/snippet-templates.md`：可重复使用的代码片段。  
- `references/role-soul-blueprints.md`：针对每个角色的详细操作指南。  
- `references/team-leader-template.md`：固定的团队领导者模板（创建时复制）。  
- `references/team-leader-agents-template.md`：固定的团队领导者与智能体之间的交互模板（创建时复制）。  
- `references/final-deliverable-sample.md`：标准化的用户交付格式。  
- `references/failure-modes.md`：故障处理方案及恢复措施。  
- `references/materialization-checklist.md`：创建完成后对角色文件的检查清单。  
- `references/config-materialization-checklist.md`：确保 `openclaw.json` 中的配置信息完整无误。