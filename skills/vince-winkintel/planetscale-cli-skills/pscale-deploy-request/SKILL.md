---
name: pscale-deploy-request
description: 通过部署请求（deploy requests）来创建、审查、部署和回滚数据库模式（schema changes）。该功能适用于将数据库模式迁移（schema migrations）部署到生产环境（production）、在部署前审查数据库变更、管理部署请求的生命周期（lifecycle），或回滚已部署的变更。对于确保生产环境中的数据库模式安全部署至关重要。相关操作包括：触发部署请求（trigger a deploy request）、部署数据库模式（deploy a schema）、审查部署结果（review the deployment）、回滚部署操作（revert a deployment），以及执行生产环境中的迁移（perform production migrations）。
---

# `pscale deploy-request`

用于创建、审查、比较差异、回滚以及管理数据库模式变更的部署请求。

## 常用命令

```bash
# Create deploy request from branch
pscale deploy-request create <database> <branch-name>

# List deploy requests
pscale deploy-request list <database>

# Show deploy request details
pscale deploy-request show <database> <number>

# View deploy request diff
pscale deploy-request diff <database> <number>

# Deploy (apply changes)
pscale deploy-request deploy <database> <number>

# Close without deploying
pscale deploy-request close <database> <number>

# Revert deployed changes
pscale deploy-request revert <database> <number>
```

## 工作流程

### 完整的数据库模式迁移（推荐）

这是将模式变更部署到生产环境的最安全方式：

```bash
# 1. Create development branch
pscale branch create my-database feature-schema-v2 --from main

# 2. Make schema changes
pscale shell my-database feature-schema-v2
# ... execute ALTER TABLE, etc.

# 3. Review changes locally
pscale branch diff my-database feature-schema-v2

# 4. Create deploy request
pscale deploy-request create my-database feature-schema-v2

# 5. Review deploy request diff
pscale deploy-request diff my-database 1

# 6. Deploy to production
pscale deploy-request deploy my-database 1

# 7. Verify deployment
pscale deploy-request show my-database 1
```

### 部署前的审查

```bash
# List pending deploy requests
pscale deploy-request list <database> --state open

# Show details
pscale deploy-request show <database> <number>

# View schema diff
pscale deploy-request diff <database> <number>

# Deploy if approved
pscale deploy-request deploy <database> <number>
```

### 回滚部署

如果已部署的模式变更引发了问题：

```bash
# View deployment status
pscale deploy-request show <database> <number>

# Revert the deployment
pscale deploy-request revert <database> <number>

# Verify revert
pscale deploy-request show <database> <number>
```

## 决策树

### 是否应该进行部署？

```
Deploy request ready?
├─ Schema changes tested → Deploy
├─ Changes need revision → Close and create new DR from updated branch
├─ Changes no longer needed → Close
└─ Breaking changes detected → Close, fix in branch, create new DR
```

### 是否应该回滚？

```
After deployment issues?
├─ Production errors caused by schema → Revert immediately
├─ Data integrity issues → Revert, then investigate
├─ Performance degradation → Revert if severe
└─ Minor issues / non-urgent → Leave deployed, fix forward
```

## 故障排除

### 部署请求创建失败

**错误：**“未检测到模式变更”

**原因：**分支中的模式与生产环境中的模式相同

**解决方案：**
```bash
# Verify schema diff exists
pscale branch diff <database> <branch-name>

# If no diff, make schema changes first
pscale shell <database> <branch-name>
```

### “无法部署：检测到冲突”

**原因：**自创建分支以来，生产环境中的模式发生了变化

**解决方案：**
```bash
# Close conflicting deploy request
pscale deploy-request close <database> <number>

# Refresh branch schema
pscale branch refresh-schema <database> <branch-name>

# Create new deploy request
pscale deploy-request create <database> <branch-name>
```

### 部署过程中失败

**错误：**部署已开始但失败

**解决方案：**
```bash
# Check deploy request status
pscale deploy-request show <database> <number>

# If partially deployed, may need to revert
pscale deploy-request revert <database> <number>

# Contact PlanetScale support for stuck deployments
```

### 无法关闭部署请求

**错误：**“部署请求已部署”

**原因：**已部署的请求无法被关闭

**解决方案：**
```bash
# Deployed requests can only be reverted
pscale deploy-request revert <database> <number>
```

## 部署请求的状态

| 状态 | 描述 | 可用的操作 |
|-------|-------------|-------------------|
| `open` | 待部署 | 部署、关闭、比较差异、审查 |
| `in_progress` | 正在部署中 | （等待完成） |
| `complete` | 部署成功 | 回滚、查看 |
| `closed` | 未进行部署即已关闭 | （无操作 - 只读） |
| `reverted` | 先部署后回滚 | （无操作 - 只读） |

## 相关技能

- `pscale-branch` - 为部署请求创建分支
- `drizzle-kit` - 生成用于模式变更的迁移SQL语句
- `gitlab-cli-skills` - GitLab合并请求集成（将部署请求与合并请求关联）

## 最佳实践

1. **在部署前务必审查差异**（使用 `pscale deploy-request diff`）
2. **在创建部署请求之前，在分支中测试模式变更**
3. 为分支使用描述性名称（与合并请求/问题编号相匹配）
4. 在维护窗口期间进行部署（避免影响生产环境）
5. 制定回滚计划（知道如何回滚）
6. 部署后进行监控（检查是否有错误）
7. 清理旧的部署请求（关闭过期的请求）

## 自动化

有关完整的自动化流程，请参阅 `scripts/deploy-schema-change.sh`：

```bash
# Automated deploy workflow
./scripts/deploy-schema-change.sh \
  --database my-database \
  --branch feature-schema-v2 \
  --auto-approve
```

## 与Drizzle的集成

对于Drizzle ORM用户来说，常见的集成方式如下：

```bash
# 1. Edit your schema.sql file
# 2. Create PlanetScale branch
pscale branch create my-database <branch-name>

# 3. Apply schema changes
pscale shell my-database <branch-name> < schema.sql

# 4. Create deploy request
pscale deploy-request create my-database <branch-name>

# 5. Deploy
pscale deploy-request deploy my-database <number>

# 6. Pull schema back to Drizzle
pnpm drizzle-kit introspect

# 7. Review and apply generated schema
```

## 参考资料

有关 `pscale deploy-request` 命令的完整参考信息，请参阅 `references/commands.md`。