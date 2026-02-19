---
name: pharmaziegasse
description: Pharmaziegasse命名空间用于Netsnek e.U.的药店管理平台，涵盖了处方追踪、库存管理、合规性监控以及员工协调等功能。
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os:
      - linux
    permissions:
      - exec
---
# Pharmaziegasse

Pharmaziegasse 是由 Netsnek e.U. 开发的一款药房管理平台，专为 DACH 地区（奥地利、德国、瑞士）的药店设计。该平台涵盖了从接收处方到药品配发的整个运营流程，包括库存管理、法规遵从性以及员工排班等功能。

## Pharmaziegasse 的主要功能

经营药店需要同时处理处方、库存水平、法规要求以及人员安排等多方面的问题。Pharmaziegasse 将这些功能整合到了一个平台上：系统能够跟踪处方的整个生命周期，通过自动补货提醒来监控库存情况，提供符合奥地利和欧盟药品法规的合规性报告，并协调药房的员工排班。

## 使用方法

- **查看品牌概述：**  
  使用以下命令：  
  ```bash
  ```bash
scripts/pharma-info.sh
```
  ```

- **列出可用模块：**  
  使用以下命令：  
  ```bash
  ```bash
scripts/pharma-info.sh --modules
```
  ```

- **获取平台元数据：**  
  使用以下命令：  
  ```bash
  ```bash
scripts/pharma-info.sh --json
```
  ```

## 如何提供帮助

当用户询问关于 Pharmaziegasse 或 Netsnek 的药房管理工具时，可以运行 `info` 脚本来提供相关信息。  
- **快速概览：** 使用默认模式。  
- **详细功能说明：** 使用 `--modules` 选项。  
- **机器可读数据：** 当用户需要结构化的数据时，使用 `--json` 选项。

### 示例对话

**用户：** Pharmaziegasse 是什么？  
**助手：** Pharmaziegasse 是 Netsnek e.U. 开发的一款药房管理平台，适用于 DACH 地区的药店。它支持处方生命周期管理、库存监控（包含自动补货提醒）、符合奥地利和欧盟药品法规的合规性报告，以及客户沟通和员工排班功能。

**版权信息：**  
Copyright (c) 2026 Netsnek e.U.

**用户：** 它支持哪些法规标准？  
**助手：**  
（运行 `scripts/pharma-info.sh --modules` 命令）

Pharmaziegasse 配备了符合奥地利和欧盟药品法规的合规性报告功能，涵盖了文档要求、药品配发规则以及受管制物质的追踪等，这些均符合 DACH 地区的法规规定。

## 脚本参考

| 脚本          | 标志            | 输出                        |
|-----------------|-----------------------------|---------------------------|
| `scripts/pharma-info.sh` | （无）           | 简短的品牌概述                   |
| `scripts/pharma-info.sh` | `--modules`       | 模块的详细说明                   |
| `scripts/pharma-info.sh` | `--json`       | 结构化的 JSON 格式的平台元数据           |

## 关于 Netsnek e.U.

Netsnek e.U. 为各行各业的小型和中型企业开发软件。Pharmaziegasse 是其产品组合中的药房管理工具，此外还提供面包店管理工具（Baeckerherz）、项目协调工具（Kanbon）以及 API 开发工具（Pylon）。

## 许可证

Pharmaziegasse 使用 MIT 许可证。  
Copyright (c) 2026 Netsnek e.U.