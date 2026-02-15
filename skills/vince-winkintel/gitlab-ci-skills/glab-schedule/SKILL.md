---
name: glab-schedule
description: **使用说明：**  
在配合 `glab` 的调度命令（schedule commands）使用时，请参考以下说明。
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

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。