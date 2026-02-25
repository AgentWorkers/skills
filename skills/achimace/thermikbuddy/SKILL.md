---
name: soaring-weather
description: >
  **滑翔飞行与热气流预报（附热气流评分0-10）**  
  当用户询问滑翔飞行天气、热气流情况、长途飞行条件、滑翔机或滑翔伞的飞行天气时，可使用此技能。例如：“周六适合飞行吗？”、“热气流情况如何？”、“周末的滑翔飞行天气如何？”或“周日能进行长途飞行吗？”等。该技能会调用Open-Meteo（ICON-D2）数据，提供专业级别的天气分析，包括每日天气变化、上升气流强度、基础海拔高度、阿尔卑斯山地区的特殊气象现象（如焚风、山坡飞行条件）以及相关警告信息。
version: 2.0.0
---
# Soaring Weather – 为滑翔飞行员提供的热气流预报系统 v2.0

该系统采用评分引擎，综合考虑了11个参数进行综合评估，包括风切变、高空湿度、焚风识别、山坡飞行奖励以及雷电安全限制等因素。

## 第一步：查询目标区域

```bash
python3 {baseDir}/scripts/run_forecast.py --list-regions
```

向用户提供以下选项供选择：
> 您希望获取哪个地区的热气流预报？
> 1. 🏔️ Werdenfels / 巴伐利亚阿尔卑斯山北麓
> 2. 🏔️ 因特塔尔/北蒂罗尔阿尔卑斯山
> 3. ⛰️ 施瓦本阿尔布山区
> 4. 🌲 施瓦茨瓦尔德森林
> 5. 🌾 北德平原
> 6. 📍 输入您的自定义坐标

如果用户已经指定了目标区域，则跳过此步骤。

## 第二步：获取预报数据

```bash
python3 {baseDir}/scripts/run_forecast.py --region <region_id> [--days 3]
```

或者，用户也可以通过输入自己的坐标来获取预报数据：

```bash
python3 {baseDir}/scripts/run_forecast.py --lat <lat> --lon <lon> --name "Name"
```

脚本会将预报结果以JSON格式输出到标准输出（stdout），并将日志记录到标准错误输出（stderr）。

## 第三步：格式化预报结果

### 每日天气概览

```
[Emoji] THERMIK-VORHERSAGE – [Standortname]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 [Wochentag], [Datum]
🏆 SCORE: [X]/10 — [Label]

🌡️ Thermik-Kern:
   Steigwerte: ~[X] m/s | Basis: [X]m MSL | BLH: [X]m AGL
   CAPE max: [X] J/kg

💨 Wind: ⌀[X] km/h | Windscherung: [X] km/h (10m→850hPa)
💧 Höhenluft (700hPa): [X]% r.F. → [trocken/normal/feucht]
🌍 Boden: [Feuchte-Bewertung]

[🏔️ Hangflug-Bonus: +X Punkte – Nordwindlage günstig]  ← nur wenn relevant
[⚠️ Warnungen]

📊 Tagesablauf:
   09-12: [◉◉◉◎◎] ~[X]m/s · BLH [X]m
   12-15: [◉◉◉◉◎] ~[X]m/s · BLH [X]m
   15-18: [◉◉◉◉◉] ~[X]m/s · BLH [X]m
   18-20: [◉◉◎◎◎] ~[X]m/s · BLH [X]m
```

### 评分等级及说明：
- 0–2：❌ 不适合滑翔飞行
- 2–4：🌥️ 适合飞行条件有限
- 4–6：⛅️ 适合飞行
- 6–8：☀️ 非常适合飞行
- 8–10：🔥 极佳飞行条件！

### 重要警告信息：
- 🔴 焚风：评分上限被触发，阿尔卑斯山边缘可能出现湍流
- 🔴 雷电风险（CAPE >2000 或 LI <-6）：评分上限为4.5
- 🔴 凝积云（Cb）风险：700hPa高度处的湿度超过65% 且 CAPE >800 → 评分降低2分
- ⚠️ 飞行条件恶化：建议尽早起飞，14:00前降落
- ⚠️ 风切变强度超过30 km/h：可能导致热气流结构不稳定

### 山坡飞行奖励（仅适用于阿尔卑斯山区）
当评分大于0时，系统会显示该奖励信息，并简要说明风向。在焚风或降雨情况下，此奖励无效。

## 第四步：提供相关链接

在每次预报结果输出后，系统会始终提供以下参考链接：
- DHV天气预报：https://www.dhv.de/wetter/dhv-wetter/
- SkySight：https://skysight.io
- TopMeteo：https://europe.topmeteo.eu/de/
- DWD滑翔天气信息：https://www.dwd.de/DE/fachnutzer/luftfahrt/kg_segel/segel_node.html
- Soaringmeteo（WRF 2公里模型）：https://soaringmeteo.org/v2
- aufwin.de：https://aufwin.de

## 参数详情

→ 有关所有阈值、权重、计算公式及区域类型的详细信息，请参阅 `{baseDir}/references/scoring_params.md`。

## 评分参数简介：

| 参数                        | 权重    | 特殊说明                          |
|------------------------|---------|---------------------------------------|
| BLH边界高度                | 18%     | 最重要的单一参数                         |
| CAPE                      | 12%     | 当 CAPE 超过2000 J/kg 时评分上限被触发           |
| 低层至中层云量                | 12%     | 云量在15–50%时有助于产生热气流           |
| 直射辐射                  | 10%     | 对热气流生成有促进作用                     |
| Lifted Index                | 8%      | 当 Lifted Index 低于6时评分上限被触发           |
| 10米高度风速                | 8%      | 风速过大可能导致飞行条件不佳                 |
| 地面湿度                    | 8%      | 地面干燥有助于产生更好的热气流                 |
| **风切变强度（>850hPa）**         | **7%**   | 强风切变会破坏热气流结构                 |
| **700hPa高度相对湿度**           | **7%**   | 新功能：用于提前识别积云                   |
| 前一天降雨量                | 5%      | 降雨可能影响当天飞行条件                     |
| T-Td温度差                 | 5%      | 云层底部高度的参考指标                     |