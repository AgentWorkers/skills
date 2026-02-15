---
name: glab-token
description: 管理 GitLab 的个人访问令牌（Personal Access Tokens, PAT）和项目访问令牌（Project Access Tokens）。这些令牌用于在创建新令牌、撤销访问权限或管理 API 认证时使用。相关事件会触发对令牌、个人访问令牌（PAT）和 API 令牌的处理。
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