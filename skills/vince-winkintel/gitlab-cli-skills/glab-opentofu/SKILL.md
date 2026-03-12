---
name: glab-opentofu
description: 在 GitLab 中使用 OpenTofu 的状态管理功能。适用于管理 Terraform/OpenTofu 的状态、配置状态后端，或处理基础设施即代码（Infrastructure as Code, IaC）相关的工作。该功能会在 OpenTofu、Terraform、状态管理以及基础设施即代码相关操作发生时被触发。
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

## v1.89.0 更新

> **v1.89.0+：** `glab opentofu state list` 命令现在支持 `--output json` / `-F json` 选项，可生成结构化输出，非常适合用于自动化脚本。

```bash
# List OpenTofu state with JSON output (v1.89.0+)
glab opentofu state list --output json
glab opentofu state list -F json
```

## 子命令

有关完整的 `--help` 命令帮助信息，请参阅 [references/commands.md](references/commands.md)。