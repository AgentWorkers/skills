---
name: code-task-generator
description: 根据描述或PDD实施计划生成结构化的`.code-task.md`文件。自动检测输入类型，并创建格式正确的任务，同时包含“给定条件-执行操作-预期结果”（Given-When-Then）的验收标准。
type: anthropic-skill
version: "1.1"
---

# 代码任务生成器

## 概述

该工具能够根据粗略的描述或PDD（设计文档）实施计划生成结构化的代码任务文件。它会自动检测输入类型，并创建格式正确的`.code-task.md`文件。对于PDD计划，工具会逐个步骤进行处理，以便用户在各个步骤之间进行学习。

## 重要说明

以下规则适用于所有步骤：

- **需要用户批准**：在生成任何文件之前，必须向用户展示任务分解计划并获取明确批准。
- **集成测试**：在每个任务的验收标准中包含单元测试要求。切勿单独创建“添加测试”的任务。
- **引用设计文档**：始终将设计文档的路径作为必读内容。只有与特定任务直接相关的研究文档才需要包含在内。

## 参数

- **input**（必填）：任务描述、文件路径或PDD计划路径
- **step_number**（可选，仅限PDD模式）：要处理的特定步骤。如果省略，则会自动确定下一个未完成的步骤。
- **output_dir**（可选，默认值：`specs/{task_name}/tasks/`）：代码任务文件的输出目录
- **task_name**（可选，仅限描述模式）：覆盖自动生成的任务名称

**限制**：
- 必须在单个提示中一次性询问所有必需的参数。
- 支持以下输入形式：纯文本、文件路径、目录路径（查找`plan.md`文件）或URL。

## 步骤

### 1. 检测输入类型

检查输入是否为具有PDD计划结构的文件（包含检查列表和编号步骤）。将模式设置为“pdd”或“description”，并告知用户。

### 2. 分析输入

- **PDD模式**：解析计划内容，提取步骤和检查列表的状态，确定目标步骤（根据`step_number`或第一个未完成的步骤确定）。
- **描述模式**：识别核心功能、技术要求、复杂度级别（低/中/高）和技术领域。

### 3. 构建需求

- **PDD模式**：提取目标步骤的标题、描述、演示要求、约束条件以及与之前步骤的集成说明。确定相关的研究文档。
- **描述模式**：识别功能需求，推断技术约束和依赖关系。

对于这两种模式，都需要以“Given-When-Then”格式创建可衡量的验收标准，并准备任务分解计划。

### 4. 规划任务

向用户展示建议的任务分解方案：
- 每个任务的一行总结
- 建议的执行顺序和依赖关系
- 在用户明确批准之前，不得生成任何文件。

### 5. 生成任务

按照以下代码任务格式创建文件。

**PDD模式的详细要求：**
- 创建`step{NN}/`文件夹（使用零填充格式：step01, step02, step10等）
- 按顺序命名文件：`task-01-{title}.code-task.md`, `task-02-{title}.code-task.md`
- 按功能组件进行分类，而非按测试阶段分类

**所有任务**：
- 必须使用以下代码任务格式结构
- 必须包含YAML前置内容，其中包含`status: pending`, `created: YYYY-MM-DD`, `started: null`, `completed: null`
- 必须使用驼峰式命名法，并加上`.code-task.md`扩展名
- 必须包含涵盖主要功能和单元测试的验收标准

### 6. 报告结果

列出生成的文件及其路径。对于PDD模式，还需包含步骤的演示要求。建议按顺序运行代码辅助工具（code-assist），或使用Ralph工具进行自动化实现。

### 7. 提供Ralph集成服务

询问用户：“您是否希望我使用Ralph来自动执行这些任务？”

如果用户同意，创建一个简洁的`PROMPT.md`文件，其中包含目标、规范目录引用、执行顺序和验收标准。建议使用以下命令：
- 完整流程：`ralph run --config presets/pdd-to-code-assist.yml`
- 简化流程：`ralph run --config presets/spec-driven.yml`

## 代码任务格式规范

每个代码任务文件都必须遵循以下结构：

```markdown
---
status: pending
created: YYYY-MM-DD
started: null
completed: null
---
# Task: [Task Name]

## Description
[What needs to be implemented and why]

## Background
[Context needed to understand the task]

## Reference Documentation
**Required:**
- Design: specs/{task_name}/design.md

**Additional References (if relevant to this task):**
- [Specific research document or section]

**Note:** Read the design document before beginning implementation.

## Technical Requirements
1. [First requirement]
2. [Second requirement]

## Dependencies
- [Dependency with details]

## Implementation Approach
1. [Implementation step or approach]

## Acceptance Criteria

1. **[Criterion Name]**
   - Given [precondition]
   - When [action]
   - Then [expected result]

## Metadata
- **Complexity**: [Low/Medium/High]
- **Labels**: [Comma-separated labels]
- **Required Skills**: [Skills needed]
```

## 示例

**描述模式输入：**`“我需要一个能够验证电子邮件地址并返回详细错误信息的函数”`

**描述模式输出：**`specs/email-validator/tasks/email-validator.code-task.md` — 该任务包含关于有效/无效电子邮件处理、错误信息以及单元测试的验收标准。

**PDD模式输入：**`specs/data-pipeline/plan.md`

**PDD模式输出：**`specs/data-pipeline/tasks/step02/` 目录下包含`task-01-create-data-models.code-task.md`, `task-02-implement-validation.code-task.md`, `task-03-add-serialization.code-task.md` — 每个文件都包含设计文档的引用、验收标准和演示要求。

## 故障排除

- **描述模糊**：提出澄清问题，建议常见的处理方式，并提供基本的任务模板供用户细化。
- **描述复杂**：建议将任务拆分为更小的部分，先关注核心功能，然后创建相关任务。
- **缺少技术细节**：做出合理的假设，提供多种实现方案，并指出需要用户决策的环节。
- **找不到计划文件**：检查路径是否为目录（在目录内查找`plan.md`文件），并提供常见的PDD计划存放位置。
- **计划格式无效**：识别缺失的部分，建议运行PDD工具生成正确的计划，然后提取可用信息。
- **所有步骤已完成**：通知用户，询问他们是否还需要处理特定步骤，或建议重新审查以确定是否需要添加新步骤。