---
name: openmeteo-weather
description: "获取全球任何城市或坐标点的当前天气信息，以及每小时和每日的天气预报。当用户询问天气情况（如温度、降雨量、降雪量、风速、日出/日落时间、紫外线指数、湿度、气压）或需要了解是否需要带伞时，可以使用此功能。"
metadata: {"openclaw":{"emoji":"🌤","requires":{"bins":["curl","jq"]}}}
user-invocable: true
---

# OpenMeteo 天气服务

通过免费的 Open-Meteo API 获取当前天气和天气预报。无需 API 密钥，支持全球任何地点的查询。

**命令行界面 (CLI):** `bash {baseDir}/scripts/weather.sh [选项]`

## 快速参考

```
# Current weather (city name alone is enough)
bash {baseDir}/scripts/weather.sh --current --city=Berlin
bash {baseDir}/scripts/weather.sh --current --city=London

# Exact coordinates for precision if available
bash {baseDir}/scripts/weather.sh --current --lat=48.8566 --lon=2.3522

# Disambiguate with --country (any format: code, full name, partial)
bash {baseDir}/scripts/weather.sh --current --city=Portland --country=US

# Forecast (daily + hourly)
bash {baseDir}/scripts/weather.sh --forecast-days=3 --city=Paris

# Both current + forecast
bash {baseDir}/scripts/weather.sh --current --forecast-days=2 --city=Rome

# Custom params — fetch only precipitation data
bash {baseDir}/scripts/weather.sh --forecast-days=2 --city=Vienna \
  --hourly-params=precipitation,precipitation_probability,weather_code
```

## 选项

**地点（必选）:**
- `--city=名称` — 城市名称；系统会自动进行地理编码，通常这个参数就足够了。
- `--country=…` — 可选的国家信息，任何格式都可以（例如 `GB`、`France`、`Germany`）。仅用于区分不同的地点（例如区分美国的波特兰和英国的波特兰）。无需查找精确的国家代码，直接输入你知道的名称或省略该参数。
- `--lat=浮点数 --lon=浮点数` — 直接输入经纬度坐标，系统将跳过地理编码步骤。

**模式（至少选择一个）:**
- `--current` — 获取当前天气信息。
- `--forecast` — 获取每小时及每日的天气预报。
- `--forecast-days=N` — 指定预报天数（1–16 天，默认为 7 天；该选项会自动触发 `--forecast` 模式）。

**参数覆盖（用逗号分隔的参数名）:**
- `--current-params=…` — 覆盖当前天气相关的参数。
- `--hourly-params=…` — 覆盖每小时天气相关的参数。
- `--daily-params=…` — 覆盖每日天气相关的参数。

**输出格式:**
- `--human` — 适合人类阅读的格式化输出（默认格式为 `porcelain`，专为自动化系统优化）。

## 规则

1. 默认输出格式为 `porcelain`（简洁格式，适用于自动化系统）。无需额外指定 `--porcelain`，因为这是默认设置。
2. 当用户未指定地点时，从 `USER.md` 文件中获取用户的城市或国家信息。
3. 以自然语言的形式呈现结果，不要直接将 CLI 的原始输出内容提供给用户。
4. WMO 天气代码会自动转换为对应的文本描述（例如 “小雨”、“多云”）。
5. 如果用户仅询问当天或明天的天气，使用 `--forecast-days=1` 或 `--forecast-days=2`；避免不必要的数据请求。
6. 对于特定问题（例如 “雨什么时候会停？”），通过 `--hourly-params` 或 `--daily-params` 来精确获取所需信息。

## 可用的 API 参数

可以通过 `--current-params`、`--hourly-params`、`--daily-params` 来覆盖默认参数值。

### 当前天气和每小时天气参数

