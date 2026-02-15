---
name: meshtastic
description: 通过 Meshtastic LoRa 网络发送和接收消息。适用于离网通信、监控网状网络状态、读取最近的网状网络消息，或通过 LoRa 无线电发送文本信息。
---

# Meshtastic 技能

通过 USB 控制 Meshtastic 节点，实现离网 LoRa 网络通信。

## 先决条件

- 兼容 Meshtastic 的硬件（RAK4631、T-Beam、Heltec、LilyGo 等）
- 与主机计算机之间的 USB 连接
- 安装了 Python 3.9 及 `meshtastic` 和 `paho-mqtt` 包
- 请参阅 `references/SETUP.md` 以获取完整的安装指南

## 配置

使用 `CONFIG.md` 文件编辑节点详细信息、MQTT 设置以及警报接收地址。

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    MQTT Bridge                               │
├─────────────────────────────────────────────────────────────┤
│  RECEIVE: mqtt.meshtastic.org (global JSON traffic)         │
│  PUBLISH: optional map broker (protobuf)                    │
│  SOCKET:  localhost:7331 (commands: send, status, toggle)   │
├─────────────────────────────────────────────────────────────┤
│  Files:                                                      │
│  • /tmp/mesh_messages.txt - received messages log           │
│  • /tmp/mesh_nodes.json   - cached node positions           │
└─────────────────────────────────────────────────────────────┘

┌─────────────┐     USB      ┌─────────────┐
│  LoRa Node  │◄────────────►│ Bridge.py   │
│  (Radio)    │              │  - Serial   │
└─────────────┘              │  - Socket   │
                             │  - MQTT     │
                             └──────┬──────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
    localhost:7331           /tmp/mesh_*            MQTT Broker
    (send commands)          (message logs)         (mesh traffic)
```

## 快速参考

### 发送消息

```bash
# Via socket (preferred - works while bridge running)
echo '{"cmd":"send","text":"Hello mesh!"}' | nc -w 2 127.0.0.1 7331

# Direct message to specific node
echo '{"cmd":"send","text":"Hey!","to":"!abcd1234"}' | nc -w 2 127.0.0.1 7331

# Check status
echo '{"cmd":"status"}' | nc -w 2 127.0.0.1 7331

# List RF nodes (seen via radio)
echo '{"cmd":"nodes"}' | nc -w 2 127.0.0.1 7331
```

### 显示节点位置（如已配置）

```bash
# Toggle map publishing on/off
echo '{"cmd":"map"}' | nc -w 2 127.0.0.1 7331

# Explicitly enable/disable
echo '{"cmd":"map","enable":true}' | nc -w 2 127.0.0.1 7331
echo '{"cmd":"map","enable":false}' | nc -w 2 127.0.0.1 7331

# Force immediate position report
echo '{"cmd":"map_now"}' | nc -w 2 127.0.0.1 7331
```

### 读取消息

```bash
# Recent messages (last 20)
tail -20 /tmp/mesh_messages.txt

# Filter common noise
tail -50 /tmp/mesh_messages.txt | grep -v -E "(Hello!|hey|mqtt-test)"
```

### 消息日志格式

```
TIMESTAMP|CHANNEL|SENDER|DISTANCE|TEXT
2026-02-02T12:43:59|LongFast|!433bf114|1572km|Moin moin!
```

## 桥接服务

```bash
# Status
sudo systemctl status meshtastic-bridge

# Restart
sudo systemctl restart meshtastic-bridge

# View logs
sudo journalctl -u meshtastic-bridge -f

