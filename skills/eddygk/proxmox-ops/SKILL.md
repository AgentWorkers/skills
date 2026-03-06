---
name: proxmox-ops
description: >
  **基于REST API的Proxmox VE操作管理**  
  通过REST API实现对Proxmox VE的全面管理，包括监控、控制、虚拟机（VM）和LXC容器的配置以及故障排除。这些功能均基于经过实战验证的操作流程设计。  
  **适用场景：**  
  - 列出、启动、停止或重启虚拟机或LXC容器  
  - 检查节点状态、集群健康状况或资源使用情况  
  - 创建、克隆或删除虚拟机及容器  
  - 管理快照、备份、存储资源或模板  
  - 调整磁盘大小（通过API配合宿主机文件系统操作实现）  
  - 从虚拟机代理中查询IP地址  
  - 查看任务记录或系统事件日志  
  **辅助工具：**  
  - `pve.sh`辅助脚本：支持根据虚拟机ID自动发现节点；提供操作安全机制（读-only、可逆操作、破坏性操作等选项）；包含关于调整磁盘大小后的宿主机文件系统处理提示；并提供详细的配置参考。  
  **所需工具：**  
  - `curl` 和 `jq`  
  **认证信息：**  
  - `PROXMOX_HOST`、`PROXMOX_TOKEN_ID`、`PROXMOX_TOKEN_SECRET`：需设置为环境变量或存储在`~/.proxmox-credentials`文件中（运行时加载，用户自行创建，权限设置为600）。  
  **数据存储位置：**  
  - 配置信息会写入`~/.proxmox-credentials`文件（用户创建，包含API令牌，权限设置为600）。  
  **网络连接：**  
  - 仅连接到用户配置的Proxmox主机；对于自签名证书，禁用TLS验证。  
  **注意事项：**  
  - 该功能依赖于HTTPS协议进行安全通信。
metadata: { "openclaw": { "emoji": "🖥️", "homepage": "https://github.com/eddygk/proxmox-ops-skill", "requires": { "bins": ["curl", "jq"] }, "os": ["darwin", "linux"] } }
---
# Proxmox VE管理

## 首次设置

在`~/.proxmox-credentials`文件中创建一个凭证文件：

```bash
cat > ~/.proxmox-credentials <<'EOF'
PROXMOX_HOST=https://<your-proxmox-ip>:8006
PROXMOX_TOKEN_ID=user@pam!tokenname
PROXMOX_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
EOF
chmod 600 ~/.proxmox-credentials
```

**替代方案：**可以直接将`PROXMOX_HOST`、`PROXMOX_TOKEN_ID`和`PROXMOX_TOKEN_SECRET`设置为环境变量（适用于持续集成/代理环境）。辅助脚本会首先检查环境变量，如果未找到这些变量，则会从`~/.proxmox-credentials`文件中读取它们。

在Proxmox中创建API令牌：进入“Datacenter” → “Permissions” → “API Tokens” → “Add”。请仅授予工作流程所需的最低权限（例如，`PVEAuditor`用于只读监控，`PVEVMAdmin`用于虚拟机控制）。只有在工作流程需要完全的API访问权限时，才启用权限分离功能。

## 认证头

```bash
source ~/.proxmox-credentials
AUTH="Authorization: PVEAPIToken=$PROXMOX_TOKEN_ID=$PROXMOX_TOKEN_SECRET"
```

## 辅助脚本

`scripts/pve.sh`脚本会自动从虚拟机ID（VMID）中识别节点——大多数操作无需指定具体的节点。

```bash
pve.sh status              # Cluster nodes overview
pve.sh vms [node]          # List all VMs (optionally filter by node)
pve.sh lxc <node>          # List LXC containers on node
pve.sh start <vmid>        # Start VM/LXC
pve.sh stop <vmid>         # Force stop VM/LXC
pve.sh shutdown <vmid>     # Graceful shutdown VM/LXC
pve.sh reboot <vmid>       # Reboot VM/LXC
pve.sh snap <vmid> [name]  # Create snapshot (disk-only, safe)
pve.sh snapshots <vmid>    # List snapshots
pve.sh tasks <node>        # Show recent tasks
pve.sh storage <node>      # Show storage status
```

## 工作流程

1. 从`~/.proxmox-credentials`文件中加载凭证。
2. 确定操作类型：
   - **只读**（状态、列表、存储、任务）→ 直接执行。
   - **可逆操作**（启动、停止、重启、快照）→ 执行操作，并记录UPID以便追踪。
   - **破坏性操作**（删除虚拟机、调整磁盘大小、回滚快照）→ 先获取用户确认。
3. 通过curl和API令牌进行Proxmox API查询。
4. 使用jq解析JSON数据。
5. 跟踪异步任务——创建/克隆/备份操作会返回UPID。

## 常见操作

### 集群与节点

```bash
# Cluster status
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/cluster/status" | jq

# List nodes with CPU/memory
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes" | jq '.data[] | {node, status, cpu, mem: (.mem/.maxmem*100|round)}'
```

