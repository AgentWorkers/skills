---
name: meshtastic
description: 通过 Mesh Master API 实现对 Meshtastic LoRa 网络的全面控制：可以向节点/组发送消息、管理频道、配置无线电设置、查看网络拓扑结构、请求遥测数据，并控制网络的所有方面。该功能可与运行在本地网络或 Tailscale VPN 上的 Mesh Master 无缝集成。适用于用户需要执行“发送消息”、“检查节点状态”、“配置频道”或查询网络状态等操作的场景。
---

# Meshtastic 技能

通过集成 Mesh Master API，实现对整个 Meshtastic LoRa 网络的全面控制。

## 概述

该技能通过与运行在 Raspberry Pi 或其他设备上的 Mesh Master 通信，提供对 Mesh Network 的全面控制。Mesh Master 负责处理与 Meshtastic 设备的实际连接；而该技能则提供了友好的自然语言界面。

## 架构

```
Clawdbot (this skill)
    ↓ HTTP API calls
Mesh Master (RPi, Flask app)
    ↓ Python meshtastic library
Meshtastic Device (LoRa radio)
```

## 连接方式

### 1. 本地网络（推荐）
```bash
MESH_MASTER_URL=http://192.168.1.100:5000
```
- 通信速度快，直接连接
- 无需 VPN 增加延迟
- 需要连接在同一 WiFi 网络中

### 2. Tailscale VPN（远程）
```bash
MESH_MASTER_URL=http://100.64.x.x:5000
```
- 安全可靠，支持远程访问
- 使用 Tailscale 的私有网络
- 延迟略有增加

### 3. USB 串行（直接连接）
```bash
MESHTASTIC_PORT=/dev/ttyUSB0
```
- 直接连接到 Meshtastic 设备
- 在本地运行 Meshtastic CLI
- 无需 Mesh Master

## 命令与功能

### 消息传递

**向节点发送消息**
```
"send a message to bob: hello there"
"msg @snmo thanks for the update"
"/snmo how's the weather?"
```
通过 Mesh Master 中继系统发送消息，并支持确认响应（ACK）的跟踪。

**向频道/组发送消息**
```
"broadcast: emergency shelter needed"
"send to camping group: dinner at 7pm"
"ch 1 everyone gather at base"
```
向整个频道发送消息，同时尊重网络中的静默时间设置。

### 网络状态

**查看所有节点**
```
"show me all nodes"
"who's on the mesh?"
"list network nodes"
```
返回包含信号强度、电池电量和位置的格式化表格。

**节点详情**
```
"show info for node WH3R"
"what's the signal to brian?"
"node details for !ba4bf9d0"
```
返回节点的信号强度、电池电量、遥测数据、位置信息以及最后一次被检测到的时间。

**网络指标**
```
"mesh health"
"network status"
"how many nodes online?"
```
返回数据传输的跳数、频谱利用率和消息吞吐量。

### 频道管理

**列出频道**
```
"show channels"
"what channels are active?"
"list all channels"
```

**切换频道**
```
"use channel camping"
"switch to ch 2"
"primary channel"
```

**创建频道**
```
"add channel hiking"
"new channel for rescue-ops"
"create channel with name scout-ops"
```

**配置频道**
```
"set channel 1 name to hiking"
"configure camping channel encryption random"
"change modem preset to long-slow"
```

**删除频道**
```
"remove channel 2"
"delete camping channel"
```

### 无线电设置

**查看设置**
```
"show radio config"
"what's the lora settings?"
"get device settings"
```

**更改设置**
```
"set lora region to US"
"change device role to repeater"
"set power mode to always on"
"configure wifi ssid mywifi password mypass"
```

**导出/导入配置**
```
"export configuration"
"save config to file"
"load configuration from backup.yaml"
```

### 遥测与请求

**请求遥测数据**
```
"get telemetry from bob"
"request position from WH3R"
"battery status for all nodes"
```

**追踪路径**
```
"traceroute to !ba4bf9d0"
"how do i reach node camping?"
```

### 位置与定位

**设置位置**
```
"set my location to 40.7128 -74.0060"
"location 39.7392 -104.9903 1234m"
"my coordinates 25.2 -16.8"
```

