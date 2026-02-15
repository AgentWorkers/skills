---
name: glab-attestation
description: 与 GitLab 的认证机制协作，以确保软件供应链的安全性，包括对软件构件的验证及其来源的追溯。该工具可用于验证软件构件、管理认证信息，以及处理与供应链安全相关的问题。当认证机制触发时，它会自动执行构件的验证、来源追溯及供应链安全相关的检查。
---

# glab 证书（Attestation）

## 概述

```

  Manage software attestations. (EXPERIMENTAL)                                                                          
         
  USAGE  
         
    glab attestation <command> [command] [--flags]                                    
            
  EXAMPLES  
            
    # Verify attestation for the filename.txt file in the gitlab-org/gitlab project.  
    $ glab attestation verify gitlab-org/gitlab filename.txt                          
                                                                                      
    # Verify attestation for the filename.txt file in the project with ID 123.        
    $ glab attestation verify 123 filename.txt                                        
            
  COMMANDS  
            
    verify <project_id> <artifact_path>  Verify the provenance of a specific artifact or file. (EXPERIMENTAL)
         
  FLAGS  
         
    -h --help                            Show help for this command.
```

## 快速入门

```bash
glab attestation --help
```

## 子命令

有关 `--help` 命令的完整输出，请参阅 [references/commands.md](references/commands.md)。