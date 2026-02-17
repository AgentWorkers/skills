---
name: homeassistant
description: 这是一个专为 Home Assistant 设计的 AI 代理技能（Skill）。通过 REST API，可以控制 25 个以上的实体领域（Entity Domains），同时具备安全保护机制、Webhook 功能、库存管理功能以及完整的命令行界面（CLI）支持。支持的功能包括：灯光控制、气候调节、门锁控制、人员检测、天气信息、日历管理、通知系统、文本到语音（TTS）转换、脚本执行、自动化任务等。
metadata: {"openclaw":{"emoji":"🏠","requires":{"env":["HA_URL","HA_TOKEN"],"bins":["curl","jq"]},"primaryEnv":"HA_TOKEN"}}
---
# Home Assistant — 终极技能

通过 Home Assistant 的 REST API 控制您的智能家居，具备安全防护功能、设备清单管理以及全面的设备覆盖能力。

## 设置

### 1. 环境变量

```bash
export HA_URL="http://your-ha-instance:8123"
export HA_TOKEN="your-long-lived-access-token"
```

或者可以在技能目录下创建一个 `.env` 文件（某些代理会自动加载该文件）：

```env
HA_URL=http://192.168.1.100:8123
HA_TOKEN=eyJ...your-token...
```

### 2. 获取长期有效的访问令牌

1. 打开 Home Assistant → 个人资料（左下角）
2. 滚动到“长期有效访问令牌”部分
3. 点击“创建令牌”，并为其命名（例如：“OpenClaw”）
4. 立即复制令牌（仅显示一次）

### 3. 测试连接

```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/" | jq
```

或者使用 CLI 包装器进行测试：

```bash
scripts/ha.sh info
```

### 4. 生成设备清单（推荐）

运行一次命令以创建完整的设备清单：

```bash
node scripts/inventory.js
```

该命令会生成 `ENTITIES.md` 文件，其中包含按领域分类的设备信息（名称、区域和当前状态）。**在操作设备之前，请先阅读 ENTITIES.md 文件**，以了解可用的设备。

### 5. Docker / 容器网络

如果在 Docker 中运行：
- **建议使用 IP 地址**：`http://192.168.1.100:8123`
- **Tailscale**：`http://homeassistant.ts.net:8123`
- **避免使用 mDNS**：在 Docker 中 `homeassistant.local` 通常无法解析
- **Nabu Casa**：`https://xxxxx.ui.nabu.casa`（需要订阅）

---

## 安全规则

本技能实现了**分层安全系统**，以防止对安全关键设备进行意外操作。

### 第一层：强制确认（代理行为）

在执行以下操作之前，**必须先获得用户的确认**：
- **锁具** — 锁上或解锁任何锁具
- **报警面板** — 启用或关闭报警
- **车库门** — 打开或关闭车库门（使用 `device_class: garage`）
- **安全自动化** — 禁用与安全相关的自动化任务
- **遮阳帘** — 打开或关闭控制物理访问的遮阳帘（如大门、屏障）

在没有用户明确确认的情况下，切勿对安全敏感的设备进行任何操作。

### 第二层：关键操作模式

对于关键领域，使用以下工作流程：
1. **尝试执行操作** — 正常执行命令
2. **通知用户** — “⚠️ 打开车库门是一个关键操作。您确定要继续吗？”
3. **等待用户确认** — 用户回答“是”、“好的”、“可以”或任何肯定的答复
4. **只有在得到确认后** — 才继续执行操作

可接受的确认回答包括：“是”、“好的”、“可以”、“执行”或任何明确的肯定答复。不需要使用特定的短语。

### 第三层：被屏蔽的设备（可选配置）

用户可以通过在 `blocked_entities.json` 文件中列出设备来永久屏蔽这些设备：

```json
{
  "blocked": ["switch.main_breaker", "lock.front_door"],
  "notes": "Main breaker should never be automated. Front door is manual-only."
}
```

**被屏蔽的设备在任何情况下都无法被控制**，即使用户已确认也是如此。在执行任何操作之前，请检查该文件是否存在。

---

## CLI 包装器

`scripts/ha.sh` CLI 提供了对 Home Assistant 所有功能的便捷访问：

