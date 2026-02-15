---
name: ai-boss-assistant
description: 将任何人工智能（AI）系统转变为具备经过实战验证的角色和工作流程的专业执行助理。提供与 Google Workspace（Gmail、Calendar、Drive）集成的完整模板，以及里程碑交付系统和安全指南。
homepage: https://github.com/jacky6658/ai-boss-assistant
metadata:
  {
    "openclaw":
      {
        "emoji": "💼",
        "requires": { "bins": ["node"] },
      },
  }
---

# AI Boss Assistant

> 将任何人工智能（AI）转变为具备实战经验的专业执行助理，具备完善的角色设定和工作流程。

## 概述

本技能提供了完整的模板，用于训练AI代理成为您的个人助理。它包括：

- **角色设定框架**：定义AI的思维方式、沟通方式以及行为模式
- **任务分解**：将大型任务分解为可管理的阶段
- **与Google Workspace的集成**：实现Gmail、Calendar、Drive的自动化操作
- **安全指南**：内置的隐私和权限管理规则

## 快速使用方法

### 训练您的AI

请让AI按照以下步骤阅读并学习这些文件：

```
Please read and learn from:
1. agent-persona/PERSONA.md - Core personality
2. agent-persona/COMMUNICATION.md - How to communicate
3. agent-persona/WORKFLOW.md - Milestone delivery system
4. agent-persona/RULES.md - Behavioral rules
```

### 示例命令

训练完成后，您可以这样使用AI：

```
"Check my calendar for tomorrow and summarize"
"Help me draft a reply to the latest email from [client]"
"Create a project plan for [task] with milestones"
"What's on my todo list today?"
```

## 关键概念

### AI员工与聊天机器人的区别

本模板创建的“AI员工”具备以下特点：
- ✅ 能够主动执行任务
- ✅ 提供完整的解决方案
- ✅ 具备判断力和自己的观点
- ✅ 不仅提供答案，还能交付实际成果

### 任务分解

大型任务会被分解为多个阶段：
```
Task → M1 → Deliver → OK → M2 → Deliver → OK → Done
```

这样可以避免操作过程变得“不可预测”（即像“黑箱”一样难以理解），并允许在每个阶段进行审查。

### 外部化存储

重要信息会被保存在文件中：
- `MEMORY.md`：长期存储
- `memory/YYYY-MM-DD.md`：每日日志

## 系统要求

- OpenClaw 1.0及以上版本
- Node.js 18及以上版本
- Google账户（用于与Google Workspace集成）
- gog CLI（用于管理Google Workspace）

## 安装方法

```bash
# Install gog for Google Workspace
npm install -g gog
gog auth login --services gmail,calendar,drive
```

## 文件结构

```
agent-persona/     - Core persona templates
setup/             - Installation guides  
examples/          - Conversation examples
security/          - Security guidelines
tasks/             - Task management templates
```

## 链接

- **GitHub仓库**：https://github.com/jacky6658/ai-boss-assistant
- **文档**：详见README.md
- **问题反馈**：https://github.com/jacky6658/ai-boss-assistant/issues