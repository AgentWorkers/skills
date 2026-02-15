---
name: antigravity-swarm
description: 在 Antigravity IDE 中部署自主子代理以执行任务。支持手动调度以及动态的“自动雇佣”代理团队机制。
---

# **反重力子代理技能**  
（Antigravity Subagents Skill）  

该技能允许您派遣自主子代理来执行任务。它包含一个**管理器**层（`planner.py`），能够为复杂任务自动组建代理团队；以及一个**编排器**层（`orchestrator.py`），用于可视化地运行这些代理。这两个脚本默认都支持**计划模式**（需要用户确认），以防止意外使用导致资源消耗过多。  

> [!警告！]  
> **在编排器运行期间，请勿修改该目录中的文件。**  
> 系统会频繁读写 `task_plan.md`、`findings.md` 和 `subagents.yaml` 文件。  
> 在执行过程中进行手动编辑可能会导致竞态条件或代理行为异常。  

## 🛠 工具  

### `dispatch_subagent`  
用于运行具有特定任务的子代理。  

**用法：**  
当您有可并行化的任务，或者需要将某项具体工作分配给子代理时（例如：“编写测试文件”、“分析这个目录”），请使用此工具。  

**参数：**  
- `task`：对子代理应执行任务的清晰、完整的描述。  

**实现细节：**  
子代理由 `gemini` 命令行工具（CLI）驱动。Python 封装层会拦截特定的输出格式，从而执行文件系统操作和命令执行。  

**子代理使用的命令格式（自动处理）：**  
- `<<WRITE_FILE path="...">>...<<END_WRITE>>`  
- `<<RUN_COMMAND>>...<<END_COMMAND>>`  

### `run_mission`（动态编排）  
用于分析高层次的任务目标，雇佣定制的子代理团队，并为它们生成配置。  

**用法：**  
适用于需要执行多个步骤的复杂项目，您无需手动为每个子代理指定具体任务。  

**参数：**  
- `mission`：项目的整体描述（例如：“用 Python 创建一个蛇形游戏”）。  

**工作原理：**  
1. 调用 `scripts/planner.py` 生成 `subagents.yaml` 文件（除非使用 `--yes` 参数，否则会提示用户确认）。  
2. （可选）随后可以运行 `scripts/orchestrator.py` 来执行代理团队（同样需要用户确认）。  

## 使用模式  

### 模式 1：命令行用户（终端可视化）  
在终端中运行 Python 编排器，以查看图形用户界面（TUI）。  
```bash
python scripts/orchestrator.py
```  

### 模式 2：集成开发环境（IDE）代理（聊天可视化）  
作为代理，您可以充当编排者的角色：  
1. **启动子代理**：使用 `run_command` 在后台启动子代理；使用 `--format json` 选项可生成日志。  
    ```bash
    python scripts/dispatch_agent.py "Task A" --log-file logs/agent_a.json --format json &
    python scripts/dispatch_agent.py "Task B" --log-file logs/agent_b.json --format json &
    ```  
2. **监控**：定期检查 JSON 日志文件，查找 `{"type": "status", "content": "completed"}` 条目。  
3. **可视化**：在聊天响应中向用户展示 Markdown 格式的任务进度面板。  

## 🚀 示例  

### 1. 手动派遣单个子代理  
```python
run_command("python3 scripts/dispatch_agent.py 'Create a file named hello.py that prints Hello World'")
```  

### 2. 自动组建代理团队（任务模式）  
```python
# 1. Generate the team
run_command("python3 scripts/planner.py 'Create a fully functional Todo List app in HTML/JS'")

# 2. Run the team
run_command("python3 scripts/orchestrator.py")
```  

> [!警告！]  
> 请确保使用 `gemini-3-pro` 或 `gemini-3-flash` 版本。旧版本可能无法正确支持文件协议。  

## ❓ 常见问题与设计理念  

### 为什么使用子代理？  
1. **上下文隔离**：避免“上下文污染”——UI 专业人员无需查看具体的数据库迁移代码，从而提高准确性。  
2. **可扩展性**：基于循环的代理按顺序执行任务，而子代理则设计为在并行线程中运行。  
3. **容错性**：如果某个子代理失败（例如因语法错误），整个任务不会崩溃；编排器可以仅重新尝试该子代理。  

### 这真的是并行处理吗？  
是的。`orchestrator.py` 使用 Python 的 `threading.Thread` 为每个代理创建独立的操作系统进程。  
> **注意**：如果底层 `gemini` CLI 工具存在全局锁机制，或者您触发了 API 使用率限制，可能会观察到任务按顺序执行。  

### 使用文件进行任务规划（手动协议）  
该技能遵循“手动”状态管理的设计理念：所有代理都在工作区根目录下的共享文件集中进行操作：  
- `task_plan.md`：任务清单的权威来源。  
- `findings.md`：用于记录发现结果和调研内容的共享临时文件。  
- `progress.md`：记录已完成步骤和当前状态的日志文件。