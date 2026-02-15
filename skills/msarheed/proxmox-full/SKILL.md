---
name: proxmox-full
description: **Proxmox VE的全面管理功能**  
- **创建/克隆/启动/停止虚拟机（VMs）和LXC容器**  
- **管理快照、备份以及存储资源**  
- **管理模板**  

适用于需要管理Proxmox基础设施、虚拟机或容器的用户。
metadata: {"clawdbot":{"emoji":"🖥️","homepage":"https://www.proxmox.com/","requires":{"bins":["curl","jq"],"env":["PVE_TOKEN"]},"primaryEnv":"PVE_TOKEN"}}
---

# Proxmox VE - 全面管理

通过 REST API 完全控制 Proxmox VE 虚拟机管理器。

## 设置

```bash
export PVE_URL="https://192.168.1.10:8006"
export PVE_TOKEN="user@pam!tokenid=secret-uuid"
```

**创建 API 令牌：**  
进入 “Datacenter” → “Permissions” → “API Tokens” → 点击 “Add”（请取消选中 “Privilege Separation” 选项）。

## 请求头（Auth Header）

```bash
AUTH="Authorization: PVEAPIToken=$PVE_TOKEN"
```

---

## 集群与节点（Cluster & Nodes）

```bash
# Cluster status
curl -sk -H "$AUTH" "$PVE_URL/api2/json/cluster/status" | jq

# List nodes
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes" | jq '.data[] | {node, status, cpu: (.cpu*100|round), mem_pct: (.mem/.maxmem*100|round)}'

# Node details
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/status" | jq
```

---

## 列出虚拟机与容器（List VMs & Containers）

```bash
# All VMs on node
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu" | jq '.data[] | {vmid, name, status}'

# All LXC on node
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/lxc" | jq '.data[] | {vmid, name, status}'

# Cluster-wide (all VMs + LXC)
curl -sk -H "$AUTH" "$PVE_URL/api2/json/cluster/resources?type=vm" | jq '.data[] | {node, type, vmid, name, status}'
```

---

## 虚拟机/容器控制（VM/Container Control）

```bash
# Start
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}/status/start"

# Stop (immediate)
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}/status/stop"

# Shutdown (graceful)
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}/status/shutdown"

# Reboot
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}/status/reboot"

# For LXC: replace /qemu/ with /lxc/
```

---

## 创建 LXC 容器（Create LXC Container）

```bash
# Get next available VMID
NEWID=$(curl -sk -H "$AUTH" "$PVE_URL/api2/json/cluster/nextid" | jq -r '.data')

# Create container
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/lxc" \
  -d "vmid=$NEWID" \
  -d "hostname=my-container" \
  -d "ostemplate=local:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst" \
  -d "storage=local-lvm" \
  -d "rootfs=local-lvm:8" \
  -d "memory=1024" \
  -d "swap=512" \
  -d "cores=2" \
  -d "net0=name=eth0,bridge=vmbr0,ip=dhcp" \
  -d "password=changeme123" \
  -d "start=1"
```

**LXC 参数：**  
| 参数 | 示例 | 说明 |
|-------|---------|-------------|
| vmid | 200 | 容器 ID |
| hostname | myct | 容器主机名 |
| ostemplate | local:vztmpl/debian-12-... | 模板路径 |
| storage | local-lvm | rootfs 的存储空间 |
| rootfs | local-lvm:8 | 根目录磁盘（8GB） |
| memory | 1024 | 内存（MB） |
| swap | 512 | 交换空间（MB） |
| cores | 2 | CPU 核心数 |
| net0 | name=eth0,bridge=vmbr0,ip=dhcp | 网络配置 |
| password | secret | root 用户密码 |
| ssh-public-keys | ssh-rsa ... | SSH 密钥（URL 编码格式） |
| unprivileged | 1 | 无权限容器 |
| start | 1 | 创建后立即启动 |

---

## 创建虚拟机（Create VM）

```bash
# Get next VMID
NEWID=$(curl -sk -H "$AUTH" "$PVE_URL/api2/json/cluster/nextid" | jq -r '.data')

# Create VM
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu" \
  -d "vmid=$NEWID" \
  -d "name=my-vm" \
  -d "memory=2048" \
  -d "cores=2" \
  -d "sockets=1" \
  -d "cpu=host" \
  -d "net0=virtio,bridge=vmbr0" \
  -d "scsi0=local-lvm:32" \
  -d "scsihw=virtio-scsi-pci" \
  -d "ide2=local:iso/ubuntu-22.04.iso,media=cdrom" \
  -d "boot=order=scsi0;ide2;net0" \
  -d "ostype=l26"
```

