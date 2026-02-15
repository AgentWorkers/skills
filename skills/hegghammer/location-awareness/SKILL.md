---
name: location-awareness
version: 1.2.0
description: 通过隐私友好的GPS追踪实现位置感知（适用于Home Assistant、OwnTracks、GPS Logger）。可以设置基于位置的提醒，并查询移动历史、旅行时间以及附近的兴趣点（POIs）。
metadata: {"clawdbot":{"emoji":"📍","requires":{"bins":["python3"]}}}
---

# 位置感知功能

**该功能提供了一系列可执行的命令。当用户询问位置相关信息时，请运行相应的命令。**

## ⚠️ 重要提示：所有命令均需通过 `scripts/location.sh` 来执行**

所有命令都必须通过 `scripts/location.sh` 来执行。例如：

**用户提问：“步行回家需要多长时间？”**  
**你运行：**  
```bash
scripts/location.sh eta home --mode walk
```  
**输出结果：** `4.6 公里，大约需要 45 分钟步行**  
**你直接将输出结果告知用户。**

**注意：** 请勿直接运行 `eta` 或其他子命令——这些命令并非独立的可执行文件。

## 快速参考 — 需要执行的命令**

| 用户输入 | 应执行的命令 | 回答内容 |
|-----------|----------|------------|
| “我在哪里？” | `scripts/location.sh status` | 仅返回所在区域的名称 |
| “地图” / “地图链接” | `scripts/location.sh herewego` | 仅提供地图的 URL |
| “我的坐标是什么？” | `scripts/location.sh status` | 从输出中获取经纬度坐标 |
| “步行回家需要多长时间？” | `scripts/location.sh eta home --mode walk` | 返回步行距离及所需时间 |
| “骑自行车去 X 地点需要多长时间？” | `scripts/location.sh eta X --mode bike` | 返回骑行距离及所需时间 |
| “开车去 X 地点需要多长时间？” | `scripts/location.sh eta X --mode car` | 返回驾车距离及所需时间 |
| “当我到达 Y 地点时提醒我去做 X 事” | `scripts/location.sh remind "X" Y` | 简短确认提醒 |
| “我有哪些待办事项？” | `scripts/location.sh reminders` | 显示待办事项列表 |
| “列出我常去的地方” | `scripts/location.sh places` | 列出常去的地方 |
| “列出附近的地点” | `scripts/location.sh places --near` | 按距离排序的地点列表 |
| “列出市中心的酒吧” | `scripts/location.sh places --region downtown --category pub` | 过滤后的酒吧列表 |
| “将这个地点保存为 X” | `scripts/location.sh addplace "X"` | 确认保存地点 |
| “删除地点 X” | `scripts/location.sh delplace X` | 确认删除地点 |
| “关闭购物提醒功能” | `scripts/location.sh disable grocery` | 确认关闭功能 |
| “列出我的地理围栏设置” | `scripts/location.sh geofences` | 显示所有地理围栏的详细信息 |
| “我上次去 X 地点是什么时候？” | `scripts/location.sh history X` | 显示上次访问的时间 |
| “我今天去过哪些地方？” | `scripts/location.sh history --days 1` | 显示今天访问过的地点列表 |
| “在附近找一家咖啡馆” | `scripts/location.sh nearby cafe` | 显示附近的咖啡馆列表及距离 |
| “1 公里范围内有酒吧吗？” | `scripts/location.sh nearby pub 1000` | 显示 1 公里范围内的酒吧列表 |
| “我这周在工作上花了多少时间？” | `scripts/location.sh stats --days 7` | 显示每个地点的停留时间 |

**回复方式：** 简洁明了。无需前缀说明，直接给出答案。

## 所有命令

所有命令的格式均为：`scripts/location.sh <命令>`：

| 命令 | 功能描述 |
|---------|-------------|
| `status` | 显示当前位置、已设置的地理围栏及地图链接 |
| `herewego` | 提供 HERE WeGo 地图的链接 |
| `check` | 检查是否有触发的提醒或任务（由 cron 任务使用） |
| `places [--near] [--region R] [--category C]` | 列出保存的地点 |
| `geofences` | 显示所有地理围栏的详细信息 |
| `remind <文本> <地点ID>` | 设置一次性位置提醒 |
| `reminders` | 显示所有待处理的提醒 |
| `addplace <名称> [半径] [--region R] [--category C]` | 保存当前位置信息 |
| `editplace <ID> [--名称] [--半径] [--region] [--类别] [--动作] [--冷却时间]` | 修改地点信息 |
| `delplace <ID>` | 删除指定的地点 |
| `enable <ID>` / `disable <ID>` | 开启/关闭地理围栏功能 |
| `history [地点] [--天数 N]` | 显示上次访问该地点的时间 |
| `nearby <类别> [半径]` | 查找附近的兴趣点（如咖啡馆、酒吧等） |
| `stats [--天数 N]` | 显示在每个地点的停留时间及访问次数 |
| `proximity <文本> <经纬度> [半径>` | 当接近某个地点时发出警报 |
| `eta <地点> [--模式 walk|bike|car]` | 计算前往该地点的旅行时间和距离 |

**注意：** `eta` 命令可以接受保存的地点名称、经纬度坐标，或通过 OpenStreetMap 标准化的地点名称（优先使用用户当前位置附近的地点）。

**补充说明：**  
- `status` 命令会在用户位于已知地点时返回该地点的名称；否则会将该位置反向地理编码为街道地址（例如：“123 Main Street, Downtown”）。  
- 所有命令均通过 `scripts/location.sh <命令>` 来执行。  

## 相关概念  

- **地理围栏（Geofences）**：保存的地点信息，包含经纬度、半径及可选的触发动作（如“进入/离开围栏时触发提醒”）。  
- **提醒（Reminders）**：与特定地点关联的一次性提醒，执行完成后会被删除。  
- **区域/类别（Region/Category）**：用于过滤地点的标签（例如“市中心”或“酒吧”）。  

---

## 设置说明（管理员专用）

### 提供商配置

编辑 `scripts/config.json` 文件：

- **Home Assistant（默认配置）：**  
```json
{
  "provider": "homeassistant",
  "homeassistant": {
    "url": "https://your-ha.example.com",
    "token": "your-long-lived-token",
    "entity_id": "device_tracker.phone"
  }
}
```  
- **OwnTracks：**  
```json
{
  "provider": "owntracks",
  "owntracks": {
    "url": "https://owntracks.example.com",
    "user": "username",
    "device": "phone"
  }
}
```  
- **通用 HTTP 服务：**  
```json
{
  "provider": "http",
  "http": {
    "url": "https://your-api.com/location",
    "headers": {"Authorization": "Bearer token"}
  }
}
```  
- **基于文件的 GPS 日志记录器（GPSLogger）：**  
```json
{
  "provider": "gpslogger",
  "gpslogger": {
    "file": "/path/to/location.json"
  }
}
```  

**注意事项：**  
- 配置信息可以通过环境变量 `env:VAR_NAME` 来设置（例如 `env:LOCATION_PROVIDER`）。  

**替代方案：**  
所有配置也可以完全通过环境变量来完成，无需修改 `config.json` 文件：

| 提供商 | 需要设置的环境变量 |
|---------|-------------------|
| `LOCATION_PROVIDER` | `homeassistant`、`owntracks`、`http` 或 `gpslogger`（默认值：`homeassistant`） |
| **Home Assistant** | `HA_URL`、`HA_TOKEN`、`HA_entity_ID` |
| **OwnTracks** | `OWNTRACKS_URL`、`OWNTRACKS_USER`、`OWNTRACKS_DEVICE`、`OWNTRACKS_TOKEN` |
| **HTTP** | `LOCATION_HTTP_URL` |
| **GPSLogger** | `GPSLOGGER_FILE` |

环境变量的配置优先级高于 `config.json` 文件中的设置。请将相关变量添加到 `~/.openclaw/.env` 文件或 shell 环境中。

**输出格式：**  
大多数查询命令默认输出人类可读的文本；如需 JSON 格式输出，可使用 `--json` 选项（适用于脚本编写）。  

### 行驶速度设置

你可以在 `scripts/config.json` 文件中自定义步行/骑自行车的速度，以便更准确地计算旅行时间（例如：**```json
{
  "speeds_kmh": {
    "walk": 6,
    "bike": 15
  }
}
```**）。  

### 地理围栏配置

编辑 `scripts/geofences.json` 文件以自定义地理围栏的参数。  

### 自动通知（使用 OpenClaw 的 cron 任务）

利用 OpenClaw 内置的 cron 任务定期检查用户位置。将相关任务添加到 `~/.openclaw/cron/jobs.json` 文件中：  
```json
{
  "name": "Location Check",
  "schedule": "*/5 * * * *",
  "prompt": "Run scripts/location.sh check --json and notify me of any triggered actions, reminders, or proximity alerts.",
  "channel": "signal",
  "to": "+1234567890",
  "wakeMode": "now"
}
```  

这种方式可以确保位置检测功能在 OpenClaw 内部自动运行，无需依赖外部系统服务。