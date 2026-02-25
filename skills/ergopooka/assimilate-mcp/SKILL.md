---
name: assimilate-mcp
description: **Control Assimilate Live FX / SCRATCH** — 一款专业的色彩分级、合成及虚拟制作软件，可通过 MCP（Media Control Platform）进行操作。该软件提供了涵盖14个类别的88种工具。
homepage: https://github.com/amac-roguelabs/assimilate-mcp
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["npx"]},"install":[{"id":"node","kind":"node","package":"assimilate-mcp","bins":["assimilate-mcp"],"label":"Install assimilate-mcp"}]}}
---
# 使用 MCP 集成 [Assimilate Live FX / SCRATCH](https://assimilateinc.com)  

**Assimilate Live FX / SCRATCH** 是一款专业的色彩分级、合成及虚拟制作软件。通过 MCP，您可以实现 [Assimilate REST API](https://github.com/Assimilate-Inc/Assimilate-REST) 与 14 个类别下的 88 种工具之间的完全集成。  

## 先决条件  
- 已启用 REST API 的 [Assimilate Live FX 或 SCRATCH](https://assimilateinc.com)  
- [Node.js](https://nodejs.org) v18+  
- 已启用 Live FX 的 HTTP 服务器：**系统设置 → 通用 → 启用 HTTP 服务器**（默认端口为 8080）  

## 设置  

### MCPorter  
（相关代码块请参见：```bash
mcporter config add assimilate --command npx --args '["-y", "assimilate-mcp"]'
mcporter list assimilate
```）  

### Claude Desktop  
将以下配置添加到 `claude_desktop_config.json` 文件中：  
（相关代码块请参见：```json
{
  "mcpServers": {
    "assimilate": {
      "command": "npx",
      "args": ["-y", "assimilate-mcp"]
    }
  }
}
```）  

### Claude 代码  
（相关代码块请参见：```bash
claude mcp add assimilate -- npx -y assimilate-mcp
```）  

## 配置参数  
| 参数 | 环境变量 | 默认值 | 说明 |  
|------|---------|---------|-------------|  
| `--host` | `ASSIMILATE_HOST` | `127.0.0.1` | Live FX 服务器地址 |  
| `--port` | `ASSIMILATE_PORT` | `8080` | REST API 端口 |  
| `--key` | `ASSIMILATE_KEY` | — | 认证密钥 |  
| `--timeout` | `ASSIMILATE_TIMEOUT` | `30000` | HTTP 请求超时时间（毫秒） |  

**使用自定义端口的示例：**  
（相关代码块请参见：```json
{
  "mcpServers": {
    "assimilate": {
      "command": "npx",
      "args": ["-y", "assimilate-mcp", "--port=9090"]
    }
  }
}
```）  

## 支持的工具（共 88 种）  
| 类别 | 工具数量 | 主要工具 |  
|----------|:-----:|-----------|  
| **系统** | 8 | `get_system` `check_connection` `list_users` `select_user` |  
| **项目** | 7 | `list_projects` `enter_project` `create_project` |  
| **组** | 9 | `list_groups` `get_current_group` `create_group` |  
| **构建内容** | 10 | `list_constructs` `create_construct` `enter_construct` |  
| **插槽** | 5 | `list_slots` `get_slot` `set_slot` `create_slot` |  
| **版本** | 5 | `list_versions` `get_version` `set_version` |  
| **镜头** | 7 | `get_shot` `set_shot` `create_shot` `import_media` |  
| **输入** | 4 | `get_inputs` `get_input` `set_input` |  
| **色彩分级** | 5 | `get_grade` `set_grade` `get_framing` `set_framing` |  
| **播放器** | 8 | `enter_timeline` `set_playmode` `enter_shot` `exit_player` |  
| **渲染** | 10 | `start_render` `stop_render` `get_render_status` |  
| **输出** | 6 | `list_outputs` `create_output` `set_output` |  
| **快照** | 2 | `render_snapshot` `get_shot_metadata` |  
| **文件** | 2 | `list_directory` `find_media` |  

## 使用示例  
您可以使用自然语言与 AI 助手进行交互：  
- “有哪些项目可用？”  
- “从 /Volumes/Shuttle/Day_14 目录导入 ARRIRAW 文件。”  
- “调整这个镜头的伽马值。”  
- “设置 ProRes 4444 格式并渲染时间线。”  
- “截取这帧的快照。”  

### MCPorter 命令行界面（CLI）  
（相关代码块请参见：```bash
mcporter call assimilate.check_connection
mcporter call assimilate.list_projects
mcporter call 'assimilate.enter_project(name: "Commercial_Nike_Q3")'
mcporter call assimilate.get_grade
```）  

## 远程访问  
Live FX 默认接受本地主机（localhost）的连接。如需远程访问，请使用 SSH 隧道：  
（相关代码块请参见：```bash
ssh -f -N -L 8080:127.0.0.1:8080 user@livefx-host
```）  

## 链接  
- [GitHub](https://github.com/amac-roguelabs/assimilate-mcp)  
- [npm](https://www.npmjs.com/package/assimilate-mcp)  
- [Assimilate REST API](https://github.com/Assimilate-Inc/Assimilate-REST)  
- [Assimilate Inc](https://assimilateinc.com)