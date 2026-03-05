---
name: glab-ssh-key
description: 管理 GitLab 账户的 SSH 密钥，包括添加、列出和删除操作。适用于设置 SSH 认证、管理 SSH 密钥或配置通过 SSH 进行的 Git 仓库访问。相关操作会触发在 SSH 密钥的添加、SSH 认证或 Git SSH 配置过程中。
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

## ⚠️ 安全警告：仅上传公钥

**请务必确认您上传的是公钥，而非私钥。**

- ✅ 公钥：`~/.ssh/id_rsa.pub`、`~/.ssh/id_ed25519.pub`（文件扩展名为 `.pub`）
- ❌ 私钥：`~/.ssh/id_rsa`、`~/.ssh/id_ed25519`（文件没有扩展名——切勿上传这些文件）

将私钥上传到 GitLab 会暴露您的凭据。在运行 `glab ssh-key add` 命令之前，请仔细检查文件名。

```bash
# ✅ Safe — public key
glab ssh-key add ~/.ssh/id_ed25519.pub --title "My Laptop"

# ❌ NEVER do this — private key
# glab ssh-key add ~/.ssh/id_ed25519 --title "My Laptop"
```

**上传前，请确认您的密钥是公钥：**
```bash
# Should start with 'ssh-rsa', 'ssh-ed25519', 'ecdsa-sha2-*', etc.
head -c 20 ~/.ssh/id_ed25519.pub
```

## 快速入门

```bash
glab ssh-key --help
```

## 子命令

有关完整的 `--help` 命令帮助信息，请参阅 [references/commands.md](references/commands.md)。