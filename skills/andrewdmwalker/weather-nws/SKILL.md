---
name: weather-nws
description: 使用美国国家气象局（National Weather Service）的API获取可靠的天气数据。完全免费，无需API密钥，提供详细的天气预报和官方天气警报。
version: 1.0.0
author: awalker
homepage: https://weather.gov
keywords: weather, forecast, alerts, nws, national-weather-service
metadata:
  openclaw:
    emoji: 🌤️
    requires:
      bins: ["curl", "node"]
---

# 天气信息（NWS）

通过美国国家气象局（National Weather Service, NWS）的API获取可靠、详细的天气数据。非常适合美国境内的使用——完全免费，无需API密钥，并提供官方天气警报。

## 使用场景

当您需要以下功能时，可以使用此技能：
- **无需API密钥的可靠美国天气数据**
- **官方天气警报**（龙卷风预警、洪水预警等）
- **超出基本温度信息的详细当前天气状况**
- **包含详细描述的7天天气预报**
- **包含准确当地天气信息的晨间天气简报**
- **用于自动化或定时任务中的天气监控**
- **针对恶劣天气的警报通知**

此技能非常适合基于OpenClaw的系统，能够满足对专业级天气数据的需求，同时避免了商业API的复杂性及高昂费用。

## 主要功能

- 🌡️ **详细当前天气状况**：温度、体感温度、湿度、风速、气压、能见度、露点
- 📅 **7天天气预报**：每日详细的天气预报
- 🚨 **官方警报**：寒冷天气预警、龙卷风预警、洪水预警等
- 🆓 **100% 免费**：无需API密钥，无使用限制，使用的是政府提供的可靠服务
- 📍 **数据准确性**：数据来源于美国国家气象局的官方气象站

## 快速入门

### 获取当前天气信息

```bash
node weather-nws.js
```

### JSON输出（适用于脚本）

```bash
node weather-nws.js --json
```

## 配置

请在`weather-nws.js`文件中修改坐标，以设置您的位置：

```javascript
// Example: Fort Worth, Texas
const FORT_WORTH = {
    lat: 32.7555,
    lon: -97.3308
};
```

