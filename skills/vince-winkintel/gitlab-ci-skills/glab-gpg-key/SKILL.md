---
name: glab-gpg-key
description: **使用说明：**  
在操作 `glab gpg-key` 命令时，请参考以下说明。
---

# glab gpg-key

## 概述

```

  Manage GPG keys registered with your GitLab account.                                                                  
         
  USAGE  
         
    glab gpg-key <command> [command] [--flags]  
            
  COMMANDS  
            
    add [key-file]   Add a GPG key to your GitLab account.
    delete <key-id>  Deletes a single GPG key specified by the ID.
    get <key-id>     Returns a single GPG key specified by the ID.
    list [--flags]   Get a list of GPG keys for the currently authenticated user.
         
  FLAGS  
         
    -h --help        Show help for this command.
    -R --repo        Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab gpg-key --help
```

## 子命令

有关完整的 `--help` 命令帮助信息，请参阅 [references/commands.md](references/commands.md)。