---
name: ai-social-media-content
description: "**生成适用于 TikTok、Instagram、YouTube 和 Twitter 的 AI 驱动型社交媒体内容**  
- **内容类型**：图片、视频、Reels（TikTok 功能）、Shorts（YouTube 功能）、缩略图、标题文字、标签  
- **工具**：FLUX、Veo、Seedance、Wan、Kokoro TTS、Claude（用于文案创作）  
- **适用对象**：内容创作者、社交媒体经理、影响者、品牌  
- **应用场景**：社交媒体内容生成、TikTok 视频制作、Instagram Reels 制作、YouTube Shorts 制作、Twitter 发文  
**功能说明：**  
该工具能够利用 AI 技术自动生成高质量的社交媒体内容，包括图片、视频、Reels 和 Shorts，以及相应的缩略图和标题文字。具体流程如下：  
1. 使用 FLUX 或其他工具设计内容框架；  
2. 利用 Veo 或 Wan 生成高质量的图片和视频素材；  
3. 通过 Kokoro TTS 为内容添加自然语言的旁白；  
4. 借助 Claude 生成吸引人的文案；  
5. 生成适合不同平台的标签（如 #TikTokVideo、#InstagramReels、#YouTubeShorts 等）；  
6. 所生成的内容可用于内容创作者、社交媒体经理和影响者的日常创作，帮助提升内容的吸引力和传播效果。  
**适用场景示例：**  
- **内容创作者**：利用这些工具快速制作原创内容，节省时间并提高效率；  
- **社交媒体经理**：批量生成符合平台规范的内容，提升平台活跃度；  
- **影响者**：借助 AI 助手提升内容质量，吸引更多粉丝；  
- **品牌**：通过自动化内容生成提升品牌影响力。"
allowed-tools: Bash(infsh *)
---
# AI社交媒体内容生成

您可以通过 [inference.sh](https://inference.sh) 命令行工具为所有平台生成社交媒体内容。

![AI社交媒体内容示例](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg2c0egyg243mnyth4y6g51q.jpeg)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a TikTok-style video
infsh app run google/veo-3-1-fast --input '{
  "prompt": "POV walking through a neon-lit Tokyo street at night, vertical format 9:16, cinematic"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可通过 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt) 进行操作。

## 平台格式

| 平台 | 长宽比 | 时长 | 分辨率 |
|----------|--------------|----------|------------|
| TikTok | 9:16（竖屏） | 15-60秒 | 1080x1920 |
| Instagram Reels | 9:16（竖屏） | 15-90秒 | 1080x1920 |
| Instagram Feed | 1:1 或 4:5 | - | 1080x1080 |
| YouTube Shorts | 9:16（竖屏） | <60秒 | 1080x1920 |
| YouTube 缩略图 | 16:9 | - | 1280x720 |
| Twitter/X | 16:9 或 1:1 | <140秒 | 1920x1080 |

## 内容制作流程

### TikTok/Reels 视频

```bash
# Generate trending-style content
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Satisfying slow motion video of paint being mixed, vibrant colors swirling together, vertical 9:16, ASMR aesthetic, viral TikTok style"
}'
```

### Instagram 旋转图

```bash
# Generate cohesive carousel images
for i in 1 2 3 4 5; do
  infsh app run falai/flux-dev --input "{
    \"prompt\": \"Minimalist lifestyle flat lay photo $i/5, morning coffee routine, neutral tones, Instagram aesthetic, consistent style\"
  }" > "carousel_$i.json"
done
```

### YouTube 缩略图

```bash
# Eye-catching thumbnail
infsh app run falai/flux-dev --input '{
  "prompt": "YouTube thumbnail, shocked face emoji, bright yellow background, bold text area on right, attention-grabbing, high contrast, professional"
}'
```

### Twitter/X 视觉帖子

```bash
# Generate image for tweet
infsh app run falai/flux-dev --input '{
  "prompt": "Tech infographic style image showing AI trends, modern design, data visualization aesthetic, shareable"
}'

# Post with Twitter automation
infsh app run twitter/post-tweet --input '{
  "text": "The future of AI is here. Here are the top 5 trends reshaping tech in 2024 🧵",
  "media_url": "<image-url>"
}'
```

### 人物特写内容

