---
name: role-orchestrator
description: 这是一个多代理协调系统，能够整合产品经理（PM）、架构师（Architect）、DevOps团队、质量保证（QA）人员、技术负责人（Tech Lead）以及安全专家（Security Agent），共同完成复杂任务。该系统适用于构建完整产品、开发SaaS应用程序，或任何需要多个专业团队协作的端到端项目。它采用了分层式的协调器-工作者（Orchestrator-Worker）架构模式。
---

# 角色编排器 - 多代理协调系统

**一个独立运行的编排系统，可在任何用户项目中使用，只需执行 `specweave init` 即可。**

---

## 目的

通过智能的任务分解和角色分配，协调多个专业代理来执行复杂的多步骤任务。

**架构**：分层式的编排器-工作节点模式
```
User Request → Orchestrator → PM → Architect → Tech Lead → Implement → QA → Deploy
```

---

## 何时启用

在需要 **3个或更多代理** 或 **完整产品开发** 的情况下启用该系统：

| 用户需求 | 所需代理 | 运行模式 |
|-----------|---------------|---------|
| “开发一个SaaS产品” | 产品经理 → 架构师 → 技术负责人 → 开发人员 → 测试人员 → DevOps团队 | 顺序执行 |
| “创建实时聊天功能” | 架构师 → 后端开发 → 前端开发 → 测试人员 | 并行执行 |
| “实现安全认证机制” | 安全专家 → 技术负责人 → 后端开发 → 测试人员 | 顺序执行 |
| “优化系统性能” | 技术负责人 → 性能优化团队 → 后端开发 → DevOps团队 | 迭代执行 |

---

## 代理角色

### 战略层

**产品经理代理 (pm-agent)**
- 负责产品策略、用户需求梳理及优先级制定
- **适用场景**：新产品/功能的启动阶段

**架构师代理 (architect-agent)**
- 负责系统设计及技术选型
- **适用场景**：系统设计或重要功能的开发阶段

### 执行层

**技术负责人代理 (tech-lead-agent)**
- 负责技术规划、代码审查及质量标准制定
- **适用场景**：需要做出复杂技术决策的场景

**后端开发代理 (backend-agent)**
- 负责使用 Node.js、Python 或 .NET 开发后端服务
- **适用场景**：服务器端代码实现

**前端开发代理 (frontend-agent)**
- 负责使用 React/Next.js 等技术进行前端界面开发
- **适用场景**：用户界面的构建

### 质量与运维层

**测试负责人代理 (qa-lead-agent)**
- 负责测试策略的制定及质量保证工作
- **适用场景**：测试流程的规划阶段

**安全专家代理 (security-agent)**
- 负责安全架构的设计及威胁建模
- **适用场景**：涉及安全性的关键功能开发

**DevOps 代理 (devops-agent)**
- 负责基础设施搭建、持续集成/持续部署（CI/CD）及监控工作
- **适用场景**：运维相关任务的执行

---

## 关键规则：安全的编排流程

**规则**：编排器负责构建整体框架，并指导用户按主流程调用各个代理（禁止嵌套调用代理）。

### 第0阶段：首先创建增量开发结构

在调用任何代理之前，必须先创建一个增量开发文件夹：

```typescript
// 1. Parse user request
const projectName = extractProjectName(userRequest);
// "event management" → "event-management"

// 2. Get next number
const nextNumber = getNextIncrementNumber();
// e.g., 0001, 0002, 0003

// 3. Create structure
const incrementPath = `.specweave/increments/${nextNumber}-${projectName}/`;
mkdir -p ${incrementPath}
mkdir -p ${incrementPath}logs/
mkdir -p ${incrementPath}scripts/
mkdir -p ${incrementPath}reports/

// 4. Create placeholder files (ORDER MATTERS!)
// metadata.json MUST be created FIRST (metadata-json-guard.sh blocks spec.md otherwise)
write ${incrementPath}metadata.json (MANDATORY - CREATE FIRST!)
write ${incrementPath}spec.md (basic template)
write ${incrementPath}plan.md (basic template)
write ${incrementPath}tasks.md (basic template)
```

**metadata.json 模板**（必须先创建！）：
```json
{
  "id": "0001-project-name",
  "status": "planned",
  "type": "feature",
  "priority": "P1",
  "created": "2025-11-24T12:00:00Z",
  "lastActivity": "2025-11-24T12:00:00Z"
}
```

