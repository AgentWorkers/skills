---
name: veo-video-generator
description: 使用 Google Veo 3.1 生成高保真度的 1080p 视频，并实现音频与视频的同步。该工具适用于根据文本描述制作电影风格的视频片段。
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

使用谷歌先进的 Veo 3.1 模型生成包含原生音频的短视频片段。

## 使用说明

1. **触发方式**：当用户需要创建或渲染视频时，激活该功能。
2. **设置**：在首次执行之前，代理程序必须运行 `npm install` 以获取所需的依赖项。
3. **执行方式**：通过将用户输入的提示作为单独的参数传递来调用脚本，**切勿将其插入到 shell 命令字符串中**。建议使用参数数组或 `execFile` 方式进行调用，以避免 shell 解析用户输入的内容。示例（Node.js 风格的伪代码）：

   ```javascript
   execFile('node', ['generate.js', '--prompt', userPrompt])
   ```

   **请勿** 将命令构建为单个连接的字符串，例如 `"node generate.js --prompt " + userPrompt"`。

4. **输出格式**：默认输出分辨率为 1080p 的 9:16 宽高比视频。
5. **完成结果**：将生成的 .mp4 文件路径提供给用户。

## 安全性与隐私保护

- **防止 Shell 注入**：用户输入的提示必须作为独立的参数传递（例如通过 `execFile` 或 `argv` 数组），**严禁将其插入到 shell 命令字符串中**。将用户输入直接连接到 shell 命令中（例如使用模板字符串 `shell: true`）可能会导致 Shell 注入攻击，这是严格禁止的。
- **功能范围**：该功能仅向 Google GenAI API 发送文本提示。
- **环境依赖**：该工具使用 OpenClaw 环境提供的 `GEMINI_API_KEY`。
- **数据访问**：该工具不会读取本地文件或 `.env` 文件，所有配置均由代理程序处理。