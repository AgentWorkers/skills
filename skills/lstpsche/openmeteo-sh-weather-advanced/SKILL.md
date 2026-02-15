---
name: openmeteo-sh-weather-advanced
description: "来自免费 OpenMeteo API 的高级天气服务：提供历史数据、详细的变量选择功能、多种天气模型选项、过去几天的天气信息以及深入的天气预报。当用户需要查询历史天气数据、特定的天气模型、某些专业性较强的天气变量（如气压、露点、积雪深度等），或者希望获得超出简单当前/未来天气查询范围的详细信息时，可以使用该服务。"
metadata: {"openclaw":{"emoji":"🌦","requires":{"bins":["openmeteo"]}}}
homepage: https://github.com/lstpsche/openmeteo-sh
user-invocable: true
---

# OpenMeteo Weather — 高级版 (openmeteo-sh)

通过 `openmeteo` 命令行界面 (CLI) 进行高级天气查询：可获取历史数据（自 1940 年起）、详细选择天气变量、选择不同的天气模型，并能精细控制预报内容。无需 API 密钥。

**CLI 使用格式：**  
`openmeteo <命令> [选项]`

## 输出格式  
始终使用 `--llm` 选项，以生成适合大型语言模型 (LLMs) 的紧凑型 TSV 格式输出。天气代码会自动转换为文本格式。只有在用户明确要求 JSON 格式时，才使用 `--raw` 选项。

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

## 位置选择（必填）  
- `--city=城市名称` — 输入城市名称，系统会自动进行地理编码；通常单独使用此选项即可。  
- `--country=国家代码` — 可选的国家代码，用于消除歧义（例如：US、GB）。仅在城市名称不明确时使用。输入实际的国家代码或省略该选项。  
- `--lat=纬度值 --lon=经度值` — 直接输入 WGS84 坐标，系统将跳过地理编码步骤。

## 命令说明  
### `weather` — 提供未来 16 天的天气预报及当前天气状况  
**至少需要指定一个模式：**  
- `--current` — 获取当前天气状况。  
- `--forecast-days=天数` — 指定预报天数（0–16 天，默认为 7 天）。  
- `--forecast-since=天数` — 指定预报的起始日期（1 表示今天，2 表示明天等）。服务器端会自动调整时间范围，确保 `forecast-days` 的值在有效范围内。  

**参数覆盖（用逗号分隔的参数名称）：**  
- `--current-params=参数列表` — 覆盖当前天气的参数设置。  
- `--hourly-params=参数列表` — 覆盖每小时天气的参数设置。  
- `--daily-params=参数列表` — 覆盖每日天气的参数设置。  

**单位设置：**  
- `--temperature-unit=单位` — 温度单位（摄氏度/华氏度，默认为摄氏度）。  
- `--wind-speed-unit=单位` — 风速单位（公里/小时/米/秒/节，默认为公里/小时）。  
- `--precipitation-unit=单位` — 降水量单位（毫米/英寸，默认为毫米）。  

**其他选项：**  
- `--past-days=天数` — 包含过去的天数（0–92 天，默认为 0 天）。  
- `--timezone=时区` — IANA 时区代码或自动识别时区（默认为自动识别）。  
- `--model=模型` — 选择的天气模型（默认为最佳匹配模型）。  

### `history` — 提供自 1940 年以来的历史天气数据  
需要指定 `--start-date=开始日期` 和 `--end-date=结束日期`。支持 `--hourly-params`、`--daily-params` 和 `--model` 参数（如 era5、era5_land、cerra、ecmwf_ifs 等）。  

## 常见天气变量  
可以通过 `--current-params`、`--hourly-params`、`--daily-params` 覆盖默认值。如需查看所有变量及其描述，可运行：  
`openmeteo weather help --daily-params`（或 `--hourly-params`、`--current-params`）。  

### 常用变量  
- `temperature_2m` — 海拔 2 米处的气温（摄氏度）。  
- `apparent_temperature` — 体感温度（摄氏度）。  
- `relative_humidity_2m` — 相对湿度（百分比）。  
- `precipitation` — 总降水量（雨/阵雨/雪，单位：毫米）。  
- `precipitation_probability`（仅适用于每小时数据） — 降水概率（百分比）。  
- `weather_code` — 天气状况代码，系统会自动转换为文本（例如：“小雨”）。  
- `wind_speed_10m` — 海拔 10 米处的风速（公里/小时）。  
- `wind_gusts_10m` — 海拔 10 米处的阵风速度（公里/小时）。  
- `cloud_cover` — 总云量（百分比）。  
- `is_day`（仅适用于当前天气） — 是否为白天的标志（0/1）。  
- `uv_index`（仅适用于每小时数据） — 紫外线指数。  
- `snowfall` — 降雪量（厘米）。  
- `visibility` — 能见度（米）。  
- `pressure_msl` — 海平面气压（百帕）。  

