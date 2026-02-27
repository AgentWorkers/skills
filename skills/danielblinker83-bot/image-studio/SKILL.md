---
name: image-studio
version: 1.0.0
description: 生成适用于任何平台和场景的专业AI图像提示——适用于Instagram、LinkedIn、博客标题、YouTube缩略图、品牌视觉素材以及广告设计。支持与DALL-E、Midjourney、Stable Diffusion和Ideogram等AI模型配合使用。同时提供样式指南和平台尺寸规范。
tags: [image-generation, dall-e, midjourney, visual-content, design, ai-art, social-media, branding]
author: contentai-suite
license: MIT
---
# Image Studio — 通用 AI 图像提示系统

## 该技能的功能

该技能能够为任何平台、任何领域以及任何视觉风格生成优化过的 AI 图像提示。它根据您的内容要求，生成详细的提示，适用于 DALL-E、Midjourney、Stable Diffusion 或 Ideogram 等图像生成工具。

## 使用方法

**输入格式：**
```
BRAND NAME: [Your brand]
NICHE: [Your industry]
VISUAL STYLE: [Photorealistic / Illustrated / Minimalist / Bold/Graphic / Corporate / Lifestyle]
BRAND COLORS: [Primary and secondary colors or "default"]
PLATFORM: [Instagram / LinkedIn / Blog / YouTube / Twitter / Ad]
IMAGE TYPE: [Post background / Profile visual / Product / Person / Abstract concept / Infographic]
MOOD: [Energetic / Professional / Warm / Bold / Calm / Inspiring]
CONTENT CONTEXT: [What is the image for — the post topic]
```

---

## 平台规格

| 平台        | 推荐尺寸        | 宽高比        | 备注                |
|------------|------------------|--------------|-------------------|
| Instagram 主页   | 1080×1080px     | 1:1           | 支持 1080×1350 (4:5) 的尺寸以获得更多显示空间 |
| Instagram 故事/短视频 | 1080×1920px     | 9:16           | 垂直全屏显示           |
| LinkedIn 帖子     | 1200×628px     | 1.91:1          | 建议使用横向布局           |
| LinkedIn 个人资料   | 1584×396px     | 4:1           | 用作背景图片           |
| Twitter/X 主页   | 1500×500px     | 3:1           | 用作封面图片           |
| 博客标题栏     | 1200×628px     | 1.91:1          | 也适用于 Open Graph 格式     |
| YouTube 缩略图   | 1280×720px     | 16:9           | 高对比度以提高点击率         |
| Facebook 广告     | 1200×628px     | 1.91:1          | 与 LinkedIn 帖子规格相同       |

---

## 图像提示的结构

一个优秀的 AI 图像提示应包含以下组成部分：

```
[SUBJECT] + [ACTION/POSE] + [SETTING/BACKGROUND] + [STYLE] + [LIGHTING] + [MOOD] + [TECHNICAL SPECS]
```

**示例：**
```
A confident professional in modern business casual clothing, standing in a minimalist office with natural light,
looking at camera with a warm smile, photorealistic photography style,
soft natural window lighting from the left, professional and approachable mood,
high resolution, 16:9 aspect ratio, sharp focus
```

---

## 按类别划分的提示模板

### 1. 专业肖像/头像风格
```
[Person description: gender-neutral if needed, professional appearance],
[specific clothing style matching brand],
[location: office / outdoor urban / studio background],
professional headshot photography,
[lighting: studio lighting / natural window light / golden hour],
[mood: confident / approachable / authoritative],
high resolution, sharp focus, clean background,
[brand colors if applicable] color palette
```

**生成提示：**
```
Create a DALL-E prompt for a professional portrait image for [BRAND NAME] in [NICHE].
The person should: [appearance guidelines without specific race/gender unless needed]
Setting: [SETTING]
Style: photorealistic, professional photography
Mood: [MOOD]
Must work as: [PLATFORM] image at [SIZE]
```

### 2. 生活方式/动作场景
```
[Scene description: person doing specific activity related to niche],
authentic candid photography style,
[setting: specific location type],
[time of day: morning light / golden hour / indoor artificial warm light],
[emotion: focused / joyful / determined / relaxed],
documentary photography style, high resolution
```

