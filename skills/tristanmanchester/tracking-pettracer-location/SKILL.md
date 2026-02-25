---
name: tracking-pettracer-location
description: 通过 PetTracer 门户 API 追踪 PetTracer (pettracer.com) 提供的 GPS 吊坠：可以获取宠物的最新位置、位置历史记录，并可选地通过 PetTracer 的 WebSocket (SockJS/STOMP) 协议实时推送更新信息。适用于用户询问“我的宠物/猫在哪里？”、“追踪我的 PetTracer 宠物”的场景，或者需要获取宠物的 GPS 坐标/位置历史记录，以及需要帮助处理 PetTracer 的认证令牌或实时追踪功能的情况。
  Tracks PetTracer (pettracer.com) GPS collars via the PetTracer portal API: fetches a pet’s latest location,
  location history, and optionally streams updates via the PetTracer WebSocket (SockJS/STOMP).
  Use when the user asks “where is my pet/cat”, “track my PetTracer”, wants GPS coordinates/history,
  or needs help with PetTracer authentication tokens or live tracking.
---
# 追踪 PetTracer 宠物的位置

## 该功能的用途

PetTracer 提供了一个（非官方的）Web 端口 API，供其应用程序或网站使用。该功能提供了可靠且操作简单的工作流程，用于获取以下信息：
- **当前位置**（最新的已知位置）
- **最近的活动路线/历史记录**（按时间窗口划分的位置点）
- **近乎实时的更新**（通过 WebSocket 推送，可选）

该功能旨在减少对 API 的负载，并生成 **一致且易于复制/粘贴的输出结果**。

## 快速入门

### 获取宠物位置快照（推荐默认方式）
1. 设置凭据（建议使用环境变量，而非命令行参数）：
```bash
export PETTRACER_USERNAME="you@example.com"
export PETTRACER_PASSWORD="••••••••"
```

2. 列出所有宠物设备：
```bash
python scripts/pettracer_cli.py list --format json --pretty
```

3. 定位宠物：
- 通过名称：
```bash
python scripts/pettracer_cli.py locate --pet "Fluffy" --format json --pretty
```

- 通过 ID：
```bash
python scripts/pettracer_cli.py locate --device-id 12345 --format json --pretty
```

- 如果账户仅关联了一个宠物项圈，可以省略 `--pet/--device-id` 参数：
```bash
python scripts/pettracer_cli.py locate --format json --pretty
```

### 获取宠物位置历史记录（过去 6 小时）
```bash
python scripts/pettracer_cli.py history --pet "Fluffy" --hours 6 --format json --pretty
```

## 代理应遵循的核心工作流程

### 1) 确定所需的数据类型：快照、历史记录还是实时更新
- **快照**：用户询问“X 现在在哪里？” → 使用 `locate` 命令。
- **历史记录**：用户询问“X 今天/过去一小时在哪里活动？” → 使用 `history` 命令。
- **实时更新**：用户需要持续的位置更新 → 使用 WebSocket（详见 [references/websocket.md](references/websocket.md)）。

默认情况下使用 **快照**，除非用户明确要求获取路线或实时跟踪信息。

### 2) 安全认证
推荐的认证顺序：
1. 如果已有 `PETTRACER_TOKEN`，请使用该令牌进行认证。
2. 否则，使用 `PETTRACER_USERNAME` 和 `PETTRACER_PASSWORD`（或 `PETTRACER_EMAIL`）进行登录。

**切勿** 要求用户在聊天框中输入令牌。建议用户将令牌设置到环境变量中或存储在安全的地方。

可选的配置项（有助于调试或未来扩展）：
- `PETTRACER_API_BASE`（REST API 的基础地址；默认为 `https://portal.pettracer.com/api`）
- `PETTRACER_WS_BASE`（WebSocket 的基础地址；默认为 `wss://pt.pettracer.com/sc`）

### 3) 确定正确的宠物设备
- 通过 `GET /api/map/getccs` 获取设备列表（该请求由 `pettracer_cli.py list` 函数处理）。
- 根据 `details.name` 进行不区分大小写的匹配。
- 如果有多个匹配项，显示一个列表（包含设备 ID 和名称），让用户选择目标设备。
- 如果没有匹配项，显示所有可用的设备名称。
- 如果账户仅关联了一个宠物项圈，系统会自动选择该设备。

