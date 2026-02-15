---
name: jira-resource-validator
description: 用于验证 JIRA 项目和看板是否存在；如果缺少相关资源，会自动创建这些资源。适用于设置 JIRA 集成、验证 `.env` 配置文件，或排查缺失的项目/看板问题。支持通过 `JIRA_BOARDS_{ProjectKey}` 的模式进行项目级别的看板配置。
allowed-tools: Read, Bash, Write, Edit
---

# Jira资源验证器技能

**用途**：验证并自动创建Jira项目和看板，确保`.env`配置正确。

**自动激活**：在需要设置或验证Jira时触发。

## 该技能的功能

该技能可确保您的`.env`中的Jira配置有效，并且所有资源都存在。它非常“智能”，能够：

1. **验证Jira项目** - 检查`JIRA_Project`是否存在
2. **提示操作** - 选择现有项目或创建新项目
3. **验证Jira看板** - 检查看板是否存在（通过ID或名称）
4. **创建缺失的看板** - 如果提供了看板名称，则自动创建它们
5. **使用ID更新`.env` - 创建后用实际的看板ID替换看板名称

## 该技能何时激活

✅ **在以下情况下自动激活**：
- 首次设置Jira集成时
- 运行`/sw-jira:sync`时资源缺失
- `.env`中的Jira配置无效
- 提到“jira设置”或“jira验证”时

## Jira配置结构

### 必需的`.env`变量

```bash
JIRA_API_TOKEN=your_token_here
JIRA_EMAIL=your_email@company.com
JIRA_DOMAIN=yourcompany.atlassian.net
JIRA_STRATEGY=board-based
JIRA_PROJECT=PROJECTKEY
JIRA_BOARDS=1,2,3  # IDs (if exist) OR names (if creating)
```

### 智能的看板检测（支持多种组合！**

**系统能够处理任何ID和名称的组合：**

**仅使用ID**（验证现有看板）：
```bash
JIRA_BOARDS=1,2,3
```
→ 验证看板1、2、3是否存在

**仅使用名称**（创建新看板）：
```bash
JIRA_BOARDS=Frontend,Backend,Mobile
```
→ 创建3个看板，并用ID更新`.env`：`JIRA_BOARDS=101,102,103`

**混合使用ID和名称**（智能处理！）：
```bash
JIRA_BOARDS=101,102,QA,Dashboard
```
→ 验证101、102是否存在
→ 创建“QA”和“Dashboard”看板
→ 更新`.env`：`JIRA_BOARDS=101,102,103,104`（所有ID！）

**工作原理**：每个条目都会被单独检查：
- 数字（例如，“123”）→ 验证ID是否存在
- 非数字（例如，“QA”）→ 使用该名称创建看板
- 创建后，`.env`会更新为所有看板的ID

### 新功能：按项目配置（高级 - 多个项目×多个看板）

**多个Jira项目及其各自的看板**：

```bash
# Multiple projects with their own boards
JIRA_STRATEGY=project-per-team
JIRA_PROJECTS=BACKEND,FRONTEND,MOBILE

# Per-project boards (hierarchical naming)
JIRA_BOARDS_BACKEND=123,456         # Sprint + Kanban (IDs)
JIRA_BOARDS_FRONTEND=Sprint,Bug     # Create these boards
JIRA_BOARDS_MOBILE=789,012,345      # iOS + Android + Release (IDs)
```
→ 验证3个项目存在：BACKEND、FRONTEND、MOBILE
→ 按项目验证/创建看板：
  - BACKEND：验证看板123、456是否存在
  - FRONTEND：创建“Sprint”和“Bug”看板，并用ID更新`.env`
  - MOBILE：验证看板789、012、345是否存在

**命名规则**：`{PROVIDER}_{RESOURCE_TYPE}_{PROJECT_KEY}`

**每个项目混合使用ID和名称**：
```bash
JIRA_BOARDS_BACKEND=123,NewBoard,456
```
→ 验证123、456是否存在
→ 创建“NewBoard”看板
→ 更新`.env`：`JIRA_BOARDS_BACKEND=123,789,456`（所有ID！）

## 验证流程

### 第一步：项目验证

**检查项目是否存在**：
```bash
# API call to Jira
GET /rest/api/3/project/PROJECTKEY
```

**如果项目存在**：
```
✅ Project "PROJECTKEY" exists
   ID: 10001
   Name: My Project
```

