---
name: google-workspace-automation
description: 使用具有范围感知（scope-aware）功能的自动化脚本来设计 Gmail、Drive、 Sheets 和 Calendar 的自动化流程。这些脚本可用于实现每日重复性任务的自动化处理，同时支持明确的 OAuth 权限设置，并生成可供审计的日志输出。
---
# Google Workspace 自动化

## 概述

为常见的 Gmail、Drive、Sheets 和 Calendar 工作流程创建结构化的自动化方案。

## 工作流程

1. 定义自动化目标、所需服务及具体操作。
2. 确定所需的 OAuth 权限范围及集成边界。
3. 制定包含执行计划和重试机制的执行方案。
4. 生成可供审核的自动化脚本以供实际使用。

## 使用捆绑资源

- 运行 `scripts/plan_workspace_automation.py` 以进行自动化方案的规划。
- 阅读 `references/workspace-guide.md` 以了解权限范围和配额相关注意事项。

## 安全规范

- 始终使用最低权限的 OAuth 权限范围。
- 确保自动化脚本具有幂等性（即多次执行不会产生不同的结果），并便于审计。