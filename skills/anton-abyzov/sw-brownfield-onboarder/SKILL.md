---
name: brownfield-onboarder
description: 通过将现有的 CLAUDE.md 备份文件合并到 SpecWeave 结构中，智能地整合现有的旧项目（brownfield projects）。适用于在已有 CLAUDE.md 文件的项目中安装 SpecWeave、合并相关文档或导入项目信息的情况。该功能能够将内容分发到适当的文件夹中，而不会导致主 CLAUDE.md 文件变得过于臃肿。
---

# Brownfield Onboarder - 智能合并 CLAUDE.md 文档

**目的**：智能地将现有的 CLAUDE.md 备份文件合并到 SpecWeave 的文档结构中，同时避免使主 CLAUDE.md 文件变得过于臃肿。

**使用场景**：在将 SpecWeave 安装到已存在 CLAUDE.md 文件的项目中之后使用。

**设计理念**：保持 CLAUDE.md 作为简洁的指南，将详细内容分布到相应的 SpecWeave 文件夹中。

**支持模式**：支持快速启动（增量式）和全面整合（一次性）两种方式 🆕

---

## 两种合并模式 🆕

Brownfield Onboarder 的工作方式会根据所选择的文档路径而有所不同：

### 快速启动模式（增量式）
**设计理念**：仅合并必要的内容，将详细文档留待后续逐步添加。

**立即合并的内容**：
- ✅ 核心架构概述（高级别）
- ✅ 技术栈和基础设施
- ✅ 关键模式（认证、支付、安全）
- ✅ 团队规范和工作流程
- ✅ 项目总结和领域背景

**推迟合并的内容**（在修改相关代码时再生成）：
- ⏸️ 详细的业务规则
- ⏸️ 模块特定的文档
- ⏸️ API 级别的文档
- ⏸️ 代码示例

**结果**：初期合并工作量小（30-60分钟），详细文档逐步增加。

### 全面整合模式（一次性）
**设计理念**：一次性合并所有内容，确保信息完整。

**合并的内容**：
- ✅ 所有架构文档
- ✅ 所有业务规则
- ✅ 所有模块特定的文档
- ✅ 所有 API 文档
- ✅ 所有规范和模式
- ✅ 所有代码示例

**结果**：一次性完成合并（1-3小时），所有信息立即可用。

### 模式选择

**自动检测**：
```typescript
// Settings auto-detected
const mode = config.brownfield?.mode || 'auto';

if (mode === 'auto') {
  // Use complexity from brownfield-analyzer
  const complexity = await readComplexityAssessment();
  mode = complexity.recommendedPath === 'Quick Start' ? 'incremental' : 'comprehensive';
}
```

**用户可手动选择**：
```bash
# Force Quick Start mode
brownfield-onboarder --mode quick-start

# Force Comprehensive mode
brownfield-onboarder --mode comprehensive
```

---

## 面临的问题

在将 SpecWeave 安装到现有项目中时：
1. 项目中已有包含项目特定信息的 `CLAUDE.md` 文件。
2. SpecWeave 会安装自己的 `CLAUDE.md` 文件作为开发指南。
3. 旧的 `CLAUDE.md` 文件会被备份到 `.claude/backups/CLAUDE-backup-{timestamp}.md` 目录中。
4. 需要智能地合并项目特定内容，同时避免使 SpecWeave 的 `CLAUDE.md` 文件变得臃肿。

---

## 解决方案：智能内容分发

**避免 CLAUDE.md 文件变得臃肿**，而是将内容分发到相应的文件夹中：

```
Project-specific content → SpecWeave folders:

# Internal Documentation (strategic, team-only)
Architecture details    → .specweave/docs/internal/architecture/existing-system.md
Technology stack        → .specweave/docs/internal/architecture/tech-stack.md
Business rules          → .specweave/docs/internal/strategy/business-rules.md
Team workflows          → .specweave/docs/internal/processes/team-workflows.md
Deployment process      → .specweave/docs/internal/processes/deployment.md
Domain knowledge        → .specweave/increments/{####-name}/docs/domain/{domain}.md

# Public Documentation (user-facing, can be published)
Project conventions     → .specweave/docs/public/guides/project-conventions.md
API conventions         → .specweave/docs/public/guides/api-conventions.md
Code style              → .specweave/docs/public/guides/code-style.md
```

**仅添加到 CLAUDE.md 中的内容**：简短的项目总结（最多 1-2 段落）

