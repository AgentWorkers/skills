---
name: ai-content-pipeline
description: |
  Build multi-step AI content creation pipelines combining image, video, audio, and text.
  Workflow examples: generate image -> animate -> add voiceover -> merge with music.
  Tools: FLUX, Veo, Kokoro TTS, OmniHuman, media merger, upscaling.
  Use for: YouTube videos, social media content, marketing materials, automated content.
  Triggers: content pipeline, ai workflow, content creation, multi-step ai,
  content automation, ai video workflow, generate and edit, ai content factory,
  automated content creation, ai production pipeline, media pipeline, content at scale
allowed-tools: Bash(infsh *)
---

# 人工智能内容制作流程

![人工智能内容制作流程](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg06qgcg105rh6y1kvxm4wvm.png)

通过 [inference.sh](https://inference.sh) 命令行界面（CLI）构建多步骤的内容制作流程。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Simple pipeline: Generate image -> Animate to video
infsh app run falai/flux-dev --input '{"prompt": "portrait of a woman smiling"}' > image.json
infsh app run falai/wan-2-5 --input '{"image_url": "<url-from-previous>"}'
```

## 流程模式

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

### YouTube 短视频制作流程

根据指定主题制作一个完整的短视频。

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

### 语音播报视频流程

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

### 产品演示流程

制作产品展示视频。

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

### 博文转视频流程

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

## 流程构建模块

### 内容生成

| 步骤 | 应用程序 | 用途 |
|------|-----|---------|
| 脚本 | `openrouter/claude-sonnet-45` | 编写内容 |
| 研究 | `tavily/search-assistant` | 收集信息 |
| 摘要 | `openrouter/claude-haiku-45` | 提炼内容 |

### 视觉素材

| 步骤 | 应用程序 | 用途 |
|------|-----|---------|
| 图片 | `falai/flux-dev` | 生成图片 |
| 图片 | `google/imagen-3` | 替代图片生成工具 |
| 图像放大 | `falai/topaz-image-upscaler` | 提升图片质量 |

### 动画制作

| 步骤 | 应用程序 | 用途 |
|------|-----|---------|
| I2V | `falai/wan-2-5` | 图片动画化 |
| T2V | `google/veo-3-1-fast` | 从文本生成动画 |
| 阿凡达 | `bytedance/omnihuman-1-5` | 生成语音播报的阿凡达 |

### 音频处理

| 步骤 | 应用程序 | 用途 |
|------|-----|---------|
| 文本转语音 | `infsh/kokoro-tts` | 语音合成 |
| 音乐 | `infsh/ai-music` | 背景音乐 |
| 音效 | `infsh/hunyuanvideo-foley` | 音效制作 |

### 后期制作

| 步骤 | 应用程序 | 用途 |
|------|-----|---------|
| 视频放大 | `falai/topaz-video-upscaler` | 提升视频质量 |
| 媒体合并 | `infsh/media-merger` | 合并多种媒体文件 |
| 字幕添加 | `infsh/caption-video` | 添加字幕 |

## 最佳实践

1. **先规划流程** - 在开始之前明确每个步骤的具体内容。
2. **保存中间结果** - 将输出结果保存以便后续迭代。
3. **选择合适的质量设置** - 草稿阶段使用快速模型，最终成品使用高质量模型。
4. **保持分辨率一致** - 确保整个流程中的画面比例一致。
5. **测试每个步骤** - 在继续下一步之前验证输出结果。

## 相关技能

```bash
# Video generation models
npx skills add inferencesh/skills@ai-video-generation

# Image generation
npx skills add inferencesh/skills@ai-image-generation

# Text-to-speech
npx skills add inferencesh/skills@text-to-speech

# LLM models for scripts
npx skills add inferencesh/skills@llm-models

# Full platform skill
npx skills add inferencesh/skills@inference-sh
```

浏览所有可用应用程序：`infsh app list`

## 文档资料

- [内容制作流程示例](https://inference.sh/docs/examples/content-pipeline) - 官方流程指南
- [工作流程构建指南](https://inference.sh/blog/guides/ai-workflows) - 工作流程最佳实践