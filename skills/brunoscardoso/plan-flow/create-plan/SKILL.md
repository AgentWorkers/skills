---
name: create-plan
description: 创建一个包含各个阶段和复杂性评分的结构化实施计划
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---
# 创建计划

根据发现文档或用户输入，生成一个结构化的实施计划。

## 功能简介

1. 从发现文档（或用户输入）中提取需求。
2. 分析项目的范围和复杂性。
3. 将各个实施阶段按照复杂性评分（0-10分）进行分类。
4. 为每个阶段分配相应的任务。
5. 确保测试始终是最后一个阶段。

## 使用方法

```
/create-plan <discovery_document>
/create-plan "<feature_description>"
```

**参数：**
- `discovery_document`：发现文档的路径（推荐使用）
- `feature_description`：功能的直接描述（如果没有发现文档时使用）

## 输出结果

生成文件：`flow/plans/plan_<feature>_v<version>.md`

## 复杂性评分标准

| 评分 | 级别 | 描述 |
|-------|-------|-------------|
| 0-2 | 非常简单 | 仅涉及简单的、机械性的修改 |
| 3-4 | 较简单 | 实现过程较为直接 |
| 5-6 | 中等复杂 | 需要做出一些决策 |
| 7-8 | 相当复杂 | 需要考虑多个因素 |
| 9-10 | 非常复杂 | 复杂度较高，风险较大 |

## 计划结构

```markdown
# Plan: [Feature Name]

## Overview
Brief description

## Goals
- Goal 1
- Goal 2

## Phases

### Phase 1: [Name]
**Scope**: What this phase covers
**Complexity**: X/10

- [ ] Task 1
- [ ] Task 2

**Build Verification**: Run `npm run build`

### Phase N: Tests (Final)
**Scope**: Write comprehensive tests
**Complexity**: X/10

- [ ] Unit tests
- [ ] Integration tests

## Key Changes
1. **Category**: Description
```

## 示例

```
/create-plan @flow/discovery/discovery_user_auth_v1.md
```

## 重要规则

- **禁止编写代码**：计划仅描述需要实现的内容，不涉及具体的编码方式。
- **测试必须在最后阶段进行**：测试始终是计划的最后一个步骤。
- **禁止自动执行**：切勿自动调用 `/execute-plan` 命令。

## 下一步操作

创建计划后，请先对其进行审查，然后运行 `/execute-plan @flow/plans/plan_<feature>_v1.md` 命令。