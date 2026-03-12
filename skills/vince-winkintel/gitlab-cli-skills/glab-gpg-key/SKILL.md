---
name: glab-gpg-key
description: 管理用于提交签名的GPG密钥，包括添加、列出和删除等操作。适用于配置提交签名、管理GPG密钥或验证已签名的提交。相关事件会在GPG密钥更新、提交签名完成或提交被验证时触发。
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

## v1.89.0 更新

> **v1.89.0+：** `glab gpg-key list` 和 `glab gpg-key get` 命令新增了 `--output json` / `-F json` 选项，支持结构化输出，非常适合用于自动化脚本。

```bash
# List GPG keys with JSON output (v1.89.0+)
glab gpg-key list --output json
glab gpg-key list -F json

# Get a specific GPG key with JSON output (v1.89.0+)
glab gpg-key get <key-id> --output json
glab gpg-key get <key-id> -F json
```

## 子命令

有关完整的 `--help` 信息，请参阅 [references/commands.md](references/commands.md)。