---

## 激活流程

**触发条件**：用户运行 `specweave merge-docs` 命令或请求“合并我的旧 CLAUDE.md”。

**自动检测**：
1. 检查是否存在 `.claude/backups/CLAUDE-backup-*.md` 备份文件。
2. 如果有多个备份文件，使用最新的一个。
3. 如果没有备份文件，向用户提示并优雅地退出程序。

---

## 分析流程

### 第一步：解析备份文件 CLAUDE.md

**提取相关内容**：
```typescript
interface ParsedCLAUDEmd {
  projectName: string;
  projectDescription: string;
  techStack: TechStack;
  architecture: ArchitectureSection[];
  conventions: Convention[];
  workflows: Workflow[];
  domainKnowledge: DomainSection[];
  teamGuidelines: TeamGuideline[];
  deploymentProcess: DeploymentSection[];
  apiDesign: APISection[];
  businessRules: BusinessRule[];
  codeExamples: CodeExample[];
  customInstructions: Instruction[];
}
```

**识别相关章节的关键词**：
- **技术栈**：`technology`、`framework`、`database`、`infrastructure`、`stack`、`tools`
- **架构**：`architecture`、`system design`、`components`、`services`、`microservices`
- **规范**：`naming convention`、`code style`、`pattern`、`standard`、`guideline`
- **工作流程**：`workflow`、`process`、`pipeline`、`deployment flow`、`release process`
- **领域**：特定领域的术语（如 `patient`、`booking`、`payment`、`order`
- **业务规则**：`business rule`、`validation`、`policy`、`constraint`、`requirement`
- **API 设计**：`API`、`endpoint`、`REST`、`GraphQL`、`authentication`、`authorization`
- **部署**：`deploy`、`CI/CD`、`environment`、`production`、`staging`

### 第二步：根据模式对内容进行分类 🆕

**对于每个章节，判断**：
1. **内容是通用的还是特定于项目的？**
   - 通用内容：常见的编程建议、通用最佳实践
   - 项目特定内容：领域知识、团队规范、项目架构
2. **与 SpecWeave 的 CLAUDE.md 有重复吗？**
   - 与 SpecWeave 的 CLAUDE.md 对比，如果相似度超过 80%，则跳过；如果相似度低于 80%，则提取独特内容
3. **内容是必要的还是详细的？** 🆕
   - 必要内容：核心架构、关键模式、技术栈、团队工作流程
   - 详细内容：模块特定规则、API 文档、代码示例
4. **根据模式决定合并方式** 🆕
   - **快速启动模式**：仅合并必要内容
   - **全面整合模式**：合并所有内容
5. **确定目标文件夹**：
   - 确定这些内容应放置到的 SpecWeave 文件夹
   - 详见“内容分发规则”

**内容分类表** 🆕：

| 内容类型 | 是否必要 | 快速启动模式 | 全面整合模式 |
|--------------|-----------|-------------------|---------------------|
| 核心架构 | ✅ 是 | 立即合并 | 立即合并 |
| 技术栈 | ✅ 是 | 立即合并 | 立即合并 |
| 关键模式（认证、支付） | ✅ 是 | 立即合并 | 立即合并 |
| 团队规范 | ✅ 是 | 立即合并 | 立即合并 |
| 项目总结 | ✅ 是 | 立即合并 | 立即合并 |
| 详细业务规则 | ❌ 否 | **推迟到后续合并** | 立即合并 |
| 模块文档 | ❌ 否 | **推迟到后续合并** | 立即合并 |
| API 级文档 | ❌ 否 | **推迟到后续合并** | 立即合并 |
| 代码示例 | ❌ 否 | **推迟到后续合并** | 立即合并 |

**示例（快速启动模式）**：
```
Analyzing CLAUDE.md backup (Quick Start mode)...

Found sections:
  ✅ Core Architecture (merge now)
  ✅ Tech Stack (merge now)
  ✅ Auth Pattern (merge now - critical)
  ⏸️ Payment Business Rules (defer - extract when working on payments)
  ⏸️ User Module API (defer - extract when modifying user code)
  ⏸️ Code Examples (defer - extract as needed)

Merging 3 sections immediately, deferring 3 for incremental extraction.
```

### 第三步：内容分发规则

#### 规则 1：领域知识 → `specifications` 文件夹

**判断依据**：业务概念、实体、领域术语

