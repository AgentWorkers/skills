---
name: plan-flow
version: 1.0.8
description: 结构化的AI辅助开发工作流程——包括发现（问题）、规划、执行、代码审查以及测试。
metadata: {"openclaw":{"requires":{"bins":["git","gh"]}},"clawhub":{"requires":{"bins":["git","gh"]},"emoji":"🗺️","homepage":"https://github.com/brunoscardoso/plan-flow"}}
homepage: https://github.com/brunoscardoso/plan-flow
user-invocable: true
---
# Plan-Flow：结构化的人工智能辅助开发工具

这是一个全面的人工智能辅助软件开发工具集，它提供了结构化的工作流程和持久的项目记录功能。

## 可用命令

| 命令 | 描述 |
|---------|-------------|
| `/setup` | 分析项目并生成模式文件 |
| `/discovery` | 创建用于收集需求的文档 |
| `/create-plan` | 创建包含各个阶段和复杂性评分的实施计划 |
| `/execute-plan` | 执行计划各阶段，并进行验证 |
| `/create-contract` | 根据API文档创建集成合同 |
| `/review-code` | 审查未提交的本地代码更改 |
| `/review-pr` | 审查Pull Request（代码合并请求） |
| `/write-tests` | 编写测试代码以达到覆盖目标 |
| `/flow` | 切换自动驾驶模式（自动执行整个工作流程） |

## 始终激活的功能

| 功能 | 描述 |
|---------|-------------|
| 项目日志 | 项目日志存储在`flow/ledger.md`中——会默默记录错误、修正内容以及跨会话的特定项目知识 |

## 推荐的工作流程

**自动化流程（无需用户许可即可运行）：**

```
1. /setup           → Index project patterns (run once)
2. /discovery       → Gather requirements for a feature
3. /create-plan     → Create structured implementation plan (auto-runs after discovery)
4. /execute-plan    → Execute the plan phase by phase (auto-runs after plan)
5. /review-code     → Review changes before committing
6. Archive          → Move discovery + plan to flow/archive/
```

**仅在以下情况下请求用户输入：**
- 缺少关键信息（如设备类型、浏览器等）
- 需要重现问题
- 需要批准可能破坏现有系统的操作

**切勿询问“是否准备创建计划？”或“是否继续执行？”——直接执行即可。**

## 核心概念

### 复杂性评分

每个计划阶段都有一个复杂性评分（0-10分）：

| 评分 | 级别 | 描述 |
|-------|-------|-------------|
| 0-2 | 极简单 | 仅需进行简单的、机械性的修改 |
| 3-4 | 低 | 实施过程直接明了 |
| 5-6 | 中等 | 复杂度适中，需要做出一些决策 |
| 7-8 | 高 | 复杂度高，需要综合考虑多个因素 |
| 9-10 | 非常高 | 复杂度极高，风险也较大 |

### 流程目录结构

所有项目相关文件都存储在`flow/`目录下：

```
flow/
├── archive/           # Completed/abandoned plans
├── contracts/         # Integration contracts
├── discovery/         # Discovery documents
├── plans/             # Active implementation plans
├── references/        # Reference materials
├── reviewed-code/     # Code review documents
├── reviewed-pr/       # PR review documents
└── ledger.md          # Persistent project learning journal
```

## 重要规则

1. **自动化工作流程**：自动执行发现（discovery）→ 制定计划（create-plan）→ 执行（execute）的流程。仅在需要用户输入信息时才停止。
2. **必须先进行需求发现（Discovery First）**：在创建实施计划之前，必须先运行`/discovery`命令。没有例外。如果不存在需求发现文档，则必须先执行发现步骤。
3. **测试最后进行**：测试始终是任何实施计划的最后一步。
4. **仅在所有阶段完成后进行构建验证**：只有在所有阶段都完成后，才执行构建和验证操作。
5. **完成项目后归档**：将已完成的需求发现文档和计划文件移至`flow/archive/`目录。

## 配置

在项目根目录下创建`.plan-flow.yml`配置文件：

```yaml
ai:
  provider: claude
  anthropic_api_key: sk-ant-api03-your-key-here
```

## 所需软件/工具

- `git`：用于版本控制操作
- `gh`：GitHub命令行工具，用于审查Pull Request

## 安装方法

```bash
clawhub install plan-flow
```

或者将此工具添加到您的工作区技能文件夹中：

```bash
git clone https://github.com/brunoscardoso/plan-flow.git ~/.openclaw/skills/plan-flow
```