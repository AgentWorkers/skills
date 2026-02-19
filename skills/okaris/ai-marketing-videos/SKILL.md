---
name: ai-marketing-videos
description: "**创建用于广告、宣传、产品发布和品牌内容的AI营销视频**  
**使用的工具及平台：**  
- **视觉效果制作工具：** Veo、Seedance、Wan、FLUX  
- **旁白制作工具：** Kokoro  
**视频类型：**  
  - 产品演示视频  
  - 用户评价视频  
  - 说明视频  
  - 社交媒体广告  
  - 品牌宣传视频  
**适用场景：**  
- Facebook广告  
- YouTube广告  
- 产品发布活动  
- 品牌推广  
**触发条件（即视频使用的场景）：**  
- 营销视频  
- 广告视频  
- 宣传视频  
- 商业广告  
- 品牌视频  
- 产品介绍视频  
- 视频广告  
- Facebook广告视频  
- YouTube广告  
- Instagram广告  
- TikTok广告  
- 宣传视频  
- 产品发布视频"
allowed-tools: Bash(infsh *)
---
# AI营销视频

您可以通过 [inference.sh](https://inference.sh) 命令行工具来制作专业的营销视频。

![AI营销视频示例](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg2c0egyg243mnyth4y6g51q.jpeg)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a product promo video
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Sleek product reveal video, smartphone emerging from light particles, premium tech aesthetic, commercial quality"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择[手动安装及验证](https://dist.inference.sh/cli/checksums.txt)。

## 视频广告类型

| 类型 | 时长 | 平台 |
|------|----------|----------|
| 开场广告 | 6 秒 | YouTube |
| 短广告 | 15 秒 | Instagram、Facebook |
| 标准广告 | 30 秒 | YouTube、电视 |
| 说明视频 | 60-90 秒 | 网站、YouTube |
| 产品演示 | 30-60 秒 | 所有平台 |

## 营销视频模板

### 产品发布

```bash
# Dramatic product reveal
infsh app run google/veo-3 --input '{
  "prompt": "Cinematic product launch video, premium tech device floating in space, dramatic lighting, particles and light effects, Apple-style reveal, commercial quality"
}'
```

### 品牌故事

```bash
# Emotional brand narrative
infsh app run google/veo-3-1 --input '{
  "prompt": "Brand story video showing diverse people connecting through technology, warm color grading, lifestyle montage, emotional and inspiring, commercial"
}'
```

### 功能亮点

```bash
# Focus on specific feature
infsh app run bytedance/seedance-1-5-pro --input '{
  "prompt": "Close-up product feature demonstration, hands interacting with device, clean background, informative, tech commercial style"
}'
```

### 用户评价

```bash
# Talking head testimonial
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Customer testimonial style video, person speaking to camera, neutral office background, professional lighting, authentic feel"
}'
```

### 使用前/使用后对比

```bash
# Transformation reveal
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Before and after transformation video, split screen transition, dramatic reveal, satisfying comparison, commercial style"
}'
```

## 完整的广告制作流程

### 30秒产品广告

```bash
# 1. Opening hook (0-3s)
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Attention-grabbing opening, product silhouette in dramatic lighting, building anticipation"
}' > hook.json

# 2. Problem statement (3-8s)
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Frustrated person dealing with common problem, relatable everyday situation, documentary style"
}' > problem.json

# 3. Solution reveal (8-15s)
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Product reveal with features highlighted, clean demonstration, solving the problem shown before"
}' > solution.json

# 4. Benefits showcase (15-25s)
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Happy customer using product, lifestyle integration, multiple quick cuts showing benefits"
}' > benefits.json

# 5. Call to action (25-30s)
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Product hero shot with space for text overlay, professional lighting, commercial ending"
}' > cta.json

# 6. Generate voiceover
infsh app run infsh/kokoro-tts --input '{
  "text": "Tired of [problem]? Introducing [Product]. [Key benefit 1]. [Key benefit 2]. [Key benefit 3]. Get yours today.",
  "voice": "af_nicole"
}' > voiceover.json

# 7. Merge all clips with voiceover
infsh app run infsh/media-merger --input '{
  "videos": ["<hook>", "<problem>", "<solution>", "<benefits>", "<cta>"],
  "audio_url": "<voiceover>",
  "transition": "crossfade"
}'
```

### Instagram/TikTok广告（15秒）

```bash
# Vertical format, fast-paced
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Fast-paced product showcase, vertical 9:16, quick cuts, trending style, hook in first 2 seconds, satisfying visually, Gen-Z aesthetic"
}'

# Add trendy music
infsh app run infsh/media-merger --input '{
  "video_url": "<video>",
  "audio_url": "https://trending-music.mp3"
}'
```

### 说明视频

```bash
# 1. Write script
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "Write a 60-second explainer video script for a SaaS product. Include: hook, problem, solution, 3 key features, social proof, CTA. Make it conversational."
}' > script.json

# 2. Generate visuals for each section
SECTIONS=("hook" "problem" "solution" "feature1" "feature2" "feature3" "social_proof" "cta")

for section in "${SECTIONS[@]}"; do
  infsh app run google/veo-3-1-fast --input "{
    \"prompt\": \"Explainer video scene for $section, motion graphics style, clean modern aesthetic, SaaS product\"
  }" > "$section.json"
done

# 3. Generate professional voiceover
infsh app run infsh/kokoro-tts --input '{
  "text": "<full-script>",
  "voice": "am_michael"
}' > voiceover.json

# 4. Assemble final video
infsh app run infsh/media-merger --input '{
  "videos": ["<hook>", "<problem>", "<solution>", ...],
  "audio_url": "<voiceover>",
  "transition": "fade"
}'
```

## 平台特定格式

### Facebook/Instagram动态

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Square format product video 1:1, eye-catching visuals, works without sound, text-friendly, scroll-stopping"
}'
```

### YouTube前置广告

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "YouTube ad style, skip button awareness (hook in 5 seconds), 16:9, professional commercial quality"
}'
```

