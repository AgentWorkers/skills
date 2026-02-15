---
name: glab-iteration
description: 用于管理 GitLab 的迭代周期，以支持项目规划和冲刺管理。适用于创建迭代周期、将问题分配给冲刺任务，或查看迭代进度。该功能会在迭代周期、冲刺周期、迭代计划或冲刺计划阶段被触发。
---

# glab 迭代（glab iteration）

## 概述

```

  Retrieve iteration information.                                                                                       
         
  USAGE  
         
    glab iteration <command> [command] [--flags]  
            
  COMMANDS  
            
    list [--flags]  List project iterations
         
  FLAGS  
         
    -h --help       Show help for this command.
    -R --repo       Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab iteration --help
```

## 子命令

有关 `--help` 命令的完整输出，请参阅 [references/commands.md](references/commands.md)。