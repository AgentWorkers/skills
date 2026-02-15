---
name: smart-model-switching-glm
description: >-
  Auto-route tasks to the cheapest z.ai (GLM) model that works correctly.
  Three-tier progression: Flash → Standard → Plus/32B. Classify before responding.

  FLASH (default): factual Q&A, greetings, reminders, status checks, lookups,
  simple file ops, heartbeats, casual chat, 1–2 sentence tasks, cron jobs.

  ESCALATE TO STANDARD: code >10 lines, analysis, comparisons, planning, reports,
  multi-step reasoning, tables, long writing >3 paragraphs, summarization,
  research synthesis, most user conversations.

  ESCALATE TO PLUS/32B: architecture decisions, complex debugging, multi-file
  refactoring, strategic planning, nuanced judgment, deep research, critical
  production decisions.

  Rule: If a human needs >30 seconds of focused thinking, escalate.
  If Standard struggles with complexity, go to Plus/32B.
  Save major API costs by starting cheap and escalating only when needed.

author: "OpenClaw Community"
version: 1.0.0
homepage: https://clawhub.com
metadata:
  openclaw:
    emoji: "💰"
  provider: "z.ai (GLM)"
---

# 智能模型切换

**z.ai（GLM）的三层路由系统：Flash → Standard → Plus / 32B**

建议从最便宜的模型开始使用，仅在必要时升级。该系统旨在在保证准确性的同时，将API成本降至最低。

---

## 使用原则

> 如果人类需要超过30秒的专注思考时间，应从Flash模型升级到Standard模型。
> 如果任务涉及架构设计、复杂的权衡或深度推理，应升级到Plus / 32B模型。

---

## 模型适用场景（相对划分）

| 模型层级 | 适用模型 | 用途 |
|---------|---------|-------|
| Flash    | GLM-4.5-Flash, GLM-4.7-Flash | 最快且最便宜 |
| Standard | GLM-4.6, GLM-4.7   | 强大的推理能力与代码处理能力 |
| Plus / 32B | GLM-4-Plus, GLM-4-32B-128K | 需要深度推理和复杂架构设计的任务 |

**总结：** 选择错误的模型会浪费金钱或时间。简单任务使用Flash模型，常规工作使用Standard模型，复杂决策使用Plus/32B模型。

---

## 💚 FLASH — 简单任务的默认选择

**适用于以下场景：**
- 事实性问答（例如：“X是什么？”、“Y是谁？”、“Z发生在什么时候？”）
- 快速查询（定义、单位转换、简短翻译）
- 状态检查（监控、文件读取、会话状态）
- 周期性检查（心跳请求、确认回复）
- 记忆功能与提醒
- 轻松的对话（问候语、确认信息）
- 简单的文件操作（读取、列出、基本写入）
- 仅需1-2句话就能回答的任务
- Cron作业（默认使用Flash模型）

### **禁止在Flash模型上执行以下操作：**
- ❌ 编写超过10行的代码
- ❌ 创建比较表格
- ❌ 写作超过3段的文字
- ❌ 进行多步骤分析
- ❌ 编写报告或提案

---

## 💛 STANDARD — 核心工作模型

**在以下情况下升级到Standard模型：**

### **代码与技术相关：**
- 代码生成（函数、脚本、功能开发）
- 调试（常规错误排查）
- 代码审查（代码提交、重构）
- 文档编写（README文件、注释、使用指南）

### **分析与规划：**
- 数据分析与评估
- 任务规划（路线图、任务分解）
- 研究成果的整理与总结

### **写作与内容相关：**
- 长篇写作（超过3段）
- 长文档的摘要
- 结构化输出（表格、大纲）

**大多数实际用户交互场景都属于这一层级。**

---

## ❤️ PLUS / 32B — 仅适用于复杂推理任务**

**在以下情况下升级到Plus / 32B模型：**

### **架构与设计：**
- 系统与服务架构设计
- 数据库模式设计
- 分布式或多租户系统
- 涉及多个文件的重大代码重构

### **深度分析：**
- 复杂的调试（如竞态条件、隐蔽性错误）
- 安全性评估
- 性能优化策略
- 根本原因分析

### **战略性与判断性工作：**
- 战略性规划
- 需要细致判断或处理模糊性问题的场景
- 深度研究或跨多个来源的信息整合
- 关键的生产决策

---

## 🔄 实施指南

### 对于子代理（Subagents）：

```javascript
// 常规监控
sessions_spawn(task="Check backup status", model="GLM-4.5-Flash");

// 标准代码任务
sessions_spawn(task="Build the REST API endpoint", model="GLM-4.7");

// 架构设计任务
sessions_spawn(task="Design the database schema for multi-tenancy", model="GLM-4-Plus");
```

**对于Cron作业：** 除非任务确实需要复杂的推理能力，否则始终使用Flash模型。

---

**快速决策树：**

```plaintext
Is it a greeting, lookup, status check, or a 1–2 sentence answer?
  YES → FLASH
  NO ↓

Is it code, analysis, planning, writing, or multi-step?
  YES → STANDARD
  NO ↓

Is it architecture, deep reasoning, or a critical decision?
  YES → PLUS / 32B
  NO → Default to STANDARD; escalate if necessary
```

**快速参考卡：**

```plaintext
┌─────────────────────────────────────────────────────────────┐
│                  智能模型切换                        │
│              Flash → Standard → Plus / 32B                  │
├─────────────────────────────────────────────────────────────┤
│  💚 FLASH（最便宜）                                        │
│  • 适用于问候、状态查询、快速查询                  │
│  • 适用于事实性问答、提醒功能                  │
│  • 简单文件操作、1-2句话的回答                  │
├─────────────────────────────────────────────────────────────┤
│  💛 STANDARD（核心工作模型）                                    │
│  • 适用于编写超过10行的代码、调试                  │
│  • 适用于分析、比较、规划                  │
│  • 适用于编写报告、长篇写作                  │
├─────────────────────────────────────────────────────────────┤
│  ❤️ PLUS / 32B（高级模型）                                    │
│  • 适用于架构设计、复杂调试                  │
│  • 适用于复杂代码重构、战略规划                  │
│  • 适用于深度研究                      │
├─────────────────────────────────────────────────────────────┤
│  💡 规则：若需要超过30秒的人类思考时间，则升级模型          │
│  💰 仅在必要时升级模型                        │
└─────────────────────────────────────────────────────────────┘
```

**适用于z.ai（GLM）系统环境。**