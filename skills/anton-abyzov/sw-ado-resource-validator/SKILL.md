---
name: ado-resource-validator
description: 该工具用于验证 Azure DevOps 项目、区域路径（area paths）以及团队的存在性；如果发现缺失的资源，会自动创建这些资源。适用于设置 ADO（Azure DevOps）集成、配置 `.env` 变量或排查项目相关错误时。支持按项目、按区域路径或按团队进行资源管理的策略。
allowed-tools: Read, Bash, Write, Edit
---

# Azure DevOps 资源验证器技能

**功能**：验证并自动创建 Azure DevOps 项目及资源，确保 `.env` 配置正确。

**自动激活条件**：在需要设置或验证 Azure DevOps 时触发。

## 该技能的作用

该技能用于确保您的 `.env` 文件中的 Azure DevOps 配置有效，并且所有资源都存在。它具备以下智能功能：

1. **验证 Azure DevOps 项目**：检查项目是否存在（每个团队对应一个项目）。
2. **提示操作**：允许用户选择现有项目或创建新项目。
3. **验证区域路径**：检查区域路径是否存在（针对基于区域路径的策略）。
4. **创建缺失的区域路径**：如果区域路径缺失，会自动创建。
5. **验证团队**：检查团队是否存在（针对基于团队的策略）。
6. **使用正确的值更新 `.env` 文件**：确保配置有效。

## 该技能的激活时机

✅ **在以下情况下会自动激活**：
- 首次设置 Azure DevOps 集成时。
- 运行 `/sw-ado:sync` 时发现资源缺失。
- `.env` 文件中的 Azure DevOps 配置无效。
- 提到“ado 设置”或“azure devops 验证”等关键词时。

## Azure DevOps 配置结构

### 必需的 `.env` 变量

```bash
AZURE_DEVOPS_PAT=your_token_here
AZURE_DEVOPS_ORG=yourorganization
AZURE_DEVOPS_STRATEGY=project-per-team  # or area-path-based, team-based
```

### 根据策略不同的变量

**策略 1：每个团队一个项目**（多个项目）  
```bash
AZURE_DEVOPS_STRATEGY=project-per-team
AZURE_DEVOPS_PROJECTS=WebApp,MobileApp,Platform
```  
→ 验证 WebApp、MobileApp 和 Platform 项目是否存在。

**策略 2：基于区域路径**（一个项目，多个区域路径）  
```bash
AZURE_DEVOPS_STRATEGY=area-path-based
AZURE_DEVOPS_PROJECT=MainProduct
AZURE_DEVOPS_AREA_PATHS=Frontend,Backend,Mobile
```  
→ 验证 MainProduct 项目是否存在；  
→ 如果区域路径缺失，会自动创建：MainProduct\Frontend、MainProduct-backend、MainProduct\Mobile。

**策略 3：基于团队**（一个项目，多个团队）  
```bash
AZURE_DEVOPS_STRATEGY=team-based
AZURE_DEVOPS_PROJECT=MainProduct
AZURE_DEVOPS_TEAMS=Alpha Team,Beta Team,Gamma Team
```  
→ 验证 MainProduct 项目是否存在；  
→ 如果团队缺失，会自动创建：Alpha Team、Beta Team、Gamma Team。

**新功能：项目级配置**（高级版本 - 多个项目 × 多种资源）  
```bash
# Multiple projects with their own area paths and teams
AZURE_DEVOPS_STRATEGY=project-per-team
AZURE_DEVOPS_PROJECTS=Backend,Frontend,Mobile

# Per-project area paths (hierarchical naming)
AZURE_DEVOPS_AREA_PATHS_Backend=API,Database,Cache
AZURE_DEVOPS_AREA_PATHS_Frontend=Web,Admin,Public
AZURE_DEVOPS_AREA_PATHS_Mobile=iOS,Android,Shared

# Per-project teams (optional)
AZURE_DEVOPS_TEAMS_Backend=Alpha,Beta
AZURE_DEVOPS_TEAMS_Frontend=Gamma
```  
→ 验证是否存在以下三个项目：Backend、Frontend、Mobile；  
→ 为每个项目创建相应的区域路径：  
  - Backend\API、Backend\Database、Backend\Cache  
  - Frontend\Web、Frontend\Admin、Frontend\Public  
  - Mobile\iOS、Mobile\Android、Mobile\Shared；  
