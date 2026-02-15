---
name: tuebingen-weather
description: 使用 open-meteo.com 每天 08:00 发送蒂宾根的天气报告。当管理员需要自动化的天气总结（当前天气状况、当天的最高/最低温度以及降雨概率）时，这些信息会被存储在本地并通过 Telegram 转发。
---

# 图宾根天气

## 概述  
该技能提供图宾根的每日天气概要（使用Open-Meteo API，无需API密钥）。输出形式为简洁的文本，包含当前天气状况、当日最低/最高温度以及降雨概率。

## 快速入门  
1. **手动获取**  
   ```bash
   python3 skills/tuebingen-weather/scripts/fetch_tuebingen_weather.py \
     --output data/weather/$(date +%F)_tuebingen.txt
   ```  
   -> 可输出天气概要，并可选择将其保存到文件中。  

2. **无需文件**（仅通过控制台/Telegram获取）：  
   ```bash
   python3 skills/tuebingen-weather/scripts/fetch_tuebingen_weather.py
   ```  

## 自动发送（每天08:00）  
1. **设置Cron任务**  
   ```bash
   openclaw cron add <<'JSON'
   {
     "name": "tuebingen-weather-08",
     "schedule": { "kind": "cron", "expr": "0 8 * * *", "tz": "Europe/Berlin" },
     "sessionTarget": "isolated",
     "payload": {
       "kind": "agentTurn",
       "model": "default",
       "message": "Run `python3 skills/tuebingen-weather/scripts/fetch_tuebingen_weather.py --output data/weather/$(date +%F)_tuebingen.txt`. Send Master the stdout summary + mention the saved file. Report errors if the command fails."
     }
   }
   JSON
   ```  
2. **工作原理**：  
   - 将天气信息保存到`data/weather/YYYY-MM-DD_tuebingen.txt`文件中（文件名可自定义）。  
   - Cron任务会在每天早上08:00自动发送天气信息。  

## 注意事项：  
- 该脚本仅使用Python的标准库（`urllib`、`json`），无需安装额外的库。  
- 天气代码对应的德文描述请参考`WEATHER_CODES`文件。  
- 时区设置为`Europe/Berlin`，会自动切换为夏令时/冬令时。  
- 如需添加更多天气信息（如风速、紫外线指数等），可直接修改脚本内容。  

## 资源文件：  
- `scripts/fetch_tuebingen_weather.py` – 用于从Open-Meteo获取天气数据的命令行脚本。