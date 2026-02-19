---
name: ai-content-pipeline
description: "构建结合图像、视频、音频和文本的多步骤AI内容创作流程。工作流程示例包括：生成图像 -> 添加动画效果 -> 添加旁白 -> 与音乐合成。使用的工具包括：FLUX、Veo、Kokoro TTS、OmniHuman、媒体合并工具以及图像质量提升工具。应用场景包括：YouTube视频、社交媒体内容、营销材料以及自动化内容生成。相关概念包括：内容创作流程（content pipeline）、AI工作流程（AI workflow）、多步骤AI技术（multi-step AI）、内容自动化（content automation）、AI视频制作流程（AI video workflow）、AI内容工厂（AI content factory）等。"
allowed-tools: Bash(infsh *)
---
# 人工智能内容管道

通过 [inference.sh](https://inference.sh) 命令行界面（CLI）构建多步骤的内容创作管道。

![人工智能内容管道](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg06qgcg105rh6y1kvxm4wvm.png)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Simple pipeline: Generate image -> Animate to video
infsh app run falai/flux-dev --input '{"prompt": "portrait of a woman smiling"}' > image.json
infsh app run falai/wan-2-5 --input '{"image_url": "<url-from-previous>"}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或启动后台进程。也可以选择[手动安装与验证](https://dist.inference.sh/cli/checksums.txt)。

## 管道模式

### 模式 1：图片 -> 视频 -> 音频

```
[FLUX Image] -> [Wan 2.5 Video] -> [Foley Sound]
```

### 模式 2：脚本 -> 语音 -> 阿凡达

```
[LLM Script] -> [Kokoro TTS] -> [OmniHuman Avatar]
```

### 模式 3：研究 -> 内容 -> 分发

```
[Tavily Search] -> [Claude Summary] -> [FLUX Visual] -> [Twitter Post]
```

## 完整工作流程

### YouTube 短视频管道

根据指定主题创建一个完整的短视频。

```bash
# 1. Generate script with Claude
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "Write a 30-second script about the future of AI. Make it engaging and conversational. Just the script, no stage directions."
}' > script.json

# 2. Generate voiceover with Kokoro
infsh app run infsh/kokoro-tts --input '{
  "text": "<script-text>",
  "voice": "af_sarah"
}' > voice.json

# 3. Generate background image with FLUX
infsh app run falai/flux-dev --input '{
  "prompt": "Futuristic city skyline at sunset, cyberpunk aesthetic, 4K wallpaper"
}' > background.json

# 4. Animate image to video with Wan
infsh app run falai/wan-2-5 --input '{
  "image_url": "<background-url>",
  "prompt": "slow camera pan across cityscape, subtle movement"
}' > video.json

# 5. Add captions (manually or with another tool)

# 6. Merge video with audio
infsh app run infsh/media-merger --input '{
  "video_url": "<video-url>",
  "audio_url": "<voice-url>"
}'
```

### 语音播报视频管道

创建一个能够播报内容的人工智能阿凡达。

```bash
# 1. Write the script
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "Write a 1-minute explainer script about quantum computing for beginners."
}' > script.json

# 2. Generate speech
infsh app run infsh/kokoro-tts --input '{
  "text": "<script>",
  "voice": "am_michael"
}' > speech.json

# 3. Generate or use a portrait image
infsh app run falai/flux-dev --input '{
  "prompt": "Professional headshot of a friendly tech presenter, neutral background, looking at camera"
}' > portrait.json

# 4. Create talking head video
infsh app run bytedance/omnihuman-1-5 --input '{
  "image_url": "<portrait-url>",
  "audio_url": "<speech-url>"
}' > talking_head.json
```

### 产品演示管道

创建一个产品展示视频。

```bash
# 1. Generate product image
infsh app run falai/flux-dev --input '{
  "prompt": "Sleek wireless earbuds on white surface, studio lighting, product photography"
}' > product.json

# 2. Animate product reveal
infsh app run falai/wan-2-5 --input '{
  "image_url": "<product-url>",
  "prompt": "slow 360 rotation, smooth motion"
}' > product_video.json

# 3. Upscale video quality
infsh app run falai/topaz-video-upscaler --input '{
  "video_url": "<product-video-url>"
}' > upscaled.json

# 4. Add background music
infsh app run infsh/media-merger --input '{
  "video_url": "<upscaled-url>",
  "audio_url": "https://your-music.mp3",
  "audio_volume": 0.3
}'
```

### 博文转视频管道

将文本内容转换为视频格式。

```bash
# 1. Summarize blog post
infsh app run openrouter/claude-haiku-45 --input '{
  "prompt": "Summarize this blog post into 5 key points for a video script: <blog-content>"
}' > summary.json

# 2. Generate images for each point
for i in 1 2 3 4 5; do
  infsh app run falai/flux-dev --input "{
    \"prompt\": \"Visual representing point $i: <point-text>\"
  }" > "image_$i.json"
done

# 3. Animate each image
for i in 1 2 3 4 5; do
  infsh app run falai/wan-2-5 --input "{
    \"image_url\": \"<image-$i-url>\"
  }" > "video_$i.json"
done

# 4. Generate voiceover
infsh app run infsh/kokoro-tts --input '{
  "text": "<full-script>",
  "voice": "bf_emma"
}' > narration.json

# 5. Merge all clips
infsh app run infsh/media-merger --input '{
  "videos": ["<video1>", "<video2>", "<video3>", "<video4>", "<video5>"],
  "audio_url": "<narration-url>",
  "transition": "crossfade"
}'
```

## 管道构建模块

### 内容生成

| 步骤 | 应用程序 | 功能 |
|------|-----|---------|
| 脚本 | `openrouter/claude-sonnet-45` | 生成文本内容 |
| 研究 | `tavily/search-assistant` | 收集相关信息 |
| 摘要 | `openrouter/claude-haiku-45` | 提取内容要点 |

### 视觉素材

| 步骤 | 应用程序 | 功能 |
|------|-----|---------|
| 图片 | `falai/flux-dev` | 生成图片 |
| 图片 | `google/imagen-3` | 替代图片生成工具 |
| 图像缩放 | `falai/topaz-image-upscaler` | 提升图片质量 |

### 动画

| 步骤 | 应用程序 | 功能 |
|------|-----|---------|
| I2V | `falai/wan-2-5` | 图片动画化 |
| T2V | `google/veo-3-1-fast` | 从文本生成动画 |
| 阿凡达 | `bytedance/omnihuman-1-5` | 生成语音播报的阿凡达 |

### 音频

| 步骤 | 应用程序 | 功能 |
|------|-----|---------|
| 文本转语音 (TTS) | `infsh/kokoro-tts` | 为内容添加语音解说 |
| 音乐 | `infsh/ai-music` | 背景音乐 |
| 音效 | `infsh/hunyuanvideo-foley` | 添加音效 |

### 后期制作

| 步骤 | 应用程序 | 功能 |
|------|-----|---------|
| 视频缩放 | `falai/topaz-video-upscaler` | 提升视频质量 |
| 媒体合并 | `infsh/media-merger` | 合并多种媒体文件 |
| 字幕添加 | `infsh/caption-video` | 为视频添加字幕 |

## 最佳实践

1. **先规划管道** - 在运行之前明确每个步骤的流程。
2. **保存中间结果** - 存储中间输出以便后续修改。
3. **选择合适的质量设置** - 草稿阶段使用快速模型，最终版本使用高质量模型。
4. **保持分辨率一致** - 确保整个流程中的画面比例一致。
5. **测试每个步骤** - 在继续下一步之前验证输出结果。

## 相关技能

```bash
# Video generation models
npx skills add inference-sh/skills@ai-video-generation

# Image generation
npx skills add inference-sh/skills@ai-image-generation

# Text-to-speech
npx skills add inference-sh/skills@text-to-speech

# LLM models for scripts
npx skills add inference-sh/skills@llm-models

# Full platform skill
npx skills add inference-sh/skills@inference-sh
```

浏览所有可用应用程序：`infsh app list`

## 文档资料

- [内容管道示例](https://inference.sh/docs/examples/content-pipeline) - 官方管道指南
- [工作流程构建](https://inference.sh/blog/guides/ai-workflows) - 工作流程最佳实践指南