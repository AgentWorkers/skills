---
name: music-video-generation
description: 使用 each::sense AI 生成音乐视频。可以创建可视化效果、歌词视频、动画音乐视频、演唱会视觉效果，以及与音频同步的、符合特定音乐风格的美学设计。
metadata:
  author: eachlabs
  version: "1.0"
---
# 音乐视频制作

使用 `each-sense` 功能，您可以制作出令人惊叹的音乐视频。该功能能够生成与音频同步的可视化效果、歌词视频、动画序列以及电影风格的音乐视频。

## 主要功能

- **音频可视化效果**：根据音频频率动态变化的视觉效果
- **歌词视频**：带有歌词的动画文字
- **抽象视觉效果**：艺术性的、非具象化的视频内容
- **艺术家表演**：模拟艺术家或乐队的表演画面
- **动画音乐视频**：卡通、动漫或风格化的动画形式
- **音乐会视觉效果**：LED屏幕展示和舞台投影
- **专辑封面动画**：让静态的专辑封面焕发生机
- **节拍同步内容**：根据节奏和速度变化的视觉效果
- **特定类型的视觉风格**：嘻哈、电子舞曲（EDM）、摇滚、流行等

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an audio visualizer video with neon geometric shapes that pulse to the beat, dark background with vibrant colors",
    "mode": "max"
  }'
```

## 视频格式与纵横比

| 平台 | 纵横比 | 分辨率 | 适用场景 |
|--------|--------|---------|---------|
| YouTube | 16:9 | 1920x1080 | 标准音乐视频 |
| YouTube Shorts | 9:16 | 1080x1920 | 垂直视频、预告片 |
| Instagram Reels | 9:16 | 1080x1920 | 社交媒体推广 |
| TikTok | 9:16 | 1080x1920 | 爱看视频 |
| Square | 1:1 | 1080x1080 | Instagram 主页、Spotify Canvas |
| Ultrawide | 21:9 | 2560x1080 | 音乐会LED屏幕 |

## 使用场景示例

### 1. 基于音频的可视化效果

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 16:9 audio visualizer video. Circular waveform in the center with particles emanating outward on each beat. Deep purple and electric blue color palette. Dark space background with subtle stars. 10 seconds loop.",
    "mode": "max"
  }'
```

### 2. 歌词视频制作

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a lyric video for the lyrics: \"Running through the night, chasing starlight, we are infinite tonight\". Animated text appearing word by word with a dreamy night sky background. Stars twinkling, soft gradient from dark blue to purple. Modern sans-serif font with subtle glow effect. 16:9 aspect ratio.",
    "mode": "max"
  }'
```

### 3. 抽象音乐视觉效果

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate abstract music visuals for an ambient electronic track. Flowing liquid metal morphing shapes, iridescent surfaces reflecting rainbow colors, slow hypnotic movement. Think art installation meets music video. 16:9, 15 seconds.",
    "mode": "max"
  }'
```

### 4. 艺术家表演视频

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a music video showing a female singer performing on a dark stage. Dramatic spotlight lighting, smoke effects, cinematic camera movement circling the performer. She is wearing an elegant black dress, passionate emotional performance. 16:9 widescreen, film grain aesthetic.",
    "mode": "max"
  }'
```

### 5. 动画音乐视频（动漫风格）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime-style animated music video. A young character with colorful hair running through a neon-lit cyberpunk city at night. Dynamic action poses, speed lines, rain effects. Japanese anime aesthetic like Studio Trigger. High energy and dramatic. 16:9.",
    "mode": "max"
  }'
```

### 6. 音乐会LED屏幕视觉效果

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate concert visuals for LED wall projection. Abstract geometric patterns - triangles and hexagons morphing and pulsing. High contrast black and white with occasional bursts of red. Designed for live performance, loopable, high impact visuals that work on massive screens. 21:9 ultrawide aspect ratio.",
    "mode": "max"
  }'
```

### 7. 专辑封面动画（Spotify Canvas）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Spotify Canvas style animation from album art concept. A surreal landscape with floating islands and waterfalls going upward. Soft pastel colors - pink clouds, turquoise water, golden sunset light. Subtle parallax motion, dreamy and ethereal mood. 9:16 vertical format, 8 second seamless loop.",
    "mode": "max"
  }'
```

### 8. 节拍同步视觉效果

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create beat-synced visuals for a 120 BPM track. Geometric shapes (cubes, spheres, pyramids) that flash and transform on each beat. Strobe-like intensity changes. Black background with neon pink, cyan, and yellow shapes. High energy, rave aesthetic. Design cuts to happen every 0.5 seconds to match tempo. 16:9.",
    "mode": "max"
  }'
```

### 9. 嘻哈风格视觉效果

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a hip-hop music video aesthetic. Urban street scene at night, street lights with lens flares, graffiti walls, luxury cars in background. Slow motion rain falling. Moody cinematic color grading - teal shadows and orange highlights. Trap music vibe, high production value look. 16:9 widescreen.",
    "mode": "max"
  }'
```

