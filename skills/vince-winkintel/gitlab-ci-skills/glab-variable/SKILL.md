---
name: glab-variable
description: **使用说明：**  
在处理与 `glab` 变量相关的命令时，请参考本说明。
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

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。