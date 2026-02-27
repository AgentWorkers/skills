---
name: agentic-workflow-automation
description: 生成可重用的多步骤代理工作流蓝图。这些蓝图可用于触发器/动作的编排、确定性工作流的定义，以及自动化流程的交接文档。
---
# **代理工作流自动化 (Agentic Workflow Automation)**

## **概述**  
构建工作流蓝图，这些蓝图可以被转换为自动化平台（如 n8n）或内部编排工具（internal orchestrators）可执行的脚本。

## **工作流流程**  
1. 定义工作流的名称、触发条件以及各个步骤的顺序。  
2. 将每个步骤转化为简单的执行契约（execution contract）。  
3. 构建包含依赖关系和执行顺序的工作流蓝图。  
4. 导出 JSON 或 Markdown 格式的工作流文件以供后续实施使用。  

## **使用捆绑资源 (Use Bundled Resources)**  
- 运行 `scripts/generate_workflow_blueprint.py` 命令以生成确定性的工作流输出文件。  
- 阅读 `references/workflow-blueprint-guide.md` 以获取步骤设计的指导信息。  

## **注意事项 (Guardrails)**  
- 确保每个步骤仅用于单一功能。  
- 为失败步骤设置明确的回退机制（fallback behavior）。