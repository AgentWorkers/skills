---
name: yr-weather
description: 使用 yr.no API 从挪威气象研究所（MET）获取天气预报。当用户请求特定地点的天气信息、天气预报、温度、降水量、风况或任何与天气相关的查询时，可以使用此功能。该服务支持基于坐标的查询，能够返回当前天气状况以及未来几天的天气预报。
---
# Yr.no 天气服务

通过免费的 yr.no API 从挪威气象研究所（MET Norway）获取天气预报。

## 概述

该功能使用 MET Norway 的 Locationforecast API 提供天气数据——这是一个提供全球覆盖范围的免费且可靠的天气服务，无需 API 密钥。

**特点：**
- 当前天气状况
- 每小时天气预报（最多 9 天）
- 温度、风速、湿度、降水量
- 带有表情符号的天气图标

## 快速入门

```bash
# Get current weather for Cape Town (default)
python3 {baseDir}/scripts/weather.py

# Get weather for specific coordinates
python3 {baseDir}/scripts/weather.py -33.9288 18.4174

# Get weather with altitude
python3 {baseDir}/scripts/weather.py 59.9139 10.7522 100

# Get tomorrow's forecast
python3 {baseDir}/scripts/tomorrow.py

# Get tomorrow's forecast for specific location
python3 {baseDir}/scripts/tomorrow.py -33.9288 18.4174
```

## API 详情

**端点：** `https://api.met.no/weatherapi/locationforecast/2.0/compact`

**参数：**
- `lat`：纬度（-90 至 90）
- `lon`：经度（-180 至 180）
- `altitude`：海拔高度（米，可选）

**响应：** JSON 数据，包含以下时间序列信息：
- `instant.details.air_temperature`：温度（摄氏度）
- `instant.details.wind_speed`：风速（米/秒）
- `instant.details.relative_humidity`：相对湿度（%）
- `next_1_hours.summary.symbol_code`：天气状况图标代码
- `next_1_hours.details.precipitation_amount`：降水量（毫米）

## 天气图标

| 图标 | 描述 |
|--------|-------------|
| clearsky | 晴朗 |
| fair | 万里无云 |
| partlycloudy | 部分多云 |
| cloudy | 多云 |
| rain | 下雨 |
| lightrain | 小雨 |
| heavyrain | 大雨 |
| rainshowers | 阵雨 |
| sleet | 雨夹雪 |
| snow | 下雪 |
| lightsnow | 小雪 |
| heavysnow | 大雪 |
| snowshowers | 雪阵 |
| fog | 雾 |

某些图标可能有后缀（如 `_day`、`_night`、`_polartwilight`），表示不同的时间时段。

## 常见地点

| 城市 | 纬度 | 经度 |
|------|----------|-----------|
| 开普敦 | -33.9288 | 18.4174 |
| 约翰内斯堡 | -26.2041 | 28.0473 |
| 德班 | -29.8587 | 31.0218 |
| 伦敦 | 51.5074 | -0.1278 |
| 纽约 | 40.7128 | -74.0060 |
| 东京 | 35.6762 | 139.6503 |
| 悉尼 | -33.8688 | 151.2093 |

## 使用须知

**MET Norway 的要求：**
- 必须在请求头中包含用户代理（User-Agent）信息及联系信息
- 对同一地点的天气数据请勿超过 10 分钟内重复请求
- 在显示数据时需标注数据来源为“MET Norway”

本脚本遵守所有使用条款。