**如果项目不存在**：
```
⚠️  Project "PROJECTKEY" not found

What would you like to do?
1. Select an existing project
2. Create a new project
3. Cancel

Your choice [1]:
```

**选项1：选择现有项目**：
```
Available projects:
1. PROJ1 - Project One
2. PROJ2 - Project Two
3. PROJ3 - Project Three

Select a project [1]:

✅ Updated .env: JIRA_PROJECT=PROJ1
```

**选项2：创建新项目**：
```
Enter project name: My New Project

📦 Creating Jira project: PROJECTKEY (My New Project)...
✅ Project created: PROJECTKEY (ID: 10005)
```

### 第二步：看板验证（智能检测每个看板）

**场景A：所有看板ID都是数字**：
```bash
JIRA_BOARDS=1,2,3
```

**验证**：
```
Checking boards: 1,2,3...
  ✅ Board 1: Frontend Board (exists)
  ✅ Board 2: Backend Board (exists)
  ⚠️  Board 3: Not found

⚠️  Issues found: 1 board(s)
```

**场景B：所有看板名称都是非数字**：
```bash
JIRA_BOARDS=Frontend,Backend,Mobile
```

**自动创建**：
```
Checking boards: Frontend,Backend,Mobile...
  📦 Creating board: Frontend...
  ✅ Created: Frontend (ID: 101)
  📦 Creating board: Backend...
  ✅ Created: Backend (ID: 102)
  📦 Creating board: Mobile...
  ✅ Created: Mobile (ID: 103)

📝 Updating .env with board IDs...
✅ Updated JIRA_BOARDS: 101,102,103

✅ All boards validated/created successfully
```

**场景C：混合使用ID和名称**（非常智能！）：
```bash
JIRA_BOARDS=101,102,QA,Dashboard
```

**智能处理**：
```
Checking boards: 101,102,QA,Dashboard...
  ✅ Board 101: Frontend Board (exists)
  ✅ Board 102: Backend Board (exists)
  📦 Creating board: QA...
  ✅ Created: QA (ID: 103)
  📦 Creating board: Dashboard...
  ✅ Created: Dashboard (ID: 104)

📝 Updating .env with board IDs...
✅ Updated JIRA_BOARDS: 101,102,103,104

✅ All boards validated/created successfully
```

## 使用示例

### 示例1：新Jira设置

**场景**：新项目，尚未创建任何Jira资源

**操作**：运行`/sw-jira:sync`

**结果**：
```bash
🔍 Validating Jira configuration...

Checking project: MINIDOOM...
⚠️  Project "MINIDOOM" not found

What would you like to do?
1. Select an existing project
2. Create a new project
3. Cancel

Your choice [2]: 2

Enter project name: Mini DOOM Tournament

📦 Creating Jira project: MINIDOOM (Mini DOOM Tournament)...
✅ Project created: MINIDOOM (ID: 10005)

Checking boards: Frontend,Backend,Mobile...
📦 Creating boards from names...

Creating board: Frontend in project MINIDOOM...
✅ Board created: Frontend (ID: 101)

Creating board: Backend in project MINIDOOM...
✅ Board created: Backend (ID: 102)

Creating board: Mobile in project MINIDOOM...
✅ Board created: Mobile (ID: 103)

✅ Updated .env: JIRA_BOARDS=101,102,103

🎉 Jira configuration complete! All resources ready.
```

**结果**：`.env`现在包含正确的项目和看板ID

### 示例2：选择现有项目

**场景**：项目已经在Jira中存在

**操作**：运行验证

**结果**：
```bash
🔍 Validating Jira configuration...

Checking project: PROJ...
⚠️  Project "PROJ" not found

What would you like to do?
1. Select an existing project
2. Create a new project
3. Cancel

Your choice [1]: 1

Available projects:
1. FRONTEND - Frontend Team
2. BACKEND - Backend Team
3. MOBILE - Mobile Team

Select a project [1]: 2

✅ Updated .env: JIRA_PROJECT=BACKEND
✅ Project "BACKEND" exists

Checking boards: 45,46...
✅ All boards exist
```

### 示例3：混合使用看板ID（部分存在，部分不存在）

**场景**：某些看板ID无效

**操作**：运行验证

