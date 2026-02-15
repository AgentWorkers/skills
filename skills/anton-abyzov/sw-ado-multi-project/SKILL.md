---
name: ado-multi-project
description: 通过智能的基于内容的映射功能，可以在多个 Azure DevOps 项目中组织和协调规范（specifications）与任务。该功能适用于采用“项目按团队划分”（project-per-team）、“按区域路径划分”（area-path-based）或“按团队划分”（team-based）的 Azure DevOps 架构的场景。同时，它能够处理跨项目之间的协作以及文件夹结构的组织管理工作。
allowed-tools: Read, Write, Edit, Glob
---

# Azure DevOps 多项目管理技能

**用途**：通过智能的映射和文件夹组织方式，管理多个 Azure DevOps 项目中的规范和增量内容。

## 该技能的功能

该技能能够处理复杂的多项目 Azure DevOps 环境，具体包括：

1. **分析增量内容**，以确定其所属项目；
2. 在 `.specweave/docs/internal/specs/` 目录下创建特定于项目的文件夹结构；
3. 根据关键词和上下文将用户故事分配到正确的项目中；
4. 当增量涉及多个团队时，将任务分配到相应的项目中；
5. 维护本地规范与 Azure DevOps 工作项之间的双向同步。

## 支持的架构

### 1. 每个团队对应一个项目（推荐用于微服务架构）

```
Organization: mycompany
├── AuthService (Project)
├── UserService (Project)
├── PaymentService (Project)
└── NotificationService (Project)

Local Structure:
.specweave/docs/internal/specs/
├── AuthService/
├── UserService/
├── PaymentService/
└── NotificationService/
```

### 2. 基于区域路径的架构（单体应用程序）

```
Organization: enterprise
└── ERP (Project)
    ├── Finance (Area Path)
    ├── HR (Area Path)
    ├── Inventory (Area Path)
    └── Sales (Area Path)

Local Structure:
.specweave/docs/internal/specs/ERP/
├── Finance/
├── HR/
├── Inventory/
└── Sales/
```

### 3. 基于团队的架构（小型组织）

```
Organization: startup
└── Platform (Project)
    ├── Alpha Team
    ├── Beta Team
    └── Gamma Team

Local Structure:
.specweave/docs/internal/specs/Platform/
├── AlphaTeam/
├── BetaTeam/
└── GammaTeam/
```

## 智能项目检测

该技能通过分析增量内容来识别正确的项目：

### 检测规则

```typescript
const projectPatterns = {
  'AuthService': {
    keywords: ['authentication', 'login', 'oauth', 'jwt', 'session', 'password'],
    filePatterns: ['auth/', 'login/', 'security/'],
    confidence: 0.0
  },
  'UserService': {
    keywords: ['user', 'profile', 'account', 'registration', 'preferences'],
    filePatterns: ['users/', 'profiles/', 'accounts/'],
    confidence: 0.0
  },
  'PaymentService': {
    keywords: ['payment', 'stripe', 'billing', 'invoice', 'subscription'],
    filePatterns: ['payment/', 'billing/', 'checkout/'],
    confidence: 0.0
  }
};

// Analyze spec content
const spec = readSpec(incrementId);
for (const [project, pattern] of Object.entries(projectPatterns)) {
  pattern.confidence = calculateConfidence(spec, pattern);
}

// Select project with highest confidence
const selectedProject = Object.entries(projectPatterns)
  .sort((a, b) => b[1].confidence - a[1].confidence)[0][0];
```

### 信任度计算

- **关键词匹配**：每个匹配的关键词加 0.2 分；
- **文件模式匹配**：每个匹配的模式加 0.3 分；
- **明确提及项目名称**：项目名称在规范文件中时加 1.0 分；
- **提及团队名称**：团队名称与项目名称匹配时加 0.5 分；
**阈值**：信任度大于 0.7 时自动分配，否则提示用户手动选择项目。

## 使用示例

### 示例 1：单项目增量

**场景**：为 AuthService 功能实现身份验证功能

**规范分析**：
```
Title: "Add OAuth 2.0 authentication"
Keywords found: authentication, oauth, jwt
File patterns: src/auth/oauth-provider.ts
Confidence: AuthService = 0.9 ✅
```

**操作**：
```bash
# Auto-creates folder structure
.specweave/docs/internal/specs/AuthService/
└── spec-001-oauth-authentication.md

# Maps to Azure DevOps
Project: AuthService
Work Item: Epic "OAuth 2.0 Authentication"
```

