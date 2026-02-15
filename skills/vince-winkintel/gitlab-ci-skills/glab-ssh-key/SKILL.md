---
name: glab-ssh-key
description: **使用说明：**  
在操作与 `glab` 相关的 SSH 密钥命令时，请参考以下说明。
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