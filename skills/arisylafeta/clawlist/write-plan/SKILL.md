---
name: write-plan
description: "必须在头脑风暴之后、执行之前使用。该工具会生成详细的实施计划，其中包含检查点、验证标准以及执行选项。"
---

# 编写实施计划

## 概述

将经过验证的设计转化为详细的、可执行的实施计划，并设置相应的检查点。

每个计划应包括：
- 任务量适中的任务（每个任务耗时2-5分钟）
- 带有验证标准的检查点
- 每个部分的预计完成时间
- 计划末尾提供执行选项

## 计划结构

```markdown
# [Project Name] - Implementation Plan

**Goal:** One sentence describing success
**Approach:** Brief summary of the chosen approach
**Estimated Total Time:** X minutes

## Checkpoint 1: [Milestone Name]
- [ ] Task 1: [Description] (~X min)
  - **Action:** [Specific action]
  - **Verify:** [How to confirm done]
- [ ] Task 2: [Description] (~X min)
  ...

## Checkpoint 2: [Milestone Name]
...

## Verification Criteria
- [ ] All checkpoints complete
- [ ] Quality standards met
- [ ] User approval obtained
```

## 任务粒度

- **小任务：** 需要2-5分钟完成
- **具体明确：** 明确“完成”的标准
- **可验证：** 可以确认任务是否已完成
- **独立性：** 不会阻碍同一检查点内的其他任务

## 执行方式的选择

保存计划后，提供以下两种执行方式：

**“计划已保存至 `memory/plans/<filename>.md`。**  
**执行选项：**  
**1. 单个代理执行（当前会话）**：按顺序执行任务，并在每个检查点进行汇报  
**2. 分配多个代理执行（并行）**：为独立任务创建子代理以并行处理  

**选择哪种方式？**  

**如果选择单个代理执行：**  
- 保持当前会话状态  
- 按顺序执行任务  
- 在每个检查点报告进度  

**如果选择分配多个代理执行：**  
- 使用 `dispatch-multiple-agents` 技能  
- 为任务创建子代理以实现并行处理  
- 整合各子代理的执行结果  

## 与其他技能的集成  

- 在进行**头脑风暴**之后 → 使用 `write-plan` 技能  
- 在开始**执行任务**之前 → 必须先制定计划  
- 与 `dispatch-multiple-agents` 技能结合使用 → 以实现任务并行执行