---
name: codebase-documenter
description: 此技能适用于编写代码库的文档，包括 README 文件、架构文档、代码注释以及 API 文档。当用户需要帮助记录他们的代码、创建入门指南、解释项目结构，或使代码库对新开发者更易于理解时，可以运用此技能。该技能提供了模板、最佳实践以及结构化的方法，以生成清晰、适合初学者的文档。
---

# 代码库文档生成工具

## 概述

此技能能够帮助您为代码库创建全面且易于初学者理解的文档。它提供了结构化的模板和最佳实践，用于编写 README 文件、架构指南、代码注释以及 API 文档，帮助新用户快速了解项目并参与其中。

## 为初学者编写文档的核心原则

在为新用户编写代码文档时，请遵循以下基本原则：

1. **从“为什么”开始** – 在深入实现细节之前，先解释代码的目的。
2. **采用渐进式展示方式** – 从简单到复杂逐步呈现信息。
3. **提供背景说明** – 不仅解释代码的功能，还要说明其存在的理由。
4. **包含示例** – 为每个概念提供具体的使用示例。
5. **假设用户没有先验知识** – 尽量避免使用专业术语。
6. **使用可视化辅助工具** – 利用图表、流程图和文件结构图。
7. **快速上手** – 帮助用户在5分钟内就能运行代码。

## 文档类型及其适用场景

### 1. README 文档

**适用场景：** 项目根目录、主要功能模块或独立组件。

**编写结构：**
```markdown
# Project Name

## What This Does
[1-2 sentence plain-English explanation]

## Quick Start
[Get users running the project in < 5 minutes]

## Project Structure
[Visual file tree with explanations]

## Key Concepts
[Core concepts users need to understand]

## Common Tasks
[Step-by-step guides for frequent operations]

## Troubleshooting
[Common issues and solutions]
```

**最佳实践：**
- 首先介绍项目的价值主张。
- 提供可实际操作的设置指南（请进行测试！）
- 提供项目结构的可视化概览。
- 链接到更深入的文档（针对高级主题）。
- 保持 README 文件的重点在于帮助用户快速入门。

### 2. 架构文档

**适用场景：** 包含多个模块、复杂数据流或设计决策不明确的项目。

**编写结构：**
```markdown
# Architecture Overview

## System Design
[High-level diagram and explanation]

## Directory Structure
[Detailed breakdown with purpose of each directory]

## Data Flow
[How data moves through the system]

## Key Design Decisions
[Why certain architectural choices were made]

## Module Dependencies
[How different parts interact]

## Extension Points
[Where and how to add new features]
```

**最佳实践：**
- 使用图表展示系统组件及其之间的关系。
- 解释架构决策背后的理由。
- 文档化正常流程和错误处理方式。
- 明确模块之间的边界。
- 包含带有注释的文件结构图。

### 3. 代码注释

**适用场景：** 复杂逻辑、不易理解的算法或需要背景说明的代码。

**注释格式示例：**

**函数/方法文档：**
```javascript
/**
 * Calculates the prorated subscription cost for a partial billing period.
 *
 * Why this exists: Users can subscribe mid-month, so we need to charge
 * them only for the days remaining in the current billing cycle.
 *
 * @param {number} fullPrice - The normal monthly subscription price
 * @param {Date} startDate - When the user's subscription begins
 * @param {Date} periodEnd - End of the current billing period
 * @returns {number} The prorated amount to charge
 *
 * @example
 * // User subscribes on Jan 15, period ends Jan 31
 * calculateProratedCost(30, new Date('2024-01-15'), new Date('2024-01-31'))
 * // Returns: 16.13 (17 days out of 31 days)
 */
```

**复杂逻辑文档：**
```python
# Why this check exists: The API returns null for deleted users,
# but empty string for users who never set a name. We need to
# distinguish between these cases for the audit log.
if user_name is None:
    # User was deleted - log this as a security event
    log_deletion_event(user_id)
elif user_name == "":
    # User never completed onboarding - safe to skip
    continue
```

**最佳实践：**
- 解释“为什么”而不是“怎么做”——代码本身已经展示了功能。
- 文档化边缘情况和业务逻辑。
- 为复杂函数添加示例。
- 解释那些不显而易见的参数。
- 提醒潜在的问题或反直觉的行为。

### 4. API 文档

**适用场景：** 任何 HTTP 端点、SDK 方法或公共接口。

**编写结构：**
```markdown
## Endpoint Name

### What It Does
[Plain-English explanation of the endpoint's purpose]

### Endpoint
`POST /api/v1/resource`

### Authentication
[What auth is required and how to provide it]

### Request Format
[JSON schema or example request]

### Response Format
[JSON schema or example response]

### Example Usage
[Concrete example with curl/code]

### Common Errors
[Error codes and what they mean]

### Related Endpoints
[Links to related operations]
```

**最佳实践：**
- 提供可运行的 curl 示例。
- 显示成功和错误响应。
- 清晰解释认证流程。
- 文档化速率限制和约束条件。
- 包括常见问题的解决方法。

## 文档编写流程

### 第一步：分析代码库

在编写文档之前：
1. **确定入口点** – 主要文件、索引文件、应用程序初始化代码。
2. **梳理依赖关系** – 模块之间的相互依赖关系。
3. **识别核心概念** – 用户需要理解的关键抽象概念。
4. **查找配置信息** – 环境设置、配置文件。
5. **审查现有文档** – 在现有基础上进行补充，避免重复。

