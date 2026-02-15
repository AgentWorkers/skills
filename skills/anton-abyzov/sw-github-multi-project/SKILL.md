---
name: github-multi-project
description: 擅长整理技术规范，并将任务分配到多个 GitHub 仓库中，适用于单仓库（monorepo）、多仓库（polyrepo）以及父仓库（parent repo）架构。适用于需要在多个仓库之间管理技术规范、协调跨仓库的工作，或将任务分配给不同的团队或仓库的情况。
---

# GitHub多项目管理技能

这是一种专门用于管理跨多个GitHub仓库的SpecWeave项目的专业技能。

## 核心能力

### 1. 规范组织
- 将规范文件组织在`.specweave/docs/internal/projects/{project-id}/`结构中
- 将规范文件的更新映射到具体的项目/仓库
- 保持各仓库之间的可追溯性
- 处理跨项目依赖关系

### 2. 任务分解
当一个SpecWeave更新涉及多个仓库时：
- 分析`tasks.md`文件中的任务
- 确定每个任务属于哪个仓库
- 为每个仓库创建相应的任务列表
- 保持跨仓库的协调性

### 3. 仓库架构

#### 单个仓库
```
my-app/
├── .specweave/
│   └── docs/internal/projects/default/
└── src/
```

#### 多个仓库（Polyrepo）
```
my-app-frontend/
├── .git
└── src/

my-app-backend/
├── .git
└── src/

my-app-shared/
├── .git
└── src/
```

#### 父仓库模式（多仓库项目推荐）
```
my-app-parent/              # Parent repo with .specweave
├── .specweave/
│   └── docs/internal/projects/
│       ├── frontend/
│       ├── backend/
│       └── shared/
└── services/               # Implementation repos
    ├── frontend/
    ├── backend/
    └── shared/
```

#### 单一仓库（Monorepo）
```
my-app/
├── .specweave/
│   └── docs/internal/projects/
│       ├── frontend/
│       ├── backend/
│       └── shared/
└── packages/
    ├── frontend/
    ├── backend/
    └── shared/
```

## 任务分解示例

### 示例1：电子商务平台
**更新内容**：添加购物车功能

**按仓库划分的任务**：

**前端（my-app-frontend）**：
- T-001：创建CartItem组件
- T-002：实现购物车状态管理
- T-003：添加包含添加/删除按钮的购物车用户界面

**后端（my-app-backend）**：
- T-004：创建购物车数据库模式
- T-005：实现购物车API接口
- T-006：添加购物车验证逻辑

**共享组件（my-app-shared）**：
- T-007：定义购物车的TypeScript类型
- T-008：创建购物车辅助函数

### 示例2：微服务架构
**更新内容**：实现用户通知功能

**按服务划分的任务**：

**用户服务**：
- T-001：在用户资料中添加通知偏好设置
- T-002：创建偏好设置API接口

**通知服务**：
- T-003：实现通知队列
- T-004：创建邮件发送器
- T-005：创建推送通知发送器

**网关服务**：
- T-006：添加通知路由
- T-007：实现速率限制

## 命令

### 分析任务分布
```typescript
// Analyze which tasks belong to which repository
function analyzeTaskDistribution(tasks: Task[]): Map<string, Task[]> {
  const distribution = new Map();

  for (const task of tasks) {
    const repo = detectRepository(task);
    if (!distribution.has(repo)) {
      distribution.set(repo, []);
    }
    distribution.get(repo).push(task);
  }

  return distribution;
}
```

### 为每个仓库创建问题（Issues）
```typescript
// Create GitHub issues in each repository
async function createRepoSpecificIssues(
  increment: Increment,
  distribution: Map<string, Task[]>
) {
  for (const [repo, tasks] of distribution) {
    const issue = await createGitHubIssue({
      repo,
      title: `[${increment.id}] ${increment.name} - ${repo}`,
      body: formatTasksAsChecklist(tasks),
      labels: ['specweave', 'increment', repo]
    });

    console.log(`Created issue #${issue.number} in ${repo}`);
  }
}
```

## 最佳实践

### 1. 父仓库模式
**多仓库项目推荐使用**：
- 在父仓库中设置一个中央的`.specweave/`文件夹
- 将所有文档同步到父仓库（确保信息的一致性）
- 实现仓库保持整洁
- 更适合企业或多团队项目

### 2. 任务命名规范
```
T-{repo}-{number}: {description}
T-FE-001: Create user profile component
T-BE-001: Implement user API
T-SHARED-001: Define user types
```

### 3. 跨仓库依赖关系
明确标注依赖关系：
```
T-FE-002: Consume user API
  Dependencies: T-BE-001 (must complete first)
```

### 4. 规范组织
```
.specweave/docs/internal/projects/
├── frontend/
│   └── specs/
│       ├── spec-001-user-interface.md
│       └── spec-002-cart-ui.md
├── backend/
│   └── specs/
│       ├── spec-001-api-design.md
│       └── spec-002-database.md
└── shared/
    └── specs/
        └── spec-001-types.md
```

## 与GitHub项目的集成

### 多仓库的GitHub项目
创建一个涵盖多个仓库的GitHub项目：
1. 在组织级别创建项目
2. 从所有仓库中添加问题（Issues）
3. 使用项目看板进行跨仓库协调
4. 跟踪整个项目的更新进度

### 仓库级别的项目
每个仓库都可以有自己的项目：
- 前端项目：处理与用户界面相关的任务
- 后端项目：处理API相关的任务
- 共享项目：处理通用任务

## 自动化
### 集成GitHub Actions
```yaml
# .github/workflows/specweave-sync.yml
name: SpecWeave Multi-Repo Sync

on:
  workflow_dispatch:
  schedule:
    - cron: '0 */6 * * *' # Every 6 hours

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Sync to repositories
        run: |
          # Sync tasks to frontend repo
          gh issue create --repo myorg/frontend ...

          # Sync tasks to backend repo
          gh issue create --repo myorg/backend ...
```

## 错误处理

### 常见问题
1. **仓库未找到**：确保仓库存在，并且令牌具有访问权限
2. **任务不明确**：使用清晰的命名来指定目标仓库
3. **跨仓库冲突**：以父仓库作为信息来源的统一标准
4. **权限错误**：令牌需要具有对所有仓库的访问权限

## 相关技能
- github-sync：基本的GitHub同步工具
- github-issue-tracker：用于任务级别的问题跟踪工具
- specweave:multi-project-spec-mapper：智能的规范文件分解工具