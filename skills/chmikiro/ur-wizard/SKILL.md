---
name: ur-wizard
description: URnetwork Wizard——一个功能齐全的去中心化隐私网络工具，支持创建HTTPS/SOCKS/WireGuard代理（消费者模式），同时通过提供出站带宽来赚取奖励（提供者模式）。适用于需要匿名上网、设置VPN连接、使用代理进行数据抓取，或运行提供者节点以获取USDC收益的场景。该工具前身为proxy-vpn，现已拥有完整的官方文档支持。
---
# URnetwork（代理VPN）技能

URnetwork是一个去中心化的隐私网络，用户可以在其中：
1. **作为消费者**：使用该网络通过HTTPS/SOCKS/WireGuard代理进行安全、匿名的互联网访问；
2. **作为提供者**：共享出站带宽并赚取奖励（以USDC形式支付）。

**官方文档：** https://docs.ur.io

## 终端点

| 服务 | URL |
|---------|-----|
| API | https://api.bringyour.com |
| MCP服务器 | https://mcp.bringyour.com |
| API规范 | https://github.com/urnetwork/connect/blob/main/api/bringyour.yml |
| Web UI | https://ur.io |

---

## 认证

所有API调用都需要在`Authorization`头部包含一个JWT令牌：

```bash
# Get auth code from human (from https://ur.io web UI)
# Then exchange for JWT:
curl -X POST https://api.bringyour.com/auth/code-login \
  -d '{"auth_code": "<AUTH CODE>"}' | jq ".by_jwt"
```

请妥善保存JWT令牌并重复使用。如需刷新令牌，请获取新的认证代码并重新执行操作。

---

## 消费者模式：创建代理

### 代理类型

| 使用场景 | 协议 | 配置来源 |
|----------|----------|---------------|
| **网页爬取/浏览** | HTTPS | `proxy_config_result.https_proxy_url` |
| **低级套接字/UDP** | SOCKS5 | `proxy_config_result.socks_proxy_url` |
| **系统级/操作系统级** | WireGuard | `proxy_config_result.wg_config.config` |

**SOCKS5注意事项：** 使用`access_token`作为用户名，密码为空。支持SOCKS5H（远程DNS解析）。

**WireGuard注意事项：** 必须在认证客户端请求中设置`proxy_config.enable_wg: true`。

### 方法1：MCP技能（推荐）

MCP技能简化了位置搜索和代理创建流程：
1. 询问用户所需的位置（国家/地区/城市）；
2. 通过MCP搜索并创建代理；
3. 如果没有匹配项，扩大搜索范围（从城市到地区再到国家）；
4. 如果仍然没有匹配项，显示可用的前10个国家。

### 方法2：按国家查询API

```bash
# Step 1: Find locations
curl -X POST -H 'Authorization: Bearer <JWT>' \
  https://api.bringyour.com/network/find-locations \
  -d '{"query": "Germany"}' | jq '.locations'

# Step 2: Note country_code (e.g., "DE")

# Step 3: Create proxy
curl -X POST -H 'Authorization: Bearer <JWT>' \
  https://api.bringyour.com/network/auth-client \
  -d '{
    "proxy_config": {
      "initial_device_state": {
        "country_code": "DE"
      }
    }
  }'
```

### 方法3：按位置ID查询API

```bash
# Step 1: Find locations
curl -X POST -H 'Authorization: Bearer <JWT>' \
  https://api.bringyour.com/network/find-locations \
  -d '{"query": "Berlin"}' | jq '.locations'

# Step 2: Note location_id

# Step 3: Create proxy with specific location
curl -X POST -H 'Authorization: Bearer <JWT>' \
  https://api.bringyour.com/network/auth-client \
  -d '{
    "proxy_config": {
      "initial_device_state": {
        "location": {
          "connect_location_id": {
            "location_id": "<LOCATION_ID>"
          }
        }
      }
    }
  }'
```

### 方法4：查询出站IP

用于在某个位置轮换使用多个提供者：

