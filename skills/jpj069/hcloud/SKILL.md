---
name: hcloud
description: 使用 `hcloud` CLI 管理 Hetzner Cloud 的基础设施。适用于处理 Hetzner 服务器、防火墙、网络、卷、负载均衡器或任何 Hetzner Cloud 资源。支持服务器管理（创建/删除/启动/停止）、防火墙配置、SSH 密钥管理、卷操作以及基础设施监控。
---
# Hetzner Cloud CLI (hcloud)

使用官方的 CLI 工具来管理 Hetzner Cloud 的基础设施。

## 先决条件

**安装**（如果尚未安装）：
```bash
# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
  URL="https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-arm64.tar.gz"
else
  URL="https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-amd64.tar.gz"
fi

# Install
cd /tmp
wget -q "$URL"
tar xzf hcloud-linux-*.tar.gz
sudo mv hcloud /usr/local/bin/
chmod +x /usr/local/bin/hcloud
```

**配置**（首次使用时）：
```bash
mkdir -p ~/.config/hcloud
cat > ~/.config/hcloud/cli.toml <<EOF
active_context = "default"

[[contexts]]
name = "default"
token = "YOUR_HETZNER_API_TOKEN"
EOF
chmod 600 ~/.config/hcloud/cli.toml
```

**验证**：
```bash
hcloud version
hcloud server list
```

## 常用命令

### 服务器
```bash
# List servers
hcloud server list

# Get server details
hcloud server describe <name-or-id>

# Create server
hcloud server create \
  --name my-server \
  --type cx11 \
  --image ubuntu-24.04 \
  --ssh-key <key-id-or-name> \
  --location nbg1

# Start/stop/reboot
hcloud server start <name-or-id>
hcloud server stop <name-or-id>
hcloud server reboot <name-or-id>

# Delete server
hcloud server delete <name-or-id>

# SSH into server
hcloud server ssh <name-or-id>

# Run command on server
hcloud server ssh <name-or-id> -- 'uname -a'
```

### 防火墙
```bash
# List firewalls
hcloud firewall list

# Get firewall details
hcloud firewall describe <name-or-id>

# Create firewall
hcloud firewall create \
  --name my-firewall \
  --rules-file rules.json

# Add rule to firewall
hcloud firewall add-rule <name-or-id> \
  --direction in \
  --port 22 \
  --protocol tcp \
  --source-ips 0.0.0.0/0 \
  --source-ips ::/0 \
  --description "SSH"

# Apply firewall to server
hcloud firewall apply-to-resource <firewall-name> \
  --type server \
  --server <server-name-or-id>

# Remove firewall from server
hcloud firewall remove-from-resource <firewall-name> \
  --type server \
  --server <server-name-or-id>

# Delete firewall
hcloud firewall delete <name-or-id>
```

### SSH 密钥
```bash
# List SSH keys
hcloud ssh-key list

# Add SSH key
hcloud ssh-key create \
  --name my-key \
  --public-key-from-file ~/.ssh/id_ed25519.pub

# Delete SSH key
hcloud ssh-key delete <name-or-id>
```

### 服务器类型与镜像
```bash
# List available server types
hcloud server-type list

# List available images
hcloud image list
hcloud image list --type system  # Only system images

# List locations
hcloud location list
```

### 存储卷
```bash
# List volumes
hcloud volume list

# Create volume
hcloud volume create \
  --name my-volume \
  --size 10 \
  --location nbg1

# Attach volume to server
hcloud volume attach <volume-name> <server-name>

# Detach volume
hcloud volume detach <volume-name>

# Delete volume
hcloud volume delete <volume-name>
```

### 网络
```bash
# List networks
hcloud network list

# Create network
hcloud network create \
  --name my-network \
  --ip-range 10.0.0.0/16

# Add subnet
hcloud network add-subnet <network-name> \
  --type cloud \
  --network-zone eu-central \
  --ip-range 10.0.1.0/24

# Attach server to network
hcloud server attach-to-network <server-name> \
  --network <network-name>
```

### 负载均衡器
```bash
# List load balancers
hcloud load-balancer list

# Create load balancer
hcloud load-balancer create \
  --name my-lb \
  --type lb11 \
  --location nbg1

# Add target (server)
hcloud load-balancer add-target <lb-name> \
  --server <server-name>

# Add service
hcloud load-balancer add-service <lb-name> \
  --protocol http \
  --listen-port 80 \
  --destination-port 80
```

## 防火墙规则格式

对于复杂的防火墙规则，请使用 JSON 格式：
```json
[
  {
    "direction": "in",
    "port": "22",
    "protocol": "tcp",
    "source_ips": ["0.0.0.0/0", "::/0"],
    "description": "SSH"
  },
  {
    "direction": "in",
    "port": "80",
    "protocol": "tcp",
    "source_ips": ["0.0.0.0/0", "::/0"],
    "description": "HTTP"
  },
  {
    "direction": "in",
    "port": "443",
    "protocol": "tcp",
    "source_ips": ["0.0.0.0/0", "::/0"],
    "description": "HTTPS"
  },
  {
    "direction": "in",
    "protocol": "icmp",
    "source_ips": ["0.0.0.0/0", "::/0"],
    "description": "ICMP (ping)"
  }
]
```

## 常见服务器类型

| 类型 | vCPU | 内存 | 磁盘 | 每月价格（约） |
|-------|------|-------|--------|-------------------|
| cx11  | 1    | 2 GB  | 20 GB  | €4                |
| cx21  | 2    | 4 GB  | 40 GB  | €6                |
| cx22  | 2    | 4 GB  | 40 GB  | €6（已弃用）   |
| cx23  | 2    | 4 GB  | 40 GB  | €3                |
| cx31  | 2    | 8 GB  | 80 GB  | €10               |
| cx33  | 4    | 8 GB  | 80 GB  | €5                |
| cpx11 | 2    | 2 GB  | 40 GB  | €5                |
| cpx21 | 3    | 4 GB  | 80 GB  | €10               |
| cpx31 | 4    | 8 GB  | 160 GB | €18               |

**cx 系列**：共享 vCPU（成本优化）  
**cpx 系列**：专用 vCPU（性能优化）

## 提示

- **使用 `--output json` 进行解析**：`hcloud server list --output json | jq`
- **上下文切换**：在 `~/.config/hcloud/cli.toml` 中为不同的项目/账户创建多个上下文
- **服务器标签**：使用标签进行分类：`--labels environment=production,project=web`
- **默认位置**：设置默认位置以避免重复指定：`hcloud context config default-location nbg1`
- **模拟执行**：许多命令支持 `--dry-run` 或 `--validate` 标志

## 文档

官方文档：https://docs.hetzner.cloud/
GitHub：https://github.com/hetznercloud/cli