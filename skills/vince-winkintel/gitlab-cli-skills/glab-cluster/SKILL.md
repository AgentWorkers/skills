---
name: glab-cluster
description: 管理 GitLab Kubernetes 集群及其代理集成。适用于连接集群、管理集群代理或处理与 Kubernetes 集成相关的工作。相关操作会在集群、Kubernetes、k8s 或集群代理层面触发。
---
# glab 集群

## 概述

```

  Manage GitLab Agents for Kubernetes and their clusters.                                                               
         
  USAGE  
         
    glab cluster <command> [command] [--flags]  
            
  COMMANDS  
            
    agent <command> [command] [--flags]  Manage GitLab Agents for Kubernetes.
    graph [--flags]                      Queries the Kubernetes object graph, using the GitLab Agent for Kubernetes. (EXPERIMENTAL)
         
  FLAGS  
         
    -h --help                            Show help for this command.
    -R --repo                            Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab cluster --help
```

## v1.89.0 更新

> **v1.89.0+：** `glab cluster agent list` 和 `glab cluster agent token list` 命令支持 `--output json` / `-F json` 选项，可生成结构化的输出，非常适合用于自动化脚本的编写。

```bash
# List cluster agents with JSON output (v1.89.0+)
glab cluster agent list --output json
glab cluster agent list -F json

# List agent tokens with JSON output (v1.89.0+)
glab cluster agent token list <agent-id> --output json
glab cluster agent token list <agent-id> -F json
```

## 子命令

有关完整的 `--help` 选项说明，请参阅 [references/commands.md](references/commands.md)。