```bash
# Step 1-2: Get location_id as above

# Step 3: Find providers (egress IPs) for location
curl -X POST -H 'Authorization: Bearer <JWT>' \
  https://api.bringyour.com/network/find-providers2 \
  -d '{
    "specs": [{"client_id": "<CLIENT_ID>"}],
    "count": 10
  }' | jq '.providers'

# Step 4: Create proxy for each client_id
curl -X POST -H 'Authorization: Bearer <JWT>' \
  https://api.bringyour.com/network/auth-client \
  -d '{
    "proxy_config": {
      "initial_device_state": {
        "location": {
          "connect_location_id": {
            "client_id": "<CLIENT_ID>"
          }
        }
      }
    }
  }'
```

### 地理位置类型

搜索时，可以通过`location_type`进行过滤：
| 类型 | 描述 |
|------|-------------|
| `country` | 国家 |
| `region` | 州、省、大都市区 |
| `city` | 城市 |

---

## 提供者模式：通过共享带宽赚钱

### 高级选项：通过Shadowsocks代理作为提供者

### 高级选项：通过SOCKS5代理作为提供者（透明路由）

通过上游的SOCKS5代理运行URnetwork提供者，以增加匿名性或匹配特定的出站IP。

**架构：**
```
┌─────────────────────────────────────────┐
│        URnetwork Provider Container     │
│  ┌──────────────┐  ┌──────────────┐    │
│  │ Provider     │──│ Redsocks     │────┼───▶ Upstream SOCKS5
│  │ (egress)     │  │ (iptables)   │    │    (residential/datacenter)
│  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────┘
```

**Dockerfile设置：**

```dockerfile
FROM bringyour/community-provider:g4-latest

USER root
RUN apt-get update && apt-get install -y redsocks iptables supervisor curl

# Copy configs
COPY redsocks.conf /etc/redsocks/redsocks.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY start-proxied.sh /usr/local/bin/start-proxied.sh
RUN chmod +x /usr/local/bin/start-proxied.sh

EXPOSE 80
ENTRYPOINT ["/usr/local/bin/start-proxied.sh"]
```

**redsocks.conf：**
```
base {
    log_debug = off;
    log_info = on;
    daemon = off;
    redirector = iptables;
}

redsocks {
    local_ip = 0.0.0.0;
    local_port = 12345;
    ip = <SOCKS5_PROXY_IP>;
    port = <SOCKS5_PROXY_PORT>;
    type = socks5;
    login = "<USERNAME>";
    password = "<PASSWORD>";
}
```

**start-proxied.sh：**
```bash
#!/bin/bash
set -e

# Configure iptables to redirect all TCP through redsocks
iptables -t nat -N REDSOCKS 2>/dev/null || true
iptables -t nat -F REDSOCKS 2>/dev/null || true

# Exclude local networks and proxy server
iptables -t nat -A REDSOCKS -d <SOCKS5_PROXY_IP> -j RETURN
iptables -t nat -A REDSOCKS -d 0.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 10.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 127.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 172.16.0.0/12 -j RETURN
iptables -t nat -A REDSOCKS -d 192.168.0.0/16 -j RETURN

# Redirect to redsocks
iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports 12345
iptables -t nat -A OUTPUT -p tcp -j REDSOCKS

# Start supervisor (manages redsocks + provider)
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
```

**运行容器：**
```bash
docker run --name urnetwork-proxied \
  --cap-add=NET_ADMIN \
  --mount type=bind,source=$HOME/.urnetwork,target=/root/.urnetwork \
  --restart always \
  -d urnetwork-proxied:latest
```

**要求：**
- `--cap-add=NET_ADMIN`（用于iptables）
- 将相同的JWT文件挂载到`/root/.urnetwork/jwt`
- 容器使用supervisor来管理redsocks和提供者服务

**验证：**
```bash
# Check egress IP from inside container
docker exec urnetwork-proxied curl -s http://ipinfo.io/ip
# Should match your SOCKS5 proxy IP
```

**弹性机制：**
- 提供者在故障时自动重启；
- Redsocks通过supervisor自动重启；
- 容器设置为`--restart always`以确保持续运行；
- 重试机制能够优雅地处理代理中断。

---

### 标准提供者模式：通过共享带宽赚钱

### 什么是提供者？

