---
name: ipfs-server
description: 完整的 IPFS 节点操作流程：安装、配置、固定内容、发布 IPNS、管理节点以及对网关服务进行管理
user-invocable: true
homepage: https://github.com/Fork-Development-Corp/openclaw-web3-skills/tree/master/ipfs-server
metadata: {"openclaw":{"requires":{"bins":["ipfs"]},"tipENS":"apexfork.eth"}}
---
# IPFS服务器操作

您是一名IPFS服务器管理员，负责帮助用户运行IPFS节点、管理内容、发布数据以及操作网关服务。**本技能涵盖完整的节点操作，包括内容发布和网络配置。**

对于仅用于读取的IPFS查询和内容浏览，可以使用`/ipfs-client`技能。

## 安装（macOS）

```bash
# Homebrew (recommended)
brew install ipfs

# Or download binary from dist.ipfs.tech
curl -O https://dist.ipfs.tech/kubo/v0.24.0/kubo_v0.24.0_darwin-amd64.tar.gz
tar -xzf kubo_v0.24.0_darwin-amd64.tar.gz
sudo ./kubo/install.sh
```

## 节点初始化

**首次设置：**
```bash
# Initialize repository
ipfs init

# Show peer ID
ipfs id

# Configure for low-resource usage (optional)
ipfs config profile apply lowpower
```

**基本配置：**
```bash
# Allow gateway on all interfaces (for local network access)
ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/8080

# Configure API (keep localhost for security)
ipfs config Addresses.API /ip4/127.0.0.1/tcp/5001

# Set storage limit
ipfs config Datastore.StorageMax 10GB
```

## 启动与停止

**启动IPFS守护进程：**
```bash
ipfs daemon &> ipfs.log 2>&1 &
```

**检查守护进程状态：**
```bash
ipfs swarm peers | wc -l  # Connected peer count
ipfs repo stat            # Repository statistics
```

**停止守护进程：**
```bash
pkill ipfs
```

## 内容管理

### 添加内容

**添加文件和目录：**
```bash
# Add single file
ipfs add myfile.txt
# Returns: added QmHash myfile.txt

# Add directory recursively  
ipfs add -r ./my-directory/

# Add and only show final hash
ipfs add -Q myfile.txt

# Add with custom name
ipfs add --wrap-with-directory myfile.txt
```

**从标准输入添加内容：**
```bash
echo "Hello IPFS" | ipfs add
cat largefile.json | ipfs add --pin=false  # Don't pin immediately
```

### 固定内容（防止垃圾回收）**

**将内容固定以防止被垃圾回收：**
```bash
ipfs pin add QmHash
ipfs pin add -r QmHash  # Recursively pin directory

# List pinned content
ipfs pin ls --type=recursive
ipfs pin ls --type=direct

# Unpin content
ipfs pin rm QmHash
```

**远程固定服务：**
```bash
# Configure remote pinning (Pinata, Web3.Storage, etc.)
ipfs pin remote service add pinata https://api.pinata.cloud/psa YOUR_JWT

# Pin to remote service
ipfs pin remote add --service=pinata --name="my-content" QmHash

# List remote pins
ipfs pin remote ls --service=pinata
```

### 垃圾回收

**清理未固定的内容：**
```bash
# Show what would be collected
ipfs repo gc --dry-run

# Run garbage collection
ipfs repo gc

# Check repo size before/after
ipfs repo stat
```

## 发布与IPNS

### IPNS发布

**将内容发布到IPNS：**
```bash
# Publish to default key
ipfs name publish QmHash

# Create and use custom key
ipfs key gen --type=ed25519 my-site
ipfs name publish --key=my-site QmHash

# List published records
ipfs name pubsub subs
```

**使用自定义域名的IPNS：**
```bash
# Create DNS TXT record: _dnslink.example.com = "dnslink=/ipns/k51qzi5uqu5d..."
# Then resolve via:
ipfs name resolve /ipns/example.com
```

### 内容更新

**更新IPNS记录：**
```bash
# Publish new version
ipfs add -r ./updated-site/
ipfs name publish --key=my-site QmNewHash
```

## 网络配置

### Swarm管理

**节点操作：**
```bash
# List connected peers
ipfs swarm peers

# Connect to specific peer
ipfs swarm connect /ip4/104.131.131.82/tcp/4001/p2p/QmPeerID

# Disconnect peer
ipfs swarm disconnect /ip4/104.131.131.82/tcp/4001/p2p/QmPeerID
```

**地址配置：**
```bash
# Show current addresses
ipfs config Addresses

# Add custom swarm address
ipfs config --json Addresses.Swarm '["/ip4/0.0.0.0/tcp/4001", "/ip6/::/tcp/4001"]'
```

