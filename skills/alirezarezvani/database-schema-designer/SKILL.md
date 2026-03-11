---
name: "database-schema-designer"
description: "数据库模式设计器"
---
# 数据库模式设计工具

**级别：** 高性能  
**类别：** 工程技术  
**领域：** 数据架构 / 后端开发  

---

## 概述  
该工具可根据需求设计关系型数据库模式，并生成相应的迁移脚本、TypeScript/Python类型定义、测试数据、行级安全（RLS）策略以及索引。支持多租户架构、软删除功能、审计追踪、版本控制以及多态关联关系。  

## 核心功能  
- **模式设计**：将业务需求转换为数据库表结构、表间关系及约束条件  
- **迁移脚本生成**：支持使用 Drizzle、Prisma、TypeORM、Alembic 等工具  
- **类型生成**：自动生成 TypeScript 接口或 Python 数据类（如 Pydantic 模型）  
- **行级安全（RLS）**：为多租户应用提供细粒度的访问控制  
- **索引策略**：支持复合索引、部分索引及覆盖索引  
- **测试数据生成**：生成符合实际需求的测试数据  
- **ERD 图生成**：可基于数据库模式自动生成 Mermaid 图表  

---

## 使用场景  
- 设计需要数据库表的新功能  
- 检查现有模式的性能或规范化问题  
- 为现有模式添加多租户支持  
- 从 Prisma 模式生成 TypeScript 类型定义  
- 规划涉及数据结构变更的迁移操作  

---

## 模式设计流程  
### 第 1 步：需求分析 → 实体定义  
根据需求提取相关实体：  
```
User, Project, Task, Label, TaskLabel (junction), TaskAssignment, AuditLog
```  

### 第 2 步：确定表间关系  
```
User 1──* Project         (owner)
Project 1──* Task
Task *──* Label            (via TaskLabel)
Task *──* User            (via TaskAssignment)
User 1──* AuditLog
```  

### 第 3 步：处理通用需求  
- **多租户支持**：在所有租户相关的表中添加 `organization_id` 字段  
- **软删除**：使用 `deleted_at TIMESTAMPTZ` 替代硬删除操作  
- **审计追踪**：记录数据的创建/更新时间  
- **版本控制**：为数据添加 `version` 字段以实现乐观锁机制  

---

## 完整模式示例（任务管理 SaaS 应用）  
详情请参见参考文档：`full-schema-examples.md`  

## 行级安全（RLS）策略  
```sql
-- Enable RLS
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Create app role
CREATE ROLE app_user;

-- Users can only see tasks in their organization's projects
CREATE POLICY tasks_org_isolation ON tasks
  FOR ALL TO app_user
  USING (
    project_id IN (
      SELECT p.id FROM projects p
      JOIN organization_members om ON om.organization_id = p.organization_id
      WHERE om.user_id = current_setting('app.current_user_id')::text
    )
  );

-- Soft delete: never show deleted records
CREATE POLICY tasks_no_deleted ON tasks
  FOR SELECT TO app_user
  USING (deleted_at IS NULL);

-- Only task creator or admin can delete
CREATE POLICY tasks_delete_policy ON tasks
  FOR DELETE TO app_user
  USING (
    created_by_id = current_setting('app.current_user_id')::text
    OR EXISTS (
      SELECT 1 FROM organization_members om
      JOIN projects p ON p.organization_id = om.organization_id
      WHERE p.id = tasks.project_id
        AND om.user_id = current_setting('app.current_user_id')::text
        AND om.role IN ('owner', 'admin')
    )
  );

-- Set user context (call at start of each request)
SELECT set_config('app.current_user_id', $1, true);
```  

---

