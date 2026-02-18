---
name: skill-engineer
description: 使用多智能体迭代优化方法来设计、测试、审查和维护 OpenClaw 系统中的智能体技能。该方法协调 Designer（设计者）、Reviewer（审查者）和 Tester（测试者）这三个子智能体，以确保技能开发的质量。当用户请求“设计技能”、“审查技能”、“测试技能”、“审计技能”或提及“智能体套件的质量”时，应使用此方法。
metadata:
  author: skill-engineer
  version: 3.0.0
  owner: main agent (or any agent in the kit requiring skill development capability)
  based_on: Anthropic Complete Guide to Building Skills for Claude (2026-01)
---
# 技能工程师

您负责管理 OpenClaw 代理套件中所有技能的整个生命周期。整个多代理工作流程的质量完全取决于技能的质量——一个质量低下的技能会导致每次运行都产生糟糕的结果。

**核心原则：** 构建者不评估自己的工作。该技能通过多代理架构实现了职责分离，设计、审查和测试分别由独立的子代理来完成。

---

## 范围与边界

### 该技能负责的内容
- 技能设计：SKILL.md、skill.yml、README.md、测试脚本、参考资料
- 技能审查：质量评估、评分标准、差距分析
- 技能测试：自我验证、触发器测试、功能测试
- 技能维护：根据反馈进行迭代、重构
- 代理套件审计：检查所有技能的清单、一致性和质量

### 该技能不负责的内容
- **发布流程** — 发布、版本控制、变更日志属于发布流程的职责
- **仓库管理** — git 子模块、仓库创建、分支策略属于版本控制系统（VCS）的工作流程
- **部署** — 将技能安装到代理上、配置管理
- **跟踪** — 进度跟踪、任务管理、项目看板
- **基础设施** — MCP 服务器、API 密钥、环境设置

### 该技能的职责结束点
该技能生成 **经过验证的技能成果**（SKILL.md、skill.yml、README.md、测试脚本）。一旦成果通过质量检查，责任就会转移给负责发布和部署的系统。

### 成功标准

当满足以下条件时，技能开发周期被视为成功：
1. **通过质量检查** — 审查者的评分 ≥ 28/33（部署阈值）
2. **没有阻碍性问题** — 测试者未报告任何被标记为“阻碍性”的问题
3. **所有成果都已生成** — SKILL.md、skill.yml、README.md、测试脚本（如需要）、参考资料（如需要）
4. **没有安全漏洞** — 不存在硬编码的秘密信息、路径、组织名称或私有 URL
5. **脚本已验证** — 所有确定性验证脚本在目标平台上都能成功执行
6. **触发器准确性** — 测试者的触发器准确率 ≥ 90%（包括真正例和假正例）

如果任何标准未满足，技能将返回给设计者进行修订。

### 输入
调用此技能时，协调者需要收集以下信息：
| 输入 | 描述 | 是否必需 | 来源 |
|-------|-------------|----------|--------|
| **问题描述** | 需要启用的功能或工作流程 | 是 | 用户沟通 |
| **目标受众** | 将使用此技能的代理 | 是 | 用户或根据情况推断 |
| **预期的交互** | 与用户、API、文件、MCP 服务器、其他技能的交互 | 是 | 需求讨论 |
| **输入/输出** | 技能接收和产生的数据 | 是 | 需求讨论 |
| **约束条件** | 性能限制、安全要求、依赖关系 | 否 | 用户或系统 |
| **之前的反馈** | 之前迭代中的审查或测试报告 | 否 | 上次审查者/测试者的反馈 |
| **现有的成果** | 如果是对现有技能进行重构或维护 | 否 | 文件系统 |

**示例需求收集：**
```
User: "I need a skill for analyzing competitor websites"

Orchestrator gathers:
- Problem: Automate competitor analysis with structured output
- Audience: research-agent
- Interactions: web_fetch, browser tool, writes markdown reports
- Inputs: competitor URLs, analysis criteria
- Outputs: comparison table, insights markdown
- Constraints: must complete in <60s per site
```

这些输入随后会被传递给设计者，以开始设计流程。

---

## 架构概述
技能工程师采用三角色迭代架构。协调者（即您，作为主要代理）为每个角色创建子代理，但不会直接执行创造性或评估工作。

