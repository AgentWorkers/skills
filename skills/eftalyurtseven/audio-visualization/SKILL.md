---
name: audio-visualization
description: 使用 each::sense AI 生成音频可视化视频。可以从音频文件中创建波形图、频谱分析图、粒子效果、3D 可视化内容以及与节拍同步的动画。
metadata:
  author: eachlabs
  version: "1.0"
---
# 音频可视化

使用 `each-sense` 生成令人惊叹的音频可视化视频。该功能可以创建动态的音频视觉效果，包括波形图、频谱分析器、粒子效果、3D 可视化以及与节拍同步的动画。

## 特点

- **波形可视化器**：经典的示波器风格的音频波形图
- **频谱分析器**：具有可定制样式的频率条形图
- **圆形可视化器**：放射状的音频响应式设计
- **粒子系统**：由音频驱动的粒子效果和爆炸效果
- **3D 可视化**：沉浸式的三维音频景观
- **抽象可视化器**：艺术化的、抽象的音频响应式视觉效果
- **播客波形图**：适用于播客和语音内容的简洁波形图
- **音乐视频**：带有特效的完整音乐视频可视化效果
- **与节拍同步的动画**：与音乐节拍完美同步的动画
- **定制品牌可视化器**：可定制的品牌音频可视化效果

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a neon waveform visualizer video for this electronic music track, purple and cyan colors, 16:9 format",
    "mode": "max",
    "audio_urls": ["https://example.com/music-track.mp3"]
  }'
```

## 可视化样式

| 样式 | 描述 | 适用场景 |
|-------|-------------|----------|
| 波形 | 经典的示波器波形图 | 音乐、播客、语音内容 |
| 频谱条形图 | 频率分析器条形图 | 电子舞曲（EDM）、电子音乐 |
| 圆形 | 放射状的音频响应式设计 | 专辑封面、社交媒体 |
| 粒子系统 | 由音频驱动的粒子效果 | 戏剧性、充满活力的音乐 |
| 3D 可视化 | 三维地形/形状 | 沉浸式内容 |
| 抽象 | 艺术化的、抽象的视觉效果 | 创意、艺术类视频 |
| 极简风格 | 简洁的波形图 | 播客、访谈 |

## 使用案例示例

### 1. 波形可视化器

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a smooth waveform visualizer video for this audio. Use a gradient from electric blue to pink, dark background, 1080p 16:9 format. The waveform should be centered and react smoothly to the audio frequencies.",
    "mode": "max",
    "audio_urls": ["https://example.com/song.mp3"]
  }'
```

### 2. 频谱分析器条形图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a spectrum analyzer visualization with vertical bars that react to the music. EDM style with neon green and yellow gradient bars on a black background. Add glow effects and mirror reflection at the bottom. 1920x1080 landscape video.",
    "mode": "max",
    "audio_urls": ["https://example.com/edm-track.mp3"]
  }'
```

### 3. 圆形音频可视化器

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a circular audio visualizer with radial bars emanating from the center. Place an album art placeholder in the center circle. Use warm orange and red colors with a subtle pulsing glow effect. Square 1:1 format for social media.",
    "mode": "max",
    "audio_urls": ["https://example.com/album-track.mp3"]
  }'
```

### 4. 基于粒子的可视化器

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an audio-reactive particle system visualization. Particles should explode outward on bass hits and swirl gently during quieter sections. Use a cosmic color palette with blues, purples, and white sparkles. Deep space background. 16:9 HD video.",
    "mode": "max",
    "audio_urls": ["https://example.com/electronic.mp3"]
  }'
```

### 5. 3D 音频可视化

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3D audio visualization with a geometric landscape that responds to the music. The terrain should rise and fall with the frequencies, camera slowly moving forward through the scene. Synthwave aesthetic with neon grid lines, pink and cyan lighting. 1080p cinematic format.",
    "mode": "max",
    "audio_urls": ["https://example.com/synthwave.mp3"]
  }'
```

### 6. 抽象可视化效果

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate abstract audio-reactive visuals with fluid, organic shapes that morph and flow with the music. Use a dreamy color palette with soft pastels transitioning through the spectrum. The visuals should feel like living art, responding to both rhythm and melody. Vertical 9:16 format for Instagram Reels.",
    "mode": "max",
    "audio_urls": ["https://example.com/ambient-track.mp3"]
  }'
```

### 7. 播客波形图视频

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a clean, minimal podcast waveform video. Simple horizontal waveform bar in the center that responds to voice audio. White waveform on a dark gray background. Leave space at the top for a podcast title and bottom for episode info. Professional and clean look. Square 1:1 format.",
    "mode": "eco",
    "audio_urls": ["https://example.com/podcast-episode.mp3"]
  }'
```

### 8. 音乐视频可视化器

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a full music video visualizer combining multiple effects. Start with abstract flowing shapes, transition to particle bursts during the chorus, and include subtle waveform elements throughout. High energy, colorful, psychedelic style matching the energetic music. 1920x1080 landscape format, full track length.",
    "mode": "max",
    "audio_urls": ["https://example.com/full-song.mp3"]
  }'
