---
name: tailscale
version: 1.0.0
description: 通过 CLI 和 API 管理 Tailscale 的 tailnet 功能。当用户需要执行以下操作时，请使用这些工具：  
- 检查 Tailscale 的状态  
- 列出所有 Tailscale 设备  
- 对设备发送 Ping 请求  
- 通过 Tailscale 传输文件  
- 使用 Tailscale 的 funnel 功能  
- 创建身份验证密钥  
- 查看当前在线的用户  
- 或者进行与 Tailscale 网络管理相关的操作。
---

# Tailscale Skill

这是一个混合型技能，使用命令行界面（CLI）进行本地操作，同时通过API实现整个Tailnet网络的管理。

## 设置

API配置（可选，用于整个Tailnet网络的操作）：`~/.clawdbot/credentials/tailscale/config.json`

```json
{
  "apiKey": "tskey-api-k...",
  "tailnet": "-"
}
```

您可以从Tailscale管理控制台的“设置”→“密钥”→“生成API密钥”处获取API密钥。

“Tailnet”可以是“-”（自动检测）、您的组织名称或电子邮件域名。

---

## 本地操作（CLI）

这些操作仅适用于当前机器。

### 状态与诊断

```bash
# Current status (peers, connection state)
tailscale status
tailscale status --json | jq '.Peer | to_entries[] | {name: .value.HostName, ip: .value.TailscaleIPs[0], online: .value.Online}'

# Network diagnostics (NAT type, DERP, UDP)
tailscale netcheck
tailscale netcheck --format=json

# Get this machine's Tailscale IP
tailscale ip -4

# Identify a Tailscale IP
tailscale whois 100.x.x.x
```

### 连接性

```bash
# Ping a peer (shows direct vs relay)
tailscale ping <hostname-or-ip>

# Connect/disconnect
tailscale up
tailscale down

# Use an exit node
tailscale up --exit-node=<node-name>
tailscale exit-node list
tailscale exit-node suggest
```

### 文件传输（Taildrop）

```bash
# Send files to a device
tailscale file cp myfile.txt <device-name>:

# Receive files (moves from inbox to directory)
tailscale file get ~/Downloads
tailscale file get --wait ~/Downloads  # blocks until file arrives
```

### 暴露服务

```bash
# Share locally within tailnet (private)
tailscale serve 3000
tailscale serve https://localhost:8080

# Share publicly to internet
tailscale funnel 8080

# Check what's being served
tailscale serve status
tailscale funnel status
```

### SSH

```bash
# SSH via Tailscale (uses MagicDNS)
tailscale ssh user@hostname

# Enable SSH server on this machine
tailscale up --ssh
```

---

## 整个Tailnet网络的操作（API）

这些操作用于管理您的整个Tailnet网络。需要API密钥。

### 列出所有设备

```bash
./scripts/ts-api.sh devices

# With details
./scripts/ts-api.sh devices --verbose
```

### 设备详情

```bash
./scripts/ts-api.sh device <device-id-or-name>
```

### 检查在线状态

```bash
# Quick online check for all devices
./scripts/ts-api.sh online
```

### 授权/删除设备

```bash
./scripts/ts-api.sh authorize <device-id>
./scripts/ts-api.sh delete <device-id>
```

### 设备标签与路由

```bash
./scripts/ts-api.sh tags <device-id> tag:server,tag:prod
./scripts/ts-api.sh routes <device-id>
```

### 认证密钥

```bash
# Create a reusable auth key
./scripts/ts-api.sh create-key --reusable --tags tag:server

# Create ephemeral key (device auto-removes when offline)
./scripts/ts-api.sh create-key --ephemeral

# List keys
./scripts/ts-api.sh keys
```

### DNS管理

```bash
./scripts/ts-api.sh dns                 # Show DNS config
./scripts/ts-api.sh dns-nameservers     # List nameservers
./scripts/ts-api.sh magic-dns on|off    # Toggle MagicDNS
```

### 访问控制列表（ACLs）

```bash
./scripts/ts-api.sh acl                 # Get current ACL
./scripts/ts-api.sh acl-validate <file> # Validate ACL file
```

---

## 常见用例

**“现在谁在线？”**
```bash
./scripts/ts-api.sh online
```

**“将这个文件发送到我的手机上”**
```bash
tailscale file cp document.pdf my-phone:
```

**“公开我的开发服务器”**
```bash
tailscale funnel 3000
```

**“为新服务器创建一个密钥”**
```bash
./scripts/ts-api.sh create-key --reusable --tags tag:server --expiry 7d
```

**“连接是直接的还是中继的？”**
```bash
tailscale ping my-server
```