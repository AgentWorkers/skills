---
name: network-scanner
description: 扫描网络以发现设备，收集设备的MAC地址、厂商信息以及主机名。系统包含安全机制，以防止意外扫描公共网络。
homepage: https://clawhub.com/skills/network-scanner
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["nmap", "dig"]
    tags:
      - network
      - discovery
      - devices
      - nmap
      - security
---

# 网络扫描器

使用 `nmap` 发现并识别本地或远程网络中的设备。可以获取 IP 地址、主机名（通过反向 DNS 查询）、MAC 地址以及设备厂商信息。

**安全第一：** 该工具内置了防护机制，可防止用户意外扫描公共 IP 范围或未配置私有路由的网络，从而避免收到来自网络服务提供商的滥用报告。

## 所需软件

- `nmap`：网络扫描工具（可通过 `apt install nmap` 或 `brew install nmap` 安装）
- `dig`：DNS 查询工具（通常已预装）
- 建议使用 `sudo` 权限来获取 MAC 地址

## 快速入门

```bash
# Auto-detect and scan current network
python3 scripts/scan.py

# Scan a specific CIDR
python3 scripts/scan.py 192.168.1.0/24

# Scan with custom DNS server for reverse lookups
python3 scripts/scan.py 192.168.1.0/24 --dns 192.168.1.1

# Output as JSON
python3 scripts/scan.py --json
```

## 配置

在 `~/.config/network-scanner/networks.json` 文件中配置网络信息：

```json
{
  "networks": {
    "home": {
      "cidr": "192.168.1.0/24",
      "dns": "192.168.1.1",
      "description": "Home Network"
    },
    "office": {
      "cidr": "10.0.0.0/24",
      "dns": "10.0.0.1",
      "description": "Office Network"
    }
  },
  "blocklist": [
    {
      "cidr": "10.99.0.0/24",
      "reason": "No private route from this host"
    }
  ]
}
```

然后通过设备名称进行扫描：

```bash
python3 scripts/scan.py home
python3 scripts/scan.py office --json
```

## 安全特性

该扫描器包含多种安全机制，以防止误用：

1. **阻止列表**：`blocklist` 配置数组中的网络将被始终阻止。
2. **公共 IP 检查**：禁止扫描非 RFC1918 标准的公共 IP 范围。
3. **路由验证**：对于临时创建的 CIDR 地址，会验证其是否使用了私有网关。

**受信任的网络**（在 `networks.json` 中配置）会自动跳过路由验证，因为您已明确允许这些网络的使用。

```bash
# Blocked - public IP range
$ python3 scripts/scan.py 8.8.8.0/24
❌ BLOCKED: Target 8.8.8.0/24 is a PUBLIC IP range

# Blocked - in blocklist  
$ python3 scripts/scan.py 10.99.0.0/24
❌ BLOCKED: 10.99.0.0/24 is blocklisted

# Allowed - configured trusted network
$ python3 scripts/scan.py home
✓ Scanning 192.168.1.0/24...
```

## 命令

```bash
# Create example config
python3 scripts/scan.py --init-config

# List configured networks
python3 scripts/scan.py --list

# Scan without sudo (may miss MAC addresses)
python3 scripts/scan.py home --no-sudo
```

## 输出格式

- **Markdown（默认格式）：**
```
### Home Network
*Last scan: 2026-01-28 00:10*

| IP | Name | MAC | Vendor |
|----|------|-----|--------|
| 192.168.1.1 | router.local | AA:BB:CC:DD:EE:FF | Ubiquiti |
| 192.168.1.100 | nas.local | 11:22:33:44:55:66 | Synology |

*2 devices found*
```

- **JSON（格式：--json）：**
```json
{
  "network": "Home Network",
  "cidr": "192.168.1.0/24",
  "devices": [
    {
      "ip": "192.168.1.1",
      "hostname": "router.local",
      "mac": "AA:BB:CC:DD:EE:FF",
      "vendor": "Ubiquiti"
    }
  ],
  "scanned_at": "2026-01-28T00:10:00",
  "device_count": 2
}
```

## 使用场景

- **设备清单**：记录网络中的所有设备。
- **安全审计**：识别未知设备。
- **文档生成**：生成网络拓扑图以供文档使用。
- **自动化**：与家庭自动化系统集成，检测设备是否存在。

## 提示

- 使用 `sudo` 权限以获取准确的 MAC 地址（`nmap` 需要权限来执行 ARP 请求）。
- 配置本地 DNS 服务器以优化主机名解析。
- 将已配置的网络添加到列表中，以便在每次扫描时跳过路由验证。
- 将无法通过私有网络访问的网络添加到阻止列表中，以防误操作。
- 扩展脚本中的 `MAC_VENDORS` 列表，以更准确地识别设备厂商。