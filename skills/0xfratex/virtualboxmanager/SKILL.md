---
name: virtualbox
description: "您可以直接通过 openclaw 来控制和管理 VirtualBox 虚拟机。使用 VBoxManage CLI 可以启动、停止、创建快照、克隆、配置以及监控虚拟机。该工具支持完整的虚拟机生命周期管理功能，包括虚拟机的创建、网络配置、共享文件夹设置以及性能监控等。"
homepage: https://www.virtualbox.org/manual/ch08.html
metadata: {"openclaw":{"emoji":"🖥️","requires":{"bins":["VBoxManage"]}}}
---
# VirtualBox 技能

您可以使用 `VBoxManage` 命令行接口直接从 openclaw 控制和管理 VirtualBox 虚拟机。该技能提供了全面的虚拟机生命周期管理、配置和监控功能。

## 设置

### 先决条件
1. 主机系统上必须已安装 VirtualBox。
2. 必须能够访问 `VBoxManage` 命令行接口（通常在安装 VirtualBox 后会自动添加到 PATH 环境变量中）。
3. 用户必须具有控制虚拟机的相应权限。

### 验证安装
```bash
VBoxManage --version
```

### 常见路径
- **Linux**: `/usr/bin/VBoxManage` 或 `/usr/local/bin/VBoxManage`
- **macOS**: `/Applications/VirtualBox.app/Contents/MacOS/VBoxManage`
- **Windows**: `C:\Program Files\Oracle\VirtualBox\VBoxManage.exe`

## 核心功能

### 虚拟机生命周期管理
- 创建、启动、停止、暂停和删除虚拟机
- 管理虚拟机状态（运行中、暂停、已保存、已关闭）
- 强制停止和 ACPI 关机选项
- 重置和重启虚拟机

### 配置管理
- 修改虚拟机设置（CPU、内存、存储）
- 配置网络适配器和模式
- 设置共享文件夹
- 管理 USB 设备的透传功能

### 快照与克隆
- 创建和恢复快照
- 克隆现有虚拟机
- 导出/导入虚拟机配置文件

### 监控与信息
- 列出所有虚拟机及其状态
- 获取详细的虚拟机信息
- 监控虚拟机指标和性能
- 查看日志和调试信息

## 使用方法

### 列出所有虚拟机
```bash
# List all registered VMs
VBoxManage list vms

# List running VMs only
VBoxManage list runningvms

# Get detailed info about all VMs (JSON-like output)
VBoxManage list vms --long
```

### 查看虚拟机信息
```bash
# Get detailed info about a specific VM
VBoxManage showvminfo "VM_NAME"

# Get info in machine-readable format
VBoxManage showvminfo "VM_NAME" --machinereadable
```

### 启动虚拟机
```bash
# Start VM with GUI
VBoxManage startvm "VM_NAME"

# Start VM headless (no GUI)
VBoxManage startvm "VM_NAME" --type headless

# Start VM with separate UI process
VBoxManage startvm "VM_NAME" --type separate
```

### 停止虚拟机
```bash
# ACPI shutdown (graceful, like pressing power button)
VBoxManage controlvm "VM_NAME" acpipowerbutton

# Power off (hard stop, like pulling plug)
VBoxManage controlvm "VM_NAME" poweroff

# Save state (hibernate)
VBoxManage controlvm "VM_NAME" savestate

# Pause VM
VBoxManage controlvm "VM_NAME" pause

# Resume paused VM
VBoxManage controlvm "VM_NAME" resume

# Reset VM (hard reboot)
VBoxManage controlvm "VM_NAME" reset
```

