---
name: unraid
version: 1.0.1
description: "通过 GraphQL API 查询和监控 Unraid 服务器。当用户请求“检查 Unraid 状态”、“监控 Unraid 服务器”、“使用 Unraid API”、“获取 Unraid 服务器信息”、“查看磁盘温度”、“读取 Unraid 日志”、“列出 Unraid 共享资源”、“查看 Unraid 阵列状态”、“管理 Unraid 容器”或提及 Unraid 系统监控、磁盘健康状况、奇偶校验或服务器状态时，可使用此功能。"
---

# Unraid API 使用指南

您可以使用 GraphQL API 来查询和监控 Unraid 服务器。该 API 提供了 27 个只读端点，用于系统监控、磁盘健康状况、日志记录、容器管理、虚拟机（VM）等功能的查询。

## 快速入门

请设置您的 Unraid 服务器凭据：

```bash
export UNRAID_URL="https://your-unraid-server/graphql"
export UNRAID_API_KEY="your-api-key"
```

**获取 API 密钥：**  
进入 “设置” → “管理访问” → “API 密钥” → 点击 “创建”（选择 “查看者” 角色）。

您可以使用以下辅助脚本来执行任何查询操作：

```bash
./scripts/unraid-query.sh -q "{ online }"
```

或者直接运行示例脚本：

```bash
./scripts/dashboard.sh              # Complete multi-server dashboard
./examples/disk-health.sh           # Disk temperatures & health
./examples/read-logs.sh syslog 20   # Read system logs
```

## 核心概念

### GraphQL API 结构

Unraid 7.2 及更高版本使用 GraphQL（而非 REST）作为接口协议。主要特点包括：
- **统一接口：** 所有查询都通过 `/graphql` 端点进行。
- **精确请求：** 在查询中明确指定所需的数据字段。
- **类型强校验：** 利用 GraphQL 的类型系统来确保数据格式的正确性。
- **无法访问容器日志：** Docker 容器的输出日志无法通过 API 获取。

### 两种数据资源

- **`info`**：包含静态硬件信息（如 CPU 型号、核心数量、操作系统版本等）。
- **`metrics`**：提供实时系统性能数据（如 CPU 使用率、内存使用率、当前负载等）。

建议使用 `metrics` 端点进行监控，而使用 `info` 端点获取硬件规格信息。

## 常见操作

### 系统监控

- **检查服务器是否在线：**  
```bash
./scripts/unraid-query.sh -q "{ online }"
```

- **获取 CPU 和内存使用情况：**  
```bash
./scripts/unraid-query.sh -q "{ metrics { cpu { percentTotal } memory { used total percentTotal } } }"
```

- **查看完整仪表盘信息：**  
```bash
./scripts/dashboard.sh
```

### 磁盘管理

- **检查磁盘健康状况和温度：**  
```bash
./examples/disk-health.sh
```

- **获取磁盘阵列状态：**  
```bash
./scripts/unraid-query.sh -q "{ array { state parityCheckStatus { status progress errors } } }"
```

- **列出所有物理磁盘（包括缓存磁盘和 USB 磁盘）：**  
```bash
./scripts/unraid-query.sh -q "{ disks { name } }"
```

### 存储共享

- **列出网络共享资源：**  
```bash
./scripts/unraid-query.sh -q "{ shares { name comment } }"
```

### 日志记录

- **列出可用的日志文件：**  
```bash
./scripts/unraid-query.sh -q "{ logFiles { name size modifiedAt } }"
```

- **读取日志内容：**  
```bash
./examples/read-logs.sh syslog 20
```

### 容器和虚拟机

- **列出 Docker 容器：**  
```bash
./scripts/unraid-query.sh -q "{ docker { containers { names image state status } } }"
```

- **列出虚拟机：**  
```bash
./scripts/unraid-query.sh -q "{ vms { name state cpus memory } } }"
```

**注意：** 容器的输出日志无法通过 API 获取，需要通过 SSH 使用 `docker logs` 命令来查看。

### 通知功能

- **获取通知记录数量：**  
```bash
./scripts/unraid-query.sh -q "{ notifications { overview { unread { info warning alert total } } } }"
```

## 辅助脚本的使用

`scripts/unraid-query.sh` 是一个实用的辅助脚本，可用于执行各种查询操作：

```bash
# Basic usage
./scripts/unraid-query.sh -u URL -k API_KEY -q "QUERY"

# Use environment variables
export UNRAID_URL="https://unraid.local/graphql"
export UNRAID_API_KEY="your-key"
./scripts/unraid-query.sh -q "{ online }"

# Format options
-f json    # Raw JSON (default)
-f pretty  # Pretty-printed JSON
-f raw     # Just the data (no wrapper)
```

## 额外资源

- **参考文档：**  
- **`references/endpoints.md`：包含所有 27 个 API 端点的完整列表。  
- **`references/troubleshooting.md`：介绍常见错误及其解决方法。  
- **`references/api-reference.md`：提供详细的字段说明。  

### 辅助脚本示例

- **`scripts/unraid-query.sh`：主要的 GraphQL 查询工具。  
- **`scripts/dashboard.sh`：用于自动收集多台服务器的监控数据的脚本。  

## 常用命令参考

```bash
# System status
./scripts/unraid-query.sh -q "{ online metrics { cpu { percentTotal } } }"

# Disk health
./examples/disk-health.sh

# Array status
./scripts/unraid-query.sh -q "{ array { state } }"

# Read logs
./examples/read-logs.sh syslog 20

# Complete dashboard
./scripts/dashboard.sh

# List shares
./scripts/unraid-query.sh -q "{ shares { name } }"

# List containers
./scripts/unraid-query.sh -q "{ docker { containers { names state } } }"
```