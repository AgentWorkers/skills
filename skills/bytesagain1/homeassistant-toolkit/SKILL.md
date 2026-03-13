---
name: homeassistant-toolkit
version: 1.0.0
description: 通过 REST API 与 Home Assistant 深度集成。可以从命令行控制设备、管理自动化任务、查询实体状态以及编排场景/脚本。
---
# Home Assistant 工具包

> 专为 Home Assistant 高级用户设计的功能齐全的命令行工具（CLI），无需打开浏览器即可控制您的智能家居。

## 先决条件

| 条件 | 详情 |
|---|---|
| Home Assistant | 版本需达到 2023.1 或更高，并且已启用 REST API |
| 长期有效的访问令牌 | 请在 `/profile` 页面生成长期有效的访问令牌 |
| Python 3.6 或更高版本 | 大多数系统已预装 Python 3.6 |
| `curl` | 用于直接进行 API 调用（作为备用方式） |

## 环境变量

```bash
export HA_URL="http://192.168.1.100:8123"    # Your HA instance URL
export HA_TOKEN="eyJ0eXAiOiJKV..."           # Long-Lived Access Token
```

## 快速入门

```bash
# Check connection & server info
bash scripts/ha-toolkit.sh status

# List all entities
bash scripts/ha-toolkit.sh entities

# Turn on a light
bash scripts/ha-toolkit.sh call light.turn_on light.living_room

# Get entity state
bash scripts/ha-toolkit.sh state sensor.temperature_outdoor

# Fire an automation
bash scripts/ha-toolkit.sh automation trigger automation.morning_routine

# List all scenes and activate one
bash scripts/ha-toolkit.sh scenes
bash scripts/ha-toolkit.sh scene activate scene.movie_night
```

## 命令参考

### 设备控制

| 命令 | 描述 |
|---|---|
| `call <service> <entity_id> [json_data]` | 调用任意 Home Assistant 服务，可携带 JSON 数据 |
| `toggle <entity_id>` | 切换设备的开关状态 |
| `state <entity_id>` | 获取设备的完整状态及属性 |
| `entities [domain]` | 列出所有设备，可按域名进行筛选 |
| `history <entity_id> [hours]` | 获取设备的状态历史记录（默认为 24 小时） |

### 自动化管理

| 命令 | 描述 |
|---|---|
| `automations` | 列出所有自动化任务及其状态 |
| `automation trigger <automation_id>` | 手动触发某个自动化任务 |
| `automation enable <automation_id>` | 启用被禁用的自动化任务 |
| `automation disable <automation_id>` | 禁用某个自动化任务 |

### 场景与脚本

| 命令 | 描述 |
|---|---|
| `scenes` | 列出所有配置好的场景 |
| `scene activate <scene_id>` | 激活某个场景 |
| `scripts` | 列出所有脚本 |
| `script run <script_id>` | 运行某个脚本 |

### 系统与诊断

| 命令 | 描述 |
|---|---|
| `status` | 查看 Home Assistant 服务器信息（版本、位置、时区） |
| `config` | 显示 Home Assistant 的完整配置 |
| `logs [lines]` | 获取最近的日志记录 |
| `services [domain]` | 列出可用的服务 |
| `dashboard` | 提供关键设备的交互式概览 |

## 高级用法

### 批量操作

```bash
# Turn off all lights
bash scripts/ha-toolkit.sh call light.turn_off all

# Set multiple attributes
bash scripts/ha-toolkit.sh call light.turn_on light.bedroom '{"brightness": 128, "color_temp": 350}'
```

### 监控模式

```bash
# Watch an entity for changes (polls every 5 seconds)
bash scripts/ha-toolkit.sh watch sensor.power_consumption 5
```

### 与 Cron 任务集成

```bash
# Check garage door every 30 min, notify if open
*/30 * * * * bash /path/to/ha-toolkit.sh state cover.garage_door | grep -q "open" && echo "Garage is open!" | mail -s "Alert" you@example.com
```

## 错误处理

该工具包会进行以下检查：
- 在执行任何 API 调用之前，确保 `HA_URL` 和 `HA_TOKEN` 已正确设置 |
- 处理 HTTP 响应码（如 401（未经授权）、404（未找到等） |
- 对 JSON 数据进行解析，并提供优雅的错误处理机制 |
- 实现网络连接的超时控制

## 故障排除

- **“连接被拒绝”**：请确认 Home Assistant 正在运行且 URL 正确，同时检查防火墙规则。
- **“401 未经授权”**：可能是访问令牌过期或无效，请从 Home Assistant 的配置页面重新生成令牌。
- **“设备未找到”**：使用 `entities` 命令列出有效的设备 ID，并检查设备所属的域名前缀（例如 `light.` 或 `switch.`）。

## 安全注意事项

- 令牌仅从环境变量中读取，不会被脚本保存到磁盘上 |
- 当您的 Home Assistant 实例支持 HTTPS 时，所有 API 调用都会使用 HTTPS 协议 |
- 建议为自动化脚本分配具有有限权限的专用用户账户。