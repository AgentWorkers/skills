---
name: video-ad-specs
description: |
  Video ad creation with exact platform-specific specs for TikTok, Instagram, YouTube, Facebook, LinkedIn.
  Covers dimensions, duration limits, AIDA framework, and caption requirements.
  Use for: video ads, social media ads, paid media creative, video marketing, ad production.
  Triggers: video ad, social media ad, tiktok ad, instagram ad, youtube ad, facebook ad,
  linkedin ad, video creative, ad specs, paid media, video marketing, ad production,
  reels ad, stories ad, pre roll, bumper ad
allowed-tools: Bash(infsh *)
---

# 视频广告规范

您可以通过 [inference.sh](https://inference.sh) 命令行工具为不同的平台创建定制的视频广告。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a vertical video ad scene
infsh app run bytedance/seedance-1-5-pro --input '{
  "prompt": "vertical video, person excitedly unboxing a product, clean modern room, bright natural lighting, social media ad style, authentic feeling, 9:16 format"
}'
```

## 平台规格

### TikTok

| 规格 | 值 |
|------|-------|
| 长宽比 | **9:16**（竖屏） |
| 分辨率 | 1080 x 1920 像素 |
| 时长 | 5-60 秒（建议 15-30 秒） |
| 文件大小 | 最大 500 MB |
| 格式 | MP4, MOV |
| 音频 | 默认开启（建议包含音频） |
| 文本安全区 | 距边缘 150 像素 |
| 吸引观众窗口 | **1 秒** — 首帧必须吸引注意力 |

### Instagram Reels

| 规格 | 值 |
|------|-------|
| 长宽比 | **9:16**（竖屏） |
| 分辨率 | 1080 x 1920 像素 |
| 时长 | 最长 90 秒（广告时长建议 15-30 秒） |
| 封面图片 | 需单独上传，会显示在网格中 |
| 音频 | 默认开启 |
| 字幕区域 | 底部 20% 用于显示文字 |

### Instagram Stories

| 规格 | 值 |
|------|-------|
| 长宽比 | **9:16** |
| 分辨率 | 1080 x 1920 像素 |
| 时长 | 每个片段最长 15 秒 |
| 向上滑动/链接 | 广告可以使用该功能 |
| 顶部/底部区域 | 顶部 14%、底部 20% 不适合放置关键内容 |

### YouTube

| 格式 | 长宽比 | 时长 | 是否可跳过 |
|--------|--------|----------|------|
| Bumper 视频 | 16:9 | **恰好 6 秒** | 不可跳过 |
| 非可跳过视频 | 16:9 | **15 秒** | 不可跳过 |
| 可跳过视频（TrueView） | 16:9 | 任意时长 | **5 秒后开始可跳过** |
| Shorts 视频 | 9:16 | 最长 60 秒 | 不适用 |

### Facebook 动态广告

| 规格 | 值 |
|------|-------|
| 长宽比 | **1:1**（正方形）或 **4:5**（推荐用于移动设备） |
| 分辨率 | 1080 x 1080 或 1080 x 1350 |
| 时长 | 最长 240 秒（建议 15-30 秒） |
| 自动播放 | **静音** — 字幕非常重要 |
| 音频 | 85% 的 Facebook 视频观众在静音状态下观看 |

### LinkedIn

| 规格 | 值 |
|------|-------|
| 长宽比 | **1:1** 或 **16:9** |
| 分辨率 | 1080 x 1080 或 1920 x 1080 |
| 时长 | 3 秒至 10 分钟（广告时长建议 15-30 秒） |
| 风格 | 专业风格 |
| 自动播放 | 动态广告默认静音 |

## 视频广告的 AIDA 框架

| 阶段 | 时间 | 目标 | 技巧 |
|-------|------|------|-----------|
| **吸引注意力** | 0-3 秒 | 阻止观众继续滚动 | 使用视觉冲击、问题式陈述或疑问句 |
| **激发兴趣** | 3-10 秒 | 让观众继续观看 | 说明问题并展示相关性 |
| **激发欲望** | 10-20 秒 | 引发观众对解决方案的兴趣 | 展示产品/效果及用户评价 |
| **促使行动** | 最后 3-5 秒 | 提供明确的行动号召（CTA） | 强调紧迫性并提供购买/注册的选项 |

### 吸引观众的技术（前 3 秒）

| 技巧 | 例子 |
|-----------|---------|
| 强烈陈述 | “这个工具取代了我的整个营销团队” |
| 提问 | “你为什么还在手动做这件事？” |
| 惊喜效果 | 展示使用前后的对比 |
| 视觉冲击 | 使用不寻常的角度或颜色 |
| 用户评价 | “200 万人已经使用了这个工具” |
| 指出痛点 | “如果你讨厌 [常见的问题]，请观看这个视频” |

## 创建视频广告

### 竖屏广告（TikTok、Reels、Stories、Shorts）

```bash
# Hook scene (0-3s)
infsh app run google/veo-3-1-fast --input '{
  "prompt": "vertical 9:16 video, close-up of hands struggling with tangled cables and messy desk, frustrated energy, shaky handheld camera, authentic social media style, bright lighting"
}'