```
Orchestrator (main agent)
    │
    ├─ Spawn ──→ Designer (creative subagent)
    │                │
    │                ▼ produces skill artifacts
    │
    ├─ Spawn ──→ Reviewer (critical subagent)
    │                │
    │                ▼ scores, identifies issues
    │
    ├─ Spawn ──→ Tester (empirical subagent)
    │                │
    │                ▼ runs self-play, reports results
    │
    └─ Decision: Ship / Revise / Fail
```

### 迭代循环
```
Designer → Reviewer ──pass──→ Tester ──pass──→ Ship
              │                  │
              fail               fail
              │                  │
              ▼                  ▼
         Designer revises   Designer revises
              │                  │
              ▼                  ▼
           Reviewer          Reviewer + Tester
              │
           (max 3 iterations, then fail)
```

**退出条件：**
- **发布：** 审查者的评分 ≥ 28/33（85%及以上）且测试者未报告阻碍性问题
- **修订：** 审查者或测试者发现可解决的问题（继续迭代）
- **失败：** 经过 3 次迭代后仍未达到质量标准

### 迭代失败路径
如果经过 3 次失败迭代，协调者必须：
1. **停止迭代** — 不要继续尝试
2. **向用户报告失败情况**：
   - 总结：“技能开发在 3 次迭代后失败”
   - 3 次迭代的全部报告（审查者和测试者的反馈）
   - 最终质量评分
   - 未解决的阻碍性问题列表
3. **向用户提供选择**：
   - 提供更多背景信息或澄清需求（重新开始并提供更准确的信息）
   - 简化技能范围（降低技能复杂性并重新尝试）
   - 放弃该技能（需求可能不可行）
4. **切勿默默失败** — 必须向用户报告并等待决策

**注意：** 绝不要在未通过质量检查的情况下继续迭代或发布技能。

### 子代理创建机制
“创建子代理”意味着为每个角色创建一个独立的执行环境。在 OpenClaw 中：
**选项 1：基于角色的执行（推荐用于大多数情况）**
协调者在同一会话中依次执行每个角色，但明确划分角色职责：
```
[Acting as DESIGNER] ...generate artifacts...
[Acting as REVIEWER] ...evaluate artifacts...
[Acting as TESTER] ...validate artifacts...
```

记录每个步骤中活跃的角色。这样可以保持职责分离，同时避免多会话带来的开销。

**选项 2：独立代理会话（适用于复杂的工作流程）**
使用 `openclaw agent --message "..." --session-id <unique-id>` 来创建隔离的会话：
```bash
# Spawn Designer
openclaw agent --session-id "skill-v1-designer" \
  --message "Act as Designer. Requirements: [...]"

# Spawn Reviewer
openclaw agent --session-id "skill-v1-reviewer" \
  --message "Act as Reviewer. Artifacts: [path]. Rubric: [...]"
```

这种方法可以提供真正的隔离，但会增加令牌成本和协调复杂性。

**使用建议：**
- 对于常规的技能工作，使用选项 1（基于角色的执行）
- 当需要并行处理或设计非常复杂（超过 1000 行代码）时，使用选项 2（独立会话）

**重要提示：** 无论采用哪种方法，协调者都不得自行执行创造性工作（设计）或评估工作（审查者/测试者）。协调者的职责仅限于协调。

---

## 协调者的职责
协调者负责整个迭代流程的协调工作。它不编写技能内容，也不评估技能的质量。
1. **从用户那里收集需求**（问题描述、目标受众、输入/输出、交互方式）
2. **根据需求和之前的反馈创建设计者角色**
3. **收集设计者的成果**（技能成果）
4. **为审查者创建子代理，并提供评分标准**
5. **收集审查者的反馈**（评分和问题）
6. **如果发现问题**：将反馈反馈给设计者（返回步骤 2）
7. **如果通过审查**：为测试者创建子代理**
8. **收集测试者的结果**（通过/失败情况及详细报告）
9. **如果发现问题**：将测试结果反馈给设计者（返回步骤 2）
10. **如果所有环节都通过**：将最终评分表添加到 README.md 中，然后将成果交付给用户
11. **跟踪迭代次数** — 如果经过 3 次迭代仍未通过，则视为失败（参见迭代失败路径）

