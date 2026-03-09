---
name: hilink-lte
description: 通过 REST API 控制华为 HiLink USB LTE 移动模块（如 E3372、E8372 等）。支持发送/接收短信、查看信号强度、管理 SIM 卡 PIN 码、查询预付费余额以及监控连接状态。该功能适用于发送或读取短信、检查 LTE 信号/状态、输入 SIM 卡 PIN 码、查询移动电话余额（USSD 消息）或管理 HiLink USB 移动模块的场景。
---
# HiLink LTE调制解调器

通过其本地REST API来控制华为HiLink USB LTE调制解调器。

## 设置

调制解调器必须处于**HiLink模式**（而非stick/serial模式），并且可以通过HTTP访问。

### 配置

在`~/.config/hilink/config`文件中设置网关IP地址：
```bash
HILINK_GATEWAY=192.168.200.1
```

或者通过环境变量设置：`export HILINK_GATEWAY=192.168.200.1`

默认值：`192.168.200.1`

### 网络要求

LTE USB接口需要一个属于调制解调器子网的IP地址（例如：192.168.200.x）。请将其配置为**静态IP地址**，且不设置网关和DNS，以避免路由冲突：
```
# /etc/network/interfaces.d/lte
allow-hotplug lte0
iface lte0 inet static
    address 192.168.200.100/24
```

**重要提示：**切勿允许LTE接口设置默认路由或DNS地址——这会覆盖您的局域网连接。您可以在`dhcpcd`命令中使用`nogateway`和`nohook resolv.conf`选项，或者使用不包含网关设置的静态IP配置。

### 确保接口名称的稳定性

每次系统启动时，USB网络接口的名称可能会随机变化。请创建一个udev规则以固定接口名称：
```bash
# Find MAC address
cat /sys/class/net/enx*/address

# Create udev rule
echo 'SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="xx:xx:xx:xx:xx:xx", NAME="lte0"' \
  | sudo tee /etc/udev/rules.d/70-lte-modem.rules
```

## 命令行接口（CLI）使用方法

```bash
# SMS
scripts/hilink.sh sms send "+41791234567" "Hello!"
scripts/hilink.sh sms list
scripts/hilink.sh sms read 40001
scripts/hilink.sh sms delete 40001

# Status & Signal
scripts/hilink.sh status
scripts/hilink.sh signal

# SIM PIN
scripts/hilink.sh pin enter 1234
scripts/hilink.sh pin disable 1234
scripts/hilink.sh pin status

# Prepaid Balance (USSD)
scripts/hilink.sh balance

# Connection info
scripts/hilink.sh info
```

## API概述

所有HiLink API调用都需要一个会话令牌（session token）和一个CSRF令牌（CSRF token）的组合：
```bash
# Get tokens
curl -s http://GATEWAY/api/webserver/SesTokInfo
# Returns: <SesInfo>cookie</SesInfo><TokInfo>csrf_token</TokInfo>

# Use in requests
curl -X POST http://GATEWAY/api/endpoint \
  -H "Cookie: <SesInfo value>" \
  -H "__RequestVerificationToken: <TokInfo value>" \
  -H "Content-Type: application/xml" \
  -d '<xml request body>'
```

有关详细的API端点信息，请参阅[references/api.md](references/api.md)。

## 故障排除

- **发送短信时出现错误113018**：SIM卡未注册到网络。请检查SIM卡的PIN码状态和信号强度。
- **SimState 260**：需要输入PIN码。请先通过`scripts/hilink.sh pin enter <PIN>`命令输入PIN码。
- **SignalStrength 0**：表示未进行网络注册。请等待一段时间后再尝试，或者检查天线连接。
- **DNS/路由问题**：可能是LTE接口设置了默认路由。请使用`sudo ip route del default via 192.168.200.1`命令删除默认路由。
- **接口名称更改**：可能是USB接口的MAC地址发生了变化。请创建相应的udev规则以固定接口名称（参见“设置”部分）。