**spec.md 模板**（在创建 metadata.json 之后创建）：
```yaml
---
increment: 0001-project-name
title: "Project Name"
type: feature
priority: P1
status: planned
created: 2025-11-24
---

# Project Name

## Overview
(To be filled by PM Agent)

## User Stories
(To be filled by PM Agent)
```

### 第1阶段：指导用户完成代理工作流程

**将此工作流程展示给用户**：

```
✅ Increment structure created: .specweave/increments/0001-project-name/

🎯 Complete workflow (run these commands in MAIN conversation):

STEP 1: Product Strategy & Requirements
Tell Claude: "Complete the spec for increment 0001-project-name"
(PM agent will activate automatically)

STEP 2: Architecture & Design
Tell Claude: "Design architecture for increment 0001-project-name"
(Architect agent will create ADRs and system design)

STEP 3: Technical Planning
Tell Claude: "Create technical plan for increment 0001-project-name"
(Tech Lead agent will create implementation approach)

STEP 4: Implementation Tasks
Tell Claude: "Create tasks for increment 0001-project-name"
(Test-aware planner will generate tasks with tests)

STEP 5: Security Review (if needed)
Tell Claude: "Review security for increment 0001-project-name"
(Security agent will perform threat modeling)

STEP 6: Implementation
Tell Claude: "Implement increment 0001-project-name"
(Backend/Frontend agents will implement code)

STEP 7: Quality Assurance
Tell Claude: "Run QA for increment 0001-project-name"
(QA agent will verify tests and coverage)

STEP 8: Deployment Planning
Tell Claude: "Plan deployment for increment 0001-project-name"
(DevOps agent will create infrastructure)

⚠️  Run these sequentially in MAIN conversation to prevent context explosion!
```

****请勿使用 Task() 工具同时启动所有代理！**

---

## 编排模式

### 模式1：顺序执行（默认模式）

**适用场景**：任务之间存在依赖关系
```
PM → Architect → Tech Lead → Backend → Frontend → QA → DevOps
```

**用户操作流程**：
1. 创建增量开发结构
2. 按顺序调用各个代理
3. 每个代理完成后再启动下一个代理
4. 用户实时跟踪进度

### 模式2：并行执行

**适用场景**：任务之间相互独立
```
PM + Architect (parallel)
    ↓
Backend + Frontend (parallel)
    ↓
QA + DevOps (parallel)
```

**用户操作流程**：
1. 创建增量开发结构
2. 识别可以并行执行的代理任务
3. 指导用户：“这些任务可以同时执行：[代理列表]”
4. 用户同时启动这些代理

### 模式3：自适应执行（根据实际情况调整）

**适用场景**：在执行过程中发现新的需求
```
PM → Architect → [Discover need] → Security → Tech Lead → ...
```

**用户操作流程**：
1. 根据初始计划开始执行
2. 代理在运行过程中发现新的需求
3. 在流程中动态添加新的代理
4. 动态调整执行计划

---

## 质量检查点（关卡）

### 第1关卡：产品经理完成需求梳理后
**检查内容**：
- [ ] 用户需求已明确，并分配了相应的 AC 编号
- [ ] 成功标准已确定
- [ ] 任务之间的依赖关系已明确
- [ ] 超出项目范围的需求已被排除

**决策**：继续进行系统设计或进一步完善需求

### 第2关卡：架构师完成设计后
**检查内容**：
- [ ] 系统设计文档已完成
- [ ] 详细的设计文档（ADRs）已生成（至少3份）
- [ ] 技术选型已确定
- [ ] 数据模型已定义

**决策**：继续进行代码实现或重新设计系统

### 第3关卡：代码实现完成后
**检查内容**：
- [ ] 所有 P1 阶段的任务均已完成
- [ ] 测试通过率达到80%以上
- [ ] 代码已通过审查
- [ ] 文档已更新

**决策**：准备进行部署或解决存在的问题

### 第4关卡：部署前
**检查内容**：
- [ ] 安全审查已通过
- [ ] 系统性能符合要求
- [ ] 监控机制已配置
- [ ] 有备用的回滚方案

**决策**：进行部署或解决剩余问题

---

## 错误处理

