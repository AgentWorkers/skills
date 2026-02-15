---
name: tuebingen-weather-graphics
description: 从 open-meteo.com 生成并发送一份为期 5 天的图宾根天气图表（PNG 格式）。当 Master 需要更直观的天气预报以及未来几天的天气总结文本时，可以使用这份图表。
---

# 图宾根天气图表

## 概述  
该脚本基于 Open-Meteo 数据生成一张美观的 PNG 图表（显示未来 5 天的最高/最低温度及降雨概率），非常适合通过 Telegram 发送晨间天气预报或用于数据存档。

## 系统要求  
- Python 3.11 或更高版本  
- 必需安装 `matplotlib`, `numpy`, `pillow` 库（建议通过虚拟环境安装）：  
  ```bash
  python3 -m venv /tmp/tuebingen-plot
  source /tmp/tuebingen-plot/bin/activate
  pip install matplotlib
  ```

## 快速入门  
执行以下命令后，天气图表将生成并保存在 `data/weather/` 目录下：  
```bash
/tmp/tuebingen-plot/bin/python \
  skills/tuebingen-weather-graphics/scripts/generate_forecast_graph.py \
  --days 5 \
  --output data/weather/tuebingen_forecast.png
```  
输出结果包括：  
- 一张 PNG 图片  
- 终端中显示的文字摘要（例如：“2023年2月13日星期五：最高温度 5°C，最低温度 10°C，降雨概率 85%”）

## 自动化发送  
1. **定时任务（例如每天早上 7:30）：**  
   ```bash
   openclaw cron add <<'JSON'
   {
     "name": "tuebingen-forecast-graphic",
     "schedule": { "kind": "cron", "expr": "30 7 * * *", "tz": "Europe/Berlin" },
     "sessionTarget": "isolated",
     "payload": {
       "kind": "agentTurn",
       "model": "default",
       "message": "Run `/tmp/tuebingen-plot/bin/python skills/tuebingen-weather-graphics/scripts/generate_forecast_graph.py --output data/weather/tuebingen_forecast.png`. Send Master the summary text plus attach the PNG."
     }
   }
   JSON
   ```  
2. **通过 Telegram 发送图表：** 使用 `message.send` 函数，并将生成的图片文件（`tuebingen_forecast.png`）作为附件发送。  

## 常见问题及解决方法：  
- **`Matplotlib ImportError`：** 确保已激活虚拟环境，或确保相关库已全局安装。  
- **数据为空：** Open-Meteo 有时可能不提供降雨概率数据，此时脚本会显示 0%；可以通过修改代码来解决。  
- **显示更多天数的数据：** 可使用 `--days 7` 等参数来获取更多天的天气信息（API 提供最多 7 天的每日数据）。  

## 相关资源  
- `scripts/generate_forecast_graph.py`：该脚本负责加载每日天气数据，绘制折线图/面积图，并添加降雨概率柱状图，最终生成 PNG 文件。