**示例**：
```markdown
# Old CLAUDE.md
## Domain Model

Our platform manages **patient appointments** with **healthcare providers**.
Key entities:
- Patient (demographics, insurance, medical history)
- Provider (specialties, availability, credentials)
- Appointment (time slot, status, notes)
- Clinic (location, services, staff)

Business rules:
- Appointments must be 15-60 minutes
- Patients can cancel up to 24 hours before
- Providers can override cancellation policy
```

**目标文件夹**：`specifications/modules/appointments/domain-model.md`

**CLAUDE.md 的处理方式**：无需添加内容（在 CLAUDE.md 中添加链接指向 `specifications` 文件夹）

---

#### 规则 2：架构 → `.specweave/docs/architecture/` 文件夹

**判断依据**：系统设计、组件描述、数据流

**示例**：
```markdown
# Old CLAUDE.md
## System Architecture

We use a microservices architecture:
- API Gateway (Kong) - routing, authentication
- Booking Service (Node.js) - appointment management
- Notification Service (Python) - email/SMS
- Payment Service (Node.js) - Stripe integration
- Database (PostgreSQL) - shared across services
```

**目标文件夹**：`.specweave/docs/internal/architecture/existing-system.md`

**CLAUDE.md 的处理方式**：
```markdown
## Project-Specific Architecture

See [Existing System Architecture](.specweave/docs/internal/architecture/existing-system.md) for complete microservices architecture.
```

---

#### 规则 3：规范 → `.specweave/docs/guides/` 文件夹

**判断依据**：命名规范、代码风格、模式

**示例**：
```markdown
# Old CLAUDE.md
## Naming Conventions

- API endpoints: `/api/v1/{resource}/{action}` (kebab-case)
- Database tables: `{domain}_{entity}` (snake_case)
- TypeScript interfaces: `I{Name}` prefix (PascalCase)
- React components: `{Name}Component.tsx` suffix
```

**目标文件夹**：`.specweave/docs/public/guides/project-conventions.md`

**CLAUDE.md 的处理方式**：无需添加内容（这些是标准规范，无需重复）

---

#### 规则 4：工作流程 → `.specweave/docs/guides/` 文件夹

**判断依据**：部署流程、CI/CD、发布流程

**示例**：
```markdown
# Old CLAUDE.md
## Deployment Process

1. Create feature branch from `main`
2. Implement feature with tests
3. Create PR (requires 2 approvals)
4. Merge → auto-deploy to staging
5. Manual approval → deploy to production
6. Rollback via GitHub Actions if needed
```

**目标文件夹**：`.specweave/docs/internal/processes/deployment.md`

**CLAUDE.md 的处理方式**：
```markdown
## Deployment

See [Deployment Guide](.specweave/docs/internal/processes/deployment.md).
```

---

#### 规则 5：业务规则 → `specifications/modules/` 文件夹

**判断依据**：验证规则、政策、约束条件

**示例**：
```markdown
# Old CLAUDE.md
## Business Rules

### Appointment Booking
- Patients can book up to 3 months in advance
- Maximum 5 active appointments per patient
- Same-day appointments require $50 deposit
- Insurance verification required before booking
```

**目标文件夹**：`.specweave/docs/internal/strategy/appointments/business-rules.md`

**CLAUDE.md 的处理方式**：无需添加内容（详细规则存储在 `specifications` 文件中）

---

#### 规则 6：技术栈 → `.specweave/docs/architecture/` 文件夹

**判断依据**：技术、框架、工具

**示例**：
```markdown
# Old CLAUDE.md
## Tech Stack

- Frontend: Next.js 14, React, Tailwind CSS
- Backend: Node.js 20, Express, TypeScript
- Database: PostgreSQL 16, Prisma ORM
- Cache: Redis
- Queue: BullMQ
- Infrastructure: Hetzner Cloud, Terraform
- Monitoring: Grafana, Prometheus
```

**目标文件夹**：`.specweave/docs/internal/architecture/tech-stack.md`

**CLAUDE.md 的处理方式**：
```markdown
## Tech Stack

Next.js 14 + Node.js 20 + PostgreSQL 16 + Hetzner Cloud

See [Tech Stack Details](.specweave/docs/internal/architecture/tech-stack.md).
```

---

#### 规则 7：API 设计 → `.specweave/docs/guides/` 文件夹

**判断依据**：API 规范、认证机制、错误处理

