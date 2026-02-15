---
name: increment-planner
description: 在项目经理（PM）和架构师（Architect）的协作下，规划和创建 SpecWeave 的增量更新。该流程适用于启动新功能、进行紧急修复（hotfixes）、处理 bug，或任何需要详细规范和任务分解的开发工作。通过该流程，会生成 spec.md、plan.md 和 tasks.md 文件，并确保这些文件包含正确的 AC-IDs（活动代码标识符），同时实现与现有文档系统的集成。
visibility: public
context: fork
model: opus
hooks:
  PreToolUse:
    - matcher: Write
      hooks:
        - type: command
          command: bash plugins/specweave/hooks/v2/guards/spec-template-enforcement-guard.sh
---

# 增量规划技能（Increment Planning Skill）

**适用于任何用户项目，在执行 `specweave init` 后使用的自包含增量规划工具。**

## 逐步披露（Progressive Disclosure）

根据需要加载各个阶段，以减少上下文信息量：

| 阶段 | 加载时机 | 文件名 |
|-------|--------------|------|
| 预飞行阶段（Pre-flight） | 开始规划时 | `phases/00-preflight.md` |
| 项目背景（Project Context） | 解决项目/团队相关问题时 | `phases/01-project-context.md` |
| 创建增量（Create Increment） | 创建相关文件时 | `phases/02-create-increment.md` |
| 参考资料（Reference） | 示例与故障排除指南 | `phases/03-reference.md` |

## 快速参考（Quick Reference）

### 增量类型（Increment Types）

| 类型 | 使用场景 | 在进行中的任务数量上限 |
|------|----------|-----------|
| **功能开发（Feature）** | 新功能的开发 | 最多2个任务 |
| **热修复（Hotfix）** | 产品出现故障时 | 无限制 |
| **漏洞修复（Bug）** | 需要根本原因分析（RCA）时 | 无限制 |
| **变更请求（Change Request）** | 业务需求变更时 | 最多2个任务 |
| **代码重构（Refactor）** | 用于处理技术债务时 | 最多1个任务 |
| **实验性功能（Experiment）** | 用于测试或快速原型开发时 | 无限制 |

### 目录结构（Directory Structure）

```
.specweave/increments/####-name/
├── metadata.json  # REQUIRED - create FIRST
├── spec.md        # REQUIRED - user stories, ACs
├── plan.md        # OPTIONAL - architecture
└── tasks.md       # REQUIRED - implementation
```

## 工作流程概述（Workflow Overview）

```
STEP 0: Pre-flight (TDD mode, multi-project)
        → Load phases/00-preflight.md

STEP 1: Project Context (resolve project/board)
        → Load phases/01-project-context.md

STEP 2: Create Increment (via Template API)
        → Load phases/02-create-increment.md

STEP 3: Guide User (complete in main conversation)
```

## 重要规则（Critical Rules）

### 1. 必须填写“项目字段”（Project Field）

每个增量规划任务都必须包含 `**Project:**` 字段：
```markdown
### US-001: Feature Name
**Project**: my-app    # ← REQUIRED!
**As a** user...
```

获取项目信息：`specweave context projects`

### 2. 使用模板创建器 API（Use the Template Creator API）

**禁止直接编写代码！** 请使用官方提供的 API 进行操作：
```bash
specweave create-increment --id "0021-name" --project "my-app"
```

### 3. 禁止生成任务代理（No Agent Spawning）

增量规划技能不允许生成 `Task()` 类型的代理任务（这可能导致程序崩溃）。请引导用户通过主线对话来完成相关操作。

### 4. 增量命名规则（Increment Naming Rules）

命名格式：`####-描述性内容-驼峰式命名法（descriptive-kebab-case）`

```
✅ 0001-user-authentication
❌ 0001 (no description)
❌ my-feature (no number)
```

## 令牌预算（Token Budget）

- **快速参考文件**：约需 400 个令牌
- **每个阶段**：约需 300–500 个令牌
- **全部阶段加载完毕**：总计约需 2000 个令牌

**请按需加载各个阶段，不要一次性加载所有内容！**

## 任务分配（Delegation Rules）

- **预飞行检查**：使用 `/sw:increment` 命令进行任务分配与管理
- **规格文档完成**：由项目经理（PM）负责相关任务
- **架构设计**：由架构师负责相关任务
- **任务生成**：由具备测试知识的规划工具负责

## 使用方法（Usage Instructions）

```typescript
// Direct invocation
Skill({ skill: "sw:increment-planner", args: "--description=\"Add auth\"" })

// Via command (recommended - handles pre-flight)
/sw:increment "Add user authentication"
```

> **注意**：请使用前缀 `sw:`！直接使用 `increment-planner` 会导致错误。