→ 为每个项目创建相应的团队：  
  - Backend: Alpha、Beta  
  - Frontend: Gamma。

**命名规则**：`{PROVIDER}_{RESOURCE_TYPE}_{PROJECT_NAME}`

## 验证流程

### 第一步：策略检测

**读取 `.env` 文件并确定策略**：
```bash
AZURE_DEVOPS_STRATEGY=project-per-team
```

**验证结果**：
```
🔍 Detected strategy: Project-per-team
   Projects to validate: WebApp, MobileApp, Platform
```

### 第二步：项目验证（每个团队一个项目）

**检查项目是否存在**：
```bash
# API calls to Azure DevOps
GET https://dev.azure.com/{org}/_apis/projects/WebApp
GET https://dev.azure.com/{org}/_apis/projects/MobileApp
GET https://dev.azure.com/{org}/_apis/projects/Platform
```

**如果所有项目都存在**：
```
✅ All projects validated:
   • WebApp (ID: abcd1234)
   • MobileApp (ID: efgh5678)
   • Platform (ID: ijkl9012)
```

**如果某些项目缺失**：
```
⚠️ Projects not found:
   ✅ WebApp (exists)
   ❌ MobileApp (not found)
   ❌ Platform (not found)

What would you like to do?
1. Create missing projects
2. Select existing projects
3. Fix project names manually
4. Cancel

Your choice [1]:
```

**选项 1：创建缺失的项目**：
```
📦 Creating Azure DevOps projects...

Creating project: MobileApp...
✅ Project created: MobileApp (ID: mnop3456)

Creating project: Platform...
✅ Project created: Platform (ID: qrst7890)

✅ All projects now exist!
```

**选项 2：选择现有项目**：
```
Available projects in organization:
1. WebApp
2. ApiGateway
3. AuthService
4. NotificationService
5. DataPipeline

Select projects (comma-separated numbers) [2,3]:

✅ Updated .env: AZURE_DEVOPS_PROJECTS=WebApp,ApiGateway,AuthService
```

### 第三步：区域路径验证（基于区域路径的策略）

**场景**：一个项目包含多个区域路径  
```bash
AZURE_DEVOPS_STRATEGY=area-path-based
AZURE_DEVOPS_PROJECT=MainProduct
AZURE_DEVOPS_AREA_PATHS=Frontend,Backend,Mobile,QA
```

**验证过程**：
```
Checking project: MainProduct...
✅ Project "MainProduct" exists

Checking area paths...
  ✅ MainProduct\Frontend (exists)
  ✅ MainProduct\Backend (exists)
  ⚠️ MainProduct\Mobile (not found)
  ⚠️ MainProduct\QA (not found)

📦 Creating missing area paths...
✅ Created: MainProduct\Mobile
✅ Created: MainProduct\QA

✅ All area paths validated/created successfully
```

### 第四步：团队验证（基于团队的策略）

**场景**：一个项目包含多个团队  
```bash
AZURE_DEVOPS_STRATEGY=team-based
AZURE_DEVOPS_PROJECT=MainProduct
AZURE_DEVOPS_TEAMS=Alpha Team,Beta Team,Gamma Team
```

**验证过程**：
```
Checking project: MainProduct...
✅ Project "MainProduct" exists

Checking teams...
  ✅ Alpha Team (exists)
  ⚠️ Beta Team (not found)
  ⚠️ Gamma Team (not found)

📦 Creating missing teams...
✅ Created: Beta Team
✅ Created: Gamma Team

✅ All teams validated/created successfully
```

## 使用示例

### 示例 1：新的 Azure DevOps 设置（每个团队一个项目）

**场景**：为新团队设置多个项目  

**操作**：运行 `/sw-ado:sync`  

**执行结果**：
```bash
🔍 Validating Azure DevOps configuration...

Strategy: Project-per-team
Checking projects: WebApp, MobileApp, Platform...

⚠️ Projects not found:
   • WebApp
   • MobileApp
   • Platform

What would you like to do?
1. Create new projects
2. Select existing projects
3. Cancel

Your choice [1]: 1

📦 Creating Azure DevOps projects...

Creating project: WebApp
  Description: Web application frontend
  Process template: Agile
✅ Created: WebApp (ID: proj-001)

Creating project: MobileApp
  Description: Mobile application
  Process template: Agile
✅ Created: MobileApp (ID: proj-002)

Creating project: Platform
  Description: Backend platform services
  Process template: Agile
✅ Created: Platform (ID: proj-003)

🎉 Azure DevOps configuration complete! All resources ready.
```