提供者与URnetwork共享出站带宽（互联网连接）。用户通过提供者连接以安全地访问互联网。提供者因参与其中而获得USDC奖励。

**奖励结构：**
- 高级会员收入的10% + 每月活跃用户（MAU）至少0.10美元；
- 推荐奖励：推荐用户收入的50%加上推荐者奖励的50%；
- 奖励以USDC形式在Polygon或Solana平台上发放；
- 每周进行一次奖励结算。

### 安装方法

#### 选项1：Linux的一行安装命令

```bash
curl -fSsL https://raw.githubusercontent.com/urnetwork/connect/refs/heads/main/scripts/Provider_Install_Linux.sh | sh
```

**卸载：**
```bash
curl -fSsL https://raw.githubusercontent.com/urnetwork/connect/refs/heads/main/scripts/Provider_Uninstall_Linux.sh | sh
```

#### 选项2：Windows（PowerShell）

```powershell
powershell -c "irm https://raw.githubusercontent.com/urnetwork/connect/refs/heads/main/scripts/Provider_Install_Win32.ps1 | iex"
```

**卸载：**
```powershell
powershell -c "irm https://raw.githubusercontent.com/urnetwork/connect/refs/heads/main/scripts/Provider_Uninstall_Win32.ps1 | iex"
```

#### 选项3：从源代码构建

```bash
mkdir urnetwork && cd urnetwork
git clone https://github.com/urnetwork/connect
git clone https://github.com/urnetwork/protocol
cd connect/provider
go build  # Binary at ./provider
```

#### 选项4：Docker容器

可用镜像：`bringyour/community-provider:g1-latest`至`g4-latest`（g4是最稳定的版本）

```bash
# Initialize (first time)
docker run --mount type=bind,source=$HOME/.urnetwork,target=/root/.urnetwork \
  bringyour/community-provider:g4-latest auth

# Run provider
docker run --mount type=bind,source=$HOME/.urnetwork,target=/root/.urnetwork \
  --restart no -d bringyour/community-provider:g4-latest provide
```

### 设置提供者

1. **获取认证代码：**
   - 访问https://ur.io
   - 注册并登录网络
   - 点击“复制认证代码”

2. **进行认证：**
   ```bash
   ./provider auth
   # Paste auth code when prompted
   # Saved to ~/.urnetwork/jwt
   ```

3. **运行提供者：**
   ```bash
   ./provider provide
   # "Provider XXX started"
   ```

4. **在应用中设置钱包**以接收奖励（奖励以Polygon/Solana货币支付）

### 作为后台服务运行

**Linux（systemd）：**
```bash
systemctl --user start urnetwork    # Start
systemctl --user stop urnetwork     # Stop
systemctl --user enable urnetwork   # Auto-start on login
systemctl --user disable urnetwork  # Disable auto-start
```

**macOS（launchd）：**
```bash
# Download launchd template from GitHub
# Edit paths and user
sudo cp urnetwork-provider.plist /Library/LaunchAgents/
sudo launchctl load /Library/LaunchAgents/urnetwork-provider.plist
sudo launchctl start /Library/LaunchAgents/urnetwork-provider.plist

# Check logs
tail -f /var/log/system.log | grep -i provider
```

**Windows：**
- 安装程序会询问是否启动该服务；
- 或者手动在后台运行：

```powershell
powershell -NoProfile -WindowStyle Hidden -Command \
  "Start-Process urnetwork.exe -ArgumentList 'provide' -WindowStyle Hidden"
```

### 多平台构建

可以为多种架构构建提供者服务：

```bash
cd connect/provider
make build

# Outputs to:
# build/darwin/amd64/provider
# build/darwin/arm64/provider
# build/linux/amd64/provider
# build/linux/arm64/provider
# build/linux/arm/provider
# build/linux/386/provider
# build/windows/amd64/provider
# build/windows/arm64/provider
```

或者从夜间版本下载预构建的二进制文件。

---

## 其他命令行工具（CLIs）

