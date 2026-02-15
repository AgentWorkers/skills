---
name: planetscale-cli-skills
description: **Comprehensive PlanetScale CLI (pscale) 命令参考及终端数据库管理工作流程**  
当用户提及 PlanetScale CLI、pscale 命令、数据库分支、部署请求、模式迁移或任何与 PlanetScale 相关的终端操作时，请参考本文档。本文档提供了关于这些功能的详细说明，并链接到了与身份验证、数据库管理、部署请求、备份等相关的子功能。相关触发事件包括 pscale 命令的执行、PlanetScale CLI 的使用、数据库分支的创建/修改、部署请求的提交以及模式迁移的操作。
requirements:
  binaries:
    - pscale
  binaries_optional:
    - grep
  env_optional:
    - PLANETSCALE_SERVICE_TOKEN_ID
    - PLANETSCALE_SERVICE_TOKEN
  notes: |
    Requires PlanetScale CLI authentication via 'pscale auth login' (stores token in ~/.config/planetscale/).
    Automation scripts use shell eval - ensure branch/database names come from trusted sources only (not user input).
    Scripts require PCRE-enabled grep (grep -oP) - may need adjustment on BSD/macOS systems.
---

# PlanetScale CLI 技能

本文档提供了关于 `pscale` 命令的全面参考信息，以及通过终端管理 PlanetScale 数据库的工作流程。

## 概述

PlanetScale CLI 可让您轻松地创建数据库分支、提交部署请求以及执行数据库模式迁移操作。本文档包含了所有 `pscale` 命令的参考信息、自动化脚本以及决策树（用于指导您选择合适的操作方式）。

## 子技能

| 命令                | 技能                        | 使用场景                          |
|-------------------|-----------------------------|-----------------------------------------|
| **auth**             | `pscale-auth`                    | 登录、登出、管理服务令牌                   |
| **branch**             | `pscale-branch`                    | 创建、删除、升级数据库分支                   |
| **deploy-request**         | `pscale-deploy-request`                | 创建、审核、部署数据库模式变更                 |
| **database**           | `pscale-database`                   | 创建、列出、显示、删除数据库                   |
| **backup**            | `pscale-backup`                    | 创建、列出、显示、删除数据库备份                   |
| **password**           | `pscale-password`                    | 创建、列出、删除数据库连接密码                   |
| **org**             | `pscale-org`                    | 列出、切换组织                         |
| **service-token**        | `pscale-service-token`                | 创建和管理 CI/CD 服务令牌                   |

## 决策树

### 应该使用“分支”还是“部署请求”？

```
What's your goal?
├─ Experimenting with schema changes → Create branch (pscale-branch)
├─ Testing schema in isolation → Create branch (pscale-branch)
├─ Ready to deploy schema to production → Create deploy request (pscale-deploy-request)
└─ Reviewing schema changes before production → Review deploy request (pscale-deploy-request)
```

### 服务令牌与密码，哪个更安全？

```
What's your use case?
├─ CI/CD pipeline → Service token (pscale-service-token)
├─ Local development → Password (pscale-password)
├─ Production application → Service token (rotatable, secure)
└─ One-off admin task → Password (temporary)
```

### 直接升级数据库模式还是通过部署请求？

```
Production readiness?
├─ Immediate promotion (dangerous) → pscale branch promote (pscale-branch)
├─ Review + approval workflow → pscale deploy-request create (pscale-deploy-request)
└─ Safe production deployment → Always use deploy requests
```

## 常见工作流程

### 数据库模式迁移流程

从创建分支到生产环境部署的完整流程：

```bash
# 1. Create development branch
pscale branch create <database> <branch-name>

# 2. Make schema changes (via shell, ORM, or direct SQL)
pscale shell <database> <branch-name>

# 3. View schema diff
pscale branch diff <database> <branch-name>

# 4. Create deploy request
pscale deploy-request create <database> <branch-name>

# 5. Review and deploy
pscale deploy-request deploy <database> <deploy-request-number>

# 6. Verify deployment
pscale deploy-request show <database> <deploy-request-number>
```

自动化脚本请参见 `scripts/` 目录：

- `create-branch-for-mr.sh`：根据 MR/PR 分支名称创建对应的 PlanetScale 分支
- `deploy-schema-change.sh`：完成数据库模式迁移流程
- `sync-branch-with-main.sh`：将开发分支与主分支同步

这些脚本在运行时无需加载额外环境信息（可节省约 90% 的令牌使用量）。

## 资源

- 官方文档：https://planetscale.com/docs/reference/planetscale-cli
- GitHub 仓库：https://github.com/planetscale/cli
- 社区论坛：https://github.com/planetscale/discussion