### 示例 2：从单项目切换到多项目**

**场景**：当前使用单个项目，希望将其拆分为多个项目  

**当前的 `.env` 文件**：
```bash
AZURE_DEVOPS_PROJECT=MainProduct
```

**新的 `.env` 文件**：
```bash
AZURE_DEVOPS_STRATEGY=project-per-team
AZURE_DEVOPS_PROJECTS=MainProduct-Frontend,MainProduct-Backend,MainProduct-Mobile
```

**执行结果**：
```bash
🔍 Detected strategy change: team-based → project-per-team

Validating new projects...
  ✅ MainProduct-Frontend (exists from previous split)
  ⚠️ MainProduct-Backend (not found)
  ⚠️ MainProduct-Mobile (not found)

Would you like to:
1. Create missing projects
2. Keep single project with area paths instead
3. Cancel

Your choice [1]: 1

📦 Creating projects...
✅ Created: MainProduct-Backend
✅ Created: MainProduct-Mobile

💡 Tip: You can now organize specs by project:
   .specweave/docs/internal/specs/MainProduct-Frontend/
   .specweave/docs/internal/specs/MainProduct-Backend/
   .specweave/docs/internal/specs/MainProduct-Mobile/
```

### 示例 3：设置区域路径**

**场景**：大型单体应用程序，采用基于区域路径的组织结构  

**操作**：为团队设置区域路径  

**执行结果**：
```bash
🔍 Validating Azure DevOps configuration...

Strategy: Area-path-based
Project: EnterpriseApp
Area Paths: Core, UserManagement, Billing, Reports, Analytics

Checking project: EnterpriseApp...
✅ Project exists

Checking area paths...
  ✅ EnterpriseApp\Core
  ✅ EnterpriseApp\UserManagement
  ⚠️ EnterpriseApp\Billing (not found)
  ⚠️ EnterpriseApp\Reports (not found)
  ⚠️ EnterpriseApp\Analytics (not found)

📦 Creating area paths...

Creating: EnterpriseApp\Billing
✅ Area path created with default team

Creating: EnterpriseApp\Reports
✅ Area path created with default team

Creating: EnterpriseApp\Analytics
✅ Area path created with default team

✅ All area paths ready!

Work items will be organized by area:
  • Billing features → EnterpriseApp\Billing
  • Report features → EnterpriseApp\Reports
  • Analytics features → EnterpriseApp\Analytics
```

## 实现细节

**代码位置**：`src/utils/external-resource-validator.ts`

**核心类**：
```typescript
// Main validator class
export class AzureDevOpsResourceValidator {
  private pat: string;
  private organization: string;
  private envPath: string;

  constructor(envPath: string = '.env') {
    this.envPath = envPath;
    const env = this.loadEnv();
    this.pat = env.AZURE_DEVOPS_PAT || '';
    this.organization = env.AZURE_DEVOPS_ORG || '';
  }

  // Main validation entry point
  async validate(): Promise<AzureDevOpsValidationResult> {
    const env = this.loadEnv();
    const strategy = env.AZURE_DEVOPS_STRATEGY || 'project-per-team';

    // Validate based on strategy
    if (strategy === 'project-per-team') {
      return this.validateMultipleProjects(projectNames);
    } else if (strategy === 'area-path-based') {
      return this.validateAreaPaths(projectName, areaPaths);
    } else if (strategy === 'team-based') {
      return this.validateTeams(projectName, teams);
    }
  }
}

// Public API function
export async function validateAzureDevOpsResources(
  envPath: string = '.env'
): Promise<AzureDevOpsValidationResult> {
  const validator = new AzureDevOpsResourceValidator(envPath);
  return validator.validate();
}
```

**主要实现特性**：
1. **异步项目创建**（特定于 Azure DevOps）：  
   ```typescript
   // ADO creates projects asynchronously - need to poll for completion
   async createProject(name: string): Promise<AzureDevOpsProject> {
     const result = await this.callAzureDevOpsApi('projects?api-version=7.0', 'POST', body);

     // Wait for project to be fully created (ADO async behavior)
     await this.waitForProjectCreation(result.id);

     return { id: result.id, name, description };
   }

   // Poll until project is in 'wellFormed' state
   private async waitForProjectCreation(projectId: string): Promise<void> {
     const maxAttempts = 30; // 30 seconds max wait
     for (let i = 0; i < maxAttempts; i++) {
       const project = await this.getProject(projectId);
       if (project.state === 'wellFormed') {
         return; // Project is ready!
       }
       await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second
     }
     throw new Error('Project creation timeout');
   }
   ```

