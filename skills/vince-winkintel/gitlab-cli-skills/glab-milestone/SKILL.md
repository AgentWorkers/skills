---
name: glab-milestone
description: 管理项目里程碑，包括创建、列出、更新、查看和关闭等操作。适用于规划发布、跟踪里程碑进度，或按里程碑组织问题/任务（Issues/Requirements）。该功能会在里程碑达成、发布计划制定、里程碑进度更新或版本更新时触发。
---

# glab 里程碑

## 概述

```

  Manage group or project milestones.                                                                                   
         
  USAGE  
         
    glab milestone <command> [command] [--flags]  
            
  COMMANDS  
            
    create [--flags]  Create a group or project milestone.
    delete [--flags]  Delete a group or project milestone.
    edit [--flags]    Edit a group or project milestone.
    get [--flags]     Get a milestones via an ID for a project or group.
    list [--flags]    Get a list of milestones for a project or group.
         
  FLAGS  
         
    -h --help         Show help for this command.
    -R --repo         Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab milestone --help
```

## 子命令

有关 `--help` 命令的完整输出，请参阅 [references/commands.md](references/commands.md)。