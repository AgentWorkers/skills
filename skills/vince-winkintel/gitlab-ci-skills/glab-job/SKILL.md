---
name: glab-job
description: **使用说明：**  
在处理 Glab 的作业命令时，请参考以下说明。
---

# glab job

## 概述

```

  Work with GitLab CI/CD jobs.                                                                                          
         
  USAGE  
         
    glab job <command> [command] [--flags]  
            
  COMMANDS  
            
    artifact <refName> <jobName> [--flags]  Download all artifacts from the last pipeline.
         
  FLAGS  
         
    -h --help                               Show help for this command.
    -R --repo                               Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab job --help
```

## 子命令

有关完整的 `--help` 命令帮助信息，请参阅 [references/commands.md](references/commands.md)。