2. **交互式提示**（当资源缺失时）：  
   ```typescript
   const { action } = await inquirer.prompt([
     {
       type: 'select',
       name: 'action',
       message: `Project "${projectName}" not found. What would you like to do?`,
       choices: [
         { name: 'Create new project', value: 'create' },
         { name: 'Select existing project', value: 'select' },
         { name: 'Skip this project', value: 'skip' },
         { name: 'Cancel', value: 'cancel' }
       ]
     }
   ]);
   ```

3. **自动更新 `.env` 文件**：  
   ```typescript
   // After creating projects, update .env
   updateEnv(key: string, value: string): void {
     const envContent = fs.readFileSync(this.envPath, 'utf-8');
     const updated = envContent.replace(
       new RegExp(`^${key}=.*$`, 'm'),
       `${key}=${value}`
     );
     fs.writeFileSync(this.envPath, updated);
   }
   ```

## 命令行接口（CLI）

**自动验证**（在设置过程中）：
```bash
# Runs automatically during specweave init
npx specweave init

# Also runs automatically before sync
/sw-ado:sync 0014
```

**手动验证**：
```bash
# Via skill activation
"Can you validate my Azure DevOps configuration?"

# Via TypeScript directly
npx tsx -e "import { validateAzureDevOpsResources } from './dist/utils/external-resource-validator.js'; await validateAzureDevOpsResources();"

# Via CLI (future command - planned)
specweave validate-ado
```

**验证结果输出**：
```typescript
interface AzureDevOpsValidationResult {
  valid: boolean;
  strategy: 'project-per-team' | 'area-path-based' | 'team-based';
  projects: Array<{
    name: string;
    id: string;
    exists: boolean;
  }>;
  created: string[];      // Names of newly created resources
  envUpdated: boolean;    // Whether .env was modified
}

// Example output:
{
  valid: true,
  strategy: 'project-per-team',
  projects: [
    { name: 'WebApp', id: 'proj-001', exists: true },
    { name: 'MobileApp', id: 'proj-002', exists: true, created: true },
    { name: 'Platform', id: 'proj-003', exists: true, created: true }
  ],
  created: ['MobileApp', 'Platform'],
  envUpdated: false
}
```

## 智能项目检测

**根据现有工作项自动推荐项目组织结构**：
```typescript
// Analyze existing work items
const workItems = await analyzeWorkItems(org, project);

// Detect patterns
const patterns = {
  byArea: workItems.groupBy('areaPath'),      // Area-based organization
  byTeam: workItems.groupBy('assignedTeam'),  // Team-based organization
  byType: workItems.groupBy('workItemType')   // Type-based organization
};

// Suggest strategy
if (patterns.byArea.length > 3) {
  console.log('💡 Detected area-based organization');
  console.log('   Suggested strategy: area-path-based');
} else if (patterns.byTeam.length > 2) {
  console.log('💡 Detected team-based organization');
  console.log('   Suggested strategy: team-based or project-per-team');
}
```

## 项目创建 API

**Azure DevOps REST API**（v7.0）：

### 创建项目  
```bash
POST https://dev.azure.com/{org}/_apis/projects?api-version=7.0
Content-Type: application/json
Authorization: Basic {base64(":PAT")}

{
  "name": "MobileApp",
  "description": "Mobile application project",
  "capabilities": {
    "versioncontrol": {
      "sourceControlType": "Git"
    },
    "processTemplate": {
      "templateTypeId": "adcc42ab-9882-485e-a3ed-7678f01f66bc"  # Agile
    }
  }
}

Response:
{
  "id": "proj-002",
  "name": "MobileApp",
  "state": "wellFormed"
}
```

### 创建区域路径  
```bash
POST https://dev.azure.com/{org}/{project}/_apis/wit/classificationnodes/areas?api-version=7.0
Content-Type: application/json

{
  "name": "Frontend",
  "attributes": {
    "startDate": null,
    "finishDate": null
  }
}

Response:
{
  "id": 123,
  "name": "Frontend",
  "path": "\\MainProduct\\Area\\Frontend"
}
```

