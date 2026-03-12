---
name: glab-deploy-key
description: 管理 GitLab 项目的 SSH 部署密钥，包括添加、列出和删除操作。这些功能可用于配置持续集成/持续部署（CI/CD）所需的部署密钥、管理只读访问权限，或配置部署认证。相关操作会触发与部署密钥、SSH 密钥或只读访问权限相关的事件。
---
# glab deploy-key

## 概述

```

  Manage deploy keys.                                                                                                   
         
  USAGE  
         
    glab deploy-key <command> [command] [--flags]  
            
  COMMANDS  
            
    add [key-file] [--flags]  Add a deploy key to a GitLab project.
    delete <key-id>           Deletes a single deploy key specified by the ID.
    get <key-id>              Returns a single deploy key specified by the ID.
    list [--flags]            Get a list of deploy keys for the current project.
         
  FLAGS  
         
    -h --help                 Show help for this command.
    -R --repo                 Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab deploy-key --help
```

## v1.89.0 更新

> **v1.89.0+：** `glab deploy-key list` 和 `glab deploy-key get` 命令新增了 `--output json` / `-F json` 选项，支持结构化输出，非常适合自动化脚本使用。

```bash
# List deploy keys with JSON output (v1.89.0+)
glab deploy-key list --output json
glab deploy-key list -F json

# Get a specific deploy key with JSON output (v1.89.0+)
glab deploy-key get <key-id> --output json
glab deploy-key get <key-id> -F json
```

## 子命令

有关完整的 `--help` 信息，请参阅 [references/commands.md](references/commands.md)。