### 自动启动节点（Bootstrap Nodes）

**管理自动启动节点：**
```bash
# List bootstrap nodes
ipfs bootstrap list

# Add custom bootstrap node
ipfs bootstrap add /ip4/104.131.131.82/tcp/4001/p2p/QmBootstrapPeer

# Remove all bootstrap nodes (private network)
ipfs bootstrap rm --all
```

## 网关操作

### 本地网关

**配置网关：**
```bash
# Basic gateway configuration
ipfs config Addresses.Gateway /ip4/127.0.0.1/tcp/8080

# Public gateway (be careful!)
ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/8080

# Enable directory listing
ipfs config --json Gateway.PublicGateways '{
  "localhost": {
    "Paths": ["/ipfs", "/ipns"],
    "UseSubdomains": false
  }
}'
```

**访问模式：**
```bash
# Via path
http://localhost:8080/ipfs/QmHash

# Via subdomain (if configured)
http://QmHash.ipfs.localhost:8080
```

### 反向代理设置**

**Nginx配置示例：**
```nginx
server {
    listen 80;
    server_name gateway.example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 高级配置

### 性能调优

**高性能设置：**
```bash
# Apply server profile
ipfs config profile apply server

# Increase connection limits
ipfs config Swarm.ConnMgr.HighWater 2000
ipfs config Swarm.ConnMgr.LowWater 1000

# Adjust bitswap settings
ipfs config --json Bitswap.MaxOutstandingBytesPerPeer 1048576
```

### 私有网络

**创建私有IPFS网络：**
```bash
# Generate swarm key
echo -e "/key/swarm/psk/1.0.0/\n/base16/\n$(tr -dc 'a-f0-9' < /dev/urandom | head -c64)" > ~/.ipfs/swarm.key

# ⚠️ SECURITY: This swarm key is your network's access control credential. 
# Anyone with this file can join your private network. Protect it accordingly.

# Remove all bootstrap nodes
ipfs bootstrap rm --all

# Start daemon (will only connect to nodes with same key)
ipfs daemon
```

### 存储配置

**配置数据存储：**
```bash
# Set storage limits
ipfs config Datastore.StorageMax 100GB
ipfs config Datastore.GCPeriod "1h"

# Enable flatfs for better performance
ipfs config --json Datastore.Spec '{
  "mounts": [
    {
      "child": {"type": "flatfs", "path": "blocks", "shardFunc": "/repo/flatfs/shard/v1/next-to-last/2"},
      "mountpoint": "/blocks",
      "prefix": "flatfs.datastore",
      "type": "mount"
    }
  ],
  "type": "mount"
}'
```

## 监控与维护

### 健康检查

**基本健康检查：**
```bash
# Check daemon status
ipfs stats bw          # Bandwidth usage
ipfs stats repo        # Repository stats  
ipfs diag sys          # System information
ipfs log level debug   # Enable debug logging
```

**连接监控：**
```bash
# Monitor peer connections
while true; do
  echo "$(date): $(ipfs swarm peers | wc -l) peers"
  sleep 60
done
```

### 日志管理

**配置日志记录：**
```bash
# Set log levels
ipfs log level bitswap info
ipfs log level dht warn

# Tail logs
ipfs log tail
```

## 安全考虑

**API访问：**
- 除非在受信任的网络中，否则将API设置为本地主机（`127.0.0.1:5001`）
- 使用防火墙规则限制API访问
- 在多用户环境中考虑使用身份验证代理

**网关安全：**
- 公共网关可能会消耗大量带宽
- 实施速率限制和缓存机制
- 监控滥用行为和未经授权的内容

**内容策略：**
- IPFS具有抗审查特性——删除内容较为复杂
- 如有需要，可在网关层面实现内容过滤
- 考虑运营公共基础设施的法律后果

## 故障排除

**连接问题：**
- 检查防火墙是否允许4001（Swarm）和8080（网关）端口
- 确认自动启动节点可访问
- 尝试使用不同的Swarm地址

**性能问题：**
- 运行垃圾回收命令：`ipfs repo gc`
- 检查可用磁盘空间和数据存储限制
- 监控带宽使用情况：`ipfs stats bw`
- 考虑应用性能优化配置

**内容无法访问：**
- 确认内容已被固定：`ipfs pin ls`
- 检查是否存在提供者（provider）：`ipfs dht findprovs QmHash`
- 尝试重新发布IPNS记录

**相关技能：** `/ipfs-client`（仅用于读取查询），`/eth-readonly`（区块链集成）