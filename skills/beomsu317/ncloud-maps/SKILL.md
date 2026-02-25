---
name: ncloud-maps
description: "查询 Naver Cloud Maps 的 API 以进行路线导航。默认使用 Directions5 功能；当需要规划 5 个以上的路线点时，系统会自动切换到 Directions15 功能。"
---
# Ncloud Maps

该技能用于查询Naver Cloud Maps API，以获取智能路由信息（Directions5和Directions15两种方式）。

## 主要功能：智能路由

**v1.0.6+** — 默认情况下，当路径点少于5个时，该技能使用Directions5；当路径点达到或超过5个时，会自动切换到Directions15。无需手动选择。

| 路径点数量 | 使用的API | 最大路径点数量 |
|-----------|----------|---------------|
| 0–4       | Directions5 | 5 |
| 5+        | Directions15 | 15 |

## 设置

1. **从Naver Cloud控制台获取API凭证：**
   - 在Naver Cloud控制台中创建/注册一个应用程序
   - 获取`Client ID`（API密钥ID）和`Client Secret`（API密钥）
   - 启用“Maps Directions15”API

2. **设置环境变量（或使用.env文件）：**

```bash
export NCLOUD_API_KEY_ID="your-api-key-id"
export NCLOUD_API_KEY="your-api-key-secret"
```

或者创建一个.env文件：
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

### 与“地址转坐标”技能配合使用

ncloud-maps需要`longitude, latitude`格式的坐标。如果您有基于地址的位置数据，可以使用以下兼容的技能将地址转换为坐标：

**可选技能（根据您的环境选择）：**

| 技能 | 提供者 | 坐标格式 | 需要的设置 |
|-------|----------|-------------|-----------------|
| `goplaces` | Google Places API | 是 (lon, lat) | `GOOGLE_PLACES_API_KEY` |
| `naver-local-search` | Naver Local Search | 是 (lon, lat) | `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` |
| 自定义API | 您选择的API | 是 (lon, lat) | 您的配置 |

**使用goplaces的示例工作流程：**

```bash
# Get coordinates from address
COORDS=$(goplaces resolve "강남역, 서울" --json | jq -r '.places[0] | "\(.location.longitude),\(.location.latitude)"')

# Use coordinates with ncloud-maps
npx ts-node scripts/index.ts --start "$COORDS" --goal "127.0049,37.4947"
```

**使用naver-local-search的示例工作流程：**

```bash
# Get coordinates from address
COORDS=$(naver-local-search search "강남역" --format json | jq -r '.[0] | "\(.x),\(.y)"')

# Use coordinates with ncloud-maps
npx ts-node scripts/index.ts --start "$COORDS" --goal "127.0049,37.4947"
```

**或者使用任何返回`longitude, latitude`坐标的地理编码服务。**

### 智能路由（默认行为）

默认情况下，无需使用`--api`参数。该技能会自动：
- 对于0–4个路径点，使用Directions5（速度更快）
- 对于5个或更多路径点，切换到Directions15（更准确）

提供`longitude, latitude`格式的坐标：

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

### 基本路线查询（按坐标）

```bash
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087"
```

### 强制使用特定API（可选）

如果您需要覆盖智能路由设置：

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

### 输入路径点（仅提供坐标）

```bash
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087" \
  --waypoints "127.0100,37.5000"
```

**多个路径点：**

```bash
npx ts-node scripts/index.ts \
  --start "127.0683,37.4979" \
  --goal "126.9034,37.5087" \
  --waypoints "127.0100,37.5000|127.0200,37.5100"
```

### 路线选项**

可以选择以下路线类型：`trafast`（快速）、`tracomfort`（舒适）、`traoptimal`（默认）、`traavoidtoll`（免收费）、`traavoidcaronly`（避开仅限汽车的道路）

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
- `2`：中型厢式货车/货运车
- `3`：大型车辆
- `4`：三轴货运卡车
- `5`：四轴以上特殊货运车
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

### 响应字段

- `success` - 查询是否成功
- `start` - 起点坐标
- `goal` - 目标坐标
- `distance` - 总距离（米）
- `duration` - 总耗时（毫秒，除以1000转换为秒）
- `toll_fare` - 收费/高速公路费用（韩元）
- `taxi_fare` - 估计的出租车费用（韩元）
- `fuel_price` - 估计的燃油费用（韩元）
- `departure_time` - 查询时间戳
- `error` - 错误信息（如果查询失败）

## 工作原理

1. **地址解析（可选 - 任何地理编码技能）**
   - 使用可用的提供坐标的技能（如goplaces、naver-local-search等）
   - 从结果中提取`longitude, latitude`格式的坐标
   - 将坐标传递给ncloud-maps

2. **坐标验证**
   - 输入格式应为`longitude, latitude`
   - 验证坐标格式是否有效
   - 如果格式无效，将返回错误

3. **路线计算（Directions15或Directions5）**
   - 将坐标发送到相应的Directions API
   - 返回距离、耗时、费用、出租车费用和燃油费用
   - **仅适用于车辆路线**（不适用于步行或公共交通）

4. **路径点支持**
   - 每个路径点必须为`longitude, latitude`格式
   - 所有坐标都会被发送到Directions API

## 限制

⚠️ **该技能仅计算车辆（汽车）路线。** 不支持以下类型：
- 公共交通（地铁、公交车等）
- 步行路线
- 多模式出行
- 交通相关的特定功能（费用、站点、时刻表）

对于这些场景，请使用专门的交通API（例如Kakao Map、Naver Map Transit API）。

## 环境变量

**必需的变量：**
- `NCLOUD_API_KEY_ID` - Naver Cloud API密钥ID
- `NCLOUD_API_KEY` - Naver Cloud API密钥

## API限制

**智能路由：**
- 0–4个路径点：使用Directions5 API（最多5个路径点）
- 5个或更多路径点：使用Directions15 API（最多15个路径点）

**其他注意事项：**
- 结果包含实时交通信息
- 请求频率受您的Naver Cloud套餐限制

## 错误处理

常见错误：
- `좌표 형식 오류`（坐标格式无效，应使用`longitude, latitude`）
- `Authentication Failed`（身份验证失败）
- `Quota Exceeded`（超出API请求限制）
- `No routes found`（两点之间没有有效路线）

请在Naver Cloud控制台检查：
- 您的应用程序是否已启用相关API
- API的配额/请求限制状态
- 提供的坐标是否有效

## 参考资料

详细API规范请参阅[api-spec.md](references/api-spec.md)。