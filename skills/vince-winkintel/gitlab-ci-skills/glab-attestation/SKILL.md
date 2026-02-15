---
name: glab-attestation
description: **使用说明：**  
在处理 glab 的认证（attestation）命令时，请参考本说明。
---

# glab 证明（Attestation）

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

有关完整的 `--help` 命令帮助信息，请参阅 [references/commands.md](references/commands.md)。