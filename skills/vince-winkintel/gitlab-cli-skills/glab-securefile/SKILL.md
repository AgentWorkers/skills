---
name: glab-securefile
description: 用于管理 CI/CD 过程中的安全文件，包括上传、下载、列出和删除等操作。适用于存储敏感文件（如用于管道处理的文件）、管理证书或处理安全配置文件的场景。该工具会在安全文件、CI 密钥或证书发生变化时自动触发相应的操作。
---

# glab securefile

## 概述

```

  Store up to 100 files for secure use in CI/CD pipelines. Secure files are                                             
  stored outside of your project's repository, not in version control.                                                  
  It is safe to store sensitive information in these files. Both plain text                                             
  and binary files are supported, but they must be smaller than 5 MB.                                                   
                                                                                                                        
         
  USAGE  
         
    glab securefile <command> [command] [--flags]  
            
  COMMANDS  
            
    create <fileName> <inputFilePath>  Create a new project secure file.
    download <fileID> [--flags]        Download a secure file for a project.
    get <fileID>                       Get details of a project secure file. (GitLab 18.0 and later)
    list [--flags]                     List secure files for a project.
    remove <fileID> [--flags]          Remove a secure file.
         
  FLAGS  
         
    -h --help                          Show help for this command.
    -R --repo                          Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab securefile --help
```

## 子命令

有关完整的 `--help` 命令帮助信息，请参阅 [references/commands.md](references/commands.md)。