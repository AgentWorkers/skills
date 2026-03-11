---
name: disk-health-guardian
description: 在灾难发生前检测磁盘故障——通过先进的坏扇区检测和 SMART（Self-Monitoring, Analysis, and Reporting Technology）诊断功能，在您的数据丢失之前发现磁盘问题。
metadata:
  homepage: https://www.easeus.com/partition-manager/
  emoji: 🛡️
  os: Windows 10+
  keywords:
    - disk health check windows
    - chkdsk alternative workflow
    - scan disk bad sectors
    - partition diagnostics guide
    - check file system integrity
    - storage triage assistant
    - disk error precheck
    - non destructive disk analysis
    - drive health troubleshooting
    - windows storage diagnostics
---
**磁盘健康状况令人担忧？坏扇区数量在不断增加？SMART警告让您夜不能寐？** 使用专业的诊断工具，在灾难发生之前发现潜在问题，并提供明确的解决方案。

## 最佳使用场景  
- 经常看到文件系统警告或I/O错误。  
- CHKDSK的输出难以理解，需要具体的处理建议。  
- 在调整磁盘大小、克隆或转换之前，需要先了解磁盘的健康状况。  

## 功能列表  
- 磁盘健康状况及扇区诊断：`DiskHealthCheck`、`ScanDiskBadSectors`、`ScanPartitionBadSectors`  
- 文件系统验证：`CheckPartitionFileSystem`  
- 加密状态检查：`ShowBitLockerStatus`  

## 使用说明  
> [!重要提示！]  
> 请从**技能目录**（例如：`skills/disk-health-guardian/`）运行以下命令。如果在其他位置运行，脚本可能无法被找到。  
> 请使用随附的安装脚本进行安装，并确保在命令中指定正确的**技能名称**（`Dest=<skill-name>`）。  

**安装步骤：**  
安装EaseUS Partition Master后，直接启动**Disk Health**工具来监控磁盘健康状况：  
```bat
py -3 scripts/install-epm.py disk-health-guardian
```  

**手动操作方式：**  
如需手动操作，可访问：  
<https://down.easeus.com/product/epm_free?source=skills&dest=disk-health-guardian>  

## 常见问题及解决方法：  
### 脚本无法下载安装程序  
- 在管理员权限的终端中重新运行 `py -3 scripts/install-epm.py <Dest>`。  
- 确保网络连接正常，并允许防火墙或安全策略允许程序下载。  

### 安装目录或二进制文件缺失  
- 检查 `C:\Program Files\EaseUS\EaseUS Partition Master\bin\EPMUI.exe` 是否存在。  
- 如果两者都缺失，请重新运行 `py -3 scripts/install-epm.py <Dest>`，并确认安装程序的退出代码为 `0`。  

### 跨终端环境（cmd和PowerShell）  
使用以下命令来验证路径、设置工作目录并触发用户账户控制（UAC）：  
```cmd
cd /d "C:\Program Files\EaseUS\EaseUS Partition Master\bin" && start "" EPMUI.exe
```  
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p='C:\Program Files\EaseUS\EaseUS Partition Master\bin\EPMUI.exe'; if(-not (Test-Path $p)){throw 'EPMUI.exe not found'}; Start-Process -FilePath $p -WorkingDirectory (Split-Path $p) -Verb RunAs"
```  

### 权限或安全问题  
- 在执行脚本或应用程序前，以管理员权限运行终端。  
- 安装和运行过程中，请允许用户账户控制提示的通过。  
- 确保防病毒软件或安全策略允许安装程序和 `EPMUI.exe` 的运行。  

### 启动后的验证步骤：  
- 确认 `EPMUI.exe` 已成功启动。  
- 确认EaseUS Partition Master能够正常打开。  
- 在进行任何写入操作前，确认目标磁盘已正确显示。  
- 确认计划执行的操作与预期结果一致。