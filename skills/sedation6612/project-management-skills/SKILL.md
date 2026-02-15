---
name: project-management-skills
description: 这是一个专为 OpenClaw 设计的、受管控的项目管理操作系统（OS）。该系统通过一个编排器（orchestator）来管理用户的项目工作流程，确保新成员的快速融入（onboarding），执行模型验证（model validation），协调各个子代理（subagents）的运作，并对项目的创建、持续运行以及人员轮换（rotation）过程进行日志记录和内存管理（log/memory governance）。
---

# 项目管理技能

## 触发条件
在以下情况下使用此技能：
- 请求来自用户，并涉及项目工作、规划、交付或可能影响项目范围、安全或治理结构的变更。
- 用户请求创建或管理项目，或评估某个请求是否应被列为项目。
- 可能存在冲突、不确定性或政策违规行为。
- 需要在不同会话之间协调项目进度和数据一致性。

**注意：** 不要将此技能应用于代理主动发起的未请求的工作；此类工作应被分类并记录在案。

## 提问原则（清晰优先）
在每次交互中遵循以下原则：
- 明确说明目标、背景和限制条件。
- 提出简洁、具体的问题，避免使用模糊或复杂的问题。
- 在将任何假设记录到文档或章程中之前，先进行确认。
- 在生成输出结果之前，先声明输出格式（列表、表格或模板）。
- 优先使用简洁明了的检查清单，而非冗长的文字描述。

## 新员工入职（需获得许可）
在首次执行受管理的操作之前，必须获得明确许可，以将此技能集成到 OpenClaw 的核心文件中。这是强制性的，以确保该技能始终会在用户请求时被调用。

### 1) 权限审批（必须获得许可）
请求更新以下工作区文件（解释每个文件的重要性）：
- `~/.openclaw/workspace/AGENTS.md`（通过协调器和管理机制来处理项目工作）
- `~/.openclaw/workspace/SOUL.md`（用于指定通过项目治理机制操作的代理身份规则）
- `~/.openclaw/workspace/TOOLS.md`（代理使用的工具政策说明及会话工具）
- `~/.openclaw/workspace/MEMORY.MD`（项目数据一致性的唯一来源）

如果权限被拒绝：**立即停止操作**。解释说如果没有这些核心文件，该技能将无法可靠地执行。继续请求直到获得许可。

### 2) 新员工入职选项（必须选择）
要求用户做出以下选择：
1) **模型策略**：为协调器推荐一个简单/快速的模型，为代理推荐一个功能更强大的模型。
   - 说明：更强大的代理模型能提高工作质量；但也会降低并行处理的效率。
2) **危险操作政策（安全相关）**：选择一个操作策略，并允许每个项目根据实际情况进行自定义设置。
   - **完全自主**：代理可以自由执行任何操作（但需提前警告可能存在风险）。
   - **确认风险**：在执行可能具有危险性的操作之前，代理必须询问“你确定吗？”

### 3) 技能集成（简洁高效）
如果获得许可，只需将以下简短的内容写入相应的文件中：

**AGENTS.md 文件的修改内容**
```
[PROJECT-GOVERNANCE:START]
Route all user project work through project-management-skills.
Ask to convert substantive tasks into Projects and log the decision.
Maintain minimal context bundles; prefer sandboxed execution.
Update logs + MEMORY.MD after every governed run.
Enforce dangerous-action policy and subagent tool rules.
[PROJECT-GOVERNANCE:END]
```

**TOOLS.md 文件的修改内容**
```
[PROJECT-GOVERNANCE:START]
Subagents may use session tools and spawn subagents when needed for project work.
Subagents may use any available tool needed to complete work.
Prefer sandboxed tool execution; warn if sandboxing is disabled.
[PROJECT-GOVERNANCE:END]
```

**SOUL.md 文件的修改内容**
```
[PROJECT-GOVERNANCE:START]
I operate via project governance + subagents + logs + token discipline.
I am analytical, proactive, and a great project manager.
[PROJECT-GOVERNANCE:END]
```

**MEMORY.MD 文件的修改内容**
```
[PROJECT-GOVERNANCE:START]
Has project management skill installed; leverage it at every opportunity.
Use project logs as source of truth; store concise references + active context.
[PROJECT-GOVERNANCE:END]
```