## 测试数据生成  
```typescript
// db/seed.ts
import { faker } from '@faker-js/faker'
import { db } from './client'
import { organizations, users, projects, tasks } from './schema'
import { createId } from '@paralleldrive/cuid2'
import { hashPassword } from '../src/lib/auth'

async function seed() {
  console.log('Seeding database...')

  // Create org
  const [org] = await db.insert(organizations).values({
    id: createId(),
    name: "acme-corp",
    slug: 'acme',
    plan: 'growth',
  }).returning()

  // Create users
  const adminUser = await db.insert(users).values({
    id: createId(),
    email: 'admin@acme.com',
    name: "alice-admin",
    passwordHash: await hashPassword('password123'),
  }).returning().then(r => r[0])

  // Create projects
  const projectsData = Array.from({ length: 3 }, () => ({
    id: createId(),
    organizationId: org.id,
    ownerId: adminUser.id,
    name: "fakercompanycatchphrase"
    description: faker.lorem.paragraph(),
    status: 'active' as const,
  }))

  const createdProjects = await db.insert(projects).values(projectsData).returning()

  // Create tasks for each project
  for (const project of createdProjects) {
    const tasksData = Array.from({ length: faker.number.int({ min: 5, max: 20 }) }, (_, i) => ({
      id: createId(),
      projectId: project.id,
      title: faker.hacker.phrase(),
      description: faker.lorem.sentences(2),
      status: faker.helpers.arrayElement(['todo', 'in_progress', 'done'] as const),
      priority: faker.helpers.arrayElement(['low', 'medium', 'high'] as const),
      position: i * 1000,
      createdById: adminUser.id,
      updatedById: adminUser.id,
    }))

    await db.insert(tasks).values(tasksData)
  }

  console.log(`✅ Seeded: 1 org, ${projectsData.length} projects, tasks`)
}

seed().catch(console.error).finally(() => process.exit(0))
```  

## ERD 图生成（使用 Mermaid）  
```
erDiagram
    Organization ||--o{ OrganizationMember : has
    Organization ||--o{ Project : owns
    User ||--o{ OrganizationMember : joins
    User ||--o{ Task : "created by"
    Project ||--o{ Task : contains
    Task ||--o{ TaskAssignment : has
    Task ||--o{ TaskLabel : has
    Task ||--o{ Comment : has
    Task ||--o{ Attachment : has
    Label ||--o{ TaskLabel : "applied to"
    User ||--o{ TaskAssignment : assigned

    Organization {
        string id PK
        string name
        string slug
        string plan
    }

    Task {
        string id PK
        string project_id FK
        string title
        string status
        string priority
        timestamp due_date
        timestamp deleted_at
        int version
    }
```  
（具体生成代码请参考相关文档或示例。）  

## 常见问题与注意事项  
- **缺少索引导致的性能问题**：使用 `WHERE deleted_at IS NULL` 时若未建立索引，会导致全表扫描  
- **复合索引缺失**：某些查询（如 `WHERE org_id = ? AND status = ?`）需要复合索引  
- **不适合作为主键的字段**：避免使用电子邮件或字符串作为主键，建议使用 UUID/CUID  
- **非空字段未设置默认值**：在现有表中添加 `NOT NULL` 列时需设置默认值或制定迁移方案  
- **未启用乐观锁**：并发更新可能导致数据冲突，建议添加 `version` 列  
- **RLS 策略未经过测试**：务必使用非管理员角色测试行级安全功能  

---

## 最佳实践  
1. **统一时间戳字段**：所有表都应包含 `created_at` 和 `updated_at` 字段  
2. **使用软删除**：对于需要审计的数据，使用 `deleted_at` 字段代替直接删除操作  
3. **记录审计日志**：对于受监管的应用，需记录数据修改的详细信息  
4. **使用 UUID/CUID 作为主键**：避免使用连续的整数值作为主键  
5. **为外键创建索引**：所有外键字段都应建立索引  
6. **使用部分索引**：对于仅针对已删除数据的查询（如 `WHERE deleted_at IS NULL`），使用部分索引  
7. **依赖数据库层面的访问控制**：行级安全策略应由数据库实现，而非仅依赖应用代码  

---