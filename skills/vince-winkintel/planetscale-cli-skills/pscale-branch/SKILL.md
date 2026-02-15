---
name: pscale-branch
description: 创建、删除、推送（Promote）、比较差异（Diff）以及管理 PlanetScale 数据库分支。这些操作适用于为数据库模式变更创建开发分支、查看模式差异、将分支推送到生产环境，或管理分支的生命周期。这些功能对于数据库模式迁移的工作流程至关重要。相关事件包括：分支创建（Branch Create）、分支创建操作（Branch Create）、模式差异更新（Schema Diff）、分支推送操作（Branch Promote）、开发分支（Development Branch）以及数据库分支（Database Branch）。
---

# `pscale` 分支管理

用于创建、删除、比较分支以及管理数据库分支。

## 常用命令

```bash
# Create branch from main
pscale branch create <database> <branch-name>

# Create branch from specific source
pscale branch create <database> <branch-name> --from <source-branch>

# List all branches
pscale branch list <database>

# Show branch details
pscale branch show <database> <branch-name>

# View schema diff
pscale branch diff <database> <branch-name>

# View schema
pscale branch schema <database> <branch-name>

# Delete branch
pscale branch delete <database> <branch-name>

# Promote to production
pscale branch promote <database> <branch-name>
```

## 工作流程

### 模式迁移流程（标准）

```bash
# 1. Create development branch
pscale branch create my-database feature-migration --from main

# 2. Make schema changes (via shell, ORM, or direct SQL)
pscale shell my-database feature-migration
# ... run ALTER TABLE, CREATE TABLE, etc.

# 3. View changes
pscale branch diff my-database feature-migration

# 4. Create deploy request (safer than direct promotion)
pscale deploy-request create my-database feature-migration

# 5. Deploy via deploy request (see pscale-deploy-request)
```

### 用于合并请求（MR/PR）的快速分支创建流程

```bash
# Match PlanetScale branch to your MR/PR branch
BRANCH_NAME="feature-add-user-preferences"
pscale branch create my-database $BRANCH_NAME --from main
```

有关自动化流程，请参见 `scripts/create-branch-for-mr.sh`。

### 模式比较

```bash
# Compare branch schema with main
pscale branch diff <database> <branch-name>

# View full branch schema
pscale branch schema <database> <branch-name>

# Export schema to file
pscale branch schema <database> <branch-name> > schema.sql
```

### 分支清理

```bash
# List all branches
pscale branch list <database>

# Delete merged/stale branches
pscale branch delete <database> <old-branch-name>
```

## 决策树

### 是应该直接推送更改，还是使用部署请求？

```
What's your environment?
├─ Production database → ALWAYS use deploy request (safe, reviewable)
├─ Pre-production database with team → Use deploy request (review workflow)
├─ Personal dev database → Direct promotion OK (but deploy request still safer)
└─ Experimental changes → Keep as branch, don't promote
```

### 何时创建新分支？

```
What's your goal?
├─ Schema migration for feature → Create branch (from main)
├─ Testing schema changes → Create branch (isolated)
├─ Hotfix schema change → Create branch (from production)
├─ Experiment / spike → Create branch (delete after)
└─ Working on existing schema → Use existing branch
```

## 故障排除

### “分支已存在”

**解决方案：**
```bash
# Check existing branches
pscale branch list <database>

# Use different name or delete existing
pscale branch delete <database> <existing-branch>
```

### 模式比较结果显示没有变化

**原因：**
- 尚未进行任何模式更改
- 更改未提交到数据库会话中
- 比较的是同一个分支

**解决方案：**
```bash
# Verify schema was modified
pscale branch schema <database> <branch-name>

# Ensure you're in the right branch when making changes
pscale shell <database> <branch-name>
```

### 无法删除分支

**错误信息：** “分支受保护” 或 “分支是生产环境分支”

**解决方案：**
```bash
# Demote production branch first
pscale branch demote <database> <branch-name>

# Then delete
pscale branch delete <database> <branch-name>
```

### 分支创建失败

**常见原因：**
- 分支名称无效（包含空格或特殊字符）
- 源分支不存在
- 权限不足

**解决方案：**
```bash
# Use valid branch name (alphanumeric, hyphens, underscores)
pscale branch create <database> my-feature-branch --from main

# Verify source branch exists
pscale branch list <database> | grep main
```

## 相关技能

- **`pscale-deploy-request`**：从分支创建部署请求（比直接推送更安全）
- **`pscale-database`**：数据库管理工具
- **`drizzle-kit`**：基于 ORM 的模式迁移工具（为 `pscale` shell 生成 SQL 语句）
- **`gitlab-cli-skills`**：合并请求（MR/PR）集成工具（跨工具统一分支名称）

## 参考资料

有关 `pscale` 分支管理的完整命令参考，请参见 `references/commands.md`。

## 分支生命周期

```
main (production)
  │
  ├─ Create branch ──> feature-branch (development)
  │                         │
  │                         ├─ Make schema changes
  │                         ├─ Test changes
  │                         └─ Create deploy request
  │                               │
  └─ Deploy ←──────────────────────┘
```

## 最佳实践

1. **始终从 `main` 分支创建用于模式更改的分支**
2. **使用描述性强的分支名称**（在适用的情况下与合并请求/拉取请求（MR/PR）的编号相匹配）
3. **在提交部署请求之前运行 `diff` 命令以审核更改**
4. **删除已合并的分支** 以保持分支列表的整洁
5. **使用部署请求** 而不是直接推送更改（便于审核和回滚）
6. **在部署之前在分支中测试模式更改**