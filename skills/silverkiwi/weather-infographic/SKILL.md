---
name: infographic-weather
description: 生成一个具有特定地理位置季节性背景的电视风格天气信息图。当用户请求可视化天气预报或某个特定地址的天气信息图时，可以使用该信息图。
metadata: {"clawdbot":{"emoji":"📺","requires":{"env":["GEMINI_API_KEY"]},"install":[{"id":"pip-google-ai","kind":"exec","command":"pip install -U google-generativeai requests --break-system-packages","label":"Install dependencies"}]}}
---

# 信息图式天气预报

使用 Gemini 3 Pro 图像（Nano Banana）生成专业的电视风格天气预报画面。

## 特点
- **季节性背景**：根据用户提供的地址和当前当地季节（支持南北半球），生成逼真的背景图像。
- **实时数据**：从 Open-Meteo 获取实时天气信息和7天天气预报。
- **广播用户界面**：将数据与背景图像整合成专业的电视广播布局。

## 使用方法

```bash
python3 {baseDir}/scripts/generate_infographic.py --address "10 Downing St, London" --lat 51.5033 --lon -0.1276 --output "out/london-weather.png"
```

## 环境要求
- `GEMINI_API_KEY`：生成图像所需的关键参数。