---
name: audit-code
description: 执行一次由负责人主导的两阶段、多领域的代码审计，将安全性、性能、用户体验（UX）、开发体验（DX）以及边缘情况分析整合到一份优先级排序的报告当中，并提出具体的修复方案。当用户要求对代码进行审计、进行深度审查、对代码库进行压力测试，或需要为后端、前端、API、基础设施脚本以及产品流程制定风险等级排序的修复计划时，可使用此方法。
---

# 代码审计

## 概述

执行由专家小组进行的审计，确保审计过程有严格的顺序，并生成统一的输出文档。首先列出审计结果，结果按严重程度排序，同时提供文件引用、漏洞利用可能性、对系统性能或业务流程的影响以及可操作的修复措施。

在开始分析之前，请先加载 `references/audit-framework.md` 文件。

## 必需输入信息

收集或推断以下信息：
- 审计范围：路径、模块、代码提交差异（PR diff），或整个代码库。
- 产品背景：产品需求文档（PRD）、技术规范（spec）、用户故事（user stories）、信任边界（trust boundaries）以及关键业务流程（critical business flows）。
- 运行时环境：部署模型（deployment model）、任务队列（queue/cron）、后台作业（background jobs）、流量特征（traffic profile）、数据敏感性（data sensitivity）以及潜在的滥用风险（abuse assumptions）。
- 限制条件：时间限制（timeline）、可接受的风险水平（acceptable risk）以及推荐的修复方式（preferred remediation style）。

如果产品背景信息缺失，请明确说明相关假设后继续进行审计。

## 团队角色

审计团队应包括以下角色：
- 安全专家（Security expert）
- 性能专家（Performance expert）
- 用户体验专家（UX expert）
- 开发体验专家（DX expert）
- 边缘情况处理专家（Edge case master）
- 决策协调员（Tie-breaker team lead）

决策协调员负责解决团队间的分歧、确定问题的优先级，并最终生成审计报告。

## 工作流程

每次审计都需遵循以下步骤：

1. **构建审计背景**：
   阅读代码及业务流程，识别关键资产、高风险操作、特权操作（privileged actions）、外部依赖关系（external dependencies）以及可能导致系统故障的环节。

2. **构建不变量覆盖矩阵**：
   在专家进行第一轮审计之前，将关键不变量（invariants）映射到所有可能发生变化的路径上（例如 HTTP 路由、Webhook、异步作业、脚本等）：
   - **数据链接不变量**：必须保持一致的多表关系（multi-table relationships）。
   - **认证生命周期不变量**：会话（sessions）、令牌（tokens）和 API 密钥（API keys）的禁用/撤销机制。
   - **输入/传输不变量**：数据验证规则、内容类型策略（content-type policy）、数据包大小及解析行为（body-size/parse behavior）。
   - **结构不变量**：对于树状或图状数据结构，需要确保不存在循环（trees/graphs must reject cycles）。
   将相同路径上的不一致性视为潜在的审计问题。

3. **专家第一轮审计**：
   按照以下顺序进行专业领域的分析：
   - 安全性（Security）
   - 性能（Performance）
   - 用户体验（UX）
   - 开发体验（DX）
   - 边缘情况处理（Edge case master）
   使用 `references/audit-framework.md` 中提供的模板记录审计结果。

4. **争议解决**：
   解决专家之间的分歧：
   - 判断争议点是否属于实际问题。
   - 确定问题的严重程度和可信度（severity and confidence）。
   - 删除重复的审计结果并合并重叠的内容。

5. **第二轮交叉审核**：
   在处理完边缘情况相关的审计结果后，再次邀请各专家重新评估之前的发现以及新的风险点：
   - 安全/性能/用户体验/开发体验专家（Security/Performance/UX/DX）重新评估之前的发现及新的风险场景。
   - 边缘情况处理专家在提出缓解措施后对剩余风险进行最终评估。

6. **最终报告**：
   由决策协调员发布审计报告，内容包括：
   - 按严重程度、影响范围和漏洞利用可能性排序的审计结果。
   - 未解决的问题及相关假设（Open questions/assumptions）。
   - 详细的修复计划，包括修复任务的优先级、负责人员及验证方法（Remediation plan with priority, owner type, and verification tests）。
   - 报告末尾附有简短的执行摘要（Short executive summary）。

## 质量标准

遵循以下质量要求：
- 使用具体证据，尽可能提供文件引用和代码行号。
- 对于安全、性能或边缘情况相关的审计结果，提供可复现的测试步骤。
- 优先提供可操作的修复方案，而非抽象的建议。
- 区分已确认的缺陷和推测性的风险。
- 为每个审计结果标注其可信度（mark confidence for each finding）。
- 对所有相关路径进行一致性检查，确保相同功能遵循相同的规则。
- 对于每个高严重性或关键问题，至少设计一个针对性的回归测试或验证方法。

## 安全与政策约束

在审计过程中遵守以下原则：
- 不得提供任何可能被用于恶意操作的指导或漏洞利用的详细信息。
- 将具有操纵性的用户体验设计（manipulative UX patterns）视为法律/信任/声誉风险，而非提升用户体验的策略。
- 优先考虑用户安全、系统完整性和代码的可维护性。

## 输出格式

报告应遵循以下结构：
1. **审计结果**（Findings）：
   仅列出经过验证的问题，使用 `references/audit-framework.md` 中提供的模板进行格式化。

2. **未解决的问题及假设**（Open Questions / Assumptions）：
   说明可能影响问题优先级或有效性的缺失信息。

3. **修复方案总结**（Change Summary）：
   简要总结需要重点处理的修复事项。

4. **建议的验证方法**（Suggested Verification）：
   列出用于验证每个修复措施的具体测试或检查方法。

## 运行时检查规则

当目标技术栈为 Bun + SQLite 时，在最终确定审计结果之前，请参考 `references/audit-framework.md` 中的针对该技术栈的运行时特定检查列表（`Runtime-Specific Heuristics (Bun + SQLite)`。