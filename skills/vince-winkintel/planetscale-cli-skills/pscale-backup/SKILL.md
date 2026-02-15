---
name: pscale-backup
description: 创建、列出、显示和删除分支备份。这些功能可用于创建数据库备份、从备份中恢复数据、管理备份生命周期，或安排自动备份任务。相关操作会在备份、恢复、数据库备份或分支备份时被触发。
---

# pscale 备份

用于创建、列出、显示和删除分支备份。

## 常用命令

```bash
# Create backup
pscale backup create <database> <branch>

# List backups
pscale backup list <database> <branch>

# Show backup details
pscale backup show <database> <branch> <backup-id>

# Delete backup
pscale backup delete <database> <branch> <backup-id>
```

## 工作流程

### 迁移前的备份

```bash
# Create backup before schema changes
pscale backup create my-database main

# Proceed with migration
pscale deploy-request deploy my-database 1

# If issues, restore from backup (contact PlanetScale support)
```

## 相关技能

- **pscale-branch** - 备份特定分支
- **pscale-deploy-request** - 部署前的备份

## 参考资料

请参阅 `references/commands.md` 以获取完整的命令参考信息。