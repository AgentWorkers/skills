---
name: esxi-debian-deploy
description: >
  在 VMware ESXi 8 上实现零干预（零手动操作）的 Debian 13 虚拟机部署：  
  - 构建自定义的预安装配置文件（preseed ISO）；  
  - 创建支持 NVMe 和 vmxnet3 协议的虚拟机，并配置串行控制台；  
  - 执行无人值守的安装过程。  
  该方案适用于在 ESXi 上部署 Debian 虚拟机、自动化虚拟机配置，或为无界面（headless）的 ESXi 环境设置串行控制台访问功能。
---
# ESXi Debian 13 零干预部署

在大约8分钟内，无需任何手动操作即可在ESXi 8上部署配置齐全的Debian 13虚拟机。

## 所需的环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `ESXI_HOST` | 是 | ESXi主机的IP地址 |
| `ESXI_PASS` | 是 | ESXi root密码 |
| `ESXI_USER` | 否 | ESXi用户（默认：`root`） |
| `ESXI_DATASTORE` | 否 | 目标数据存储（默认：`datastore1`） |
| `NETWORK` | 否 | 端口组名称（默认：`VM Network`） |
| `DOMAIN` | 否 | 虚拟机所在的域（默认：`local`） |
| `VM_PASS` | 是（仅用于磁盘扩展） | 用于磁盘扩展脚本的虚拟机root密码 |

> **⚠️ 注意：** 部署脚本会生成一个随机虚拟机密码，并将其打印到标准输出（stdout）中。该密码也会被嵌入到上传到ESXi数据存储的预安装文件（preseed ISO）中。部署完成后请删除该ISO文件，并将stdout输出视为敏感信息。

## 系统要求

