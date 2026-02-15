---
name: weather
description: 获取当前天气和天气预报（无需API密钥）。
homepage: https://wttr.in/:help
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["curl"] } } }
---

# 天气信息

有两项免费的服务，无需使用API密钥。

## wttr.in（主要推荐）

**简短的使用方式：**

```bash
curl -s "wttr.in/London?format=3"
# Output: London: ⛅️ +8°C
```

**紧凑格式：**

```bash
curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"
# Output: London: ⛅️ +8°C 71% ↙5km/h
```

**完整天气预报：**

```bash
curl -s "wttr.in/London?T"
```

**格式说明：**
- `%c`：天气状况
- `%t`：温度
- `%h`：湿度
- `%w`：风速
- `%l`：位置
- `%m`：月亮状态

**使用提示：**
- 对URL中的空格进行URL编码：`wttr.in/New+York`
- 机场代码示例：`wttr.in/JFK`
- 单位选择：`?m`（公制）`?u`（英制）
- 仅显示今日天气：`?1`  
- 仅显示当前信息：`?0`
- 下载天气图片（PNG格式）：`curl -s "wttr.in/Berlin.png" -o /tmp/weather.png`

## Open-Meteo（备用方案，返回JSON格式）

完全免费，无需密钥，适合程序化使用：

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
```

**操作步骤：**
1. 首先查找目标城市的坐标。
2. 使用这些坐标查询天气信息，Open-Meteo会返回包含温度、风速和天气代码的JSON数据。

**文档链接：** https://open-meteo.com/en/docs