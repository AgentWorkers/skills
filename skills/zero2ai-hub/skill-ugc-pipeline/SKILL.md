---
name: skill-ugc-pipeline
version: 1.2.0
description: >
  端到端的人工智能用户生成（UGC）视频制作流程：  
  产品信息 → 使用 GPT-4o-mini 脚本生成视频内容 → ElevenLabs 提供旁白服务 → Aurora 模型进行人物对话（由 fal-ai/creatify/aurora 提供技术支持） → 使用 Kling 2.6 Pro 软件制作产品背景视频 → 添加同步字幕 → 对视频进行后期处理（包括调整画质、消除手抖效果、优化人物形象等） → 最终生成 MP4 格式的视频文件。  
  整个制作流程的成本约为每段视频 1.75 美元。
requires:
  env:
    - FAL_KEY
    - ELEVENLABS_API_KEY
    - OPENAI_API_KEY
  bins:
    - node
    - ffmpeg
    - uv
---
# skill-ugc-pipeline v1.2.0

您可以自行构建一个MakeUGC（Make User-Generated Content）流程。该流程支持直接通过API进行操作，无需每月支付300美元的企业级费用。

**默认模型：Aurora**（`fal-ai/creatify/aurora`）——在A/B测试后锁定为默认模型。  
与其它模型相比，Aurora生成的唇部同步效果和旁白更加真实自然。

## v1.2.0的新功能  
- **B-roll片段拼接**：Kling 2.6 Pro工具能够将图像转换为视频，并根据配置的时间码将其插入到虚拟角色的视频中，从而生成更具电影感的片段。  
- **UGC滤镜**：仅对虚拟角色的部分应用颗粒感效果和手持拍摄的抖动效果；产品相关的B-roll片段保持清晰、专业的视觉效果。  
- 拼接点之间的音频连续播放（无音频间隙）。

## 架构  

```
product info → [GPT-4o-mini] → script
                             → [ElevenLabs] → audio.mp3
avatar image + audio         → [fal.ai Aurora] → avatar.mp4
product image                → [Kling 2.6 Pro] → broll.mp4
avatar + broll + ugc-filter  → [ffmpeg] → final.mp4
audio.mp3                    → [OpenAI Whisper] → captions overlay
```

## 完整流程（共6个步骤）  

```
1. Script       GPT-4o-mini → spoken script
2. Voice        ElevenLabs → audio.mp3
3. Avatar       fal-ai/creatify/aurora → talking head MP4
4. B-roll       Kling 2.6 Pro image-to-video → product shot
5. Splice       ffmpeg: avatar(hook) + broll + avatar(resume) + continuous audio
6. Captions     Whisper word-level → overlay.py → final MP4
7. UGC filter   grain + handheld shake on avatar ONLY (product shot stays clean)
```

## 快速入门——完整流程  

```bash
cd skill-ugc-pipeline
npm install

# Step 1-3: Script + voice + avatar
node scripts/generate.js \
  --product "Rain Cloud Humidifier" \
  --product-desc "USB cool mist humidifier. 300ml tank, LED glow, silent mode." \
  --avatar avatars/my_avatar.png \
  --output output/ad_raincloud.mp4

# Step 4-5: Add B-roll + UGC filter
node scripts/broll.js \
  --avatar-video output/ad_raincloud_aurora.mp4 \
  --audio output/ad_raincloud_audio.mp3 \
  --product-image https://example.com/product.jpg \
  --product-name "Rain Cloud Humidifier" \
  --splice-at 4.5 \
  --broll-duration 5 \
  --ugc-filter \
  --output output/final.mp4

# Step 6: Whisper captions
node scripts/transcribe_captions.js \
  --audio output/ad_raincloud_audio.mp3 \
  --video output/final.mp4 \
  --output output/final_captioned.mp4
```

## 脚本  

| 脚本 | 描述 |
|--------|-------------|
| `generate.js` | 主要流程：处理脚本内容 → 添加语音 → 生成Aurora虚拟角色的视频 |
| `broll.js` | 拼接B-roll片段；可选应用UGC滤镜（为虚拟角色添加颗粒感效果和抖动效果） |
| `transcribe_captions.js` | 为视频添加字幕（Whisper API提供） |
| `aurora_only.js` | 仅生成Aurora虚拟角色的视频（跳过脚本和语音处理） |
| `batch.js` | 为多个产品批量执行整个流程 |
| `product_in_hand.js` | 生成产品手握状态的合成图像 |

## `broll.js` 的参数选项  

| 参数 | 默认值 | 描述 |
|------|---------|-------------|
| `--avatar-video` | 必需 | Aurora虚拟角色视频的MP4路径 |
| `--audio` | 必需 | 原始旁白的MP3文件（持续播放） |
| `--product-image` | 必需 | 产品图片的URL或本地路径 |
| `--product-name` | 必需 | 产品名称（用于Kling提示中显示） |
| `--splice-at` | `4.5` | B-roll片段插入到虚拟角色视频中的时间点（以秒为单位） |
| `--broll-duration` | `5` | B-roll片段的时长（5秒或10秒） |
| `--ugc-filter` | `off` | 为虚拟角色添加颗粒感效果和抖动效果（产品部分保持原样） |
| `--output` | 必需 | 输出视频的MP4路径 |

## 成本估算  

| 流程步骤 | 使用的模型 | 成本（每视频） |
|------|-------|-----------|
| 脚本处理 | GPT-4o-mini | 约0.01美元 |
| 语音处理 | ElevenLabs | 约0.05美元 |
| 虚拟角色生成 | Aurora（fal.ai） | 约1.00美元 |
| B-roll片段处理 | Kling 2.6 Pro（fal.ai） | 约0.40美元 |
| 字幕添加 | Whisper API | 约0.01美元 |
| **总计** | | 约1.47–1.75美元 |

## 所需工具/许可证  
- `FAL_KEY`：fal.ai的API密钥（用于Aurora和Kling功能）  
- `ELEVENLABS_API_KEY`：ElevenLabs的API密钥 |
- `OPENAI_API_KEY`：OpenAI的API密钥（用于GPT-4o-mini和Whisper功能） |
- `ffmpeg`：用于视频拼接和UGC滤镜处理 |
- `uv`：用于通过`skill-tiktok-ads-video`工具添加字幕 |

## 虚拟角色要求  
- 使用肖像照片，面部清晰可见（避免浓妆或可能遮挡嘴巴的配饰）  
- 分辨率：最低512×512像素，推荐1024×1024像素  
- 文件格式：PNG或JPG