### 列出虚拟机与容器

```bash
# Cluster-wide (all VMs + LXC)
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/cluster/resources?type=vm" | jq '.data[] | {node, vmid, name, type, status}'

# VMs on specific node
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu" | jq '.data[] | {vmid, name, status}'

# LXC on specific node
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/lxc" | jq '.data[] | {vmid, name, status}'
```

### 虚拟机/容器控制

```bash
# Start / Stop / Shutdown / Reboot
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/status/start"
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/status/stop"
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/status/shutdown"
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/status/reboot"

# For LXC: replace /qemu/ with /lxc/
```

### 快照

**⚠️ vmstate参数：** 除非确实需要保留运行中的进程状态，否则不要使用`vmstate=1`。
- 使用`vmstate=1`会冻结虚拟机并导致严重的I/O操作——可能会影响同一节点上的其他虚拟机。
- 对于变更前的备份操作，请省略`vmstate`参数（默认情况下仅备份磁盘数据，不会导致I/O峰值）。

```bash
# List snapshots
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/snapshot" | jq

# Create snapshot (disk-only, safe)
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/snapshot" \
  -d "snapname=snap1" -d "description=Before update"

# Rollback
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/snapshot/{snapname}/rollback"

# Delete snapshot
curl -ks -X DELETE -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/snapshot/{snapname}"
```

### 调整磁盘大小

```bash
# Get current disk config
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/config" | jq

# Resize disk (use absolute size, NOT relative — +10G fails regex validation)
curl -ks -X PUT -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/resize" \
  -d "disk=scsi0" -d "size=20G" | jq
```

**调整磁盘大小后的操作：**
1. 修复GPT分区：`parted /dev/sda print` → 修复分区问题。
2. 调整分区大小：`parted /dev/sda resizepart 3 100%`
3. 如果使用LVM：`pvresize /dev/sda3 && lvextend -l +100%FREE /dev/vg/root`
4. 调整文件系统大小：`resize2fs /dev/mapper/vg-root`（ext4文件系统）或`xfs_growfs /`（xfs文件系统）。

### 客户端代理（IP地址获取）

```bash
# Get VM network interfaces (requires qemu-guest-agent)
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/agent/network-get-interfaces" | \
  jq -r '.data.result[] | select(.name != "lo") | .["ip-addresses"][] | select(.["ip-address-type"] == "ipv4") | .["ip-address"]' | head -1
```

始终通过客户端代理获取虚拟机的当前IP地址——不要硬编码IP地址。

### 存储与备份

```bash
# List storage
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/storage" | jq '.data[] | {storage, type, active, used_fraction: (.used/.total*100|round|tostring + "%")}'

# List backups
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/storage/{storage}/content?content=backup" | jq

# Start backup
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/vzdump" \
  -d "vmid={vmid}" -d "storage={storage}" -d "mode=snapshot"
```

### 任务管理

```bash
# Recent tasks
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/tasks" | jq '.data[:10] | .[] | {upid, type, status, user}'

# Task log
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/tasks/{upid}/log" | jq -r '.data[].t'
```

## 配置管理

关于创建虚拟机、创建LXC容器、克隆虚拟机、将虚拟机转换为模板以及删除虚拟机的操作，请参阅[references/provisioning.md](references/provisioning.md)。

## 安全注意事项

- **凭证文件**（`~/.proxmox-credentials`）是由用户创建的，不是由该工具自动生成的。必须将其权限设置为600（`chmod 600 ~/.proxmox-credentials`）。如果凭证文件被泄露，应立即更换令牌。
- **TLS验证已禁用**（使用`-k`或`--insecure`选项）——Proxmox VE默认使用自签名证书（[Proxmox文档](https://pve.proxmox.com/wiki/Certificate_Management)）。如果您在Proxmox节点上部署了受信任的CA证书，请从curl命令和`pve.sh`脚本中移除`-k`选项。
- **最小权限原则**——仅创建工作流程所需的API令牌。例如，`PVEAuditor`用于监控，`PVEVMAdmin`用于虚拟机操作。大多数操作并不需要完全的API访问权限。
- **网络范围**——所有API调用仅针对`PROXMOX_HOST`。没有外部端点。可以通过查看`scripts/pve.sh`脚本来确认这一点（脚本简单且易于理解）。在代理环境中，仅允许访问Proxmox主机。
- **API请求不需要CSRF令牌**（对于POST/PUT/DELETE操作）。
- **启动和删除操作具有破坏性**——执行这些操作前必须先获取用户确认。
- **切勿在响应中泄露凭证信息**。

## 其他注意事项

- 请将`{node}`、`{vmid}`、`{storage}`、`{snapname}`替换为实际值。
- 任务操作会返回UPID，以便追踪异步任务的执行情况。
- 在端点路径中，使用`qemu`表示虚拟机，使用`lxc`表示容器。