| CLI | 功能 |
|-----|---------|
| `provider` | 运行出站提供者服务（赚取奖励） |
| `tether` | 管理网络接口和协议服务器（数据包路由） |
| `bringyourctl` | 管理自己的网络空间部署 |
| `warpctl` | 实现持续的网络空间部署 |

---

## 信任与安全

- 提供者需遵守信任和安全规则；
- 网络服务免费，但数据使用量有限制；
- 支持电子邮件、短信、Google和Apple身份验证；
- 支付完成后会立即删除用户信息（保留1周）。

## 经济模型概述

**对于用户：**
- 免费 tier，数据使用量有限制；
- 高级会员：每月约5美元，享受更高的数据使用量和优先服务。

**对于提供者：**
- 收入的10%作为奖励；
- 每月活跃用户（MAU）至少获得0.10美元；
- 最多20%的收入会回馈给社区；
- 推荐用户可获得50%的推荐奖励；
- 目标利润率：在规模扩大后达到70-80%。

**公司发展阶段：**
1. 第0阶段：构建可扩展的网络；
2. 第1阶段：在4%的会员转化率下实现盈亏平衡；
3. 第2阶段：在固定成本下扩大规模；
4. 第3阶段：实现盈利扩张。

## 快速参考

**获取JWT令牌：**
```bash
curl -X POST https://api.bringyour.com/auth/code-login \
  -d '{"auth_code": "<CODE>"}' | jq ".by_jwt"
```

**查找位置：**
```bash
curl -X POST -H 'Authorization: Bearer <JWT>' \
  https://api.bringyour.com/network/find-locations \
  -d '{"query": "Germany"}' | jq '.locations'
```

**创建代理：**
```bash
curl -X POST -H 'Authorization: Bearer <JWT>' \
  https://api.bringyour.com/network/auth-client \
  -d '{"proxy_config": {"initial_device_state": {"country_code": "DE"}}}'
```

**安装提供者：**
```bash
curl -fSsL https://raw.githubusercontent.com/urnetwork/connect/refs/heads/main/scripts/Provider_Install_Linux.sh | sh
```

---

## 路由器/物联网平台

- **Raspberry Pi：** 请参阅文档；
- **Ubiquiti EdgeOS：** 请参阅文档；
- **MikroTik RouterOS：** 请参阅文档。

所有这些平台都支持提供者服务的部署。

### 高级选项：通过Shadowsocks代理作为提供者

通过Shadowsocks代理运行URnetwork提供者，以增强隐私性或实现特定的出站路由。

**Shadowsocks与SOCKS5的比较：**
- Shadowsocks使用加密技术（如AES-256-GCM）——更难被检测或阻止；
- 更适合绕过防火墙（例如在中国或企业网络中）；
- 比纯SOCKS5稍显复杂一些。

**架构：**
```
┌─────────────────────────────────────────┐
│        URnetwork Provider Container     │
│  ┌──────────────┐  ┌──────────────┐    │
│  │ Provider     │──│ ss-local     │────┼───▶ Shadowsocks Server
│  │ (egress)     │  │ (SOCKS5:1080)│    │    (encrypted tunnel)
│  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────┘
```

**Shadowsocks配置格式：**
```
Shadowsocks/proxy/server/port/method/country/password

Example:
Shadowsocks/proxy/138.249.106.2/64619/aes-256-gcm/France/NedyYDqp
```

**Dockerfile设置：**

```dockerfile
FROM bringyour/community-provider:g4-latest

# Install shadowsocks-libev
RUN apt-get update && apt-get install -y \
    shadowsocks-libev \
    && rm -rf /var/lib/apt/lists/*

# Copy config
COPY shadowsocks.json /etc/shadowsocks-libev/config.json

# Copy startup script
COPY start-shadowsocks.sh /start-shadowsocks.sh
RUN chmod +x /start-shadowsocks.sh

EXPOSE 1080

ENTRYPOINT ["/start-shadowsocks.sh"]
```

**shadowsocks.json：**
```json
{
    "server": "138.249.106.2",
    "server_port": 64619,
    "local_port": 1080,
    "local_address": "0.0.0.0",
    "password": "NedyYDqp",
    "timeout": 300,
    "method": "aes-256-gcm"
}
```

