---
name: planetscale-cli-skills
description: >
  **PlanetScale CLI（pscale）命令参考及终端数据库管理工作流程**  
  当用户提及 PlanetScale CLI、pscale 命令、数据库分支、部署请求、模式迁移或任何与 PlanetScale 相关的终端操作时，请参考本文档。本文档提供了关于这些功能的详细说明，并链接到了与身份验证、数据库管理、部署请求、备份等相关的子功能。相关操作会触发 pscale、PlanetScale CLI、数据库分支、部署请求或模式迁移等自动化流程。  
  **主要内容包括：**  
  - pscale 命令的全面参考  
  - 通过终端进行数据库管理的具体工作流程  
  - 与身份验证、数据库分支、部署请求、备份等相关的子功能链接  
  - 自动化操作的相关说明  
  **适用场景：**  
  适用于需要通过终端执行 PlanetScale 相关操作的场景，如命令行管理、数据库维护、自动化部署等。  
  **注意事项：**  
  1. 保持技术内容的准确性和专业性。  
  2. 代码示例、命令和 URL 保持不变。  
  3. 保留 Markdown 格式。  
  4. 在适当的情况下使用英文技术术语（如 OpenClaw、ClawHub、API、CLI）。  
  5. 仅翻译代码块中的解释性注释。  
  6. 保持与原文相同的结构和组织方式。  
  7. 不添加或删除任何内容。  
  8. 保留所有占位符（如 `___CODE_BLOCK_0___`）的原样。
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
    Scripts require PCRE-enabled grep (grep -oP) - may need adjustment on BSD/macOS systems.
metadata:
  openclaw:
    purpose: >
      Provide command reference and automation for PlanetScale CLI (pscale) operations only.
      Scope is limited to: database and branch management, deploy requests, backups, passwords,
      service tokens, and organization management via the pscale CLI tool.
    capabilities:
      - Run pscale CLI commands to manage PlanetScale databases, branches, and deploy requests
      - Execute bundled automation scripts (create-branch-for-mr.sh, deploy-schema-change.sh, sync-branch-with-main.sh)
      - Read PlanetScale CLI output and help users interpret results
    install_mechanism: >
      Skill files are loaded into agent context when a matching PlanetScale/pscale task is detected.
      Automation scripts are executed directly via shell (bash). No network access beyond pscale CLI calls.
      Scripts do not use eval or dynamic code execution; all pscale arguments are passed as discrete tokens.
    requires:
      credentials:
        - name: PLANETSCALE_SERVICE_TOKEN_ID
          description: >
            PlanetScale service token ID for CI/CD authentication. Optional — interactive login
            via 'pscale auth login' can be used instead. Token stored in environment variable only;
            this skill does not read, store, or transmit credentials beyond passing them to pscale CLI.
          required: false
        - name: PLANETSCALE_SERVICE_TOKEN
          description: >
            PlanetScale service token secret for CI/CD authentication. Optional — interactive login
            via 'pscale auth login' can be used instead. Token stored in environment variable only;
            this skill does not read, store, or transmit credentials beyond passing them to pscale CLI.
          required: false
---
# PlanetScale CLI 技能

这是一份关于如何通过终端管理 PlanetScale 数据库的 `pscale` 命令的全面参考指南及工作流程。

## 概述

PlanetScale CLI 使您能够轻松地创建数据库分支、提交部署请求以及执行数据库模式迁移操作。本文档提供了所有 `pscale` 命令的详细参考信息、自动化脚本以及决策辅助工具。

## 子技能

| 命令          | 技能            | 使用场景                           |
|----------------|-----------------------------|-------------------------------------------|
| **auth**        | `pscale-auth`       | 登录、登出、管理服务令牌、身份验证管理             |
| **branch**       | `pscale-branch`      | 创建、删除、升级数据库分支                   |
| **deploy-request**   | `pscale-deploy-request`  | 创建、审核、部署数据库模式变更                 |
| **database**     | `pscale-database`     | 创建、列出、显示、删除数据库                   |
| **backup**      | `pscale-backup`     | 创建、列出、显示、删除数据库备份                   |
| **password**     | `pscale-password`     | 创建、列出、删除数据库连接密码                   |
| **org**        | `pscale-org`       | 列出、显示、切换组织                         |
| **service-token**   | `pscale-service-token` | 创建和管理 CI/CD 服务令牌                   |

## 决策辅助工具

### 应该使用“分支”还是“部署请求”？

```
What's your goal?
├─ Experimenting with schema changes → Create branch (pscale-branch)
├─ Testing schema in isolation → Create branch (pscale-branch)
├─ Ready to deploy schema to production → Create deploy request (pscale-deploy-request)
└─ Reviewing schema changes before production → Review deploy request (pscale-deploy-request)
```

### 使用服务令牌还是密码？

```
What's your use case?
├─ CI/CD pipeline → Service token (pscale-service-token)
├─ Local development → Password (pscale-password)
├─ Production application → Service token (rotatable, secure)
└─ One-off admin task → Password (temporary)
```

### 直接升级数据库还是提交部署请求？

```
Production readiness?
├─ Immediate promotion (dangerous) → pscale branch promote (pscale-branch)
├─ Review + approval workflow → pscale deploy-request create (pscale-deploy-request)
└─ Safe production deployment → Always use deploy requests
```

## 常见工作流程

### 数据库模式迁移流程

从创建数据库分支到最终部署的完整流程：

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

- `create-branch-for-mr.sh`：根据您的 MR/PR 分支名称创建对应的 PlanetScale 分支
- `deploy-schema-change.sh`：完成数据库模式迁移流程
- `sync-branch-with-main.sh`：将开发分支与主分支同步

这些脚本在运行时无需加载额外环境信息（可节省约 90% 的令牌使用量）。

## 资源

- 官方文档：https://planetscale.com/docs/reference/planetscale-cli
- GitHub 仓库：https://github.com/planetscale/cli
- 社区论坛：https://github.com/planetscale/discussion