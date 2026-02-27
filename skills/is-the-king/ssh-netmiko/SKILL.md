---
description: "提供了对MCP_Server_Trigger（v0.1.0）MCP服务器的访问权限。该工具提供了7个功能：  
1. **close_ssh_session**:  
   - 关闭一个当前的SSH会话。  
   - 参数：  
     - session_id: 需要关闭的会话ID。  
2. **create_ssh_session**:  
   - 显式创建一个新的SSH会话。  
   - 参数：  
     - host: 设备的IP地址或主机名。  
     - username: SSH用户名。  
     - password: SSH密码。  
     - session_id: 新会话的唯一标识符。  
     - device_type: 设备类型（例如：cisco_ios、linux）。默认值：cisco_ios。  
     - port: SSH端口。默认值：22。  
3. **execute_ssh_command**:  
   - 在远程设备上执行SSH命令。  
   - 参数：  
     - command: 要执行的命令。  
     - session_id: 会话的唯一ID（如果不存在，则会使用提供的凭据创建新会话）。  
     - host: 设备的IP地址或主机名（新会话必需）。  
     - username: SSH用户名（新会话必需）。  
     - password: SSH密码（新会话必需）。  
     - device_type: 设备类型（例如：cisco_ios、linux、juniper_junos）。默认值：cisco_ios。  
     - port: SSH端口。  
     - timeout: 命令的超时时间（可选）。  
4. **health_check**:  
   - 检查REST SSH服务的运行状态，并返回当前的服务状态。  
5. **list_active_sessions**:  
   - 列出内存中所有活动的SSH会话。  
6. **list_history_commands**:  
   - 显示特定会话中执行的命令历史记录。  
   - 参数：  
     - session_id: 要查询历史记录的会话ID。  
7. **list_history_sessions**:  
   - 列出数据库中记录的所有会话的历史记录（包括活动会话和已关闭的会话）。"
name: restssh
---
# restssh

该技能提供了对 `MCP_Server_Trigger` MCP 服务器的访问权限。

## MCP 服务器信息

- **服务器名称：** MCP_Server_Trigger
- **服务器版本：** 0.1.0
- **协议版本：** 2025-06-18
- **功能：** 提供各种工具

## 可用的工具

该技能提供了以下工具：

- **health_check**：检查 REST SSH 服务的运行状态，并返回当前的服务状态。
- **create_ssh_session**：显式创建一个新的 SSH 会话。参数：
  - `host`：设备的 IP 地址或主机名。
  - `username`：SSH 用户名。
  - `password`：SSH 密码。
  - `session_id`：新会话的唯一标识符。
  - `device_type`：设备类型（例如：cisco_ios、linux）。默认值：cisco_ios。
  - `port`：SSH 端口。默认值：22。
- **execute_ssh_command**：在远程设备上执行 SSH 命令。参数：
  - `command`：要执行的命令。
  - `session_id`：会话的唯一 ID（如果不存在，则会使用提供的凭据创建一个新的会话）。
  - `host`：设备的 IP 地址或主机名（新会话必需）。
  - `username`：SSH 用户名（新会话必需）。
  - `password`：SSH 密码（新会话必需）。
  - `device_type`：设备类型（例如：cisco_ios、linux、juniper_junos）。默认值：cisco_ios。
  - `port`：SSH 端口。默认值：22。
  - `timeout`：命令的执行超时时间（可选）。
- **list_active_sessions**：列出内存中所有活动的 SSH 会话。
- **list_history_sessions**：列出数据库中记录的所有会话历史记录，包括活动会话和已关闭的会话。
- **list_history_commands**：列出特定会话中执行的命令历史记录。参数：
  - `session_id`：要查询历史记录的会话 ID。
- **close_ssh_session**：关闭一个活动的 SSH 会话。参数：
  - `session_id`：要关闭的会话的 ID。

## 使用方法

当需要使用该 MCP 服务器提供的工具时，此技能会自动被调用。

使用此技能之前，需要全局安装 `mcp2skill`（如果尚未安装，可以从 [https://github.com/fenwei-dev/mcp2skill](https://github.com/fenwei-dev/mcp2skill) 安装）。  
- 使用 `mcp2skill --help` 查看可用的命令。
- 使用 `mcp2skill list-tools --server restssh` 列出所有工具。
- 使用 `mcp2skill call-tool --server restssh --tool <name> --args '<json>'` 调用某个工具。
- 使用 `mcp2skill update-skill --skill <skill-dir>` 检查并更新此技能（其中 `<skill-dir>` 是该技能的目录路径）。
（注意：不要使用 `generate-skill` 子命令。它不应用于技能内部。）

有关每个工具的参数和使用的详细文档，请参阅 [TOOLS.md](references/TOOLS.md)。