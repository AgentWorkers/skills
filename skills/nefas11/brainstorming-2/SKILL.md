---
name: brainstorming
description: 在编码之前，先进行苏格拉底式的设计优化（Socratic design refinement）。当用户提出功能需求但缺乏明确规格说明时，可以采用这种方法。
---
# 头脑风暴技巧

## 适用场景

在编写代码之前，当遇到以下情况时，请使用此技巧：
- 用户需求不明确（例如：“改进现有功能”或“添加功能X”）；
- 需要实现的功能较为复杂，存在多种实现方法；
- 设计决策会影响到多个组件或系统模块。

## 工作流程

### 第一步：明确需求
提出以下问题以澄清需求：
- 我们要解决什么问题？
- 使用该功能的用户是谁？
- 成功的标准是什么？
- 存在哪些限制因素？（时间、兼容性、依赖关系等）

### 第二步：探索多种方案
提出2-3种实现方案：
- 方案A（简单）：[描述]
- 方案B（稳健）：[描述]
- 方案C（具有前瞻性，适用于未来扩展）：[描述]

针对每种方案，列出其优缺点及复杂度（1-5分）。

### 第三步：编写设计文档
在用户选定方案后，生成详细的设计文档：

```markdown
# Feature: [Name]

## Problem
[1-2 sentences]

## Solution
[Chosen approach, 3-5 sentences]

## Components Affected
- [Component 1]: [Change description]
- [Component 2]: [Change description]

## Testing Strategy
- Unit tests: [What to test]
- Integration tests: [What to test]

## Edge Cases
- [Case 1]
- [Case 2]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

将设计文档保存在：`docs/design/YYYY-MM-DD-feature-name.md` 文件夹中。

### 第四步：转入规划阶段
将设计文档交给负责制定实施计划的团队。

## 常见错误做法：
❌ 直接开始编码；
❌ 只展示一种方案；
❌ 忽略对极端情况的讨论；
❌ 忘记保存设计文档。

## 示例

**用户需求：** “添加缓存功能”

**错误做法：**
```
I'll add Redis caching to the API.
```

**正确做法：**
```
Let me understand the requirements first:

1. What should be cached? (API responses, DB queries, computed results?)
2. What's the invalidation strategy? (TTL, event-based, manual?)
3. What's the acceptable staleness? (seconds, minutes, hours?)

Based on your answers, I'll present 3 approaches with trade-offs.
```