**示例**：
```markdown
# Old CLAUDE.md
## API Design

All APIs follow REST conventions:
- Authentication: JWT in Authorization header
- Errors: Standard structure { error, message, details }
- Pagination: page, limit query params
- Filtering: field[operator]=value
- Versioning: /api/v1, /api/v2
```

**目标文件夹**：`.specweave/docs/public/guides/api-conventions.md`

**CLAUDE.md 的处理方式**：无需添加内容（这些内容已在指南中）

---

#### 规则 8：代码示例 **（是否保留或删除）**

**判断依据**：代码片段、示例实现

**处理方式**：
- 如果是通用模式（标准代码示例），则删除（SpecWeave 的 CLAUDE.md 中已有相关内容）
- 如果是项目特定模式，則提取到指南中

**示例**：
```markdown
# Old CLAUDE.md - Generic React pattern
function UserList() {
  const [users, setUsers] = useState([]);
  // ... standard React code
}
```（通用 React 模式，无需保留）
**示例**：
```markdown
# Old CLAUDE.md - Custom authentication pattern
// Our custom auth hook (wraps Supabase)
function useCustomAuth() {
  const { session } = useSupabase();
  const { roles } = useRoleProvider();
  return { user: session?.user, hasRole: (role) => roles.includes(role) };
}
```（项目特定模式，提取到 `.specweave/docs/public/guides/authentication.md`）

---

### 第四步：更新 CLAUDE.md 文件

**仅在 SpecWeave 的 CLAUDE.md 中添加** 简短的项目总结：

**添加的内容**：最多 1-2 段落

---

## 智能合并规则

**避免文件臃肿**

**切勿将以下内容添加到 CLAUDE.md 中**：
- 通用编程建议（SpecWeave 的 CLAUDE.md 中已有）
- 详细的代码示例（放入指南文件）
- 长篇的架构描述（放入架构文档中）
- 业务规则细节（放入规范文件中）
- API 文档（放入指南文件中）

**仅在 CLAUDE.md 中添加**：
- 1-2 句的项目描述
- 领域/行业背景信息
- 链接到详细文档的链接

**避免重复**

**在创建新文件之前，请检查是否存在类似内容**：
```typescript
// Check if domain model already exists
if (exists("specifications/modules/appointments/domain-model.md")) {
  // Compare content
  existingContent = read("specifications/modules/appointments/domain-model.md");
  newContent = extractDomainModel(backupCLAUDEmd);

  if (similarity(existingContent, newContent) > 0.8) {
    // Skip, already documented
    skip();
  } else {
    // Merge unique content
    mergedContent = merge(existingContent, newContent);
    write("specifications/modules/appointments/domain-model.md", mergedContent);
  }
}
```

**确保内容准确性**

**在提取内容时**：
- 不要改写技术细节
- 保持术语的一致性
- 保持代码示例的原始格式
- 保持格式的准确性（表格、列表、代码块等）

**用户确认**

**在生成新文件之前，请向用户展示内容**：
```
I found the following project-specific content in your backup CLAUDE.md:

📦 Domain Model (Healthcare Appointments)
   → .specweave/increments/####-name/docs/domain/appointments/domain-model.md

🏗️ Microservices Architecture
   → .specweave/docs/internal/architecture/existing-system.md

🛠️ Tech Stack (Next.js + Node.js + PostgreSQL)
   → .specweave/docs/internal/architecture/tech-stack.md

📋 Business Rules (Booking policies)
   → .specweave/docs/internal/strategy/appointments/business-rules.md

🔧 Project Conventions (Naming, code style)
   → .specweave/docs/public/guides/project-conventions.md

🚀 Deployment Process (CI/CD workflow)
   → .specweave/docs/internal/processes/deployment.md

📝 CLAUDE.md Update
   → Add 12-line project summary with links

Total files to create: 6
Total lines added to CLAUDE.md: 12

Proceed with merge? (y/n)
```

---

## 合并结果

**合并完成后，生成特定模式的报告**：

### 快速启动模式报告 🆕

