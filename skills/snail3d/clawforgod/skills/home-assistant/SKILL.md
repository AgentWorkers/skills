---
name: home-assistant
description: 控制 Home Assistant 智能家居设备，运行自动化任务，并接收 Webhook 事件。适用于控制灯光、开关、空调系统、场景设置、脚本以及任何 Home Assistant 实体。支持通过 REST API（出站通信）和 Webhook（来自 Home Assistant 自动化任务的入站触发）进行双向通信。
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["jq","curl"]}}}
---

# Home Assistant

通过 Home Assistant 的 REST API 和 Webhook 来控制您的智能家居。

## 设置

### 选项 1：配置文件（推荐）

创建 `~/.config/home-assistant/config.json`：
```json
{
  "url": "https://your-ha-instance.duckdns.org",
  "token": "your-long-lived-access-token"
}
```

### 选项 2：环境变量

```bash
export HA_URL="http://homeassistant.local:8123"
export HA_TOKEN="your-long-lived-access-token"
```

### 获取长期有效的访问令牌

1. 打开 Home Assistant → 个人资料（左下角）
2. 滚动到“长期有效访问令牌”（Long-Lived Access Tokens）
3. 点击“创建令牌”（Create Token），并为其命名（例如：“Clawdbot”）
4. 立即复制令牌（该令牌仅显示一次）

## 快速参考

### 列出设备/实体

```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states" | jq '.[].entity_id'
```

### 获取设备/实体状态

```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states/light.living_room"
```

### 控制设备

```bash
# Turn on
curl -X POST -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" \
  "$HA_URL/api/services/light/turn_on" -d '{"entity_id": "light.living_room"}'

# Turn off
curl -X POST -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" \
  "$HA_URL/api/services/light/turn_off" -d '{"entity_id": "light.living_room"}'

# Set brightness (0-255)
curl -X POST -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" \
  "$HA_URL/api/services/light/turn_on" -d '{"entity_id": "light.living_room", "brightness": 128}'
```

### 运行脚本和自动化任务

```bash
# Trigger script
curl -X POST -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/services/script/turn_on" \
  -H "Content-Type: application/json" -d '{"entity_id": "script.goodnight"}'

# Trigger automation
curl -X POST -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/services/automation/trigger" \
  -H "Content-Type: application/json" -d '{"entity_id": "automation.motion_lights"}'
```

### 激活场景

```bash
curl -X POST -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/services/scene/turn_on" \
  -H "Content-Type: application/json" -d '{"entity_id": "scene.movie_night"}'
```

## 常用服务

| 服务领域 | 服务名称 | 示例设备/实体 ID |
|--------|---------|-------------------|
| `light`   | `turn_on`, `turn_off`, `toggle` | `light.kitchen`   |
| `switch`  | `turn_on`, `turn_off`, `toggle` | `switch.fan`   |
| `climate` | `set_temperature`, `set_hvac_mode` | `climate.thermostat` |
| `cover`  | `open_cover`, `close_cover`, `stop_cover` | `cover.garage`   |
| `media_player` | `play_media`, `media.pause`, `volume_set` | `media_player.tv`   |
| `scene`  | `turn_on`   | `scene.relax`   |
| `script`  | `turn_on`   | `script.welcome_home`   |
| `automation` | `trigger`, `turn_on`, `turn_off` | `automation.sunrise` |

## 入站 Webhook（Home Assistant → Clawdbot）

要接收来自 Home Assistant 自动化任务的事件：

### 1. 创建带有 Webhook 动作的自动化任务

```yaml
# In HA automation
action:
  - service: rest_command.notify_clawdbot
    data:
      event: motion_detected
      area: living_room
```

### 2. 在 Home Assistant 中定义 REST 命令

```yaml
# configuration.yaml
rest_command:
  notify_clawdbot:
    url: "https://your-clawdbot-url/webhook/home-assistant"
    method: POST
    headers:
      Authorization: "Bearer {{ webhook_secret }}"
      Content-Type: "application/json"
    payload: '{"event": "{{ event }}", "area": "{{ area }}"}'
```

### 3. 在 Clawdbot 中处理事件

Clawdbot 会接收 Webhook 并根据事件内容通知您或执行相应操作。

## 命令行工具（CLI）

`scripts/ha.sh` 命令行工具可方便地访问 Home Assistant 的所有功能：

```bash
# Test connection
ha.sh info

# List entities
ha.sh list all          # all entities
ha.sh list lights       # just lights
ha.sh list switch       # just switches

# Search entities
ha.sh search kitchen    # find entities by name

# Get/set state
ha.sh state light.living_room
ha.sh states light.living_room   # full details with attributes
ha.sh on light.living_room
ha.sh on light.living_room 200   # with brightness (0-255)
ha.sh off light.living_room
ha.sh toggle switch.fan

# Scenes & scripts
ha.sh scene movie_night
ha.sh script goodnight

# Climate
ha.sh climate climate.thermostat 22

# Call any service
ha.sh call light turn_on '{"entity_id":"light.room","brightness":200}'
```

## 故障排除

- **401 Unauthorized**：令牌过期或无效。请生成新的令牌。
- **连接被拒绝**：检查 HA_URL，确保 Home Assistant 正在运行且可访问。
- **设备/实体未找到**：列出所有设备/实体以找到正确的 ID。

## API 参考

有关高级用法，请参阅 [references/api.md](references/api.md)。