**查看位置**
```
"show all locations"
"where's bob?"
"node positions map"
```

### 业余无线电模式

**启用业余无线电模式**
```
"enable ham mode with callsign KI1345"
"set ham radio KI1345"
```
为持有许可证的操作员启用未加密的通信模式。

**禁用业余无线电模式**
```
"disable ham mode"
"back to normal encryption"
```

### 设备管理

**重命名设备**
```
"rename myself to Snail"
"set owner John Smith"
"short name JS"
```

**获取设备信息**
```
"show device info"
"radio status"
"firmware version"
```

**重启设备**
```
"reboot radio"
"restart meshtastic"
```

### 高级功能

**二维码**
```
"show channel qr"
"generate qr for all channels"
"qr code"
```

**预设消息**
```
"set canned messages: hello | busy | brb"
"get canned messages"
```

**铃声**
```
"set ringtone <rtttl-string>"
"get ringtone"
```

**配置 MQTT**
```
"enable mqtt server.com:1883"
"set mqtt username user password pass"
```

## 配置

### 环境变量

```bash
# Mesh Master location
export MESH_MASTER_URL="http://192.168.1.100:5000"
# or
export MESH_MASTER_URL="http://100.64.x.x:5000"  # Tailscale

# Direct Meshtastic connection (optional)
export MESHTASTIC_PORT="/dev/ttyUSB0"

# Timeouts
export MESH_TIMEOUT=10  # seconds

# Debug logging
export MESH_DEBUG=true
```

### 本地开发

在没有 Mesh Master 的情况下进行测试：
```bash
# Mock mode (simulates responses)
export MESH_MOCK=true
```

## 性能

- **发送消息**：0.5-2 秒（取决于网络状况）
- **获取节点列表**：1-3 秒
- **配置设置**：1-5 秒（需要重启设备）
- **请求遥测数据**：2-10 秒（距离越远，耗时越长）

## 错误处理

该技能能够处理以下错误情况：
- Mesh Master 连接失败 → 显示错误信息并提供重试选项
- 节点 ID 无效 → 检查是否存在部分匹配的节点或建议使用有效的节点 ID
- 网络超时 → 显示“网络响应缓慢”的提示信息
- 输入格式错误 → 提供示例帮助用户纠正输入

## 参考资料

- **cli-commands.md** - 完整的 Meshtastic CLI 命令参考
- **mesh-master-api.md** - Mesh Master API 的端点及使用示例
- **networking.md** - Tailscale 的网络配置与故障排除指南
- **examples.md** - 实际应用场景示例

## 故障排除

**“无法连接到 Mesh Master”**
- 确认 `MESH_MASTER_URL` 的地址是否正确
- 验证 Mesh Master 是否正在 Raspberry Pi 上运行
- 检查网络连接、WiFi 连接以及 Tailscale 的配置
- 确保防火墙允许端口 5000 的访问

**“找不到节点”**
- 使用 `/nodes` 命令确认节点是否已加入网络
- 尝试使用节点的简称而非 ID 进行通信
- 可能需要等待节点完成网络加入过程

**“消息发送失败”**
- 确认目标节点是否可到达
- 检查频道加密设置是否正确
- 尝试使用广播模式发送消息（可覆盖更多节点）
- 检查网络中的静默时间设置

**“设置更改未生效”**
- 可能需要重启设备
- 某些设置可能需要重新配置频道
- 检查设备固件的兼容性

## GitHub 与部署

该技能已发布在 GitHub 上，并经过了全面的安全审查：
- ✅ 使用 `.gitignore` 文件防止敏感信息泄露
- ✅ 不包含硬编码的 API 密钥
- ✅ 所有敏感数据均来自环境变量
- ✅ 提供了配置模板

要将其集成到 Mesh Master 中，请按照以下步骤操作：
1. 将该技能克隆到 `~/Mesh-Master/mesh_master/skills/meshtastic/` 目录下
2. 将其添加到 Mesh Master 的命令注册表中
3. 重启 Mesh Master
4. 该技能的命令将通过仪表盘和 Telegram 聊天机器人提供

## 安全性

- API 调用仅使用基于环境的凭据
- 日志中不记录实际的消息内容
- 保护用户隐私并确保数据加密
- 与 Mesh Master 的安全机制兼容