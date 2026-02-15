---
name: openmeteo-sh-weather-advanced
description: "来自免费 OpenMeteo API 的高级天气服务：提供历史数据、详细的变量选择功能、多种天气模型选项、过去几天的天气信息以及深入的天气预报。当用户需要查询历史天气数据、特定的天气模型、一些特殊气象变量（如气压、露点、积雪深度等），或者希望获得超出简单当前/未来天气查询范围的详细信息时，可以使用该服务。"
metadata: {"openclaw":{"emoji":"🌦","requires":{"bins":["openmeteo"]}}}
homepage: https://github.com/lstpsche/openmeteo-sh
user-invocable: true
---

# OpenMeteo Weather — 高级版 (openmeteo-sh)

通过 `openmeteo` 命令行界面 (CLI) 进行高级天气查询：可获取历史数据（自 1940 年起）、详细选择天气变量、选择不同的天气模型，并对天气预报进行精细控制。无需 API 密钥。

**CLI 使用格式：**  
`openmeteo <命令> [选项]`

## 输出格式  
始终使用 `--llm` 选项，以生成适用于大型语言模型 (LLMs) 的紧凑型 TSV（制表符分隔的文本）输出。天气代码会自动转换为人类可读的文本格式。只有在用户明确要求 JSON 格式时，才使用 `--raw` 选项。

## 快速参考  
```
# Current weather
openmeteo weather --current --city=Berlin --llm

# Current + 2-day forecast
openmeteo weather --current --forecast-days=2 --city=London --llm

# Only precipitation data
openmeteo weather --forecast-days=2 --city=Vienna \
  --hourly-params=precipitation,precipitation_probability,weather_code --llm

# Coordinates instead of city
openmeteo weather --current --lat=48.8566 --lon=2.3522 --llm

# Disambiguate city with country
openmeteo weather --current --city=Portland --country=US --llm

# Forecast starting from day 3 (skip today and tomorrow)
openmeteo weather --forecast-days=7 --forecast-since=3 --city=London --llm

# Historical weather
openmeteo history --city=Paris --start-date=2024-01-01 --end-date=2024-01-31 --llm
```

## 位置设置（必须选择一项）  
- `--city=城市名称` — 输入城市名称，系统会自动进行地理编码；通常单独使用即可。  
- `--country=国家代码` — 可选的国家代码，用于消除歧义（例如：US、GB）。仅在城市名称不明确时使用。输入实际的国家代码或省略该选项。  
- `--lat=纬度值 --lon=经度值` — 直接输入 WGS84 坐标，系统将跳过地理编码步骤。

## 命令说明  

### `weather` 命令：查询未来 16 天内的天气情况及当前天气状况  
**至少需要指定一个模式：**  
- `--current` — 获取当前天气状况。  
- `--forecast-days=天数` — 查询的天数（0–16 天，默认为 7 天）。  
- `--forecast-since=天数` — 指定查询的起始日期（1 表示今天，2 表示明天等）。服务器会自动调整查询范围，确保结果在指定范围内。  

**参数覆盖（用逗号分隔的参数名称）：**  
- `--current-params=参数列表` — 覆盖当前天气数据的参数设置。  
- `--hourly-params=参数列表` — 覆盖每小时天气数据的参数设置。  
- `--daily-params=参数列表` — 覆盖每日天气数据的参数设置。  

**单位设置：**  
- `--temperature-unit=单位` — 温度单位（摄氏度或华氏度，默认为摄氏度）。  
- `--wind-speed-unit=单位` — 风速单位（公里/小时、米/秒、英里/小时、节，默认为公里/小时）。  
- `--precipitation-unit=单位` — 降水量单位（毫米或英寸，默认为毫米）。  

**其他选项：**  
- `--past-days=天数` — 包含过去的天数（0–92 天，默认为 0 天）。  
- `--timezone=时区` — IANA 时区代码或自动识别时区（默认为自动识别）。  
- `--model=模型` — 选择的天气模型（默认为最适合当前数据的模型）。  

### `history` 命令：查询 1940 年以来的历史天气数据  
需要指定 `--start-date=开始日期` 和 `--end-date=结束日期`。支持 `--hourly-params`、`--daily-params` 和 `--model` 选项（可选的天气模型）。  

