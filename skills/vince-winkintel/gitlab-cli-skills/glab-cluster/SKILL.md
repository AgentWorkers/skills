---
name: glab-cluster
description: 管理 GitLab Kubernetes 集群及其代理集成。适用于连接集群、管理集群代理或处理与 Kubernetes 集成相关的工作。触发条件包括集群状态变化、Kubernetes 系统事件以及集群代理的相关操作。
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

## 子命令

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。