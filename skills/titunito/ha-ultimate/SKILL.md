---
name: ha-ultimate
description: 这是一个专为 Home Assistant 设计的 AI 代理技能（Skill）。通过 REST API 可以控制 25 个以上的实体领域（Entity Domains），同时具备安全保护机制、Webhook 功能、库存管理功能以及完整的命令行接口（CLI）支持。该技能支持对灯光、气候系统、门锁、人员检测、天气信息、日历、通知系统、文本到语音（TTS）功能、脚本执行、自动化任务等进行控制。
metadata: {"openclaw":{"emoji":"🏠","requires":{"env":["HA_URL","HA_TOKEN"],"bins":["curl","jq"]},"optionalBins":["node"],"primaryEnv":"HA_TOKEN","configPaths":["$HOME/.config/homeassistant/config.json",".env"]}}
---
# ha-ultimate — 完整的Home Assistant技能

通过Home Assistant的REST API控制您的智能家居，具备安全保护功能、设备清单管理以及全面的设备覆盖能力。

## 设置

### 1. 环境变量

```bash
export HA_URL="http://your-ha-instance:8123"
export HA_TOKEN="your-long-lived-access-token"
```

或者您可以在技能目录下创建一个`.env`文件（由`ha.sh`自动加载）：

```env
HA_URL=http://192.168.1.100:8123
HA_TOKEN=eyJ...your-token...
```

CLI封装工具也会检查`$HOME/.config/homeassistant/config.json`文件作为备用选项（该文件包含`url`和`token`键）。请使用严格的权限保护此文件（`chmod 600`），因为它可能包含您的访问令牌。

### 2. 获取长期有效的访问令牌

1. 打开Home Assistant → 个人资料（左下角）
2. 滚动到“长期访问令牌”
3. 点击“创建令牌”，并为其命名（例如：“OpenClaw”）
4. 立即复制令牌（仅显示一次）

### 3. 测试连接

```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/" | jq
```

或者使用CLI封装工具：

```bash
scripts/ha.sh info
```

### 4. 生成设备清单（推荐，需要Node.js）

**注意：**Node.js是一个**可选**的依赖项，仅在`inventory.js`中需要。如果无法使用Node.js，`ha.sh inventory`会回退到使用curl+jq来列出设备。

```bash
node scripts/inventory.js
```

这会生成`ENTITIES.md`文件，其中包含按领域分类的所有设备信息，包括设备名称、区域和当前状态。**在操作设备之前，请先阅读ENTITIES.md文件**以了解可用的设备。

### 5. Docker / 容器网络

如果在Docker中运行：
- **使用IP地址**（推荐）：`http://192.168.1.100:8123`
- **Tailscale**：`http://homeassistant.ts.net:8123`
- **避免使用mDNS**：在Docker中`homeassistant.local`通常无法解析
- **Nabu Casa**：`https://xxxxx.ui.nabu.casa`（需要订阅）

---

## 安全规则

此技能实现了**分层的安全系统**，以防止对安全关键设备进行意外操作。

### 第一层：强制确认（代理行为）

在执行以下操作之前，**必须始终获得用户的确认**：
- **锁** — 锁定或解锁任何锁具
- **报警面板** — 启用或禁用报警
- **车库门** — 打开或关闭（使用`device_class: garage`的命令）
- **安全自动化** — 禁用与安全相关的自动化
- **遮阳帘** — 打开或关闭控制物理访问的遮阳帘（如大门、屏障）

在没有用户明确确认的情况下，切勿对安全敏感的设备进行任何操作。

### 第二层：关键操作工作流程

对于关键领域（锁、报警面板、车库门、控制物理访问的遮阳帘），在执行任何命令之前，请遵循以下工作流程：
1. **识别操作的性质** — 检查设备领域是否为锁、报警控制面板或遮阳帘（`device_class`为garage/gate）
2. **通知用户并请求确认** — “⚠️ 打开车库门是一个关键操作。您确定要继续吗？”
3. **等待明确的确认** — 用户回答“是”、“好的”、“可以”或任何肯定的回应
4. **只有在得到确认后才能执行命令** — 绝不要在没有确认的情况下执行命令

**重要提示：** 是代理（而非脚本）负责执行这一确认流程。CLI封装工具（`scripts/ha.sh`）会检查`blocked_entities.json`文件，但交互式确认必须在代理对话层面完成，才能对关键领域执行任何命令。

### 第三层：被阻止的设备（可选配置）

用户可以通过在`blocked_entities.json`文件中列出设备来永久阻止这些设备：

```json
{
  "blocked": ["switch.main_breaker", "lock.front_door"],
  "notes": "Main breaker should never be automated. Front door is manual-only."
}
```

**被阻止的设备在任何情况下都无法被控制**，即使获得了用户确认。在执行任何操作之前，请检查该文件是否存在。

---

