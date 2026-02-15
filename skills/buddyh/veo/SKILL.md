---
name: veo
description: 使用 Google Veo（Veo 3.1 / Veo 3.0）生成视频。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires":
          {
            "env": { "GEMINI_API_KEY": "" },
            "bins": ["uv"],
          },
      },
  }
---

# Veo（Google 视频生成）

使用 Google 的 Veo API 生成视频片段。

**生成视频**  
```bash
uv run {baseDir}/scripts/generate_video.py --prompt "your video description" --filename "output.mp4"
```

**可选参数**  
- `--duration` / `-d`：视频时长（以秒为单位，默认值：8 秒，具体时长取决于所使用的模型）  
- `--aspect-ratio` / `-a`：宽高比（16:9、9:16、1:1）  
- `--model`：要使用的 Veo 模型（例如：veo-2.0-generate-001、veo-3.0-generate-001、veo-3.1-generate-preview 等）  

**API 密钥**  
- 推荐使用环境变量 `GEMINI_API_KEY`  
- 或者在 `~/.clawdbot/clawdbot.json` 文件中设置 `skills."veo".env.GEMINI_API_KEY`  

**注意事项**  
- Veo 3.1 支持更高的视频质量和更长的时长  
- 输出格式为 MP4  
- 使用 `--model veo-3.1-generate-preview` 可获得最佳效果  
- `veo-3.0-fast-generate-001` 生成速度更快，但视频质量较低  
- 脚本会输出 `MEDIA:` 行，以便 Clawdbot 在支持的聊天平台上自动嵌入视频。