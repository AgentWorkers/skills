---
name: marine-forecast
description: "通过 Open-Meteo 获取海洋和航行相关的天气信息：包括海浪、涌浪、海水温度、风向、潮汐、海洋 currents（洋流）以及航行评估数据。完全免费，无需 API 密钥，覆盖全球范围。"
homepage: https://open-meteo.com/en/docs/marine-weather-api
metadata: {"clawdbot":{"emoji":"🌊","requires":{"bins":["curl"]}}}
---
# 海洋预报

本系统利用 Open-Meteo Marine API 和 Weather API 提供海洋及航海天气信息。完全免费，无需 API 密钥，支持全球范围内的查询。

系统同时使用了两个 API，请在所有命令中替换 `LAT`、`LON` 和 `TZ` 参数：
- **海洋 API** (`marine-api.open-meteo.com`)：提供海浪高度、海浪周期、海水温度、海流及潮汐信息
- **天气 API** (`api.open-meteo.com`)：提供风速、阵风、气温、气压及能见度数据

您可以通过网络搜索或用户输入来获取任意地点的坐标，并使用最近的时区（遵循 IANA 格式，例如 `Europe/London`、`America/New_York`、`Atlantic/Canary`）。

## 当前天气状况

**海况**：
```bash
curl -s "https://marine-api.open-meteo.com/v1/marine?latitude=LAT&longitude=LON&current=wave_height,wave_direction,wave_period,swell_wave_height,swell_wave_direction,swell_wave_period,sea_surface_temperature&timezone=TZ"
```

**风况及大气状况**：
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&current=temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m,apparent_temperature,pressure_msl,cloud_cover,visibility&timezone=TZ"
```

运行这两个 API 并将结果整合成一份完整的航海天气简报。

## 每小时天气预报

**海洋状况**（可预测未来 16 天，通过调整 `forecast_days` 参数来更改预报时长）：
```bash
curl -s "https://marine-api.open-meteo.com/v1/marine?latitude=LAT&longitude=LON&hourly=wave_height,wave_direction,wave_period,swell_wave_height,swell_wave_direction,swell_wave_period,swell_wave_peak_period,wind_wave_height,wind_wave_direction,sea_surface_temperature,ocean_current_velocity,ocean_current_direction,sea_level_height_msl&forecast_days=3&timezone=TZ"
```

**风况**（可预测未来 16 天）：
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&hourly=wind_speed_10m,wind_direction_10m,wind_gusts_10m,temperature_2m,pressure_msl,visibility,cloud_cover,precipitation_probability&forecast_days=3&timezone=TZ"
```

## 每日天气总结

**海洋状况**：
```bash
curl -s "https://marine-api.open-meteo.com/v1/marine?latitude=LAT&longitude=LON&daily=wave_height_max,wave_direction_dominant,wave_period_max,swell_wave_height_max,swell_wave_direction_dominant,swell_wave_period_max&forecast_days=7&timezone=TZ"
```