### 示例 2：多项目增量

**场景**：涉及多个服务的签出流程

**规范分析**：
```
Title: "Implement checkout flow with payment processing"
Keywords found: user, cart, payment, stripe, notification
Confidence:
  - UserService = 0.6
  - PaymentService = 0.8 ✅
  - NotificationService = 0.5
```

**操作**：
```bash
# Creates multi-project structure
.specweave/docs/internal/specs/
├── PaymentService/
│   └── spec-002-checkout-payment.md (primary)
├── UserService/
│   └── spec-002-checkout-user.md (linked)
└── NotificationService/
    └── spec-002-checkout-notifications.md (linked)

# Creates linked work items in Azure DevOps
PaymentService: Epic "Checkout Payment Processing" (primary)
UserService: Feature "User Cart Management" (links to primary)
NotificationService: Feature "Order Notifications" (links to primary)
```

### 示例 3：基于区域路径的架构

**场景**：采用模块化组织的 ERP 系统

**配置**：
```bash
AZURE_DEVOPS_STRATEGY=area-path-based
AZURE_DEVOPS_PROJECT=ERP
AZURE_DEVOPS_AREA_PATHS=Finance,HR,Inventory
```

**规范分析**：
```
Title: "Add payroll calculation engine"
Keywords found: payroll, salary, tax, employee
Area match: HR (confidence = 0.85)
```

**操作**：
```bash
# Creates area-based structure
.specweave/docs/internal/specs/ERP/HR/
└── spec-003-payroll-engine.md

# Maps to Azure DevOps
Project: ERP
Area Path: ERP\HR
Work Item: Epic "Payroll Calculation Engine"
```

## 任务跨项目分配

当一个增量涉及多个项目时，系统会智能地分配任务：

### 输入：UnifiedTasks.md 文件
```markdown
# Tasks for Checkout Flow

- T-001: Create shopping cart API (UserService)
- T-002: Implement Stripe integration (PaymentService)
- T-003: Add order confirmation email (NotificationService)
- T-004: Update user order history (UserService)
- T-005: Process payment webhook (PaymentService)
```

**输出**：各项目的工作项

**UserService**（2 个任务）：
- 任务：创建购物车 API
- 任务：更新用户订单历史

**PaymentService**（2 个任务）：
- 任务：实现 Stripe 集成
- 任务：处理支付 Webhook

**NotificationService**（1 个任务）：
- 任务：发送订单确认邮件

## 文件夹结构创建

该技能会自动创建并维护文件夹结构：

### 增量创建时
```typescript
async function createProjectFolders(increment: Increment) {
  const projects = detectProjects(increment);

  for (const project of projects) {
    const specPath = `.specweave/docs/internal/specs/${project}/`;
    await ensureDir(specPath);

    // Create project-specific spec
    const spec = extractProjectSpec(increment, project);
    await writeSpec(`${specPath}/spec-${increment.number}-${increment.name}.md`, spec);

    // Create README if first spec in project
    if (isFirstSpec(project)) {
      await createProjectReadme(project);
    }
  }
}
```

### 项目 README 模板
```markdown
# {Project} Specifications

## Overview
This folder contains specifications for the {Project} project.

## Architecture
{Brief description of project architecture}

## Team
- Team Lead: {name}
- Developers: {list}

## Specifications
- [spec-001-feature.md](spec-001-feature.md) - {description}

## External Links
- Azure DevOps: https://dev.azure.com/{org}/{project}
- Repository: {git-url}
```

## 同步命令

### 将增量内容同步到项目中
```bash
/sw-ado:sync-increment 0014

# Detects projects from spec
# Creates work items in each project
# Links work items together
```

### 将规范文件同步到项目中
```bash
/sw-ado:sync-spec AuthService/spec-001

# Syncs single spec to specific project
# Updates existing work item or creates new
```

### 同步所有规范文件
```bash
/sw-ado:sync-all

# Syncs all specs across all projects
# Maintains relationships
# Updates bidirectionally
```

## 项目映射配置

### 手动配置（config.json 文件）
```json
{
  "ado": {
    "projectMappings": {
      "auth-.*": "AuthService",
      "user-.*": "UserService",
      "payment-.*": "PaymentService",
      "notification-.*": "NotificationService"
    },
    "defaultProject": "Platform",
    "crossProjectLinking": true
  }
}
```

