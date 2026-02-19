---
name: veo-video-generator
description: 使用 Google Veo 3.1 生成高保真度的 1080p 视频，并实现音频与视频的同步。该工具可用于将文本描述转换为具有视觉效果的影片片段。
metadata:
  clawdbot:
    emoji: "🎬"
    requires:
      env: ["GEMINI_API_KEY"]
      bins: ["node", "npm"]
    install: "npm install"
    primaryEnv: "GEMINI_API_KEY"
    category: "Video & Media"
---
# Veo 视频生成器  
使用 Google 最先进的 Veo 3.1 模型生成带有原生音频的短视频片段。  

## 使用说明  
1. **触发方式**：当用户需要创建或渲染视频时，激活该功能。  
2. **设置**：在首次执行前，代理程序必须运行 `npm install` 以获取所需依赖项。  
3. **执行方式**：运行 `node generate.js --prompt "<user_prompt>"`  
4. **输出格式**：默认生成分辨率为 1080p、宽高比为 9:16 的视频文件（.mp4 格式）。  
5. **完成方式**：将生成的视频文件（.mp4 格式）的路径提供给用户。  

## 安全性与隐私保护  
- **功能范围**：该功能仅向 Google GenAI API 发送文本请求。  
- **环境依赖**：使用 OpenClaw 环境提供的 `GEMINI_API_KEY`。  
- **数据访问**：不会读取本地文件或 `.env` 文件；所有配置均由代理程序处理。