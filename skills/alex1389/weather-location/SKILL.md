---
name: Weather&Webcam
description: 从 wttr.in 获取当前天气信息，并自动从 Meteoblue 或 Windy 获取请求位置的实时网络摄像头图像。当用户查询天气并希望查看当前天气状况的实时图像时，可以使用此功能。
---
# 天气信息获取与实时网络摄像头图像显示功能

该功能可自动获取天气数据并捕捉实时网络摄像头图像，从而提供完整的视觉信息。

## 工作流程

1. **获取天气信息（wttr.in）**：
   - 执行命令 `curl -s "wttr.in/[地点]?format=%l:+%c+%t+%h+%w"` 以获取基本天气信息（地点、图标、温度、湿度和风速）。
   - 注意：在 URL 中需要正确编码空格（例如：`Sant+Adria+de+Besos`）。

2. **搜索网络摄像头（Meteoblue/Windy）**：
   - 在浏览器中搜索 `meteoblue [地点] webcam` 或 `windy [地点] webcam`。
   - 选择显示该地区网络摄像头信息的 Meteoblue 链接（例如：`meteoblue.com/.../webcams/...`）。

3. **获取图像（推荐方法）**：
   - 访问该页面，使用 `browser(action=snapshot)` 找到直接获取图像的 URL（例如：`imgproxy.windy.com/...`）。
   - **重要提示**：避免使用 `browser(action=screenshot)`，以防生成重复的图像（预览图）。
   - 使用命令 `exec(command="curl -s '[URL]' -o /tmp/webcam.jpg")` 下载图像。
   - 如果可能的话，优先选择 16:9 比例的图像。

4. **用户反馈**：
   - 使用 `message(action=send, media="/tmp/webcam.jpg", caption="[wttr.in 数据]\n[评论]")` 发送图像。
   - 使用 `message` 工具后，在主会话中回复 `NO_REPLY` 以表示操作完成。

## 使用示例

- “伦敦的天气怎么样？”
- “纽约现在的天空状况如何？”
- “显示巴塞罗那的天气情况。”