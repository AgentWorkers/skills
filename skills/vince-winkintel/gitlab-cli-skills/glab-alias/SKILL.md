---
name: glab-alias
description: 创建、列出和删除 GitLab CLI 命令的别名（aliases）和快捷方式（shortcuts）。这些功能可用于创建自定义的 GitLab 命令、管理 CLI 快捷方式，或查看现有的别名。相关操作会在别名、快捷方式或自定义命令被使用时触发。
---

# glab 别名

## 概述

```

  Create, list, and delete aliases.                                                                                     
         
  USAGE  
         
    glab alias [command] [--flags]  
            
  COMMANDS  
            
    delete <alias name> [--flags]           Delete an alias.
    list [--flags]                          List the available aliases.
    set <alias name> '<command>' [--flags]  Set an alias for a longer command.
         
  FLAGS  
         
    -h --help                               Show help for this command.
```

## 快速入门

```bash
glab alias --help
```

## 子命令

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。