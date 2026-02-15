---
name: home-assistant
description: 通过 ClawBridge API 控制 Home Assistant 设备。当 James 请求开关灯、检查设备状态或与任何已暴露的 Home Assistant 实体交互时，可以使用该功能。该功能支持实体发现、状态检查以及需要人工审批的服务调用。
---

# Home Assistant 技能

通过 ClawBridge（基于空气隔离的 API）控制 Home Assistant 设备。

## 配置

- **基础 URL：** `http://192.168.0.238:8100`
- **API 密钥：** `cb_Z2_Kcoc5Efrztj58lk7SlpZISkwbYlkAkxYjLc_U6lY`
- **Discord Webhook：** `https://discord.com/api/webhooks/1471253559323656194/bGAVuOBcC66p7pyuUFN465lXOHdeScffN1ZyclDj1jb8kmgvocgBwd6J-F5W6qmNQymf`

## 实时通知（主要方式）

**Python → Discord 直接发送** — 无需任何 AI 成本，即时通知。

### 开始监控
```bash
python3 /root/.openclaw/workspace/skills/home-assistant/scripts/ha-discord.py &
```

### 停止监控
```bash
process kill sessionId={session_id}
```

### 过滤设备

编辑 `scripts/ha-discord.py` 文件：
```python
# Watch only these (empty = all)
WATCH_ENTITIES = ["light.office", "binary_sensor.front_door"]

# Ignore these
IGNORE_ENTITIES = ["sensor.cpu_temp"]
```

### 当 James 请求监控新设备时

1. **询问：** 需要监控的设备 ID 是什么？需要关注的状态是什么？
2. **更新** 脚本中的 `WATCH_EntITIES` 或 `IGNORE_EntITIES` 列表。
3. **重新启动** 监控任务。

## 设备控制

### 检查可访问的设备
```bash
curl -s "http://192.168.0.238:8100/api/states" \
  -H "Authorization: Bearer cb_Z2_Kcoc5Efrztj58lk7SlpZISkwbYlkAkxYjLc_U6lY" \
  | grep -o '"entity_id": "[^"]*"' | cut -d'"' -f4
```

### 检查设备状态
```bash
curl -s "http://192.168.0.238:8100/api/states/{entity_id}" \
  -H "Authorization: Bearer cb_Z2_Kcoc5Efrztj58lk7SlpZISkwbYlkAkxYjLc_U6lY"
```

### 控制设备
```bash
curl -s -X POST "http://192.168.0.238:8100/api/services/{domain}/{service}" \
  -H "Authorization: Bearer cb_Z2_Kcoc5Efrztj58lk7SlpZISkwbYlkAkxYjLc_U6lY" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "{entity_id}"}'
```

**注意：** 所有服务调用都需要通过 ClawBridge 用户界面进行人工确认。

### 快速脚本
```bash
./skills/home-assistant/scripts/ha-control.sh state light.office
./skills/home-assistant/scripts/ha-control.sh on light.office
./skills/home-assistant/scripts/ha-control.sh off light.office
```

## 通知格式

| 通知类型 | 通知内容 |
|--------|---------|
| 灯具 | 💡 **{设备名称}** 已 **开启/关闭** |
| 开关 | 🔌 **{设备名称}** 已 **开启/关闭** |
| 门磁传感器 | 🚪 **{设备名称}** **门已打开/关闭** |
| 运动传感器 | 📡 **{设备名称}** **检测到运动** |
| 人员 | 👤 **{设备名称}** 的状态变为 **{新状态}** |
| 锁具 | 🔒 **{设备名称}** **已锁定/解锁** |
| 其他设备 | 🔔 **{设备名称}** 从 **旧状态** 变为 **新状态** |

## 脚本

| 脚本名称 | 功能 |
|--------|---------|
| `ha-discord.py` | **主要脚本** — 通过 WebSocket 直接发送通知到 Discord（无需成本） |
| `ha-monitor.py` | 通过 WebSocket 将通知内容写入文件（用于定时发送） |
| `ha-control.sh` | 用于快速控制设备（开启/关闭/查看状态）的命令行脚本 |

## API 参考

请参阅 [references/clawbridge-api.md](references/clawbridge-api.md)