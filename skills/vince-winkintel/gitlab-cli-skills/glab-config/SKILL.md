---
name: glab-config
description: 管理 glab CLI 的配置设置，包括默认值、偏好设置以及针对每个主机的自定义设置。该工具可用于配置 glab 的行为、设置默认值或查看当前的配置信息。相关关键词包括：config、configuration、settings、glab settings、set default。
---

# glab 配置

## 概述

```

  Manage key/value strings.                                                                                             
                                                                                                                        
  Current respected settings:                                                                                           
                                                                                                                        
  - browser: If unset, uses the default browser. Override with environment variable $BROWSER.                           
  - check_update: If true, notifies of new versions of glab. Defaults to true. Override with environment variable       
  $GLAB_CHECK_UPDATE.                                                                                                   
  - display_hyperlinks: If true, and using a TTY, outputs hyperlinks for issues and merge request lists. Defaults to    
  false.                                                                                                                
  - editor: If unset, uses the default editor. Override with environment variable $EDITOR.                              
  - glab_pager: Your desired pager command to use, such as 'less -R'.                                                   
  - glamour_style: Your desired Markdown renderer style. Options are dark, light, notty. Custom styles are available    
  using [glamour](https://github.com/charmbracelet/glamour#styles).                                                     
  - host: If unset, defaults to `https://gitlab.com`.                                                                   
  - token: Your GitLab access token. Defaults to environment variables.                                                 
  - visual: Takes precedence over 'editor'. If unset, uses the default editor. Override with environment variable       
  $VISUAL.                                                                                                              
                                                                                                                        
         
  USAGE  
         
    glab config [command] [--flags]  
            
  COMMANDS  
            
    edit [--flags]               Opens the glab configuration file.
    get <key> [--flags]          Prints the value of a given configuration key.
    set <key> <value> [--flags]  Updates configuration with the value of a given key.
         
  FLAGS  
         
    -g --global                  Use global config file.
    -h --help                    Show help for this command.
```

## 快速入门

```bash
glab config --help
```

## 子命令

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。