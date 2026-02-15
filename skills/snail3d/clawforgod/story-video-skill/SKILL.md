---
name: story-video
description: 将带有旁白的故事（音频+文本）转换为YouTube Shorts视频（9:16分钟，竖屏格式），视频需包含同步的字幕、与故事内容相匹配的动态背景图片以及专业的字幕效果。
---

# 将故事内容转换为吸引人的YouTube Shorts视频的技能

该技能可以将睡前故事、朗读内容或任何口语内容转换为精美的YouTube Shorts视频，具备以下特点：
- **同步字幕**：单词在发音时实时高亮显示
- **动态背景**：根据故事内容或章节选择相应的图片作为背景
- **YouTube Shorts格式**：9:16的竖屏视频，适合在移动设备上观看
- **专业设计**：字幕居中显示，并带有动画效果

## 快速入门

### 输入要求
1. **音频文件**：包含朗读内容的MP3/WAV文件（例如，使用ElevenLabs的TTS服务生成）
2. **完整文本转录**：故事的完整文本
3. **故事章节（可选）**：如果有的话，为每个章节指定相应的背景图片

### 基本工作流程

```bash
# 1. Transcribe audio to get word timing (automatic)
story-video transcribe --audio story.mp3 --output story.json

# 2. Generate video with auto-searched backgrounds
story-video generate \
  --audio story.mp3 \
  --text "Once upon a time..." \
  --title "Bedtime Story" \
  --output story.mp4
```

输出结果：`story.mp4`（9:16竖屏格式，适合上传到YouTube Shorts）

### 高级功能：自定义章节和背景

```bash
# Create a config with sections and suggested image searches
story-video generate \
  --audio story.mp3 \
  --text full_text.txt \
  --config story-config.json \
  --output story.mp4
```

**story-config.json**：配置文件示例
```json
{
  "title": "The Snail Designer",
  "sections": [
    {
      "start_time": 0,
      "end_time": 15,
      "text": "Once upon a time, in the beautiful city of El Paso...",
      "search_query": "El Paso desert sunset"
    },
    {
      "start_time": 15,
      "end_time": 35,
      "text": "...a gentle snail named Snail was a designer.",
      "search_query": "3D design workshop creative tools"
    }
  ]
}
```

## 工作原理

### 1. **音频转录与时间标注**
- 使用Groq Whisper（或本地的语音转文本工具）获取每个单词的发音时间
- 输出包含`{word, start_ms, end_ms}`的JSON格式数据，以实现精确的字幕同步

### 2. **章节划分**
- 将音频分割成10-30秒长的段落
- 根据文本内容生成相应的图片搜索查询
- 在Unsplash或Pexels网站上搜索高质量的图片

### 3. **视频制作**
- 创建9:16像素的画布（1080x1920）
- 将背景图片居中裁剪并应用微妙的缩放效果
- 渲染字幕，使其与音频同步显示
- 应用多种字幕效果：
  - **淡入/淡出**：单词出现或消失时使用淡入淡出效果
  **颜色高亮**：当前显示的单词用鲜艳的颜色突出显示，背景部分显示为白色
  **字体大小调整**：当前单词的字体稍大一些
  **阴影效果**：在任何背景上都能保证良好的可读性

### 4. **视频导出**
- 将音频和视频层合并
- 采用H.264编码格式，并优化比特率以适应YouTube Shorts的播放要求
- 为视频添加元数据标签（如宽高比、时长等）

## 配置选项

### 字幕样式

```json
{
  "subtitles": {
    "font": "Inter",
    "size": 48,
    "color_current": "#FFD700",
    "color_context": "#FFFFFF",
    "shadow": true,
    "shadow_blur": 8,
    "shadow_color": "#000000",
    "shadow_offset_y": 3,
    "animation_type": "fade_scale",
    "animation_duration_ms": 200
  }
}
```

### 背景选项

```json
{
  "background": {
    "source": "unsplash",
    "fallback_color": "#1a1a1a",
    "zoom_effect": "subtle",
    "zoom_speed": 0.3,
    "fade_between_sections": true,
    "fade_duration_ms": 500
  }
}
```

## 命令行工具

### `story-video transcribe`
从音频文件中提取每个单词的发音时间。

**参数示例：**
- `--audio`（必选）：音频文件路径
- `--output`（必选）：包含时间信息的JSON输出文件路径
- `--engine`（可选）：使用groq、google或本地的语音转文本工具（默认为groq）

**输出格式：**
```json
{
  "duration_ms": 45000,
  "words": [
    {"word": "Once", "start_ms": 0, "end_ms": 250},
    {"word": "upon", "start_ms": 250, "end_ms": 450},
    ...
  ]
}
```

