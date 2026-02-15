---
name: glab-incident
description: 用于管理 GitLab 中的事件（incidents），以实现问题跟踪（issue tracking）和事件处理（incident management）的功能。适用于创建事件、管理事件响应（incident response），或将事件与问题（issues）关联起来。该功能会在事件发生、事件管理过程启动、事件被创建或事件响应开始时触发。
---

# glab 事件

## 概述

```

  Work with GitLab incidents.                                                                                           
         
  USAGE  
         
    glab incident [command] [--flags]  
            
  EXAMPLES  
            
    $ glab incident list               
            
  COMMANDS  
            
    close [<id> | <url>] [--flags]   Close an incident.
    list [--flags]                   List project incidents.
    note <incident-id> [--flags]     Comment on an incident in GitLab.
    reopen [<id> | <url>] [--flags]  Reopen a resolved incident.
    subscribe <id>                   Subscribe to an incident.
    unsubscribe <id>                 Unsubscribe from an incident.
    view <id> [--flags]              Display the title, body, and other information about an incident.
         
  FLAGS  
         
    -h --help                        Show help for this command.
    -R --repo                        Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab incident --help
```

## 子命令

有关 `--help` 命令的完整输出，请参阅 [references/commands.md](references/commands.md)。