**天气状况**：
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&daily=wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_probability_max&forecast_days=7&timezone=TZ"
```

## 潮汐情况

**海平面高度**：
```bash
curl -s "https://marine-api.open-meteo.com/v1/marine?latitude=LAT&longitude=LON&hourly=sea_level_height_msl&forecast_days=3&timezone=TZ"
```

**高潮/低潮**：请在 `sea_level_height_msl` 数组中查找当地的高潮和低潮值。海平面高度包含潮汐影响及气压变化的影响。

## 海流情况
```bash
curl -s "https://marine-api.open-meteo.com/v1/marine?latitude=LAT&longitude=LON&hourly=ocean_current_velocity,ocean_current_direction&forecast_days=3&timezone=TZ"
```

## 结果展示方式

所有海洋数据均以结构化的航海天气简报形式呈现：

### 当前天气状况的展示格式
```
Sea:    [wave_height]m waves, [wave_period]s period, from [direction]
Swell:  [swell_wave_height]m from [direction], [swell_wave_period]s period
Wind:   [wind_speed] km/h [direction], gusts [wind_gusts] km/h
Temp:   Air [temperature]C (feels [apparent_temperature]C), Sea [sea_surface_temperature]C
Sky:    [cloud_cover]% cloud, [visibility/1000]km visibility
```

### 航海天气评估

根据数据对天气状况进行分级：
- **平静**：海浪高度 < 0.5 米，风速 < 12 公里/小时（蒲福风级 0-2）
- **微风**：海浪高度 0.5-1 米，风速 12-19 公里/小时（蒲福风级 3）
- **中等**：海浪高度 1-2 米，风速 20-38 公里/小时（蒲福风级 4-5）
- **大浪**：海浪高度 2-3 米，风速 39-49 公里/小时（蒲福风级 6）
- **狂风**：海浪高度 3-4 米，风速 50-61 公里/小时（蒲福风级 7）
- **危险**：海浪高度 > 4 米或风速 > 62 公里/小时（蒲福风级 8及以上）

**特殊天气警告**：
- **小型船只警告**：阵风风速 > 50 公里/小时或海浪高度 > 3 米
- **大风警告**：持续风速 > 62 公里/小时或海浪高度 > 5 米
- **建议的活动类型**：适合航行、潜水、钓鱼、游泳或冲浪

### 蒲福风级

| 风力等级 | 风速（公里/小时） | 描述 | 海况 |
|---------|-----------------|--------|---------|
| 0       | 0-1            | 平静          | 海面平静     |
| 1       | 2-5            | 微风          | 小浪       |
| 2       | 6-11            | 轻风          | 中等波浪    |
| 3       | 12-19            | 温和微风        | 大波浪     |
| 4       | 20-28            | 中等风          | 中等波浪    |
| 5       | 29-38            | 强风          | 大波浪     |
| 6       | 39-49            | 猛风          | 巨浪       |
| 7       | 50-61            | 飓风          | 巨浪       |
| 8       | 62-74            | 飓风级          | 高浪       |
| 9       | 75-88            | 强飓风          | 非常高的浪   |
| 10      | 89-102            | 风暴          | 极高的浪    |

### 风向转换

将角度转换为罗盘方位：除以 22.5，取整后对应 `[N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW]`。

**快速参考**：0 = N, 45 = NE, 90 = E, 135 = SE, 180 = S, 225 = SW, 270 = W, 315 = NW。

## 单位说明

| 测量参数 | 单位           |
|------------|-----------------|
| 海浪高度   | 米（m）         |
| 海浪周期   | 秒（s）         |
| 风速       | 公里/小时（km/h）     |
| 温度       | 摄氏度（C）       |
| 海流速度   | 公里/小时（km/h）     |
| 方向       | 度（0 = N, 90 = E, 180 = S, 270 = W） |
| 海平面高度 | 相对于平均海平面的高度（m） |
| 能见度     | 米（m）         |
| 气压       | 公斤/平方厘米（hPa）    |

用户可能更习惯使用“节”作为风速单位。转换公式为：`knots = km/h * 0.539957`。在调用天气 API 时添加 `&wind_speed_unit=kn` 可直接获取风速单位为“节”的数据。

## 常见航海目的地参考

| 地区        | 例子         | 纬度（Lat） | 经度（Lon）   |
|------------|-------------|---------|---------|
| 加那利群岛    | 拉斯帕尔马斯     | 28.1      | -15.4      |
| 巴利阿里群岛    | 帕尔马德马略卡     | 39.57      | 2.65      |
| 希腊群岛    | 比雷埃夫斯     | 37.94      | 23.65      |
| 克罗地亚     | 斯普利特      | 43.51      | 16.44      |
| 加勒比海      | 圣马丁       | 18.04      | -63.05      |
| 南太平洋    | 塔希提        | -17.53      | -149.57      |
| 东南亚      | 普吉         | 7.88      | 98.39      |
| 东非        | 桑给巴尔       | -6.16      | 39.19      |
| 澳大利亚      | 悉尼        | -33.87      | 151.21      |
| 美国东海岸    | 安纳波利斯     | 38.97      | -76.49      |
| 英国        | 索伦特       | 50.77      | -1.30      |
| 斯堪的纳维亚    | 哥德堡       | 57.71      | 11.97      |

## 数据来源

- ECMWF WAM（欧洲中期天气预报中心）
- NOAA GFS Wave（全球预报系统）
- DWD GWAM/EWAM（德国气象服务）

**数据精度与更新频率**：
- 数据分辨率：根据地区和模型不同，范围为 5-25 公里
- 更新频率：每天多次
- 预报时长：最长可达 16 天（`forecast_days=16`）

**注意事项**：
- 所有数据以 JSON 格式提供。如支持 `jq`，可使用 `jq` 工具解析数据；否则直接读取原始 JSON 文件。
- 每小时数据返回的数组可能较大。如需快速查看，可使用 `current` 参数；如需详细规划信息，建议使用 `daily` 参数；仅在需要详细分析时使用 `hourly` 参数。
- 需结合海洋 API 和天气 API 的数据才能获得完整的航海天气信息。单独使用任一 API 都无法提供全面的预报。
- 海平面高度数据为近似潮汐值，未明确标注高潮/低潮的具体时间；实际潮汐情况需根据每小时数据中的最高/最低值计算得出。
- 对于沿海地区，数据精度受距离最近网格点的距离影响；开阔海域的数据精度较高，而港口和海湾地区的数据可能稍有偏差。

更多文档请参阅：https://open-meteo.com/en/docs/marine-weather-api