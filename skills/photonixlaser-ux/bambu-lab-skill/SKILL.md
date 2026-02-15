---
name: bambu-lab
description: 通过 MQTT 控制 Bambu Lab 3D 打印机（型号：A1，连接方式：P1P，X1）。使用此功能可以监控打印进度、查询设备状态、控制打印机的暂停/停止操作，以及在打印完成或出现错误时接收通知。需要启用 LAN 模式并输入访问代码才能使用该功能。
---

# Bambu Lab 3D打印机技能

通过MQTT在本地网络中控制和管理Bambu Lab 3D打印机。

## 配置

默认配置（可在`scripts/bambu.sh`中修改）：
- **主机：**`192.168.30.103`（A1打印机）
- **端口：**`8883`（MQTT over TLS）
- **用户名：**`03919A3A2200009`（序列号）
- **密码：**`33576961`（访问代码）
- **型号：**A1

## 使用方法

使用`scripts/bambu.sh`脚本执行所有操作：

```bash
./skills/bambu-lab/scripts/bambu.sh <befehl>
```

### 命令

**状态与监控：**
- `status` - 当前打印状态
- `progress` - 打印进度（百分比）
- `temps` - 温度（喷嘴、打印床、打印舱）
- `watch` - 实时监控（持续运行）

**控制命令：**
- `pause` - 暂停打印
- `resume` - 继续打印
- `stop` - 中止打印
- `light on|off` - 打印机灯开关
- `fans <0-255>` - 风扇转速（0-255之间）

**通知：**
- `notify` - 通过Telegram发送通知以启动监控

**MQTT调试：**
- `raw` - 显示原始MQTT消息

## 示例

```bash
# Status abfragen
./skills/bambu-lab/scripts/bambu.sh status

# Druckfortschritt
./skills/bambu-lab/scripts/bambu.sh progress

# Live-Überwachung
./skills/bambu-lab/scripts/bambu.sh watch

# Druck pausieren
./skills/bambu-lab/scripts/bambu.sh pause

# Mit Benachrichtigung
./skills/bambu-lab/scripts/bambu.sh notify
```

## 自动通知

在打印完成时发送自动通知：

```bash
# Im Hintergrund starten
./skills/bambu-lab/scripts/bambu.sh notify &
```

或者通过Cron/Heartbeat任务定期执行。

## API参考

有关MQTT的完整文档，请参阅[references/mqtt.md]。

## 支持的型号

- ✅ A1（已测试）
- ✅ A1 Mini
- ✅ P1P / P1S
- ✅ X1 / X1C

所有型号在局域网模式下均使用相同的MQTT协议。