### 创建团队  
```bash
POST https://dev.azure.com/{org}/_apis/projects/{projectId}/teams?api-version=7.0
Content-Type: application/json

{
  "name": "Alpha Team",
  "description": "Alpha development team"
}

Response:
{
  "id": "team-001",
  "name": "Alpha Team",
  "projectName": "MainProduct"
}
```

## 配置示例

### 示例 1：微服务架构（每个团队一个项目）

**配置前的 `.env` 文件**：
```bash
AZURE_DEVOPS_ORG=mycompany
AZURE_DEVOPS_PAT=xxx
```

**验证后的 `.env` 文件**：
```bash
AZURE_DEVOPS_ORG=mycompany
AZURE_DEVOPS_PAT=xxx
AZURE_DEVOPS_STRATEGY=project-per-team
AZURE_DEVOPS_PROJECTS=AuthService,UserService,PaymentService,NotificationService
```

**创建的文件夹结构**：
```
.specweave/docs/internal/specs/
├── AuthService/
│   └── spec-001-oauth-implementation.md
├── UserService/
│   └── spec-001-user-management.md
├── PaymentService/
│   └── spec-001-stripe-integration.md
└── NotificationService/
    └── spec-001-email-notifications.md
```

### 示例 2：单体应用程序（基于区域路径）

**配置前的 `.env` 文件**：
```bash
AZURE_DEVOPS_PROJECT=ERP
```

**验证后的 `.env` 文件**：
```bash
AZURE_DEVOPS_ORG=enterprise
AZURE_DEVOPS_PAT=xxx
AZURE_DEVOPS_STRATEGY=area-path-based
AZURE_DEVOPS_PROJECT=ERP
AZURE_DEVOPS_AREA_PATHS=Finance,HR,Inventory,Sales,Reports
```

**工作项组织结构**：
```
ERP
├── Finance/          → Finance module features
├── HR/               → HR module features
├── Inventory/        → Inventory management
├── Sales/            → Sales module features
└── Reports/          → Reporting features
```

### 示例 3：平台团队（基于团队的策略）

**配置前的 `.env` 文件**：
```bash
AZURE_DEVOPS_PROJECT=Platform
```

**验证后的 `.env` 文件**：
```bash
AZURE_DEVOPS_ORG=techcorp
AZURE_DEVOPS_PAT=xxx
AZURE_DEVOPS_STRATEGY=team-based
AZURE_DEVOPS_PROJECT=Platform
AZURE_DEVOPS_TEAMS=Infrastructure,Security,Data,DevOps
```

**团队职责分配**：
- Infrastructure Team：负责云资源、网络配置  
- Security Team：负责身份验证、合规性、审计  
- Data Team：负责数据库、数据分析、机器学习  
- DevOps Team：负责持续集成/持续交付（CI/CD）、监控、工具开发  

## 错误处理

### 错误 1：无效的凭据  
**症状**：API 调用失败，返回 401 Unauthorized 错误。  
**解决方案**：
```
❌ Azure DevOps API authentication failed

Please check:
1. AZURE_DEVOPS_PAT is correct
2. Token has not expired
3. AZURE_DEVOPS_ORG is correct

Generate new token at:
https://dev.azure.com/{org}/_usersSettings/tokens
```

### 错误 2：权限不足  
**症状**：无法创建项目（返回 403 Forbidden 错误）。  
**解决方案**：
```
❌ Insufficient permissions to create projects

You need:
- Project Collection Administrator role (for creating projects)
- Project Administrator role (for area paths and teams)

Contact your Azure DevOps administrator to request permissions.
```

### 错误 3：项目名称冲突  
**症状**：项目创建失败（因为名称已存在）。  
**解决方案**：
```
❌ Project name "WebApp" already exists

Options:
1. Use a different project name
2. Select the existing project
3. Add a suffix (e.g., WebApp-v2)

Your choice [2]:
```

### 错误 4：组织限制  
**症状**：无法创建更多项目。  
**解决方案**：
```
❌ Organization project limit reached (250 projects)

Consider:
1. Using area-path-based strategy (one project)
2. Archiving old projects
3. Upgrading organization plan

Contact Azure DevOps support for limit increases.
```

## 与 SpecWeave 工作流的集成

**自动验证**：  
在使用 `/sw-ado:sync` 时，验证会自动执行：  
```bash
/sw-ado:sync 0014

# Internally calls:
1. validateAzureDevOpsResources()
2. Fix missing projects/area paths/teams
3. Create folder structure for specs
4. Proceed with sync
```

