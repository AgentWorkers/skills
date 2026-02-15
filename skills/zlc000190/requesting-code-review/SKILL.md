---
name: requesting-code-review
description: **使用场景：**  
在完成任务、实现核心功能时，或在代码合并前，使用该工具来验证工作成果是否符合项目要求。
---

# 请求代码审查

**核心原则：**尽早审查，频繁审查。

## 何时请求代码审查

**强制要求：**
- 在使用子代理进行开发完成每个任务后
- 在完成主要功能后
- 在将代码合并到主代码库之前

**可选但很有帮助：**
- 当遇到开发难题时（寻求新的视角）
- 在进行重构之前（作为基准检查）
- 在修复复杂错误后

## 如何请求代码审查

**1. 获取 Git 提交哈希值：**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 派遣代码审查子代理：**
使用 `Task` 工具，并指定 `superpowers:code-reviewer` 类型，填写 `code-reviewer.md` 模板。

**模板中的占位符：**
- `{WHAT_WASImplemented}` - 你刚刚实现的功能
- `{PLAN_OR.requireMENTS}` - 该功能应该实现的目标
- `{BASE_SHA}` - 开始提交的哈希值
- `{HEAD_SHA}` - 结束提交的哈希值
- `{DESCRIPTION}` - 简要说明

**3. 根据反馈采取行动：**
- 立即修复关键问题
- 在继续进行之前修复重要问题
- 将次要问题记录下来以备后续处理
- 如果审查者的意见有误，请提出合理的反驳意见

## 示例
```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch superpowers:code-reviewer subagent]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## 与工作流程的集成

**使用子代理进行开发：**
- 在每个任务完成后进行审查
- 在问题恶化之前发现并解决它们
- 在进入下一个任务之前修复问题

**按计划执行：**
- 每完成 3 个任务后进行一次审查
- 获取反馈，应用修改后继续进行

**非计划性开发：**
- 在合并代码之前进行审查
- 在遇到开发难题时进行审查

## 需注意的警告：

**绝对不要：**
- 因为任务简单而跳过审查
- 忽视关键问题
- 在问题未解决的情况下继续执行
- 与合理的 technical feedback 争论

**如果审查者的意见有误：**
- 用技术依据进行反驳
- 提供代码或测试结果来证明你的观点是正确的
- 请求进一步的解释或澄清

更多模板请参见：`requesting-code-review/code-reviewer.md`