### LinkedIn

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Professional B2B product video, corporate style, clean and modern, business audience, subtle motion"
}'
```

### TikTok/Reels

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "TikTok native style ad, vertical 9:16, raw authentic feel, not overly polished, trendy, user-generated content aesthetic"
}'
```

## 广告创意最佳实践

### 吸引观众注意力的方法（前3秒）

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Opening hook: [choose one]
  - Surprising visual transformation
  - Bold statement text animation
  - Relatable problem scenario
  - Curiosity gap visual
  - Satisfying action"
}'
```

### 视觉层次结构

1. **产品主角** - 清晰、突出显示
2. **产品优势** - 通过图片或图表展示，而不仅仅是文字说明
3. **用户评价** - 显示真实的用户反馈或数据
4. **行动号召** - 为文字或图片提供足够的空间

### 音频设计

```bash
# Add appropriate music
infsh app run infsh/ai-music --input '{
  "prompt": "Upbeat commercial background music, modern, energetic, 30 seconds"
}' > music.json

infsh app run infsh/media-merger --input '{
  "video_url": "<ad-video>",
  "audio_url": "<music>",
  "audio_volume": 0.5
}'
```

## A/B测试方案

```bash
# Generate multiple creative variants
HOOKS=(
  "Problem-focused opening"
  "Product reveal opening"
  "Testimonial opening"
  "Statistic opening"
)

for hook in "${HOOKS[@]}"; do
  infsh app run google/veo-3-1-fast --input "{
    \"prompt\": \"Marketing video with $hook, professional commercial quality\"
  }" > "variant_${hook// /_}.json"
done
```

## 视频广告检查清单

- [ ] 前3秒内能够吸引观众注意力
- [ ] 无需声音也能正常播放（支持字幕/文字）
- [ ] 产品特征清晰可见
- [ ] 信息以产品优势为核心
- [ ] 有一个明确的行动号召
- [ ] 根据平台调整正确的宽高比
- [ ] 保持品牌一致性
- [ ] 适配移动设备

## 相关技能

```bash
# Video generation
npx skills add inference-sh/skills@ai-video-generation

# Image generation for thumbnails
npx skills add inference-sh/skills@ai-image-generation

# Text-to-speech for voiceover
npx skills add inference-sh/skills@text-to-speech

# Social media content
npx skills add inference-sh/skills@ai-social-media-content

# Full platform skill
npx skills add inference-sh/skills@inference-sh
```

查看所有可用工具：`infsh app list`