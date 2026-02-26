---
name: ncloud-maps
description: "查询 Naver Cloud Maps 的 API 以进行路线导航。默认使用 Directions5 功能；当有 5 个以上的导航点时，系统会自动切换到 Directions15 功能。"
---
## 提示

当用户请求根据地址或坐标进行路线计算时，使用此技能来计算行驶时间、距离和费用。

**使用方法：**
- `/skill ncloud-maps <起点> <终点> [途经点]`
- 起点和终点必须以 `longitude,latitude` 的格式提供，或者直接提供地址（请先使用 `goplaces/naver-local-search` 进行地址转换）
- 返回结果包括：距离、行驶时间、通行费、出租车费用和燃油费用

**示例：**
- `/skill ncloud-maps "126.9633,37.5524" "127.0165,37.4889"` （坐标）
- `/skill ncloud-maps 아현역 서초역` （地址 - 需要先使用地理编码技能）

# Ncloud Maps

该技能通过查询 Naver Cloud Maps 的 API 来提供智能路线规划服务（Directions5 和 Directions15）。

## 主要特性：智能路线规划

**v1.0.8+** — 默认情况下，当途经点少于 5 个时，该技能使用 **Directions5**；当途经点超过 5 个时，会自动切换到 **Directions15**，无需手动选择。

| 途经点数量 | 使用的 API | 最大途经点数量 |
|-----------|----------|---------------|
| 0–4       | Directions5 | 5             |
| 5+        | Directions15 | 15             |

## 设置

1. **从 Naver Cloud 控制台获取 API 凭据：**
   - 在 Naver Cloud 控制台中创建/注册一个应用程序
   - 获取 `Client ID`（API 密钥 ID）和 `Client Secret`（API 密钥）
   - 启用 “Maps Directions15” API

2. **设置环境变量（或使用 `.env` 文件）：**

```bash
export NCLOUD_API_KEY_ID="your-api-key-id"
export NCLOUD_API_KEY="your-api-key-secret"
```

或者创建一个 `.env` 文件：
```
NCLOUD_API_KEY_ID=your-api-key-id
NCLOUD_API_KEY=your-api-key-secret
```

3. **安装依赖项：**

```bash
cd ~/.openclaw/workspace/skills/ncloud-maps
npm install
```

## 使用方法

### 与地址转坐标技能结合使用

`ncloud-maps` 需要 `longitude,latitude` 格式的坐标。如果您有基于地址的位置数据，可以使用以下兼容的技能将地址转换为坐标：

**可选技能（根据您的环境选择）：**

| 技能 | 提供商 | 坐标格式 | 需要的设置 |
|-------|----------|-------------|-----------------|
| `goplaces` | Google Places API | 是（lon, lat） | `GOOGLE_PLACES_API_KEY` |
| `naver-local-search` | Naver Local Search | 是（lon, lat） | `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` |
| 自定义 API | 您选择的 API | 是（lon, lat） | 您的配置 |

**使用 `goplaces` 的示例工作流程：**

```bash
# Get coordinates from address
COORDS=$(goplaces resolve "강남역, 서울" --json | jq -r '.places[0] | "\(.location.longitude),\(.location.latitude)"')

# Use coordinates with ncloud-maps
npx ts-node scripts/index.ts --start "$COORDS" --goal "127.0049,37.4947"
```

**使用 `naver-local-search` 的示例工作流程：**

```bash
# Get coordinates from address
COORDS=$(naver-local-search search "강남역" --format json | jq -r '.[0] | "\(.x),\(.y)"')

# Use coordinates with ncloud-maps
npx ts-node scripts/index.ts --start "$COORDS" --goal "127.0049,37.4947"
```

**或者使用任何其他返回 `longitude,latitude` 坐标的地理编码服务。**

### 智能路线规划（默认行为）

默认情况下，不需要使用 `--api` 标志。该技能会自动：
- 当途经点少于 5 个时，使用 **Directions5**（更快）
- 当途经点超过 5 个时，切换到 **Directions15**（更精确）

请提供 `longitude,latitude` 格式的坐标：

```bash
# 0–4 waypoints → Directions5 (automatic)
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087" \
  --waypoints "127.0100,37.5000|127.0200,37.5100"

# 5+ waypoints → Directions15 (automatic)
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087" \
  --waypoints "127.0100,37.5000|127.0200,37.5100|127.0300,37.5200|127.0400,37.5300|127.0500,37.5400"
```

### 直接根据坐标查询路线

```bash
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087"
```

### 强制使用特定 API（可选）

如果您需要覆盖智能路线规划功能，请使用以下命令：