**start-shadowsocks.sh：**
```bash
#!/bin/bash
set -e

# Start shadowsocks client
ss-local -c /etc/shadowsocks-libev/config.json &
SS_PID=$!
echo "Shadowsocks client started (PID: $SS_PID)"

# Wait for shadowsocks to be ready
sleep 3

# Verify shadowsocks is listening
if ! netstat -tlnp 2>/dev/null | grep -q ':1080' && \
   ! ss -tlnp 2>/dev/null | grep -q ':1080'; then
    if ! pgrep -x "ss-local" > /dev/null; then
        echo "ERROR: Shadowsocks not running"
        exit 1
    fi
fi
echo "Shadowsocks proxy ready on 127.0.0.1:1080"

# Start URnetwork provider with proxy environment
export HTTP_PROXY="socks5://127.0.0.1:1080"
export HTTPS_PROXY="socks5://127.0.0.1:1080"
export ALL_PROXY="socks5://127.0.0.1:1080"

exec /usr/local/sbin/bringyour-provider provide
```

**构建镜像：**
```bash
docker build -t urnetwork-shadowsocks:latest .
```

**运行Shadowsocks提供者：**
```bash
# Create JWT directory
mkdir -p ~/.urnetwork-ss-1
echo "<JWT>" > ~/.urnetwork-ss-1/jwt

# Run container
docker run -d \
  --name urnetwork-shadowsocks-1 \
  --restart always \
  -v ~/.urnetwork-ss-1:/root/.urnetwork \
  -e WARP_ENV=community \
  urnetwork-shadowsocks:latest
```

**扩展多个提供者：**
```bash
JWT="<YOUR_JWT>"

for i in $(seq 1 10); do
  mkdir -p ~/.urnetwork-ss-$i
  echo "$JWT" > ~/.urnetwork-ss-$i/jwt
  
  docker run -d \
    --name urnetwork-shadowsocks-$i \
    --restart always \
    -v ~/.urnetwork-ss-$i:/root/.urnetwork \
    -e WARP_ENV=community \
    urnetwork-shadowsocks:latest
done
```

**验证：**
```bash
# Check container status
docker ps --filter "name=urnetwork-shadowsocks"

# Check shadowsocks logs
docker logs urnetwork-shadowsocks-1 | grep "listening"
# Should show: "listening at 0.0.0.0:1080"

# Check provider logs
docker logs urnetwork-shadowsocks-1 | grep "Provider"
# Should show: "Provider XXX started"
```

**常见的Shadowsocks配置方法：**
| 方法 | 描述 |
|--------|-------------|
| `aes-256-gcm` | 推荐使用，支持硬件加速 |
| `aes-128-gcm` | 更快，但安全性稍低 |
| `chacha20-ietf-poly1305` | 适用于移动设备/ARM处理器 |

**故障排除：**
- **401 Unauthorized**：与Shadowsocks无关，可能是URnetwork API的问题；
- **连接被拒绝**：检查Shadowsocks服务器的IP地址/端口；
- **方法不支持**：确保使用的协议与服务器配置一致。

---

## 快速参考：代理提供者

**构建镜像：**
```bash
docker build -t urnetwork-proxied:latest .
```

**运行代理提供者：**
```bash
docker run --name urnetwork-proxied \
  --cap-add=NET_ADMIN \
  --mount type=bind,source=$HOME/.urnetwork,target=/root/.urnetwork \
  --restart always \
  -d urnetwork-proxied:latest
```

**验证出站IP：**
```bash
docker exec urnetwork-proxied curl -s http://ipinfo.io/ip
```

**所需文件：**
- `Dockerfile`：用于扩展提供者镜像，包含redsocks和iptables配置；
- `redsocks.conf`：SOCKS5代理配置文件；
- `start-proxied.sh`：用于设置iptables和启动supervisor；
- `supervisord.conf`：用于管理redsocks和提供者服务。

**代理配置格式：**
```
socks5/45.91.198.75:7778/username/password
```

## Shadowsocks提供者

**构建镜像：**
```bash
docker build -t urnetwork-shadowsocks:latest .
```

