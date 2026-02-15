---
name: glab-mcp
description: 与 Model Context Protocol (MCP) 服务器配合使用，以实现 AI 助手的集成。该协议将 GitLab 的功能暴露为工具，供 AI 助手（如 Claude Code）与项目、问题、合并请求以及管道等进行交互。适用于将 AI 助手与 GitLab 集成，或在与 MCP 服务器协作时使用。相关触发事件包括 MCP、Model Context Protocol、AI 助手集成以及 glab mcp serve。
---

# glab mcp

## 概述

```

  Manage Model Context Protocol server features for GitLab integration.                                                 
                                                                                                                        
  The MCP server exposes GitLab features as tools for use by                                                            
  AI assistants (like Claude Code) to interact with GitLab projects, issues,                                            
  merge requests, pipelines, and other resources.                                                                       
                                                                                                                        
  This feature is an experiment and is not ready for production use.                                                    
  It might be unstable or removed at any time.                                                                          
  For more information, see                                                                                             
  https://docs.gitlab.com/policy/development_stages_support/.                                                           
                                                                                                                        
         
  USAGE  
         
    glab mcp <command> [command] [--flags]  
            
  EXAMPLES  
            
    $ glab mcp serve                        
            
  COMMANDS  
            
    serve      Start a MCP server with stdio transport. (EXPERIMENTAL)
         
  FLAGS  
         
    -h --help  Show help for this command.
```

## 快速入门

```bash
glab mcp --help
```

## 子命令

有关完整的 `--help` 命令输出，请参阅 [references/commands.md](references/commands.md)。