```

### 9. 与节拍同步的动画

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a beat-synced animation where geometric shapes pulse, rotate, and transform exactly on the beat. Sharp, precise animations on every kick drum and snare hit. Minimal black and white design with red accent flashes on the strongest beats. Perfect sync is critical. 16:9 HD video.",
    "mode": "max",
    "audio_urls": ["https://example.com/drum-track.mp3"]
  }'
```

### 10. 定制品牌可视化器

```bash
# Initial branded visualizer
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a branded audio visualizer for a record label. Use brand colors: deep purple (#6B21A8) and gold (#F59E0B). Include a circular visualizer with space in the center for a logo. Add a subtle animated gradient background. Professional, premium feel. 1:1 square format for social media.",
    "mode": "max",
    "audio_urls": ["https://example.com/label-release.mp3"],
    "session_id": "branded-viz-001"
  }'

# Iterate on the design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more gold particle sparkles that react to high frequencies, and make the purple glow more intense on bass hits",
    "session_id": "branded-viz-001"
  }'
```

## 最佳实践

### 音频质量
- **文件格式**：支持 MP3、WAV、FLAC、AAC 格式
- **采样率**：建议使用 44.1kHz 或更高
- **清晰的音频**：高质量的音频能产生更好的可视化效果
- **音量级别**：标准化音量可避免在可视化中出现音量溢出问题

### 视觉设计
- **对比度**：视觉元素与背景之间的对比度要高
- **色彩搭配**：使用互补色或类似色的配色方案
- **响应性**：视觉效果的强度应与音频的动态变化相匹配
- **安全区域**：为平台用户界面留出足够的显示空间

### 格式指南

| 平台 | 宽高比 | 分辨率 | 备注 |
|----------|--------------|------------|-------|
| YouTube | 16:9 | 1920x1080 | 横屏格式，全高清 |
| Instagram 帖子 | 1:1 | 1080x1080 | 正方形格式 |
| Instagram Reels | 9:16 | 1080x1920 | 垂直格式，适合 Stories |
| TikTok | 9:16 | 1080x1920 | 垂直格式 |
| Spotify Canvas | 9:16 | 720x1280 | 3-8 秒的循环视频 |
| SoundCloud | 16:9 | 1280x720 | 波形图风格受欢迎 |

## 音频可视化提示

在提示中包含以下细节：

1. **可视化类型**：波形、频谱、圆形、粒子、3D、抽象
2. **色彩方案**：具体的颜色、渐变或调色板风格
3. **背景**：纯色、渐变、动画背景等
4. **效果**：发光、模糊、反射、粒子效果等
5. **响应性**：哪些视觉效果会随着低音、中音、高音或节拍的变化而变化
6. **格式**：宽高比和分辨率
7. **风格**：电子舞曲（EDM）、极简风格、迷幻风格、企业风格等
8. **品牌元素**：预留空间用于放置 logo 和文字

### 示例提示结构

```
"Create a [visualization type] for [audio type/genre].
Use [color scheme] with [background style].
Add [effects] that react to [audio elements].
[Format and resolution]. [Style description]."
```

## 模式选择

**“您需要快速且低成本的效果，还是高质量的效果？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终发布版本、音乐视频、高级内容 | 较慢 | 最高质量 |
| `eco` | 草稿、预览、社交媒体片段、播客 | 较快 | 优质效果 |

## 多轮创意迭代

使用 `session_id` 进行多次可视化效果迭代：

```bash
# Initial visualization
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a spectrum analyzer visualization for this EDM track",
    "audio_urls": ["https://example.com/track.mp3"],
    "session_id": "viz-project-001"
  }'

# Refine colors
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the color scheme to cyan and magenta, add more glow",
    "session_id": "viz-project-001"
  }'

# Add effects
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add particle trails on the peaks and a subtle mirror reflection",
    "session_id": "viz-project-001"
  }'
```

## 批量生成多首音乐的可视化效果

```bash
# Track 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a circular visualizer for this track, purple and blue colors",
    "mode": "eco",
    "audio_urls": ["https://example.com/track1.mp3"]
  }'

# Track 2 (same style)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a circular visualizer for this track, same purple and blue style as track1",
    "mode": "eco",
    "audio_urls": ["https://example.com/track2.mp3"]
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| **创建可视化失败：HTTP 422** | 平衡性不足 | 请在 eachlabs.ai 平台上补充数据 |
| 音频处理失败 | 不支持的文件格式或损坏的文件 | 使用 MP3/WAV 格式，并检查文件完整性 |
| 超时 | 音频文件过长或可视化效果复杂 | 将客户端超时时间设置为至少 10 分钟 |
| 同步问题 | 节拍检测复杂 | 提供清晰、音质良好的音频文件 |

## 相关技能

- `each-sense`：核心 API 文档
- `music-generation`：人工智能音乐生成
- `video-generation`：通用视频生成
- `video-editing`：视频后期编辑