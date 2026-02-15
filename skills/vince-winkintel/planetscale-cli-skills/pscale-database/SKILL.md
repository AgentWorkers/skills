---
name: pscale-database
description: 创建、列出、显示、删除和管理 PlanetScale 数据库。这些命令用于创建新数据库、查看现有数据库列表、查询数据库详细信息、删除数据库或打开数据库 shell。相关触发器包括：database、create_database、list_databases、database_shell、pscale_shell。
---

# pscale 数据库

用于创建、读取、删除和管理数据库。

## 常用命令

```bash
# List all databases
pscale database list --org <org>

# Create database
pscale database create <database> --org <org>

# Show database details
pscale database show <database>

# Delete database
pscale database delete <database>

# Open database shell
pscale shell <database> <branch>
```

## 工作流程

### 数据库创建

```bash
# Create new database
pscale database create my-new-db --org my-org

# Create main branch (automatic)
# Create development branch
pscale branch create my-new-db development
```

### 数据库 shell 访问

```bash
# Open shell to specific branch
pscale shell my-database main

# Execute SQL directly
pscale shell my-database main --execute "SHOW TABLES"

# Run SQL from file
pscale shell my-database main < schema.sql
```

## 故障排除

### 无法创建数据库

**错误消息：** “组织使用限制已达到”

**解决方法：** 升级计划或删除未使用的数据库

### shell 连接失败

**错误消息：** “身份验证失败”

**解决方法：**
```bash
# Re-authenticate
pscale auth logout && pscale auth login

# Verify branch exists
pscale branch list <database>
```

## 相关技能

- **pscale-branch** - 管理数据库分支
- **pscale-password** - 为数据库创建连接密码

## 参考资料

有关完整命令的详细信息，请参阅 `references/commands.md`。