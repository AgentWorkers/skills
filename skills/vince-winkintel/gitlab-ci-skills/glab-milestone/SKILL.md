---
name: glab-milestone
description: **使用说明：**  
在处理 glab 的里程碑命令时，请参考以下说明。
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

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。