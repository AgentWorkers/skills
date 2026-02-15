---
name: ez-unifi
description: **使用说明：**  
当需要管理 UniFi 网络时，可以使用该工具执行以下操作：  
- 列出/重启/升级设备  
- 阻止/解除对客户端的访问  
- 管理 WiFi 网络  
- 控制 PoE 端口  
- 管理流量规则  
- 创建访客凭证  
- 以及执行任何与 UniFi 控制器相关的任务。  

该工具兼容 UDM Pro/SE、Dream Machine、Cloud Key Gen2+ 以及自托管的 UniFi 控制器。
metadata: {"openclaw":{"emoji":"📶"}}
---

# ez-unifi

这是一个专为网络管理员设计的UniFi网络管理工具，基于`aiounifi`库开发。支持UDM Pro/SE、Dream Machine、Cloud Key Gen2+以及自托管的UniFi控制器。

**执行所有命令时，请使用以下命令格式：**  
`uv run scripts/unifi.py <command> [args]`

## 设置

**步骤1：要求用户创建一个专用的本地管理员账户**

> 为了管理您的UniFi网络，我需要API访问权限。请创建一个专用的本地管理员账户：
>
> 1. 打开您的UniFi控制器（例如：https://192.168.1.1）
> 2. 进入**设置 → 系统 → 管理员与用户**
> 3. 点击**添加管理员**
> 4. 输入用户名（例如：`agent-api`）
> 5. 输入电子邮件和密码
> 6. **重要提示：禁用“远程访问”**——仅限本地访问可以避免多因素认证（MFA）的问题
> 7. 将角色设置为**超级管理员**或**站点管理员**
> 8. 点击**添加**
>
> 然后提供以下信息：
> - 控制器IP地址（例如：`192.168.1.1`
> - 用户名
> - 密码
> - 该控制器是UDM Pro/SE/Dream Machine类型吗？（是/否）

**步骤2：将凭据保存到`.env`文件中**

```bash
UNIFI_HOST=https://192.168.1.1
UNIFI_USERNAME=agent-api
UNIFI_PASSWORD=the_password
UNIFI_SITE=default
UNIFI_IS_UDM=true
```

对于Cloud Key Gen1或自托管的控制器，请将`UNIFI_IS_UDM`设置为`false`。

---

## 系统与站点设置

```bash
unifi.py sites                     # List all sites
unifi.py sysinfo                   # System information
unifi.py health                    # Site health status (WAN, WLAN, LAN)
```

## 设备管理（AP、交换机、网关）

```bash
unifi.py devices                   # List all devices
unifi.py device MAC                # Device details
unifi.py restart MAC               # Restart device
unifi.py restart MAC --hard        # Hard restart (cycles PoE on switches)
unifi.py upgrade MAC               # Upgrade device firmware
unifi.py locate MAC                # Blink LED to locate
unifi.py unlocate MAC              # Stop LED blinking
unifi.py led MAC on|off|default    # Set LED status
unifi.py led MAC on --color=#FF0000 --brightness=50  # With color/brightness
```

## 交换机端口配置

```bash
unifi.py ports                     # List all switch ports
unifi.py port MAC PORT_IDX         # Port details
unifi.py port-enable MAC PORT_IDX  # Enable switch port
unifi.py port-disable MAC PORT_IDX # Disable switch port
unifi.py poe MAC PORT_IDX MODE     # Set PoE mode (auto|off|passthrough|24v)
unifi.py power-cycle MAC PORT_IDX  # Power cycle a PoE port
```

## 智能电源管理（PDU/插座）

```bash
unifi.py outlets                   # List all outlets
unifi.py outlet MAC IDX on|off     # Control outlet relay
unifi.py outlet-cycle MAC IDX on|off  # Enable/disable auto-cycle on internet down
```

## 客户端管理

```bash
unifi.py clients                   # List active clients
unifi.py clients-all               # List all clients (including offline/known)
unifi.py client MAC                # Client details
unifi.py block MAC                 # Block client from network
unifi.py unblock MAC               # Unblock client
unifi.py reconnect MAC             # Kick/reconnect client
unifi.py forget MAC [MAC2...]      # Forget client(s) permanently
```

## WiFi网络配置

```bash
unifi.py wlans                     # List wireless networks
unifi.py wlan ID                   # WLAN details
unifi.py wlan-enable ID            # Enable WLAN
unifi.py wlan-disable ID           # Disable WLAN
unifi.py wlan-password ID NEWPASS  # Change WLAN password
unifi.py wlan-qr ID                # Generate WiFi QR code (PNG file)
unifi.py wlan-qr ID -o myqr.png    # Custom output filename
```