# Solution reveal (3-15s)
infsh app run bytedance/seedance-1-5-pro --input '{
  "prompt": "vertical video, smooth product reveal, clean wireless charging station on minimalist desk, satisfying organization transformation, bright modern room, social media ad aesthetic"
}'

# Add voiceover
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Stop wasting time with this mess. This one product changed my entire setup. Everything charges. Everything is organized. Link in bio."
}'

# Merge video + audio
infsh app run infsh/video-audio-merger --input '{
  "video": "solution-reveal.mp4",
  "audio": "voiceover.mp3"
}'

# Add captions (critical for silent autoplay)
infsh app run infsh/caption-videos --input '{
  "video": "ad-with-audio.mp4",
  "caption_file": "captions.srt"
}'
```

### 正方形广告（Facebook、LinkedIn 动态广告）

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "square 1:1 video, professional person at desk discovering a new software tool, laptop screen showing clean dashboard, natural office lighting, corporate commercial style, satisfied expression"
}'
```

### YouTube Bumper 视频（6 秒）

```bash
# 6-second bumper: one message, one visual, one CTA
infsh app run google/veo-3-1-fast --input '{
  "prompt": "6 second product ad, quick montage of a sleek app being used on phone, fast cuts, modern, energetic, brand logo reveal at end, punchy and dynamic, wide 16:9"
}'

# Keep it tight
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Your reports. Automated. Try DataFlow free."
}'
```

## 字幕是必须的

85% 的 Facebook 视频和 40% 以上的 Instagram 视频观众在静音状态下观看。

### 字幕的最佳实践

| 规则 | 原因 |
|------|--------|
| 必须添加字幕 | 大多数平台默认为静音观看 |
| 使用大字号、易读的字体 | 小字体在移动设备上难以看清 |
| 高对比度 | 白色文字搭配深色背景 |
| 字幕位于中心或底部三分之一位置 | 标准的观看位置 |
| 每次最多 2 行 | 过多文字会导致观众无法快速阅读 |
| 关键词加粗/高亮显示 | 引导观众注意重要信息 |

```bash
# Generate captions from audio
# (create SRT file from your script, then burn in)
infsh app run infsh/caption-videos --input '{
  "video": "ad-video.mp4",
  "caption_file": "ad-captions.srt"
}'
```

## 广告结构模板

### 评价型广告（15-30 秒）

| 时间 | 内容 |
|------|---------|
| 0-3 秒 | 客户描述他们遇到的问题 |
| 3-15 秒 | 他们如何发现并尝试该产品 |
| 15-25 秒 | 他们获得的具体效果 |
| 25-30 秒 | 产品名称 + 行动号召（CTA） |

### 演示型广告（15-30 秒）

| 时间 | 内容 |
|------|---------|
| 0-3 秒 | 问题（文字或视觉效果） |
| 3-20 秒 | 产品演示 |
| 20-25 秒 | 关键效果/好处 |
| 25-30 秒 | 行动号召（CTA） |

### 对比前后效果广告（15 秒）

| 时间 | 内容 |
|------|---------|
| 0-3 秒 | “使用前”的状态（混乱、缓慢、令人沮丧） |
| 3-5 秒 | 过渡到使用产品后的状态 |
| 5-12 秒 | “使用后”的状态（整洁、高效、令人满意） |
| 12-15 秒 | 行动号召（CTA） |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 前 1-3 秒没有吸引观众注意力的内容 | 观众会直接滚动过去 | 使用视觉冲击或问题式陈述来吸引注意力 |
| 在 TikTok/Reels 上使用横屏视频 | 视频会被裁剪，显得不专业 | 使用 9:16 的竖屏格式 |
| 没有字幕 | 大多数观众在静音状态下观看 | 必须添加字幕 |
| 行动号召太晚 | 观众可能已经离开页面 | 在最后 5 秒内提供明确的行动号召 |
| 视频时长超过平台规定 | 观众可能会直接跳过 | 根据平台时长要求调整视频长度 |
| 所有平台使用相同的广告内容 | 规格和风格不匹配 | 为每个平台创建定制版本 |
| 视频开头出现品牌标志 | 会让人觉得像广告，导致观众跳过 | 将品牌元素放在视频结尾 |

## 检查清单

- [ ] 使用目标平台的正确长宽比 |
- [ ] 前 1-3 秒内吸引观众注意 |
- [ ] 添加字幕（清晰易读，高对比度） |
- [ ] 行动号召明确且在最后 5 秒内显示 |
- [ ] 时长符合平台规定 |
- [ ] 文本不在平台规定的安全区域内 |
- [ ] 音频设计适合开启和关闭声音的情况 |
- [ ] 为每个平台创建定制版本 |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-video-generation
npx skills add inferencesh/skills@video-prompting-guide
npx skills add inferencesh/skills@text-to-speech
npx skills add inferencesh/skills@prompt-engineering
```

浏览所有应用程序：`infsh app list`