### 代理故障处理
```
If agent fails:
1. Capture error details
2. Retry with backoff (max 3 attempts)
3. Try fallback agent if available
4. If critical: pause and notify user
5. NEVER fail silently
```

### 优雅的降级处理
```
If PM fails → Use basic template
If Architect fails → Tech Lead creates simple design
If Backend fails → Create manual implementation guide
If DevOps fails → Create manual deployment steps
```

### 用户干预机制
```
If orchestrator stuck:
1. Show current state
2. Present options to user
3. Let user decide next step
4. Resume from checkpoint
```

---

## 进度跟踪

**实时更新**

向用户展示当前的工作阶段和进度：
```
🚀 Building SaaS for Event Management

Progress: 3/8 phases complete (37.5%)

✅ Phase 1: Requirements (PM) - COMPLETE
✅ Phase 2: Architecture (Architect) - COMPLETE
✅ Phase 3: Technical Planning (Tech Lead) - COMPLETE
🔄 Phase 4: Implementation (Backend + Frontend) - IN PROGRESS
⏳ Phase 5: QA - PENDING
⏳ Phase 6: Security Review - PENDING
⏳ Phase 7: DevOps - PENDING
⏳ Phase 8: Deployment - PENDING

Current: Backend implementing user authentication (T-015/45)
```

---

## 示例工作流程

### 示例1：开发SaaS产品

**用户需求**：“开发一个用于事件管理的SaaS产品”

**编排器响应**：
```
🎯 Creating increment for Event Management SaaS

Created: .specweave/increments/0001-event-management/

📋 8-Phase Workflow:

Phase 1: Requirements & Strategy
Tell Claude: "Complete spec for increment 0001"
→ PM will define user stories, features, success criteria

Phase 2: System Architecture
Tell Claude: "Design architecture for increment 0001"
→ Architect will create system design and ADRs

Phase 3: Technical Planning
Tell Claude: "Create technical plan for increment 0001"
→ Tech Lead will plan implementation approach

Phase 4: Test Strategy
Tell Claude: "Create test strategy for increment 0001"
→ QA Lead will define testing approach

Phase 5: Backend Implementation
Tell Claude: "Implement backend for increment 0001"
→ Backend agent will build APIs and services

Phase 6: Frontend Implementation
Tell Claude: "Implement frontend for increment 0001"
→ Frontend agent will build UI

Phase 7: Security Review
Tell Claude: "Review security for increment 0001"
→ Security agent will validate security

Phase 8: Deployment Setup
Tell Claude: "Setup deployment for increment 0001"
→ DevOps agent will create infrastructure

Start with Phase 1!
```

### 示例2：紧急修复安全漏洞

**用户需求**：“修复安全漏洞 CVE-2024-1234”

**编排器响应**：
```
🚨 CRITICAL HOTFIX WORKFLOW

Created: .specweave/increments/0016-security-fix-cve-2024-1234/
Type: hotfix (expedited workflow)

⚡ 4-Phase Fast Track:

Phase 1: Security Assessment (5 min)
Tell Claude: "Assess security vulnerability for increment 0016"

Phase 2: Fix Implementation (15 min)
Tell Claude: "Implement security fix for increment 0016"

Phase 3: Validation (10 min)
Tell Claude: "Validate security fix for increment 0016"

Phase 4: Emergency Deploy (5 min)
Tell Claude: "Deploy hotfix for increment 0016"

Total estimated time: 35 minutes
```

---

## 最佳实践

**✅ 应该**：
- 首先创建增量开发结构
- 按顺序指导用户完成各个步骤
- 在每个阶段设置质量检查点
- 实时跟踪进度并向用户展示更新情况
- 优雅地处理错误并允许重试
- 允许用户跳过某些可选步骤

**❌ 不应该**：
- 同时启动所有代理（避免系统崩溃）
- 跳过增量开发结构的创建
- 在没有通过质量检查的情况下直接继续执行
- 对代理的错误置之不理
- 假设代理永远不会出错
- 阻止用户进行手动干预

---

## 与 SpecWeave 命令的集成

**编排完成后**：
```bash
# Check status
/sw:status

# Sync to external tools
/sw:sync-progress 0001

# Validate quality
/sw:qa 0001

# Close increment
/sw:done 0001
```

---

**本系统是一个独立运行的工具，可在任何使用 SpecWeave 的项目中使用，只需执行 `specweave init` 即可。**