### 10. 基于故事的音乐视频

```bash
# Part 1: Opening scene
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the opening scene of a narrative music video. A lonely figure standing at a train station at dawn. Empty platform, morning mist, warm golden light breaking through clouds. Melancholic mood, cinematic widescreen composition. The character is looking at a departing train. 16:9.",
    "session_id": "music-video-story-001",
    "mode": "max"
  }'

# Part 2: Middle scene (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the next scene continuing our music video story. The same character is now walking through a sunlit field of wildflowers. Memories and flashbacks - double exposure effect showing happy moments. Bittersweet emotion, hope emerging. Maintain the same cinematic color grading and style.",
    "session_id": "music-video-story-001",
    "mode": "max"
  }'

# Part 3: Final scene
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the final climactic scene of our music video. The character reunites with a loved one on a rooftop at sunset. City skyline in background, warm embrace, emotional payoff. Golden hour lighting, lens flares, cinematic slow motion. End on a hopeful note with them looking at the horizon together.",
    "session_id": "music-video-story-001",
    "mode": "max"
  }'
```

## 最佳实践

### 视觉设计
- **色彩一致性**：在整个视频中保持统一的色彩搭配
- **动态节奏**：让视觉效果的强度与音乐的节奏相匹配
- **安全区域**：在社交媒体平台上，确保关键元素远离屏幕边缘
- **循环设置**：为可视化效果和短视频设置无缝循环
- **文本可读性**：在歌词视频中确保文字与背景有足够的对比度

### 技术注意事项
- **节拍同步**：对于需要节拍同步的内容，请尽可能提供BPM（每分钟拍数）
- **时长**：建议视频时长控制在5-30秒之间
- **循环播放**：如需重复播放，请明确要求无缝循环
- **平台规格**：始终指定目标平台的纵横比

### 不同类型的视觉风格指南

| 音乐类型 | 视觉风格 | 色彩搭配 | 动态效果 |
|---------|----------------|----------------|-------------------|
| 电子舞曲（EDM） | 几何形状、霓虹灯、未来感 | 明亮的霓虹色、RGB色调 | 快速、充满活力 |
| 嘻哈/说唱 | 城市风格、奢华感、电影感 | 深色调搭配金色/蓝绿色 | 慢动作、戏剧性 |
| 摇滚/金属乐 | 粗糙感、高对比度 | 深色调、红色、单色 | 强烈、混乱感 |
| 流行音乐 | 色彩丰富、精致、轻松愉快 | 明亮的淡色调 | 平滑、动感 |
| 悠闲/轻松风格 | 抽象、流畅的视觉效果 | 温和的渐变效果 | 慢节奏、催眠感 |
| 独立/另类音乐 | 复古风格、艺术感 | 低调的色彩、电影质感 | 自然、有机的视觉元素 |

## 制作音乐视频的提示

在制作音乐视频时，请提供以下详细信息：

1. **音乐类型/情绪**：音乐的类型和情感基调
2. **视觉风格**：现实主义、动画效果、抽象风格等
3. **色彩搭配**：具体的颜色或整体氛围
4. **纵横比**：16:9、9:16、1:1或21:9
5. **视频时长**：视频的预计长度
6. **动态效果**：快速切换、慢动作、平滑过渡等
7. **关键元素**：视频中应包含的元素
8. **循环要求**：是否需要无缝循环播放

### 示例提示结构

```
"Create a [duration] [genre] music video in [aspect ratio].
Visual style: [style description].
Show [key visual elements].
Color palette: [colors].
Mood: [emotional tone].
[Additional requirements like looping, beat-sync, etc.]"
```

## 模式选择

**“您想要快速且低成本的结果，还是高质量的作品？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|---------|--------|---------|
| `max` | 最终版本、官方视频、高品质内容 | 较慢 | 最高级别 |
| `eco` | 快速概念、社交媒体视频、初步尝试 | 较快 | 适中 |

## 多轮创意迭代

使用 `session_id` 进行多次迭代，逐步完善您的音乐视频：

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a visualizer with glowing orbs floating in space",
    "session_id": "visualizer-project-001"
  }'

# Refine based on result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more particle trails to the orbs and make the colors shift from blue to purple",
    "session_id": "visualizer-project-001"
  }'

# Create variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a more intense version of this for the chorus section with faster movement",
    "session_id": "visualizer-project-001"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|---------|--------|-------------------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 请在 eachlabs.ai 网站补充数据 |
| 内容违规 | 视频内容不符合规定 | 调整提示内容以符合平台政策 |
| 超时 | 生成过程复杂 | 将客户端超时时间设置为至少10分钟 |

## 相关技能

- `each-sense`：核心API文档
- `video-generation`：通用视频生成工具
- `image-generation`：静态图片和截图制作
- `audio-generation`：音乐和声音制作