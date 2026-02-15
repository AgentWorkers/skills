---
name: spec-generator
description: 生成针对 SpecWeave 增量的全面规范文件（包括 spec.md、plan.md 和 tasks.md，其中包含嵌入式测试）。这些文件可用于创建新的增量版本、规划功能开发，或将想法转化为可执行的规范。该工具采用经过验证的模板和基于上下文的组织结构，生成结构化、易于理解的文档。
---

# Spec Generator - 灵活的增量文档生成工具

**用途**：使用经过验证的模板和灵活的、基于上下文的结构，自动为 SpecWeave 的每个增量生成全面的规范文档（包括 spec.md、plan.md 和 tasks.md，其中包含嵌入式测试）。

**使用场景**：
- 创建新的增量（`/sw:inc` 命令）
- 规划功能或产品
- 生成结构化的文档
- 将想法转化为可执行的规范

**基于**：Flexible Spec Generator（V2）——具备上下文感知能力的非刚性模板

---

## Spec Generator 的工作原理

### 1. 灵活的规范生成（spec.md）

**适应不同场景**：
- **新产品**：包含市场分析、用户角色和竞争格局的完整产品需求文档（PRD）
- **功能添加**：聚焦于用户故事、验收标准和集成点
- **错误修复**：问题描述、根本原因、解决方案和影响分析
- **重构**：当前状态、建议的变更、好处和迁移计划

**YAML 前言部分**：
```yaml
---
increment: 0001-feature-name
title: "Feature Title"
type: feature
priority: P1
status: planned
created: 2025-12-04
# NOTE: project: and board: fields REMOVED from frontmatter!
# Use per-US **Project**: and **Board**: fields instead (see below)
---
```

**⛔ 重要规则：每个用户故事都必须包含 `**Project**:` 字段！**
- 这在单项目模式和多项目模式中都是强制性的。