您可以在[latlong.net](https://www.latlong.net)获取坐标。

## 使用示例

### 基本天气查询

快速获取当前天气状况和天气预报：

```bash
node weather-nws.js
```

**输出：**
```
=== CURRENT CONDITIONS ===
Temperature: 30°F (Feels like: 21°F)
Condition: Clear
Humidity: 69%
Wind: 10 mph 310
Pressure: 30 inHg
Visibility: 10 miles
Dewpoint: 21°F

=== TODAY'S FORECAST ===
Sunny, with a high near 47. North northwest wind 5 to 10 mph.

=== 7-DAY OUTLOOK ===
Today: 47°F - Sunny
Tonight: 21°F - Mostly Clear
Saturday: 33°F - Sunny
Saturday Night: 22°F - Mostly Clear
Sunday: 53°F - Sunny
Sunday Night: 34°F - Clear
Monday: 64°F - Mostly Sunny

🚨 ACTIVE NWS ALERTS:
Cold Weather Advisory (Moderate/Expected)
Cold Weather Advisory issued January 29 at 11:49PM CST until January 31 at 11:00AM CST
```

### 程序化使用（JSON格式）

适用于自动化和集成：

```bash
node weather-nws.js --json
```

返回的结构化JSON数据包含：
- `current`：当前天气状况对象
- `forecast`：7天天气预报数组
- `alerts`：检测到的天气警报信息
- `timestamp`：ISO时间戳
- `source`："National Weather Service"

### 与OpenClaw集成

您可以在OpenClaw的提示功能或定时任务中使用此技能：

```
Check the weather and let me know if I need a jacket today.
```

### 天气警报监控

该技能支持检测以下类型的警报：
- 🌪️ **龙卷风**预警（紧急级别）
- ⛈️ **强风暴**（伴有强风和冰雹，高风险）
- 🌊 **洪水**预警和山洪暴发（高风险）
- ❄️ **冬季天气**：冰暴、暴风雪、大雪（高风险）
- 🔥 **高温**预警和极端高温预警（中等风险）
- 💨 **大风**预警（中等风险）

## API详细信息

### 美国国家气象局API

- **端点**：`api.weather.gov`
- **认证**：无需认证（建议添加User-Agent头部）
- **使用限制**：无（合理使用情况下无限制）
- **覆盖范围**：仅限美国境内
- **文档**：https://weather-gov.github.io/api/

### 数据来源

1. **Points API**：获取您所在位置的预报办公室和网格坐标
2. **Forecast API**：提供7天天气预报及详细描述
3. **Observations API**：获取最近气象站的实时数据
4. **Alerts API**：获取您所在地区的实时天气警报

## 高级用法

### 自定义位置

为其他城市创建相应的脚本：

```javascript
const NWSWeather = require('./weather-nws.js');

// Chicago coordinates
const weather = new NWSWeather(41.8781, -87.6298);
const data = await weather.getWeather();
console.log(JSON.stringify(data, null, 2));
```

### 检查天气警报

实时监控官方发布的天气警报：

```javascript
const NWSWeather = require('./weather-nws.js');

const weather = new NWSWeather(32.7555, -97.3308);
const alerts = await weather.getActiveAlerts();

if (alerts.length > 0) {
    console.log('⚠️ ACTIVE ALERTS:');
    alerts.forEach(alert => {
        console.log(`${alert.event} - ${alert.severity}/${alert.urgency}`);
        console.log(alert.headline);
    });
}
```

## 输出格式

### 当前天气状况对象

```json
{
  "current": {
    "temp": "30°F",
    "feelsLike": "21°F",
    "condition": "Clear",
    "humidity": "69%",
    "windSpeed": "10 mph",
    "windDirection": "310",
    "pressure": "30 inHg",
    "visibility": "10 miles",
    "dewpoint": "21°F"
  },
  "forecast": {
    "today": "Sunny, with a high near 47...",
    "tonight": "Mostly clear...",
    "high": "47°F",
    "periods": [...]
  },
  "alerts": [],
  "timestamp": "2026-01-30T15:00:00.000Z",
  "source": "National Weather Service"
}
```

## 为什么选择NWS？

与其他天气API相比：

| 功能 | NWS | wttr.in | OpenWeather | WeatherAPI |
|---------|-----|---------|-------------|------------|
| 费用 | 免费 | 免费 | 每月40美元起 | 每月0-50美元 |
| API密钥 | 不需要 | 不需要 | 需要 | 需要 |
| 可靠性 | 非常可靠 | 一般 | 相对可靠 | 相对可靠 |
| 官方警报 | 支持 | 不支持 | 不支持 | 仅部分支持 |
| 详细程度 | 非常详细 | 一般 | 相对详细 | 非常详细 |
| 美国覆盖范围 | 完全覆盖 | 完全覆盖 | 完全覆盖 | 完全覆盖 |

## 故障排除

### “NWS返回无效响应”

请确认您的坐标正确且位于美国境内。NWS API仅覆盖美国领土。

### 超时错误

请在脚本中增加超时时间：

```javascript
{ encoding: 'utf8', timeout: 30000 } // 30 seconds
```

### 未显示警报

这是正常现象！该技能仅在您所在地区有天气警报时才会显示警报信息。

## 集成示例

### 晨间天气简报

在每日自动化任务中包含天气信息：

```javascript
const NWSWeather = require('./weather-nws.js');
const weather = new NWSWeather(32.7555, -97.3308);
const data = await weather.getWeather();

console.log(`Good morning! It's ${data.current.temp} and ${data.current.condition}.`);
console.log(`Today's high will be ${data.forecast.high}.`);

if (data.alerts.length > 0) {
    console.log(`⚠️ Weather alerts: ${data.alerts.map(a => a.type).join(', ')}`);
}
```

### Discord/Telegram机器人

将天气更新发布到聊天频道：

```javascript
const data = await weather.getWeather();
const message = `🌤️ **Weather Update**\n` +
    `Current: ${data.current.temp} (feels like ${data.current.feelsLike})\n` +
    `Today's high: ${data.forecast.high}\n` +
    `Forecast: ${data.forecast.today}`;

// Send to your messaging platform
await sendMessage(message);
```

### 基于警报的定时任务

实时监控恶劣天气：

```bash
#!/bin/bash
# Check weather every 15 minutes, alert on warnings

weather_json=$(node weather-nws.js --json)
alerts=$(echo "$weather_json" | jq -r '.alerts[] | .type')

if [ -n "$alerts" ]; then
    # Send notification
    echo "Weather alerts detected: $alerts"
    # Your notification logic here
fi
```

## 许可证

该技能使用了美国国家气象局的API，属于公共领域（美国政府所有）。

## 技术支持

- **NWS API相关问题**：[https://github.com/weather-gov/weather.gov/issues]
- **技能使用问题**：请联系作者

## 致谢

天气数据由美国国家气象局（NOAA）提供。

---

**专为OpenClaw设计**（原名Clawdbot）