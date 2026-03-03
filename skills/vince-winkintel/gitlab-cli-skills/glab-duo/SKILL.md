---
name: glab-duo
description: 与 GitLab Duo AI 助手进行交互，以获取代码建议和进行聊天。适用于需要使用 AI 功能来辅助编写代码、获取代码建议或与 GitLab Duo 进行交流的场景。触发条件包括：Duo 功能被激活、AI 助手被启用、收到代码建议或进行 AI 相关的聊天操作。
---
# glab duo

## 概述

```

  Work with GitLab Duo, our AI-native assistant for the command line.                                                   
                                                                                                                        
  GitLab Duo for the CLI integrates AI capabilities directly into your terminal                                         
  workflow. It helps you retrieve forgotten Git commands and offers guidance on                                         
  Git operations. You can accomplish specific tasks without switching contexts.                                         
                                                                                                                        
         
  USAGE  
         
    glab duo <command> prompt [command] [--flags]  
            
  COMMANDS  
            
    ask <prompt> [--flags]  Generate Git commands from natural language.
         
  FLAGS  
         
    -h --help               Show help for this command.
```

## 快速入门

```bash
glab duo --help
```

## v1.87.0 的变更

### 二进制文件下载管理
从 v1.87.0 开始，`glab duo` 提供了一个 CLI 命令，用于下载和更新 GitLab Duo AI 的二进制文件。

```bash
# Download/update the Duo CLI binary
glab duo update

# Check current Duo binary version
glab duo --version
```

**使用说明：** 在升级 `glab` 之后，运行 `glab duo update` 以确保 Duo AI 的二进制文件与您的 CLI 版本相匹配。如果 `glab duo ask` 在升级后无法正常使用，通常可以通过运行此命令来解决问题。

## 子命令

有关完整的 `--help` 命令帮助信息，请参阅 [references/commands.md](references/commands.md)。