```markdown
# CLAUDE.md Merge Report - Quick Start Mode

**Date**: 2025-10-26
**Backup File**: .claude/backups/CLAUDE-backup-20251026-143022.md
**Merge Status**: ✅ Complete (Essential content only)
**Mode**: Quick Start (Incremental Documentation)

---

## Files Created (Essential Only)

1. ✅ `.specweave/docs/internal/architecture/core-architecture.md` (120 lines)
2. ✅ `.specweave/docs/internal/architecture/tech-stack.md` (80 lines)
3. ✅ `.specweave/docs/internal/architecture/critical-patterns.md` (100 lines)
4. ✅ `.specweave/docs/public/guides/project-conventions.md` (90 lines)
5. ✅ `.specweave/docs/internal/processes/deployment.md` (70 lines)

**Total**: 5 files, 460 lines (essential content)

---

## CLAUDE.md Updated

**Added**: 10 lines (project summary + links)

**Location**: Lines 850-860

---

## Content Distribution (Quick Start)

| Content Type | Lines | Status | Destination |
|--------------|-------|--------|-------------|
| Core Architecture | 120 | ✅ Merged | .specweave/docs/internal/architecture/ |
| Tech Stack | 80 | ✅ Merged | .specweave/docs/internal/architecture/ |
| Critical Patterns | 100 | ✅ Merged | .specweave/docs/internal/architecture/ |
| Conventions | 90 | ✅ Merged | .specweave/docs/public/guides/ |
| Deployment | 70 | ✅ Merged | .specweave/docs/internal/processes/ |
| **CLAUDE.md** | **10** | ✅ **Updated** | **Root** |
| **Subtotal Merged** | **470** | | |
| | | | |
| Domain Model (detailed) | 450 | ⏸️ Deferred | Extract when working on appointments |
| Business Rules (detailed) | 280 | ⏸️ Deferred | Extract when working on payments |
| User Module API | 150 | ⏸️ Deferred | Extract when modifying user code |
| Code Examples | 200 | ⏸️ Deferred | Extract as needed per increment |
| **Subtotal Deferred** | **1,080** | | **Document incrementally** |

**Result**: 470 lines merged now, 1,080 lines to extract per increment

**Benefit**: Start in 30-60 minutes, not 1-3 hours

---

## Deferred Content (Extract Per Increment)

The following content remains in the backup and will be extracted when you work on related features:

### 📦 Domain Documentation
- `appointments/domain-model.md` (450 lines)
  → Extract when creating increment for appointments feature

### 📋 Business Rules
- `payments/business-rules.md` (280 lines)
  → Extract when creating increment for payment modifications

### 🔌 API Documentation
- `users/api-endpoints.md` (150 lines)
  → Extract when creating increment for user service changes

### 💻 Code Examples
- Various code snippets (200 lines)
  → Extract as needed

**How to extract later**:
```bash
# 开始更新 appointments 模块的文档时：
# 使用命令：
# `inc "Refactor appointment booking"
# 在 spec.md 中引用：
# “查看备份文件：.claude/backups/CLAUDE-backup-*.md (appointments 部分)”
# 或者请求：
# “从 CLAUDE.md 备份中提取 appointments 相关文档”

```

---

## Skipped Content

- Generic React patterns (25 lines) - Already covered in SpecWeave
- Standard git workflow (15 lines) - Common knowledge
- TypeScript basics (40 lines) - Not project-specific

**Total skipped**: 80 lines (generic content)

---

## Next Steps

1. ✅ Review merged essential docs (30 min)
2. ✅ Start first increment (immediate)
3. ⏸️ Extract detailed docs as you work on features

**Time saved**: ~2 hours (vs comprehensive upfront)

---
```

### 全面整合模式报告

```markdown
# CLAUDE.md Merge Report - Comprehensive Mode

**Date**: 2025-10-26
**Backup File**: .claude/backups/CLAUDE-backup-20251026-143022.md
**Merge Status**: ✅ Complete (All content)
**Mode**: Comprehensive (Upfront Documentation)

---

## Files Created

1. ✅ `.specweave/increments/####-name/docs/domain/appointments/domain-model.md` (450 lines)
2. ✅ `.specweave/docs/internal/architecture/existing-system.md` (320 lines)
3. ✅ `.specweave/docs/internal/architecture/tech-stack.md` (180 lines)
4. ✅ `.specweave/docs/internal/strategy/appointments/business-rules.md` (280 lines)
5. ✅ `.specweave/docs/public/guides/project-conventions.md` (200 lines)
6. ✅ `.specweave/docs/internal/processes/deployment.md` (150 lines)

**Total**: 6 files, 1,580 lines

---

## CLAUDE.md Updated

**Added**: 12 lines (project summary + links)

**Location**: Lines 850-862 (after "Living Documentation Principles")

---

## Content Distribution

