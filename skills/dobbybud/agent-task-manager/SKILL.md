---
name: agent-task-manager
description: 管理和协调多步骤、具有状态变化的代理工作流程；处理任务依赖关系、持久化状态、错误恢复以及外部速率限制机制。适用于创建新的多代理系统、优化顺序工作流程或管理具有时间限制的操作。
---

# 代理任务管理器 (Agent Task Manager)

## 概述

该技能为在 OpenClaw 环境中构建具备弹性和复杂性的多代理系统提供了基础结构和核心功能。它能够将简单的脚本转换为可用于生产环境的工作流程。

## 核心功能

### 1. **任务编排与状态管理**

- **功能：** 以清晰的方式定义任务，包括输入、输出及依赖关系（类似有向无环图 (DAG) 的结构）。
- **执行方式：** 使用 `molt_task.py` 文件来管理 `task_state.json` 中的任务状态。
- **价值：** 避免重复工作，并允许代理在会话重置后继续执行未完成的任务。

### 2. **外部速率限制管理**

- **功能：** 管理需要遵守外部速率限制的操作（如 API 请求、网络爬取等）的冷却时间和重试逻辑。
- **执行方式：** 使用 `scripts/cooldown.sh` 脚本来记录最后一次执行的时间戳，并自动等待或重试。
- **价值：** 确保在 Moltbook 等环境中能够持续运行，同时不会违反 API 的使用规则。

### 3. **模块化、基于角色的代理**

- **功能：** 提供专门角色的模板结构（例如 `ContractAuditor`、`FinancialAnalyst`）。
- **执行方式：** 这些模块可以独立运行，也可以由任务编排器按顺序执行。
- **价值：** 有助于创建专注于特定任务的专家级代理，例如用于 MoltFinance-Auditor 的代理。

## 示例工作流程：MoltFinance-Auditor

1. **任务：** `FinancialAudit`
2. **依赖关系：**
   - **角色 1：** `ContractAuditor`（输入：合同地址；输出：合同安全评分）
   - **角色 2：** `FinancialAnalyst`（输入：合同地址 + 安全评分；输出：信任评分）
3. **外部操作：** `MoltbookPost`（取决于最终信任评分；受速率限制）

## 资源

### scripts/
- `molt_task.py`：用于任务状态管理的 Python 类。
- `cooldown.sh`：用于管理速率限制执行的 Shell 脚本。

### references/
- `workflow_schema.md`：用于定义复杂任务依赖关系的 JSON 模式。
- `rate_limit_patterns.md：** 关于处理常见 API 速率限制的指南（例如 Moltbook、Helius）。