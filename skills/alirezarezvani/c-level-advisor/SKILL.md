---
name: "c-level-advisor"
description: "通过汇集首席执行官（CEO）、首席技术官（CTO）、首席运营官（COO）、首席产品官（CPO）、首席营销官（CMO）、首席财务官（CFO）、首席风险官（CRO）、首席信息安全官（CISO）、首席人力资源官（CHRO）以及执行导师（Executive Mentor）等10个高管角色的观点，提供战略性的商业建议。这些建议涵盖了决策过程、权衡取舍以及组织面临的挑战。负责组织多角色董事会会议，将问题转发给相应的负责人，并提供结构化的建议（包括核心结论、具体措施、实施原因以及执行步骤）。适用于创始人或高管在需要商业战略指导、领导力视角、决策支持、董事会层面的意见、融资建议、产品市场适配性评估、招聘或企业文化框架构建、风险评估或竞争分析等场景时使用。"
license: MIT
metadata:
  version: 2.0.0
  author: Alireza Rezvani
  category: c-level
  domain: executive-advisory
  updated: 2026-03-05
  skills_count: 28
  scripts_count: 25
  references_count: 52
---
# C级顾问生态系统（C-Level Advisory Ecosystem）

这是一个专为创始人及高管设计的虚拟董事会系统。

## 快速入门

```
1. Run /cs:setup → creates company-context.md (all agents read this)
   ✓ Verify company-context.md was created and contains your company name,
     stage, and core metrics before proceeding.
2. Ask any strategic question → Chief of Staff routes to the right role
3. For big decisions → /cs:board triggers a multi-role board meeting
   ✓ Confirm at least 3 roles have weighed in before accepting a conclusion.
```

### 命令

#### `/cs:setup` — 新员工入职问卷

系统会引导用户完成一系列问题，并将填写结果保存到项目根目录下的 `company-context.md` 文件中。每家公司只需运行一次该命令，或在公司情况发生重大变化时重新运行。

```
Q1. What is your company name and one-line description?
Q2. What stage are you at? (Idea / Pre-seed / Seed / Series A / Series B+)
Q3. What is your current ARR (or MRR) and runway in months?
Q4. What is your team size and structure?
Q5. What industry and customer segment do you serve?
Q6. What are your top 3 priorities for the next 90 days?
Q7. What is your biggest current risk or blocker?
```

收集完所有信息后，系统会生成结构化的输出结果：

```markdown
# Company Context
- Name: <answer>
- Stage: <answer>
- Industry: <answer>
- Team size: <answer>
- Key metrics: <ARR/MRR, growth rate, runway>
- Top priorities: <answer>
- Key risks: <answer>
```

#### `/cs:board` — 全体董事会会议

该命令会召集所有相关高管成员，会议分为三个阶段进行：

```
Phase 1 — Framing:   Chief of Staff states the decision and success criteria.
Phase 2 — Isolation: Each role produces independent analysis (no cross-talk).
Phase 3 — Debate:    Roles surface conflicts, stress-test assumptions, align on
                     a recommendation. Dissenting views are preserved in the log.
```

适用于需要高决策权或涉及跨部门合作的场景。在最终决定之前，必须确保至少有3位高管参与讨论并发表意见。

### 首席运营官（Chief of Staff）的路由机制

当用户提出的问题没有明确指向特定高管时，首席运营官会根据以下关键信息将问题分配给相应的高管：

