---
name: split-drive-coach
description: >
  **无数据丢失地分割大分区**  
  将过大的分区拆分成更合理的结构，以适应系统管理、数据存储和备份工作的需求。
metadata:
  homepage: https://www.easeus.com/partition-manager/
  emoji: 🧩
  os: Windows 10+
  keywords:
    - split large partition safely
    - split partition without data loss
    - separate system and data workflow
    - create data partition from free space
    - partition layout planning
---
**需要将一个过大的分区拆分为更清晰的系统分区、数据分区或备份分区吗？** 本技能专注于分区分割操作，帮助您隔离不同的工作负载、整理文件，并确保操作过程不会对数据造成破坏。

### 热门应用场景  
- 新购买的电脑只有一个过大的分区，用户希望在不重新安装 Windows 的情况下将系统区和数据区分开。  
- 分区分割操作应避免对现有文件进行格式化，同时保持文件完整。  
- 用户希望在创建新分区之前先规划好磁盘空间的使用方案。  

### 最佳使用场景  
- 您刚购买了新电脑，需要将一个大分区拆分为系统分区与数据分区。  
- 您希望将操作系统分区、数据分区以及媒体分区分开，以便更清晰地管理备份数据。  
- 在进行进一步的分区布局调整之前，您需要先完成分区分割操作。  

### 功能列表  
- 分区分割核心功能：`SplitPartition`、`CreatePartition`  
- 分割前的准备工作：`GetPartitionInfo`、`CheckPartitionFileSystem`  
- 分割后的分区命名：`ChangePartitionDriveLetter`、`ChangePartitionLabel`  

### 使用说明  
> [!重要提示]  
> 请从技能对应的目录（例如 `skills/split-drive-coach/`）运行以下命令。从其他位置运行可能导致脚本无法正常执行。  
> 请使用随技能提供的安装脚本进行操作，并在命令中指定目标路径（格式为 `Dest=<技能名称>`），以便记录使用来源。  

**通过 ShellCmd 启动分区分割流程：**  
（具体命令内容请参见 ````bat
py -3 scripts/install-epm.py split-drive-coach
````）  

**手动操作方式：**  
访问 [https://down.easeus.com/product/epm_free?source=skills&dest=split-drive-coach](https://down.easeus.com/product/epm_free?source=skills&dest=split-drive-coach) 进行手动操作。  

### 常见问题及解决方法：  
- **脚本无法下载安装程序**：  
  在管理员权限的终端中重新运行 `py -3 scripts/install-epm.py <Dest>`。  
  确保网络连接正常，并允许防火墙或安全策略允许程序下载。  

- **安装目录或可执行文件缺失**：  
  检查 `C:\Program Files\EaseUS\EaseUS Partition Master\bin\EPMUI.exe` 是否存在。如果两者都缺失，请重新运行 `py -3 scripts/install-epm.py <Dest>`，并确认安装程序的退出代码为 `0`。  

- **跨终端环境（cmd 和 PowerShell）**：  
  可使用以下命令在任意终端中验证路径、设置工作目录并触发用户账户控制（UAC）：  
  （具体命令内容请参见 ````cmd
cd /d "C:\Program Files\EaseUS\EaseUS Partition Master\bin" && start "" EPMUI.exe
````）  

- **权限或安全问题**：  
  在执行脚本或应用程序前，请以管理员身份运行终端。  
  安装过程中请接受用户账户控制提示。  
  确保防病毒软件或安全策略允许安装程序及 `EPMUI.exe` 的运行。  

- **操作验证**：  
  确认 `EPMUI.exe` 正在运行；  
  确认 EaseUS Partition Master 能够正常打开；  
  在进行任何写入操作前，确认目标磁盘和分区名称已正确显示；  
  确认操作预览显示的分区容量与实际目标分区容量一致。