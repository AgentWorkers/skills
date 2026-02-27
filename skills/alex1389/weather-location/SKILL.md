---
name: Weather&Webcam
description: 从 wttr.in 获取当前天气信息，并自动从 Meteoblue 或 Windy 获取所请求位置的实时网络摄像头图像。当用户询问天气状况并希望查看当前天气的实时图像时，可以使用此功能。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["agent-browser", "curl"] },
      },
  }
---
# 天气信息与网络摄像头图像获取

该技能利用 **agent-browser** 自动获取天气数据并实时捕获网络摄像头图像，确保图像质量达到最佳。

## 工作流程

1. **获取天气信息（wttr.in）**：
   - 执行命令 `curl -s "wttr.in/[地点]?format=%l:+%c+%t+%h+%w"` 以获取基本天气信息。
   - 注意：需要对地址中的空格进行编码（例如，`Sant+Adria+de+Besos`）。

2. **搜索网络摄像头**：
   - 在网上搜索 `site:meteoblue.com [地点] webcam` 或 `site:windy.com [地点] webcam`。
   - 选择目标地点的网络摄像头页面的直接链接。

3. **捕获图像（使用 agent-browser）**：
   - 使用 **agent-browser** 进行页面导航和交互：
      ```bash
      /home/user/.npm-global/bin/agent-browser --session-name webcam open "[URL]"
      ```
   - **交互步骤**：
     - 使用 `snapshot` 和 `click @ref` 点击显示cookie的按钮（“OK/Accept”）。
     - 点击特定地点的链接以查看高清图像或图库。
   - **提取图像链接**：
     - 使用 `eval` 函数提取最高分辨率的图像链接（通常包含 `/full/` 和 `original.jpg`）：
        ```javascript
        Array.from(document.querySelectorAll('img')).map(img => img.src).filter(src => src.includes('original.jpg') && src.includes('/full/'))[0]
        ```
   - **下载图像**：
     - 使用 `curl` 将图像下载到 `/home/user/.openclaw/workspace/webcam.jpg` 文件夹中。

4. **用户响应**：
   - 使用 `message(action=send, media="/home/user/.openclaw/workspace/webcam.jpg", caption="[wttr.in 数据]\n[评论]")` 发送图像和天气信息。
   - 用户也可以选择回复 `NO_REPLY` 表示不需要进一步操作。

## 优化措施（节省资源）

- **agent-browser**：这是首选方法，可确保有效的用户交互（通过设置cookie）和高质量的图像获取。
- **会话持久化**：使用 `--session-name webcam` 选项来保存用户会话信息（包括cookie）。
- **备用方案**：仅在 **agent-browser** 失败时使用其他方法（如网络爬虫）。

## 使用示例

- “伦敦的天气怎么样？”
- “显示巴塞罗那的网络摄像头图像。”
- “维拉萨德马尔的天空情况如何？”