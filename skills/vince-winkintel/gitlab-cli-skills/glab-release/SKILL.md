---
name: glab-release
description: 管理 GitLab 的发布版本，包括创建、列出、查看、删除以及上传/下载发布相关的资产。该工具适用于发布软件版本、管理发布说明、上传二进制文件/工件、下载发布文件或查看发布历史等场景。它会根据发布事件（如版本更新、标签变更、发布操作、发布说明的更新或发布文件的下载等）自动触发相应的操作。
---

# glab 发布版

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

有关 `--help` 命令的完整输出，请参阅 [references/commands.md](references/commands.md)。