- `temperature_2m`（默认）—— 海拔 2 米处的空气温度，单位：°C
- `apparent_temperature`（默认）—— 体感温度，单位：°C
- `relative_humidity_2m`（默认）—— 海拔 2 米处的相对湿度，单位：%
- `precipitation`（默认）—— 总降水量（包括雨、阵雨和雪），单位：mm
- `precipitation_probability`（仅限每小时数据）—— 降水概率，单位：%
- `weather_code`（默认）—— 天气状况，系统会自动转换为文本描述
- `wind_speed_10m`（默认）—— 海拔 10 米处的风速，单位：km/h
- `wind_gusts_10m`—— 海拔 10 米处的阵风速度，单位：km/h
- `wind_direction_10m`—— 风向，单位：°
- `cloud_cover`（仅限当前数据）—— 总云量，单位：%
- `is_day`（仅限当前数据）—— 是否为白天的标志，0/1
- `pressure_msl` — 海平面大气压力，单位：hPa
- `surface_pressure` — 地表压力，单位：hPa
- `visibility` — 能见度，单位：m
- `rain`—— 仅指降雨量（不包括阵雨和雪），单位：mm
- `showers`—— 仅指阵雨量，单位：mm
- `snowfall`—— 降雪量，单位：cm
- `snow_depth`—— 地面上的积雪深度，单位：m
- `dew_point_2m`—— 海拔 2 米处的露点温度，单位：°C
- `uv_index`（仅限每小时数据）—— 紫外线指数

### 每日天气参数

- `temperature_2m_max`（默认）—— 当天最高温度，单位：°C
- `temperature_2m_min`（默认）—— 当天最低温度，单位：°C
- `precipitation_sum`（默认）—— 当天总降水量，单位：mm
- `precipitation_probability_max`（默认）—— 最大降水概率，单位：%
- `weather_code`（默认）—— 当天的主要天气状况
- `wind_speed_10m_max`（默认）—— 最大风速，单位：km/h
- `wind_gusts_10m_max`—— 最大阵风速度，单位：km/h
- `wind_direction_10m_dominant`—— 主导风向，单位：°
- `sunrise`—— 日出时间（ISO 8601 格式）
- `sunset`—— 日落时间（ISO 8601 格式）
- `daylight_duration`—— 白昼时长，单位：秒
- `sunshine_duration`—— 日照时长，单位：秒
- `precipitation_hours`—— 有降水的小时数
- `rain_sum`—— 当天总降雨量，单位：mm
- `showers_sum`—— 当天总阵雨量，单位：mm
- `snowfall_sum`—— 当天总降雪量，单位：cm
- `uv_index_max`—— 最高紫外线指数
- `apparent_temperature_max`—— 当天最高体感温度，单位：°C
- `apparent_temperature_min`—— 当天最低体感温度，单位：°C

## 使用示例

**用户:** “天气怎么样？”
- 如果未指定地点，从 `USER.md` 文件中获取用户的城市或国家信息。
- 如果用户想要了解整体天气情况，使用 `--current`。

**示例输出:** “天气晴朗，温度为 -12°C（体感温度为 -17°C），风速为 9 km/h。”

**用户:** “雨什么时候会停？”
- 如果需要每小时天气更新，使用 `--forecast-days=2` 并仅指定与降雨相关的参数。

**示例输出:** “预计今天 14:00 左右雨会停止。”

**用户:** “我需要带伞吗？”
- 同样需要查看未来几小时的降水情况。

**示例输出:** “在 11:00 到 15:00 之间有 70% 的概率会下雨，预计降水量为 2 毫米，建议带伞。”

**用户:** “这个周末罗马的天气怎么样？”
- 如果用户指定了具体城市和日期，使用 `--forecast` 并指定 `--daily-params`。
- 计算出适合的预报天数，然后从每日预报中提取周六和周日的天气信息。

**示例输出:** “周六：温度 14°C，天气多云；周日：温度 16°C，天气晴朗。”

**用户:** “外面的温度是多少？”
- 如果用户仅想知道温度，使用 `--current` 并指定相关参数。

**示例输出:** “温度为 -5°C，体感温度为 -9°C。”