---
name: pixeldojo
description: 使用 PixelDojo API 生成 AI 图像和视频。支持 60 多种模型，包括 Flux 2、WAN、Veo 3.1、Imagen 4、Kling 等。支持异步任务提交、状态查询以及结果的自动下载。
metadata:
  {
    "clawhub":
      {
        "requires": { 
          "env": ["PIXELDOJO_API_KEY"],
          "bins": ["curl", "jq"]
        },
        "homepage": "https://pixeldojo.ai",
        "source": "https://github.com/blovett80/pixeldojo-skill"
      }
  }
---
# PixelDojo 技能

使用 PixelDojo API 平台生成 AI 图像和视频。

## 设置

1. **获取 API 密钥：** 在 [https://pixeldojo.ai/api-platform](https://pixeldojo.ai/api-platform) 注册
2. **购买信用点数：** 在 [https://pixeldojo.ai/api-platform/buy-credits](https://pixeldojo.ai/api-platform/buy-credits) 购买信用点数
   - **5 美元** = 约 800 张使用 P-Image 模型生成的图像
3. **设置环境变量：**
   ```bash
   export PIXELDOJO_API_KEY=your_api_key_here
   ```
   （或复制 `.env.example` 到 `.env` 文件，并填写您的密钥）

- **API 文档：** [https://pixeldojo.ai/api-platform](https://pixeldojo.ai/api-platform)
- **基础 URL：** `https://pixeldojo.ai/api/v1`

## 可用模型

### 图像模型
- `flux-1.1-pro` - 最新的专业模型，具有更高的图像质量（推荐）
- `flux-1.1-pro-ultra` - 最高质量的 Flux 模型，支持原始图像格式
- `flux-dev` - 开发模型，支持自定义生成步骤和 LoRA 技术
- `flux-krea-dev` - 具有高度真实感的图像模型，避免过度饱和的 AI 效果
- `flux-kontext-pro` - 高级模型，支持图像编辑功能
- `flux-kontext-max` - 高端模型，提供最佳性能

### 视频模型
- `wan-2.6-flash` - 快速视频生成模型
- `wan-2.2` - 更高质量的视频模型
- `veo-3.1` - 使用 Google 的 Veo 3.1 技术生成的视频，支持原生音频
- `kling-2.5-turbo-pro` - 高性能视频生成模型
- `kling-pro` - 专业级视频生成模型
- `minimax` - 最小化资源消耗的视频生成模型

## 核心操作

### 生成图像
```bash
# Basic image generation
bash ~/.openclaw/skills/pixeldojo/generate.sh image "a serene mountain landscape at sunset" flux-2

# With options
bash ~/.openclaw/skills/pixeldojo/generate.sh image "cyberpunk city" flux-2 --aspect-ratio 16:9 --output ~/Desktop/cyberpunk.png
```

### 生成视频
```bash
# Text-to-video
bash ~/.openclaw/skills/pixeldojo/generate.sh video "ocean waves crashing on rocks" wan-2.6-flash --duration 5

# Image-to-video
bash ~/.openclaw/skills/pixeldojo/generate.sh video "make it cinematic" wan-2.6-flash --image-url https://example.com/image.png --duration 5
```

### 检查任务状态
```bash
bash ~/.openclaw/skills/pixeldojo/status.sh job_abc123
```

### 列出可用模型
```bash
bash ~/.openclaw/skills/pixeldojo/models.sh
```

## API 参考

### 提交任务
- **端点：** `POST /api/v1/models/{model}/run`
- **请求头：** `Authorization: Bearer {API_KEY}`, `Content-Type: application/json`
- **请求体（图像）：**
  ```json
  {
    "prompt": "description of image",
    "aspect_ratio": "16:9"
  }
  ```
- **请求体（视频）：**
  ```json
  {
    "prompt": "description of video",
    "image_url": "https://...",  // optional, for image-to-video
    "duration": 5,                // seconds
    "aspect_ratio": "16:9"
  }
  ```
- **响应：**
  ```json
  {
    "jobId": "job_abc123",
    "status": "pending",
    "statusUrl": "https://pixeldojo.ai/api/v1/jobs/job_abc123"
  }
  ```

### 检查任务状态
- **端点：** `GET /api/v1/jobs/{job_id}`
- **请求头：** `Authorization: Bearer {API_KEY}`
- **响应（任务已完成）：**
  ```json
  {
    "jobId": "job_abc123",
    "status": "completed",
    "output": {
      "image": "https://temp.pixeldojo.ai/...png",
      "video": "https://temp.pixeldojo.ai/...mp4"
    }
  }
  ```

### 下载结果
生成的结果会自动保存到 `~/Pictures/AI Generated/` 目录中，文件名包含时间戳，便于查找。

## 工作流程

1. **提交任务：** 调用生成 API，获取任务 ID
2. **检查状态：** 每 2-5 秒检查一次任务状态
3. **下载结果：** 当任务状态变为 “completed” 时，从指定 URL 下载结果
4. **保存结果：** 将文件保存在工作区，并使用描述性文件名保存

## 错误处理

- **请求限制：** 每分钟 10 次请求（如需增加请联系客服）
- **信用点数：** 在控制面板中查看剩余信用点数
- **视频生成时间：** 视频生成可能需要 30-120 秒

## 示例用法
```bash
# Generate a cyberpunk portrait
bash ~/.openclaw/skills/pixeldojo/generate.sh image "cyberpunk samurai with neon lights, detailed, 8k" flux-2 --output ~/Desktop/samurai.png

# Animate a photo
bash ~/.openclaw/skills/pixeldojo/generate.sh video "slow motion drift, cinematic" wan-2.6-flash --image-url https://mycdn.com/photo.jpg --duration 5
```

## 输出路径

所有生成的文件将保存在 **Pictures** 目录中，方便访问：
- `~/Pictures/AI Generated/images/`
- `~/Pictures/AI Generated/videos/`

文件格式为：`{timestamp}_{prompt_snippet}.{ext}`

可以使用 `--output <path>` 参数将文件保存到自定义路径。