## 端口转发设置

```bash
unifi.py port-forwards             # List port forwarding rules
unifi.py port-forward ID           # Port forward details
```

## 流量规则管理

```bash
unifi.py traffic-rules             # List traffic rules
unifi.py traffic-rule ID           # Traffic rule details
unifi.py traffic-rule-enable ID    # Enable traffic rule
unifi.py traffic-rule-disable ID   # Disable traffic rule
unifi.py traffic-rule-toggle ID on|off  # Toggle traffic rule state
```

## 流量路由配置

```bash
unifi.py traffic-routes            # List traffic routes
unifi.py traffic-route ID          # Traffic route details
unifi.py traffic-route-enable ID   # Enable traffic route
unifi.py traffic-route-disable ID  # Disable traffic route
```

## 防火墙设置

```bash
unifi.py firewall-policies         # List firewall policies
unifi.py firewall-policy ID        # Firewall policy details
unifi.py firewall-zones            # List firewall zones
unifi.py firewall-zone ID          # Firewall zone details
```

## 深度包检测（DPI）功能

```bash
unifi.py dpi-apps                  # List DPI restriction apps
unifi.py dpi-app ID                # DPI app details
unifi.py dpi-app-enable ID         # Enable DPI app restriction
unifi.py dpi-app-disable ID        # Disable DPI app restriction
unifi.py dpi-groups                # List DPI restriction groups
unifi.py dpi-group ID              # DPI group details
```

## 热点优惠券管理

```bash
unifi.py vouchers                  # List vouchers
unifi.py voucher-create --duration=60 --quota=1 --note="Guest"
unifi.py voucher-create --duration=1440 --quota=5 --rate-up=5000 --rate-down=10000
unifi.py voucher-delete ID         # Delete voucher
```

优惠券使用选项：
- `--duration`：优惠券的有效时长（单位：分钟，默认值：60分钟）
- `--quota`：优惠券的使用次数（默认值：1次）
- `--usage-quota`：优惠券的流量配额（单位：MB）
- `--rate-up`：上传速率限制（单位：Kbps）
- `--rate-down`：下载速率限制（单位：Kbps）
- `--note`：优惠券的备注/说明

## 事件日志管理

```bash
unifi.py events                    # Stream events in real-time (Ctrl+C to stop)
```

## 原始API访问权限

```bash
unifi.py raw GET /stat/health      # Raw GET request
unifi.py raw POST /cmd/devmgr '{"cmd":"restart","mac":"aa:bb:cc:dd:ee:ff"}'
unifi.py raw PUT /rest/wlanconf/ID '{"enabled":false}'
```

## 输出格式设置

在需要以JSON格式输出结果的命令前，添加`--json`参数：
```bash
unifi.py devices --json            # JSON output
unifi.py clients --json
```

---

## 使用示例

```bash
# Check network health
uv run scripts/unifi.py health

# List all connected clients
uv run scripts/unifi.py clients

# Block a device
uv run scripts/unifi.py block "aa:bb:cc:dd:ee:ff"

# Restart an access point
uv run scripts/unifi.py restart "11:22:33:44:55:66"

# Disable guest WiFi
uv run scripts/unifi.py wlan-disable "5f8b3d2e1a4c7b9e0d6f8a2c"

# Upgrade device firmware
uv run scripts/unifi.py upgrade "11:22:33:44:55:66"

# Power cycle a PoE port (useful for rebooting PoE devices)
uv run scripts/unifi.py power-cycle "switch_mac" 5

# Create a guest voucher (24 hours, single use)
uv run scripts/unifi.py voucher-create --duration=1440 --quota=1 --note="Guest access"

# Generate WiFi QR code for easy connection
uv run scripts/unifi.py wlan-qr "wlan_id" -o guest_wifi.png

# Control traffic rule
uv run scripts/unifi.py traffic-rule-disable "rule_id"
```

## 查找设备ID

- **WLAN设备ID**：运行`wlans`命令，查看`ID`列
- **设备MAC地址**：运行`devices`命令，查看`MAC`列
- **客户端MAC地址**：运行`clients`或`clients-all`命令，查看`MAC`列
- **流量规则ID**：运行`traffic-rules`命令，查看`ID`列
- **优惠券ID**：运行`vouchers`命令，查看`ID`列

## 注意事项

- MAC地址可以采用任何格式（包含冒号、破折号或无格式）
- 所有输出结果均为JSON格式，便于解析
- 使用专用本地管理员账户可以避免与云连接账户相关的多因素认证问题
- 如果遇到速率限制（出现429错误），请等待几分钟后再尝试操作