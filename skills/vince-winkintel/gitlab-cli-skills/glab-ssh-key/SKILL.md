---
name: glab-ssh-key
description: 管理 GitLab 账户的 SSH 密钥，包括添加、列出和删除操作。适用于设置 SSH 认证、管理 SSH 密钥或配置通过 SSH 进行的 Git 传输。相关操作会触发 SSH 密钥的添加、SSH 认证以及 Git 的 SSH 配置相关事件。
---

# glab ssh-key

## 概述

```

  Manage SSH keys registered with your GitLab account.                                                                  
         
  USAGE  
         
    glab ssh-key <command> [command] [--flags]  
            
  COMMANDS  
            
    add [key-file] [--flags]   Add an SSH key to your GitLab account.
    delete <key-id> [--flags]  Deletes a single SSH key specified by the ID.
    get <key-id> [--flags]     Returns a single SSH key specified by the ID.
    list [--flags]             Get a list of SSH keys for the currently authenticated user.
         
  FLAGS  
         
    -h --help                  Show help for this command.
    -R --repo                  Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab ssh-key --help
```

## 子命令

有关完整的 `--help` 信息，请参阅 [references/commands.md](references/commands.md)。