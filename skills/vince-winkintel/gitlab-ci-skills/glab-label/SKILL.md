---
name: glab-label
description: **使用说明：**  
在处理 `glab` 的标签命令时，请参考以下说明。
---

# glab label

## 概述

```

  Manage labels on remote.                                                                                              
         
  USAGE  
         
    glab label <command> [command] [--flags]  
            
  COMMANDS  
            
    create [--flags]  Create labels for a repository or project.
    delete [--flags]  Delete labels for a repository or project.
    edit [--flags]    Edit group or project label.
    get <label-id>    Returns a single label specified by the ID.
    list [--flags]    List labels in the repository.
         
  FLAGS  
         
    -h --help         Show help for this command.
    -R --repo         Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab label --help
```

## 子命令

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。