## 常用天气变量  
可以通过 `--current-params`、`--hourly-params` 和 `--daily-params` 来覆盖默认值。如需查看所有变量及其描述，运行：  
`openmeteo weather help --daily-params`（或 `--hourly-params`、`--current-params`）。  

### 常用变量示例（当前/每小时数据）  
- `temperature_2m` — 海拔 2 米处的气温（摄氏度）。  
- `apparent_temperature` — 体感温度（摄氏度）。  
- `relative_humidity_2m` — 相对湿度（百分比）。  
- `precipitation` — 总降水量（雨、阵雨、雪的总量，单位为毫米）。  
- `precipitation_probability`（仅适用于每小时数据） — 降水量概率（百分比）。  
- `weather_code` — 天气状况代码，会自动转换为人类可读的文本（例如：“小雨”）。  
- `wind_speed_10m` — 海拔 10 米处的风速（公里/小时）。  
- `wind_gusts_10m` — 海拔 10 米处的阵风速度（公里/小时）。  
- `cloud_cover` — 总云量（百分比）。  
- `is_day`（仅适用于当前数据） — 是否为白天的标志（0/1）。  
- `uv_index`（仅适用于每小时数据） — 紫外线指数。  
- `snowfall` — 降雪量（厘米）。  
- `visibility` — 能见度（米）。  
- `pressure_msl` — 海平面气压（百帕）。  

### 日常数据（常用变量）  
- `temperature_2m_max` / `temperature_2m_min` — 当天的最高/最低气温（摄氏度）。  
- `precipitation_sum` — 当天的总降水量（毫米）。  
- `precipitation_probability_max` — 当天的最大降水量概率（百分比）。  
- `weather_code` — 当天的主要天气状况。  
- `wind_speed_10m_max` — 当天的最大风速（公里/小时）。  
- `sunrise` / `sunset` — 当天的日出/日落时间（ISO 8601 格式）。  
- `uv_index_max` — 当天的最大紫外线指数。  
- `snowfall_sum` — 当天的总降雪量（厘米）。  
- `apparent_temperature_max` / `apparent_temperature_min` — 当天的最高/最低体感温度（摄氏度）。  

## 详细变量查询  
运行 `openmeteo weather help <参数>` 可查看所有可用变量及其描述：  
```
openmeteo weather help --daily-params
openmeteo weather help --hourly-params
openmeteo weather help --current-params
openmeteo history help --daily-params
```  
若需紧凑型 TSV 输出格式，添加 `--llm` 选项：  
`openmeteo weather help --daily-params --llm`  

当需要查询上述常用变量之外的其他特定变量时，请使用此命令。  

## 使用规则：  
1. 始终使用 `--llm` 输出格式，该格式对语言模型最为高效。  
2. 如果用户未指定位置，请从 `USER.md` 文件中获取用户所在的城市或国家信息。  
3. 以自然语言的形式呈现查询结果，切勿直接将原始 CLI 输出内容提供给用户。  
4. 对于仅询问当前或明天天气的情况，使用 `--forecast-days=1` 或 `--forecast-days=2`；避免不必要的数据查询。  
5. 对于具体日期的天气查询（例如：“雨什么时候会停？”），通过 `--hourly-params` 或 `--daily-params` 来筛选所需数据，并根据分析结果给出答案。  
6. 当用户询问特定日期的天气时（例如：“周五的天气如何？”），使用 `--forecast-since=日期` 来避免获取不需要的早期数据。  
7. 当用户更换查询城市时（例如：“伦敦的天气如何？”），请保留之前查询中使用的所有参数；新城市的参数设置应包含之前所有请求的参数。  

## 对话示例：  
**用户：“天气怎么样？”**  
- 未指定位置 → 从 `USER.md` 文件中获取用户所在城市或国家信息。  
- 获取总体天气概况 → 使用 `--current` 命令。  
**用户：“雨什么时候会停？”**  
  使用 `--hourly-params` 来获取每小时降水量数据，并根据结果回答。  
**用户：“我需要带伞吗？”**  
  根据降水量概率（70%）判断是否需要带伞。  
**用户：“罗马这个周末的天气如何？”**  
  使用 `--forecast-since=周六` 和 `--forecast-days=2` 来查询周末的天气。  
**用户：“外面的温度是多少？”**  
  仅查询温度时，使用相应的参数。  
**用户：“去年六月东京的降水量是多少？”**  
  查询总降水量及具体降雪量。