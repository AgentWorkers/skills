---
name: home-assistant
description: >
  **控制 Home Assistant 智能家居设备、运行自动化任务以及接收 Webhook 事件**  
  适用于控制灯光、开关、空调系统、场景设置、脚本执行或任何 Home Assistant 实体。支持通过 REST API（用于发送指令）和 Webhook（用于接收来自 Home Assistant 自动化任务的触发信号）实现双向通信。
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["jq","curl"]}}}
---
# Home Assistant

您可以通过 Home Assistant 的 REST API 和 Webhook 来控制您的智能家居。

## 设置

### 选项 1：配置文件（推荐）

创建 `~/.config/home-assistant/config.json`：
```json
{
  "url": "http://192.168.1.32:8123",
  "token": "<YOUR_LONG_LIVED_ACCESS_TOKEN>"
}
```

### 选项 2：环境变量

```bash
export HA_URL="http://192.168.1.32:8123"
export HA_TOKEN="<YOUR_LONG_LIVED_ACCESS_TOKEN>"
```

### 获取长期有效的访问令牌

1. 打开 Home Assistant → 个人资料（左下角）
2. 滚动到“长期有效访问令牌”（Long-Lived Access Tokens）
3. 点击“创建令牌”（Create Token），并为其命名（例如：“OpenClaw”）
4. 立即复制令牌（该令牌仅显示一次）

## 快速参考

### 列出实体

```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states" | jq '.[].entity_id'
```

### 获取实体状态

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

| 功能领域 | 服务名称 | 示例实体 ID |
|--------|---------|-------------------|
| `light` | `turn_on`（打开），`turn_off`（关闭），`toggle`（切换） | `light.kitchen`（厨房灯） |
| `switch` | `turn_on`（打开），`turn_off`（关闭），`toggle`（切换） | `switch.fan`（风扇开关） |
| `climate` | `set_temperature`（设置温度），`set_hvac_mode`（设置空调模式） | `climate.thermostat`（恒温器） |
| `cover` | `open_cover`（打开遮帘），`close_cover`（关闭遮帘），`stop_cover`（停止遮帘） | `cover.garage`（车库遮帘） |
| `media_player` | `play_media`（播放媒体），`media_pause`（暂停媒体），`volume_set`（设置音量） | `media_player.tv`（电视媒体播放器） |
| `scene` | `turn_on`（激活场景） | `scene.relax`（放松场景） |
| `script` | `turn_on`（运行脚本） | `script.welcome_home`（欢迎回家脚本） |
| `automation` | `trigger`（触发自动化任务），`turn_on`（打开设备），`turn_off`（关闭设备） | `automation.sunrise`（日出自动化任务） |

## 入站 Webhook（Home Assistant → Clawdbot）

要接收来自 Home Assistant 自动化任务的事件：

### 1. 创建带有 Webhook 功能的自动化任务

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

`scripts/ha.sh` 命令行工具可让您轻松访问所有 Home Assistant 功能：

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
- **实体未找到**：列出所有实体以找到正确的实体 ID。

## 本地实体映射

对于此设置，请参考 [references/local-entities.md](references/local-entities.md)，以获取实体名称的友好显示方式（例如：台灯、吊灯）。

## API 参考

有关高级用法，请参阅 [references/api.md](references/api.md)。