---
description: 通过信号分析、频道扫描、速度测试和DNS检查来诊断Wi-Fi问题。
---

# Wi-Fi 诊断

通过信号分析、频道扫描和速度测试来诊断 Wi-Fi 连接问题。

## 所需系统

- 安装了 `nmcli`, `iwconfig` 或 `iw` 的 Linux 系统
- 用于速度测试的 `curl` 工具
- 可选：用于 DNS 诊断的 `dig` 工具
- 某些命令在无线扫描时需要 `sudo` 权限

## 操作步骤

### 连接信息
```bash
# Current network details
nmcli -t -f active,ssid,signal,chan,freq,bssid dev wifi | grep '^yes'

# Interface details
iwconfig 2>/dev/null | grep -E 'ESSID|Quality|Bit Rate'

# IP and gateway
ip route | grep default
ip addr show | grep 'inet '
```

### 频道扫描
```bash
# Nearby networks (may need sudo)
nmcli dev wifi list

# Channel utilization summary
nmcli -t -f chan,signal dev wifi list | sort -t: -k1 -n | \
  awk -F: '{ch[$1]++; sig[$1]+=$2} END{for(c in ch) printf "Ch %s: %d networks, avg signal %d%%\n", c, ch[c], sig[c]/ch[c]}'
```

### 速度测试（无需额外依赖）
```bash
# Download test (~10MB)
curl -o /dev/null -s -w "Download: %{speed_download} bytes/sec (%{time_total}s)\n" https://speed.cloudflare.com/__down?bytes=10000000

# Upload test (~10MB)
dd if=/dev/zero bs=1M count=10 2>/dev/null | curl -X POST -d @- -s -w "Upload: %{speed_upload} bytes/sec\n" https://speed.cloudflare.com/__up
```

### DNS 诊断
```bash
dig google.com | grep "Query time"
ping -c 5 8.8.8.8 | tail -1
ping -c 5 1.1.1.1 | tail -1
```

### 输出格式
```
## 📶 Wi-Fi Diagnostics — <timestamp>

**Network**: MyWiFi | **Channel**: 6 (2.4GHz) | **Signal**: 72%

| Test | Result | Status |
|------|--------|--------|
| Signal | -45 dBm (72%) | 🟢 Good |
| Download | 48.2 Mbps | 🟢 Good |
| Upload | 12.1 Mbps | 🟡 Fair |
| DNS Latency | 15ms | 🟢 Good |
| Ping (8.8.8.8) | 22ms avg | 🟢 Good |

**Channel Congestion**: Ch 6 has 8 networks. Consider switching to Ch 1 or 11.

**Thresholds**: Signal: 🟢>60% 🟡30-60% 🔴<30% | Speed: 🟢>25Mbps 🟡>5Mbps 🔴<5Mbps
```

## 特殊情况

- **没有 Wi-Fi 适配器**：使用 `iw dev` 命令进行检测。如果未找到无线接口，请报告该情况。
- **仅使用以太网**：请注意，这些诊断工具仅适用于 Wi-Fi，以太网需要使用其他工具进行诊断。
- **5GHz 与 2.4GHz**：报告当前使用的频段。不同频段的频道推荐方案也有所不同。
- **启用 VPN**：VPN 可能会影响速度测试结果。如果检测到 VPN 接口，请予以说明。
- **`nmcli` 无法使用**：此时请切换到使用 `iwconfig` 和 `iw` 命令进行操作。

## 安全注意事项

- 速度测试会将数据发送到外部服务器（例如 Cloudflare）——这对于诊断目的来说是安全的。
- Wi-Fi 扫描会显示附近网络的信息——请勿在公共场合分享这些信息。
- 绝不要在诊断输出中显示 Wi-Fi 密码。