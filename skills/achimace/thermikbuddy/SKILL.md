---
name: soaring-weather
description: >
  **滑翔飞行与热气流天气预报（附带热气流评分 0–10）**  
  当用户询问滑翔飞行天气、热气流情况、长途飞行条件、滑翔机或滑翔伞的飞行天气时，可以使用此技能。例如：“周六适合飞行吗？”、“热气流情况如何？”、“周末的滑翔飞行天气如何？”或“周日可以进行长途飞行吗？”  
  该技能会根据用户提供的地区/位置信息，调用 Open-Meteo (ICON-D2) 和 DHV 的天气数据，提供专业的天气评估，包括天气变化趋势、上升气流强度、基础高度以及可能的天气警告。
version: 1.0.0
metadata: {"openclaw":{"emoji":"🪂","requires":{"bins":["python3"],"env":[]},"homepage":"https://github.com/soaring-weather/openclaw-skill"}}
---
# Soaring Weather – 为滑翔飞行员提供的热气流预报

该功能提供基于热气流的滑翔飞行预报，评分范围为0-10分，包含一天内的四个时间段、上升气流强度预测、基础高度信息以及与DHV（德国滑翔联合会）天气数据的整合。

## 第一步：询问用户所在地区

在获取预报之前，请先询问用户所需预报的地区。从配置文件中显示可用的地区选项：

```bash
python3 {baseDir}/scripts/run_forecast.py --list-regions
```

该代码段会将可用地区以JSON列表的形式输出。向用户提供选择选项，例如：
> 您想获取哪个地区的热气流预报？
> 1. 🏔️ Werdenfels / 巴伐利亚阿尔卑斯山北部边缘
> 2. 🏔️ 因特塔尔 / 北蒂罗尔阿尔卑斯山
> 3. ⛰️ 施瓦本阿尔布山区
> 4. 🌄 施瓦茨瓦尔德
> 5. 🌾 北德平原
> 6. 📍 输入您的自定义坐标

如果用户已经指定了一个地区或坐标（例如：“因斯布鲁克的热气流预报”或“瓦斯克库佩的滑翔飞行天气”），则可以直接跳过这一步并选择相应的地区或使用提供的坐标。

## 第二步：获取预报

使用用户选择的地区启动预报脚本：

```bash
python3 {baseDir}/scripts/run_forecast.py --region <region_id>
```

或者使用用户提供的自定义坐标启动预报脚本：

```bash
python3 {baseDir}/scripts/run_forecast.py --lat <lat> --lon <lon> --name "Standortname"
```

可选参数：
- `--days 3`（1–7天，默认为3天）
- `--no-dhv`（跳过DHV天气数据）

脚本会将预报结果以JSON格式输出到标准输出（stdout），日志则输出到标准错误（stderr）。

## 第三步：格式化预报结果

将JSON输出结果格式化以便用户阅读。使用以下模板进行展示：

### 每日天气概览

```
[Emoji] THERMIK-VORHERSAGE – [Standortname]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 [Wochentag], [Datum]
🏆 SCORE: [X]/10 — [Bewertungstext]

🌡️ Thermik-Kern:
   Steigwerte: ~[X] m/s | Basis: [X]m MSL
   CAPE: [X] J/kg | BLH: [X]m AGL

☁️ [Wolken-Beschreibung]
💨 Wind: [Richtung] [Geschwindigkeit] km/h
🌍 Boden: [Feuchte-Bewertung]
⚠️ [Warnungen falls zutreffend]

📊 Tagesablauf:
   09-12: [●-Balken] [Kurzbeschreibung]
   12-15: [●-Balken] [Kurzbeschreibung]
   15-18: [●-Balken] [Kurzbeschreibung]
   18-20: [●-Balken] [Kurzbeschreibung]
```

### 评分与表情符号对应关系
- 0–2分：❌ 无法进行滑翔飞行
- 3–4分：🌥️ 条件有限
- 5–6分：⛅ 适合滑翔的天气
- 7–8分：☀️ 非常适合滑翔的天气
- 9–10分：🔥 极佳的滑翔天气！

使用 ◉ 表示当前处于活跃状态的天气区域，使用 ◎ 表示天气不活跃的区域（每个时间段有5个这样的区域）。

### DHV天气信息块

如果DHV天气数据可用（`dhv_available`字段为`true`），则额外显示以下信息：

```
━━━ DHV WETTER – [Region] ━━━
Stand: [Zeitstempel]

[🔴/🟠/🟡/🟢] [Tag]: [Titel]
   [Beschreibung]
   💨 [Wind]
```

注意：DHV热气流预报在10月至次年3月期间暂停服务。即使在冬季，风力和风暴警报仍然具有参考价值。

### 详细信息链接

在预报结果末尾始终提供以下参考链接：
- DHV天气网站：https://www.dhv.de/wetter/dhv-wetter/
- SkySight：https://skysight.io
- TopMeteo：https://europe.topmeteo.eu/de/
- DWD滑翔天气网站：https://www.dwd.de/DE/fachnutzer/luftfahrt/kg_segel/segel_node.html
- aufwin.de：https://aufwin.de
- Soaringmeteo（WRF 2公里分辨率预报）：https://soaringmeteo.org/v2

## 评分说明

评分综合考虑了9个关键参数：
- CAPE指数
- 边界层高度（BLH）
- 升力指数
- 云层状况
- 风速
- 温度差异
- 太阳辐射
- 地面湿度
- 前一天的降水量。详细信息请参阅 `{baseDir}/references/scoring_params.md`。

地区特定调整：
- **阿尔卑斯山区**：识别焚风现象、防止天气过度发展的警告、Cu波热气流的额外加分机制
- **平原地区**：不识别焚风现象，使用不同的边界层高度阈值
- **中部山区**：进行适度的参数调整

DHV专家的每日两次评估（由气象学家Volker Schwaniz提供）用于验证预报结果；在风力/风暴警报情况下，专家评估结果可对算法评分进行修正——安全始终是首要考虑因素。