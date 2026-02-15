---
name: pscale-password
description: 创建、列出和删除分支连接密码。这些功能可用于为应用程序生成连接字符串、管理数据库凭据、为本地开发生成密码或定期更新凭据。相关操作会在密码、连接字符串或数据库凭据发生变化时被触发。
---

# pscale 密码管理

用于创建、列出和删除数据库连接的分支密码。

## 常用命令

```bash
# Create password
pscale password create <database> <branch> <password-name>

# List passwords
pscale password list <database> <branch>

# Delete password
pscale password delete <database> <branch> <password-id>
```

## 工作流程

### 应用程序连接

```bash
# Create password for production app
pscale password create my-database main production-app

# Returns connection string:
# mysql://username:password@host/database

# Use in application environment variables
export DATABASE_URL="mysql://..."
```

### 本地开发

```bash
# Create temporary password for local dev
pscale password create my-db main local-dev

# Delete when done
pscale password delete my-db main <password-id>
```

## 故障排除

### 密码无法使用

**解决方案：** 删除并重新创建密码（密码可能已过期）

```bash
pscale password list <database> <branch>
pscale password delete <database> <branch> <old-id>
pscale password create <database> <branch> new-name
```

## 相关技能

- **pscale-service-token** - 用于 CI/CD 认证（优于使用密码）
- **pscale-database** - 数据库管理

## 参考资料

请参阅 `references/commands.md` 以获取完整的命令参考信息。