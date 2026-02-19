---
name: ztm-tunnel
description: "在 ZTM 网络端点之间创建和管理 TCP/UDP 隧道。通过这种方式，可以在 ZTM 网状网络中实现安全的点对点（P2P）端口转发。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔌",
        "requires":
          {
            "bins": ["ztm"],
            "services": ["ztm-agent"],
          },
        "install":
          [
            {
              "id": "download",
              "kind": "download",
              "label": "Download ZTM from GitHub releases",
              "url": "https://github.com/flomesh-io/ztm/releases",
            },
          ],
        "env":
          {
            "ZTM_AGENT": "http://localhost:7777",
          },
        "config":
          {
            "path": "~/.ztm.conf",
            "fields":
              {
                "agent": "ZTM Agent URL (default: localhost:7777)",
                "mesh": "Default mesh name",
              },
          },
      },
  }
---
# ZTM隧道功能

用于在ZTM网络终端之间创建和管理TCP/UDP隧道。

## 前提条件

1. **必须运行ZTM代理**  
   ```bash
   ztm start agent
   ```

2. **必须加入网状网络**  
   ```bash
   ztm join <mesh-name> --as <your-endpoint-name> --permit <permit-file.json>
   ```

3. **必须安装隧道应用程序**  
   ```bash
   ztm app install tunnel
   ```

## 概念

- **入站（Inbound）**：本地终端，用于监听连接并将其转发给远程终端。
- **出站（Outbound）**：远程终端，用于接收连接并将其转发到目标服务。
- **隧道（Tunnel）**：由入站和出站连接组成的完整通信路径。

## 列出隧道

- 列出网状网络中的所有隧道：  
   ```bash
ztm tunnel get tunnel
```

- 列出入站隧道（本地监听端口）：  
   ```bash
ztm tunnel get inbound
```

- 列出出站隧道（远程目标）：  
   ```bash
ztm tunnel get outbound
```

## 创建隧道

### 情景：将本地服务暴露给另一个终端

**步骤1：在远程终端（出站端）**，指定目标服务：  
   ```bash
ztm tunnel open outbound my-tunnel --targets 192.168.1.100:8080
```

**步骤2：在本地终端（入站端）**，设置端口转发：  
   ```bash
ztm tunnel open inbound my-tunnel --listen 0.0.0.0:9000 --exits <remote-endpoint-id>
```

这样会创建一个隧道：
- 本地端口`9000`用于监听连接。
- 连接会被转发到远程终端。
- 远程终端会将连接转发到`192.168.1.100:8080`。

### 快速操作（两端使用相同命令）

在相应终端上运行以下命令即可同时创建两端：  
```bash
# On endpoint A (listening side)
ztm tunnel open inbound tunnel-name --listen 0.0.0.0:9000 --exits <endpoint-B-id>

# On endpoint B (target side) 
ztm tunnel open outbound tunnel-name --targets 127.0.0.1:8080
```

## 删除隧道

- 关闭入站端：  
   ```bash
ztm tunnel close inbound my-tunnel
```

- 关闭出站端：  
   ```bash
ztm tunnel close outbound my-tunnel
```

## 隧道详情

- 查看隧道详细信息：  
   ```bash
ztm tunnel describe tunnel tcp/my-tunnel
```

- 查看入站端详细信息：  
   ```bash
ztm tunnel describe inbound tcp/my-tunnel
```

- 查看出站端详细信息：  
   ```bash
ztm tunnel describe outbound tcp/my-tunnel
```

## 常见用途

- **从任何地方访问家庭服务器**  
   ```bash
# On home endpoint
ztm tunnel open inbound home-server --listen 0.0.0.0:22 --exits <office-endpoint-id>

# On office endpoint
ztm tunnel open outbound home-server --targets 192.168.1.10:22
```

- **转发Web服务**  
   ```bash
# Remote endpoint exposes local web service
ztm tunnel open outbound web-tunnel --targets 192.168.1.100:80

# Local endpoint listens on port 8080
ztm tunnel open inbound web-tunnel --listen 0.0.0.0:8080 --exits <remote-endpoint-id>
```

- **UDP隧道（用于DNS、VoIP等）**  
   ```bash
ztm tunnel open outbound dns-tunnel --targets 8.8.8.8:53
ztm tunnel open inbound dns-tunnel --listen 0.0.0.0:5300 --exits <remote-endpoint-id>
```

## 故障排除

- 检查ZTM代理是否正在运行：  
   ```bash
curl http://localhost:7777/api/status
```

- 检查网状网络状态：  
   ```bash
ztm get mesh
ztm get ep
```

- 检查已安装的应用程序：  
   ```bash
ztm get app
```

- 如果未安装隧道应用程序：  
   ```bash
ztm app install tunnel
```

- 查看隧道应用程序日志：  
   ```bash
ztm log app tunnel
```

## 配置

ZTM的命令行接口（CLI）配置存储在`~/.ztm.conf`文件中：  
```json
{
  "agent": "localhost:7777",
  "mesh": "my-mesh-name"
}
```

或者通过环境变量进行配置：  
```bash
export ZTM_AGENT=http://localhost:7777
export ZTM_MESH=my-mesh-name
```

## API参考

如需程序化访问，可以使用ZTM代理的HTTP API：  
```bash
# Get all tunnels
curl http://localhost:7777/api/meshes/{mesh}/apps/ztm/tunnel/api/tunnel

# Get inbound tunnels
curl http://localhost:7777/api/meshes/{mesh}/apps/ztm/tunnel/api/inbound

# Create inbound
curl -X POST http://localhost:7777/api/meshes/{mesh}/apps/ztm/tunnel/api/inbound/tcp/tunnel-name \
  -H "Content-Type: application/json" \
  -d '{"listens":[{"ip":"0.0.0.0","port":9000}],"exits":["endpoint-id"]}'
```