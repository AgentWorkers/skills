---
name: glab-opentofu
description: 在 GitLab 中使用 OpenTofu 的状态管理功能。适用于管理 Terraform/OpenTofu 的状态、配置状态后端，或处理基础设施即代码（Infrastructure as Code, IaC）相关的工作。该功能会在 OpenTofu、Terraform、状态管理以及基础设施即代码相关操作触发时执行。
---

# glab opentofu

## 概述

```

  Work with the OpenTofu or Terraform integration.                                                                      
         
  USAGE  
         
    glab opentofu <command> [command] [--flags]  
            
  COMMANDS  
            
    init <state> [--flags]               Initialize OpenTofu or Terraform.
    state <command> [command] [--flags]  Work with the OpenTofu or Terraform states.
         
  FLAGS  
         
    -h --help                            Show help for this command.
    -R --repo                            Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab opentofu --help
```

## 子命令

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。