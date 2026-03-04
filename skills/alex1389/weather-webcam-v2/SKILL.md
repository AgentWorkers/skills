---
name: Weather&Webcam
description: 从 Open-Meteo API 获取当前天气信息，并自动从 Meteoblue 或 Windy 获取指定位置的实时网络摄像头图像。当用户询问天气情况并希望查看当前天气状况的实时图像时，可以使用该功能。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["agent-browser", "curl"] },
      },
  }
---
# 天气信息获取

该技能通过 Open-Meteo 获取天气数据，并使用 **agent-browser** 功能捕获实时的网络摄像头图像。

## 工作流程

1. **获取坐标（地理编码）**：
   - 执行 `curl -s "https://geocoding-api.open-meteo.com/v1/search?name=[地点]&count=1&language=es&format=json"`，将地点名称转换为坐标。

2. **获取天气信息（Open-Meteo）**：
   - 执行 `curl -s "https://api.open-meteo.com/v1/forecast?latitude=[纬度]&longitude=[经度]&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"`，以获取实时天气数据。

3. **搜索网络摄像头**：
   - 在网上搜索 `site:meteoblue.com [地点] webcam` 或 `site:windy.com [地点] webcam`，找到该地点的网络摄像头页面的直接链接。

4. **捕获图像（使用 Agent Browser 方法）**：
   - 使用 **agent-browser** 进行导航和操作：
      ```bash
      /home/user/.npm-global/bin/agent-browser --session-name webcam open "[URL]"
      ```
   - **操作步骤**：
     - 使用 `snapshot` 和 `click @ref` 点击 cookie 广告。
     - **提取信息**：
       - 使用 `eval` 找到最高分辨率的图像链接（通常包含 `/full/` 和 `original.jpg`）：
         ```javascript
        Array.from(document.querySelectorAll('img')).map(img => img.src).filter(src => src.includes('original.jpg') && src.includes('/full/'))[0]
        ```
   - **下载图像**：
     - 使用 `curl` 将图像下载到 `/home/user/.openclaw/workspace/webcam.jpg`。

5. **用户反馈**：
   - 向用户发送消息：`message(action=send, media="/home/user/.openclaw/workspace/webcam.jpg", caption="[城市]: [图标] [温度]°C [湿度]% [风速]km/h\n[评论]")`。
   - 用户也可以选择回复 `NO_REPLY`。

## 优化措施（节省资源）

- **Open-Meteo API**：比 wttr.in 更快速、无需注册账号，且更可靠。
- **Agent Browser**：是获取交互数据（如 cookie）和高质量图像的首选方法。
- **会话持久化**：使用 `--session-name webcam` 选项来保存会话信息（包括 cookie）。