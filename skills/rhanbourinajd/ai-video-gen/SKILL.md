---
name: ai-video-gen
description: 端到端的AI视频生成技术——通过图像生成、视频合成、旁白以及编辑功能，根据文本提示创建视频。支持使用OpenAI的DALL-E模型、Replicate模型、LumaAI模型以及FFmpeg进行视频编辑。
---

# 人工智能视频生成技能

使用人工智能根据文本描述生成完整的视频。

## 功能

1. **图像生成** - DALL-E 3、Stable Diffusion、Flux
2. **视频生成** - LumaAI、Runway、Replicate模型
3. **旁白** - OpenAI TTS、ElevenLabs
4. **视频编辑** - 使用FFmpeg进行剪辑、添加过渡效果和叠加层

## 快速入门

```bash
# Generate a complete video
python skills/ai-video-gen/generate_video.py --prompt "A sunset over mountains" --output sunset.mp4

# Just images to video
python skills/ai-video-gen/images_to_video.py --images img1.png img2.png --output result.mp4

# Add voiceover
python skills/ai-video-gen/add_voiceover.py --video input.mp4 --text "Your narration" --output final.mp4
```

## 设置

### 所需的API密钥

将API密钥添加到您的环境变量或`.env`文件中：

```bash
# Image Generation (pick one)
OPENAI_API_KEY=sk-...              # DALL-E 3
REPLICATE_API_TOKEN=r8_...         # Stable Diffusion, Flux

# Video Generation (pick one)
LUMAAI_API_KEY=luma_...           # LumaAI Dream Machine
RUNWAY_API_KEY=...                # Runway ML
REPLICATE_API_TOKEN=r8_...        # Multiple models

# Voice (optional)
OPENAI_API_KEY=sk-...             # OpenAI TTS
ELEVENLABS_API_KEY=...            # ElevenLabs

# Or use FREE local options (no API needed)
```

### 安装依赖项

```bash
pip install openai requests pillow replicate python-dotenv
```

### FFmpeg

已通过Winget安装。

## 使用示例

### 1. 从文本生成视频（完整流程）

```bash
python skills/ai-video-gen/generate_video.py \
  --prompt "A futuristic city at night with flying cars" \
  --duration 5 \
  --voiceover "Welcome to the future" \
  --output future_city.mp4
```

### 2. 多个场景

```bash
python skills/ai-video-gen/multi_scene.py \
  --scenes "Morning sunrise" "Busy city street" "Peaceful night" \
  --duration 3 \
  --output day_in_life.mp4
```

### 从图像序列生成视频

```bash
python skills/ai-video-gen/images_to_video.py \
  --images frame1.png frame2.png frame3.png \
  --fps 24 \
  --output animation.mp4
```

## 工作流程选项

### 经济模式（免费）
- 图像：使用Stable Diffusion（本地资源或免费API）
- 视频：使用开源模型
- 旁白：使用OpenAI TTS（价格较低）或免费TTS服务
- 编辑：使用FFmpeg

### 高质量模式（付费）
- 图像：使用DALL-E 3或Midjourney
- 视频：使用Runway Gen-3或LumaAI
- 旁白：使用ElevenLabs
- 编辑：使用FFmpeg并添加特效

## 脚本参考

- `generate_video.py` - 主要的端到端生成脚本
- `images_to_video.py` - 将图像序列转换为视频
- `add_voiceover.py` - 为现有视频添加旁白
- `multi_scene.py` - 创建多场景视频
- `edit_video.py` - 应用特效、过渡效果和叠加层

## API费用估算

- **DALL-E 3**：每张图片约0.04-0.08美元
- **Replicate**：每次生成约0.01-0.10美元
- **LumaAI**：每5秒0.50美元（提供免费 tier）
- **Runway**：每秒约0.05美元
- **OpenAI TTS**：每1000个字符约0.015美元
- **ElevenLabs**：每1000个字符约0.30美元（提供更高质量的服务）

## 示例

请查看`examples/`文件夹中的示例输出和提示。