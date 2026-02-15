---
name: esxi
description: 通过 SSH 和 vim-cmd 管理 VMware ESXi 主机和虚拟机。适用于执行虚拟机操作（如列表、启动、停止、创建快照）、主机监控、资源检查或故障排除等任务，适用于与 ESXi 基础设施进行交互的场景。
---

# ESXi管理

## 概述

您可以使用原生工具（`vim-cmd`、`esxcli`）通过SSH与VMware ESXi虚拟机管理程序进行交互。这些工具提供了用于虚拟机生命周期管理、主机监控以及常见ESXi操作的工作流程。

## 连接要求

- 具备通过SSH访问ESXi主机的权限（`vim-cmd`通常需要root权限）
- 配置了主机名/IP地址以及无密码SSH登录或密钥认证的凭据
- 目标主机上已安装`vim-cmd`和`esxcli`程序

## 环境变量

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `ESXI_USER` | `root` | ESXi主机的SSH用户名 |

### 核心操作

### 虚拟机管理

- **列出所有虚拟机：**
```bash
ssh root@esxi-host "vim-cmd vmsvc/getallvms"
```

- **获取虚拟机的电源状态：**
```bash
ssh root@esxi-host "vim-cmd vmsvc/power.getstate <vmid>"
```

- **执行电源操作：**
```bash
# Start VM
ssh root@esxi-host "vim-cmd vmsvc/power.on <vmid>"

# Stop VM (graceful shutdown)
ssh root@esxi-host "vim-cmd vmsvc/power.shutdown <vmid>"

# Force power off
ssh root@esxi-host "vim-cmd vmsvc/power.off <vmid>"

# Reboot VM
ssh root@esxi-host "vim-cmd vmsvc/power.reboot <vmid>"
```

### 快照管理

- **列出快照：**
```bash
ssh root@esxi-host "vim-cmd vmsvc/snapshot.get <vmid>"
```

- **创建快照：**
```bash
ssh root@esxi-host "vim-cmd vmsvc/snapshot.create <vmid> <snapshot-name>"
```

- **恢复到快照：**
```bash
ssh root@esxi-host "vim-cmd vmsvc/snapshot.revert <vmid> <snapshot-id>"
```

- **删除快照：**
```bash
ssh root@esxi-host "vim-cmd vmsvc/snapshot.remove <vmid> <snapshot-id>"
```

### 主机信息

- **系统信息：**
```bash
ssh root@esxi-host "esxcli system version get"
ssh root@esxi-host "esxcli system hostname get"
```

- **运行时间与健康状况：**
```bash
ssh root@esxi-host "uptime"
ssh root@esxi-host "esxcli hardware platform get"
```

- **存储信息：**
```bash
ssh root@esxi-host "esxcli storage filesystem list"
ssh root@esxi-host "esxcli storage core device list"
```

- **网络信息：**
```bash
ssh root@esxi-host "esxcli network ip interface ipv4 get"
ssh root@esxi-host "esxcli network vswitch standard list"
```

### 资源监控

- **CPU/内存使用情况：**
```bash
ssh root@esxi-host "esxcli hardware memory get"
ssh root@esxi-host "esxtop -b -n 1 | head"
```

- **正在运行的进程：**
```bash
ssh root@esxi-host "esxcli system process list"
```

## 虚拟机创建

使用`vm-create.sh`脚本创建新的虚拟机。该脚本会直接生成VMX文件，并通过`vim-cmd solo/registervm`命令将其注册到ESXi系统中。

### 快速入门

```bash
# Basic VM (1 CPU, 1GB RAM, 16GB disk)
./vm-create.sh esxi-host myvm "datastore1"

# Custom specs (2 CPUs, 4GB RAM, 50GB disk, Rocky Linux)
./vm-create.sh esxi-host myvm "datastore1" 2 4096 50 rockylinux-64 "VM Network" "[datastore1] ISOs/rocky.iso"
```

### 工作原理

该脚本通过以下步骤创建虚拟机：
1. 在数据存储设备上创建虚拟机目录。
2. 使用`vmkfstools`工具创建虚拟磁盘。
3. 生成包含正确PCI桥接配置的VMX配置文件。
4. 使用`vim-cmd solo/registervm`命令将虚拟机注册到ESXi系统中。

### 安全特性

- **重复检查**：如果虚拟机名称已存在，脚本会退出。
- **正确的PCI配置**：确保包含ESXi 6.x-8.x版本所需的`pciBridge`条目。
- **UEFI启动**：使用启用了安全启动功能的UEFI系统。
- **手动启动**：虚拟机不会自动启动（作为验证步骤）。

### 客户端操作系统标识符

客户端操作系统的格式因ESXi版本而异。常见值包括：
- `rockylinux-64` - Rocky Linux 8/9（ESXi 7.0及以上版本）
- `rhel9-64` - RHEL 9
- `centos8-64` - CentOS 8
- `ubuntu-64` - Ubuntu
- `otherLinux64Guest` - 通用Linux系统

注意：尽管某些文档中可能使用`rockylinux_64Guest`作为标识符，但ESXi 8.x版本实际上也接受`rockylinux-64`。

### 创建后的步骤

1. 验证虚拟机是否已成功创建：`./vm-control.sh esxi-host list`
2. 如有需要，配置启动参数或网络设置。
3. 启动虚拟机：`./vm-control.sh esxi-host start <vmid>`
4. 通过ESXi控制台监控虚拟机的运行状态。

## 故障排除

### SSH密钥认证

如果SSH连接失败并出现“权限被拒绝”或提示输入密码的错误，可能是ESXi主机未配置SSH公钥。

**在ESXi主机上配置公钥：**
```bash
esxcli system ssh key add -u <username> -k "<public-key-contents>"
```

**在本地客户端上，确保`~/.ssh/config`文件中包含与连接字符串匹配的主机条目：**
```
Host esxi-host
    HostName <esxi-ip-or-hostname>
    User <username>
    IdentityFile ~/.ssh/id_rsa
```

注意：SSH配置文件中的`Host`条目需要与实际连接使用的名称完全一致。如果使用简短的主机名进行连接，则配置文件中也应使用该简短名称；如果使用完全 Qualified Domain Name (FQDN) 进行连接，则配置文件中必须使用FQDN。

## 资源

### 脚本

- `vm-control.sh`：用于执行常见虚拟机操作的脚本（支持`ESXI_USER`环境变量）
- `vm-create.sh`：用于创建具有正确PCI桥接配置的新虚拟机（支持`ESXI_USER`环境变量）
- `host-info.sh`：用于收集主机统计信息和健康状况数据（支持`ESXI_USER`环境变量）