**结果**：
```bash
🔍 Validating Jira configuration...

Checking project: PROJECTKEY...
✅ Project "PROJECTKEY" exists

Checking boards: 1,2,999...

Board 1: ✅ Exists (Frontend Board)
Board 2: ✅ Exists (Backend Board)
Board 999: ❌ Not found

⚠️  Boards not found: 999

Available boards in project PROJECTKEY:
1. Frontend Board (ID: 1)
2. Backend Board (ID: 2)
3. QA Board (ID: 3)
4. DevOps Board (ID: 4)

Would you like to:
1. Remove invalid board (999) from configuration
2. Replace with correct board ID
3. Create new board

Your choice [2]: 2

Enter correct board ID or name: 3

✅ Updated .env: JIRA_BOARDS=1,2,3
```

## CLI命令

**手动验证**：
```bash
# From TypeScript
npx tsx src/utils/external-resource-validator.ts

# Or via skill activation
"Can you validate my Jira configuration?"
```

**验证输出**：
```typescript
{
  valid: true,
  project: {
    exists: true,
    key: 'PROJECTKEY',
    id: '10001',
    name: 'My Project'
  },
  boards: {
    valid: true,
    existing: [1, 2, 3],
    missing: [],
    created: []
  },
  envUpdated: false
}
```

## 智能的看板创建逻辑（智能检测每个看板）

### 检测算法

```typescript
// Parse JIRA_BOARDS from .env
const boardsConfig = "101,102,QA,Dashboard"; // Mixed!
const boardEntries = boardsConfig.split(',').map(b => b.trim());
const finalBoardIds = [];

// Check EACH board individually
for (const entry of boardEntries) {
  const isNumeric = /^\d+$/.test(entry);

  if (isNumeric) {
    // Entry is a board ID - validate it exists
    const boardId = parseInt(entry);
    const board = await checkBoard(boardId);
    if (board) {
      console.log(`✅ Board ${boardId}: ${board.name} (exists)`);
      finalBoardIds.push(boardId);
    } else {
      console.error(`⚠️  Board ${boardId}: Not found`);
    }
  } else {
    // Entry is a board name - create it
    console.log(`📦 Creating board: ${entry}...`);
    const board = await createBoard(entry, projectKey);
    console.log(`✅ Created: ${entry} (ID: ${board.id})`);
    finalBoardIds.push(board.id);
  }
}

// Update .env if any boards were created
if (createdBoardIds.length > 0) {
  updateEnv({ JIRA_BOARDS: finalBoardIds.join(',') });
}
```

**关键改进**：逐个看板进行检测，而不是全有或全无！
- `JIRA_BOARDS=1,2,3` → 验证所有ID是否存在
- `JIRA_BOARDS=A,B,C` → 创建所有看板
- `JIRA_BOARDS=1,2,C` → 验证1和2的存在，并创建C（混合情况！）

### 看板创建API

**Jira REST API**（v3）：
```bash
POST /rest/api/3/board
Content-Type: application/json

{
  "name": "Frontend Board",
  "type": "scrum",
  "filterId": 10000,  # Filter for project issues
  "location": {
    "type": "project",
    "projectKeyOrId": "PROJECTKEY"  # CRITICAL: Associates board with project
  }
}

Response:
{
  "id": 101,
  "name": "Frontend Board",
  "type": "scrum"
}
```

**重要提示**：`location`字段是**必需的**，用于将看板与项目关联。如果没有这个字段，Jira会创建看板，但会使其处于分离状态，需要通过UI手动连接。

**创建看板的过滤**（必需）：
```bash
POST /rest/api/3/filter
Content-Type: application/json

{
  "name": "PROJECTKEY Issues",
  "jql": "project = PROJECTKEY"
}

Response:
{
  "id": 10000
}
```

## 配置示例

### 示例1：仅使用名称（创建看板）

**配置前（`.env`）**：
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=Frontend,Backend,QA,DevOps
```

**验证后**：
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=101,102,103,104
```

**发生的情况**：
- 检测到非数字值（名称）
- 在Jira中创建4个看板
- 用实际的看板ID更新`.env`

### 示例2：仅使用ID（验证现有项目）

**配置前（`.env`）**：
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=1,2,3
```

**验证后**：
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=1,2,3
```

**发生的情况**：
- 检测到数字值（ID）
- 验证所有看板是否存在
- 无需任何更改

### 示例3：混合使用ID和名称（非常智能！）

