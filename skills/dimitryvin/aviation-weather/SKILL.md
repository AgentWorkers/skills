---
name: aviation-weather
description: 从 aviationweather.gov 获取航空天气数据（METAR、TAF、PIREP）。这些数据可用于飞行计划、天气简报、检查机场状况或任何与飞行员相关的天气查询。触发条件包括 "METAR"、"TAF"、"flight weather"、"airport weather"、"aviation weather"、"pilot report" 以及特定的 ICAO 代码。
---

# 航空天气

从FAA的aviationweather.gov API获取实时航空天气数据。

## 快速参考

```bash
# METAR for specific airports
python3 scripts/wx.py KSMO KLAX KVNY

# METAR + TAF
python3 scripts/wx.py KSMO KLAX --metar --taf

# Just TAF
python3 scripts/wx.py KSMO --taf

# PIREPs near a location (lat/lon)
python3 scripts/wx.py --pirep --lat 34.0 --lon -118.4 --radius 100

# Raw output with JSON
python3 scripts/wx.py KSMO --json

# Verbose (show raw METAR text)
python3 scripts/wx.py KSMO -v
```

## 默认机场

当未指定机场时，系统将使用圣莫尼卡地区的机场：`KSMO`、`KLAX`、`KVNY`

## 飞行类别

- 🟢 VFR（视觉飞行规则）：云底高度大于3000英尺，能见度大于5海里
- 🔵 MVFR（中等视觉飞行规则）：云底高度在1000-3000英尺之间，或能见度在3-5海里之间
- 🔴 IFR（仪表飞行规则）：云底高度在500-1000英尺之间，或能见度在1-3海里之间
- 🟣 LIFR（着陆目视规则）：云底高度低于500英尺，或能见度低于1海里

## 南加州常见机场

| 代码 | 名称 |
|------|------|
| KSMO | 圣莫尼卡 |
| KLAX | 洛杉矶国际机场 |
| KVNY | 范努伊斯 |
| KBUR | 伯班克 |
| KTOA | 托伦斯 |
| KSNA | 约翰·韦恩机场 |
| KFUL | 富勒顿 |
| KCMA | 卡马里洛 |
| KOXR | 奥克斯纳德 |
| KPSP | 棕榈泉 |

## 命令行参数

- `--metar`, `-m`：获取METAR天气报告（默认）
- `--taf`, `-t`：获取TAF（天气预报）数据
- `--pirep`, `-p`：获取飞行员报告
- `--hours N`：获取METAR历史记录的时长（默认：2小时）
- `--lat`, `--lon`：指定飞行员报告的搜索位置（经纬度）
- `--radius N`：指定飞行员报告的搜索半径（单位：海里，默认：100海里）
- `--verbose`, `-v`：显示原始观测数据
- `--json`：以JSON格式输出数据