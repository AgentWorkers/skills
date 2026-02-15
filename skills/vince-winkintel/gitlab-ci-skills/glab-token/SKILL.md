---
name: glab-token
description: **使用说明：**  
在处理 glab 的令牌命令时，请参考以下说明。
---

# glab 令牌

## 概述

```

  Manage personal, project, or group tokens                                                                             
         
  USAGE  
         
    glab token [command] [--flags]  
            
  COMMANDS  
            
    create <name> [--flags]                 Creates user, group, or project access tokens.
    list [--flags]                          List user, group, or project access tokens.
    revoke <token-name|token-id> [--flags]  Revoke user, group or project access tokens
    rotate <token-name|token-id> [--flags]  Rotate user, group, or project access tokens
         
  FLAGS  
         
    -h --help                               Show help for this command.
    -R --repo                               Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab token --help
```

## 子命令

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。