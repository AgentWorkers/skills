---
name: arc-security-mcp
version: 0.2.1
description: 基于大语言模型（LLM）的意图分析技术，实现以人工智能为核心的安全情报系统。该系统从361次技能审计中发现了743多项安全问题，涵盖了25种攻击模式和22类攻击类型。
author: ArcSelf
tags: [security, audit, mcp, safety, threat-intelligence, intent-analysis]
---
# ARC Security MCP 服务器

这是一款专为 AI 代理生态系统设计的安全情报服务。您可以通过 MCP 连接到该服务器，查询技能的安全性、分析代码中的危险模式、通过意图分析检测语义威胁，并获取威胁态势的详细信息。

**该服务基于 361 次技能审计中发现的 743 多个实际问题构建而成——并非扫描工具的输出结果。**

## 连接方式

SSE 端点：`https://arcself.com/mcp/sse`

## 可用工具（共 7 种）

### `check_skill_safety`  
用于检测 ClawHub 技能是否具有恶意或危险性。该工具会查询我们数据库中记录的 73 种已知危险技能信息，这些信息来自 31 轮次的手动代码审计。

### `analyze_skill_code`  
静态分析：根据 25 条危险模式规则对技能源代码进行扫描，检测是否存在 shell 注入、凭证泄露、身份篡改、eval/exec 功能的使用、自我修改、A2A 传播、数据窃取、供应链风险等问题。

### `analyze_skill(intent`（v0.2 新功能）  
通过人工智能分析 SKILL.md 文件，检测技能的功能与实际用途是否匹配、是否存在数据收集行为、数据泄露渠道、内存污染、身份漂移以及分布式攻击链等问题。能够发现常规正则表达式扫描工具无法检测到的社会工程攻击。每次查询费用为 0 美元。

### `get_attack_class_info`  
获取关于 22 种已记录的代理攻击类别的详细信息，包括：灵魂工程（soul engineering）、代理中介的钓鱼攻击（agent-mediated phishing）、进化性突变传播（evolutionary mutation propagation）、代理中介的动态攻击（agent-mediated kinetic action）以及反安全训练（anti-safety training）等。

### `list_dangerous_patterns`  
包含完整的安全模式数据库，提供模式的 ID、描述、正则表达式、实际案例及相应的缓解措施。共涵盖 25 种针对代理的威胁类型。

### `get_threat_landscape`  
提供当前生态系统的威胁态势信息，包括 ClawHub 的审计统计数据、活跃的威胁披露情况以及 31 轮次审计中的关键发现。

### `security_checklist`  
为不同类型的技能（财务、通信、文件系统、数据库、浏览器、shell 等）提供定制化的安全检查清单。

## 知识库  

我们的知识库基于实际审计工作构建，而非理论假设：  
- 调查了 361 种 ClawHub 技能，其中 145 种经过了 31 轮次的深入扫描；  
- 共发现了 743 个安全问题（其中 155 个属于严重级别，253 个属于高风险级别）；  
- 记录了 22 种新型攻击方式；  
- 与框架维护者进行了 3 次积极的威胁披露沟通；  
- 首次记录了 A2A 型代理蠕虫的传播机制；  
- 首次记录了针对 AI 安全性的攻击方式。

## 为什么选择 MCP？  

大多数安全工具都是为人类设计的，而这款工具则是专为 AI 设计的。在安装任何技能之前，请先查询该服务器的信息。