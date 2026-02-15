---
name: homeassistant-skill
description: >
  Control Home Assistant devices and automations via REST API. 25 entity domains
  including lights, climate, locks, presence, weather, calendars, notifications,
  scripts, and more. Use when the user asks about their smart home, devices, or automations.
license: MIT
homepage: https://github.com/anotb/homeassistant-skill
compatibility: Requires curl and jq. Network access to Home Assistant instance.
metadata: {"author": "anotb", "version": "2.1.0", "openclaw": {"requires": {"env": ["HA_URL", "HA_TOKEN"], "bins": ["curl", "jq"]}, "primaryEnv": "HA_TOKEN"}}
---

# Home Assistant 技能

通过 Home Assistant 的 REST API 控制智能家居设备。

## 设置

配置环境变量：
- `HA_URL` — 您的 Home Assistant 主机地址（例如：`http://10.0.0.10:8123`）
- `HA_TOKEN` — 长期有效的访问令牌（在 Home Assistant 的“配置”→“用户”→“长期访问令牌”中生成）

## 安全规则

**在执行以下操作前，请务必获得用户的确认：**
- **锁具**：锁定或解锁任何锁具
- **报警面板**：启动或关闭报警系统
- **车库门**：打开或关闭车库门（使用 `device_class: garage`）
- **安全自动化**：禁用与安全相关的自动化脚本
- **遮阳帘**：打开或关闭控制物理访问的遮阳帘（如大门、屏障）

在没有用户明确确认的情况下，切勿对涉及安全的设备进行任何操作。

## 实体发现

### 列出所有实体

```bash
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[].entity_id' | sort
```

### 按领域列出实体

```bash
# Switches
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("switch.")) | "\(.entity_id): \(.state)"'

# Lights
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("light.")) | "\(.entity_id): \(.state)"'

# Sensors
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("sensor.")) | "\(.entity_id): \(.state) \(.attributes.unit_of_measurement // "")"'
```

请根据需要替换领域前缀（如 `switch.`、`light.`、`sensor.` 等），以发现相应领域的实体。

### 获取单个实体的状态

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

# Only lights in an area
curl -s -X POST "$HA_URL/api/template" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ area_entities(\"kitchen\") | select(\"match\", \"light.\") | list }}"}'

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
# Turn on with brightness
curl -s -X POST "$HA_URL/api/services/light/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "brightness_pct": 80}'

# Turn on with color (RGB)
curl -s -X POST "$HA_URL/api/services/light/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "rgb_color": [255, 150, 50]}'

# Turn on with color temperature (mireds)
curl -s -X POST "$HA_URL/api/services/light/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "color_temp": 300}'

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

## 自动化脚本

```bash
# List all automations
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("automation.")) | "\(.entity_id): \(.state)"'

# Trigger an automation
curl -s -X POST "$HA_URL/api/services/automation/trigger" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine"}'

# Enable automation
curl -s -X POST "$HA_URL/api/services/automation/turn_on" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine"}'

# Disable automation
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
  -d '{"entity_id": "climate.thermostat", "temperature": 72}'

# Set HVAC mode (heat, cool, auto, off)
curl -s -X POST "$HA_URL/api/services/climate/set_hvac_mode" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "climate.thermostat", "hvac_mode": "auto"}'
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
```

## 锁具

**安全提示：** 在锁定/解锁锁具之前，请务必获得用户的确认。

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
# Turn on
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

**安全提示：** 在启动或关闭报警系统之前，请务必获得用户的确认。

```bash
# Arm (home mode)
curl -s -X POST "$HA_URL/api/services/alarm_control_panel/alarm_arm_home" \
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

请将 `mobile_app_phone` 替换为实际的服务名称。

## 人员与位置追踪

```bash
# Who is home?
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("person.")) | "\(.attributes.friendly_name // .entity_id): \(.state)"'

# Device tracker locations
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("device_tracker.")) | "\(.entity_id): \(.state)"'
```

状态值：`home`（在家）、`not_home`（不在家）或区域名称。

## 天气信息

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
curl -s "$HA_URL/api/calendars/calendar.personal?start=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)&end=$(date -u -v+7d +%Y-%m-%dT%H:%M:%S.000Z)" \
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

请将 `tts.google_en` 替换为您使用的文本转语音服务，将 `media_player.living_room_speaker` 替换为目标扬声器。

## 调用任意服务

调用 Home Assistant 服务的通用格式如下：

```bash
curl -s -X POST "$HA_URL/api/services/{domain}/{service}" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "domain.entity_name", ...}'
```

### 批量操作

通过传递实体 ID 的数组，一次控制多个实体：

```bash
# Turn off all living room lights at once
curl -s -X POST "$HA_URL/api/services/light/turn_off" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": ["light.living_room", "light.living_room_lamp", "light.living_room_ceiling"]}'
```

## 错误处理

### 检查 API 连接状态

```bash
curl -s -o /dev/null -w "%{http_code}" "$HA_URL/api/" \
  -H "Authorization: Bearer $HA_TOKEN"