```bash
# Test connection
scripts/ha.sh info

# List entities
scripts/ha.sh list all          # all entities
scripts/ha.sh list light        # just lights
scripts/ha.sh list switch       # just switches

# Search entities
scripts/ha.sh search kitchen    # find entities by name

# Get/set state
scripts/ha.sh state light.living_room
scripts/ha.sh full light.living_room    # full details with attributes
scripts/ha.sh on light.living_room
scripts/ha.sh on light.living_room 200  # with brightness (0-255)
scripts/ha.sh off light.living_room
scripts/ha.sh toggle switch.fan

# Scenes & scripts
scripts/ha.sh scene movie_night
scripts/ha.sh script goodnight

# Climate
scripts/ha.sh climate climate.thermostat 22

# Dashboard (quick status of everything)
scripts/ha.sh dashboard

# Call any service
scripts/ha.sh call light turn_on '{"entity_id":"light.room","brightness":200}'

# Areas
scripts/ha.sh areas
```

---

## 设备发现

### 列出所有设备

```bash
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[].entity_id' | sort
```

### 按领域列出设备

```bash
# Lights
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("light.")) | "\(.entity_id): \(.state)"'

# Sensors (with units)
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("sensor.")) | "\(.entity_id): \(.state) \(.attributes.unit_of_measurement // "")"'
```

替换 `switch.`、`light.`、`sensor.` 等前缀，可以查询任何领域的设备。

### 获取单个设备的状态

```bash
curl -s "$HA_URL/api/states/ENTITY_ID" -H "Authorization: Bearer $HA_TOKEN"
```

### 区域与楼层发现

使用模板 API 查询区域、楼层和标签信息。

```bash
# List all areas
curl -s -X POST "$HA_URL/api/template" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ areas() }}"}'

# Entities in a specific area
curl -s -X POST "$HA_URL/api/template" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ area_entities(\"kitchen\") }}"}'

# Find which area an entity belongs to
curl -s -X POST "$HA_URL/api/template" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ area_name(\"light.kitchen\") }}"}'

# List all floors and their areas
curl -s -X POST "$HA_URL/api/template" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "{% for floor in floors() %}{{ floor }}: {{ floor_areas(floor) }}\n{% endfor %}"}'
```

---

## 开关

```bash
# Turn on
curl -s -X POST "$HA_URL/api/services/switch/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "switch.office_lamp"}'

# Turn off
curl -s -X POST "$HA_URL/api/services/switch/turn_off" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "switch.office_lamp"}'

# Toggle
curl -s -X POST "$HA_URL/api/services/switch/toggle" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "switch.office_lamp"}'
```

## 灯具

```bash
# Turn on with brightness (percentage)
curl -s -X POST "$HA_URL/api/services/light/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "brightness_pct": 80}'

# Turn on with color (RGB)
curl -s -X POST "$HA_URL/api/services/light/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "rgb_color": [255, 150, 50]}'

# Turn on with color temperature (mireds, 153-500)
curl -s -X POST "$HA_URL/api/services/light/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "color_temp": 300}'

# Turn on with transition (seconds)
curl -s -X POST "$HA_URL/api/services/light/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "brightness_pct": 100, "transition": 3}'

# Turn off
curl -s -X POST "$HA_URL/api/services/light/turn_off" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room"}'
```

## 场景

```bash
curl -s -X POST "$HA_URL/api/services/scene/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "scene.movie_time"}'
```

## 脚本

```bash
# List all scripts
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("script.")) | "\(.entity_id): \(.state)"'

# Run a script
curl -s -X POST "$HA_URL/api/services/script/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "script.bedtime_routine"}'

# Run a script with variables
curl -s -X POST "$HA_URL/api/services/script/bedtime_routine" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"variables": {"brightness": 20, "delay_minutes": 5}}'
```

## 自动化任务

```bash
# List all automations
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("automation.")) | "\(.entity_id): \(.state)"'

# Trigger an automation
curl -s -X POST "$HA_URL/api/services/automation/trigger" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine"}'

# Enable / Disable automation
curl -s -X POST "$HA_URL/api/services/automation/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine"}'

curl -s -X POST "$HA_URL/api/services/automation/turn_off" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine"}'
```

## 气候控制

```bash
# Get thermostat state
curl -s "$HA_URL/api/states/climate.thermostat" -H "Authorization: Bearer $HA_TOKEN" \
  | jq '{state: .state, current_temp: .attributes.current_temperature, target_temp: .attributes.temperature}'

# Set temperature
curl -s -X POST "$HA_URL/api/services/climate/set_temperature" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "climate.thermostat", "temperature": 22}'

# Set HVAC mode (heat, cool, auto, off)
curl -s -X POST "$HA_URL/api/services/climate/set_hvac_mode" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "climate.thermostat", "hvac_mode": "auto"}'

# Set preset mode (away, home, sleep, etc.)
curl -s -X POST "$HA_URL/api/services/climate/set_preset_mode" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "climate.thermostat", "preset_mode": "away"}'
```

