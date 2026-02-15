---
name: dc-weather
description: 使用 Open-Meteo API 检查华盛顿特区的天气。当用户询问华盛顿特区的天气、当前状况或需要该地区的天气报告时，可以使用此功能。
---

# 华盛顿特区天气查询技能

无需API密钥，即可使用Open-Meteo获取华盛顿特区的天气信息。

## 快速查看

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=38.9072&longitude=-77.0369&current_weather=true&temperature_unit=fahrenheit" | jq -r '"DC: \(.current_weather.temperature)°F, wind \(.current_weather.windspeed) mph, code \(.current_weather.weathercode)"'
```

## 天气代码

| 代码 | 天气状况 |
|------|-----------|
| 0   | 晴朗 |
| 1-3  | 部分多云 |
| 45-48 | 雾 |
| 51-57 | 小雨 |
| 61-67 | 中雨 |
| 71-77 | 下雪 |
| 95-99 | 雷暴 |

## 美观显示格式

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=38.9072&longitude=-77.0369&current_weather=true&temperature_unit=fahrenheit" | jq -r '"\n🌤️ Washington, DC\n━━━━━━━━━━━━━━\n🌡️  \(.current_weather.temperature)°F\n💨  Wind: \(.current_weather.windspeed) mph\n🌪️  Code: \(.current_weather.weathercode)\n"'
```