# Expect: 200
```

### 在执行操作前验证实体是否存在

```bash
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  "$HA_URL/api/states/light.nonexistent" \
  -H "Authorization: Bearer $HA_TOKEN")
# 200 = exists, 404 = not found
```

### HTTP 状态码

| 状态码 | 含义 |
|------|---------|
| 200 | 操作成功 |
| 400 | 请求错误（JSON 格式不正确或服务数据无效） |
| 401 | 未经授权（令牌错误或缺失） |
| 404 | 实体或端点未找到 |
| 405 | 不允许的 HTTP 方法 |
| 503 | Home Assistant 正在启动或暂时不可用 |

## 响应格式

服务调用会返回受影响实体的状态对象数组：

```json
[{"entity_id": "light.living_room", "state": "on", "attributes": {...}, "last_changed": "..."}]
```

- 如果操作成功且状态未发生变化：返回 `[]`（空数组）
- 获取实体状态（例如：`/api/states/...`）：返回单个实体状态对象
- 出现错误时：返回 `{"message": "..."` 以及相应的 HTTP 错误代码

## 模板解析

`/api/template` 端点会在服务器端解析 Jinja2 模板，适用于计算型查询。

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

# Get entity state in a template
curl -s -X POST "$HA_URL/api/template" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ states(\"light.living_room\") }}"}'

# List all entities that are "on"
curl -s -X POST "$HA_URL/api/template" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ states | selectattr(\"state\", \"eq\", \"on\") | map(attribute=\"entity_id\") | list }}"}'
```

可用的模板函数包括：`states()`、`is_state()`、`state_attr()`、`areas()`、`area_entities()`、`area_name()`、`floors()`、`floor_areas()`、`labels()`、`label_entities()`、`devices()`、`device_entities()`、`now()`、`relative_time()`。

## 历史记录与日志

### 实体状态历史记录

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

## 仪表盘概览

显示所有活跃设备的快速状态信息：

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

# Climate summary (all thermostats)
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("climate.")) | "\(.attributes.friendly_name // .entity_id): \(.state), current: \(.attributes.current_temperature)°, target: \(.attributes.temperature)°"'

# Lock status
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("lock.")) | "\(.attributes.friendly_name // .entity_id): \(.state)"'

# Who is home
curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_TOKEN" \
  | jq -r '.[] | select(.entity_id | startswith("person.")) | "\(.attributes.friendly_name // .entity_id): \(.state)"'
```

## 实体领域

| 领域 | 实体示例 |
|--------|----------|
| `switch.*` | 智能插座、通用开关 |
| `light.*` | 灯具（Hue、LIFX 等） |
| `scene.*` | 预配置的场景 |
| `script.*` | 可重用的动作序列 |
| `automation.*` | 自动化脚本 |
| `climate.*` | 温度控制器、空调设备 |
| `cover.*` | 遮阳帘、车库门 |
| `lock.*` | 智能锁 |
| `fan.*` | 风扇 |
| `media_player.*` | 电视、扬声器、流媒体设备 |
| `vacuum.*` | 吸尘器 |
| `alarm_control_panel.*` | 安防系统 |
| `notify.*` | 通知接收设备 |
| `person.*` | 人员/位置追踪 |
| `device_tracker.*` | 设备位置信息 |
| `weather.*` | 天气状况与预报 |
| `calendar.*` | 日历事件 |
| `tts.*` | 文本转语音服务 |
| `sensor.*` | 温度、湿度、电量等传感器数据 |
| `binary_sensor.*` | 运动传感器、门窗传感器、人员检测 |
| `input_boolean.*` | 布尔值输入开关 |
| `input_number.*` | 数字滑块 |
| `input_select.*` | 下拉选择器 |
| `input_text.*` | 文本输入框 |
| `input_datetime.*` | 日期/时间输入框 |

## 注意事项

- API 默认返回 JSON 格式的数据
- 长期有效的访问令牌不会过期，请妥善保管
- 在使用前，请先用 `list` 命令测试实体 ID 是否正确
- 对于锁具、报警系统和车库门相关的操作，务必在操作前获得用户的确认