### 第二步：选择文档类型

根据用户需求和代码库分析情况选择合适的文档类型：
- **新项目或缺少 README 文件** → 从 README 文档开始。
- **架构复杂或包含多个模块** → 创建架构文档。
- **代码部分难以理解** → 添加内联代码注释。
- **HTTP/API 端点** → 编写 API 文档。
- **需要多种类型的文档** → 按顺序处理：README → 架构 → API → 注释。

### 第三步：生成文档

使用 `assets/templates/` 目录中的模板作为起点：
- `assets/templates/README.template.md` – 用于项目 README 文件。
- `assets/templates/ARCHITECTURE.template.md` – 用于架构文档。
- `assets/templates/API.template.md` – 用于 API 文档。

根据具体代码库进行模板定制：
1. **填写项目特定信息** – 用实际内容替换占位符。
2. **添加具体示例** – 使用项目中的实际代码。
3. **添加可视化辅助工具** – 创建文件结构图、图表。
4. **测试设置步骤** – 确保设置步骤能够正常工作。
5. **链接相关文档** – 将各个文档部分连接起来。

### 第四步：审查文档的清晰度

在最终确定文档之前：
1. **以初学者的角度阅读** – 不了解项目背景时，文档是否易于理解？
2. **检查完整性** – 解释是否有遗漏？
3. **验证示例** – 代码示例是否能够正常运行？
4. **测试设置步骤** – 用户能否按照步骤进行操作？
5. **优化结构** – 信息是否易于查找？

## 文档模板

此技能提供了 `assets/templates/` 目录中的多个模板，用于生成结构化的文档：

### 可用的模板：

- **README.template.md** – 包含快速入门、项目结构和常见任务的全面 README 文档模板。
- **ARCHITECTURE.template.md** – 包含系统设计、数据流和设计决策的架构文档模板。
- **API.template.md** – 包含请求/响应格式和示例的 API 端点文档模板。
- **CODE_COMMENTS.template.md** – 包含有效内联注释的示例和格式指南。

### 使用模板的方法：

1. 从 `assets/templates/` 目录中选择合适的模板。
2. 根据具体项目进行定制。
3. 添加项目特定的内容。
4. 使用代码库中的实际代码。
5. 删除不适用的部分。

## 最佳实践参考

有关详细的文档编写最佳实践、样式指南和高级技巧，请参考：
- `references/documentation_guidelines.md` – 全面的样式指南和最佳实践。
- `references/visual_aids_guide.md` – 如何创建有效的图表和文件结构图。

在以下情况下请参考这些资源：
- 为复杂的企业代码库编写文档时。
- 面对多个利益相关者的需求时。
- 需要高级文档编写技巧时。
- 在大型项目中统一文档格式时。

## 常见文档编写模式

### 创建文件结构图

文件结构图有助于新用户理解项目的组织结构：

```
project-root/
├── src/                    # Source code
│   ├── components/        # Reusable UI components
│   ├── pages/             # Page-level components (routing)
│   ├── services/          # Business logic and API calls
│   ├── utils/             # Helper functions
│   └── types/             # TypeScript type definitions
├── public/                # Static assets (images, fonts)
├── tests/                 # Test files mirroring src structure
└── package.json           # Dependencies and scripts
```

### 解释复杂的数据流

使用编号步骤和图表进行说明：

```
User Request Flow:
1. User submits form → 2. Validation → 3. API call → 4. Database → 5. Response

[1] components/UserForm.tsx
    ↓ validates input
[2] services/validation.ts
    ↓ sends to API
[3] services/api.ts
    ↓ queries database
[4] Database (PostgreSQL)
    ↓ returns data
[5] components/UserForm.tsx (updates UI)
```

### 文档化设计决策

记录架构选择背后的理由：

```markdown
## Why We Use Redux

**Decision:** State management with Redux instead of Context API

**Context:** Our app has 50+ components that need access to user
authentication state, shopping cart, and UI preferences.

**Reasoning:**
- Context API causes unnecessary re-renders with this many components
- Redux DevTools helps debug complex state changes
- Team has existing Redux expertise

**Trade-offs:**
- More boilerplate code
- Steeper learning curve for new developers
- Worth it for: performance, debugging, team familiarity
```

## 文档输出指南

在生成文档时，请注意：
1. **针对目标受众写作** – 根据文档的目标用户（初学者、中级用户或高级用户）调整复杂程度。
2. **保持格式一致性** – 遵循 markdown 规范和一致的标题层次结构。
3. **提供可运行的示例** – 测试所有代码片段和命令。
4. **建立文档之间的链接** – 创建清晰的文档导航结构。
5. **保持文档的可维护性** – 随着代码的更新，文档也应易于维护。
6. **添加日期和版本信息** – 记录文档的最后更新时间。

## 快速参考

**生成 README 文件的命令：**
“为该项目生成一个帮助新开发者快速入门的 README 文件。”

**生成架构文档的命令：**
“记录该代码库的架构，解释各个模块之间的交互方式。”

**添加代码注释的命令：**
“为该文件添加解释性注释，帮助新开发者理解代码逻辑。”

**生成 API 文档的命令：**
“为该文件中的所有 API 端点生成文档。”