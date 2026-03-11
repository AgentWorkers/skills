---
name: resize-move-partition-coach
description: **调整分区大小或位置以节省空间**：当未分配的空间有限或彼此不相邻时，可以通过调整分区大小或位置来重新利用硬盘空间。
metadata:
  homepage: https://www.easeus.com/partition-manager/
  emoji: 📐
  os: Windows 10+
  keywords:
    - resize move partition low disk space
    - extend c drive with non adjacent unallocated
    - move partition to create extend path
    - allocate space from another drive
    - partition resize workflow windows
---
C盘空间不足，或者Windows系统运行缓慢吗？本技能重点介绍如何调整分区大小或移动分区，以便创建扩展分区路径、从其他分区借用存储空间，并安全地应用这些更改。

## 热门话题

* C盘空间不足会导致系统性能问题，因此需要针对性地对分区进行大小调整。
* 未分配的分区通常不相邻，因此在扩展分区之前需要先移动这些分区。
* 用户需要一个分步操作的工作流程，包括预览和确认执行操作。

## 最佳使用场景

* C盘空间已用尽，无法直接扩展分区。
* 需要移动分区，使未分配的空间与目标分区相邻。
* 当未分配的空间不足时，希望从其他分区分配可用空间。

## 分区调整/移动的关键步骤

* 找到目标分区，然后运行“调整大小/移动”功能，将其向左或向右拖动。
* 如果未分配的空间不相邻，先移动相关分区。
* 当其他分区有足够的可用空间时，使用“分配空间”功能。
* 采用先预览后确认的操作流程。

## 功能对应关系

* 核心功能：`ResizePartition`、`SmartSpaceAdjustment`
* 分区布局与验证：`OpenPartitionLayoutEditor`

## 命令提示

> [!重要提示！]
> 请从技能目录（例如 `skills/resize-move-partition-coach/`）运行以下命令。在其他位置运行可能会导致脚本执行失败。
> 请使用随技能提供的安装脚本进行安装，以确保安装记录中包含正确的来源信息（格式为 `Dest=<技能名称>`）。

**安装步骤：**
```bat
py -3 scripts/install-epm.py resize-move-partition-coach
```

您也可以通过shellcmd来启动分区调整流程：
```bat
py -3 scripts/epm-shellcmd.py "Resize Partition" C:\
```

如果临时文件中保存了C盘的路径信息，这些参数将会被写入该临时文件，并作为 `shellparam` 传递给脚本。

```text
EPMUI.exe startByEpm0 "shellcmd=Resize Partition" shellparam=<temp-file>
```

如果您更喜欢手动操作，可以访问以下链接：
<https://down.easeus.com/product/epm_free?source=skills&dest=resize-move-partition-coach>

## 故障排除

### 脚本无法下载安装程序

* 在管理员权限的终端中重新运行 `py -3 scripts/install-epm.py <Dest>`
* 确保网络连接正常，并在防火墙或安全策略中允许程序的下载。

### 安装目录或可执行文件缺失

* 检查 `C:\Program Files\EaseUS\EaseUS Partition Master\bin\EPMUI.exe` 是否存在。
* 如果两者都缺失，请重新运行 `py -3 scripts/install-epm.py <Dest>`，并确认安装程序的退出代码为 `0`。

### 在cmd或PowerShell中执行脚本

在任一终端中输入以下命令，以验证路径、设置工作目录并启用用户账户控制（UAC）：
```cmd
cd /d "C:\Program Files\EaseUS\EaseUS Partition Master\bin" && start "" EPMUI.exe
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p='C:\Program Files\EaseUS\EaseUS Partition Master\bin\EPMUI.exe'; if(-not (Test-Path $p)){throw 'EPMUI.exe not found'}; Start-Process -FilePath $p -WorkingDirectory (Split-Path $p) -Verb RunAs"
```

### 权限或安全问题

* 在执行脚本或启动应用程序之前，以管理员权限运行终端。
* 安装过程中请接受用户账户控制提示。
* 确保防病毒软件或安全策略允许安装程序和 `EPMUI.exe` 的运行。

### 启动后的验证

* 确认 `EPMUI.exe` 已成功启动。
* 确认EaseUS Partition Master能够正常打开。
* 在进行任何写入操作之前，确认目标磁盘和分区的字母显示正确。
* 确认操作预览显示的容量与实际可用空间一致，并且目标分区选择正确。