### 创建新虚拟机
```bash
# Create a new VM
VBoxManage createvm --name "NewVM" --register

# Set OS type
VBoxManage modifyvm "NewVM" --ostype "Ubuntu_64"

# Set memory (RAM in MB)
VBoxManage modifyvm "NewVM" --memory 4096

# Set CPU count
VBoxManage modifyvm "NewVM" --cpus 2

# Create a virtual disk
VBoxManage createhd --filename "/path/to/NewVM.vdi" --size 50000

# Add storage controller
VBoxManage storagectl "NewVM" --name "SATA Controller" --add sata

# Attach virtual disk
VBoxManage storageattach "NewVM" --storagectl "SATA Controller" \
  --port 0 --device 0 --type hdd --medium "/path/to/NewVM.vdi"

# Attach ISO for installation
VBoxManage storageattach "NewVM" --storagectl "SATA Controller" \
  --port 1 --device 0 --type dvddrive --medium "/path/to/install.iso"
```

### 克隆虚拟机
```bash
# Full clone (all disks copied)
VBoxManage clonevm "SourceVM" --name "ClonedVM" --register

# Linked clone (uses same base disk, saves space)
VBoxManage clonevm "SourceVM" --name "LinkedVM" --options link --register

# Clone with specific snapshot
VBoxManage clonevm "SourceVM" --name "FromSnapshotVM" \
  --snapshot "SnapshotName" --register
```

### 删除虚拟机
```bash
# Delete VM (keep disks)
VBoxManage unregistervm "VM_NAME"

# Delete VM and all associated files
VBoxManage unregistervm "VM_NAME" --delete
```

### 创建快照
```bash
# List snapshots
VBoxManage snapshot "VM_NAME" list

# Take a snapshot
VBoxManage snapshot "VM_NAME" take "SnapshotName" --description "Description here"

# Restore a snapshot
VBoxManage snapshot "VM_NAME" restore "SnapshotName"

# Delete a snapshot
VBoxManage snapshot "VM_NAME" delete "SnapshotName"

# Restore current snapshot (go back to last snapshot)
VBoxManage snapshot "VM_NAME" restorecurrent
```

### 网络配置
```bash
# List network adapters
VBoxManage showvminfo "VM_NAME" | grep -A 5 "NIC"

# Set NAT networking
VBoxManage modifyvm "VM_NAME" --nic1 nat

# Set bridged networking
VBoxManage modifyvm "VM_NAME" --nic1 bridged --bridgeadapter1 eth0

# Set host-only networking
VBoxManage modifyvm "VM_NAME" --nic1 hostonly --hostonlyadapter1 vboxnet0

# Port forwarding (NAT only)
VBoxManage modifyvm "VM_NAME" --natpf1 "ssh,tcp,,2222,,22"

# Remove port forwarding
VBoxManage modifyvm "VM_NAME" --natpf1 delete "ssh"

# List host-only networks
VBoxManage list hostonlyifs

# Create host-only network
VBoxManage hostonlyif create

# Configure host-only network
VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0
```

### 共享文件夹
```bash
# Add shared folder
VBoxManage sharedfolder add "VM_NAME" --name "share" --hostpath "/path/on/host"

# Add read-only shared folder
VBoxManage sharedfolder add "VM_NAME" --name "share" --hostpath "/path/on/host" --readonly

# Add with automount
VBoxManage sharedfolder add "VM_NAME" --name "share" --hostpath "/path/on/host" --automount

# Remove shared folder
VBoxManage sharedfolder remove "VM_NAME" --name "share"

# List shared folders
VBoxManage showvminfo "VM_NAME" | grep -A 5 "Shared Folder"
```

### 修改虚拟机设置
```bash
# Change memory allocation
VBoxManage modifyvm "VM_NAME" --memory 8192

# Change CPU count
VBoxManage modifyvm "VM_NAME" --cpus 4

# Enable/disable VRAM (video memory)
VBoxManage modifyvm "VM_NAME" --vram 128

# Enable 3D acceleration
VBoxManage modifyvm "VM_NAME" --accelerate3d on

# Enable nested virtualization
VBoxManage modifyvm "VM_NAME" --nested-hw-virt on

# Set VRDE (remote desktop) port
VBoxManage modifyvm "VM_NAME" --vrde on --vrdeport 3389

# Change VM name
VBoxManage modifyvm "VM_NAME" --name "NewName"

# Set description
VBoxManage modifyvm "VM_NAME" --description "Production server VM"
```