**配置前（`.env`）**：
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=101,102,QA,Dashboard
```

**验证后**：
```bash
JIRA_PROJECT=PROJ
JIRA_BOARDS=101,102,103,104
```

**发生的情况**：
- 验证101和102看板存在
- 创建“QA”看板（ID为103）
- 创建“Dashboard”看板（ID为104）
- 用所有看板ID更新`.env`
- **这是关键功能**：您可以混合使用现有的ID和新看板名称！

### 示例4：修复无效的项目

**配置前（`.env`）**：
```bash
JIRA_PROJECT=NONEXISTENT
JIRA_BOARDS=1,2
```

**验证后（用户选择了现有项目）**：
```bash
JIRA_PROJECT=EXISTINGPROJ
JIRA_BOARDS=1,2
```

**发生的情况**：
- 未找到不存在的项目
- 用户从列表中选择了现有项目
- 用正确的项目键更新`.env`

## 错误处理

### 错误1：无效凭据

**症状**：API调用失败，返回401 Unauthorized错误

**解决方法**：
```
❌ Jira API authentication failed

Please check:
1. JIRA_API_TOKEN is correct
2. JIRA_EMAIL matches your Jira account
3. JIRA_DOMAIN is correct (yourcompany.atlassian.net)

Generate new token at:
https://id.atlassian.com/manage-profile/security/api-tokens
```

### 错误2：权限不足

**症状**：无法创建项目/看板（返回403 Forbidden错误）

**解决方法**：
```
❌ Insufficient permissions to create resources

You need:
- Project Creator permission (for projects)
- Board Creator permission (for boards)

Contact your Jira administrator to request permissions.
```

### 错误3：项目键已被占用

**症状**：项目创建失败（键已存在）

**解决方法**：
```
❌ Project key "PROJ" already exists

Options:
1. Use a different project key
2. Select the existing project
3. Cancel

Your choice [2]:
```

### 错误4：网络/API错误

**症状**：API调用超时或失败

**解决方法**：
```
❌ Jira API error: Request timeout

Please check:
1. Internet connection
2. Jira domain is correct
3. Jira is not down (check status.atlassian.com)

Retry? [Y/n]:
```

## 与SpecWeave工作流的集成

### 自动验证

当使用`/sw-jira:sync`时，验证会自动运行：

```bash
/sw-jira:sync 0014

# Internally calls:
1. validateJiraResources()
2. Fix missing project/boards
3. Proceed with sync
```

### 手动验证

可以独立运行验证：

```bash
# Via skill
"Validate my Jira configuration"

# Via TypeScript
npx tsx src/utils/external-resource-validator.ts

# Via CLI (future)
specweave validate-jira
```

## 最佳实践

✅ **在初始设置时使用看板名称**：
```bash
JIRA_BOARDS=Sprint-1,Sprint-2,Backlog
```
- 系统会自动创建看板
- 用ID更新`.env`
- 一次性设置完成后，后续使用ID

✅ **创建后使用看板ID**：
```bash
JIRA_BOARDS=101,102,103
```
- 验证更快（无需创建）
- 更可靠（ID不会更改）

✅ **将`.env`文件放入版本控制**（使用git忽略的标记）：
```bash
# Commit project/board structure
JIRA_PROJECT=PROJ
JIRA_BOARDS=101,102,103

# Don't commit sensitive data
JIRA_API_TOKEN=<redacted>
JIRA_EMAIL=<redacted>
```

✅ **记录看板映射**（在README文件中）：
```markdown
## Jira Boards

- Board 101: Frontend Team
- Board 102: Backend Team
- Board 103: QA Team
```

## 总结

该技能通过以下方式确保您的Jira配置始终有效：

1. ✅ **验证项目** - 检查项目是否存在，并提示选择或创建
2. ✅ **验证看板** - 检查看板是否存在（通过ID）或创建它们（通过名称）
3. ✅ **自动更新`.env` - 创建后用ID替换看板名称
4. ✅ **提供清晰的错误信息** - 为所有失败情况提供可操作的指导
5. ✅ **非阻塞式设计** - 具有手动回退机制，确保系统能够优雅地处理问题

**结果**：完全无需手动设置Jira——系统会处理所有操作！

---

**技能版本**：1.0.0
**引入版本**：SpecWeave v0.9.5
**最后更新时间**：2025-11-09