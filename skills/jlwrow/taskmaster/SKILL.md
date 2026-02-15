---
name: taskmaster
description: 项目经理与任务分配系统：当您需要将复杂的工作分解为更小的任务时，可以根据任务的复杂性分配相应的AI模型，创建子代理以实现并行执行，跟踪进度，并管理代币预算。该系统非常适合研究项目、多步骤工作流程，或者当您希望将常规任务委托给成本较低的模型，同时自己负责复杂的协调工作时使用。
---

# TaskMaster：人工智能项目管理系统与任务分配工具  
通过智能的模型选择和子代理协调机制，将复杂的项目转化为可管理的工作流程。  

## 核心功能  

**🎯 智能任务分类**  
- 分析任务复杂性，选择合适的模型（Haiku/Sonnet/Opus）  
- 将大型项目分解为更小、更易于管理的任务  
- 避免过度设计（简单的网络搜索任务无需使用Opus模型）  

**🤖 子代理协调**  
- 创建具有特定模型限制的独立子代理  
- 并行执行任务以提高完成速度  
- 将结果整合为连贯的交付物  

**💰 预算管理**  
- 记录每个任务的代币成本及项目总成本  
- 设置预算限制以防止开支失控  
- 优化模型选择以提升成本效益  

**📊 进度跟踪**  
- 实时显示所有活跃任务的进度  
- 失败的任务会自动重试，并由人工进行审核  
- 最终生成统一的交付物  

## 快速入门  

### 1. 基本任务分配  
```markdown
TaskMaster: Research PDF processing libraries
- Budget: $2.00
- Priority: medium
- Deadline: 2 hours
```  

### 2. 复杂项目分解  
```markdown
TaskMaster: Build recipe app MVP
- Components: UI mockup, backend API, data schema, deployment
- Budget: $15.00
- Timeline: 1 week
- Auto-assign models based on complexity
```  

## 模型选择规则  

**Haiku（0.25美元/1.25美元）** – 简单、重复性任务：  
- 网络搜索与信息汇总  
- 数据格式化与提取  
- 基本文件操作  
- 状态检查与监控  

**Sonnet（3美元/15美元）** – 大多数开发工作：  
- 研究与分析  
- 代码编写与调试  
- 文档编写  
- 技术设计  

**Opus（15美元/75美元）** – 复杂的推理任务：  
- 架构决策  
- 创造性问题解决  
- 代码审查与优化  
- 战略规划  

## 高级用法  

### 自定义模型选择  
在您更了解任务需求时，可覆盖自动模型选择机制：  
```markdown
TaskMaster: Debug complex algorithm [FORCE: Opus]
```  

### 并行执行  
同时运行多个任务：  
```markdown
TaskMaster: Multi-research project
- Task A: Library comparison
- Task B: Performance benchmarks  
- Task C: Security analysis
[PARALLEL: true]
```  

### 预算控制  
设置支出限制：  
```markdown
TaskMaster: Market research
- Max budget: $5.00
- Escalate if >$3.00 spent
- Stop if any single task >$1.00
```  

## 关键资源  

- **模型选择**：详见 [references/model-selection-rules.md](references/model-selection-rules.md) 中的复杂性指南  
- **任务模板**：参考 [references/task-templates.md](references/task-templates.md) 中的常见任务模板  
- **任务分配引擎**：使用 `scripts/delegate_task.py` 实现核心协调逻辑  

## 实施说明  

**会话管理**：每个子代理都拥有独立的会话环境，并遵循特定的模型限制；除非另有设计，否则各子代理之间不会互相通信。  
**错误处理**：失败的任务在Sonnet模型下会自动重试一次，之后会转交人工审核。  
**结果整合**：TaskMaster会将所有子代理的结果整合为用户可用的统一交付物。  
**代币监控**：实时跟踪成本，并在接近预算限制时发出警报。