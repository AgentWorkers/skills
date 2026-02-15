---
name: agent-orchestrator
description: |
  Meta-agent skill for orchestrating complex tasks through autonomous sub-agents. Decomposes macro tasks into subtasks, spawns specialized sub-agents with dynamically generated SKILL.md files, coordinates file-based communication, consolidates results, and dissolves agents upon completion.

  MANDATORY TRIGGERS: orchestrate, multi-agent, decompose task, spawn agents, sub-agents, parallel agents, agent coordination, task breakdown, meta-agent, agent factory, delegate tasks
---

# 代理编排器（Agent Orchestrator）

通过将复杂任务分解为子任务、创建自主的子代理，并整合它们的工作来协调这些任务。

## 核心工作流程（Core Workflow）

### 第1阶段：任务分解（Task Decomposition）

分析宏观任务，并将其分解为独立且可并行执行的子任务：

```
1. Identify the end goal and success criteria
2. List all major components/deliverables required
3. Determine dependencies between components
4. Group independent work into parallel subtasks
5. Create a dependency graph for sequential work
```

**分解原则（Decomposition Principles）：**
- 每个子任务都应该能够独立完成。
- 尽量减少代理之间的依赖关系。
- 优先选择范围更广、更自主的任务，而非依赖性强的任务。
- 为每个子任务设定明确的成功标准。

### 第2阶段：代理生成（Agent Generation）

为每个子任务创建一个子代理工作空间：

```bash
python3 scripts/create_agent.py <agent-name> --workspace <path>
```

这将生成：
```
<workspace>/<agent-name>/
âââ SKILL.md          # Generated skill file for the agent
âââ inbox/            # Receives input files and instructions
âââ outbox/           # Delivers completed work
âââ workspace/        # Agent's working area
âââ status.json       # Agent state tracking
```

**动态生成SKILL.md文件**，其中包含以下内容：  
- 代理的具体角色和目标  
- 所需的工具和能力  
- 输入/输出规范  
- 成功标准  
- 通信协议  

有关预构建的模板，请参阅 [references/sub-agent-templates.md](references/sub-agent-templates.md)。

### 第3阶段：代理调度（Agent Dispatch）

通过以下步骤初始化每个代理：  
1. 将任务指令写入 `inbox/instructions.md`。  
2. 将所需的输入文件复制到 `inbox/` 目录中。  
3. 将 `status.json` 文件的状态设置为 `{"state": "pending", "started": null}`。  
4. 使用 Task 工具启动代理：

```python
# Spawn agent with its generated skill
Task(
    description=f"{agent_name}: {brief_description}",
    prompt=f"""
    Read the skill at {agent_path}/SKILL.md and follow its instructions.
    Your workspace is {agent_path}/workspace/
    Read your task from {agent_path}/inbox/instructions.md
    Write all outputs to {agent_path}/outbox/
    Update {agent_path}/status.json when complete.
    """,
    subagent_type="general-purpose"
)
```

### 第4阶段：监控（基于检查点，Checkpoint-based Monitoring）

对于完全自主的代理，几乎不需要进行监控：

```python
# Check agent completion
def check_agent_status(agent_path):
    status = read_json(f"{agent_path}/status.json")
    return status.get("state") == "completed"
```

定期检查每个代理的 `status.json` 文件。代理会在任务完成后更新该文件。

### 第5阶段：整合（Consolidation）

所有代理完成任务后：  
1. 从每个代理的 `outbox/` 目录中收集输出结果。  
2. 根据成功标准验证交付成果。  
3. 根据需要合并或整合输出结果。  
4. 如果多个代理处理了相同的任务，解决可能出现的数据冲突。  
5. 生成所有已完成工作的总结报告。

```python
# Consolidation pattern
for agent in agents:
    outputs = glob(f"{agent.path}/outbox/*")
    validate_outputs(outputs, agent.success_criteria)
    consolidated_results.extend(outputs)
```

### 第6阶段：解散与总结（Dissolution & Summary）

整合完成后：  
1. （可选）归档代理的工作空间。  
2. 清理临时文件。  
3. 生成最终总结报告：  
   - 每个代理完成了哪些工作。  
   - 遇到的任何问题。  
   - 最终交付成果的位置。  
   - 时间/资源使用情况。

```python
python3 scripts/dissolve_agents.py --workspace <path> --archive
```

## 基于文件的通信协议（File-Based Communication Protocol）

有关详细规范，请参阅 [references/communication-protocol.md](references/communication-protocol.md)。

**快速参考（Quick Reference）：**  
- `inbox/`：代理只能读取，由编排器写入。  
- `outbox/`：代理只能写入，由编排器读取。  
- `status.json`：代理用于更新状态（`pending` → `running` → `completed` → `failed`）。

## 示例：研究报告任务（Example: Research Report Task）

```
Macro Task: "Create a comprehensive market analysis report"

Decomposition:
âââ Agent: data-collector
â   âââ Gather market data, competitor info, trends
âââ Agent: analyst
â   âââ Analyze collected data, identify patterns
âââ Agent: writer
â   âââ Draft report sections from analysis
âââ Agent: reviewer
    âââ Review, edit, and finalize report

Dependency: data-collector â analyst â writer â reviewer
```

## 子代理模板（Sub-Agent Templates）

[references/sub-agent-templates.md](references/sub-agent-templates.md) 中提供了常见代理类型的预构建模板：  
- **研究代理（Research Agent）**：网络搜索、数据收集  
- **代码代理（Code Agent）**：代码实现、测试  
- **分析代理（Analysis Agent）**：数据处理、模式识别  
- **写作代理（Writer Agent）**：内容创作、文档编写  
- **审核代理（Review Agent）**：质量保证、编辑  
- **集成代理（Integration Agent）**：合并输出结果、解决冲突  

## 最佳实践（Best Practices）：  
1. **从小规模开始**：先使用2-3个代理，随着模式逐渐清晰再逐步扩展。  
2. **明确职责边界**：每个代理负责特定的交付成果。  
3. **使用结构化的文件进行通信**：确保代理之间的信息传递有条理。  
4. **优雅地处理失败**：代理报告失败情况，由编排器负责恢复。  
5. **记录所有操作**：状态文件有助于调试过程中的问题追踪。