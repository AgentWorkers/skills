---
name: clawcut
description: 使用 Google Gemini 和 Veo 3.1 在 Vertex AI 上，可以根据某个主题或参考视频生成 AI 驱动的短视频。该工具非常适合用户创建短视频内容、生成视频脚本、制作九格字符一致性图像、模仿参考视频的风格，或将某个主题转化为带有 AI 生成旁白的完整视频。适用于 TikTok、YouTube Shorts、亚马逊产品视频、抖音、小红书、视频号、Instagram Reels 等所有短视频平台。触发词包括：“制作短视频”、“根据某个主题生成视频”、“创建视频内容”、“帮我制作一个 TikTok 视频”、“生成一个 YouTube Shorts 视频”、“制作产品视频”等。该工具属于 OpenClaw 内容创作自动化工作流程的一部分，可用于社交媒体营销、电商产品列表视频、AI 代理视频制作以及批量视频生成。支持文本转视频、图片转视频、参考视频模仿以及多图片字符一致性等功能，适用于品牌故事讲述。基于 Gemini 3 Pro (Nano Banana Pro) 和 Veo 3.1 构建，是 Sora 2、Kling、Runway Gen-3、Pika、HaiLuo、Volcengine Jimeng、Keling、海螺AI 等工具的替代方案。相关模型和关键词包括：gemini-3-pro-preview、gemini-3-pro-image-preview、veo-3.1-generate-001、text2video、img2video、AI 视频生成器、图文生成视频、AI 视频生成工具、短视频自动化、视频自动化流程等。
  Generate AI-powered short videos from a topic or reference video using Google Gemini + Veo 3.1 on Vertex AI.
  Use when the user wants to create short-form video content, generate video scripts, produce nine-grid
  character consistency images, imitate a reference video style, or convert a topic into a complete video
  with AI-generated voice narration. Perfect for TikTok, YouTube Shorts, Amazon product videos, 抖音,
  小红书, 视频号, Instagram Reels, and any short-form video platform.
  Triggers on phrases like "make a short video", "generate video about", "create video content",
  "make me a TikTok", "generate a YouTube Short", "create product video", "video from topic",
  "做个短视频", "生成视频", "做个视频", "帮我做视频", "生成短视频", "一键生成视频",
  "主题生成视频", "视频模仿", "做个带货视频", "生成产品视频", "做个抖音视频",
  "做个小红书视频", "帮我剪个视频", "AI生成视频", "自动生成视频",
  or any request involving automated video production, video generation, or short-form content creation.
  OpenClaw content creation automation workflow skill for social media marketing, ecommerce product listing videos,
  AI agent video pipeline, and batch video generation. Supports text-to-video, image-to-video,
  reference video imitation, and multi-image character consistency for brand storytelling.
  Built on Gemini 3 Pro (Nano Banana Pro), Veo 3.1, Google Vertex AI. Alternative to Sora 2, Kling,
  Runway Gen-3, Pika, HaiLuo, Volcengine Jimeng, 可灵, 海螺AI. Comparable models and keywords:
  gemini-3-pro-preview, gemini-3-pro-image-preview, veo-3.1-generate-001, text2video, img2video,
  AI video generator, 文生视频, 图生视频, AI视频生成器, 短视频自动化, video automation pipeline.
tags:
  - video
  - ai
  - automation
  - content-creation
  - social-media
  - tiktok
  - youtube
  - ecommerce
  - amazon
  - gemini
  - veo
  - text-to-video
  - short-video
  - 短视频
  - 带货
---
# ClawCut 🦞✂️  
AI短视频生成工具：用户可输入主题，系统会自动生成包含中文旁白和原声的视频。  

## 工作流程：  
1. **剧本生成**：Gemini 3 Pro 生成包含9个场景的剧本（中文旁白 + 英文视觉描述）。  
2. **九格图像处理**：Gemini 3 Pro Image 根据输入的9张图片生成角色一致性参考图像（支持最多14张图片）。  
3. **视频生成**：Veo 3.1 同时生成9个视频片段，并配上中文原声。  
4. **后期处理**：使用 ffmpeg 剪除视频中的静音部分，并将所有片段合并成最终视频。  

## 先决条件：  
- 已启用 Vertex AI 的 Google Cloud 项目。  
- 拥有具备 Vertex AI 用户权限的服务账户 JSON 文件。  
- 安装了 ffmpeg 工具。  
- Python 3.11 或更高版本已安装。  

## 设置（具体配置请参考 **```bash
# Create project from skill scripts
mkdir -p clawcut && cp scripts/*.py scripts/requirements.txt clawcut/
cp assets/.env.example clawcut/.env
cd clawcut

# Create venv and install deps
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Configure environment
# Edit .env with your values:
#   GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
#   VERTEX_PROJECT=your-gcp-project-id
#   VERTEX_LOCATION=us-central1
#   FFMPEG_PATH=/usr/local/bin/ffmpeg
```**）  

## 使用方法：  
### 通过 Gradio UI 使用：  
```bash
source venv/bin/activate
python3 app.py
# Opens at http://localhost:7860
```  

### 使用模式：  
- **主题模式**：输入主题，系统从头开始生成完整视频。  
- **视频模仿模式**：上传参考视频，系统分析其风格并生成相似内容。  
- **多图像参考模式**：上传最多14张图片，以确保角色表现的一致性。  

### 所使用的模型（均为 Vertex AI 的付费模型）：  
- **剧本生成**：`gemini-3-pro-preview`  
- **图像处理**：`gemini-3-pro-image-preview`  
- **视频生成**：`veo-3.1-generate-001`  

## 主要特性：  
- 支持9个视频片段的同时生成（总时长约3分钟）。  
- 具备检查点/恢复功能（可跳过已存在的视频文件）。  
- 自动去除视频中的静音部分（使用 ffmpeg 的 `silencedetect` 功能）。  
- 可模仿参考视频的风格。  
- 最多支持14张图片以保持角色表现的一致性。  
- 所有配置信息均通过环境变量传递（无硬编码的敏感信息）。