## CLI封装工具

`scripts/ha.sh` CLI提供了对所有Home Assistant功能的便捷访问：

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

替换领域前缀（`switch.`、`light.`、`sensor.`等）以发现任何领域的设备。

### 获取单个设备的状态

```bash
curl -s "$HA_URL/api/states/ENTITY_ID" -H "Authorization: Bearer $HA_TOKEN"
```

### 区域与楼层发现

使用模板API查询区域、楼层和标签。

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

## 自动化

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

**安全提示：** 在打开/关闭车库门或大门之前，请务必获得用户的确认。

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

**安全提示：** 在锁定/解锁之前，请务必始终获得用户的确认。

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

**安全提示：** 在启用/禁用报警系统之前，请务必始终获得用户的确认。

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

将`mobile_app_phone`替换为列表命令中的实际服务名称。

## 人员与位置

```bash
# Who is home?
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("person.")) | "\(.attributes.friendly_name // .entity_id): \(.state)"'

# Device tracker locations
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("device_tracker.")) | "\(.entity_id): \(.state)"'
```

状态：`home`、`not_home`或区域名称。

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

## 输入辅助设备

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

将`tts.google_en`替换为您的文本转语音服务，将媒体播放器替换为目标扬声器。

---

## 调用任何服务

调用任何Home Assistant服务的一般模式：

```bash
curl -s -X POST "$HA_URL/api/services/{domain}/{service}" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "domain.entity_name", ...}'
```

### 批量操作

通过传递设备ID数组，可以在一次调用中控制多个设备：

```bash
curl -s -X POST "$HA_URL/api/services/light/turn_off" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": ["light.living_room", "light.kitchen", "light.bedroom"]}'
```

---

## 模板评估

 `/api/template`端点在服务器端评估Jinja2模板。这对于需要复杂计算的查询非常有用。

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

可用的模板函数：`states()`、`is_state()`、`state_attr()`、`areas()`、`area_entities()`、`area_name()`、`floors()`、`floor_areas()`、`labels()`、`label_entities()`、`devices()`、`device_entities()`、`now()`、`relative_time()`。

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

### 日志

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

## 仪表板概览

所有活跃设备的快速状态：

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

## 入站Webhook（Home Assistant → 代理）

要接收来自Home Assistant自动化的事件：

### 1. 在Home Assistant中定义REST命令

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

### 2. 使用Webhook动作创建Home Assistant自动化

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

### 3. 在代理中处理

代理会接收Webhook的POST请求，并可以根据事件类型和数据通知用户或采取相应行动。

有关完整的Webhook设置，请参阅[references/webhooks.md](references/webhooks.md)。

---

## 错误处理

### 检查API连接

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

### HTTP状态码

| 代码 | 含义 |
|------|---------|
| 200 | 成功 |
| 400 | 请求错误（JSON格式不正确或服务数据无效） |
| 401 | 未经授权（令牌错误或缺失） |
| 404 | 设备或端点未找到 |
| 405 | 方法不允许（HTTP方法错误） |
| 503 | Home Assistant正在启动或不可用 |

### 响应格式

服务调用会返回受影响设备的状态对象数组：

```json
[{"entity_id": "light.living_room", "state": "on", "attributes": {...}, "last_changed": "..."}]
```

- 如果调用成功且状态未改变：返回`[]`（空数组）
- 获取状态（`/api/states/...`）：返回单个状态对象
- 出现错误：返回`{"message": "..."`以及HTTP错误代码

有关更多故障排除信息，请参阅[references/troubleshooting.md](references/troubleshooting.md)。

---

## 设备领域

| 领域 | 示例 |
|--------|----------|
| `switch.*` | 智能插座、通用开关 |
| `light.*` | 灯具（Hue、LIFX等） |
| `scene.*` | 预配置的场景 |
| `script.*` | 可重用的动作序列 |
| `automation.*` | 自动化任务 |
| `climate.*` | 温控器、空调设备 |
| `cover.*` | 百叶窗、车库门、大门 |
| `lock.*` | 智能锁 |
| `fan.*` | 风扇、通风设备 |
| `media_player.*` | 电视、扬声器、流媒体设备 |
| `vacuum.*` | 吸尘机器人 |
| `alarm_control_panel.*` | 安全系统 |
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
| `input_text.*` | 文本输入 |
| `input_datetime.*` | 日期/时间输入 |

---

## 注意事项

- API默认返回JSON格式的数据
- 长期有效的令牌不会过期 — 请妥善保管
- 在首次使用前，先用列表命令测试设备ID
- 对于锁具、报警系统和车库门，**必须始终获得用户的确认**
- 使用`scripts/inventory.js`在首次使用前生成完整的设备清单
- 在对任何设备执行操作之前，请检查`blocked_entities.json`文件是否存在
- 有关完整的API参考，请参阅[references/api.md](references/api.md)