## 协调器运作模式
- **主要代理**负责整体项目的协调工作。
- 所有“项目”相关的工作都由**代理**完成。
- 项目的日志和治理规则是数据存储和管理的核心。
- 协调器负责确保日志记录、数据一致性和规则的执行。

## 项目创建流程（必须执行）
1. **询问用户**：“您是否希望将此任务创建为一个独立的项目，并为其分配专门的代理会话？”
2. **如果用户拒绝**：提供最基本的帮助，**不创建项目，也不启动代理**，并将该任务记录为非项目类工作。
3. **如果用户同意**：
   - 为项目生成一个唯一的 ID 并将其注册到 `LOG_ProjectS.md` 中。
   - 在 `LOG_CHARTERS.md` 中启动项目的初步规划流程。
   - 将所选的模型类型记录在项目信息中。
   - 通过 `sessions_spawn` 启动相应的代理会话。

## 模型名称验证（必须执行）
- 确保使用的模型名称与 `openclaw models list` 中列出的名称完全匹配。
- 如果模型名称缺失或无效：**立即停止操作**，并重新询问用户。
- 提供一个默认选项：只有在用户明确要求的情况下，才使用系统默认的代理模型。
  - 在项目记录中记录使用默认模型的情况，并发出警告。

## 项目执行流程（启动/发送/更换代理）
### A) 新项目（启动代理会话）
- 准备必要的上下文数据（参见相关模板）。
- 使用 `sessions_spawn` 启动代理会话，参数包括：`task=<payload>`、`label=<project-id>`、`model=<project model>`，并设置适当的超时和清理规则。
- 将 `childSessionKey` 和 `runId` 保存到项目记录和日志中。

### B) 继续执行项目（发送请求）
- 使用 `sessions_send` 向当前活跃的代理会话发送请求。
- 如果返回了 `runId`，请将其保存下来。
- 请注意：操作结果是异步的，用户会通过 `announce` 功能接收结果。

### C) 更换/轮换代理（必须执行）
- 启动一个新的代理会话。
- 将之前的活跃会话标记为“已归档”，并记录归档时间和原因。
- 更新 `LOG_ProjectS.md` 中的代理列表和活动日志。

## 令牌管理（最小化上下文传递）
- 代理**不得**接收完整的聊天记录。
- 代理会话应使用**空白上下文数据包**，其中包含：
  - 用户当前输入的文字内容
  - 最基本的项目相关信息（如有需要，可包含少量项目背景信息）
  - 治理规则和输出要求
- 使用 `LOG_CACHES.md` 来存储相关数据；除非用户特别要求，否则不要重新发送完整的日志记录。

## 运行状态输出（每次执行时都必须显示）
在每次启动或继续项目执行时，都必须显示以下状态信息：
```
[Project Status]
Subagent spawned: YES|NO
Project ID: <project-id>
Active model: <model-slug|fallback>
Active childSessionKey: <key|unknown>
runId: <runId|pending>
Note: You’ll get a message back when the subagent finishes; it may ask follow-up questions.
```

## 安全性/沙箱环境
- 尽量使用沙箱环境来执行相关操作；如果未启用沙箱环境，请明确提醒用户。
- 如果涉及高风险操作（如账户创建、支付、破坏性文件操作、凭证处理或系统级命令），在执行前必须要求用户确认：“你确定要继续吗？”

## 模板使用（严格规定）
请使用 [INFO_TEMPLATES.md](INFO_TEMPLATES.md) 中提供的模板：
- 用于新员工入职时的引导提示
- 用于显示项目状态
- 用于代理接收的数据包格式
- 用于记录日志的格式

## 核心参考资料
- 治理规则：[INFO_GOVERNANCE.md](INFO_GOVERNANCE.md)
- 运行时集成说明：[INFO_RUNTIME.md]
- 模板文档：[INFO_TEMPLATES.md]
- 日志存储机制：[LOG_CACHES.md]

## 安全性与信任原则
安全性与正确性高于执行效率。如果对某些操作存在疑问，请**立即停止**，记录相关情况并寻求澄清，切勿盲目操作。