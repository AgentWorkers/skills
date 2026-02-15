---
name: glab-snippet
description: **使用说明：**  
在处理 glab 插件中的代码片段（snippet）命令时，请遵循以下规则。
---

# glab 插件片段

## 概述

```

  Create, view and manage snippets.                                                                                     
         
  USAGE  
         
    glab snippet <command> [command] [--flags]                                 
            
  EXAMPLES  
            
    $ glab snippet create --title "Title of the snippet" --filename "main.go"  
            
  COMMANDS  
            
    create  -t <title> <file1>                                        [<file2>...] [--flags]  Create a new snippet.
    glab snippet create  -t <title> -f <filename>  # reads from stdin                                              
         
  FLAGS  
         
    -h --help                                                                                 Show help for this command.
    -R --repo                                                                                 Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab snippet --help
```

## 子命令

有关 `--help` 命令的完整输出，请参阅 [references/commands.md](references/commands.md)。