## 遮阳帘（百叶窗、车库门）

**安全提示：** 在打开/关闭车库门或大门之前，请先获得用户的确认。

```bash
# Open
curl -s -X POST "$HA_URL/api/services/cover/open_cover" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "cover.garage_door"}'

# Close
curl -s -X POST "$HA_URL/api/services/cover/close_cover" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "cover.garage_door"}'

# Set position (0 = closed, 100 = open)
curl -s -X POST "$HA_URL/api/services/cover/set_cover_position" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "cover.blinds", "position": 50}'

# Stop
curl -s -X POST "$HA_URL/api/services/cover/stop_cover" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "cover.blinds"}'
```

## 锁具

**安全提示：** 在锁上/解锁之前，请务必先获得用户的确认。

```bash
# Lock
curl -s -X POST "$HA_URL/api/services/lock/lock" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "lock.front_door"}'

# Unlock
curl -s -X POST "$HA_URL/api/services/lock/unlock" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "lock.front_door"}'
```

## 风扇

```bash
# Turn on with speed percentage
curl -s -X POST "$HA_URL/api/services/fan/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "fan.bedroom", "percentage": 50}'

# Turn off
curl -s -X POST "$HA_URL/api/services/fan/turn_off" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "fan.bedroom"}'
```

## 媒体播放器

```bash
# Play/pause
curl -s -X POST "$HA_URL/api/services/media_player/media_play_pause" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "media_player.living_room_tv"}'

# Set volume (0.0 to 1.0)
curl -s -X POST "$HA_URL/api/services/media_player/volume_set" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "media_player.living_room_tv", "volume_level": 0.5}'

# Play media
curl -s -X POST "$HA_URL/api/services/media_player/play_media" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "media_player.tv", "media_content_id": "https://example.com/stream", "media_content_type": "music"}'
```

## 吸尘器

```bash
# Start cleaning
curl -s -X POST "$HA_URL/api/services/vacuum/start" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "vacuum.robot"}'

# Return to dock
curl -s -X POST "$HA_URL/api/services/vacuum/return_to_base" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "vacuum.robot"}'
```

## 报警控制面板

**安全提示：** 在启用/关闭报警系统之前，请先获得用户的确认。

```bash
# Arm (home mode)
curl -s -X POST "$HA_URL/api/services/alarm_control_panel/alarm_arm_home" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "alarm_control_panel.home"}'

# Arm (away mode)
curl -s -X POST "$HA_URL/api/services/alarm_control_panel/alarm_arm_away" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "alarm_control_panel.home"}'

# Disarm (requires code if configured)
curl -s -X POST "$HA_URL/api/services/alarm_control_panel/alarm_disarm" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "alarm_control_panel.home", "code": "1234"}'
```

## 通知

```bash
# List available notification targets
curl -s "$HA_URL/api/services" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.domain == "notify") | .services | keys[]' | sort

# Send a notification to a mobile device
curl -s -X POST "$HA_URL/api/services/notify/mobile_app_phone" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Front door opened", "title": "Home Alert"}'

# Send to all devices (default notify service)
curl -s -X POST "$HA_URL/api/services/notify/notify" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "System alert", "title": "Home Assistant"}'
```

将 `mobile_app_phone` 替换为实际的服务名称。

## 人员与位置追踪

```bash
# Who is home?
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("person.")) | "\(.attributes.friendly_name // .entity_id): \(.state)"'

# Device tracker locations
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("device_tracker.")) | "\(.entity_id): \(.state)"'
```

状态：`home`、`not_home` 或区域名称。

## 天气

```bash
# Current weather
curl -s "$HA_URL/api/states/weather.home" -H "Authorization: Bearer $HA_TOKEN" \
  | jq '{state: .state, temperature: .attributes.temperature, humidity: .attributes.humidity, wind_speed: .attributes.wind_speed}'

# Get forecast (daily)
curl -s -X POST "$HA_URL/api/services/weather/get_forecasts" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "weather.home", "type": "daily"}'

# Get forecast (hourly)
curl -s -X POST "$HA_URL/api/services/weather/get_forecasts" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "weather.home", "type": "hourly"}'
```

## 输入辅助功能

```bash
# Toggle an input boolean
curl -s -X POST "$HA_URL/api/services/input_boolean/toggle" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_boolean.guest_mode"}'

# Set input number
curl -s -X POST "$HA_URL/api/services/input_number/set_value" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_number.target_temperature", "value": 72}'

# Set input select
curl -s -X POST "$HA_URL/api/services/input_select/select_option" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_select.house_mode", "option": "Away"}'

# Set input text
curl -s -X POST "$HA_URL/api/services/input_text/set_value" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_text.welcome_message", "value": "Welcome home!"}'

# Set input datetime
curl -s -X POST "$HA_URL/api/services/input_datetime/set_datetime" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_datetime.alarm_time", "time": "07:30:00"}'
```