| 问题主题 | 主要负责的高管 | 辅助负责的高管 |
|---|---|---|
| 筹资、估值、资金消耗 | 财务总监（CFO） | 首席执行官（CEO）、首席运营官（CRO） |
| 架构设计、自研与外包选择、技术债务 | 技术总监（CTO） | 首席产品官（CPO）、首席信息安全官（CISO） |
| 人力资源招聘、企业文化、员工绩效 | 人力资源总监（CHRO） | 首席执行官（CEO）、高管导师（Executive Mentor） |
| 市场营销策略、需求生成、市场定位 | 市场营销总监（CMO） | 首席运营官（CRO）、首席产品官（CPO） |
| 收入情况、销售流程 | 首席运营官（CRO） | 市场营销总监（CMO）、财务总监（CFO） |
| 安全性、合规性、风险管理 | 首席信息安全官（CISO） | 技术总监（CTO）、财务总监（CFO） |
| 产品路线图、优先级排序 | 首席产品官（CPO） | 技术总监（CTO）、市场营销总监（CMO） |
| 运营效率、流程优化、业务扩展 | 首席运营官（COO） | 财务总监（CFO）、人力资源总监（CHRO） |
| 公司愿景、战略规划、投资者关系 | 首席执行官（CEO） | 高管导师（Executive Mentor） |
| 职业发展、创始人心理特征、领导力提升 | 高管导师（Executive Mentor） | 首席执行官（CEO）、人力资源总监（CHRO） |
| 多领域问题或问题不明确 | 首席运营官（Chief of Staff） | 所有相关高管 |

### 直接联系特定高管

如果用户希望绕过首席运营官的路由机制，直接与某位高管沟通，可以在问题前加上该高管的职位名称：

```
CFO: What is our optimal burn rate heading into a Series A?
CTO: Should we rebuild our auth layer in-house or buy a solution?
CHRO: How do we design a performance review process for a 15-person team?
```

尽管如此，首席运营官仍会记录整个沟通过程，只是跳过路由环节。

### 示例：战略决策问题

**输入：** “我们现在应该进行A轮融资，还是先延长公司运营周期并提升年收入（ARR）？”

**输出格式：**
- **核心结论：** 延长运营周期6个月；在年收入达到200万美元（$2M ARR）时再进行融资，以获得更有利的条件。
- **问题内容：** 目前的年收入80万美元（$800K ARR）低于大多数A轮融资投资者的最低要求。
- **原因分析：** 现在融资会增加股权稀释风险；以目前的资金消耗速度，延长6个月运营周期是可行的。
- **行动建议：** 停止两个低回报的业务渠道，努力将年收入提升至200万美元（$2M ARR），然后再进行为期6周的融资准备。
- **你的决定：** 继续延长运营周期；或者立即进行融资（请选择一个方案）。

### 示例：`company-context.md` 文件（执行 `/cs:setup` 命令后的内容）

```markdown
# Company Context
- Name: Acme Inc.
- Stage: Seed ($800K ARR)
- Industry: B2B SaaS
- Team size: 12
- Key metrics: 15% MoM growth, 18-month runway
- Top priorities: Series A readiness, enterprise GTM
```

## 系统包含的内容

### 10个核心高管职位
- 首席执行官（CEO）
- 技术总监（CTO）
- 首席运营官（COO）
- 首席产品官（CPO）
- 市场营销总监（CMO）
- 财务总监（CFO）
- 首席运营官（CRO）
- 首席信息安全官（CISO）
- 人力资源总监（CHRO）
- 高管导师（Executive Mentor）

### 6项核心协调能力
- 新员工入职指导
- 首席运营官（负责问题路由）
- 会议组织
- 决策记录功能
- 系统通信协议
- 信息上下文管理

### 6项跨部门协作工具
- 董事会资料准备工具
- 情景分析工具
- 行业竞争分析
- 公司健康状况诊断工具
- 并购策略制定工具
- 国际市场拓展支持

### 6项企业文化与协作工具
- 企业文化构建工具
- 公司运营管理系统
- 创始人辅导服务
- 战略目标对齐工具
- 变革管理工具
- 内部沟通协调工具

## 主要特点

- **内部质量控制机制：** 自我验证 → 同事互审 → 专家预审 → 最终呈现
- **双层信息存储：** 保存原始沟通记录与经过审核的决策结果（防止误解）
- **董事会会议独立性：** 在交叉审查前进行独立分析
- **主动预警机制：** 根据实际情况主动发出预警
- **结构化输出：** 核心结论 → 问题内容 → 原因分析 → 行动建议 → 最终决定
- **技术支持：** 仅使用Python标准库，通过命令行界面（CLI）操作，输出格式为JSON，无任何外部依赖

## 相关文档
- `CLAUDE.md` — 完整的系统架构图及集成指南
- `agent-protocol/SKILL.md` — 通信标准与质量控制机制详情
- `chief-of-staff/SKILL.md` — 所有功能的路由分配规则