# Stop (needed for direct CLI access)
sudo systemctl stop meshtastic-bridge
```

## 监控与警报

### 选项 1：Cron 作业（推荐）

```javascript
cron.add({
  name: "mesh-monitor",
  schedule: { kind: "every", everyMs: 300000 },  // 5 min
  sessionTarget: "isolated",
  payload: {
    kind: "agentTurn",
    message: "Check /tmp/mesh_messages.txt for new messages. Filter out noise (test messages, 'Hello!', 'hey'). Alert me of interesting ones with translations if non-English.",
    timeoutSeconds: 60,
    deliver: true,
    channel: "telegram"  // or your channel
  }
})
```

### 选项 2：摘要信息

```javascript
cron.add({
  name: "mesh-digest",
  schedule: { kind: "cron", expr: "0 8,14,20 * * *", tz: "Europe/Madrid" },
  sessionTarget: "isolated",
  payload: {
    kind: "agentTurn",
    message: "Read /tmp/mesh_messages.txt. Create a digest of interesting messages from the last 6 hours. Translate non-English, guess country from distance. Post summary.",
    timeoutSeconds: 120,
    deliver: true,
    channel: "telegram"
  }
})
```

### 选项 3：生成监控代理

```javascript
sessions_spawn({
  task: "Monitor /tmp/mesh_messages.txt every 30 seconds. Alert me for interesting messages (not noise). Run for 1 hour.",
  label: "mesh-monitor",
  runTimeoutSeconds: 3600
})
```

## 距离参考

以下为根据地理位置估算的大致距离（请根据实际情况调整）：

| 距离 | 典型区域 |
|----------|-----------------|
| <500km | 邻近国家/地区 |
| 500-1000km | 中距离 |
| 1000-1500km | 远距离 |
| 1500-2000km | 超远距离（可能需要通过 MQTT 中继） |
| >2000km | 通过 MQTT 转发的数据 |

## 隐私说明

- 地图显示可能使用模糊定位（精度约为 2 公里）
- 可以完全关闭位置信息的发布功能
- 本地射频消息会被记录，但默认不会对外共享
- 请勿在消息中广播精确位置信息

## 支持的硬件

| 设备 | 说明 |
|--------|-------|
| RAK4631 | 推荐使用，具有可靠的 USB 接口 |
| T-Beam | 广泛使用的设备，支持 GPS |
| Heltec V3 | 经济型选择 |
| LilyGo T-Echo | 配备电子纸显示屏 |

请参阅 `references/SETUP.md` 以获取针对特定硬件的详细安装说明。

## 区域频率

| 地区 | 频率 | 主题根路径 |
|--------|-----------|------------|
| 欧洲 | 868 MHz | `msh/EU_868/2/json` |
| 美洲 | 915 MHz | `msh/US/2/json` |
| 澳大利亚/新西兰 | 915 MHz | `msh/ANZ/2/json` |

## 相关文件

```
~/.openclaw/skills/meshtastic/
├── SKILL.md           # This file
├── CONFIG.md          # Your configuration
├── scripts/
│   └── mesh.py        # CLI wrapper
└── references/
    └── SETUP.md       # Installation guide
```

## 故障排除

**“资源暂时不可用”**
- 串行端口一次只能被一个进程使用
- 在直接使用 CLI 命令前，请先停止桥接服务：`sudo systemctl stop meshtastic-bridge`

**没有消息显示**
- 确保订阅的 MQTT 主题与您的地区匹配
- 检查防火墙是否允许端口 1883 的出站通信
- 查看 `journalctl -u meshtastic-bridge` 以获取错误日志

**无法发送消息**
- 确保桥接服务正在运行（即 socket 服务器正在工作）
- 检查配置文件中的串行端口设置
- 可以尝试：`echo '{"cmd":"status"}' | nc -w 2 127.0.0.1 7331`

**考虑使用 BLE 替代 USB 吗？**
- 不建议这样做。在 Linux 系统上，USB 的可靠性更高。
- Linux 上的 BLE（BlueZ/bleak）存在通知功能不稳定、配对问题以及随机断开连接的情况。
- 详情请参阅 `references/SETUP.md`。

## 更多资源

- [Meshtastic 官方文档](https://meshtastic.org/docs/)
- [MQTT 集成指南](https://meshtastic.org/docs/configuration/module/mqtt/)
- [硬件选项](https://meshtastic.org/docs/hardware/)