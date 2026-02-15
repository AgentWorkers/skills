---
name: smart-model-switching
description: >-
  Auto-route tasks to the cheapest Claude model that works correctly.
  Three-tier progression: Haiku → Sonnet → Opus. Classify before responding.
  HAIKU (default): factual Q&A, greetings, reminders, status checks, lookups,
  simple file ops, heartbeats, casual chat, 1-2 sentence tasks.
  ESCALATE TO SONNET: code >10 lines, analysis, comparisons, planning, reports,
  multi-step reasoning, tables, long writing >3 paragraphs, summarization,
  research synthesis, most user conversations.
  ESCALATE TO OPUS: architecture decisions, complex debugging, multi-file
  refactoring, strategic planning, nuanced judgment, deep research, critical
  production decisions. Rule: If a human needs >30 seconds of focused thinking,
  escalate. If Sonnet struggles with complexity, go to Opus. Save 50-90% on
  API costs by starting cheap and escalating only when needed.
author: "OpenClaw Community"
version: 1.0.0
homepage: https://clawhub.com
metadata:
  openclaw:
    emoji: "💰"
---

# 智能模型选择

**Claude 的三层路由系统：Haiku → Sonnet → Opus**

从最便宜的模型开始使用，仅在必要时升级。这样可以节省 50-90% 的 API 使用成本。

## 金科玉律

> 如果人类需要超过 30 秒的专注思考时间，就从 Haiku 升级到 Sonnet。
> 如果任务涉及架构设计、复杂的权衡或深度推理，就升级到 Opus。

## 成本对比

| 模型 | 输入成本 | 输出成本 | 相对成本 |
|-------|-------|--------|---------------|
| Haiku | 0.25 美元/次 | 1.25 美元/次 | 1 倍（基准） |
| Sonnet | 3.00 美元/次 | 15.00 美元/次 | 12 倍 |
| Opus | 15.00 美元/次 | 75.00 美元/次 | 60 倍 |

**总结：** 选择错误的模型会浪费金钱或时间。简单任务使用 Haiku，标准任务使用 Sonnet，复杂任务使用 Opus。

---

## 💚 HAIKU — 简单任务的默认选择

**适用于以下场景：**
- 事实性问答（例如：“X 是什么？”、“Y 是谁？”、“Z 是什么时候发生的？”）
- 快速查询（例如：定义、单位转换、简短翻译）
- 状态检查（例如：日历查询、文件读取、会话监控）
- 周期性检查（例如：发送 HEARTBEAT_OK 响应）
- 记忆与提醒（例如：“记住这个”、“提醒我……”）
- 简单的文件操作（例如：读取、列出、基本写入）
- 仅需 1-2 句话回答的任务

### **绝对不要在 Haiku 上执行以下操作：**
- ❌ 编写超过 10 行的代码
- ❌ 创建比较表格
- ❌ 编写超过 3 段的文本
- ❌ 进行多步骤分析
- ❌ 编写报告或提案

---

## 💛 SONNET — 标准工作工具

**适用于以下场景：**

### **代码与技术相关：**
- 代码生成（编写函数、构建功能、脚本）
- 代码审查（代码提交审核、质量检查）
- 调试（常规错误排查）
- 文档编写（README 文件、注释、用户指南）

### **分析与规划：**
- 分析与评估（比较不同选项、权衡利弊）
- 规划（项目计划、路线图、任务分解）
- 综合研究（整合多个来源的信息）

### **写作与内容：**
- 长篇写作（报告、提案、文章等，超过 3 段）
- 创意写作（博客文章、描述性文本）
- 摘要编写（长文档、会议记录）
- 结构化输出（表格、大纲、格式化文档）

---

## ❤️ OPUS — 仅用于复杂推理

**适用于以下场景：**

### **架构与设计：**
- 系统架构决策
- 大规模代码库重构
- 需要权衡的设计模式选择
- 数据库模式设计

### **深度分析：**
- 复杂的调试（涉及多个文件、竞态条件）
- 安全性审查
- 性能优化策略
- 微妙错误的根本原因分析

### **战略与创意：**
- 战略规划（商业决策、路线图制定）
- 细致的判断（涉及伦理问题、模糊性、相互冲突的价值观）
- 深度研究（全面的多源分析）

---

## 🔄 实现方式

### 对于子代理（Subagents）：

```javascript
// 常规监控
sessions_spawn(task="检查备份状态", model="haiku");

// 标准代码工作
sessions_spawn(task="构建 REST API 端点", model="sonnet");

// 架构决策
sessions_spawn(task="设计多租户数据库架构", model="opus");
```

### 对于 Cron 作业（Cron Jobs）：

```json
{
  "payload": {
    "kind": "agentTurn",
    "model": "haiku"
  }
```

**除非任务确实需要复杂的推理，否则始终使用 Haiku 来处理 Cron 作业。**

---

## 📊 快速决策树

```plaintext
- 是问候、查询、状态检查，还是只需要 1-2 句话的回答？
  是 → 使用 HAIKU
  否 → 继续向下选择

- 是代码编写、分析、规划、写作，还是多步骤操作？
  是 → 使用 SONNET
  否 → 继续向下选择

- 是涉及架构设计、深度推理，还是需要做出关键决策？
  是 → 使用 OPUS
  否 → 默认使用 SONNET；如果遇到困难再升级
```

---

## 📋 快速参考卡片

```plaintext
┌─────────────────────────────────────────────────────────────┐
│                  智能模型选择                              │
│                  Haiku → Sonnet → Opus                          │
├─────────────────────────────────────────────────────────────┤
│  💚 HAIKU（最便宜的模型）                          │
│  • 适用于问候、状态查询、快速查询                      │
│  • 适用于事实性问答、定义、提醒                      │
│  • 适用于简单的文件操作及 1-2 句话的回答                │
├─────────────────────────────────────────────────────────────┤
│  💛 SONNET（标准模型）                          │
│  • 适用于代码编写（超过 10 行）、调试                      │
│  • 适用于分析、比较、规划                        │
│  • 适用于报告撰写、提案编写                      │
├─────────────────────────────────────────────────────────────┤
│  ❤️ OPUS（高级模型）                          │
│  • 适用于架构设计、复杂调试                      │
│  • 适用于战略规划、深度研究                      │
├─────────────────────────────────────────────────────────────┤
│  💡 规则：如果需要超过 30 秒的思考时间 → 升级模型         │
│  💰 成本：Haiku 1 倍 → Sonnet 12 倍 → Opus 60 倍              │
└─────────────────────────────────────────────────────────────┘
```

---

*本指南专为仅使用 Claude 的系统设计，提供了 Haiku、Sonnet 和 Opus 三种模型。*
*灵感来源于节省成本的理念，并通过三层模型进行扩展。*