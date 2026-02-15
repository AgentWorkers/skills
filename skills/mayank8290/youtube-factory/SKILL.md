---
name: youtube-factory
description: 根据单个提示生成完整的 YouTube 视频：包括脚本、旁白、素材片段、字幕以及缩略图。整个过程完全独立，无需使用任何外部模块。所有工具均为免费。
version: 1.1.0
author: Mayank8290
homepage: https://github.com/Mayank8290/openclaw-video-skills
tags: video, youtube, content-creation, tts, automation, faceless
metadata: { "openclaw": { "requires": { "bins": ["ffmpeg", "edge-tts"], "env": ["PEXELS_API_KEY"] }, "primaryEnv": "PEXELS_API_KEY" } }
---

# YouTube Factory

该工具能够根据用户提供的单一提示自动生成完整的YouTube视频，包括脚本、旁白、素材片段、字幕和缩略图——所有步骤均为自动化完成。

**100% 免费工具**——无需使用任何昂贵的API。

> **喜欢这个工具吗？** 请支持创作者，帮助我们保持其免费：**[请为我买杯咖啡](https://buymeacoffee.com/mayank8290)**

## 该工具的功能

可以将任何主题转化为适合发布的YouTube视频：

1. **脚本生成**：利用大型语言模型（LLM）编写引人入胜的脚本。
2. **旁白**：使用免费的Microsoft Edge TTS服务（提供自然发音的配音）。
3. **素材片段**：自动从Pexels网站获取相关的背景视频（完全免费）。
4. **视频剪辑**：使用FFmpeg将所有元素无缝整合在一起。
5. **字幕**：为视频添加风格化的字幕。
6. **缩略图**：自动生成可点击的缩略图。

## 快速入门

```
Create a YouTube video about "5 Morning Habits of Successful People"
```

```
Make a faceless YouTube video:
- Topic: How AI is changing healthcare
- Style: Documentary
- Length: 8 minutes
- Voice: Professional male
```

## 命令

### 生成完整视频
```
/youtube-factory [topic]
```
生成包含所有元素的完整视频。

### 仅生成脚本
```
/youtube-factory script [topic] --length [minutes]
```
仅生成脚本，供用户审核或编辑。

### 自定义旁白
```
/youtube-factory [topic] --voice [voice-name]
```

提供的免费旁白声音：
- `en-US-ChristopherNeural` – 男性，专业风格（默认）
- `en-US-JennyNeural` – 女性，亲切风格
- `en-US-GuyNeural` – 男性，休闲风格
- `en-US-AriaNeural` – 女性，新闻播报风格
- `en-GB-SoniaNeural` – 英国女性
- `en-AU-NatashaNeural` – 澳大利亚女性

### 视频风格
```
/youtube-factory [topic] --style [style]
```

可选的视频风格：
- **纪录片**：严肃、信息丰富的风格（默认）
- **列表文章**：采用“Top 10”格式，结构清晰
- **教程**：分步骤的教学视频
- **故事**：叙事式的视频内容

### 短视频模式（9:16比例）
```
/youtube-factory [topic] --shorts
```
生成适合YouTube Shorts、TikTok和Reels平台的60秒竖版视频。

## 输出文件

生成完成后，视频文件将保存在 `~/Videos/OpenClaw/` 目录下：

```
your-video-title/
├── script.md          # The full script
├── voiceover.mp3      # Audio track
├── video_raw.mp4      # Without captions
├── video_final.mp4    # With captions (upload this!)
├── thumbnail.jpg      # YouTube thumbnail
└── metadata.json      # Title, description, tags
```

## 使用要求

- 需要免费的Pexels API密钥（获取地址：https://pexels.com/api）
- 确保已安装FFmpeg（命令：`brew install ffmpeg`）
- 安装Edge TTS插件（命令：`pip install edge-tts`）

## 设置指南

```bash
# Install dependencies
brew install ffmpeg
pip install edge-tts pillow python-dotenv requests

# Add Pexels API key
echo "PEXELS_API_KEY=your_key" >> ~/.openclaw-video-skills/config.env
```

## 盈利方式

| 盈利方式 | 潜在收益 |
|--------|-----------|
| Fiverr/Upwork服务 | 每个视频200-500美元 |
| 月度固定费用 | 每个客户1,500-3,000美元 |
| 自己的YouTube频道 | 每月通过AdSense收入2,000-10,000美元 |
| 在ClawHub上出售该技能 | 每个技能50-150美元 |

## 使用示例

- **Faceless Finance频道**  
- **快速短视频**  
- **教程内容**  

---

## 支持本项目

如果这个工具为您节省了时间或带来了收入，请考虑请我喝杯咖啡！

**[请为我买杯咖啡](https://buymeacoffee.com/mayank8290)**

每一杯咖啡都能帮助我为社区开发更多免费工具。

---

专为OpenClaw平台开发 | 100% 免费工具 | [支持创作者](https://buymeacoffee.com/mayank8290)