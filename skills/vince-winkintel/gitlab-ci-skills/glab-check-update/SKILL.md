---
name: glab-check-update
description: **使用说明：**  
在配合 `glab check-update` 命令使用时，请遵循以下规则：
---

# glab check-update

## 概述

```

  Checks for the latest version of glab available on GitLab.com.                                                        
                                                                                                                        
  When run explicitly, this command always checks for updates regardless of when the last check occurred.               
                                                                                                                        
  When run automatically after other glab commands, it checks for updates at most once every 24 hours.                  
                                                                                                                        
  To disable the automatic update check entirely, run 'glab config set check_update false'.                             
  To re-enable the automatic update check, run 'glab config set check_update true'.                                     
                                                                                                                        
         
  USAGE  
         
    glab check-update [--flags]  
         
  FLAGS  
         
    -h --help  Show help for this command.
```

## 快速入门

```bash
glab check-update --help
```

## 子命令

该命令没有子命令。