### USB 设备透传
```bash
# List USB devices
VBoxManage list usbhost

# Attach USB device to running VM
VBoxManage controlvm "VM_NAME" usbattach "UUID_OR_ADDRESS"

# Detach USB device
VBoxManage controlvm "VM_NAME" usbdetach "UUID_OR_ADDRESS"

# Add USB device filter (persistent)
VBoxManage usbfilter add 0 --target "VM_NAME" --name "FilterName" \
  --vendorid "XXXX" --productid "XXXX"
```

### 导出/导入虚拟机配置文件
```bash
# Export VM to OVA/OVF
VBoxManage export "VM_NAME" --output "/path/to/export.ova"

# Export multiple VMs
VBoxManage export "VM1" "VM2" --output "/path/to/export.ova"

# Import appliance
VBoxManage import "/path/to/export.ova"

# Import with options
VBoxManage import "/path/to/export.ova" --vsys 0 --vmname "ImportedVM"
```

### 监控与指标
```bash
# List available metrics
VBoxManage metrics list

# Setup metrics collection
VBoxManage metrics setup --period 10 --samples 5 "VM_NAME"

# Collect and display metrics
VBoxManage metrics collect "VM_NAME"

# Query specific metrics
VBoxManage metrics query "VM_NAME" "CPU/Load"
VBoxManage metrics query "VM_NAME" "RAM/Usage"
VBoxManage metrics query "VM_NAME" "Net/Rate"

# List all metrics for a VM
VBoxManage metrics list "VM_NAME"
```

### 存储设备管理
```bash
# List all virtual disks
VBoxManage list hdds

# Get disk info
VBoxManage showhdinfo "/path/to/disk.vdi"

# Resize virtual disk
VBoxManage modifyhd "/path/to/disk.vdi" --resize 100000

# Clone virtual disk
VBoxManage clonemedium "/path/to/source.vdi" "/path/to/clone.vdi"

# Compact disk (shrink)
VBoxManage modifymedium "/path/to/disk.vdi" --compact

# Set disk type
VBoxManage modifymedium "/path/to/disk.vdi" --type normal
VBoxManage modifymedium "/path/to/disk.vdi" --type immutable
VBoxManage modifymedium "/path/to/disk.vdi" --type writethrough
```

### 客户端控制（需要安装 Guest Additions）
```bash
# Execute command in guest
VBoxManage guestcontrol "VM_NAME" run --exe "/bin/ls" \
  --username user --password pass -- -la /home

# Copy file to guest
VBoxManage guestcontrol "VM_NAME" copyto \
  --username user --password pass \
  "/host/path/file.txt" "/guest/path/file.txt"

# Copy file from guest
VBoxManage guestcontrol "VM_NAME" copyfrom \
  --username user --password pass \
  "/guest/path/file.txt" "/host/path/file.txt"

# Create directory in guest
VBoxManage guestcontrol "VM_NAME" mkdir \
  --username user --password pass \
  "/home/user/newdir"

# Remove file in guest
VBoxManage guestcontrol "VM_NAME" rm \
  --username user --password pass \
  "/home/user/file.txt"

# List guest processes
VBoxManage guestcontrol "VM_NAME" process list \
  --username user --password pass
```

### 调试与日志
```bash
# View VM logs location
VBoxManage showvminfo "VM_NAME" | grep -i log

# Typical log paths:
# Linux/macOS: ~/VirtualBox VMs/VM_NAME/Logs/
# Windows: %USERPROFILE%\VirtualBox VMs\VM_NAME\Logs\

# Debug a VM
VBoxManage debugvm "VM_NAME" info item

# Get VM statistics
VBoxManage debugvm "VM_NAME" statistics
```