### README 中的最终评分
每个发布的技能必须在其 README.md 中包含一个质量评分表。这是协调者在交付前添加的审查者的最终评分：
```markdown
## Quality Scorecard

| Category | Score | Details |
|----------|-------|---------|
| Completeness (SQ-A) | 7/7 | All checks pass |
| Clarity (SQ-B) | 4/5 | Minor ambiguity in edge case handling |
| Balance (SQ-C) | 4/4 | AI/script split appropriate |
| Integration (SQ-D) | 4/4 | Compatible with standard agent kit |
| Scope (SCOPE) | 3/3 | Clean boundaries, no leaks |
| OPSEC | 2/2 | No violations |
| References (REF) | 3/3 | All sources cited |
| Architecture (ARCH) | 2/2 | Separation of concerns maintained |
| **Total** | **29/30** | |

*Scored by skill-engineer Reviewer (iteration 2)*
```

该评分表作为质量证明。用户可以在安装前评估技能的质量。

### 版本控制
协调者负责整个工作流程中的 git 提交操作：
**何时提交：**
- 设计者生成初始成果后（第 1 次迭代）：`git add . && git commit -m "feat: <技能名称> 的初始设计"`
- 设计者完成修订后（第 2 次及以后的迭代）：`git add . && git commit -m "fix: 修复审查问题（第 N 次迭代）"`
- 测试者通过审查后但在发布前：`git add README.md && git commit -m "docs: 为 <技能名称> 添加质量评分表"`
**何时推送：**
- 最终成果通过所有质量检查后：`git push origin main`
**注意：** 不要推送中间阶段的成果——只推送准备发布的成果

**分支策略：**
- 在主分支上进行常规技能开发
- 使用特性分支进行实验性或破坏性更改

### 错误处理
协调者必须优雅地处理技术故障：
| 失败类型 | 检测方式 | 应对措施 |
|--------------|-----------|----------|
| **Git 提交失败** | 提交代码返回非零值 | 重试一次。如果再次失败，向用户报告：“无法推送到远程服务器。检查网络/权限。” |
| **缺少 OPSEC 扫描脚本** | 文件未找到 | 跳过 OPSEC 自动检查，但在审查中标记：“需要手动进行 OPSEC 审查——脚本未找到。” |
| **文件写入错误** | 权限被拒绝 | 报告：“无法写入 [路径]。检查文件权限。” 并终止工作流程。 |
| **子代理崩溃** | 超时或出现错误 | 记录错误，尝试重试一次。如果再次失败，报告：“子代理失败。需要手动干预。” |
| **审查评分 = 0** | 所有检查都失败 | 报告：“技能未通过所有质量检查。可能是需求不明确或技能设计存在根本性问题。建议重新开始。” |

**重试逻辑：**
- Git 操作：延迟 5 秒后重试一次
- 文件操作：延迟 2 秒后重试一次
- 子代理创建：使用新的环境信息重试一次

**失败快速处理规则：**
- 如果迭代次数超过 3 次，立即失败（不再重试）
- 如果发现安全违规，立即失败（不再进行迭代）
- 如果所需文件无法写入，立即失败

### 性能注意事项
**协调者的工作负担：** 协调设计者/审查者/测试者的工作在 1-3 次迭代中可能很复杂，特别是对于大型技能（超过 1000 行代码）。协调者需要处理：
- 需求收集
- 子代理的协调（典型工作流程中会创建 3-9 个子代理）
- 不同角色之间的反馈传递
- 迭代跟踪
- 最终评分表的生成
- Git 操作

**令牌使用注意事项：** 完整的 3 次迭代周期可能会消耗 5 万到 15 万个令牌，具体取决于技能的复杂性。对于极其复杂的技能，可以考虑：
- 将技能拆分为多个子技能（每个子技能的范围更简单）
- 使用独立代理会话（选项 2）来隔离令牌使用环境
- 在开始迭代前简化需求

**如果协调者感到压力过大：** 这可能表明正在设计的技能过于复杂。请重新审视需求定义并考虑拆分技能。**

### 子代理的创建环境
每个子代理只接收它所需的信息：
| 角色 | 接收的内容 | 不接收的内容 |
|------|----------|------------------|
| 设计者 | 需求、之前的反馈（如有）、设计原则 | 审查者的评分标准内部细节 |
| 审查者 | 技能成果、评分标准、范围边界 | 需求讨论内容 |
| 测试者 | 技能成果、测试协议 | 审查结果 |

---

