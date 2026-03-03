---
name: glab-mcp
description: 与 Model Context Protocol (MCP) 服务器协作，以实现 AI 助手的集成。该协议将 GitLab 的功能暴露为工具，供 AI 助手（如 Claude Code）使用，以便与项目、问题、合并请求以及管道进行交互。在将 AI 助手与 GitLab 集成或与 MCP 服务器配合使用时，请使用此协议。触发条件包括：MCP、Model Context Protocol、AI 助手集成以及 glab mcp serve 的相关操作。
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

## v1.86.0 的变更

### 自动启用 JSON 输出
从 v1.86.0 开始，`glab mcp serve` 在运行时会自动启用 JSON 输出格式——无需手动设置标志。这提高了 AI 助手解析 MCP 服务器工具响应的可靠性。

### 未添加注释的命令将被排除
缺少 MCP 注释的命令将不再被视为 MCP 工具。这意味着只有明确支持的命令才会被提供给 AI 助手使用，从而减少了干扰并提高了可靠性。如果您期望的 GitLab 操作没有作为 MCP 工具提供，可能是因为当前版本中缺少相应的 MCP 注释。

## 子命令

有关完整的 `--help` 输出信息，请参阅 [references/commands.md](references/commands.md)。