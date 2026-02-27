---
name: bmad-method
description: >
  这是一个由人工智能驱动的敏捷开发框架，支持34种以上的工作流程，并配备了12种领域的专家代理（如项目经理、架构师、开发人员、用户体验设计师、Scrum主管等）。  
  适用场景：  
  (1) 用户希望借助人工智能的帮助启动一个新的软件项目；  
  (2) 用户需要关于敏捷开发工作流程的指导；  
  (3) 用户希望搭建一个人工智能开发环境；  
  (4) 用户咨询与BMad Method相关的问题或命令（例如：/bmad-help）。
---
# BMad 方法

这是一个由 AI 驱动的敏捷开发框架，旨在帮助开发者实现更多的架构梦想（AI-driven agile development framework that helps developers realize more architectural goals）。

## 快速入门

```bash
# Interactive installation (recommended)
npx bmad-method install

# Or install specific version
npx bmad-method@6.0.1 install

# Non-interactive / CI/CD
npx bmad-method install --directory /path/to/project --modules bmm --tools claude-code --yes
```

## 可用模块

| 模块        | 功能                |
|------------|-------------------|
| **BMM**      | 核心框架，包含 34 个以上的工作流程    |
| **BMB**      | 创建自定义的 BMad 代理（agents）和工作流程 |
| **TEA**      | 基于风险的测试策略与自动化工具    |
| **BMGD**      | 游戏开发支持（Unity、Unreal、Godot）   |
| **CIS**      | 创新、头脑风暴、设计思维工具     |

## 命令

- `/bmad-help`  — 获取下一步操作指南
- `/bmad-help <上下文>`  — 提出具体问题（例如：“我刚刚完成了架构设计，接下来该做什么？”）

## 先决条件

- Node.js v20 或更高版本
- 适用于 AI 开发的集成开发环境（如 Claude Code、Cursor 等）

## 文档资料

- 官方文档：https://docs.bmad-method.org
- 社交媒体群组：https://discord.gg/gk8jAdXWmj