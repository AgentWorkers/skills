---
name: open-meteo
description: "通过 Open-Meteo API 获取天气预报（免费，无需 API 密钥）。适用场景：当用户询问天气、温度、降雨概率、紫外线指数、风速或任何地点的天气预报时。该服务提供当前天气状况、每小时天气预报以及未来 7 天的每日天气预报（包括降水概率、体感温度、紫外线指数、日出/日落时间）。同时还会生成用于每日天气摘要的 Weather Strip SVG 小部件。这是默认的天气查询技能，可替代 wttr.in。"
---
# Open-Meteo 天气服务

这是一个免费的天气API，无需API密钥，返回JSON格式的数据。

## 脚本

### weather.sh — 原始JSON天气预报数据

```
scripts/weather.sh <latitude> <longitude> [current|hourly|daily] [days] [units]
```

- `days`: 1-16（默认值3）
- `units`: `华氏度`（默认）或 `摄氏度`
- `current` 模式同时返回当前天气情况和每日预报

```bash
scripts/weather.sh 37.75 -122.43 current 3 fahrenheit
scripts/weather.sh 37.75 -122.43 hourly 2 fahrenheit
scripts/weather.sh 37.75 -122.43 daily 7 fahrenheit
```

### weather_strip.py — SVG天气条插件

该插件生成一个交互式的SVG天气可视化界面，具有以下功能：
- 温度和露点的平滑贝塞尔曲线显示
- 云量图（半透明，0-100%）
- 降雨量条形图（浅蓝色，0-2英寸/小时，当降雨概率超过50%时显示）
- 雨量概率线叠加显示
- UV指数条形图（UV值超过3时显示黄色/橙色/红色）
- 天空渐变背景（白天为天蓝色，夜晚为深蓝色，日出/日落过渡平滑）
- 日落时显示月相图标
- 固定的滚动条，可滚动查看所有天气指标
- 支持多城市，并可设置时间范围
- 温度刻度固定为0-110华氏度
- 每小时显示7天的每日天气预报

```bash
# Single location
python3 scripts/weather_strip.py --lat 37.75 --lon -122.43 --days 7 \
  > /Users/dapkus/openclaw-apps/digest-app/static/weather-strip.html

# Standalone preview page
python3 scripts/weather_strip.py --lat 37.75 --lon -122.43 --days 7 \
  --output /Users/dapkus/openclaw-apps/digest-app/static/weather-strip-preview.html

# Multi-city with time ranges (for travel)
python3 scripts/weather_strip.py --schedule '[
  {"name":"SF","lat":37.75,"lon":-122.43,"ranges":[
    ["2026-03-01T00:00","2026-03-02T08:00"],
    ["2026-03-06T15:00","2026-03-07T23:00"]
  ]},
  {"name":"Palm Springs","lat":33.83,"lon":-116.55,"ranges":[
    ["2026-03-02T10:00","2026-03-06T13:00"]
  ]}
]' --days 7 > /Users/dapkus/openclaw-apps/digest-app/static/weather-strip.html
```

**调度格式：** 每个地点包含 `name`、`lat`、`lon`，以及以下信息之一：
- `ranges`: `["start_iso", "end_iso"]` 对列表（按小时精确，跳过过渡时间）
- `dates`: `"YYYY-MM-DD"` 字符串列表（表示整天的天气数据）

**输出方式：** 
- 不使用 `--output` 选项时，将生成的天气数据打印到标准输出（stdout）。
- 使用 `--output` 选项时，会生成一个独立的HTML页面。

### Digest集成

Digest应用程序会读取 `static/weather-strip.html` 文件，并将其显示在每个摘要页面的顶部。

**每日更新：** 
- 在生成晨间摘要时，会重新生成天气条数据（`static/weather-strip.html`）。
- 如果有旅行计划，可以使用 `--schedule` 选项设置时间范围。
- 默认情况下，显示旧金山的天气信息。

## 常用坐标

| 地点 | 纬度 | 经度 |
|---|---|---|
| 旧金山 | 37.75 | -122.43 |
| 纽约 | 40.71 | -74.01 |
| 洛杉矶 | 34.05 | -118.24 |
| 伦敦 | 51.51 | -0.13 |
| 棕榈泉 | 33.83 | -116.55 |

其他城市的坐标信息请参见 ```bash
curl -sf "https://geocoding-api.open-meteo.com/v1/search?name=CityName&count=1" | jq '.results[0] | {name, latitude, longitude}'
```。

## WMO天气代码

| 代码 | 含义 |
|---|---|
| 0 | 晴朗 |
| 1-3 | 大部分晴朗 / 部分多云 / 阴天 |
| 45, 48 | 雾 / 结霜雾 |
| 51-55 | 小雨 / 中等雨 / 大雨 |
| 61-65 | 小雨 / 中等雨 / 大雨 |
| 71-75 | 小雪 / 中等雪 / 大雪 |
| 80-82 | 雨阵 / 中等雨 / 暴雨 |
| 95, 96, 99 | 雷暴 / 伴有冰雹 |

## 结果解读方法：

- 使用 `jq` 工具解析JSON数据。
- `precipitation_probability_max` 可以用来判断是否会有降雨。
- `apparent_temperature` 表示体感温度（风寒指数 + 湿度）。
- 当 `uv_index_max` 大于6时，建议涂抹防晒霜。
- 时间以所在地点的当地时间显示（自动检测）。

## 呈现方式：

以通俗易懂的方式总结天气信息，重点突出温度、降雨概率以及任何异常天气情况。不要直接输出原始的JSON数据。