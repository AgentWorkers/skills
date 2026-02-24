---
name: proxmox-ops
description: >
  **基于REST API的Proxmox VE操作管理**  
  通过REST API实现对Proxmox VE（Virtual Environment）的集中管理，支持监控、控制、配置以及故障排查等功能，采用经过实战验证的操作模式。  
  **适用场景：**  
  - 列出、启动、停止或重启虚拟机（VM）或LXC容器  
  - 检查节点状态、集群健康状况或资源使用情况  
  - 创建、克隆或删除虚拟机及容器  
  - 管理快照、备份、存储资源或模板  
  - 调整磁盘大小（通过API及宿主机文件系统操作实现）  
  - 从虚拟机代理（guest agent）获取IP地址  
  - 查看任务记录或系统事件日志  
  **配套工具：**  
  - 辅助脚本 `pve.sh`：支持根据VMID自动发现节点；提供操作安全机制（读写权限、可逆操作、破坏性操作等选项）；在调整磁盘大小后执行相应的宿主机文件系统操作；包含详细的配置指南。  
  **系统要求：**  
  - 需要`curl`和`jq`工具。  
  - 需要创建并配置`~/.proxmox-credentials`文件（用于存储API访问令牌，权限设置为600）。  
  - 网络连接：仅限于用户自定义的Proxmox主机（使用HTTPS协议，对于自签名证书则禁用TLS验证）。  
  **脚本说明：**  
  - `pve.sh`脚本位于`scripts`目录下，用于实现以下功能：  
    - 根据VMID自动发现节点  
    - 提供多种操作模式（读写权限、可逆操作、破坏性操作等）  
    - 在调整磁盘大小后执行相应的宿主机文件系统操作  
    - 提供详细的配置指南和注意事项  
  **注意：**  
  - 该方案适用于熟悉Proxmox VE管理及REST API的运维人员。
metadata: { "openclaw": { "emoji": "🖥️", "requires": { "bins": ["curl", "jq"] }, "os": ["darwin", "linux"] } }
---
# Proxmox VE管理

## 配置

```bash
cat > ~/.proxmox-credentials <<'EOF'
PROXMOX_HOST=https://<your-proxmox-ip>:8006
PROXMOX_TOKEN_ID=user@pam!tokenname
PROXMOX_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
EOF
chmod 600 ~/.proxmox-credentials
```

在Proxmox中创建API令牌：点击“Datacenter” → “Permissions” → “API Tokens” → “Add”（取消选中“Privilege Separation”选项以获得完全访问权限）。

## 认证头

```bash
source ~/.proxmox-credentials
AUTH="Authorization: PVEAPIToken=$PROXMOX_TOKEN_ID=$PROXMOX_TOKEN_SECRET"
```

## 辅助脚本

`scripts/pve.sh`脚本会自动根据VMID识别节点——大多数操作无需指定具体节点。

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

1. 从`~/.proxmox-credentials`文件中加载凭据。
2. 确定操作类型：
   - **只读**（状态、列表、存储、任务）→ 直接执行。
   - **可逆操作**（启动、停止、重启、快照）→ 执行操作，并记录UPID以便跟踪。
   - **破坏性操作**（删除虚拟机、调整磁盘大小、回滚快照）→ 首先需要用户确认。
3. 通过curl和API令牌进行Proxmox API请求。
4. 使用jq解析JSON响应。
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
- 对于变更前的备份，请省略`vmstate`参数（默认情况下仅备份磁盘数据，不会引起I/O峰值）。

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

## 配置与管理

关于创建虚拟机、创建LXC容器、克隆虚拟机、将虚拟机转换为模板以及删除虚拟机等操作，请参阅[references/provisioning.md](references/provisioning.md)。

## 安全注意事项

- 凭据文件的权限必须设置为600（`chmod 600 ~/.proxmox-credentials`）。
- Proxmox默认禁用了TLS验证（使用自签名证书）。
- 对于POST/PUT/DELETE请求，API令牌不需要CSRF令牌。
- 启动和删除操作具有破坏性——执行前必须获得用户确认。
- 绝不要在响应中泄露凭据信息。

## 其他注意事项

- 请将`{node}`、`{vmid}`、`{storage}`、`{snapname}`替换为实际值。
- 任务操作会返回UPID，以便跟踪异步任务的执行情况。
- 在端点路径中，使用`qemu`表示虚拟机，使用`lxc`表示容器。