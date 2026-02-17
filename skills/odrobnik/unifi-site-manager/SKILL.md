---
name: unifi-site-manager
version: 3.2.1
homepage: https://github.com/odrobnik/unifi-skill
description: 监控并配置 UniFi 网络基础设施。实现本地网关与云连接器的自动路由。管理主机、站点、设备、客户端、无线局域网（WLAN）、无线电设备、固件以及各种网络事件。
metadata:
  openclaw:
    requires:
      env: ["UNIFI_API_KEY"]
      optionalEnv: ["UNIFI_BASE_URL", "UNIFI_GATEWAY_IP", "UNIFI_LOCAL_API_KEY"]
---
# UniFi 网络 API

用于监控和配置 UniFi 网络基础设施。

**入口点：** `{baseDir}/scripts/unifi.py`

## 设置

有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。

配置文件（`config.json`）：
- `api_key` — UniFi Cloud API 密钥（必需）
- `gateway_ip` — 本地网关 IP 地址（用于更快速的本地访问）
- `local_api_key` — 本地网关 API 密钥
- `site_id` — 默认站点 UUID（如果只有一个站点，则会自动检测）

路由是自动的：当本地网关可用时使用本地网关；当本地网关不可用时使用云连接器。使用 `--local` 选项可强制使用本地网关。

## 命令

所有命令都支持 `--json` 选项，以获取原始 JSON 格式的输出。

### 基础设施

```bash
python3 {baseDir}/scripts/unifi.py list-hosts              # Controllers/consoles
python3 {baseDir}/scripts/unifi.py list-sites              # Sites with statistics
python3 {baseDir}/scripts/unifi.py list-devices            # All network devices (summary)
python3 {baseDir}/scripts/unifi.py list-site-devices       # Devices with rich detail (ports, radios, features)
python3 {baseDir}/scripts/unifi.py list-aps                # Access points only
python3 {baseDir}/scripts/unifi.py get-device <device_id>  # Single device details
python3 {baseDir}/scripts/unifi.py firmware-status         # Firmware versions + update availability
```

### 客户端

```bash
python3 {baseDir}/scripts/unifi.py list-clients              # Currently connected clients
python3 {baseDir}/scripts/unifi.py list-clients --detailed    # With traffic/signal stats
python3 {baseDir}/scripts/unifi.py list-known-clients         # All known clients (current + historical)
python3 {baseDir}/scripts/unifi.py list-known-clients --named # Only clients with custom names
python3 {baseDir}/scripts/unifi.py list-ap-clients            # Wireless clients grouped by AP
python3 {baseDir}/scripts/unifi.py list-ap-clients --ap Living  # Filter by AP name
python3 {baseDir}/scripts/unifi.py get-client <client_id>     # Single client details
python3 {baseDir}/scripts/unifi.py label-client <mac> "Name"  # Set custom name for a client
```

### 网络与 WLAN

```bash
python3 {baseDir}/scripts/unifi.py list-networks             # Configured networks (VLANs)
python3 {baseDir}/scripts/unifi.py get-wlan-config            # WLAN/SSID configurations
python3 {baseDir}/scripts/unifi.py get-wlan-config --ssid Hogwarts  # Specific SSID
python3 {baseDir}/scripts/unifi.py set-wlan --ssid Hogwarts \
  --fast-roaming on \
  --bss-transition on \
  --pmf required \
  --band-steering prefer_5g
```

### 网络 DNS

```bash
python3 {baseDir}/scripts/unifi.py get-network-dns              # All networks
python3 {baseDir}/scripts/unifi.py get-network-dns Default       # Specific network
python3 {baseDir}/scripts/unifi.py set-network-dns Default \
  --dns1 1.1.1.1 --dns2 1.0.0.1                                 # Set DNS servers
python3 {baseDir}/scripts/unifi.py set-network-dns Default \
  --dns1 auto                                                    # Disable override (use gateway)
```

### 无线网络配置

```bash
python3 {baseDir}/scripts/unifi.py get-radio-config           # Radio config for all APs
python3 {baseDir}/scripts/unifi.py get-radio-config --ap Living  # Specific AP
python3 {baseDir}/scripts/unifi.py set-radio --ap Living --band 5 \
  --channel 36 --width 80 --power high
```

### 事件

```bash
python3 {baseDir}/scripts/unifi.py list-events                # All site events
python3 {baseDir}/scripts/unifi.py list-events --filter Roam   # Filter by event type
python3 {baseDir}/scripts/unifi.py list-events --mac aa:bb:cc:dd:ee:ff  # Filter by MAC
```

## 注意事项：
- 如果只有一个站点，则会自动检测该站点；否则请使用 `--site <siteId>` 选项指定站点。
- 使用 `--local` 选项可强制使用本地网关；如果无法访问本地网关，则会报错。
- 事件缓冲区有限（根据事件数量不同，最多可保存约 3 周的事件记录）。
- Apple 设备使用随机生成的 MAC 地址；可以使用 `label-client` 选项根据设备的 Wi-Fi 地址来区分不同的设备。