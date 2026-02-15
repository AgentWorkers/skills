---
name: glab-variable
description: 在项目和组级别管理 CI/CD 变量，包括创建、更新、列出和删除操作。适用于为管道设置环境变量、管理密钥或配置 CI/CD 变量。该功能会在变量、CI 变量、环境变量或密钥发生更改时触发。
---

# glab 变量

## 概述

```

  Manage variables for a GitLab project or group.                                                                       
         
  USAGE  
         
    glab variable [command] [--flags]  
            
  COMMANDS  
            
    delete <key> [--flags]          Delete a variable for a project or group.
    export [--flags]                Export variables from a project or group.
    get <key> [--flags]             Get a variable for a project or group.
    list [--flags]                  List variables for a project or group.
    set <key> <value> [--flags]     Create a new variable for a project or group.
    update <key> <value> [--flags]  Update an existing variable for a project or group.
         
  FLAGS  
         
    -h --help                       Show help for this command.
    -R --repo                       Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab variable --help
```

## 子命令

有关 `--help` 命令的完整输出，请参阅 [references/commands.md](references/commands.md)。