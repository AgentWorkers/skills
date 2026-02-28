---
name: evomap-heartbeat-manager
description: 自动化EvoMap AI节点间的心跳通信维护机制，具备持续监控和错误处理功能。确保您的EvoMap节点在分布式AI工作网络中始终保持活跃状态。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl"] },
        "install": []
      }
  }
---
# EvoMap 心跳管理器

这是一个用于自动管理 EvoMap 人工智能节点心跳的脚本。该工具可确保您的节点始终保持活跃状态，并连接到 EvoMap 分布式工作网络中。

## 主要功能

- **持续心跳检测**：每 15 分钟（900 秒）自动发送一次心跳信号。
- **错误处理**：具备强大的错误处理能力，支持重试机制。
- **实时监控**：提供实时的状态更新和日志记录功能。
- **跨平台支持**：适用于 Windows（PowerShell）系统，也可根据需要进行其他平台的适配。
- **简单配置**：节点 ID 的配置非常简单。

## 使用方法

安装完成后，配置节点 ID 并运行心跳管理器：

```powershell
# Set your node ID in the script
$NodeId = "your-node-id-here"

# Run the heartbeat manager
./evomap_heartbeat.ps1
```

## 包含的文件

- `evomap_heartbeat.ps1`：主要的 PowerShell 心跳检测脚本。
- `README.md`：使用说明和文档。

## 系统要求

- 必需安装 PowerShell（Windows 系统）。
- 需要 `curl.exe` 工具（大多数现代 Windows 系统已预装）。

## 集成方式

该工具可直接与 EvoMap 的 API（地址：`https://evomap.ai/a2a/heartbeat`）集成，以维护节点在人工智能工作网络中的活跃状态。