---
name: glab-schedule
description: 管理持续集成/持续交付（CI/CD）管道的调度任务，包括创建、列出、更新、删除以及运行已安排的管道。适用于自动化管道流程、设置定时任务（cron jobs）或管理定期构建（scheduled builds）的场景。触发方式包括按计划执行、通过管道调度系统、定时任务（cron）或自动化构建流程来实现。
---

# glab schedule

## 概述

```

  Work with GitLab CI/CD schedules.                                                                                     
         
  USAGE  
         
    glab schedule <command> [command] [--flags]  
            
  COMMANDS  
            
    create [--flags]       Schedule a new pipeline.
    delete <id> [--flags]  Delete the schedule with the specified ID.
    list [--flags]         Get the list of schedules.
    run <id>               Run the specified scheduled pipeline.
    update <id> [--flags]  Update a pipeline schedule.
         
  FLAGS  
         
    -h --help              Show help for this command.
    -R --repo              Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab schedule --help
```

## 子命令

有关所有 `--help` 命令的详细信息，请参阅 [references/commands.md](references/commands.md)。