### `story-video generate`
根据音频和文本生成视频。

**参数示例：**
- `--audio`（必选）：MP3/WAV音频文件路径
- `--text`（必选）：故事的完整文本转录
- `--output`（必选）：视频输出文件路径
- `--config`（可选）：配置文件（包含章节信息、字幕样式等）
- `--title`（可选）：视频标题（用于元数据）
- `--subtitle-style`（可选）：字幕样式（预设：minimal、bold、elegant；默认为bold）
- `--background-source`（可选）：图片来源（unsplash、pexels或本地目录；默认为unsplash）

### `story-video style-preset`
列出可用的字幕样式预设：
- **minimal**：小字体、居中显示、简单的动画效果
- **bold**：大字体、明显的颜色高亮、动态动画效果
- **elegant**：带衬线的字体、精致的色彩、平滑的淡入淡出效果
- **neon**：鲜艳的色彩、发光效果、快速的动画效果

## 图片搜索策略
该技能会根据故事内容自动生成图片搜索查询：
1. **提取名词**：识别关键名词（如“snail”、“designer”、“El Paso”、“daughters”等）
2. **添加上下文关键词**：根据名词生成相关关键词（如“sunset”、“desert”、“workshop”、“family”等）
3. **在Unsplash网站上搜索**：查找相关的图片
4. **质量筛选**：优先选择高分辨率的专业图片
5. **缓存图片**：将搜索到的图片保存在本地，避免重复搜索

### 系统要求

- **依赖库**：
  - `ffmpeg`：用于视频合成（使用Homebrew安装`ffmpeg`）
  - `python3`：用于图片处理（依赖PIL/Pillow库）

### API密钥
- **Groq API**：用于音频转录（设置GROQ_API_KEY）
- **Unsplash API**（可选）：用于图片搜索（设置UNSPASH_API_KEY以增加搜索次数）
- **ElevenLabs API**（可选）：如果需要从文本生成TTS的话

### 使用的Python库

### 工作流程示例

- **示例1**：使用TTS生成的睡前故事
```bash
# 1. Generate audio (your voice) via ElevenLabs
tts "Once upon a time..." --voice hjX6Urz6dBwVkFdr87DB --output story.mp3

# 2. Convert to video
story-video generate \
  --audio story.mp3 \
  --text "Once upon a time..." \
  --subtitle-style bold \
  --background-source unsplash \
  --output story-video.mp4

# 3. Upload to YouTube Shorts
# (9:16 format is ready!)
```

- **示例2**：使用现有音频文件并添加自定义章节
```bash
# Create config with specific sections and background queries
cat > config.json << EOF
{
  "title": "The Snail",
  "sections": [
    {
      "start_time": 0,
      "end_time": 20,
      "search_query": "El Paso desert landscape"
    },
    {
      "start_time": 20,
      "end_time": 45,
      "search_query": "3D design studio workspace"
    }
  ]
}
EOF

# Generate video with custom sections
story-video generate \
  --audio narration.mp3 \
  --text transcript.txt \
  --config config.json \
  --output output.mp4
```

- **示例3**：将多个故事制作成一系列YouTube Shorts视频
```bash
# Generate videos for each story
for story in stories/*.txt; do
  audio="${story%.txt}.mp3"
  output="videos/$(basename $story .txt).mp4"
  
  story-video generate \
    --audio "$audio" \
    --text "$story" \
    --subtitle-style elegant \
    --output "$output"
done

# All ready for YouTube Shorts series
ls -lh videos/*.mp4
```

## 常见问题解决方法

- **视频播放速度过快/过慢**：在生成视频前可以使用`ffmpeg -filter:a "atempo=0.9"`命令调整音频速度。
- **背景图片与内容不匹配**：在`config.json`的`sections[]`字段中自定义搜索查询。
- **字幕在明亮背景上难以阅读**：可以尝试使用`--subtitle-style elegant`选项或调整`shadow`配置参数。
- **找不到ffmpeg**：请安装`ffmpeg`。

## 配置资源
- **scripts/generate_video.py**：主要负责视频合成逻辑
- **scripts/transcribe_audio.py**：提取单词的发音时间
- **scripts/search_images.py**：在Unsplash/Pexels网站上搜索图片
- **scripts/subtitlerenderer.py**：负责渲染动画字幕
- **references/ffmpeg_settings.md**：包含针对YouTube Shorts优化的FFmpeg配置
- **references/subtitle_effects.md**：提供可用的字幕效果和自定义选项
- **assetsfonts/****：包含默认字体文件（Inter、Serif作为备用字体）