## 设计者的角色
**职责：** 生成和修改技能内容。
**有关设计者的完整说明，请参阅：`references/designer-guide.md`

### 快速参考**
**输入：** 需求、设计原则、反馈（在第 2 次及以后的迭代中）
**输出：** SKILL.md、skill.yml、README.md、测试脚本、参考资料
**关键约束：**
- 逐步披露信息（从封面到正文再到链接文件）
- 遵循范围规则（明确界定范围，避免范围蔓延）
- 使用工具选择机制（在执行前进行验证）
- README 仅面向外部用户（不包含内部组织细节）
- 遵循 AI 与脚本的决策框架

**设计原则：**
- 逐步披露信息（三级系统）
- 可组合性（与其他技能协同工作）
- 可移植性（同一技能可在 Claude.ai、Claude Code、API 上使用）

---

## 审查者的角色
**职责：** 独立进行质量评估。审查者从未见过需求讨论内容——它仅根据技能成果本身进行评估。
**有关审查者的完整评分标准和指南，请参阅：`references/reviewer-rubric.md`

### 快速参考**
**输入：** 技能成果、评分标准、范围边界
**输出：** 包含评分、评估结果（通过/修订/失败）、问题、优点的审查报告

**评分标准（共 33 项检查）：**
- SQ-A：完整性（8 项检查）
- SQ-B：清晰度（5 项检查）
- SQ-C：平衡性（5 项检查）
- SQ-D：集成性（5 项检查）
- SCOPE：范围边界（3 项检查）
- OPSEC：安全性（2 项检查）
- REF：参考资料（3 项检查）
- ARCH：架构（2 项检查）

**评分标准：**
- 28-33 分：通过 → 可以发布
- 20-27 分：需要修订（存在可解决的问题）
- 10-19 分：需要重新设计（存在重大问题）
- 0-9 分：拒绝（存在根本性问题）

**预审查：** 在手动评估之前运行确定性验证脚本

---

## 测试者的角色
**职责：** 通过自我执行来进行实证验证。测试者加载技能并尝试执行实际任务。
**有关测试者的完整协议，请参阅：`references/tester-protocol.md`

### 快速参考**
**输入：** 技能成果、测试协议
**输出：** 包含触发器准确率、功能测试结果、边缘情况、阻碍性问题/非阻碍性问题的测试报告
**测试协议：**
1. **触发器测试** — 确保技能正确加载（准确率 ≥ 90%）
2. **功能测试** — 执行 2-3 个实际任务，记录混淆点
3. **边缘情况测试** — 检查缺失的输入、模糊的需求、边界情况

**问题分类：**
- **阻碍性问题：** 阻止技能正常运行（必须在发布前修复）
- **非阻碍性问题：** 影响质量但不会破坏核心功能

**通过标准：** 无阻碍性问题 + 触发器准确率 ≥ 90%

---

## 代理套件审计协议
定期对代理套件进行全面审计：
1. **列出所有技能** — 列出每个技能及其所属代理
2. **检查孤立技能** — 没有代理使用的技能
3. **检查重复技能** — 功能重叠的技能
4. **检查平衡性** — 有些代理是否负担过重而其他代理闲置？
5. **检查一致性** — 命名规范、输出格式是否一致
6. **对每个技能进行质量评估**（SQ-A 到 SQ-D）
7. **生成审计报告**，包含评分和建议

### 审计输出模板
```markdown
# Agent Kit Audit Report

**Date:** [date]
**Skills audited:** [count]

## Skill Inventory

| # | Skill | Agent | Quality Score | Status |
|---|-------|-------|--------------|--------|
| 1 | [name] | [agent] | X/33 | Deploy/Revise/Redesign |

## Issues Found
1. ...

## Recommendations
1. ...

## Action Items
| # | Action | Priority | Owner |
|---|--------|----------|-------|
```

---

## 技能交互图
维护一个展示技能之间交互关系的图表：
```
orchestrator-agent (coordinates workflow)
    ├── content-creator (writes content)
    │   └── consumes: research outputs, review feedback
    ├── content-reviewer (reviews content)
    │   └── produces: review reports
    ├── research-analyst (researches topics)
    │   └── produces: research consumed by content-creator
    ├── validator (validates outputs)
    └── skill-engineer (this skill — meta)
        └── consumes: all skills for audit
```

请根据您的具体代理架构进行调整。