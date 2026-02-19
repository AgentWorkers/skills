---
name: weather-open-meteo
description: "通过 open-meteo.com 获取当前天气和天气预报；如果 open-meteo.com 不可用，可备用 wttr.in。无需使用 API 密钥。"
homepage: https://open-meteo.com/
metadata:
  openclaw:
    emoji: 🌤️
    requires:
      bins:
        - curl
        - jq
---
# Weather Open-Meteo 技能

该技能通过查询 open-meteo.com 的公共 API 来提供当前的天气信息和简单的天气预报。如果地理编码或天气请求失败，该技能会回退到 wttr.in 作为替代方案。

## 📌 范围与注意事项
* 该技能 **需要** `curl` 和 `jq` 工具。
* 用户提供的位置信息 **必须** 进行 URL 编码（或使用相应的工具进行编码）。例如：“São Paulo” 应编码为 `S%C3%A3o%20Paulo`。未编码的位置信息可能会导致请求失败或出现意外结果。

## ✅ 适用场景
✔ 当用户询问某个地点的天气、预报、温度或降雨概率时。
✖ 该技能不适用于获取历史数据、严重天气警报或详细的气候信息。

## 📋 命令
该技能接受一个参数：地点名称（城市、地区或经纬度坐标 `lat,lon`）。

## Open-Meteo（主要接口，返回格式为 JSON）

**地理编码**（根据坐标获取地点信息）：

```bash
curl -s "https://geocoding-api.open-meteo.com/v1/search?name=São+Paulo\u0026count=1" | jq '.results[0] | {name, latitude, longitude}'
```

**当前天气**（根据坐标获取）：

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=-23.55\u0026longitude=-46.63\u0026current_weather=true" | jq '.current_weather'
```

**7 天天气预报**（根据坐标获取）：

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=-23.55\u0026longitude=-46.63\u0026daily=temperature_2m_max,temperature_2m_min,precipitation_sum\u0026forecast_days=7" | jq '.daily'
```

**示例 JSON 数据**：

```json
{
  "latitude": -23.55,
  "longitude": -46.63,
  "current_weather": {
    "temperature": -5.3,
    "windspeed": 3.9,
    "winddirection": 200,
    "weathercode": 80,
    "time": "2024-02-18T14:00"
  }
}
```

📖 [Open-Meteo API 文档](https://open-meteo.com/en/docs)

## wttr.in（备用方案）

**简短命令（返回 HTML 格式）**：

```bash
curl -s "wttr.in/São+Paulo?format=3"
```

**简洁的纯文本格式**：

```bash
curl -s "wttr.in/São+Paulo?format=1"
```

**PNG 图像（适用于终端或嵌入）**：

```bash
curl -s -o sp.png "http://wttr.in/São+Paulo?format=1"
```

## 📚 使用示例
> **用户**：**圣保罗的天气怎么样？**
> **机器人回答**：
> **圣保罗的当前天气：🌤️，降雨概率 20%**

## 提示
- **请对城市名称进行 URL 编码**：
  ```bash
  curl -s "https://geocoding-api.open-meteo.com/v1/search?name=$(echo São Paulo | jq -sRr @uri)"
  ```
- **可以使用 `jq` 动态构建请求参数**：
  ```bash
  city="São Paulo"
  lat=$(curl -s "https://geocoding-api.open-meteo.com/v1/search?name=$(echo $city | jq -sRr @uri)" | jq -r '.results[0].latitude')
  lon=$(curl -s "https://geocoding-api.open-meteo.com/v1/search?name=$(echo $city | jq -sRr @uri)" | jq -r '.results[0].longitude')
  ```
- 如果你知道经纬度坐标，可以直接传递这些值。
- 该 API 有请求频率限制（约每分钟 100 次请求）。请确保脚本缓存结果或适当增加请求间隔。