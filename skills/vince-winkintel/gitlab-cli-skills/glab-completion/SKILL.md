---
name: glab-completion
description: 生成适用于 Bash、Zsh、Fish 或 PowerShell 的 shell 完成脚本。这些脚本可用于在您的 shell 中设置 Glab 自动补全功能。它们会在补全操作发生时被触发，实现自动补全和 tab 键补全功能。
---

# glab 完成补全功能

## 概述

```

  This command outputs code meant to be saved to a file, or immediately                                                 
  evaluated by an interactive shell. To load completions:                                                               
                                                                                                                        
  ### Bash                                                                                                              
                                                                                                                        
  To load completions in your current shell session:                                                                    
                                                                                                                        
  ```shell                                                                                                              
  source <(glab completion -s bash)                                                                                     
  ```                                                                                                                   
                                                                                                                        
  要在每个新会话中加载补全功能，请运行此命令一次：                                                 
                                                                                                                        
  #### Linux                                                                                                            
                                                                                                                        
  ```shell                                                                                                              
  glab completion -s bash > /etc/bash_completion.d/glab                                                                 
  ```                                                                                                                   
                                                                                                                        
  #### macOS                                                                                                            
                                                                                                                        
  ```shell                                                                                                              
  glab completion -s bash > /usr/local/etc/bash_completion.d/glab                                                       
  ```                                                                                                                   
                                                                                                                        
  ### Zsh                                                                                                               
                                                                                                                        
  如果您的环境中尚未启用 shell 完成补全功能，您需要先启用它。运行此命令一次：                                                                                 
                                                                                                                        
  ```shell                                                                                                              
  echo "autoload -U compinit; compinit" >> ~/.zshrc                                                                     
  ```                                                                                                                   
                                                                                                                        
  要在当前 shell 会话中加载补全功能：                                                                    
                                                                                                                        
  ```shell                                                                                                              
  source <(glab completion -s zsh); compdef _glab glab                                                                  
  ```                                                                                                                   
                                                                                                                        
  要在每个新会话中加载补全功能，请运行此命令一次：                                                 
                                                                                                                        
  #### Linux                                                                                                            
                                                                                                                        
  ```shell                                                                                                              
  glab completion -s zsh > "${fpath[1]}/_glab"                                                                          
  ```                                                                                                                   
                                                                                                                        
  #### macOS                                                                                                            
                                                                                                                        
  对于较旧版本的 macOS，您可能需要运行以下命令：                                                             
                                                                                                                        
  ```shell                                                                                                              
  glab completion -s zsh > /usr/local/share/zsh/site-functions/_glab                                                    
  ```                                                                                                                   
                                                                                                                        
  使用 Homebrew 安装的 glab 会自动配置补全功能。                                                
                                                                                                                        
  ### fish                                                                                                              
                                                                                                                        
  要在当前 shell 会话中加载补全功能：                                                                    
                                                                                                                        
  ```shell                                                                                                              
  glab completion -s fish | source                                                                                      
  ```                                                                                                                   
                                                                                                                        
  要在每个新会话中加载补全功能，请运行此命令一次：                                                 
                                                                                                                        
  ```shell                                                                                                              
  glab completion -s fish > ~/.config/fish/completions/glab.fish                                                        
  ```                                                                                                                   
                                                                                                                        
  ### PowerShell                                                                                                        
                                                                                                                        
  要在当前 shell 会话中加载补全功能：                                                                    
                                                                                                                        
  ```shell                                                                                                              
  glab completion -s powershell | Out-String | Invoke-Expression                                                        
  ```                                                                                                                   
                                                                                                                        
  要在每个新会话中加载补全功能，请将上述命令的输出添加到您的 PowerShell 配置文件中。                                                                                           
                                                                                                                        
  但是，如果您是通过包管理器安装 glab 的，可能不需要再进行额外的 shell 配置。                                                                      
  关于 Homebrew 的使用方法，请参阅 [brew shell completion](https://docs.brew.sh/Shell-Completion)                                      
                                                                                                                        
         
  **用法**  
         
    glab completion [--flags]  
         
  **参数说明**  
         
    -h        --help     显示此命令的帮助信息。  
    --no-desc    不显示 shell 完成补全功能的描述。  
    -s        --shell     指定 shell 类型：bash、zsh、fish、powershell。（默认值为 bash）  
```

## Quick start

```bash
glab completion --help
```

## 子命令  
   
此命令没有子命令。