## 日历

```bash
# List all calendars
curl -s "$HA_URL/api/calendars" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[].entity_id'

# Get upcoming events (next 7 days)
START=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)
END=$(date -u -d "+7 days" +%Y-%m-%dT%H:%M:%S.000Z 2>/dev/null || date -u -v+7d +%Y-%m-%dT%H:%M:%S.000Z)
curl -s "$HA_URL/api/calendars/calendar.personal?start=$START&end=$END" \
  -H "Authorization: Bearer $HA_TOKEN" \
  | jq '[.[] | {summary: .summary, start: .start.dateTime, end: .end.dateTime}]'
```

## 文本转语音

```bash
curl -s -X POST "$HA_URL/api/services/tts/speak" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "tts.google_en", "media_player_entity_id": "media_player.living_room_speaker", "message": "Dinner is ready"}'
```

将 `tts.google_en` 替换为您的文本转语音服务，将 `media_player` 替换为目标扬声器。

---

## 调用任何服务

调用 Home Assistant 服务的通用模式：

```bash
curl -s -X POST "$HA_URL/api/services/{domain}/{service}" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "domain.entity_name", ...}'
```

### 批量操作

通过传递设备 ID 数组，可以一次性控制多个设备：

```bash
curl -s -X POST "$HA_URL/api/services/light/turn_off" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": ["light.living_room", "light.kitchen", "light.bedroom"]}'
```

---

## 模板评估

`/api/template` 端点会在服务器端评估 Jinja2 模板。这对于需要复杂计算的查询非常有用（而不仅仅是读取设备状态）。

```bash
curl -s -X POST "$HA_URL/api/template" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "TEMPLATE_STRING"}'
```

### 示例

```bash
# Count entities by domain
curl -s -X POST "$HA_URL/api/template" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ states.light | list | count }} lights"}'

# List all entities that are "on"
curl -s -X POST "$HA_URL/api/template" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ states | selectattr(\"state\", \"eq\", \"on\") | map(attribute=\"entity_id\") | list }}"}'

# Entities in an area filtered by domain
curl -s -X POST "$HA_URL/api/template" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ area_entities(\"kitchen\") | select(\"match\", \"light.\") | list }}"}'
```

可用的模板函数包括：`states()`、`is_state()`、`state_attr()`、`areas()`、`area_entities()`、`area_name()`、`floors()`、`floor_areas()`、`labels()`、`label_entities()`、`devices()`、`device_entities()`、`now()`、`relative_time()`。

---

## 历史记录与日志

### 设备状态历史

```bash
# Last 24 hours for a specific entity
curl -s "$HA_URL/api/history/period?filter_entity_id=sensor.temperature" \
  -H "Authorization: Bearer $HA_TOKEN" \
  | jq '.[0] | [.[] | {state: .state, last_changed: .last_changed}]'

# Specific time range (ISO 8601)
curl -s "$HA_URL/api/history/period/2025-01-15T00:00:00Z?end_time=2025-01-15T23:59:59Z&filter_entity_id=sensor.temperature" \
  -H "Authorization: Bearer $HA_TOKEN" \
  | jq '.[0]'
```

### 日志记录

```bash
# Recent logbook entries
curl -s "$HA_URL/api/logbook" -H "Authorization: Bearer $HA_TOKEN" \
  | jq '.[:10]'

# Logbook for a specific entity
curl -s "$HA_URL/api/logbook?entity=light.living_room" \
  -H "Authorization: Bearer $HA_TOKEN" \
  | jq '.[:10] | [.[] | {name: .name, message: .message, when: .when}]'
```

---

## 仪表盘概览

快速查看所有活跃设备的状态：

```bash
# All lights that are on
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("light.")) | select(.state == "on") | .entity_id'

# All open doors/windows (binary sensors)
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("binary_sensor.")) | select(.state == "on") | select(.attributes.device_class == "door" or .attributes.device_class == "window") | .entity_id'

# Temperature sensors
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("sensor.")) | select(.attributes.device_class == "temperature") | "\(.attributes.friendly_name // .entity_id): \(.state)\(.attributes.unit_of_measurement // "")"'

# Climate summary
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("climate.")) | "\(.attributes.friendly_name // .entity_id): \(.state), current: \(.attributes.current_temperature)°, target: \(.attributes.temperature)°"'

# Lock status
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("lock.")) | "\(.attributes.friendly_name // .entity_id): \(.state)"'

# Who is home
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("person.")) | "\(.attributes.friendly_name // .entity_id): \(.state)"'
```