**手动验证**：  
也可以单独运行验证命令：  
```bash
# Via skill
"Validate my Azure DevOps configuration"

# Via TypeScript
npx tsx src/utils/external-resource-validator.ts --provider=ado

# Via CLI (future)
specweave validate-ado
```

## 最佳实践

✅ **选择合适的策略**：
- **每个团队一个项目**：适合自主管理的团队或微服务架构。  
- **基于区域路径**：适合单体应用程序或共享代码库的情况。  
- **基于团队**：适合小型组织或结构简单的场景。  

✅ **使用描述性强的名称**：  
为各个项目和文件夹命名，以便于理解。  

✅ **在 README 文件中记录项目映射关系**：  
确保其他开发人员了解项目之间的依赖关系。  

✅ **将 `.env` 文件放入版本控制**（使用 `git ignored` 标签）：  
避免版本控制冲突。  

## 文件夹组织结构

根据所选策略，该技能会创建相应的文件夹结构：

### 每个团队一个项目的文件夹结构  
```
.specweave/docs/internal/specs/
├── WebApp/
│   ├── spec-001-user-interface.md
│   └── spec-002-responsive-design.md
├── MobileApp/
│   ├── spec-001-ios-features.md
│   └── spec-002-android-features.md
└── Platform/
    ├── spec-001-api-design.md
    └── spec-002-database-schema.md
```

### 基于区域路径的文件夹结构  
```
.specweave/docs/internal/specs/MainProduct/
├── Frontend/
│   └── spec-001-ui-components.md
├── Backend/
│   └── spec-001-api-endpoints.md
└── Mobile/
    └── spec-001-mobile-sync.md
```

### 基于团队的文件夹结构  
```
.specweave/docs/internal/specs/MainProduct/
├── AlphaTeam/
│   └── spec-001-feature-a.md
├── BetaTeam/
│   └── spec-001-feature-b.md
└── GammaTeam/
    └── spec-001-feature-c.md
```

## 与 JIRA 的主要区别

| 方面 | Azure DevOps | JIRA |
|--------|-------------|------|
| **项目创建** | 异步（需要轮询） | 同步（立即完成） |
| **创建时间** | 5-30 秒 | <1 秒 |
| **状态跟踪** | 需要轮询 `state` 字段（如 “wellFormed”） | 无需轮询 |
| **API 复杂度** | 更高（异步处理） | 更低（同步操作） |
| **看板创建** | 与项目同时创建 | 需要单独调用 API |
| **流程模板** | 是必需的（适用于敏捷、Scrum、CMMI 等方法） | 不适用 |

**异步处理的重要性**：

当创建 Azure DevOps 项目时，API 会立即返回 `state: 'new'`，但项目实际上尚未可用。验证器会每秒轮询一次（最多尝试 30 次），直到项目状态变为 `state: 'wellFormed'**：

```typescript
// Create project (returns immediately)
const project = await createProject('MobileApp'); // state: 'new'

// Poll until ready
await waitForProjectCreation(project.id); // Polls until state: 'wellFormed'

// Now safe to use!
console.log('✅ Project ready for work items');
```

**对用户体验的影响**：
- JIRA：项目创建后立即显示 “✅ 项目已创建”。  
- Azure DevOps：会显示 “📦 正在创建项目... ⏳ 等待 Azure DevOps 完成设置... ✅ 项目已准备好！”（可能需要 5-30 秒）。  

## 总结

该技能通过以下方式确保您的 Azure DevOps 配置始终有效：  
1. **验证项目是否存在**，并提示用户选择或创建项目。  
2. **支持多种策略**（每个团队一个项目、基于区域路径、基于团队）。  
3. **自动创建项目、区域路径和团队**（采用异步处理方式）。  
4. **根据项目结构创建相应的文件夹**。  
5. **提供清晰的错误信息**，指导用户如何解决配置问题。  
6. **适应 Azure DevOps 的异步特性**，通过轮询来处理项目创建过程。  

**效果**：完全自动化 Azure DevOps 的设置过程——系统会处理所有细节，包括异步的项目创建操作！

---

**技能版本**：1.1.0  
**引入版本**：SpecWeave v0.17.0  
**最后更新时间**：2025-11-11  
**版本 1.1.0 的主要变更**：增加了实现细节、异步项目创建的处理方式以及与 JIRA 的对比信息。