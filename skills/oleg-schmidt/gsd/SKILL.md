---
name: gsd
description: **高效完成任务——完整的项目规划与执行工作流程**  
该流程涵盖项目初始化的各个环节，包括深入收集项目相关信息、自动化研究、制定项目路线图、分阶段规划以及执行过程中的验证工作。
user-invocable: true
---

## 目标  
GSD（Get Shit Done）提供了一个完整的工作流程，帮助项目从构思到实施，涵盖系统化的规划、研究和分阶段开发。  

**该工作流程完全移植自Claude Code**，包括以下内容：  
- 深度提问和背景信息收集  
- 自动化的领域研究（同时有4个并行研究团队）  
- 需求定义和范围界定  
- 带有阶段结构的路线图制定  
- 分阶段规划及研究验证  
- 基于波状的并行执行  
- 以目标为导向的验证过程  

这是一个完整的GSD系统，而非简化版本。  

## 用户交互界面  
您想执行什么操作？  

**核心工作流程命令：**  
- `new-project`：初始化新项目，包括深度背景信息收集、研究、需求分析和路线图制定  
- `plan-phase [N]`：为某个阶段创建执行计划（可选包含研究）  
- `execute-phase [N]`：以波状并行方式执行该阶段的全部计划  
- `progress`：检查项目进度，并智能地引导用户进行下一步操作  
- `debug [issue]`：进行系统化的调试，支持在上下文重置后保持数据持久性  
- `quick`：执行临时任务，享受GSD提供的保障机制，但可跳过可选的代理步骤  
- `discuss-phase [N]`：通过适应性提问收集信息，为规划做准备  
- `verify-work [N]**：通过对话式用户验收测试（UAT）验证已开发的功能  
- `map-codebase`：分析现有代码库，适用于改造型项目（brownfield projects）  
- `pause-work`：在阶段中途暂停项目  
- `resume-work`：在保留全部上下文的情况下恢复项目执行  
- `add-todo [desc]`：记录想法或任务以备后续处理  
- `check-todos [area]`：列出待办事项并进行处理  
- `add-phase <desc>`：在里程碑末尾添加新阶段  
- `insert-phase <after> <desc>`：插入紧急的阶段  
- `remove-phase <N>`：删除未来的阶段并重新编号  
- `new-milestone [name]`：启动新的里程碑周期  
- `complete-milestone <ver>`：归档里程碑并添加标签  
- `audit-milestone [ver]`：验证里程碑是否完成  
- `settings`：配置工作流程选项和模型设置  

**标志参数：**  
- `plan-phase [N] --research`：在规划前强制重新进行研究  
- `plan-phase [N] --skip-research`：跳过研究，直接进行规划  
- `plan-phase [N] --gaps`：在验证发现问题后进入间隙修复模式  
- `plan-phase [N] --skip-verify`：跳过计划验证环节  
- `execute-phase [N] --gaps-only`：仅执行间隙修复相关的计划  

**使用方法：**  
- `/gsd new-project`：启动新项目  
- `/gsd plan-phase 1`：规划第1阶段  
- `/gsd execute-phase 1`：执行第1阶段  
- `/gsd progress`：查看项目进度及下一步行动  
- `/gsd debug "button doesn't work"`：开始调试会话  
- `/gsd quick`：执行临时任务，简化流程  
- 或者直接告知您的需求，我们会引导您完成相应的操作  

**GSD的功能：**  
1. **深度提问**：通过对话了解您的开发目标  
2. **研究**：同时有4个研究团队并行调查技术领域（技术栈、功能、架构、潜在问题）  
3. **需求分析**：通过功能选择确定需求范围（v1版本）  
4. **路线图制定**：根据需求推导出阶段安排  
5. **阶段规划**：创建包含任务、依赖关系和验证步骤的可执行计划  
6. **执行**：以波状方式并行执行计划，并对每个任务进行提交  
7. **验证**：将需求与实际代码库进行对比，确保满足必要条件  

## 路由逻辑  
根据用户输入，系统会引导用户进入相应的工作流程：  

| 意图 | 对应工作流程 |  
|--------|----------|  
| “new project”, “initialize”, “start project” | workflows/new-project.md |  
| “new-project”（明确请求） | workflows/new-project.md |  
| “plan phase”, “plan-phase”, “create plan” | workflows/plan-phase.md |  
| “execute phase”, “execute-phase”, “start work” | workflows/execute-phase.md |  
| “progress”, “status”, “where am I” | workflows/progress.md |  
| “debug”, “investigate”, “bug”, “issue” | workflows/debug.md |  
| “quick”, “quick task”, “ad-hoc” | workflows/quick.md |  
| “discuss phase”, “discuss-phase”, “context” | workflows/discuss-phase.md |  
| “verify”, “verify-work”, “UAT”, “test” | workflows/verify-work.md |  
| “map codebase”, “map-codebase”, “analyze code” | workflows/map-codebase.md |  
| “pause”, “pause-work”, “stop work” | workflows/pause-work.md |  
| “resume”, “resume-work”, “continue” | workflows/resume-work.md |  
| “add todo”, “add-todo”, “capture” | workflows/add-todo.md |  
| “check-todos”, “check-todos”, “todos”, “list todos” | workflows/check-todos.md |  
| “add phase”, “add-phase” | workflows/add-phase.md |  
| “insert phase”, “insert-phase”, “urgent phase” | workflows/insert-phase.md |  
| “remove phase”, “remove-phase”, “delete phase” | workflows/remove-phase.md |  
| “new milestone”, “new-milestone”, “next milestone” | workflows/new-milestone.md |  
| “complete-milestone”, “complete-milestone”, “archive” | workflows/complete-milestone.md |  
| “audit-milestone”, “audit-milestone”, “audit” | workflows/audit-milestone.md |  
| “settings”, “config”, “configure” | workflows/settings.md |  

## 系统架构  
**工作流程文件**位于`workflows/`目录下：  
- `new-project.md`：完整的项目初始化流程  
- `plan-phase.md`：包含研究和验证的分阶段规划  
- `execute-phase.md`：负责波状执行的协调工具  
- `progress.md`：检查项目进度并智能引导下一步操作  
- `debug.md`：提供系统化的调试功能，支持数据持久性  
- `quick.md`：执行临时任务，简化流程  
- `discuss-phase.md`：通过适应性提问收集信息  
- `verify-work.md`：通过对话式用户验收测试验证功能  
- `map-codebase.md`：分析现有代码库  
- `pause-work.md`：在阶段中途暂停项目  
- `resume-work.md`：在保留全部上下文的情况下恢复项目  
- `add-todo.md`：记录想法或任务  
- `check-todos.md`：列出待办事项  
- `add-phase.md`：在里程碑末尾添加新阶段  
- `insert-phase.md`：插入紧急阶段  
- `remove-phase.md`：删除未来的阶段并重新编号  
- `new-milestone.md`：启动新的里程碑周期  
- `complete-milestone.md`：归档里程碑并添加标签  
- `audit-milestone.md`：验证里程碑是否完成  
- `settings.md`：配置工作流程选项  

**代理文件**位于`agents/`目录下：  
- `gsd-project-researcher.md`：研究技术领域（技术栈、功能、架构、潜在问题）  
- `gsd-phase-researcher.md`：研究如何实现特定阶段  
- `gsd-research-synthesizer.md`：将并行研究结果整合成统一的总结报告  
- `gsd-roadmapper.md`：根据需求制定路线图  
- `gsd-planner.md`：为每个阶段创建详细的执行计划  
- `gsd-plan-checker.md`：在执行前验证计划是否能够达成阶段目标  
- `gsd-executor.md`：逐个任务执行计划  
- `gsd-verifier.md`：通过代码库验证阶段目标是否实现  
- `gsd-debugger.md`：使用科学方法排查错误，并保持数据持久性  
- `gsd-codebase-mapper.md`：分析现有代码库  
- `gsd-integration-checker.md`：验证跨阶段的集成和端到端流程  

**参考文件**位于`references/`目录下：  
- `questioning.md`：深度提问技巧和背景信息检查清单  
- `ui-brand.md`：用户界面/用户体验原则和品牌指南  

**模板文件**位于`templates/`目录下：  
- `project.md`：项目模板  
- `requirements.md`：需求文档模板  
- `research-project/**`：研究输出模板（涵盖技术栈、功能、架构、潜在问题、总结报告等）  

**工作流程模式**  
GSD采用“协调器+子代理”模式：  
1. **协调器**（工作流程核心）：负责整体流程管理，调度子代理  
2. **子代理**（具体任务执行者）：在新的上下文中执行任务，并返回结构化结果  
3. **迭代流程**：通过规划者→验证者→规划者的循环进行验证，直到满足质量标准  

**成功标准：**  
- 用户能够通过`/gsd new-project`命令初始化新项目  
- 完整的工作流程包括提问、研究、需求分析、路线图制定  
- 分阶段规划包含研究和验证环节  
- 阶段执行采用波状并行方式  
- 验证过程会检查实际代码是否符合需求  
- 生成`.planning/`目录下的所有相关文件  
- 每个阶段都会提供明确的下一步操作指南