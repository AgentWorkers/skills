---
name: glab-check-update
description: 检查 `glab` CLI 的更新情况并查看最新版本信息。该命令用于判断 `glab` 是否为最新版本，或查找可用的更新内容。当 `glab` 发生更新时，会自动触发该命令以检查其版本号及 CLI 的更新情况。
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