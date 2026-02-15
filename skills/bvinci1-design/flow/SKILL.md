---
name: flow
description: 智能技能编排器：能够将自然语言请求转换为安全、可重用的工作流程
---

---

**摘要：**  
智能技能编排器能够将自然语言请求编译成安全、可重用的工作流程（workflows）。  

**标签：**  
- 自动化（Automation）  
- 工作流程（Workflow）  
- 自然语言处理（NLP）  
- 安全性（Security）  
- 编排（Orchestration）  
- 技能构建器（Skill Builder）  
- Clawdbot  
- MCP  

---

# **智能技能编排器（Intelligent Skill Orchestrator）**  
专为 Clawdbot/MCP 设计，可将自然语言请求转化为安全、可重用的工作流程（FLOW）技能。  

## **主要功能：**  
- **解析自然语言请求**：理解用户的需求。  
- **搜索技能库**：查找可重用的技能组件。  
- **安全扫描**：在组合技能前进行安全检查。  
- **组合技能**：将多个技能整合成统一的执行流程（FLOW）。  
- **跟踪技能使用情况**：便于后续重复使用。  
- **依赖关系处理**：通过拓扑排序解决技能间的依赖关系。  

## **工作原理：**  
1. **接收自然语言输入**：用户描述想要构建的功能。  
2. **意图解析**：提取所需的功能、标签及执行步骤。  
3. **查询技能库**：查找符合需求的现有技能。  
4. **安全检测**：检查所有组件的安全性。  
5. **组合技能**：将相关技能整合成可执行的流程。  
6. **保存结果**：将新生成的流程保存以供将来使用。  

## **使用方式：**  
- **交互式模式**  
  （具体实现代码见：```
python flow.py
Flow> Build a web scraper that extracts prices and saves to CSV
```）  

- **命令行界面（CLI）**  
  （具体实现代码见：```bash
python flow.py "Create an automation that monitors API endpoints"
```）  

- **技能列表**  
  （具体实现代码见：```bash
python flow.py --list
```）  

## **安全特性：**  
- **代码执行检测**：监控代码执行行为。  
- **数据泄露检测**：识别数据泄露风险。  
- **加密挖矿行为检测**：防范恶意加密挖矿行为。  
- **系统修改检测**：及时发现系统被篡改的尝试。  
- **基于抽象语法树（AST）的代码分析**：提高安全性。  
- **代码混淆检测**：识别代码混淆技巧。  

## **系统架构：**  
- `flow.py`：核心编排器。  
- `natural_language_parser.py`：用于解析用户意图的自然语言处理模块。  
- `skillregistry.py`：存储可重用技能的数据库。  
- `skill_scanner_integration.py`：负责安全扫描功能。  
- `skill_composer.py`：负责将技能组合成可执行的流程。  

## **系统要求：**  
- Python 3.8 或更高版本。  
- 核心功能无需依赖任何外部库。  

## **作者：**  
@bvinci1-design