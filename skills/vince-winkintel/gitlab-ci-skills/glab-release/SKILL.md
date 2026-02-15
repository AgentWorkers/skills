---
name: glab-release
description: **使用说明：**  
在处理 glab 的发布命令时，请参考以下说明。
---

# glab 版本发布

## 概述

```

  Manage GitLab releases.                                                                                               
         
  USAGE  
         
    glab release <command> [command] [--flags]  
            
  COMMANDS  
            
    create <tag> [<files>...] [--flags]  Create a new GitLab release, or update an existing one.
    delete <tag> [--flags]               Delete a GitLab release.
    download <tag> [--flags]             Download asset files from a GitLab release.
    list [--flags]                       List releases in a repository.
    upload <tag> [<files>...] [--flags]  Upload release asset files or links to a GitLab release.
    view <tag> [--flags]                 View information about a GitLab release.
         
  FLAGS  
         
    -h --help                            Show help for this command.
    -R --repo                            Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab release --help
```

## 子命令

有关完整的 `--help` 命令帮助信息，请参阅 [references/commands.md](references/commands.md)。