### 4) 获取位置数据
- **当前位置** 可以从 `device.lastPos`（宠物项圈提供的数据）或顶级 `posLat/posLong`（来自 HomeStations 的数据）获取：
  - `posLat`、`posLong`
  - `timeMeasure`（时间戳）
  - `acc`（精度，单位为米）或 `horiPrec`（备用精度）
- **历史记录** 通过 `POST /api/map/getccpositions` 获取，需要提供以下参数：
  - `devId`、`filterTime`（毫秒）、`toTime`（毫秒）

详细信息请参阅 [references/endpoints.md](references/endpoints.md) 和 [references/data-model.md]。

### 5) 一致地展示结果
在展示位置信息时，应包括以下内容：
- 宠物名称 + 设备 ID
- 坐标（纬度、经度）
- 最后一次更新的时间
- 精度（如有）
- 数据更新的时长（自上次更新以来的秒数/分钟）
- 可选：地图链接（例如 Google Maps 或 OpenStreetMap）

**推荐的 JSON 数据格式（便于不同工具之间的数据交换）：**
```json
{
  "pet": { "id": 12345, "name": "Fluffy" },
  "last_fix": {
    "lat": 48.137154,
    "lon": 11.576124,
    "time": "2026-02-25T12:34:56+00:00",
    "accuracy_m": 12
  },
  "last_fix_age_s": 90,
  "battery_mv": 4012,
  "battery_percent_est": 78,
  "home": false,
  "links": {
    "google_maps": "https://www.google.com/maps?q=48.137154,11.576124",
    "openstreetmap": "https://www.openstreetmap.org/?mlat=48.137154&mlon=11.576124#map=18/48.137154/11.576124"
  }
}
```

**注意事项：**
- `battery_percent_est` 是根据电压估算的电池电量百分比（PetTracer 报告的是毫伏值，而非百分比）。
- 如果没有 GPS 数据，应返回 `error=no_recent_fix` 并显示 `lastContact`（最后一次定位的时间）。

## 实时跟踪（可选，避免频繁轮询）

如果需要频繁获取位置信息：
- 建议使用 WebSocket 推送方式（避免频繁的轮询操作）。
- 仅在 WebSocket 不可用时才使用轮询方式；默认情况下，轮询间隔应大于 60 秒。

**安装依赖项：**
```bash
pip install aiohttp
```

**然后运行相关命令：**
```bash
python scripts/pettracer_watch.py --pet "Fluffy"
```

**参考资料：**
- [references/websocket.md](references/websocket.md)（WebSocket 相关文档）
- `scripts/pettracer_watch.py`（包含 SockJS/STOMP 协议的实现示例）

## 故障排除指南

### 无法获取位置信息或 `lastPos` 为空
常见原因：
- 宠物项圈最近没有发送 GPS 数据（可能位于室内或信号较弱）
- 电池电量低或宠物项圈未开启
- 订阅服务已过期

**处理方法：**
- 显示“最近没有定位数据”并显示 `lastContact`（如果有的话）。
- 如果用户请求，建议在 PetTracer 应用程序或网站中切换到更高频率的跟踪模式（如 Fast/Live 模式）（详见 [references/modes.md](references/modes.md)）。

### 认证失败（401/invalid_auth）
- 重新登录以获取新的 `access_token`。
- 确保登录请求中使用了 `login` 和 `password` 参数（而非 `username`）。

### 遵守服务使用限制
- 避免频繁调用 `/map/getccs` 接口。
- 对于近乎实时的位置跟踪，优先使用 WebSocket。

## 完整的位置响应格式

当用户需要人类可读的格式化输出时，请使用以下格式：
```
Give the pet’s latest known PetTracer location.

Include:
- Pet name + device id
- Time of last fix (and last contact if different)
- Coordinates + map link(s)
- Accuracy (metres) if present
- One-line assessment: “recent fix” vs “stale fix” (use last_fix_age_s if available; interpret in the context of the current tracking mode)
```