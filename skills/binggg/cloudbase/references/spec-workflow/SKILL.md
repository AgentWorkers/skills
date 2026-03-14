---
name: spec-workflow
description: 标准的软件工程工作流程包括需求分析、技术设计和任务规划。在开发新功能、复杂架构设计、多模块集成或涉及数据库/用户界面设计的项目时，应使用这一流程。
alwaysApply: false
---
## 何时使用此技能

当您需要遵循**结构化开发工作流程**时，请使用此技能，具体包括以下情况：
- 从零开始开发新功能
- 设计复杂的系统架构
- 集成多个模块
- 参与涉及数据库设计的项目
- 参与涉及用户界面设计的项目
- 确保需求分析和验收标准的高质量

**不适用场景**：
- 简单的错误修复
- 文档更新
- 配置更改
- 代码重构（除非另有明确要求）

---

## 如何使用此技能（对于编码人员）

1. **严格遵循工作流程**：
   - 每个阶段都必须完成并得到用户的确认后，才能进入下一阶段
   - 绝不要跳过任何阶段或在没有用户确认的情况下直接进行下一步操作
   - 在需要进一步说明时，使用 `interactiveDialog` 工具

2. **应用 EARS 需求描述语法**：
   - 使用 EARS（Easy Approach to Requirements Syntax）来描述需求
   - 格式示例：`当 <可选前提条件> 时，<系统名称> 应该 <系统响应>`

3. **在需要时参考用户界面设计规范**：
   - 如果需求涉及前端页面，必须严格参考 `ui-design` 技能
   - 在需求阶段确定设计风格和颜色方案
   - 在最终确定需求之前，与用户确认设计细节

4. **更新任务状态**：
   - 在 `tasks.md` 文件中及时更新任务状态
   - 任务完成后，将其标记为已完成
   - 在保持质量的同时，独立高效地完成任务

---

# 规范工作流程

**重要提示：**在进入下一阶段之前，必须得到用户的确认。

## 工作流程概述

1. 如果您确定用户的输入是一个新的需求，可以按照标准软件工程实践独立进行工作。必要时与用户确认，并可以使用 `interactiveDialog` 工具收集信息。

2. 每当用户输入新的需求时，为了标准化需求的质量和验收标准，您必须首先清楚地理解问题和需求。在进入下一阶段之前，必须与用户确认。

## 第 1 阶段：需求文档和验收标准设计

首先使用 EARS（Easy Approach to Requirements Syntax）方法完成需求设计。如果需求涉及前端页面，**必须严格参考 `ui-design` 技能**。在需求阶段确定设计风格和颜色方案，并与用户确认需求细节。确认无误后，进入下一阶段。

将结果保存到 `specs/spec_name/requirements.md` 文件中。与用户确认后，进入下一阶段。

**参考格式：**

```markdown
# Requirements Document

## Introduction

Requirement description

## Requirements

### Requirement 1 - Requirement Name

**User Story:** User story content

#### Acceptance Criteria

1. Use EARS syntax: While <optional precondition>, when <optional trigger>, the <system name> shall <system response>. For example: When "Mute" is selected, the laptop shall suppress all audio output.
2. ...
...
```

## 第 2 阶段：技术解决方案设计

完成需求设计后，根据当前的技术架构和已确认的需求，设计技术解决方案。解决方案应简洁明了，同时准确描述技术架构（例如：架构、技术栈、技术选型、数据库/界面设计、测试策略、安全性等）。必要时可以使用 mermaid 图表进行可视化展示。

将结果保存到 `specs/spec_name/design.md` 文件中。务必与用户进行充分沟通后，再进入下一阶段。

## 第 3 阶段：任务分解

在完成技术解决方案设计后，根据需求文档和技术方案，分解具体的任务。与用户详细确认后，将结果保存到 `specs/spec_name/tasks.md` 文件中。与用户确认后，进入下一阶段并开始正式执行任务。在执行过程中，需要及时更新任务状态。尽可能独立自主地工作，以确保效率和质量。

**任务参考格式：**

```markdown
# Implementation Plan

- [ ] 1. Task Information
  - Specific things to do
  - ...
  - _Requirement: Related requirement point number
```

## 第 4 阶段：任务执行

- 开始正式执行任务
- 实时更新 `tasks.md` 文件中的任务状态
- 独立自主地完成任务
- 确保效率和质量
- 任务完成后，将其标记为已完成

## 关键原则

1. **用户确认**：每个阶段都必须得到用户的确认才能继续
2. **EARS 语法**：使用 EARS 方法来描述需求
3. **用户界面设计整合**：当需求涉及前端页面时，必须参考用户界面设计规范并在需求阶段确定设计风格
4. **技术准确性**：技术解决方案应简洁且准确无误
5. **任务跟踪**：在整个执行过程中持续更新任务状态
6. **独立执行**：在保持质量的同时，独立自主地完成任务