**运行Shadowsocks提供者：**
```bash
docker run -d \
  --name urnetwork-shadowsocks-1 \
  --restart always \
  -v ~/.urnetwork-ss-1:/root/.urnetwork \
  -e WARP_ENV=community \
  urnetwork-shadowsocks:latest
```

**Shadowsocks配置格式：**
```
Shadowsocks/proxy/server/port/method/country/password

Example:
Shadowsocks/proxy/138.249.106.2/64619/aes-256-gcm/France/NedyYDqp
```

**所需文件：**
- `Dockerfile`：用于扩展提供者镜像，包含shadowsocks库；
- `shadowsocks.json`：Shadowsocks客户端配置文件；
- `start-shadowsocks.sh`：用于启动Shadowsocks服务。

## 提供者监控

### 快速状态检查**

```bash
# All URnetwork containers
docker ps --format "table {{.Names}}\t{{.Status}}" | grep urnetwork

# Count by type
docker ps --format "{{.Names}}" | grep -c "urnetwork-provider"
docker ps --format "{{.Names}}" | grep -c "urnetwork-proxied"
docker ps --format "{{.Names}}" | grep -c "urnetwork-shadowsocks"
```

**验证提供者是否实际在运行：**

**检查认证错误：**
```bash
# Count "Unauthorized" errors in logs
docker logs urnetwork-provider-1 2>&1 | grep -c "Unauthorized"

# Check recent restarts
docker ps --format "table {{.Names}}\t{{.Status}}" | grep urnetwork-provider

# "Up X minutes" = healthy, "Restarting" = auth/connection issues
```

**检查提供者的运行日志：**
```bash
# Good: "Provider XXX started" without errors
docker logs urnetwork-proxied-1 2>&1 | grep "Provider.*started"

# Bad: Stack traces with "401 Unauthorized"
docker logs urnetwork-provider-1 2>&1 | tail -20
```

**提供者健康状况检查脚本：**
```bash
#!/bin/bash
echo "=== URnetwork Provider Health ==="
for container in $(docker ps -a --format "{{.Names}}" | grep urnetwork | sort); do
  status=$(docker ps --filter "name=$container" --format "{{.Status}}")
  errors=$(docker logs $container 2>&1 | grep -c "Unauthorized" || echo "0")
  if echo "$status" | grep -q "Restarting"; then
    echo "❌ $container: $status (Errors: $errors)"
  else
    echo "✅ $container: $status"
  fi
done
```

## 多VPS部署**

### 架构模式**

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   VPS 1 (Host)  │  │   VPS 2 (DE)    │  │   VPS 3 (US)    │
│  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │
│  │ Providers │  │  │  │ Providers │  │  │  │ Providers │  │
│  │ (10 reg)  │  │  │  │ (10 reg)  │  │  │  │ (10 reg)  │  │
│  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │
│  ┌───────────┐  │  │                 │  │                 │
│  │ Proxied   │  │  │                 │  │                 │
│  │ (10 sock) │  │  │                 │  │                 │
│  └───────────┘  │  │                 │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                    │
         └────────────────────┴────────────────────┘
                              │
                    Single JWT on each VPS
                    /root/.urnetwork/jwt
```

**部署步骤：**

**1. 在本地VPS上准备JWT令牌：**
```bash
# Host VPS (source of truth)
mkdir -p /root/.urnetwork
echo "<VALID_JWT>" > /root/.urnetwork/jwt
```

**2. 部署到远程VPS：**
```bash
VPS_IP="217.154.66.195"
VPS_USER="limebot"
VPS_PASS="your-password"

# Copy JWT to remote
sshpass -p "$VPS_PASS" scp /root/.urnetwork/jwt $VPS_USER@$VPS_IP:/home/$VPS_USER/.urnetwork/jwt

# SSH and create /root/.urnetwork (if needed)
sshpass -p "$VPS_PASS" ssh $VPS_USER@$VPS_IP 'sudo mkdir -p /root/.urnetwork && sudo cp /home/'$VPS_USER'/.urnetwork/jwt /root/.urnetwork/jwt'

