---
name: x-uptime
description: >
  **增强后的“Uptime”功能：** 提供结构化的 YAML 输出，显示系统运行时间（Uptime）、用户数量以及每15分钟的平均负载（load average）。
  **依赖项说明：**  
  此功能依赖于 `x-cmd` 模块。请先安装 `x-cmd`（具体安装方法请参阅相关文档）。
license: Apache-2.0
compatibility: POSIX Shell

metadata:
  author: Li Junhao
  version: "1.0.0"
  category: x-cmd-extension
  tags: [x-cmd, system, uptime, load]
---
# x uptime - 系统运行时间与负载监测

> 改进了 `uptime` 命令，支持结构化的 YAML 输出格式，并具备跨平台运行能力。

---

## 快速入门

```bash
# YAML format output (default)
x uptime

# Raw uptime command output
x uptime --raw
```

---

## 主要特性

- **结构化的 YAML 输出**：易于解析和阅读
- **负载平均值**：提供 1 分钟、5 分钟和 15 分钟的负载趋势数据
- **跨平台支持**：支持 Linux、macOS 和 Windows（通过 cosmo/busybox）
- **自动检测**：根据系统环境自动选择使用原生 `uptime` 命令、busybox 或 cosmo 作为后端服务

---

## 输出字段

| 字段 | 描述 | 示例 |
|-------|-------------|---------|
| `time` | 当前系统时间 | `14:32:10` |
| `up` | 系统运行时间 | `5 天 3 小时 27 分钟` |
| `users` | 登录用户数量 | `2 个用户` |
| `load` | 负载平均值（1 分钟、5 分钟、15 分钟） | `0.52, 0.58, 0.59` |

---

## 命令说明

| 命令 | 功能 |
|---------|-------------|
| `x uptime` | 以 YAML 格式输出结果（默认格式） |
| `x uptime --yml` | 明确指定输出为 YAML 格式 |
| `x uptime --raw` | 以原始数据格式输出系统运行时间 |

---

## 使用示例

### 基本用法

```bash
# Default YAML output
x uptime

# Output example:
# time  : 14:32:10
# up    : 5 days, 3 hours, 27 minutes
# users : 2 users
# load  : 0.52, 0.58, 0.59
```

### 原始数据输出

```bash
# Traditional uptime output
x uptime --raw
# 14:32:10 up 5 days, 3:27, 2 users, load average: 0.52, 0.58, 0.59
```

### 数据解析方法

```bash
# Extract uptime
x uptime | awk -F': ' '/^up/{print $2}'

# Get load average
x uptime | awk -F': ' '/^load/{print $2}'
```

---

## 理解负载平均值

负载平均值反映了系统的繁忙程度——即系统中等待 CPU 或 I/O 资源的进程数量：

| 值 | 含义 |
|-------|----------------|
| `< 1.0` | 系统有空闲资源 |
| `≈ 1.0` | 系统已满负荷运行 |
| `> 1.0` | 有进程正在等待资源（形成队列） |

这三个数值分别表示：
- **1 分钟内的负载情况**：短期负载趋势 |
- **5 分钟内的负载情况**：中期负载趋势 |
- **15 分钟内的负载情况**：长期负载趋势 |

### 多核系统

对于多核系统，需要将负载值除以核心数量来得到更准确的负载指标：

```bash
# 4-core system with load 3.2
effective_load = 3.2 / 4 = 0.8  # Still has capacity
```

---

## 平台说明

### Linux
- 使用原生的 `uptime` 命令
- 全部功能均得到支持

### macOS
- 使用原生的 `uptime` 命令
- 全部功能均得到支持

### Windows
- 没有原生的 `uptime` 命令
- 系统会自动使用 cosmo 或 busybox 作为负载监测工具

---

## 相关信息

- 原生 `uptime(1)` 命令的官方文档