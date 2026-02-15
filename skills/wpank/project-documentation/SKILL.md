---
name: project-documentation
model: standard
description: 项目文档的完整工作流程，包括需求文档（ADRs）、产品需求文档（PRDs）、角色定义（personas）以及文档的组织结构。适用于为新项目设置文档或改进现有文档时使用。该流程会在项目文档、需求文档、产品需求文档、角色定义或文档结构发生变化时被触发。
---

# 项目文档（元技能）

## 项目文档的设置与维护完整工作流程

### 安装

#### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install project-documentation
```


---

## 使用场景

- 开始新项目时需要文档结构
- 改进现有项目的文档
- 设置项目需求文档（Product Requirements Documents, PRDs）或角色文档（Persona Documents）
- 希望在不同项目中保持文档的一致性

---

## “文档先行”的原则

每个项目都应该从编写文档开始，而不是从编写代码开始：

```
1. Define the idea      → What is this? What problem does it solve?
2. Define the personas  → Who uses this? What are their journeys?
3. Define the features  → What does it do for each persona?
4. Define the stack     → What technologies? Why?
5. Then build           → With full context established
```

---

## 目录结构

```
docs/
├── architecture/        # CURRENT STATE - Living docs of actual code
│   ├── overview.md
│   └── data-flow.md
├── guides/              # CURRENT STATE - How to use/operate
│   ├── getting-started.md
│   └── configuration.md
├── runbooks/            # CURRENT STATE - Short, actionable guides
│   ├── local-dev.md
│   ├── deploy.md
│   └── database.md
├── planning/            # FUTURE - Not for docs site
│   ├── roadmap.md
│   └── specs/
├── decisions/           # ADRs - Decision records
│   ├── 001-tech-stack.md
│   └── 002-auth-approach.md
└── product/             # PRD, personas
    ├── overview.md
    ├── personas/
    └── features.md
```

---

## 关键区分：当前状态与未来规划

| 类别 | 目的 | 是否应放在文档网站上？ |
|----------|---------|-------------------|
| **当前状态** | 项目当前的运作方式 | 是 |
| **规划** | 未来的规格和设计 | 否 |
| **架构** | 代码的实时文档 | 是 |
| **路线图/待办事项** | 我们正在做的事情 | 否 |
| **操作手册** | 操作指南 | 是 |
| **拟议的操作手册** | 未来的计划 | 否 |

---

## 文档类型

### 架构决策记录（Architecture Decision Records, ADRs）

模板：
```markdown
# ADR-001: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the issue we're solving?]

## Decision
[What did we decide?]

## Consequences
[What are the results - positive and negative?]

## Alternatives Considered
[What other options did we evaluate?]
```

### 产品需求文档（Product Requirements Document, PRD）

模板：
```markdown
# PRD: [Feature Name]

## Problem
[What problem are we solving?]

## Users
[Which personas does this serve?]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Non-Goals
[What are we explicitly NOT doing?]

## Success Metrics
[How do we know this worked?]
```

### 角色文档（Persona Documents）

模板：
```markdown
# Persona: [Name]

## Who They Are
- Background
- Technical level
- Goals

## Pain Points
- [Pain 1]
- [Pain 2]

## Journey
1. Discovery
2. Onboarding
3. Daily use
4. Advanced usage

## Content Needs
- Doc types they need
- Format preferences
```

### 操作手册（Runbooks）

模板：
```markdown
# Runbook: [Task Name]

## Prerequisites
- [Requirement 1]
- [Requirement 2]

## Steps
1. [Step 1]
2. [Step 2]

## Verify
[How to confirm success]

## Troubleshooting
| Problem | Solution |
|---------|----------|
| [Issue] | [Fix] |
```

---

## 路线图格式

```markdown
## Roadmap

### Current Sprint
- [ ] Add user authentication endpoint
- [ ] Create login form component
- [ ] Wire form to auth endpoint

### Backlog
- [ ] Password reset flow
- [ ] OAuth integration
- [ ] Two-factor auth
```

---

## 文档质量检查标准

在发布文档之前，需要满足以下要求：
- [ ] 将当前状态与未来规划区分开来
- [ ] 使用适合文档类型的模板
- [ ] 为目标读者群编写文档
- [ ] 文档内容具有可操作性（操作手册）或解释性（指南）
- [ ] 文档内容不陈旧/过时

---

## 应避免的错误做法

- **将未来规划与当前状态混在一起** — 会导致信息混淆
- **在文档网站上编写规划文档** — 用户期望看到的是实际运行情况
- **一刀切的文档格式** — 不同的读者需要不同深度的文档
- **在创建角色文档之前先开发功能** — 这会缺乏决策所需的上下文
- **编写一次后就不再更新的文档** — 需要持续维护文档的时效性

---

## 新项目的检查清单

- [ ] 创建文档和目录结构
- [ ] 编写初始的产品需求文档/项目概述
- [ ] 描述2-3个关键角色
- [ ] 为技术栈创建架构决策记录（ADR-001）
- [ ] 设定路线图格式
- [ ] 创建必要的操作手册（本地开发、部署等）
- [ ] 将规划文档与当前状态文档分开

---

## 相关技能

- **命令：** [/bootstrap-docs](../../../commands/bootstrap/bootstrap-docs.md), [/new-feature](../../../commands/development/new-feature.md)
- **工具：** [development](../../../agents/development/)