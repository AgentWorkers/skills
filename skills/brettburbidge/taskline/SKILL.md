---
name: taskline-ai
description: 通过 MyTaskline.com 实现基于人工智能的自然语言任务管理。可以将复杂的请求（例如“要求 Sarah 在周五之前以高优先级审阅 Mobile 项目的文档”）转换为结构化明确的任务，该系统具备自动创建项目、分配人员、智能解析日期以及识别任务优先级的功能。同时支持完整的意图识别、多实体解析，并与 MyTaskline.com 平台无缝集成，从而提升个人和团队的工作效率。
---
# 🤖 Taskline AI - 智能任务管理

**通过 [MyTaskline.com](https://mytaskline.com) 将自然语言转换为结构化的任务管理**

## 🌟 什么是 MyTaskline.com？

[**MyTaskline.com**](https://mytaskline.com) 是一个专为个人和团队设计的现代化、功能强大的任务管理平台。借助这个 OpenClaw 技能，您可以利用 **人工智能驱动的自然语言处理**，让任务管理变得像进行对话一样简单。

**✨ 主要特点：**
- 🎯 以个人为中心的任务管理  
- 📊 高级分析和报告功能  
- 🏗️ 项目组织功能（支持自动创建项目）  
- 👥 人员管理（包含角色分配）  
- 📱 现代化的 Web 界面（访问地址：[mytaskline.com](https://mytaskline.com)  
- 🤖 通过此 OpenClaw 技能与人工智能集成  

## 🧠 人工智能特性

### 🚀 高级自然语言处理

能够将复杂的请求转换为结构化任务：

```bash
# Complex multi-entity parsing
"Create high priority task for Mobile project: implement push notifications by next Friday and have Jennifer handle it with John and Mike as stakeholders"

# Smart date intelligence  
"Deploy the API updates to Production project by end of week"

# People assignment with context
"Ask Sarah to review the documentation by tomorrow - this is urgent"

# Auto project creation
"Add task for NewProductLaunch project: create landing page mockups"
```

### 🎯 智能特性

- **📅 智能日期解析**：支持“明天”、“下周一”、“周末”、“两周后”等时间表达  
- **🏗️ 项目智能**：根据上下文自动检测并创建项目  
- **👥 人员管理**：自动识别执行者和相关方  
- **🔥 优先级识别**：将“紧急”、“高”、“中”、“低”等优先级转换为相应的 API 值  
- **🤖 意图识别**：自动路由创建/更新/查询请求  
- **🧠 上下文感知**：能够解析包含多个实体的复杂句子  

### 📊 智能分析与报告

```bash
# Get intelligent insights
"What tasks are overdue?"
"Show me my task summary" 
"What's in the Mobile project?"
"List my high priority tasks"
```

## 🎯 单一命令接口

**通过人工智能意图识别，所有操作都通过一个入口点完成：**

```bash
# Task creation with full AI processing
python taskline.py "Add urgent task for Platform project: fix authentication bug by Friday"

# People assignment with smart routing  
python taskline.py "Ask David to handle the deployment by next Monday"

# Intelligent queries with context
python taskline.py "What tasks are overdue?"
python taskline.py "Show my productivity summary"

# Complex multi-entity requests
python taskline.py "Create high priority task for WebApp project: review security implementation by end of week and have Sarah lead it with Mike and John informed"
```

## 🚀 架构

### **人工智能驱动的流程**

```
Natural Language → Intent Detection → Smart Routing → Enhanced Processing → MyTaskline.com API
```

### **主要组件**
- **🤖 `taskline.py`**：包含人工智能调度器的主入口点  
- **🧠 `scripts/taskline_ai.py`**：负责意图识别和智能路由  
- **✨ `scripts/create_task_enhanced.py**：完全由人工智能驱动的任务创建功能  
- **📊 `scripts/reports.py**：提供分析和洞察功能  
- **📋 `scripts/list_tasks.py**：支持智能任务查询  
- **⚙️ `scripts/update_task.py**：实现智能状态更新  

## 🛠 设置

### 1. 获取您的 MyTaskline.com 账户  
- 访问 [**mytaskline.com**](https://mytaskline.com) 并创建您的账户  
- 转到 **设置** 以生成您的 API 密钥  
- 复制您的个人 API 密钥以用于配置  

### 2. 配置该技能  
- 打开 `references/config.json`  
- 将 `YOUR_TASKLINE_API_KEY_HERE` 替换为您在 mytaskline.com 上获得的实际 API 密钥  

### 3. 开始使用人工智能任务管理  

```bash
python taskline.py "Add task: test my AI task management system"
python taskline.py "What tasks do I have?"
```

## 💡 使用示例

### 🧠 智能任务创建  
```bash
# Basic with AI enhancement
"Add task: fix the login bug"

# Multi-entity with full intelligence  
"Create high priority task for Mobile project: implement OAuth integration by next Friday"

# People assignment with context
"Ask Jennifer to review the API documentation by end of week - include David as stakeholder"

# Complex business scenarios
"Add urgent task for Q1Launch project: deploy marketing site by tomorrow and have Sarah handle frontend with Mike reviewing backend"
```

### 📊 智能查询  
```bash
# Smart reporting
"What's overdue?"
"Show my task summary"
"What's in the Mobile project?" 

# Context-aware filtering
"List high priority tasks"
"Show tasks assigned to Jennifer"
"What did I complete this week?"
```

### ⚡ 快速更新  
```bash
# Natural status changes
"Mark the authentication task as done"
"Set the API task to in-progress"
"Update priority to urgent for login bug"
```

## 🌟 为什么选择 MyTaskline.com？

- **🎯 专为任务管理而设计**：专门针对高效的任务管理需求  
- **🤖 支持人工智能**：提供完整的 API，支持高级集成  
- **📊 强大的分析功能**：内置的洞察力和生产力跟踪工具  
- **👥 适合团队使用**：支持人员管理和角色分配  
- **🏗️ 项目组织**：支持自动创建和管理项目  
- **🔒 安全性**：使用个人 API 密钥保护访问  
- **📱 现代化界面**：简洁、快速的 Web 界面  

## 🚀 高级特性

### **多实体解析**  
人工智能能够处理包含多个实体的复杂请求：  
- **项目**：根据需要自动检测并创建  
- **人员**：自动分配执行者和相关方  
- **日期**：支持相对日期和业务相关的日期解析  
- **优先级**：能够识别自然语言中的优先级  
- **上下文**：能够智能区分任务标题和描述  

### **持续优化**  
- **兼容性**：支持基本或高级 API 功能  
- **自动升级**：能够自动利用 MyTaskline.com 的新功能  
- **错误处理**：能够优雅地处理边缘情况  

### **适合生产环境**  
- **经过大规模测试**：在实际环境中可处理 40 多个任务和 20 多个项目  
- **可靠的 API**：基于稳定的 MyTaskline.com 平台构建  
- **性能优化**：具备高效的自然语言处理能力  

## 🎯 适用场景  

- **📋 个人生产力**：借助人工智能辅助进行个人任务管理  
- **👥 小型团队**：支持协作式任务分配和跟踪  
- **🏗️ 项目管理**：根据项目上下文自动组织任务  
- **🤖 人工智能爱好者**：享受最前沿的自然语言处理技术  
- **⚡ 高级用户**：支持高级自动化和智能路由功能  

## 🔗 资源  

- **🌐 平台**：[mytaskline.com](https://mytaskline.com)  
- **⚙️ 设置**：[mytaskline.com/settings](https://mytaskline.com/settings)（API 密钥生成）  
- **📊 仪表板**：提供可视化的任务管理界面  
- **🔧 API 文档**：详见 `references/api_examples.md`  

---

**🚀 利用 [MyTaskline.com](https://mytaskline.com) 的人工智能功能，提升您的任务管理效率吧！**