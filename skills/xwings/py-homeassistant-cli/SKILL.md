---
name: homeassistant-cli
description: 通过 REST API 控制 Home Assistant 设备和自动化规则。支持 25 个实体领域，包括灯光、气候控制、门锁、人员检测、天气信息、日历、通知、脚本等。当用户询问关于他们的智能家居、设备或自动化规则时，可以使用此功能。
license: MIT
homepage: https://github.com/xwings/py-homeassistant-cli
compatibility: Requires Python 3.6+. Network access to Home Assistant instance.
metadata: {"author": "xwings", "version": "3.0.0", "openclaw": {"requires": {"env": [""], "bins": ["python3 {baseDir}/scripts/homeassistant-cli.py"]}, "primaryEnv": ""}}
---
# Home Assistant Skill

通过 `python3 {baseDir}/scripts/homeassistant-cli.py` 这个 Python CLI 工具，可以利用 Home Assistant 的 REST API 来控制智能家居设备。该工具不依赖任何外部库，仅使用 Python 标准库。

## 设置

可以通过环境变量或命令行参数进行配置（命令行参数具有优先级）：

```bash
# Environment variables
export HA_URL="http://10.0.0.10:8123"
export HA_TOKEN="your_long_lived_access_token"

# Or pass via args (overrides env vars)
python3 {baseDir}/scripts/homeassistant-cli.py --server http://10.0.0.10:8123 --token YOUR_TOKEN check
```

对于任何命令，可以使用 `--help` 选项查看详细信息：`python3 {baseDir}/scripts/homeassistant-cli.py light --help`

## 安全规则

**在以下操作之前，请务必先获得用户的确认：**  
- 锁定/解锁门锁  
- 启用/关闭报警系统  
- 打开/关闭车库门或大门  
- 禁用安全自动化功能  

## 命令参考

所有命令的格式如下：  
`python3 {baseDir}/scripts/homeassistant-cli.py [--server URL] [--token TOKEN] <command> [args]`

### 发现设备与状态查询  
```bash
check                                          # Check API connectivity
entities                                       # List all entities
entities --domain light                        # List entities by domain (light, switch, sensor, etc.)
state <entity_id>                              # Get full entity state JSON
areas                                          # List all areas
area-entities <area> [--domain light]          # Entities in an area, optionally filtered
area-of <entity_id>                            # Find which area an entity belongs to
floors                                         # List all floors and their areas
services [--domain light]                      # List available services
dashboard                                      # Quick overview: lights on, doors, temps, locks, presence
presence [--trackers]                          # Who is home (--trackers for device trackers)
weather [--forecast daily|hourly] [-e entity]  # Current weather or forecast
```

### 控制设备  
```bash
switch <turn_on|turn_off|toggle> <entity_id>
light <turn_on|turn_off> <entity_id> [--brightness 80] [--rgb 255,150,50] [--color-temp 300]
fan <turn_on|turn_off> <entity_id> [--percentage 50]
cover <open|close|set_position> <entity_id> [--position 50]
lock <lock|unlock> <entity_id>
media <play_pause|volume> <entity_id> [--level 0.5]
vacuum <start|dock> <entity_id>
climate <state|set_temp|set_mode> <entity_id> [--temperature 72] [--mode auto]
alarm <arm_home|disarm> <entity_id> [--code 1234]
scene <entity_id>
```

### 自动化脚本  
```bash
automation <list|trigger|enable|disable> [entity_id]
script <list|run> [entity_id] [--variables '{"key": "value"}']
```

### 通知功能  
```bash
notify list                                                    # List notification targets
notify send <service> "message" [--title "title"]              # Send notification
```

### 输入辅助工具  
```bash
input boolean <entity_id>                   # Toggle
input number <entity_id> <value>            # Set number
input select <entity_id> "option"           # Set selection
input text <entity_id> "value"              # Set text
input datetime <entity_id> "07:30:00"       # Set time
```

### 日历与语音合成（TTS）  
```bash
calendar list                                              # List calendars
calendar events <entity_id> [--days 14]                    # Upcoming events
tts <tts_entity> <media_player_entity> "message"           # Text-to-speech
```

### 模板、历史记录与日志  
```bash
template '{{ states.light | list | count }} lights'                                    # Evaluate Jinja2
history <entity_id> [--start ISO8601] [--end ISO8601]                                  # State history
logbook [--entity entity_id] [--limit 20]                                              # Logbook entries
```

常用的模板函数包括：  
`states()`、`is_state()`、`state_attr()`、`areas()`、`area_entities()`、`area_name()`、`floors()`、`floor_areas()`、`labels()`、`label_entities()`、`devices()`、`device_entities()`、`now()`、`relative_time()`。

### 通用服务调用  
```bash
service <domain> <service> --data '{"entity_id": "light.living_room"}'

# Batch: pass array of entity_ids
service light turn_off --data '{"entity_id": ["light.room1", "light.room2"]}'
```

## Tesla 相关功能  

相关实体包括：  
`sensor.mao_dou_battery`（电池状态传感器）、`device_tracker.mao_dou_location_tracker`（设备位置追踪器）、`device_tracker.mao_dou_destination_location_tracker`（目的地位置追踪器）、`automation.tesla_battery_below_20`（特斯拉电池电量低于 20% 的自动化规则）  

## 实体类型  

| 实体类型 | 举例设备 |  
|--------|---------|  
| `switch.*` | 智能插座  
| `light.*` | 灯具（如 Hue、LIFX）  
| `climate.*` | 温控器、空调  
| `cover.*` | 百叶窗、车库门  
| `lock.*` | 智能锁  
| `fan.*` | 风扇、通风设备  
| `media_player.*` | 电视、音响设备  
| `vacuum.*` | 吸尘机器人  
| `alarm_control_panel.*` | 安防系统  
| `scene.*` | 预定义的场景  
| `script.*` | 动作序列  
| `sensor.*` | 温度、湿度传感器  
| `binary_sensor.*` | 运动传感器、门窗传感器  
| `person.*` | 人员检测传感器  
| `device_tracker.*` | 设备位置追踪器  
| `weather.*` | 天气/预报信息  
| `calendar.*` | 日历事件  
| `notify.*` | 通知目标  
| `tts.*` | 语音合成服务  
| `input_boolean.*` | 虚拟开关  
| `input_number.*` | 数字滑块  
| `input_select.*` | 下拉选择框  
| `input_text.*` | 文本输入框  
| `input_datetime.*` | 日期/时间输入框  

## HTTP 状态码  

| 状态码 | 含义 |  
|------|---------|  
| 200 | 操作成功  
| 400 | 请求错误（JSON 格式不正确）  
| 401 | 未经授权（令牌无效或缺失）  
| 404 | 未找到相应的实体或端点  
| 503 | Home Assistant 正在启动中或暂时不可用  

## 注意事项：  
- 长期有效的令牌不会过期，请妥善保管。  
- 在使用相关命令前，建议先使用 `entities --domain` 命令查询实体信息。  
- 对于未包含在专用命令中的操作，请使用 `service` 命令来执行。  
- 服务调用会返回受影响的实体状态信息（以 JSON 数组形式）；错误信息会输出到标准错误流（stderr）。