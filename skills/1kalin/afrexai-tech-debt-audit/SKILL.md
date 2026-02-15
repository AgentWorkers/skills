# 技术债务审计

为工程团队提供系统性的技术债务评估服务。通过业务影响分析和修复计划，识别、评估并优先处理代码库中的技术债务问题。

## 功能概述

1. **债务识别** — 将技术债务分为不同类别：架构、代码质量、依赖关系、测试、基础设施、文档等。
2. **影响评分** — 使用加权公式对每个债务项进行努力程度（1-5分）、风险（1-5分）和业务影响（1-5分）的评估。
3. **成本估算** — 估算每个开发冲刺期的技术债务维护成本（以开发人员工时和美元计）。
4. **修复计划** — 生成优先级排序的修复计划，包括快速见效的修复措施、计划中的工作内容以及需要战略性重构的部分。
5. **执行摘要** — 提供一份适用于管理层的报告，展示技术债务与项目进展速度的比率以及预期节省的成本。

## 使用方法

请描述您的系统架构、所使用的技术栈以及存在的常见问题。该工具将进行系统性的审计：

```
"Audit our technical debt. We're a Node.js/React SaaS with 180K LOC, 
12 engineers. Known issues: monolithic API, no integration tests, 
3 deprecated dependencies, manual deployments."
```

## 评分公式

**优先级得分** = （风险 × 3）+ （业务影响 × 2）+ （努力程度 × 1）

得分越高，表示该债务越需要优先处理。其中，快速见效的修复措施（所需努力少但风险高）会排在首位。

## 技术债务类别

| 类别 | 例子 | 典型维护成本 |
|----------|----------|----------------------|
| 架构 | 单体应用、紧密耦合、错误的开发模式 | 项目进展速度降低15-25% |
| 代码质量 | 代码重复、存在“上帝类”（难以维护的类）、缺乏开发标准 | 项目进展速度降低10-20% |
| 依赖关系 | 过时的库、安全漏洞、已停止维护的框架 | 维护成本增加5-15%，同时存在安全风险 |
| 测试 | 未进行测试或测试不稳定、仅依赖人工质量保证 | 修复漏洞的额外工作量增加20-40% |
| 基础设施 | 手动部署、缺乏监控、服务器配置混乱 | 运维开销增加10-30% |
| 文档 | 无新员工入职培训文档、依赖团队内部知识 | 每招聘一名新员工需要2-4周的培训时间 |

## 输出格式

```markdown
# Technical Debt Audit Report
## Executive Summary
- Total debt items: [N]
- Estimated carrying cost: $[X]/month
- Debt-to-velocity ratio: [X]%
- Quick wins available: [N] items, [X] dev-days

## Critical (Fix This Sprint)
...

## High Priority (Next 30 Days)  
...

## Scheduled (Next Quarter)
...

## Strategic (Plan & Budget)
...

## Remediation Roadmap
Week 1-2: [Quick wins]
Month 1: [High priority]
Quarter: [Scheduled items]
```

## 重要性说明

根据Stripe开发者报告的数据，工程团队通常会将23-42%的开发时间用于处理技术债务。然而，大多数团队并未对这些债务进行量化评估。只有被量化的债务，才能被有效管理。

---

本工具由[AfrexAI](https://afrexai-cto.github.io/context-packs/)开发——一款基于人工智能的业务运营工具。

需要完整的工程管理工具包吗？请查看我们的[AI Context Packs](https://afrexai-cto.github.io/context-packs/)（价格：47美元），或尝试免费的[AI Revenue Calculator](https://afrexai-cto.github.io/ai-revenue-calculator/)。