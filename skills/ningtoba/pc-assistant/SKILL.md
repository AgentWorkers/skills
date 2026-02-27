---
name: pc-assistant
description: >
  **PC健康检查与诊断工具**  
  提供详细的系统信息及可操作的修复建议，适用于Windows、macOS和Linux系统。仅支持系统诊断功能（无修改系统设置的权利）。支持通过`cron`任务定时执行检查。
author: Muhammad Hakim
---
# PC Assistant - 健康检查功能

## 概述

该功能会执行全面的PC健康检查，提供详细的系统信息以及针对发现问题的可操作性建议。**支持Windows、macOS和Linux系统。**

## 使用场景

- 用户请求进行“PC健康检查”、“系统检查”或“诊断”。
- 用户想要查看存储空间、CPU、内存、GPU或网络状态。
- 用户询问“我的PC运行状况如何？”或“一切正常吗？”。
- 用户需要具体的建议来解决问题（例如磁盘空间不足）。

## 系统要求

- **平台**：Windows、macOS或Linux（包括WSL）。
- **权限**：大多数检查需要具有只读权限。
- **使用的工具**：平台特定的系统工具。

## 执行健康检查

该功能会自动检测您的操作系统，并运行相应的脚本：

```bash
~/.npm-global/lib/node_modules/openclaw/skills/pc-assistant/scripts/healthcheck.sh    # Linux/WSL
~/.npm-global/lib/node_modules/openclaw/skills/pc-assistant/scripts/healthcheck.ps1   # Windows
~/.npm-global/lib/node_modules/openclaw/skills/pc-assistant/scripts/healthcheck.command  # macOS
```

或者使用自动检测操作系统的便捷封装脚本：

```bash
~/.npm-global/lib/node_modules/openclaw/skills/pc-assistant/scripts/run.sh
```

脚本输出结果包括：
- `healthcheck_YYYYMMDD_HHMMSS.txt`：包含建议的完整人类可读报告。
- `healthcheck_YYYYMMDD_HHMMSS.json`：JSON格式的摘要报告。

## 平台特定功能

### Linux/WSL
- 系统概览（操作系统、内核、运行时间）
- 存储与磁盘（df、分区、SMART信息）
- 网络（接口、路由、DNS、端口）
- 进程与服务（systemctl）
- 用户与安全（SSH密钥、登录失败记录）
- 包管理（apt、npm、pip）
- 容器（Docker、Podman）
- GPU信息（nvidia-smi）
- 硬件信息（USB、PCI、温度）

### Windows（PowerShell）
- 系统概览（Win32_OperatingSystem）
- CPU与内存（Win32_Processor、Win32_OperatingSystem）
- 存储（Win32_LogicalDisk）
- 网络适配器
- 进程（Get-Process）
- 服务（Get-Service）
- 安装的软件（注册表）
- 安全设置（防火墙、Windows Defender）
- 事件日志

### macOS
- 系统概览（sw_vers、system_profiler）
- CPU与内存（vm_stat、sysctl）
- 存储（diskutil）
- 网络（ifconfig、airport）
- 进程（ps）
- 启动的代理与后台进程
- 安全设置（防火墙、Gatekeeper、FileVault）
- Homebrew软件包
- 电池状态

## 健康检查的内容

| 部分 | 信息内容 |
|---------|-------------|
| **系统概览** | 操作系统、内核、运行时间、用户信息、Shell版本 |
| **CPU** | 型号、核心数量、速度、使用率 |
| **内存** | 总容量、可用容量、使用量、使用百分比 |
| **存储** | 磁盘使用情况、分区信息、SMART状态 |
| **网络** | 网络接口、IP地址、DNS设置 |
| **进程** | 占用CPU/内存最多的进程 |
| **服务** | 正在运行/停止的服务 |
| **安全** | 防火墙状态、防病毒软件状态 |
| **软件** | 安装的软件与应用程序 |
| **硬件** | GPU信息、USB设备、温度 |

## 包含的建议

当检测到问题时，报告会自动提供具体的建议：

### 存储问题（磁盘空间不足）
- 需要检查的特定文件夹
- 平台特定的清理指令
- Docker/容器清理命令

### 内存问题
- 如何释放RAM
- 应关闭哪些应用程序

### 一般维护建议
- 系统更新命令
- 安全最佳实践

## 定时检查（Cron作业）

该功能包含一个定时脚本，用于自动执行定期健康检查：

### 快速入门

```bash
# Run with defaults (saves to /tmp/pc-healthcheck-reports)
~/.npm-global/lib/node_modules/openclaw/skills/pc-assistant/scripts/schedule.sh

# Custom output folder
PC_ASSISTANT_OUTPUT_DIR="$HOME/Downloads/pc-assistant reports" \
  ~/.npm-global/lib/node_modules/openclaw/skills/pc-assistant/scripts/schedule.sh
```

### 配置选项

在`~/.config/pc-assistant.conf`文件中创建配置文件：

```bash
# Output directory for reports
PC_ASSISTANT_OUTPUT_DIR="$HOME/Downloads/pc-assistant reports"

# Report filename prefix
PC_ASSISTANT_REPORT_PREFIX="HealthCheck"

# Days to keep old reports (default: 30)
PC_ASSISTANT_KEEP_DAYS=30

# Enable automatic cleanup of old reports
PC_ASSISTANT_CLEANUP=true
```

### 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `PC_ASSISTANT_OUTPUT_DIR` | `/tmp/pc-healthcheck-reports` | 报告保存路径 |
| `PC_ASSISTANT_REPORT_PREFIX` | `HealthCheck` | 报告文件前缀 |
| `PC_ASSISTANTKEEP_DAYS` | `30` | 报告保留天数 |
| `PC_ASSISTANT_CLEANUP` | `false` | 是否自动删除旧报告 |
| `PC_ASSISTANT_CONFIG` | `~/.config/pc-assistant.conf` | 配置文件路径 |

### Cron作业示例

```bash
# Add to crontab (runs daily at midnight)
0 0 * * * PC_ASSISTANT_OUTPUT_DIR="$HOME/Downloads/pc-assistant reports" \
  ~/.npm-global/lib/node_modules/openclaw/skills/pc-assistant/scripts/schedule.sh
```

## 报告输出位置

报告保存路径如下：
- **Linux/WSL**：`/tmp/pc-healthcheck/`（或通过配置文件自定义）
- **Windows**：`$env:TEMP\pc-healthcheck\`（通常为`C:\Users\...\AppData\Local\Temp\pc-healthcheck\`）
- **macOS**：`/tmp/pc-healthcheck/`

使用定时任务时，输出文件为`HealthCheck_YYYYMMDD_HHMMSS.txt`和`.json`。

## 使用提示

- 该脚本为只读文件，多次运行是安全的。
- 报告会带有时间戳以便历史记录。
- 使用JSON格式的输出便于与监控系统集成。
- 将`PC_ASSISTANT_CLEANUP`设置为`true`可自动删除旧报告。