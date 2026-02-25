---
name: open-meteo-weather
description: 使用 Open-Meteo API 可以获取任意地点的当前天气状况以及未来 7 天的每日天气预报。该 API 支持地理编码功能，可将城市名称转换为坐标。完全免费，无需 API 密钥。
  Fetch current weather conditions and 7-day daily forecasts for any location
  using the Open-Meteo API. Includes geocoding to resolve city names to
  coordinates. Free, no API key required.
---
# Open-Meteo 天气服务

提供任意地点的当前天气状况及未来7天的每日天气预报。该服务使用免费的Open-Meteo API，并内置了地理编码功能。非商业用途无需API密钥、身份验证或速率限制。

## 快速参考

| 功能 | API端点          |
|--------|-----------------|
| 将城市名称转换为经纬度 | `GET https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en` |
| 当前天气及7天预报 | `GET https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,precipitation&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,sunrise,sunset,wind_speed_10m_max,weather_code&timezone=auto` |

## 单位

默认使用公制单位。在会话中首次请求天气信息时，询问用户：“您更喜欢摄氏度还是华氏度？”并记住他们的选择，以便后续请求使用相同单位。

- **公制单位（默认）**：无需额外参数。
- **英制单位**：在预报URL后添加以下参数：

```
&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch
```

响应中的`current_units`和`daily_units`对象会反映用户选择的单位系统。

## 地理编码

在调用预报API之前，需将城市名称转换为经纬度。

**API端点：** `GET https://geocoding-api.open-meteo.com/v1/search`

| 参数    | 是否必填 | 描述                |
|---------|---------|-------------------|
| `name`   | 是      | 城市名称（至少2个字符）         |
| `count`   | 否      | 结果数量（默认10个，最多100个）     |
| `language` | 否      | 响应语言（默认为英语）         |

**示例：**

```bash
curl "https://geocoding-api.open-meteo.com/v1/search?name=Berlin&count=1&language=en"
```

**从响应中提取的信息：**

| 字段      | 描述                |
|---------|-------------------|
| `results[0].latitude` | 经度（WGS84坐标）       |
| `results[0].longitude` | 纬度（WGS84坐标）       |
| `results[0].name` | 对应的城市名称         |
| `results[0].country` | 所在城市所属的国家         |
| `results[0].admin1` | 所在城市所属的行政区划       |

如果`results`为空或未找到匹配的城市，请告知用户并请求提供更具体的信息。

如果有多个城市名称相同，可使用`count=5`来显示多个选项（城市名称、行政区划、国家名称），以便用户选择正确的地点。

## 当前天气状况

在请求预报时需包含`current`参数。

**请求参数：**

```
current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,precipitation
```

**响应字段：**

| 字段      | 描述                |
|---------|-------------------|
| `current_temperature_2m` | 海拔2米处的温度         |
| `current.apparent_temperature` | 体感温度（风寒指数）       |
| `current.relative_humidity_2m` | 相对湿度百分比         |
| `current.weather_code` | WMO天气代码           |
| `current.wind_speed_10m` | 海拔10米处的风速         |
| `current.wind_direction_10m` | 风向（度）             |
| `current.precipitation` | 过去一小时的降水量         |

所有单位均来自`current_units`对象。在显示数值时务必注明单位。

**风向转换：**  
将`current.wind_direction_10m`（度）转换为相应的罗盘方向：  
N（338-22°）、NE（23-67°）、E（68-112°）、SE（113-157°）、S（158-202°）、SW（203-247°）、W（248-292°）、NW（293-337°）。

## 日常天气预报

请求预报时需包含`daily`参数，并设置`timezone=auto`以确保时间显示为当地时区。

**请求参数：**

```
daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,sunrise,sunset,wind_speed_10m_max,weather_code&timezone=auto
```

所有`daily`字段均为按日期排序的数组。`daily.time`包含日期字符串（格式为YYYY-MM-DD）。

| 字段      | 描述                |
|---------|-------------------|
| `daily.time[i]` | 日期                |
| `daily.weather_code[i]` | 当天的WMO天气代码         |
| `daily.temperature_2m_max[i]` | 当天最高温度           |
| `daily_temperature_2m_min[i]` | 当天最低温度           |
| `daily.precipitation_sum[i]` | 总降水量             |
| `daily.precipitation_probability_max[i]` | 最大降水量概率（%）         |
| `daily.sunrise[i]` | 当天日出时间（ISO 8601格式）     |
| `daily.sunset[i]` | 当天日落时间（ISO 8601格式）     |
| `daily.wind_speed_10m_max[i]` | 当天最大风速             |

## 天气代码

`weather_code`字段返回的WMO天气代码及其含义：

| 代码 | 描述                |
|------|-------------------|
| 0    | 晴朗                |
| 1    | 多云                |
| 2    | 部分多云             |
| 3    | 阴天                |
| 45    | 雾                 |
| 48    | 结冰雾                |
| 51    | 小雨                |
| 53    | 中等雨                |
| 55    | 大雨                |
| 56    | 小雨夹雪              |
| 57    | 大雨夹雪              |
| 61    | 小雪                |
| 63    | 中等雪                |
| 65    | 大雪                |
| 71    | 大雪                |
| 73    | 雪粒                |
| 80    | 小雨阵雨              |
| 81    | 中等雨阵雨              |
| 82    | 暴雨阵雨              |
| 85    | 小雪阵雨              |
| 86    | 大雪阵雨              |
| 95    | 雷暴                |
| 96    | 伴有小冰雹的雷暴          |
| 99    | 伴有大雨雹的雷暴          |

向用户展示天气信息时，请使用相应的描述，不要直接显示数字代码。

## 响应格式

以简洁的方式呈现信息，避免显示原始JSON数据、API地址或技术细节。

**当前天气状况格式：**

```
Weather in {city}, {country}
{weather description}, {temperature} (feels like {apparent_temperature})
Humidity: {humidity}%
Wind: {speed} from the {compass_direction}
Precipitation: {amount}
```

**天气预报格式：**

在当前天气信息之后，以列表形式展示未来7天的天气情况，每天一条记录：

```
Mon Feb 24: Partly cloudy, 8/3C, 10% rain, wind 15 km/h
Tue Feb 25: Rain, 6/2C, 80% rain, 4.2mm, wind 25 km/h
```

如果用户提出具体问题（如“明天会下雨吗？”、“周五的温度是多少？”），请直接回答，无需展示完整的天气预报。

## 错误处理**

如果API请求返回非200状态码或响应无法解析，请告知用户天气服务暂时不可用，并建议用户稍后重试。不要显示原始错误信息或状态码。