---
name: ntopng-admin
description: 使用 ntopng 和 Redis 数据进行专业的网络监控和设备识别。适用于安全审计和诊断环境。
metadata:
  openclaw:
    disableModelInvocation: true
    requires:
      bins: ["ssh", "jq"]
      env: ["OPNSENSE_HOST", "OPNSENSE_SSH_PORT", "NTOP_INSECURE"]
---

# ntopng 网络监控工具（安全版）

这是一个强大的网络审计工具，它通过安全的 SSH 隧道直接从 Redis 查询 ntopng 数据。该工具专为需要详细了解本地网络流量的网络管理员和安全专业人士设计。

## ⚠️ 高权限警告与责任使用

**请谨慎操作：** 该工具会执行高权限操作，包括通过 SSH 在您的网络网关上执行命令以及读取内部网络状态。

1. **仅限严格审计用途：** 适用于实验室、测试或受控的审计环境。除非代理的访问受到严格隔离，否则请避免在关键的生产系统中使用。
2. **明确授权：** 默认情况下，自动调用功能是禁用的。您必须手动批准每个查询，以确保对访问的数据进行全面监控。
3. **安全设置：** 该工具使用 SSH 密钥认证。切勿使用明文密码。在适用的情况下，确保您的 SSH 密钥使用密码短语进行保护。
4. **数据敏感性：** 请注意，该工具会暴露 MAC 地址、内部 IP 地址和连接元数据。请像处理网络配置文件一样谨慎处理输出数据。

## 先决条件

*   **SSH 密钥访问：** OpenClaw 主机与 OPNsense/ntopng 主机之间必须配置了公钥认证。
*   **必备工具：** 当前环境中必须具备 `ssh` 和 `jq` 工具。
*   **后端服务：** 目标主机上的 ntopng 必须已启用 Redis 持久化功能。

## 配置

在您的环境或代理配置中声明以下变量：

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `OPNSENSE_HOST` | 目标网关的 IP 地址或主机名 | `192.168.1.1` |
| `OPNSENSE_SSH_PORT` | SSH 服务端口 | `50222` |
| `NTOP_INSECURE` | 如果使用自签名证书，请设置为 `true` | `false` |

## 可用的命令

辅助脚本 `scripts/ntopng-helper.sh` 提供安全的、仅读的数据提取功能：

### 1. 网络设备清单
```bash
./scripts/ntopng-helper.sh list [limit]
```
列出检测到的设备，包括 MAC 地址、IP 地址、总流量以及最后一次出现的时间戳。

### 2. 设备分析
```bash
./scripts/ntopng-helper.sh device-info <ip|mac>
```
提供详细的流量统计信息、数据包数量以及设备分类。

### 3. 连接审计
```bash
./scripts/ntopng-helper.sh connections <ip> [sample_size]
```
从 ntopng 日志中提取特定设备访问的外部域名样本。

### 4. 设备状态与统计信息
```bash
./scripts/ntopng-helper.sh status   # Verifies the ntopng service state
./scripts/ntopng-helper.sh stats    # Global network device counts
```

## 数据解读指南

*   **数据泄露模式：** 如果非服务器设备的上传与下载比率超过 5:1，则属于高优先级的异常情况。
*   **设备欺骗：** 应检查异常的 MAC 地址或以 `DE:AD:BE:EF` 为前缀的 MAC 地址（通常为 VPN/Tunnel 接口）。
* **协议异常：** 使用 `app` 命令检测使用违反本地安全策略的协议的设备（例如，意外的 SSH 或 HTTP 服务器）。

## 安全实施措施

- **防止敏感信息泄露：** 脚本经过加固，不会泄露任何凭据或敏感的环境变量。
- **输入验证：** 对输入参数进行过滤，以防止 shell 注入攻击。
- **默认采用安全模式：** 除非明确设置为实验室用途，否则会启用 SSL 验证。