## 实用示例

### 快速检查虚拟机状态
```bash
# Check if a specific VM is running
VBoxManage list runningvms | grep "VM_NAME"

# Get all VMs with their states
VBoxManage list vms --long | grep -E "Name:|State:"
```

### 自动化虚拟机启动脚本
```bash
#!/bin/bash
# Start VMs in headless mode
for vm in "WebServer" "Database" "Cache"; do
  echo "Starting $vm..."
  VBoxManage startvm "$vm" --type headless
  sleep 10
done
echo "All VMs started"
```

### 使用快照进行备份
```bash
#!/bin/bash
VM_NAME="ProductionVM"
DATE=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_NAME="Backup_$DATE"

# Create snapshot
VBoxManage snapshot "$VM_NAME" take "$SNAPSHOT_NAME" \
  --description "Automated backup $DATE"

# Keep only last 5 snapshots
SNAPSHOTS=$(VBoxManage snapshot "$VM_NAME" list --machinereadable | grep SnapshotName | wc -l)
if [ $SNAPSHOTS -gt 5 ]; then
  OLDEST=$(VBoxManage snapshot "$VM_NAME" list --machinereadable | grep SnapshotName | head -1 | cut -d'"' -f4)
  VBoxManage snapshot "$VM_NAME" delete "$OLDEST"
fi
```

### 完整的虚拟机克隆流程
```bash
#!/bin/bash
SOURCE_VM="TemplateVM"
NEW_VM="DevVM_$(date +%s)"

# Ensure source is stopped
VBoxManage controlvm "$SOURCE_VM" poweroff 2>/dev/null

# Take a clean snapshot first
VBoxManage snapshot "$SOURCE_VM" take "PreClone"

# Clone the VM
VBoxManage clonevm "$SOURCE_VM" --name "$NEW_VM" --register

# Modify the clone
VBoxManage modifyvm "$NEW_VM" --memory 2048 --cpus 2

# Start the clone
VBoxManage startvm "$NEW_VM" --type headless

echo "Cloned VM '$NEW_VM' is now running"
```

### 设置网络端口转发
```bash
#!/bin/bash
VM_NAME="WebServer"

# SSH access
VBoxManage modifyvm "$VM_NAME" --natpf1 "ssh,tcp,,2222,,22"

# HTTP access
VBoxManage modifyvm "$VM_NAME" --natpf1 "http,tcp,,8080,,80"

# HTTPS access
VBoxManage modifyvm "$VM_NAME" --natpf1 "https,tcp,,8443,,443"

# Verify
VBoxManage showvminfo "$VM_NAME" | grep "NIC 1 Rule"
```

### 监控资源使用情况
```bash
#!/bin/bash
VM_NAME="ProductionVM"

# Setup metrics
VBoxManage metrics setup --period 5 --samples 12 "$VM_NAME"

# Collect for 1 minute and show results
sleep 60
VBoxManage metrics query "$VM_NAME" "CPU/Load:RAM/Usage:Net/Rate"
```

## 常见问题及解决方法

### 虚拟机无法启动
```bash
# Check VM state
VBoxManage showvminfo "VM_NAME" | grep State

# Check for locked files
VBoxManage showvminfo "VM_NAME" | grep -i lock

# Try starting with verbose output
VBoxManage startvm "VM_NAME" --type headless 2>&1
```

### 无法删除虚拟机
```bash
# Ensure VM is stopped
VBoxManage controlvm "VM_NAME" poweroff

# Check for attached media
VBoxManage showvminfo "VM_NAME" | grep -E "Storage|Medium"

# Force unregister if needed
VBoxManage unregistervm "VM_NAME" --delete
```