### 日常天气数据（常用）  
- `temperature_2m_max` / `temperature_2m_min` — 当天的最高/最低气温（摄氏度）。  
- `precipitation_sum` — 当天的总降水量（毫米）。  
- `precipitation_probability_max` — 最高降水概率（百分比）。  
- `weather_code` — 当天的主要天气状况。  
- `wind_speed_10m_max` — 最大风速（公里/小时）。  
- `sunrise` / `sunset` — ISO 8601 标准的日出/日落时间。  
- `uv_index_max` — 最高紫外线指数。  
- `snowfall_sum` — 当天的总降雪量（厘米）。  
- `apparent_temperature_max` / `apparent_temperature_min` — 当天的体感温度范围（摄氏度）。  

## 详细变量说明  
运行 `openmeteo weather help <参数>` 可查看所有可用变量及其详细说明：  
```
openmeteo weather help --daily-params
openmeteo weather help --hourly-params
openmeteo weather help --current-params
openmeteo history help --daily-params
```  
若需紧凑型 TSV 格式输出，可使用：  
`openmeteo weather help --daily-params --llm`  

当需要查询上述常见变量之外的其他特定变量时，请使用此命令。  

**使用规则：**  
1. 始终使用 `--llm` 选项生成输出，该格式对语言模型最为高效。  
2. 在 shell 命令中务必对用户提供的所有值加上引号（如城市名称、日期等），以防被 shell 解释为普通文本：`--city="New York"`、`--city="St. Petersburg"`。只有已知安全的字符（数字、单个 ASCII 单词）可以不加引号。  
3. 如果用户未指定位置，系统会使用会话上下文中的默认城市/国家信息。  
4. 以自然语言的形式呈现结果，切勿直接将原始 CLI 输出内容提供给用户。  
5. 对于今天或明天的天气查询，使用 `--forecast-days=1` 或 `--forecast-days=2`；避免不必要的数据获取。  
6. 对于具体问题（例如：“雨什么时候会停？”），通过 `--hourly-params` 或 `--daily-params` 覆盖相关参数，仅获取所需信息并给出答案。  
7. 当用户询问特定日期的天气时（例如：“周五的天气如何？”），使用 `--forecast-since=日期` 来避免获取不必要的历史数据。  
8. 当用户更换查询城市时（例如：“伦敦的天气如何？”），请保留之前查询中使用的所有参数；新城市的参数设置将是之前所有参数的集合。  

**对话示例：**  
**用户：** “天气怎么样？”  
  - 未指定位置 → 使用会话中的默认城市/国家信息。  
  → 输出示例：`--current`。  
  **结果示例：** “天气晴朗，气温 -12°C，体感温度 -17°C，风速 9 公里/小时。”  

**用户：** “雨什么时候会停？”  
  → 需要每小时降水量的时间线。  
  → 输出示例：`--hourly-params=hourly-params`，查找降水量降至 0 的时间点，然后回答：“预计今天 14:00 左右雨会停止。”  

**用户：** “我需要带伞吗？”  
  → 根据降水概率回答：`--hourly-params=hourly-params`，判断 11:00–15:00 之间有 70% 的降水概率，降水量可达 2 毫米，因此需要带伞。  

**用户：** “这个周末罗马的天气如何？”  
  → 设置 `--forecast-since=今天` 和 `--forecast-days=2` 来获取周六到周日的天气信息。  
  → 输出示例：  
  **周六：气温 14°C，部分多云；**  
  **周日：气温 16°C，晴朗。**  

**用户：** “外面的温度是多少？”  
  → 仅查询温度，因此只需使用相关参数：  
  → 输出示例：`--temperature-unit=摄氏度`，得到答案：“-5°C，体感温度 -9°C。”  

**用户：** “去年六月东京的降水量是多少？”  
  → 获取总降水量及具体降水较多的日期：  
  → 使用 `--history` 命令，并查看 `--hourly-params` 来获取详细信息。