### 自动检测规则
```typescript
const autoDetectionRules = [
  {
    pattern: /auth|login|oauth|security/i,
    project: "AuthService"
  },
  {
    pattern: /user|profile|account/i,
    project: "UserService"
  },
  {
    pattern: /payment|billing|stripe/i,
    project: "PaymentService"
  }
];
```

## 跨项目协调

### 依赖关系管理

当增量涉及多个项目时，系统会跟踪项目间的依赖关系：

```yaml
# .specweave/increments/0014-checkout-flow/metadata.yml
projects:
  primary: PaymentService
  dependencies:
    - UserService: [T-001, T-004]
    - NotificationService: [T-003]

ado_mappings:
  PaymentService:
    epic: 12345
    work_items: [12346, 12347]
  UserService:
    feature: 12348
    work_items: [12349, 12350]
  NotificationService:
    feature: 12351
    work_items: [12352]
```

### 跨项目查询
```typescript
// Find all work items for an increment across projects
async function getIncrementWorkItems(incrementId: string) {
  const metadata = await readMetadata(incrementId);
  const workItems = [];

  for (const [project, mapping] of Object.entries(metadata.ado_mappings)) {
    const items = await adoClient.getWorkItems(project, mapping.work_items);
    workItems.push(...items);
  }

  return workItems;
}
```

## 最佳实践

### 1. 保持命名一致性

在所有项目中使用统一的命名规范：
```
spec-001-oauth-authentication.md    # Good
spec-001-auth.md                    # Too vague
SPEC_001_OAuth.md                   # Inconsistent format
```

### 2. 明确项目边界

清晰界定各项目之间的边界：
```yaml
AuthService:
  owns: [authentication, authorization, sessions]
  not: [user profiles, user preferences]

UserService:
  owns: [profiles, preferences, user data]
  not: [authentication, passwords]
```

### 3. 链接相关规范文件

链接跨项目的规范文件：
```markdown
# spec-002-checkout-payment.md

Related Specs:
- [User Cart](../UserService/spec-002-checkout-user.md)
- [Notifications](../NotificationService/spec-002-checkout-notifications.md)
```

### 4. 使用项目前缀

在增量文件名前添加主要项目的名称作为前缀：
```bash
/sw:increment "payment-stripe-integration"
/sw:increment "auth-oauth-provider"
/sw:increment "user-profile-redesign"
```

## 错误处理

### 项目未找到
```
❌ Project "AuthService" not found in Azure DevOps

Options:
1. Create project "AuthService"
2. Map to existing project
3. Skip this project

Your choice [1]:
```

### 项目识别不明确
```
⚠️ Cannot determine project for increment 0014

Multiple projects detected:
- UserService (confidence: 0.6)
- PaymentService (confidence: 0.6)

Please select primary project:
1. UserService
2. PaymentService
3. Both (multi-project)

Your choice [3]:
```

### 同步冲突
```
⚠️ Sync conflict detected

Local: spec-001 updated 2 hours ago
Azure DevOps: Work item updated 1 hour ago

Options:
1. Use local version
2. Use Azure DevOps version
3. Merge changes
4. View diff

Your choice [3]:
```

## 与 CI/CD 的集成

### 提交时自动同步
```yaml
# .github/workflows/specweave-sync.yml
on:
  push:
    paths:
      - '.specweave/docs/internal/specs/**'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npx specweave ado-sync-all
        env:
          AZURE_DEVOPS_PAT: ${{ secrets.ADO_PAT }}
```

### 为每个项目配置独立的管道
```yaml
# azure-pipelines.yml
trigger:
  paths:
    include:
      - .specweave/docs/internal/specs/$(System.TeamProject)/**

variables:
  - name: project
    value: $(System.TeamProject)

steps:
  - script: npx specweave ado-sync-project $(project)
```

## 总结

该技能通过以下方式实现高效的多项目管理：

1. ✅ 从规范内容中智能识别项目；
2. ✅ 按项目/区域/团队自动组织文件夹结构；
3. ✅ 在多个项目中分配任务；
4. ✅ 实现跨项目链接和依赖关系管理；
5. ✅ 与 Azure DevOps 工作项保持双向同步。

**结果**：实现无缝的多项目协作，无需任何人工干预！

---

**技能版本**：1.0.0
**首次引入**：SpecWeave v0.17.0
**最后更新时间**：2025-11-11