```bash
# 1. Write script with Claude
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "Write a 30-second engaging script about productivity tips for a TikTok. Conversational, hook in first 3 seconds."
}' > script.json

# 2. Generate voiceover
infsh app run infsh/kokoro-tts --input '{
  "text": "<script>",
  "voice": "af_sarah"
}' > voice.json

# 3. Create AI avatar
infsh app run bytedance/omnihuman-1-5 --input '{
  "image_url": "https://your-avatar.jpg",
  "audio_url": "<voice-url>"
}'
```

## 内容类型模板

### 热门/病毒式风格

```bash
infsh app run google/veo-3 --input '{
  "prompt": "Satisfying compilation style video, oddly satisfying content, smooth transitions, ASMR quality, vertical 9:16"
}'
```

### 教程/操作指南

```bash
infsh app run google/veo-3-1 --input '{
  "prompt": "Hands demonstrating a craft tutorial, overhead shot, clean workspace, step-by-step motion, warm lighting, vertical format"
}'
```

### 产品展示

```bash
infsh app run bytedance/seedance-1-5-pro --input '{
  "prompt": "Product unboxing aesthetic, sleek packaging reveal, soft lighting, premium feel, satisfying unwrap, vertical 9:16"
}'
```

### 生活方式/美学风格

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Day in my life aesthetic, morning routine montage, golden hour lighting, cozy apartment, coffee steam rising, vertical format"
}'
```

### 背景故事

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Behind the scenes of creative workspace, artist at work, authentic candid moments, documentary style, vertical 9:16"
}'
```

## 字幕与标签生成

```bash
# Generate engaging caption
infsh app run openrouter/claude-haiku-45 --input '{
  "prompt": "Write an engaging Instagram caption for a sunset beach photo. Include a hook, value, and call to action. Add 10 relevant hashtags."
}'
```

### 吸引观众的内容公式

```bash
infsh app run openrouter/claude-haiku-45 --input '{
  "prompt": "Generate 5 viral TikTok hooks for a video about morning routines. Use proven patterns like: curiosity gap, bold claim, relatable struggle, before/after, or tutorial format."
}'
```

## 多平台内容复用

### 从长内容到短视频的转换流程

```bash
# Take a concept and create multiple formats
CONCEPT="productivity hack: 2-minute rule"

# TikTok vertical
infsh app run google/veo-3-1-fast --input "{
  \"prompt\": \"$CONCEPT visualization, vertical 9:16, quick cuts, text overlays style\"
}"

# Twitter square
infsh app run falai/flux-dev --input "{
  \"prompt\": \"$CONCEPT infographic, square format, minimal design, shareable\"
}"

# YouTube thumbnail
infsh app run falai/flux-dev --input "{
  \"prompt\": \"$CONCEPT thumbnail, surprised person, bold text space, 16:9\"
}"
```

## 批量内容生成

```bash
# Generate a week of content
TOPICS=("morning routine" "productivity tips" "coffee aesthetic" "workspace tour" "night routine")

for topic in "${TOPICS[@]}"; do
  infsh app run google/veo-3-1-fast --input "{
    \"prompt\": \"$topic content for social media, aesthetic, vertical 9:16, engaging\"
  }" > "content_${topic// /_}.json"
done
```

## 最佳实践

1. **抓住前3秒的注意力** - 从最吸引人的部分开始。
2. **优先使用竖屏格式** - TikTok、Reels、YouTube Shorts 都适用。
3. **保持视觉风格一致** - 与品牌颜色和风格相匹配。
4. **预留文本显示区域** - 为平台的用户界面元素留出空间。
5. **使用热门背景音乐** - 可单独添加流行的音乐片段。
6. **批量生成** - 一次生成多条内容。

## 平台特定提示

### TikTok
- 快速切换镜头，使用热门背景音乐。
- 文字要突出显示。
- 立即吸引观众的注意力。

### Instagram
- 保证高质量的视频画质。
- 使用旋转图来提高互动性。
- 保持视觉风格的一致性。

### YouTube Shorts
- 清晰地传达产品价值。
- 使用订阅按钮来引导用户行动。
- 可以复用较长的视频内容。

### Twitter/X
- 使用一张引人注目的图片。
- 使用具有争议性的内容来吸引观众。
- 可以通过多条帖子形成连贯的故事线。

## 相关技能

```bash
# Video generation
npx skills add inference-sh/skills@ai-video-generation

# Image generation
npx skills add inference-sh/skills@ai-image-generation

# Twitter automation
npx skills add inference-sh/skills@twitter-automation

# Text-to-speech for voiceovers
npx skills add inference-sh/skills@text-to-speech

# Full platform skill
npx skills add inference-sh/skills@inference-sh
```

查看所有可用工具：`infsh app list`