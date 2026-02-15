---

**名称：mcporter**  
**描述：** 使用 `mcporter` 命令行工具直接列出、配置、认证以及调用 MCP（Model Context Protocol）服务器/工具（支持 HTTP 或标准输入/输出方式），包括创建临时服务器、编辑配置文件以及生成对应的命令行接口（CLI）。  
**官方网站：** https://github.com/pdxfinder/mcporter  
**元数据：**  
```json
{
  "clawdbot": {
    "emoji": "🔌",
    "os": ["darwin", "linux", "windows"],
    "requires": {
      "bins": ["mcporter"]
    },
    "install": {
      "id": "brew",
      "kind": "brew",
      "formula": "pdxfinder/tap/mcporter",
      "bins": ["mcporter"],
      "label": "安装 mcporter (brew)"
    }
  }
}
```

**使用说明：**  
使用 `mcporter` 命令行工具来管理 MCP 服务器和工具。  

**系统要求：**  
- 已安装 `mcporter` 命令行工具（通过 Homebrew 安装：`brew install pdxfinder/tap/mcporter`）。  
- MCP 服务器的配置文件应保存在 `~/.config/mcporter/` 目录下。  

**常用命令：**  
- **列出已配置的服务器：** [命令示例]  
- **进行身份认证：** [命令示例]  
- **调用 MCP 工具：** [命令示例]  
- **生成命令行接口（CLI）：** [命令示例]  
- **配置管理：** [命令示例]  

**注意事项：**  
- `mcporter` 支持 HTTP 和标准输入/输出方式的 MCP 服务器。  
- 支持创建临时服务器。  
- 通过生成命令行接口（CLI），可以更方便地使用 MCP 工具。  
- 可以使用 `exec` 工具来执行 `mcporter` 命令。