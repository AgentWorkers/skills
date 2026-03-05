# SKILL.md: 人工智能训练师与学习专家

## 概述  
该技能使助手能够自主从在线资源中学习，提炼复杂的文档内容（如 Anthropic Skilljar 或 MCP 指南），并将这些知识整合到系统的长期记忆（MEMORY.md）和操作规则（AGENTS.md）中。

## 功能  
- **深度网络数据获取（Deep Web Fetching）**：递归地获取并总结多页文档内容。  
- **知识提炼（Knowledge Distillation）**：从技术文档中提取核心信息、使用模式和工具使用策略。  
- **系统集成（System Integration）**：利用新获得的见解自动更新工作空间规则（AGENTS.md）和系统记忆（MEMORY.md）。  
- **路由优化（Routing Optimization）**：根据任务的复杂性，建议选择合适的模型（例如本地 Ollama 或云端模型）。  

## 使用指南  
- **优先规划预算（Budget First）**：在获取大型文档资源时，务必预估潜在的token使用量，并在操作前获得 Alvin 的许可。  
- **隐私保护（Privacy Protection）**：学习到的数据应存储在本地工作空间中；切勿记录文档中的敏感环境变量或密钥。  
- **验证机制（Validation）**：在学习新概念（如新的 MCP 工具模式）后，需验证其是否与当前版本的 OpenClaw 兼容，再决定是否实施。  

## 允许使用的工具  
- `web_search`：查找最新版本的文档。  
- `web_fetch`：从技术网站中提取 markdown 格式的内容。  
- `edit`/`write`：更新系统配置和记忆文件。  
- `exec`：验证本地环境状态（例如 Ollama 的版本信息、节点版本等）。  

## 成功指标  
- 成功地将新的技术概念整合到系统记忆（MEMORY.md）中。  
- 通过应用新学到的“技能”模式优化了任务流程。  
- 通过将简单任务卸载到本地模型上，减少了云资源的消耗（降低了云 token 的使用量）。