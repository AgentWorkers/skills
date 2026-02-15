---
name: glab-deploy-key
description: 在使用 `glab deploy-key` 命令时，请参考以下说明。
---

# glab deploy-key

## 概述

```

  Manage deploy keys.                                                                                                   
         
  USAGE  
         
    glab deploy-key <command> [command] [--flags]  
            
  COMMANDS  
            
    add [key-file] [--flags]  Add a deploy key to a GitLab project.
    delete <key-id>           Deletes a single deploy key specified by the ID.
    get <key-id>              Returns a single deploy key specified by the ID.
    list [--flags]            Get a list of deploy keys for the current project.
         
  FLAGS  
         
    -h --help                 Show help for this command.
    -R --repo                 Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab deploy-key --help
```

## 子命令

有关 `--help` 的完整输出，请参阅 [references/commands.md](references/commands.md)。