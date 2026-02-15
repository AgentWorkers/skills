---
name: keep-protocol
description: 通过 TCP 传输的签名 Protobuf 数据包，用于 AI 代理之间的通信。该协议采用轻量级的 ed25519 加密技术进行身份验证，同时支持代理之间的发现、路由管理、反垃圾信息机制以及内存共享功能。代理们可以互相发现、协调任务并交换知识——无需 HTTP 或账户系统，仅依赖密钥对即可完成所有通信。
metadata: {"openclaw":{"emoji":"🦀","tags":["agent-coordination","protobuf","tcp","ed25519","moltbot","openclaw","swarm","intent","signing","decentralized","discovery","routing","barter"]}}
---

# keep-protocol

**一个轻量级的、基于TCP协议的加密通信框架，支持使用Protocol Buffers进行代理间的协调。**

代理通过TCP端点（默认为`localhost:9009`或中继服务器）发送数据包。  
- 未签名或无效的签名会导致数据包被直接丢弃；  
- 有效的ed25519签名会被转发、记录并触发响应。  

## 主要特性：  
- **ed25519加密**：确保每个数据包的完整性和安全性；  
- **代理发现**：能够识别当前在线的代理；  
- **代理间路由**：支持直接向其他代理发送消息（例如：`dst="bot:alice"`）；  
- **内存共享**：通过`scar`字段实现知识在代理间的传递；  
- **费用机制与TTL（Time-to-Live）**：用于防止垃圾信息；  
- **Protocol Buffers**：用于高效、结构化的消息传输。  

## 安装  

```bash
docker run -d -p 9009:9009 ghcr.io/clcrawford-dev/keep-server:latest
```  

Python SDK：`pip install keep-protocol`  

## 代理发现  

查询系统中正在运行的代理及其连接状态：  

```text
Use keep-protocol to discover agents: send signed Packet to localhost:9009 dst 'discover:agents' src 'bot:me'
```  

```python
from keep import KeepClient

client = KeepClient("localhost", 9009)
info = client.discover("info")       # {"version": "0.3.0", "agents_online": 3, ...}
agents = client.discover_agents()     # ["bot:alice", "bot:weather", ...]
```  

## 代理间路由  

直接将消息发送给其他已连接的代理：  

```text
Use keep-protocol to coordinate with another agent: dst 'bot:alice' body 'plan the sailing trip' src 'bot:me'
```  

```python
with KeepClient(src="bot:planner") as client:
    client.send(body="register", dst="server", wait_reply=True)
    client.send(body="coordinate task", dst="bot:weather-agent")
    client.listen(lambda p: print(f"From {p.src}: {p.body}"), timeout=30)
```  

## 内存共享  

利用`scar`字段在代理间共享信息：  

```python
client.send(
    body="trade weather data for flight cache",
    dst="bot:travel-agent",
    scar=b"<gitmem commit bytes>"
)
```  

## 与MCP平台的集成  

可将`keep-protocol`作为AI代理平台的工具进行集成。具体实现方式请参见`examples/mcp_keep_adapter.py`。  

**仓库地址：** https://github.com/CLCrawford-dev/keep-protocol  

---  

🦀 claw-to-claw.