**虚拟机参数：**  
| 参数 | 示例 | 说明 |
|-------|---------|-------------|
| vmid | 100 | 虚拟机 ID |
| name | myvm | 虚拟机名称 |
| memory | 2048 | 内存（MB） |
| cores | 2 | 每个 CPU 插槽的核心数 |
| sockets | 1 | CPU 插槽数 |
| cpu | host | CPU 类型 |
| net0 | virtio,bridge=vmbr0 | 网络配置 |
| scsi0 | local-lvm:32 | 磁盘（32GB） |
| ide2 | local:iso/file.iso,media=cdrom | ISO 镜像文件 |
| ostype | l26 (Linux), win11 | 操作系统类型 |
| boot | order=scsi0;ide2 | 启动顺序 |

---

## 克隆虚拟机/容器（Clone VM/Container）

```bash
# Clone VM
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}/clone" \
  -d "newid=201" \
  -d "name=cloned-vm" \
  -d "full=1" \
  -d "storage=local-lvm"

# Clone LXC
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/lxc/{vmid}/clone" \
  -d "newid=202" \
  -d "hostname=cloned-ct" \
  -d "full=1" \
  -d "storage=local-lvm"
```

**克隆参数：**  
| 参数 | 说明 |
|-------|-------------|
| newid | 新虚拟机 ID |
| name/hostname | 新名称 |
| full | 1=完整克隆；0=链接克隆 |
| storage | 目标存储空间 |
| target | 目标节点（用于迁移） |

---

## 将虚拟机转换为模板（Convert to Template）

```bash
# Convert VM to template
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}/template"

# Convert LXC to template
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/lxc/{vmid}/template"
```

---

## 快照（Snapshots）

```bash
# List snapshots
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}/snapshot" | jq '.data[] | {name, description}'

# Create snapshot
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}/snapshot" \
  -d "snapname=before-update" \
  -d "description=Snapshot before system update"

# Rollback
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}/snapshot/{snapname}/rollback"

# Delete snapshot
curl -sk -X DELETE -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}/snapshot/{snapname}"
```

---

## 备份（Backups）

```bash
# Start backup
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/vzdump" \
  -d "vmid={vmid}" \
  -d "storage=local" \
  -d "mode=snapshot" \
  -d "compress=zstd"

# List backups
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/storage/{storage}/content?content=backup" | jq

# Restore backup
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu" \
  -d "vmid=300" \
  -d "archive=local:backup/vzdump-qemu-100-2024_01_01-12_00_00.vma.zst" \
  -d "storage=local-lvm"
```

---

## 存储与模板（Storage & Templates）

```bash
# List storage
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/storage" | jq '.data[] | {storage, type, avail, used}'

# List available templates
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/storage/local/content?content=vztmpl" | jq '.data[] | .volid'

# List ISOs
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/storage/local/content?content=iso" | jq '.data[] | .volid'

# Download template
curl -sk -X POST -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/aplinfo" \
  -d "storage=local" \
  -d "template=debian-12-standard_12.2-1_amd64.tar.zst"
```

---

## 任务管理（Tasks）

```bash
# Recent tasks
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/tasks?limit=10" | jq '.data[] | {upid, type, status}'

# Task status
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/tasks/{upid}/status" | jq

# Task log
curl -sk -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/tasks/{upid}/log" | jq -r '.data[].t'
```

---

## 删除虚拟机/容器（Delete VM/Container）

```bash
# Delete VM (must be stopped)
curl -sk -X DELETE -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}"

# Delete LXC
curl -sk -X DELETE -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/lxc/{vmid}"

# Force delete (purge)
curl -sk -X DELETE -H "$AUTH" "$PVE_URL/api2/json/nodes/{node}/qemu/{vmid}?purge=1&destroy-unreferenced-disks=1"
```

---

## 快速参考（Quick Reference）

| 操作 | 端点（Endpoint） | 方法（Method） |
|--------|----------|--------|
| 列出节点 | /nodes | GET |
| 列出虚拟机 | /nodes/{node}/qemu | GET |
| 列出 LXC 容器 | /nodes/{node}/lxc | GET |
| 创建虚拟机 | /nodes/{node}/qemu | POST |
| 创建 LXC 容器 | /nodes/{node}/lxc | POST |
| 克隆虚拟机 | /nodes/{node}/qemu/{vmid}/clone | POST |
| 启动虚拟机 | /nodes/{node}/qemu/{vmid}/status/start | POST |
| 停止虚拟机 | /nodes/{node}/qemu/{vmid}/status/stop | POST |
| 创建快照 | /nodes/{node}/qemu/{vmid}/snapshot | POST |
| 删除虚拟机 | /nodes/{node}/qemu/{vmid} | DELETE |
| 获取下一个 ID | /cluster/nextid | GET |

## 注意事项：**
- 使用 `-k` 选项生成自签名证书。
- API 令牌无需进行 CSRF 验证。
- 将 `{node}` 替换为节点名称（例如 `pve`）。
- 将 `{vmid}` 替换为虚拟机/容器的 ID。
- 对于虚拟机使用 `qemu`，对于容器使用 `lxc`。
- 所有创建/克隆操作都会返回一个任务 ID（UPID）以便追踪。