- **ESXi 8.x** 主机，支持SSH和数据存储访问 |
- **govc** CLI（[github.com/vmware/govmomi](https://github.com/vmware/govmomi)） |
- **xorriso**、**isolinux** — 用于自定义ISO构建 |
- **sshpass** — 用于自动化的SSH/SCP传输 |
- 代理主机上需要安装以下工具：`bash`、`python3`、`wget`

在Debian/Ubuntu上安装相关软件：

```bash
apt install xorriso isolinux sshpass
# govc: https://github.com/vmware/govmomi/releases
```

## 使用方法

所有凭据均通过环境变量传递——没有任何内容被硬编码或嵌入到进程参数中。

```bash
export ESXI_HOST="192.168.1.100"
export ESXI_PASS="your-esxi-root-password"

bash scripts/esxi-deploy.sh [hostname] [cpu] [ram_mb] [disk_gb] [serial_port]
```

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| hostname | 随机生成的动物名称 | 虚拟机名称 |
| cpu | 2 | vCPU数量 |
| ram_mb | 2048 | 内存大小（MB） |
| disk_gb | 20 | 磁盘大小（GB） |
| serial_port | 随机生成的8600-8699之间的数字 | 用于串行控制台的Telnet端口 |

**示例：**
```bash
bash scripts/esxi-deploy.sh webserver 4 4096 50 8610
```

## 功能说明

1. **生成preseed.cfg文件**：设置语言为德语（`de_DE.UTF-8`），启用DHCP，配置用户`root`和随机密码。
2. **构建自定义ISO文件**：结合Debian的netinst安装程序和预安装配置文件（preseed），以及经过修改的isolinux内核以实现自动启动。
3. **将ISO文件上传到ESXi数据存储**。
4. **创建虚拟机**：配置NVMe磁盘（采用精简配置），安装两个网卡（E1000用于安装过程，vmxnet3用于生产环境），并通过串行端口进行远程控制。
5. **启动并执行无人值守安装**：预安装配置文件会自动完成所有安装步骤。
6. **安装完成后**：移除E1000网卡，弹出ISO文件，并将启动设备设置为硬盘。
7. **输出凭据信息**：包括SSH连接信息和串行控制台的访问详情。

## 串行控制台

每个虚拟机都配备了一个可以通过Telnet连接到ESXi主机的串行端口：

```bash
telnet <ESXI_IP> <serial_port>
```

即使虚拟机没有网络连接，该功能也能正常使用。配置如下：
- **GRUB**：`GRUB_TERMINAL="console serial"`，波特率为115200，数据格式为8N1。
- **内核**：`console=tty0 console=ttyS0,115200n8`。
- **Getty**：启用`serial-getty@ttyS0.service`服务。

**ESXi防火墙配置要求**（脚本会自动执行这些配置）：
```bash
esxcli network firewall ruleset set -e true -r remoteSerialPort
```

**重要提示：** 请将串行端口的IP地址设置为ESXi主机的IP地址，而不是`0.0.0.0`。

## 在线磁盘扩展

可以在不关闭虚拟机的情况下扩展其磁盘容量：

```bash
export ESXI_HOST="192.168.1.100"
export ESXI_PASS="your-esxi-password"
export VM_PASS="vm-root-password"

bash scripts/esxi-vm-resize-disk.sh <vm-name> <new-size-gb>
```

虚拟机上需要预先安装`cloud-guest-utils`工具（该工具由部署脚本自动安装）。

## 配置选项

所有设置均可通过环境变量进行配置：

```bash
export ESXI_HOST="192.168.1.100"    # ESXi host IP (required)
export ESXI_PASS="secret"           # ESXi root password (required)
export ESXI_USER="root"             # ESXi user (default: root)
export ESXI_DATASTORE="datastore1"  # Target datastore (default: datastore1)
export NETWORK="VM Network"         # Port group name (default: VM Network)
export DOMAIN="example.local"       # Domain for VMs (default: local)
```

无需使用任何凭证存储或外部凭证解析工具。所有敏感信息仅通过环境变量传递，绝不会被嵌入到进程参数或URL中。

## 虚拟机配置详情

| 组件 | 选择理由 |  
|-----------|--------|--------|
| 磁盘控制器 | NVMe | 对于现代虚拟机而言，NVMe比SCSI/SATA更快。 |
| 生产环境网卡 | vmxnet3 | 采用虚拟化技术，性能最佳。 |
| 安装过程使用的网卡 | E1000 | 内核内置驱动程序，无需额外固件。 |
| 启动模式 | BIOS | 更适合自动化安装。 |
| 磁盘配置方式 | 精简配置（Thin Provisioning） | 节省数据存储空间。 |

## 预安装配置的要点

- **语言设置**：`de_DE.UTF-8`，键盘语言为德语，时区设置为`Europe/Berlin`。
- **分区设置**：自动分区，创建一个根分区和一个交换分区。
- **安装的软件包**：`open-vm-tools`、`curl`、`sudo`、`qemu-guest-agent`、`cloud-guest-utils`。
- **SSH配置**：允许`root`用户登录（`PermitRootLogin yes`），启用密码认证（`PasswordAuthentication yes`）。
- **禁用的模块**：`floppy`、`pcspkr`（防止虚拟机出现I/O错误）。

您可以根据需要修改`esxi-deploy.sh`脚本中的`preseed`配置文件，以适应不同的语言环境或软件包需求。

## 安全注意事项

- **凭证管理**：所有敏感信息均通过环境变量传递，不会被嵌入到URL或进程参数中。`govc`脚本使用`GOVC_USERNAME`/`GOVC_PASSWORD`环境变量来存储凭据。
- **SSH访问**：脚本使用`sshpass`进行自动化SSH连接。在生产环境中，建议使用基于SSH密钥的认证方式。
- **串行控制台**：Telnet传输是明文的。请确保串行端口的IP地址设置为ESXi主机的IP地址，而不是`0.0.0.0`。可以通过以下方式限制访问：
  - ESXi防火墙规则（将`remoteSerialPort`端口仅允许受信任的IP地址访问）。
  - 实施网络隔离或使用VPN。
  - 调试完成后关闭串行端口。
- **密码处理**：虚拟机密码会显示在标准输出中。在生产环境中，建议将输出重定向到安全的存储位置或使用专门的凭证管理系统。
- **建议在实验室环境中测试**：在实际生产环境使用前，请先在实验室环境中进行测试，并仔细检查所有脚本。

## 需注意的问题

- **预安装脚本中的heredoc文件**：在预安装脚本中使用shell扩展命令时，可能会导致嵌套的heredoc文件格式损坏。建议使用`echo -e`命令或单行命令来替代。
- **串行控制台仅在安装完成后可用**：Debian安装程序默认使用VGA显示器；串行输出仅在系统启动时（GRUB和内核加载阶段）生效。
- **ESXi防火墙设置**：默认情况下，ESXi防火墙会阻止串行连接。请确保`remoteSerialPort`规则已启用。
- **不要在运行中调整MBR分区**：如果使用扩展分区或交换分区，建议使用`growpart`命令调整分区大小，或者重新部署虚拟机。
- **E1000网卡的移除**：脚本会在安装完成后自动处理这一操作。

## 参考资料

- [references/preseed-template.cfg](references/preseed-template.cfg) — 完整的预安装配置模板。
- [references/vmx-template.md] — VMX网络配置参考文档。