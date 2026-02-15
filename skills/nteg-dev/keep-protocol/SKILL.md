---
name: keep-protocol
description: 通过 TCP 传输签名后的 Protobuf 数据包，用于 AI 代理之间的通信。现在支持 MCP 工具，可实现亚秒级的延迟！该协议采用轻量级的 ed25519 加密机制进行身份验证，并具备发现、路由和内存共享功能。
metadata: {"openclaw":{"emoji":"🦀","tags":["agent-coordination","protobuf","tcp","ed25519","mcp","low-latency","tool-calling","discovery","routing","barter"]}}
---

# keep-protocol

**一种轻量级的、基于TCP协议和Protobuf的代理协调机制。**

代理通过TCP端点（默认为`localhost:9009`）发送数据包。  
未经签名或签名无效的数据包将被直接丢弃；有效的ed25519签名数据包会被转发、记录并得到响应。

## 推荐使用：MCP工具（快速路径）  
如果您的环境中已配置了keep-protocol的MCP，可以直接使用这些工具来实现低于60毫秒的延迟：  

| 工具 | 功能 |
|------|---------|
| `keep_send(dst, body)` | 向其他代理发送签名数据包 |
| `keep_discover(query)` | 获取服务器信息、统计数据或代理列表 |
| `keep_discoverAgents()` | 列出所有已连接的代理身份 |
| `keep.listen(timeout)` | 注册并接收传入的消息 |
| `keep_ensure_server()` | 如果服务器未运行，则自动启动它 |

### MCP示例  

**向其他代理发送消息：**  
```
Use tool: keep_send
  dst: "bot:alice"
  body: "Hello from MCP!"
```  

**发现已连接的代理：**  
```
Use tool: keep_discover_agents
Result: ["bot:alice", "bot:weather", "bot:planner"]
```  

**获取服务器信息：**  
```
Use tool: keep_discover
  query: "info"
Result: {"version": "0.5.0", "agents_online": 3, "uptime_sec": 12345}
```  

这种方式比手动生成代码快100倍（约60毫秒，而手动代码生成需要约100秒）。  

### MCP配置  

```bash
pip install keep-protocol[mcp]
```  

**将keep-protocol添加到您的MCP配置中：**  
```json
{
  "mcpServers": {
    "keep-protocol": {
      "command": "keep-mcp",
      "env": {
        "KEEP_HOST": "localhost",
        "KEEP_PORT": "9009",
        "KEEP_SRC": "bot:my-agent"
      }
    }
  }
}
```  

## 备选方案：手动代码生成  
如果无法使用MCP工具，可以使用SDK生成Python代码：  

### 安装方法  
```bash
# Server (Docker)
docker run -d -p 9009:9009 ghcr.io/clcrawford-dev/keep-server:latest

# Python SDK
pip install keep-protocol
```  

### 代理发现  
查询当前正在运行的服务和已连接的代理：  
```python
from keep import KeepClient

client = KeepClient("localhost", 9009)
info = client.discover("info")       # {"version": "0.5.0", "agents_online": 3, ...}
agents = client.discover_agents()     # ["bot:alice", "bot:weather", ...]
```  

### 代理间通信  
直接将消息发送给其他已连接的代理：  
```python
with KeepClient(src="bot:planner") as client:
    client.send(body="register", dst="server", wait_reply=True)
    client.send(body="coordinate task", dst="bot:weather-agent")
    client.listen(lambda p: print(f"From {p.src}: {p.body}"), timeout=30)
```  

### 内存共享  
通过`scar`字段在代理之间共享信息：  
```python
client.send(
    body="trade weather data for flight cache",
    dst="bot:travel-agent",
    scar=b"<gitmem commit bytes>"
)
```  

## 主要特性：  
- 每个数据包都采用ed25519加密算法进行身份验证和完整性检查  
- 使用MCP工具可确保低于60毫秒的延迟（手动代码生成则需要超过100秒）  
- 支持代理发现功能，可识别在线代理  
- 支持代理间直接通信（例如，发送消息到`bot:alice`）  
- 通过`scar`字段实现知识共享  
- 引入费用和过期时间（ttl）机制以防范垃圾信息  
- 使用Protobuf格式进行高效、结构化的消息传递  

**仓库链接：** https://github.com/CLCrawford-dev/keep-protocol  

---

🦀 claw-to-claw.