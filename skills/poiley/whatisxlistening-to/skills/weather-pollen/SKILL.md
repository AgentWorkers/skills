---
name: weather-pollen
description: 使用免费的API，可以获取任何地点的天气和花粉报告。这些API可以提供当前天气状况、天气预报以及花粉数据。
metadata: {"clawdbot":{"emoji":"🌤️","requires":{"bins":["curl"]}}}
---

# 天气与花粉信息查询技能

使用免费的API获取任意地点的天气和花粉报告。

## 使用方法

当需要查询德克萨斯州安娜市（或配置的地点）的天气或花粉信息时，可以使用此技能中的`weather_report`工具。

## 工具

### weather_report
用于获取指定地点的天气和花粉数据。

**参数：**
- `includePollen` (布尔值，默认值：true) - 是否包含花粉数据
- `location` (字符串，可选) - 要显示的地点名称（坐标通过环境变量配置）

**示例：**
```json
{"includePollen": true, "location": "Anna, TX"}
```

## 配置

通过环境变量设置地点（安娜市，德克萨斯州的默认值）：
- `WEATHER_LAT` - 纬度（默认值：33.3506）
- `WEATHER_LON` - 经度（默认值：-96.3175）
- `WEATHER_LOCATION` - 地点显示名称（默认值：“Anna, TX”）

## 使用的API
- **天气数据：** Open-Meteo（免费，无需API密钥）
- **花粉数据：** Pollen.com（免费，无需API密钥）