### 网络问题
```bash
# Check adapter status
VBoxManage showvminfo "VM_NAME" | grep -A 10 "NIC 1"

# Reset network adapter
VBoxManage modifyvm "VM_NAME" --nic1 none
VBoxManage modifyvm "VM_NAME" --nic1 nat

# Verify host-only interface exists
VBoxManage list hostonlyifs
```

### 性能问题
```bash
# Check current allocation
VBoxManage showvminfo "VM_NAME" | grep -E "Memory|CPU"

# Increase resources (VM must be stopped)
VBoxManage modifyvm "VM_NAME" --memory 8192 --cpus 4

# Enable hardware acceleration
VBoxManage modifyvm "VM_NAME" --hwvirtex on --nestedpaging on
```

## 重要说明

1. **包含空格的虚拟机名称**：始终使用引号来引用包含空格的虚拟机名称。
   ```bash
   VBoxManage startvm "My Production VM"
   ```

2. **UUID 与名称**：虚拟机名称和 UUID 可以互换使用。
   ```bash
   VBoxManage startvm "VM_NAME"
   VBoxManage startvm "12345678-1234-1234-1234-123456789abc"
   ```

3. **操作类型**：
   - `controlvm`：用于操作正在运行的虚拟机。
   - `modifyvm`：主要用于操作已停止的虚拟机。

4. **无图形界面模式**：在无图形界面的服务器环境中，始终使用 `--type headless` 参数。

5. **权限**：某些操作需要提升权限或属于特定用户组（例如，在 Linux 中需要 `vboxusers` 组的成员权限）。

6. **Guest Additions**：以下功能需要安装 Guest Additions：
   - 共享剪贴板
   - 拖放操作
   - 共享文件夹自动挂载
   - 客户端控制命令
   - 无缝模式

## 操作系统类型参考

`--ostype` 参数支持的常见操作系统类型：
- `Windows11_64` - Windows 11（64 位）
- `Windows10_64` - Windows 10（64 位）
- `Ubuntu_64` - Ubuntu Linux（64 位）
- `Debian_64` - Debian Linux（64 位）
- `Fedora_64` - Fedora Linux（64 位）
- `ArchLinux_64` - Arch Linux（64 位）
- `macOS_ARM64` - 在 Apple Silicon 上运行的 macOS
- `macOS_128` - 在 Intel 上运行的 macOS（64 位）
- `FreeBSD_64` - FreeBSD（64 位）
- `Other_64` - 其他 64 位操作系统

完整列表请参考：
```bash
VBoxManage list ostypes
```

## 快速参考卡

| 操作          | 命令                          |
|------------------|-----------------------------|
| 列出所有虚拟机       | `VBoxManage list vms`                |
| 启动虚拟机       | `VBoxManage startvm "名称" --type headless`       |
| 停止虚拟机       | `VBoxManage controlvm "名称" acpipowerbutton`       |
| 强制停止虚拟机     | `VBoxManage controlvm "名称" poweroff`        |
| 查看虚拟机信息     | `VBoxManage showvminfo "名称"`           |
| 创建快照       | `VBoxManage snapshot "名称" take "快照名称"`       |
| 恢复快照       | `VBoxManage snapshot "名称" restore "快照名称"`       |
| 克隆虚拟机       | `VBoxManage clonevm "源虚拟机" --名称 "新名称" --register` |
| 删除虚拟机       | `VBoxManage unregistervm "名称" --delete`        |
| 修改内存         | `VBoxManage modifyvm "名称" --memory 4096`       |
| 修改 CPU 配置     | `VBoxManage modifyvm "名称" --cpus 2`        |
| 设置端口转发     | `VBoxManage modifyvm "名称" --natpf1 "规则,tcp,,主机,,客户机"` |
| 监控资源使用情况    | `VBoxManage monitorvm "名称"`           |

## 所需软件
- **必备软件**：`VBoxManage`（作为 VirtualBox 安装的一部分）
- **权限要求**：用户必须具有虚拟机管理权限。
- **Guest Additions**：用于实现客户端控制和增强功能。