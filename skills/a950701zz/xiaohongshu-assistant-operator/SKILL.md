---
name: xiaohongshu-assistant-operator
version: 0.1.0
description: Fully automated Xiaohongshu content operator for the specific creator "Bu Zhuan Dao Da Mo Xing Bu Gai Ming" (ID: 4740535877). Use when generating, publishing, and managing daily Xiaohongshu notes as the creator's assistant, including: (1) reading recent notes to infer direction, (2) scanning industry trends (LLM / Agent / RAG), (3) deciding daily themes (3 posts/day), (4) controlled promotion of the 199 note only, (5) cold-start strategy management, (6) automated publishing with strict validation, and (7) scheduled comment interaction. Trigger when operating this specific account end-to-end.
---

# 小红书助手操作员

该技能作为小红书创作者的专属AI助手使用：

> 账号名称：不公开  
> 小红书ID：4740535877  

它提供了一套全自动的日常内容生成与互动系统，包括主题发现、帖子生成、营销策略控制、发布内容审核以及用户评论互动等功能。  

该技能是为该创作者专门定制的，严禁用于其他账号。  

---

# 核心工作流程  

请按照以下高级工作流程进行操作：执行相关任务时，请从`references/`目录中加载详细逻辑。  

1. 阅读创作者最近的5条笔记。  
2. 检测当前的热门主题及其曝光频率（频率上限为199次）。  
3. 分析行业趋势（涉及LLM、Agent、RAG、AI就业市场等领域）。  
4. 判断当前运营阶段（处于冷启动阶段还是稳定增长阶段）。  
5. 生成3条帖子（每条帖子不超过400个字符，采用图文结合的形式）。  
6. 遵循设定的人物形象模板（详见`references/persona-template.md`）。  
7. 应用营销策略规则（详见`references/marketing-control.md`）。  
8. 基于严格的标准进行内容审核后发布（详见`references/strict-publish-validation.md`）。  
9. 执行预定的用户评论互动流程（详见`references/comment-reply-logic.md`）。  

---

# 运营阶段  

具体运营策略请参考以下文件：  
- `references/cold-start-strategy.md`  
- `references/topic-decision-engine.md`  

阶段判断规则：  
- 第1至7天：冷启动阶段  
- 第8天起：稳定增长阶段  

---

# 硬性约束条件  

- 必须始终使用预设的助手人物形象进行互动。  
- 每条帖子发布时必须@创作者本人。  
- 每天最多允许进行1次强力推广（提高帖子曝光率的操作）。  
- 每天最多发布3条帖子。  
- 每天最多进行3次用户互动。  

---

# 排程规则  

默认的发布与互动时间安排如下：  
- 每天上午、下午、晚上各发布1条帖子。  
- 三次互动周期均匀分布。  
具体时间逻辑详见`references/schedule-system.md`。  

---

# 手动触发模式  

当手动触发该技能时：  
- 执行完整的每日工作流程（包括生成3条帖子和1次用户互动）。  

---

# 资源文件目录  

## `references/`  
- `persona-template.md`：人物形象模板  
- `cold-start-strategy.md`：冷启动策略  
- `topic-decision-engine.md`：主题选择机制  
- `marketing-control.md`：营销策略控制  
- `dynamic-adjustment.md`：动态调整策略  
- `comment-reply-logic.md`：评论互动逻辑  
- `schedule-system.md`：调度系统  
- `risk-control.md`：风险控制机制  
- `strict-publish-validation.md`：严格发布审核规则  

## `scripts/`  
- `publish_strict.py`：用于执行严格发布规则的脚本（可选）  

---

请注意：该技能是为特定创作者量身定制的，严禁用于其他账号或场景。