# Launch providers on remote
sshpass -p "$VPS_PASS" ssh $VPS_USER@$VPS_IP '
  for i in $(seq 1 10); do
    docker run -d --name urnetwork-provider-vps-$i \
      -v /root/.urnetwork:/root/.urnetwork \
      --restart always \
      bringyour/community-provider:g4-latest provide
  done
'
```

**3. 扩展部署方案：**
```bash
# Launch N providers on current host
launch_providers() {
  local count=$1
  local prefix=$2
  for i in $(seq 1 $count); do
    docker run -d --name ${prefix}-$i \
      -v /root/.urnetwork:/root/.urnetwork \
      --restart always \
      bringyour/community-provider:g4-latest provide
  done
}

# Usage
launch_providers 10 "urnetwork-provider"
launch_providers 10 "urnetwork-proxied"
```

## 故障排除指南

### 401 Unauthorized错误

**症状：**
- 容器状态显示“正在重启”；
- 日志中显示“401 Unauthorized：未授权”；
- 提供者服务无法持续运行超过几秒钟。

**原因及解决方法：**

| 原因 | 解决方法 |
|-------|-----|
| JWT过期 | 从https://ur.io获取新的认证代码 |
| JWT格式错误 | 重新复制JWT令牌，确保没有多余的空白字符 |
| JWT文件位置错误 | 确保文件挂载在`/root/.urnetwork/jwt` |
| JWT权限问题 | 确保文件可读：`chmod 644 /root/.urnetwork/jwt` |

**快速修复：**
```bash
# 1. Get new auth code from https://ur.io
# 2. Exchange for JWT
curl -X POST https://api.bringyour.com/auth/code-login \
  -d '{"auth_code": "YOUR_CODE"}' | jq -r ".by_jwt" > /root/.urnetwork/jwt

# 3. Restart all providers
docker restart $(docker ps -q --filter "name=urnetwork")
```

### 重启循环**

**检查重启次数：**
```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep urnetwork
```

**常见原因：**

| 问题 | 可能原因 | 解决方法 |
|---------|--------------|----------|
| 每5-10秒重启 | JWT令牌过期 | 重新获取认证代码 |
| 每30秒重启 | SOCKS5/Shadowsocks服务器问题 | 检查相关配置 |
| 运行数小时后重启 | 网络不稳定 | 确保设置了`--restart always`选项 |

**调试重启循环：**
```bash
# Watch real-time logs
docker logs -f urnetwork-provider-1

# Check exit code
docker inspect urnetwork-provider-1 --format='{{.State.ExitCode}}'
```

### 代理连接问题**

**症状：**
- Shadowsocks日志显示连接被拒绝；
- Redsocks无法连接到上游服务器；
- 出站IP与预期代理IP不匹配。

**诊断方法：**
```bash
# Test SOCKS5 proxy manually
curl -x socks5://username:password@proxy_ip:port http://ipinfo.io/ip

# Check shadowsocks is listening
docker exec urnetwork-shadowsocks-1 ss -tlnp | grep 1080

# Verify iptables rules (for proxied containers)
docker exec urnetwork-proxied-1 iptables -t nat -L REDSOCKS
```

**修复代理配置：**
```bash
# Update shadowsocks.json and rebuild
docker build -t urnetwork-shadowsocks:latest .
docker restart urnetwork-shadowsocks-{1..10}
```

### 容器无法启动**

**检查：**
```bash
# Port conflicts
docker logs urnetwork-provider-1 2>&1 | grep "bind"

# Mount issues
docker logs urnetwork-provider-1 2>&1 | grep "mount"

# Disk space
df -h

# Docker daemon
docker system info
```

### 批量操作**

**重启所有提供者：**
```bash
docker restart $(docker ps -q --filter "name=urnetwork")
```

**停止所有提供者：**
```bash
docker stop $(docker ps -q --filter "name=urnetwork")
```

**删除所有提供者：**
```bash
docker rm -f $(docker ps -aq --filter "name=urnetwork")
```

**查看所有日志：**
```bash
for c in $(docker ps --format "{{.Names}}" | grep urnetwork); do
  echo "=== $c ==="
  docker logs $c 2>&1 | tail -5
done
```

## 完整文档：** https://docs.ur.io