```bash
# Force Directions5 (max 5 waypoints)
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087" \
  --api directions5 \
  --waypoints "127.0100,37.5000|127.0200,37.5100"

# Force Directions15 (max 15 waypoints)
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087" \
  --api directions15 \
  --waypoints "127.0100,37.5000|127.0200,37.5100|127.0300,37.5200|127.0400,37.5300|127.0500,37.5400"
```

### 使用途经点（仅提供坐标）

```bash
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087" \
  --waypoints "127.0100,37.5000"
```

多个途经点：
```bash
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087" \
  --waypoints "127.0100,37.5000|127.0200,37.5100"
```

### 路线选项

可以选择以下路线类型：`trafast`（快速）、`tracomfort`（舒适）、`traoptimal`（默认）、`traavoidtoll`（免收费路线）、`traavoidcaronly`（避开仅限汽车的道路）

```bash
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087" \
  --option "traavoidtoll"
```

### 车辆和燃油设置

```bash
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087" \
  --cartype 2 \
  --fueltype "diesel" \
  --mileage 10.5
```

车辆类型：
- `1`（默认）：小型轿车
- `2`：中型货车/商务车
- `3`：大型车辆
- `4`：三轴货运卡车
- `5`：四轴以上特殊货运车辆
- `6`：紧凑型汽车

燃油类型：`gasoline`（默认）、`highgradegasoline`、`diesel`、`lpg`

## 输出结果

```json
{
  "success": true,
  "start": "127.0683,37.4979",
  "goal": "126.9034,37.5087",
  "distance": 12850,
  "duration": 1145000,
  "toll_fare": 0,
  "taxi_fare": 18600,
  "fuel_price": 1550,
  "departure_time": "2026-02-21T14:10:00"
}
```

### 返回字段

- `success` - 查询是否成功
- `start` - 起点坐标
- `goal` - 目标坐标
- `distance` - 总距离（米）
- `duration` - 总行驶时间（毫秒，除以 1000 得到秒）
- `toll_fare` - 通行费/高速公路费用（韩元）
- `taxi_fare` - 估计的出租车费用（韩元）
- `fuel_price` - 估计的燃油费用（韩元）
- `departure_time` - 查询时间戳
- `error` - 错误信息（如果查询失败）

## 工作原理

1. **地址解析（可选 - 任何地理编码技能）**
   - 使用可用的地理编码技能获取坐标（如 `goplaces`、`naver-local-search` 等）
   - 从结果中提取 `longitude, latitude` 格式的坐标
   - 将坐标传递给 `ncloud-maps`

2. **坐标验证**
   - 输入的坐标必须为 `longitude, latitude` 格式
   - 验证坐标的格式和范围
   - 如果格式无效，将返回错误信息

3. **路线计算（Directions15 或 Directions5）**
   - 将坐标发送到相应的 Directions API
   - 返回距离、行驶时间、通行费、出租车费用和燃油费用
   - 该服务仅适用于车辆路线（不支持步行或公共交通）

4. **途经点支持**
   - 每个途经点都必须是 `longitude, latitude` 格式
   - 所有坐标都会被发送到 Directions API

## 限制

⚠️ **此技能仅计算车辆（汽车）路线。** 不支持以下类型：
- 公共交通（地铁、公交车等）
- 步行路线
- 多模式出行
- 交通相关的特定功能（费用、站点、时刻表）

对于这些需求，请使用专门的交通服务 API（例如 Kakao Map、Naver Map Transit API）。

## 环境变量

**必需的环境变量：**
- `NCLOUD_API_KEY_ID` - Naver Cloud API 密钥 ID
- `NCLOUD_API_KEY` - Naver Cloud API 密钥 Secret

## API 限制

**智能路线规划：**
- 0–4 个途经点：使用 Directions5 API（最多 5 个途经点）
- 5 个及以上途经点：使用 Directions15 API（最多 15 个途经点）

**其他注意事项：**
- 结果包含实时交通信息
- 请求频率受到您 Naver Cloud 计划的限制

## 错误处理

常见错误：
- `좌표 형식 오류`（坐标格式错误） - 请使用 `longitude, latitude` 格式
- `Authentication Failed`（身份验证失败） - API 凭据无效
- `Quota Exceeded`（超出 API 使用量限制）
- `No routes found`（未找到有效的路线）

请在 Naver Cloud 控制台检查：
- 您的应用程序是否已启用相关 API
- API 使用量限制状态
- 提供的坐标是否有效

## 参考资料

详细 API 规范请参阅 [api-spec.md](references/api-spec.md)。