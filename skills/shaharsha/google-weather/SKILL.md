---
name: google-weather
description: **Google Weather API**  
提供准确、实时的天气数据，包括当前天气状况、温度、湿度、风速以及天气预报。该服务基于 Google 的 Weather API 运行，能够提供每 15 分钟更新一次的、高度精确的本地化天气信息。支持全球任何地点的查询。
version: 1.2.0
author: Leo 🦁
tags: [weather, google, forecast, temperature, real-time, current-conditions, climate, wind, humidity]
metadata: {"clawdbot":{"emoji":"🌤️","requires":{"env":["GOOGLE_API_KEY"]},"primaryEnv":"GOOGLE_API_KEY","secondaryEnv":["GOOGLE_WEATHER_API_KEY","GOOGLE_MAPS_API_KEY"]}}
allowed-tools: [exec]
---

# Google Weather - 实时天气数据

使用 Google 的 Weather API 获取准确的天气信息。需要一个已启用 Weather API 的 Google Cloud API 密钥。

## 快速使用方法

```bash
# Current weather (formatted output)
python3 skills/google-weather/lib/weather_helper.py current "New York"
python3 skills/google-weather/lib/weather_helper.py current "London"
python3 skills/google-weather/lib/weather_helper.py current "Sydney"

# 24h Forecast
python3 skills/google-weather/lib/weather_helper.py forecast "Tel Aviv"

# Raw JSON data
python3 skills/google-weather/lib/weather_helper.py json "Paris"
```

## 示例输出

```
*New York*
Partly Cloudy ⛅
🌡️ 12°C (feels like 10°C)
💨 Wind: 18 km/h NORTHWEST
💧 Humidity: 55%
```

```
*24h Forecast for Tel Aviv*
18:00: 17.8°C, ☀️ 5 km/h NORTH
22:00: 14.3°C, ☀️ 6 km/h EAST_NORTHEAST
02:00: 12.8°C, ⛅ 8 km/h NORTHEAST
06:00: 10.8°C, ☀️ 6 km/h EAST_NORTHEAST
10:00: 16.1°C, ☀️ 5 km/h SOUTH
14:00: 20.4°C, 🌤️ 8 km/h WEST_NORTHWEST
```

## 支持的位置

全球任何地点——只需输入城市名称即可：
- `New York`（纽约），`London`（伦敦），`Paris`（巴黎），`Berlin`（柏林），`Sydney`（悉尼）
- `San Francisco`（旧金山），`Singapore`（新加坡），`Dubai`（迪拜）
- 或任何地址、地标或坐标

该功能会自动使用 Google Maps API 对位置进行地理编码。

## 可用的数据

- **温度**：当前温度及体感温度
- **天气状况**：晴朗、多云、下雨、下雪等，并配有相应的表情符号
- **天气预报**：每小时的温度、风速和天气状况数据
- **湿度**：百分比
- **风**：风速、风向、阵风
- **紫外线指数**：阳光暴露程度
- **降水量**：降水量及类型
- **云量**：百分比
- **能见度**：能见距离

## 设置步骤

1. 在 [Google Cloud Console](https://console.cloud.google.com/) 中创建一个项目。
2. 启用 [Weather API](https://console.cloud.google.com/apis/library/weather.googleapis.com)。
3. 启用 [Geocoding API](https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com)（用于查找地点名称）。
4. 创建一个 API 密钥，并将其设置为 `GOOGLE_API_KEY` 环境变量。

> 如果您已经配置了 API 密钥，也可以使用 `GOOGLE_WEATHER_API_KEY` 或 `GOOGLE_MAPS_API_KEY`。

## 多语言支持

输出内容会根据 `language` 参数自动调整语言，支持英语、希伯来语等多种语言。

```bash
# Hebrew output
python3 skills/google-weather/lib/weather_helper.py current "Tel Aviv"
# Output: בהיר ☀️ 19°C...
```