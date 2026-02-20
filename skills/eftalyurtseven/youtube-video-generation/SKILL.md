---
name: youtube-video-generation
description: 使用 each::sense AI 生成 YouTube 视频和 Shorts。可以创建无面部特征的视频、教学视频、教程、产品评测等内容，这些内容都经过优化，以符合 YouTube 的格式和最佳实践。
metadata:
  author: eachlabs
  version: "1.0"
---
# YouTube 视频生成

使用 `each-sense` 功能生成吸引人的 YouTube 内容。该技能可生成适用于 YouTube 各种格式的视频，包括长视频、YouTube Shorts 和缩略图。

## 特点

- **无演员视频**：使用 AI 生成的内容，无需真人出镜
- **YouTube Shorts**：9:16 的竖屏视频，时长最长 3 分钟
- **讲解视频**：包含视觉辅助工具的教育性内容
- **产品评论**：使用 AI 生成的视觉效果来展示和评论产品
- **教程**：分步操作的教学内容
- **新闻摘要**：快速的新闻回顾视频
- **合集**：精选的内容集合
- **游戏精彩片段**：游戏片段合集
- **ASMR/放松**：舒缓身心的内容
- **频道品牌建设**：频道开场、结尾视频和缩略图设计

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 30-second faceless YouTube video about the benefits of meditation, with calming visuals and text overlays",
    "mode": "max"
  }'
```

## YouTube 视频格式与尺寸

| 格式 | 长宽比 | 分辨率 | 最大时长 | 适用场景 |
|--------|--------------|------------|--------------|----------|
| 长视频 | 16:9 | 1920x1080 | 无限制 | 标准 YouTube 视频 |
| YouTube Shorts | 9:16 | 1080x1920 | 3 分钟 | 短形式的竖屏内容 |
| 缩略图 | 16:9 | 1280x720 | 不适用 | 视频缩略图 |

## 适用场景示例

### 1. 无演员 YouTube 视频生成

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 60-second faceless YouTube video about 5 interesting facts about space. Use stunning space imagery, smooth transitions, and animated text overlays for each fact. Add a cinematic orchestral background music feel. 16:9 aspect ratio at 1920x1080.",
    "mode": "max"
  }'
```

### 2. 基于脚本的 YouTube Shorts

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a YouTube Short (9:16, 1080x1920) from this script: \"Did you know that honey never spoils? Archaeologists found 3000-year-old honey in Egyptian tombs that was still edible!\" Use eye-catching visuals of honey, ancient Egypt, and include bold captions. Make it attention-grabbing for the first 2 seconds.",
    "mode": "max"
  }'
```

### 3. 解释/教育视频

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2-minute educational explainer video about how photosynthesis works. Use animated diagrams, infographics, and step-by-step visualizations. Include a friendly voiceover style with clear explanations. 16:9 at 1920x1080. Target audience: middle school students.",
    "mode": "max"
  }'
```

### 4. 产品评论视频

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 90-second product review video for wireless noise-canceling headphones. Show the product from multiple angles, highlight key features (battery life, noise cancellation, comfort), include pros and cons sections with graphics, and end with a rating. 16:9 at 1920x1080, modern tech review style.",
    "mode": "max"
  }'
```

### 5. 教程/操作指南视频

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a step-by-step tutorial video on how to make the perfect pour-over coffee. Include numbered steps, close-up shots of equipment, water temperature graphics, timing indicators, and brewing tips. 16:9 at 1920x1080. Duration: 3 minutes. Clean, minimalist aesthetic.",
    "mode": "max"
  }'
```

### 6. 新闻摘要视频

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 60-second news summary video template for a tech news channel. Include animated lower thirds, headline graphics, transition effects, and space for B-roll footage. Professional news broadcast style with modern graphics. 16:9 at 1920x1080. Blue and white color scheme.",
    "mode": "max"
  }'
```

### 7. 合集视频

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2-minute satisfying compilation video. Include various satisfying visuals: slime being pressed, perfect cake cutting, kinetic sand, soap cutting, and paint mixing. Smooth transitions between clips, no text overlays, relaxing ambient music vibe. 16:9 at 1920x1080.",
    "mode": "max"
  }'
```

### 8. 游戏精彩片段视频

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 45-second gaming highlight intro/template video. Energetic style with glitch effects, neon colors, dynamic transitions, and space for gameplay clips. Include animated subscribe button, social media handles placeholder, and channel logo placement. 16:9 at 1920x1080. EDM/trap music energy.",
    "mode": "max"
  }'
```

### 9. ASMR/放松视频

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3-minute relaxation video for sleep and meditation. Slow-moving visuals of a peaceful forest with gentle rain, soft fog drifting through trees, and occasional wildlife. Very slow, calming transitions. No text, no sudden movements. 16:9 at 1920x1080. Ambient nature sounds.",
    "mode": "max"
  }'
```