| Content Type | Lines | Destination |
|--------------|-------|-------------|
| Domain Model | 450 | .specweave/increments/####-name/docs/domain/ |
| Architecture | 320 | .specweave/docs/internal/architecture/ |
| Tech Stack | 180 | .specweave/docs/internal/architecture/ |
| Business Rules | 280 | .specweave/docs/internal/strategy/ |
| Conventions | 200 | .specweave/docs/public/guides/ |
| Deployment | 150 | .specweave/docs/internal/processes/ |
| **CLAUDE.md** | **12** | **Root** |

**Result**: 99.2% of content distributed to appropriate folders, not bloating CLAUDE.md

---

## Skipped Content

- Generic React patterns (25 lines) - Already covered in SpecWeave
- Standard git workflow (15 lines) - Common knowledge
- TypeScript basics (40 lines) - Not project-specific

**Total skipped**: 80 lines (generic content)

---

## Next Steps

1. ✅ Review generated files in `.specweave/docs/internal/` and `.specweave/docs/public/`
2. ✅ SpecWeave uses auto-detection
3. ✅ Run `npm run docs:dev` to preview documentation
4. ✅ Create features from specifications: `specweave plan-feature {name}`

---

## Backup Preserved

Original backup remains at:
`.claude/backups/CLAUDE-backup-20251026-143022.md`

You can reference it anytime.

---

**Merge Complete! 🎉**

Your project-specific knowledge is now integrated into SpecWeave's structure.
```

---

## 使用示例

### 用户请求

```
User: "I installed SpecWeave and it backed up my CLAUDE.md. Can you merge the important parts?"
```

### 用户响应

```
I'll analyze your backup CLAUDE.md and intelligently merge project-specific content.

🔍 Analyzing: .claude/backups/CLAUDE-backup-20251026-143022.md

Found:
- Project: Healthcare Appointment Booking Platform
- Domain model: Patients, Providers, Appointments, Clinics
- Architecture: Microservices (4 services)
- Tech stack: Next.js + Node.js + PostgreSQL
- Business rules: Booking policies, cancellation rules
- Conventions: Naming, API design
- Deployment: CI/CD workflow

📦 Content Distribution Plan:

1. Domain Model → specifications/modules/appointments/domain-model.md
2. Architecture → .specweave/docs/architecture/existing-system.md
3. Tech Stack → .specweave/docs/architecture/tech-stack.md
4. Business Rules → specifications/modules/appointments/business-rules.md
5. Conventions → .specweave/docs/guides/project-conventions.md
6. Deployment → .specweave/docs/guides/deployment.md

CLAUDE.md: Add 12-line summary with links (no bloat!)

Total: 6 files, ~1,580 lines
CLAUDE.md additions: 12 lines (99.2% distributed to folders)

Proceed with merge? (y/n)
```

### 用户批准后

```
✅ Merge complete!

Created:
1. .specweave/increments/####-name/docs/domain/appointments/domain-model.md
2. .specweave/docs/internal/architecture/existing-system.md
3. .specweave/docs/internal/architecture/tech-stack.md
4. .specweave/docs/internal/strategy/appointments/business-rules.md
5. .specweave/docs/public/guides/project-conventions.md
6. .specweave/docs/internal/processes/deployment.md

Updated:
- CLAUDE.md (added 12-line project summary)

Report saved: ai-logs/reports/CLAUDE-MERGE-REPORT-20251026.md

Your project knowledge is now integrated! 🎉

Next: Review files and run `npm run docs:dev` to preview.
```

---

## 工具使用流程

**扫描备份文件**：
```typescript
const backups = glob(".claude/backups/CLAUDE-backup-*.md");
const latestBackup = backups.sort().reverse()[0];  // Most recent
```

**解析文件内容**：
```typescript
const content = read(latestBackup);
const sections = parseSections(content);  // Split by headers
const classified = classifyContent(sections);  // Domain, Architecture, etc.
```

**避免重复**：
```typescript
if (exists(targetPath)) {
  const existing = read(targetPath);
  if (similarity(existing, newContent) > 0.8) {
    skip();  // Already documented
  }
}
```

---

**相关文档**：
- [BROWNFIELD-INTEGRATION-STRATEGERY.md](../../docs/internal/delivery/BROWNFIELD-INTEGRATION-STRATEGERY.md)
- [brownfield-analyzer skill](../brownfield-analyzer/SKILL.md)
- [CLAUDE.md](../../CLAUDE.md)