---

## 入站 Webhook（Home Assistant → 代理）

要接收来自 Home Assistant 自动化的事件：

### 1. 在 Home Assistant 中定义 REST 命令

```yaml
# configuration.yaml
rest_command:
  notify_agent:
    url: "https://your-agent-url/webhook/home-assistant"
    method: POST
    headers:
      Authorization: "Bearer {{ webhook_secret }}"
      Content-Type: "application/json"
    payload: '{"event": "{{ event }}", "area": "{{ area }}", "entity": "{{ entity }}"}'
```

### 2. 使用 Webhook 功能创建自动化任务

```yaml
# automations.yaml
- alias: "Notify agent on motion"
  trigger:
    - platform: state
      entity_id: binary_sensor.motion_hallway
      to: "on"
  action:
    - service: rest_command.notify_agent
      data:
        event: motion_detected
        area: hallway
        entity: binary_sensor.motion_hallway
```

### 3. 代理处理

代理会接收 Webhook 的 POST 请求，并根据事件类型和数据通知用户或采取相应操作。

有关完整的 Webhook 设置，请参阅 [references/webhooks.md](references/webhooks.md)。

---

## 错误处理

### 检查 API 连接

```bash
curl -s -o /dev/null -w "%{http_code}" "$HA_URL/api/" \
  -H "Authorization: Bearer $HA_TOKEN"
# Expect: 200
```

### 在执行操作前验证设备是否存在

```bash
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  "$HA_URL/api/states/light.nonexistent" \
  -H "Authorization: Bearer $HA_TOKEN")
# 200 = exists, 404 = not found
```

### HTTP 状态码

| 代码 | 含义 |
|------|---------|
| 200 | 成功 |
| 400 | 请求错误（JSON 格式不正确或服务数据无效） |
| 401 | 未经授权（令牌错误或缺失） |
| 404 | 设备或端点未找到 |
| 405 | 方法不允许（使用了错误的 HTTP 方法） |
| 503 | Home Assistant 正在启动或不可用 |

### 响应格式

服务调用会返回受影响设备的状态对象数组：

```json
[{"entity_id": "light.living_room", "state": "on", "attributes": {...}, "last_changed": "..."}]
```

- 如果调用成功但状态没有变化：返回 `[]`（空数组）
- 读取设备状态（`/api/states/...`）：返回单个设备状态对象
- 出现错误：返回 `{"message": "..."` 以及相应的 HTTP 错误代码

有关更多故障排除信息，请参阅 [references/troubleshooting.md](references/troubleshooting.md)。

---

## 设备领域

| 领域 | 示例 |
|--------|----------|
| `switch.*` | 智能插座、通用开关 |
| `light.*` | 灯具（Hue、LIFX 等） |
| `scene.*` | 预配置的场景 |
| `script.*` | 可重用的动作序列 |
| `automation.*` | 自动化任务 |
| `climate.*` | 温控器、空调设备 |
| `cover.*` | 遮阳帘、车库门、大门 |
| `lock.*` | 智能锁 |
| `fan.*` | 风扇、通风设备 |
| `media_player.*` | 电视、扬声器、流媒体设备 |
| `vacuum.*` | 吸尘器 |
| `alarm_control_panel.*` | 安防系统 |
| `notify.*` | 通知目标 |
| `person.*` | 人员/位置追踪 |
| `device_tracker.*` | 设备位置 |
| `weather.*` | 天气状况和预报 |
| `calendar.*` | 日历事件 |
| `tts.*` | 文本转语音引擎 |
| `sensor.*` | 温度、湿度、电量等 |
| `binary_sensor.*` | 运动传感器、门/窗传感器、人员感应 |
| `input_boolean.*` | 虚拟开关 |
| `input_number.*` | 数字滑块 |
| `input_select.*` | 下拉选择器 |
| `input_text.*` | 文本输入框 |
| `input_datetime.*` | 日期/时间输入框 |

---

## 注意事项

- API 默认返回 JSON 格式的数据
- 长期有效的访问令牌不会过期——请妥善保管
- 在使用前，请先用 `list` 命令测试设备 ID
- 对于锁具、报警系统和车库门，操作前务必先获得用户确认
- 使用 `scripts/inventory.js` 生成完整的设备清单
- 在操作任何设备之前，请检查 `blocked_entities.json` 文件是否存在
- 有关完整的 API 参考，请参阅 [references/api.md](references/api.md)