**核心部分**（始终存在）：
```markdown
# Product Specification: [Increment Name]

**Increment**: [ID]
**Title**: [Title]
**Status**: Planning
**Priority**: [P0-P3]
**Created**: [Date]

## Executive Summary
[1-2 paragraph overview]

## Problem Statement
### Current State
### User Pain Points
### Target Audience

## User Stories & Acceptance Criteria

<!--
⛔ MANDATORY: **Project**: field on EVERY User Story
- Single-project: Use config.project.name value
- Multi-project: Use one of multiProject.projects keys
NEVER generate a User Story without **Project**: field!
-->

### US-001: [Title]
**Project**: [MANDATORY - use config.project.name or multiProject.projects key]
**Board**: [MANDATORY for 2-level structures only]

**As a** [user type]
**I want** [goal]
**So that** [benefit]

**Acceptance Criteria**:
- [ ] **AC-US1-01**: [Criterion 1]
- [ ] **AC-US1-02**: [Criterion 2]

---

### MANDATORY STEP 0: Get Project Context FIRST

**⛔ YOU CANNOT GENERATE spec.md UNTIL YOU COMPLETE THIS STEP!**

**This step is BLOCKING - do not proceed until you have actual project/board IDs.**

**🧠 ULTRATHINK REQUIRED - ANALYZE ALL AVAILABLE CONTEXT FIRST!**

Before assigning ANY project, you MUST analyze:
1. **Living docs structure**: `ls .specweave/docs/internal/specs/` - what project folders exist?
2. **Recent increments**: `grep -r "^\*\*Project\*\*:" .specweave/increments/*/spec.md | tail -10`
3. **config.json**: Read `project.name` (single-project) or `multiProject.projects` (multi-project)
4. **Feature description**: What does the user want to build? Match to existing projects.

**1. Run the context API command:**
```bash
specweave context projects
```

**2. Parse the JSON output:**
```json
{
  "level": 1,
  "projects": [{"id": "frontend-app", "name": "前端应用"}],
  "detectionReason": "多项目配置"
}
```
For 2-level:
```json
{
  "level": 2,
  "projects": [{"id": "acme-corp", "name": "ACME 公司"}],
  "boardsByProject": {
    "acme-corp": [
      {"id": "digital-ops", "name": "数字运营团队"},
      {"id": "mobile-team", "name": "移动团队"}
    ]
  }
}
```

**3. 🧠 ULTRATHINK - SMART PROJECT RESOLUTION:**

**RESOLUTION PRIORITY (MUST FOLLOW THIS ORDER!):**
```
1. ✅ 完全匹配：`config.project.name` 或 `multiProject.projects` 关键字 → 使用该项目
2. ✅ 现有文档：如果 `specs/` 目录中存在相应的项目 → 使用该项目 ID
3. ✅ 过去的模式：如果之前的增量中有相同的功能类型 → 使用相同的项目
4. ⚠️ 不确定：如果有多个有效选项或没有明确匹配 → 询问用户！
5. 🔄 备用方案：如果其他方法都失败 → 使用“default”项目（切勿使用“specweave”项目！）
```

**⚠️ CRITICAL: IF UNCERTAIN - YOU MUST ASK THE USER!**
```
我找到了与该功能相关的多个潜在项目：
- frontend-app（关键词：UI、表单、React）
- backend-api（关键词：API、端点）

应该将此功能分配给哪个项目？
```

**❌ NEVER DO THIS:**
- Silently assign to "specweave" (that's the framework name, not user's project!)
- Guess without analyzing context
- Skip asking when genuinely uncertain

**✅ CORRECT FALLBACK (when no projects configured):**
```
**项目**: default
```

**4. STORE the actual IDs for use in spec.md:**
```
RESOLVED_Project = "frontend-app"  // 来自 projects[]
RESOLVED_BOARD = "digital-ops"     // 来自 boardsByProject（仅二级结构）
```

**5. Now generate spec.md using RESOLVED values (NEVER placeholders!)**

---

### Per-US Project Resolution (MANDATORY)

**🧠 USE CONTEXT API OUTPUT + LIVING DOCS TO RESOLVE PROJECT/BOARD:**

After running `specweave context projects`, you have the valid project/board IDs.
Now map each user story to the correct project:

**Resolution Flow:**
```
1. 从上下文 API 中获取有效的项目：["frontend-app", "backend-api", "shared"]
2. 分析功能描述中的关键词
3. 将关键词映射到实际的项目 ID（来自步骤 1，避免使用通用术语！）
4. 将每个用户故事分配给相应的项目
```

**Resolution Example:**
```
上下文 API 返回的结果：projects = ["frontend-app", "backend-api", "shared"]

功能：“为 React 前端添加 OAuth 登录”
检测到的关键词：“React”、“frontend”、“login”

映射结果：
- “frontend”关键词 → 对应 “frontend-app”
- “login”关键词同时关联到 “frontend-app” 和 “backend-api”

**注意**：
- 在生成 spec.md 之前，必须先运行 `specweave context projects` 命令。
- 仅使用 API 响应中的项目 ID。
- 每个用户故事都必须有明确的 `**Project**` 字段。
- 对于二级结构的项目，每个用户故事还必须有明确的 `**Board**` 字段。

**禁止的行为**：
- 未先运行上下文 API 就直接生成 spec.md。
- 禁止使用 `{{PROJECT_ID}}` 或 `{{BOARD_ID}` 占位符。
- 禁止使用通用的项目名称（如 “frontend” 而不是 “frontend-app”）。
- 禁止使用 API 响应中不存在的项目名称。

### 2. 灵活的文档部分（取决于具体场景）：
- **竞争分析**（针对新产品）
- **技术要求**（针对复杂功能）
- **API 设计**（针对后端 API）
- **UI/UX 要求**（针对前端）
- **安全考虑**（针对认证/数据相关功能）
- **迁移计划**（针对涉及重大变更的功能）

### 3. 技术计划生成（plan.md）

**根据复杂度调整内容**：
- **简单功能**：组件列表、数据流、实现步骤
- **复杂系统**：完整架构图、序列图、实体关系图（ER 图）
- **基础设施**：部署架构、扩展策略、监控方案

**核心部分**：
```markdown
# Technical Plan: [Increment Name]

## Architecture Overview
[System design, components, interactions]

## Component Architecture
### Component 1
[Purpose, responsibilities, interfaces]

## Data Models
[Entities, relationships, schemas]

## Implementation Strategy
### Phase 1: [Name]
### Phase 2: [Name]

## Testing Strategy
[Unit, integration, E2E approach]

## Deployment Plan
[How we'll roll this out]

## Risks & Mitigations
```

### 4. 任务分解生成（tasks.md）

**智能任务创建**：
```markdown
# Implementation Tasks: [Increment Name]

## Task Overview
**Total Tasks**: [N]
**Estimated Duration**: [X weeks]
**Priority**: [P0]

---

## Phase 1: Foundation (Week 1) - X tasks

### T-001: [Task Title]
**Priority**: P0
**Estimate**: [X hours]
**Status**: pending

**Description**:
[What needs to be done]

**Files to Create/Modify**:
- `path/to/file.ts`

**Implementation**:
```[语言]
[代码示例或方法]
```

**Acceptance Criteria**:
- ✅ [Criterion 1]
- ✅ [Criterion 2]

---

[Repeat for all tasks]

## Task Dependencies
[Dependency graph if complex]
```

### 5. 测试策略生成（tests.md）

**全面的测试覆盖**：
```markdown
# Test Strategy: [Increment Name]

## Test Overview
**Total Test Cases**: [N]
**Test Levels**: [Unit, Integration, E2E, Performance]
**Coverage Target**: 80%+ overall, 90%+ critical

---

## Unit Tests (X test cases)

### TC-001: [Test Name]
```[语言]
describe('[组件]', () => {
  it('[应该执行某操作]', async () => {
    // 准备
    // 执行
    // 断言
  });
});
```

## Integration Tests (X test cases)
## E2E Tests (X test cases)
## Performance Tests (X test cases)

## Coverage Requirements
- Critical paths: 90%+
- Overall: 80%+
```

---

## 规范生成模板

### 模板选择逻辑

**输入分析**：
1. 分析增量的描述（关键词、复杂度）
2. 确定领域（前端、后端、基础设施、机器学习等）
3. 确定范围（功能、产品、错误修复、重构）
4. 评估技术复杂度（简单、中等、复杂）

**模板选择**：
```
IF new_product THEN
  spec_template = "Full PRD"
  plan_template = "System Architecture"
ELSE IF feature_addition THEN
  spec_template = "User Stories Focused"
  plan_template = "Component Design"
ELSE IF bug_fix THEN
  spec_template = "Problem-Solution"
  plan_template = "Implementation Steps"
ELSE IF refactoring THEN
  spec_template = "Current-Proposed"
  plan_template = "Migration Strategy"
END IF
```

### 基于上下文的自动包含内容**：
- **“authentication”** → 安全考虑、JWT/OAuth 设计
- **“API”** → API 设计、OpenAPI 规范、速率限制
- **“database”** → 实体关系图、迁移脚本、索引
- **“frontend”** → 组件层次结构、状态管理、UI/UX
- **“deployment”** → 持续集成/持续部署（CI/CD）、基础设施、监控
- **“ML”** → 模型架构、训练流程、评估指标

---

## 使用示例

### 示例 1：简单功能
```
User: /sw:inc "Add dark mode toggle to settings"

Spec Generator:
✓ Detected: Frontend feature (UI component)
✓ Complexity: Simple
✓ Template: User Stories + Component Design

Generating specifications...
✓ spec.md: 3 user stories, UI mockups section
✓ plan.md: Component design, state management, CSS-in-JS
✓ tasks.md: 8 tasks (component, styles, state, tests)
✓ tests.md: Unit tests for component, E2E for toggle
```

### 示例 2：复杂系统
```
User: /sw:inc "Multi-tenant SaaS platform with billing"

Spec Generator:
✓ Detected: New product (SaaS, multi-tenant, payments)
✓ Complexity: High
✓ Template: Full PRD + System Architecture

Generating specifications...
✓ spec.md: Market analysis, personas, competitive landscape, 15 user stories
✓ plan.md: Multi-tenant architecture, database per tenant, Stripe integration, C4 diagrams
✓ tasks.md: 40 tasks across 4 weeks (auth, tenancy, billing, UI)
✓ tests.md: 100+ test cases (unit, integration, E2E, load testing)
```

### 示例 3：错误修复
```
User: /sw:inc "Fix race condition in user session handling"

Spec Generator:
✓ Detected: Bug fix (concurrency issue)
✓ Complexity: Moderate
✓ Template: Problem-Solution

Generating specifications...
✓ spec.md: Problem statement, root cause analysis, impact, solution
✓ plan.md: Current implementation, proposed fix, Redis locking
✓ tasks.md: 5 tasks (analysis, fix, tests, rollout, monitoring)
✓ tests.md: Concurrency tests, stress tests
```

---

## 与 `/sw:inc` 的集成

Spec Generator 会通过 `/sw:inc` 命令自动触发：
1. **用户意图分析**：
   - 分析增量描述
   - 检测关键词、领域和复杂度
2. **模板选择**：
   - 选择合适的模板
   - 自动包含相关部分
3. **规范生成**：
   - 生成包含项目管理的 spec.md
   - 生成包含架构设计的 plan.md
   - 生成包含任务分解的 tasks.md
   - 生成包含测试策略的 tests.md
4. **用户审核**：
   - 显示生成的文档结构
   - 允许用户进行修改
   - 在创建文件前确认内容

---

## 与刚性模板的优势

**灵活的（V2）方法**：
- ✅ 适应不同的增量类型（产品、功能、错误修复、重构）
- ✅ 仅包含相关内容
- ✅ 能够根据复杂度灵活调整
- ✅ 具有领域针对性（前端、后端、机器学习、基础设施）
- ✅ 对简单增量处理更快
- ✅ 对复杂产品生成全面的文档

**刚性的（V1）方法**：
- ✅ 所有增量都使用相同的模板
- ✅ 包含许多无关的内容
- ✅ 在简单功能上浪费时间
- ✅ 对复杂产品支持不足
- ✅ 无法满足多样化需求

---

## 配置

用户可以在 `.specweave/config.yaml` 文件中自定义规范生成设置：

```yaml
spec_generator:
  # Default complexity level
  default_complexity: moderate  # simple | moderate | complex

  # Always include sections
  always_include:
    - executive_summary
    - user_stories
    - success_metrics

  # Never include sections
  never_include:
    - competitive_analysis  # We're not doing market research

  # Domain defaults
  domain_defaults:
    frontend:
      include: [ui_mockups, component_hierarchy, state_management]
    backend:
      include: [api_design, database_schema, authentication]
```

---

## 🔀 多项目用户故事生成

**重要提示**：当检测到多项目模式时，每个用户故事都必须针对具体的项目生成！

### 检测步骤（必须执行）：

**自动检测**：使用 `src/utils/multi-project-detector.ts` 中的 `detectMultiProjectMode(projectRoot)` 函数。该工具会自动检查所有配置文件。

**手动检查（适用于管理员）**：阅读 `.specweave/config.json` 并检查以下内容：
- `umbrella.enabled` 和 `childRepos[]`
- `multiProject.enabled` 和 `projects{}`
- `sync.profiles[].config.boardMapping`
- `.specweave/docs/internal/specs/` 目录下是否存在多个文件夹

**如果满足以下任意条件，则表示处于多项目模式**：
- `config.json` 中的 `umbrella.enabled` 为 `true`
- `umbrella.childRepos` 中有项目条目
- `specs/` 目录下存在多个项目文件夹（例如 `sw-app-fe/`, `sw-app-be/`, `sw-app-shared/`
- 用户在输入中提到了多个项目（如 “3 个仓库”、“前端仓库”、“后端 API”、“共享库”）

### 每个用户故事指定目标项目（推荐）

每个用户故事都应明确指定其目标项目：

```markdown
## User Stories

### US-001: Thumbnail Upload & Comparison (P1)
**Project**: frontend-app
**Board**: ui-team        <!-- 2-level structures only -->
**As a** content creator
**I want** to upload multiple thumbnail variants
**So that** I can visually evaluate my options

**Acceptance Criteria**:
- [ ] **AC-US1-01**: User can drag-and-drop up to 5 images

---

### US-002: CTR Prediction API (P1)
**Project**: backend-api
**Board**: ml-team        <!-- 2-level structures only -->
**As a** frontend application
**I want** to call POST /predict-ctr endpoint
**So that** I can get AI-powered predictions

**Acceptance Criteria**:
- [ ] **AC-US2-01**: POST /predict-ctr accepts thumbnail image
```

**指定目标项目的优点**：
- 每个用户故事都会关联到正确的项目/仓库
- 单个增量可以涉及多个项目
- 文档会自动按项目分组
- 外部工具（如 GitHub/JIRA/ADO）会将问题记录在正确的项目中

### 多项目用户故事格式（每个用户故事都包含 **Project** 字段）

**✅ 正确的格式要求**：
```markdown
## User Stories

### US-001: Thumbnail Upload
**Project**: frontend-app       # ← MANDATORY!
**As a** content creator
**I want** to upload thumbnails
**So that** I can test different versions

**Acceptance Criteria**:
- [ ] **AC-US1-01**: User can drag-and-drop images
- [ ] **AC-US1-02**: Images validated for YouTube specs

### US-002: Thumbnail Analysis API
**Project**: backend-api        # ← MANDATORY! Different project = different folder
**As a** frontend application
**I want** to call POST /predict-ctr endpoint
**So that** I can get AI-powered predictions

**Acceptance Criteria**:
- [ ] **AC-US2-01**: POST /predict-ctr endpoint accepts thumbnail image
- [ ] **AC-US2-02**: ML model returns prediction score
```

### 项目分类规则

在分析用户故事时，根据关键词对项目进行分类：

| 关键词 | 项目 | 前缀 |
|----------|---------|--------|
| UI、组件、页面、表单、视图、拖放、主题、构建器、菜单显示 | 前端 | FE |
| API、端点、CRUD、Webhook、分析、数据库、服务、机器学习模型 | 后端 | BE |
| 类型、模式、验证器、工具、本地化、通用功能 | 共享 | SHARED |
| iOS、Android、移动应用、推送通知 | 移动端 | MOBILE |
| Terraform、K8s、Docker、持续集成/持续部署 | 基础设施 | INFRA |

### 按项目分类的 AC-ID 格式

```
AC-{PROJECT}-US{story}-{number}

Examples:
- AC-FE-US1-01 (Frontend, User Story 1, AC #1)
- AC-BE-US1-01 (Backend, User Story 1, AC #1)
- AC-SHARED-US1-01 (Shared, User Story 1, AC #1)
- AC-MOBILE-US1-01 (Mobile, User Story 1, AC #1)
```

### tasks.md 必须引用特定项目的项目相关用户故事

```markdown
### T-001: Create Thumbnail Upload Component
**User Story**: US-FE-001           ← MUST reference project-scoped ID!
**Satisfies ACs**: AC-FE-US1-01, AC-FE-US1-02
**Status**: [ ] Not Started

### T-004: Database Schema & Migrations
**User Story**: US-BE-001, US-BE-002   ← Backend stories only!
**Satisfies ACs**: AC-BE-US1-01, AC-BE-US2-01
**Status**: [ ] Not Started
```

### 工作流程总结

```
1. DETECT multi-project mode (check config.json, folder structure)
   ↓
2. If multi-project → Group user stories by project (FE/BE/SHARED/MOBILE/INFRA)
   ↓
3. Generate prefixed user stories: US-FE-001, US-BE-001, US-SHARED-001
   ↓
4. Generate prefixed ACs: AC-FE-US1-01, AC-BE-US1-01
   ↓
5. Generate tasks referencing correct project user stories
   ↓
6. Each project folder gets its own filtered spec
```

### 这个功能的重要性

**不使用项目分类的用户故事会导致**：
- 所有问题都记录在同一个仓库中（错误！）
- 无法明确哪些任务属于哪个团队
- 任务引用错误的项目
- GitHub 上的问题记录在错误的仓库中

**使用项目分类的用户故事后**：
- 每个仓库只包含属于它的用户故事
- 明确每个团队/仓库的任务归属
- GitHub 上的问题记录在正确的仓库中
- 问题得到清晰的分层管理

---

## 相关技能

- **计划工作流程**：指导增量规划（内部使用 Spec Generator）
- **上下文加载**：为规范生成加载相关上下文
- **质量验证**：验证生成的规范是否完整
- **多项目规范分割器**：将规范文件按项目分类
- **多仓库架构检测器**：检测多仓库架构

---

---

**基于**：Flexible Spec Generator（V2）——具备上下文感知能力的非刚性模板