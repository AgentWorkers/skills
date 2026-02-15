---
name: unifi
description: 通过本地网关API（Cloud Gateway Max / UniFi OS）查询和监控UniFi网络。当用户请求“检查UniFi网络状态”、“列出UniFi设备”、“查看网络中的用户”、“UniFi客户端信息”、“UniFi系统健康状况”、“热门应用程序”、“网络警报”或提及UniFi监控/状态/仪表板时，可使用此功能。
version: 1.0.1
metadata:
  clawdbot:
    emoji: "📡"
    requires:
      bins: ["curl", "jq"]
---

# UniFi网络监控技能

您可以通过本地UniFi操作系统网关API来监控和查询您的UniFi网络（已在Cloud Gateway Max上进行测试）。

## 目的

此技能提供对您的UniFi网络运行数据的**只读**访问权限：
- 设备（接入点、交换机、网关）的状态和健康状况
- 当前连接的客户端信息
- 网络健康状况概览
- 流量分析（通过数据包检测技术DPI分析的主要应用程序）
- 最近的警报和事件

所有操作均为**仅GET请求**，适用于监控和报告用途。

## 设置

创建凭据文件：`~/.clawdbot/credentials/unifi/config.json`

```json
{
  "url": "https://10.1.0.1",
  "username": "api",
  "password": "YOUR_PASSWORD",
  "site": "default"
}
```

- `url`：您的UniFi操作系统网关IP地址/主机名（使用HTTPS）
- `username`：本地UniFi操作系统管理员用户名
- `password`：本地UniFi操作系统管理员密码
- `site`：站点名称（通常为`default`）

## 命令

所有命令都支持可选的`json`参数，以获取原始JSON格式的输出（默认格式为人类可读的表格）。

### 网络仪表板

提供所有网络统计信息的综合视图（包括健康状况、设备、客户端、网络、DPI等）：

```bash
bash scripts/dashboard.sh
bash scripts/dashboard.sh json  # Raw JSON for all sections
```

**输出：**包含所有指标的完整ASCII格式仪表板。

### 列出设备

显示所有UniFi设备（接入点、交换机、网关）：

```bash
bash scripts/devices.sh
bash scripts/devices.sh json  # Raw JSON
```

**输出：**设备名称、型号、IP地址、状态、运行时间、连接的客户端信息

### 列出当前连接的客户端

显示当前连接的客户端信息：

```bash
bash scripts/clients.sh
bash scripts/clients.sh json  # Raw JSON
```

**输出：**客户端的主机名、IP地址、MAC地址、连接的接入点以及信号强度、接收/发送数据速率

### 健康状况总结

显示整个站点的健康状况：

```bash
bash scripts/health.sh
bash scripts/health.sh json  # Raw JSON
```

**输出：**各子系统的状态（WAN、LAN、WLAN）以及设备的数量（在线/已连接/已断开）

### 主要应用程序（DPI）

按应用程序显示带宽消耗最多的应用程序：

```bash
bash scripts/top-apps.sh
bash scripts/top-apps.sh 15  # Show top 15 (default: 10)
```

**输出：**应用程序名称、类别以及接收/发送的总流量（以GB为单位）

### 最近的警报

显示最近的警报和事件：

```bash
bash scripts/alerts.sh
bash scripts/alerts.sh 50  # Show last 50 (default: 20)
```

**输出：**警报时间戳、警报类型、警报内容以及受影响的设备

## 工作流程

当用户询问有关UniFi网络的信息时，可以按照以下步骤操作：
1. **“我的网络里有什么设备？”** → 运行 `bash scripts/devices.sh` 和 `bash scripts/clients.sh`
2. **“所有设备都正常吗？”** → 运行 `bash scripts/health.sh`
3. **“有什么问题吗？”** → 运行 `bash scripts/alerts.sh`
4. **“哪些应用程序在占用大量带宽？”** → 运行 `bash scripts/top-apps.sh`
5. **“显示仪表板”** 或进行常规检查 → 运行 `bash scripts/dashboard.sh`

在将结果呈现给用户之前，请务必确认输出内容是否合理（检查是否存在认证失败、数据为空等情况）。

## 注意事项

- 需要具备对UniFi网关的网络访问权限
- 使用UniFi操作系统登录以及 `/proxy/network` API路径
- 所有请求均为**只读的GET请求**
- 已测试的API端点记录在 `references/unifi-readonly-endpoints.md` 文件中

## 参考资料

- [已测试的API端点](references/unifi-readonly-endpoints.md) — 在Cloud Gateway Max上验证过的所有只读API调用的完整列表