---
name: ai-social-media-content
description: |
  Create AI-powered social media content for TikTok, Instagram, YouTube, Twitter/X.
  Generate: images, videos, reels, shorts, thumbnails, captions, hashtags.
  Tools: FLUX, Veo, Seedance, Wan, Kokoro TTS, Claude for copywriting.
  Use for: content creators, social media managers, influencers, brands.
  Triggers: social media content, tiktok, instagram reels, youtube shorts, twitter post,
  content creator, ai influencer, social content, reels, shorts, viral content,
  thumbnail generator, caption generator, hashtag generator, ugc content
allowed-tools: Bash(infsh *)
---

# AI社交媒体内容生成

通过 [inference.sh](https://inference.sh) 命令行工具，为所有平台生成社交媒体内容。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a TikTok-style video
infsh app run google/veo-3-1-fast --input '{
  "prompt": "POV walking through a neon-lit Tokyo street at night, vertical format 9:16, cinematic"
}'
```

## 平台格式

| 平台 | 长宽比 | 时长 | 分辨率 |
|----------|--------------|----------|------------|
| TikTok | 9:16（竖屏） | 15-60秒 | 1080x1920 |
| Instagram Reels | 9:16（竖屏） | 15-90秒 | 1080x1920 |
| Instagram Feed | 1:1 或 4:5 | - | 1080x1080 |
| YouTube Shorts | 9:16（竖屏） | <60秒 | 1080x1920 |
| YouTube 缩略图 | 16:9 | - | 1280x720 |
| Twitter/X | 16:9 或 1:1 | <140秒 | 1920x1080 |

## 内容工作流程

### TikTok / Reels 视频

```bash
# Generate trending-style content
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Satisfying slow motion video of paint being mixed, vibrant colors swirling together, vertical 9:16, ASMR aesthetic, viral TikTok style"
}'
```

### Instagram 旋转图（Carousel Images）

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

### Twitter/X 视觉帖子（Visual Post）

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

### 人物特写内容（Talking Head Content）

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

### 热门/病毒式风格（Trending/Viral Style）

```bash
infsh app run google/veo-3 --input '{
  "prompt": "Satisfying compilation style video, oddly satisfying content, smooth transitions, ASMR quality, vertical 9:16"
}'
```

### 教程/操作指南（Tutorial/How-To）

```bash
infsh app run google/veo-3-1 --input '{
  "prompt": "Hands demonstrating a craft tutorial, overhead shot, clean workspace, step-by-step motion, warm lighting, vertical format"
}'
```

### 产品展示（Product Showcase）

```bash
infsh app run bytedance/seedance-1-5-pro --input '{
  "prompt": "Product unboxing aesthetic, sleek packaging reveal, soft lighting, premium feel, satisfying unwrap, vertical 9:16"
}'
```

### 生活方式/美学风格（Lifestyle/Aesthetic）

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Day in my life aesthetic, morning routine montage, golden hour lighting, cozy apartment, coffee steam rising, vertical format"
}'
```

### 背景故事（Behind the Scenes）

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Behind the scenes of creative workspace, artist at work, authentic candid moments, documentary style, vertical 9:16"
}'
```

## 字幕与标签生成（Caption & Hashtag Generation）

```bash
# Generate engaging caption
infsh app run openrouter/claude-haiku-45 --input '{
  "prompt": "Write an engaging Instagram caption for a sunset beach photo. Include a hook, value, and call to action. Add 10 relevant hashtags."
}'
```

### 吸引观众的内容公式（Hook Formulas）

```bash
infsh app run openrouter/claude-haiku-45 --input '{
  "prompt": "Generate 5 viral TikTok hooks for a video about morning routines. Use proven patterns like: curiosity gap, bold claim, relatable struggle, before/after, or tutorial format."
}'
```

## 多平台内容复用（Multi-Platform Repurposing）

### 从长内容到短内容的转换流程（Long to Short Pipeline）

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

## 批量内容创建（Batch Content Creation）

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

1. **在开头3秒内吸引观众** – 从最吸引人的部分开始。
2. **优先使用竖屏格式** – TikTok、Reels、YouTube Shorts均采用9:16格式。
3. **保持视觉风格一致** – 与品牌颜色和风格相匹配。
4. **预留文本显示区域** – 为平台用户界面元素留出空间。
5. **使用热门音频** – 单独添加流行音效。
6. **批量生成内容** – 一次生成多个作品。

## 平台特定提示

### TikTok
- 快速切换镜头，使用热门音效。
- 重要信息需通过文字叠加显示。
- 立即吸引观众注意力。

### Instagram
- 保证高质量的视频视觉效果。
- 使用旋转图来提高互动性。
- 保持视觉风格的统一性。

### YouTube Shorts
- 清晰传达产品价值。
- 添加订阅按钮以促进用户互动。
- 可将较长内容重新剪辑为短视频使用。

### Twitter/X
- 使用一张引人注目的图片。
- 有争议性的内容更容易吸引观众。
- 可通过多条帖子构建话题讨论。

## 相关技能

```bash
# Video generation
npx skills add inference-sh/agent-skills@ai-video-generation

# Image generation
npx skills add inference-sh/agent-skills@ai-image-generation

# Twitter automation
npx skills add inference-sh/agent-skills@twitter-automation

# Text-to-speech for voiceovers
npx skills add inference-sh/agent-skills@text-to-speech

# Full platform skill
npx skills add inference-sh/agent-skills@inference-sh
```

浏览所有可用工具：`infsh app list`