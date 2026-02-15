---
name: glab-mcp
description: 管理 GitLab Managed Cluster Platform (MCP) 的资源与配置。适用于处理 MCP 部署、管理平台资源或配置托管集群的场景。相关操作会在 MCP、托管集群平台或平台资源层面触发。
---

# glab mcp

## 概述

```

  Manage Model Context Protocol server features for GitLab integration.                                                 
                                                                                                                        
  The MCP server exposes GitLab features as tools for use by                                                            
  AI assistants (like Claude Code) to interact with GitLab projects, issues,                                            
  merge requests, pipelines, and other resources.                                                                       
                                                                                                                        
  This feature is experimental. It might be broken or removed without any prior notice.                                 
  Read more about what experimental features mean at                                                                    
  https://docs.gitlab.com/policy/development_stages_support/                                                            
                                                                                                                        
  Use experimental features at your own risk.                                                                           
                                                                                                                        
         
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

有关完整的 `--help` 命令帮助信息，请参阅 [references/commands.md](references/commands.md)。