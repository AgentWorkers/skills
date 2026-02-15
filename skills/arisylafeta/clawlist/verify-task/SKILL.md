---
name: verify-task
description: "必须在完成任何多步骤任务或项目后使用该工具。它根据原始计划验证任务的完成情况，检查质量标准，并记录最终结果。"
---

# 验证任务

## 概述

确认任务已成功完成，并根据原始计划记录结果。

## 需要验证的情况

- 计划中的所有任务均被标记为已完成；
- 用户询问“任务完成了吗？”或“任务是否有效？”；
- 在宣布项目结束时；
- 在长时间运行的任务的每个检查点之后。

## 验证流程

### 第一步：加载原始计划

读取由 `write-plan` 技能创建的计划。

### 第二步：验证每个检查点

逐一检查每个检查点，确认：
- [ ] 所有标记为完成的任务均已完成；
- [ ] 验证标准均已满足；
- [ ] 质量标准均已达到。

### 第三步：最终质量检查

**一般质量标准：**
- [ ] 输出结果与原始目标一致；
- [ ] 不存在明显的错误或问题；
- [ ] 文档已更新（如适用）；
- [ ] 用户能够使用或访问结果。

### 第四步：用户确认

```
"Verification complete. Final checks:

✓ All tasks from plan completed (X/Y)
✓ Quality criteria met
✓ [Specific checks]

[Preview/demonstrate result]

Does this meet your expectations? Any adjustments needed?"
```

### 第五步：记录完成情况

将完成报告保存到：`memory/plans/YYYY-MM-DD-<project>-complete.md`

模板：
```markdown
# [Project] - Completion Report

**Date Completed:** YYYY-MM-DD
**Original Goal:** [from plan]
**Final Result:** [brief description]

## Completion Summary

| Metric | Planned | Actual |
|--------|---------|--------|
| Checkpoints | X | X |
| Tasks | Y | Y |
| Time | Z min | W min |

## Verification Checklist

- [x] All tasks complete
- [x] Quality criteria met
- [x] User approved

## What Was Delivered

[Description of final output]

## Blockers Encountered

1. [Blocker] → [Resolution]

## Lessons Learned

- [What worked well]
- [What to do differently next time]
```

## 处理问题

### 如果验证失败：

**小问题：** 迅速修复后继续执行；
**大问题：** 返回到 `doing-tasks` 阶段或重新制定计划。

## 原则

- **客观性**：根据计划进行验证，而非基于假设；
- **彻底性**：检查所有标准；
- **诚实性**：如实报告问题，不要隐瞒问题；
- **以用户为中心**：最终批准取决于用户的满意度。