### 3. 概念性/抽象性内容（适用于引用、提示、想法等）
```
Abstract concept representing [TOPIC/THEME],
[style: geometric / watercolor / gradient / minimal line art],
color palette: [BRAND COLORS or descriptive colors like "deep navy and gold"],
[mood: sophisticated / energetic / calm],
suitable as social media background,
16:9 / 1:1 format [choose for platform],
no text, clean and modern
```

### 4. 信息图背景/数据可视化
```
Clean minimal background for [TOPIC] infographic,
[style: flat design / light gradient / dark elegant],
color scheme: [BRAND COLORS],
subtle geometric patterns or lines as texture,
professional and modern,
high contrast areas for text overlay,
[platform] format
```

### 5. 产品/服务视觉元素
```
[Product/service concept] displayed professionally,
[setting: on a surface / floating / in use / lifestyle context],
[photography style: product photography / lifestyle / editorial],
[background: white studio / contextual / branded colored],
professional lighting, high resolution, sharp details
```

### 6. 引用/文字背景图片
```
Simple, elegant background suitable for text overlay,
[style: gradient / solid color with texture / subtle pattern / blurred photo background],
color: [BRAND COLORS],
mood: [inspirational / professional / energetic],
minimal visual noise,
[platform] format,
no people, no existing text
```

---

## 根据品牌个性定制的样式指南

### 企业/专业品牌
```
Style keywords: clean, minimal, sophisticated, structured
Colors: navy, white, silver, deep green
Lighting: studio, natural diffused
Avoid: chaotic compositions, oversaturated colors, casual/playful elements
```

### 教练/个人品牌（温暖且亲切）
```
Style keywords: authentic, warm, real, human
Colors: warm tones, earth tones, soft gradients
Lighting: golden hour, natural window light
Avoid: overly corporate, cold blue tones, stock photo look
```

### 健身/健康品牌
```
Style keywords: energetic, dynamic, powerful, clean
Colors: bold primary colors, black/white with accent color
Lighting: dramatic, high contrast, natural outdoor
Avoid: static poses, dull backgrounds, overly clinical
```

### 创意/设计品牌
```
Style keywords: artistic, bold, distinctive, expressive
Colors: brand-specific palette, can be unconventional
Lighting: dramatic, creative, stylized
Avoid: generic stock photo look, overly literal interpretations
```

### 食品/生活方式品牌
```
Style keywords: appetizing, warm, inviting, authentic
Colors: warm golden tones, earthy, fresh natural colors
Lighting: natural top-down or 45-degree angle
Avoid: cold lighting, clinical presentation, artificial colors
```

---

## 批量图像提示生成器

若需一次性生成一周的内容视觉素材，可以使用以下提示：

**提示：**
```
Generate 7 AI image prompts for [BRAND NAME] in [NICHE] for a week of Instagram content.
Each prompt: [describe image type for that day's content topic]
Days: [list each day's content theme]
Style consistency: all images should feel cohesive using [BRAND COLORS] color palette
Include: platform specs (1080×1080), no text in images
Tool compatibility: optimized for DALL-E 3 / Midjourney v6 [choose]
```

---

## 质量检查清单

在使用 AI 生成的图片之前，请确认以下几点：
- [ ] 该图片是否符合您的品牌视觉风格？
- [ ] 光线和氛围是否适合目标平台？
- [ ] 图片中是否存在 AI 生成时产生的瑕疵（如手部变形、奇怪的文字或奇怪的背景）？
- [ ] 是否需要添加文字？背景是否有足够的空白区域？
- [ ] 该图片是否适合所有受众群体？
- [ ] 图片是否具有真实感，而非普通的库存图片？
- [ ] 图片在目标平台尺寸下压缩效果是否良好？

---

## 与 ContentAI Suite 的集成

该技能可无缝集成到 **[ContentAI Suite](https://contentai-suite.vercel.app)** 中——这是一个免费的多代理营销平台，能够为任何企业快速生成专业内容。

→ **免费试用：** https://contentai-suite.vercel.app