---
name: glab-issue
description: **使用说明：**  
在操作 glab 的问题相关命令时，请参考本说明。
---

# glab 问题

## 概述

```

  Work with GitLab issues.                                                                                              
         
  USAGE  
         
    glab issue [command] [--flags]                                         
            
  EXAMPLES  
            
    $ glab issue list                                                      
    $ glab issue create --label --confidential                             
    $ glab issue view --web 123                                            
    $ glab issue note -m "closing because !123 was merged" <issue number>  
            
  COMMANDS  
            
    board [command] [--flags]        Work with GitLab issue boards in the given project.
    close [<id> | <url>] [--flags]   Close an issue.
    create [--flags]                 Create an issue.
    delete <id>                      Delete an issue.
    list [--flags]                   List project issues.
    note <issue-id> [--flags]        Comment on an issue in GitLab.
    reopen [<id> | <url>] [--flags]  Reopen a closed issue.
    subscribe <id>                   Subscribe to an issue.
    unsubscribe <id>                 Unsubscribe from an issue.
    update <id> [--flags]            Update issue
    view <id> [--flags]              Display the title, body, and other information about an issue.
         
  FLAGS  
         
    -h --help                        Show help for this command.
    -R --repo                        Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab issue --help
```

## 子命令

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。