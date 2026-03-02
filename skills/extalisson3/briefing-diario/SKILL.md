---
name: briefing diario
description: 提供一个用于显示日常信息的仪表板界面，内容包括地理位置、天气状况、经济数据以及天气预报。每当用户请求“每日简报”或输入“briefing”命令时，均应显示该界面。
---
# 技能：每日摘要

该技能可将 OpenClaw 转换为本地化的情境助手，通过整合来自多个免费数据源的信息来生成一个信息面板。

## 对代理的指令

### 1. 定位
获取用户所在城市的地理位置（默认值：Belo Horizonte，坐标：-19.9208, -43.9378）

### 2. 数据收集

**日期和时间：**
- 使用 `TZ="America/Sao_Paulo" date` 来获取用户的正确日期和时间
- 格式：`2026年2月22日，16:27`
- 将月份翻译成葡萄牙语

**天气和天文数据：**
使用 Open-Meteo 的 API：
```
https://api.open-meteo.com/v1/forecast?latitude=-19.9208&longitude=-43.9378&daily=uv_index_max,sunset,sunrise&hourly=precipitation_probability&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&timezone=auto
```

提取并映射以下数据：
- `current_temperature_2m` → 温度（TEMP）
- `current.apparent_temperature` → 体感温度（FEEL）
- `current.wind_speed_10m` → 风速（VENTO）
- `current.relative_humidity_2m` → 相对湿度（UMIDADE）
- `daily.uv_index_max[0]` → 紫外线指数（UV_INDEX）
- `daily.sunrise[0]` → 日出时间（SUNRISE）
- `daily.sunset[0]` → 日落时间（SUNSET）
- `current.weather_code` → 天气预报文本（将 WMO 代码映射为葡萄牙语）
- `hourly.precipitation_probability` → 当前小时的降雨概率（CHANCE_DE_CHUVA）

**天气预报数据：**
使用 AwesomeAPI：
```
https://economia.awesomeapi.com.br/json/last/USD-BRL,JPY-BRL,BTC-BRL,KRW-BRL,EUR-BRL
```

**节假日信息：**
```
https://date.nager.at/api/v3/PublicHolidays/2026/BR
```

### 3. 格式化规则

- 输出内容必须使用 markdown 代码块格式，以保持文本对齐。
- 严格遵循以下视觉模板。
- 将月相名称和天气状况翻译成葡萄牙语（巴西地区）。

### 4. WMO 代码对照表

| WMO 代码 | 天气状况 |
|--------|-------|
| 0       | 晴朗 |
| 1, 2, 3    | 部分多云 |
| 45, 48    | 雾蒙蒙 |
| 51, 53, 55 | 小雨 |
| 61, 63, 65 | 中雨 |
| 71, 73, 75 | 下雪 |
| 80, 81, 82 | 阵雨 |
| 95       | 暴风雨 |
| 96, 99     | 冰雹 |

### 5. 紫外线指数（UV Index）分级

| 紫外线指数 | 风险等级 | 建议 |
|---------|---------|------|
| 0-2       | 低       | 无需特殊防护 |
| 3-5       | 中等       | 使用防晒霜 |
| 6-7       | 高        | 避免在 10:00-16:00 晒太阳 |
| 8-10       | 非常高     | 必须使用防晒措施 |
| 11+       | 极高       | 完全避免阳光照射 |

## 输出模板

代理需要根据收集到的数据填充以下模板：

```
🌍 Tudo sobre onde você mora
🌄 Belo Horizonte - [DATA ATUAL], [HORA]

☀️ CLIMA AGORA
🌡 [TEMP]ºC (sensação [FEEL]ºC)
🌀 Vento: [VENTO] km/h
💧 Umidade: [UMIDADE]%
☁️ Previsão: [PREVISÃO_TEXTO]
🌧 Chance de Chuva: [CHANCE_DE_CHUVA]%

📊 ÍNDICES DO DIA
🌞 UV: [UV_INDEX] ([RISCO] - [DICA_UV])
🌅 Sol nasce: [SUNRISE] | põe: [SUNSET]

💵 COTAÇÕES
💲 Dólar: R$ [USD] ([USD_VAR]%)
💶 Euro: R$ [EUR] ([EUR_VAR]%)
💴 Iene: R$ [JPY] ([JPY_VAR]%)
🇰🇷 Won Sul-Coreano: R$ [KRW] ([KRW_VAR]%)
₿ Bitcoin: R$ [BTC] ([BTC_VAR]%)

📅 HOJE - [FERIADO_STATUS]

💡 DICA: [DICA_CONTEXTUAL]
```

## 注意事项：

- 用上述数据源获取的实际数据替换模板中的占位符。
- 如果某个数据源无法获取数据，应显示友好的错误信息并使用备用占位符。
- 日期和时间应反映数据收集的实时情况。
- 该技能已准备好集成到您的自动化数据收集流程中，可以通过命令 “dia”、“resumo do dia” 或 “briefing” 来触发执行。