### 10. 频道开场/结尾视频生成

```bash
# Create channel intro
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 5-second YouTube channel intro for a cooking channel called \"Kitchen Creations\". Animated logo reveal with steam/smoke effects, wooden textures, warm colors. Include a brief jingle spot. Professional but inviting. 16:9 at 1920x1080.",
    "session_id": "cooking-channel-branding"
  }'

# Create matching outro (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a matching 10-second outro for the same channel. Include animated end screen with subscribe button, two video placeholders for suggested videos, and social media icons. Match the style and colors of the intro we just created.",
    "session_id": "cooking-channel-branding"
  }'
```

## 最佳实践

### 长视频（16:9）
- **快速吸引观众**：前 5-10 秒至关重要
- **保持节奏**：每 5-10 秒更换场景以保持视觉兴趣
- **清晰的结构**：使用视觉章节和段落标记
- **结尾画面**：设计适合 YouTube 结尾画面的内容（最后 20 秒）
- **缩略图**：制作引人注目的 1280x720 缩略图

### YouTube Shorts（9:16）
- **竖屏优化**：适配全屏手机观看
- **迅速吸引注意力**：在开头 1-2 秒内抓住观众
- **适合循环播放**：尽可能制作无缝循环的视频
- **醒目的文字**：为无声观看提供大字号、易读的字幕
- **简洁明了**：虽然允许 3 分钟时长，但 30-60 秒通常效果更好

### 缩略图
- **高对比度**：使用与 YouTube 白色/深色界面形成鲜明对比的颜色
- **简洁的文字**：文字长度控制在 3-5 个词以内
- **使用表情包**：表情包能提高点击率
- **保持一致性**：所有缩略图保持频道风格的一致性

## 创建 YouTube 视频的提示建议

在创建 YouTube 内容时，请在提示中包含以下信息：

1. **格式**：指定是长视频（16:9）还是 YouTube Shorts（9:16）
2. **分辨率**：视频使用 1920x1080 分辨率，缩略图使用 1280x720 分辨率
3. **时长**：明确视频的时长
4. **风格**：描述视频的视觉风格（电影感、极简风格、动感风格等）
5. **内容类型**：无演员视频、教程、产品评论、合集等
6. **目标受众**：该视频面向哪些观众？
7. **文字/字幕**：是否需要添加文字字幕
8. **音乐/氛围**：描述音频的风格

### 示例提示结构

```
"Create a [duration] [format] YouTube [video type] about [topic].
Include [visual elements] with [style/aesthetic].
Target audience: [demographic].
[Additional requirements like text overlays, music style, transitions, etc.]
Resolution: [1920x1080 or 1080x1920]"
```

## 模式选择

在生成视频之前，请询问用户：

**“您希望快速且低成本地生成视频，还是追求高质量？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终发布的视频、高制作质量的视频 | 较慢 | 最高质量 |
| `eco` | 快速草图、概念测试、故事板可视化 | 较快 | 良好质量 |

## 多轮创意迭代

使用 `session_id` 进行视频内容的迭代：

```bash
# Initial video concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 30-second YouTube Short about morning productivity tips",
    "session_id": "productivity-short-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the transitions faster and add more energetic text animations. Also add a stronger hook in the first 2 seconds.",
    "session_id": "productivity-short-001"
  }'

# Create thumbnail for the video
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a thumbnail for this video at 1280x720. Make it eye-catching with bold text saying \"5 AM ROUTINE\" and show a sunrise with productivity imagery.",
    "session_id": "productivity-short-001"
  }'
```

## 视频系列生成

为视频系列生成一致的内容：

```bash
# Episode 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create episode 1 of a \"World Mysteries\" series - focus on the Bermuda Triangle. 2 minutes, dramatic documentary style, 16:9 at 1920x1080.",
    "session_id": "world-mysteries-series",
    "mode": "max"
  }'

# Episode 2 (same session for style consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create episode 2 about Stonehenge. Keep the same visual style, intro, and format as episode 1.",
    "session_id": "world-mysteries-series",
    "mode": "max"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 在 eachlabs.ai 网站补充数据 |
| 内容政策违规 | 内容不符合规定 | 调整提示以符合内容政策 |
| 超时 | 视频生成过程复杂/耗时过长 | 将客户端超时设置至少为 10 分钟 |

## 相关技能

- `each-sense`：核心 API 文档
- `meta-ad-creative-generation`：Meta/Facebook 广告创意生成
- `tiktok-ad-creative-generation`：TikTok 广告创意生成
- `video-generation`：通用视频生成工具