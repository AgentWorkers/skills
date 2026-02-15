---
name: writing-plans
description: 当您有一个多步骤任务的规范或需求时，在开始编写代码之前，请先使用此方法。
---

# 编写实施计划

## 概述

假设工程师对我们的代码库一无所知，且对代码质量的判断标准也不明确，为他们制定详细的实施计划。需要记录他们需要了解的所有信息：每项任务涉及的文件、代码、需要查阅的文档以及测试方法。将整个计划分解为易于执行的子任务。遵循“DRY”（Don’t Repeat Yourself）、“YAGNI”（Don’t Add What Isn’t Necessary）、“TDD”（Test-Driven Development，测试驱动开发）的原则，并鼓励频繁提交代码。

假设工程师具备一定的开发能力，但对我们使用的工具集或问题领域知之甚少，同时他们对良好的测试设计方法也了解不多。

**在开始时告知他们：**“我将使用‘编写实施计划’这项技能来创建实施计划。”

**执行环境：**该计划应在专门的工作目录中执行（该工作目录需通过“头脑风暴”技能创建）。

**计划保存路径：**`docs/plans/YYYY-MM-DD-<feature-name>.md`

## 任务分解的粒度

**每个步骤应包含一个具体的操作（耗时2-5分钟）：**
- “编写失败的测试用例”  
- “运行测试用例以确保其确实失败”  
- “编写最基本的代码以使测试通过”  
- “重新运行测试并确认所有测试都通过”  
- “提交代码”  

## 计划文档头部

**每个计划都必须以以下格式开头：**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## 任务结构

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected

def function(input):
    return expected
```

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```

## 注意事项：
- 必须提供完整的文件路径。
- 计划中应包含完整的代码示例，而不仅仅是代码片段。
- 使用`@`语法标注相关的技能或工具。
- 遵循“DRY”、“YAGNI”、“TDD”原则，并鼓励频繁提交代码。

## 执行流程

保存计划后，提供两种执行方式供选择：

**“计划已保存在`docs/plans/<filename>.md`文件中。有两种执行方式：**  
**1. **子代理驱动执行（当前会话）**：为每项任务分配一个新的子代理，任务之间进行代码审查，实现快速迭代。  
**2. **并行执行（单独会话）**：打开一个新的会话来执行计划，采用分批执行的方式，并设置检查点。**

**选择哪种执行方式？**

**如果选择“子代理驱动执行”：**  
- **必备辅助技能：** 使用`superpowers:subagent-driven-development`。  
- 请保持在该会话中继续执行任务，并在每项任务完成后进行代码审查。  

**如果选择“并行执行”：**  
- 指导他们在专门的工作目录中打开一个新的会话。  
- **必备辅助技能：** 使用`superpowers:executing-plans`。