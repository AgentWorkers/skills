---
name: fal-ai
description: 使用 fal.ai API（如 Flux、Gemini Image 等）生成图片和媒体文件。适用于需要生成图片、运行 AI 图像模型、创建视觉素材或任何与 fal.ai 相关的任务。该系统支持基于队列的请求处理，并具备自动轮询功能。
---

# fal.ai 集成

通过 fal.ai 的基于队列的 API 生成和编辑图片。

## 设置

将您的 API 密钥添加到 `TOOLS.md` 文件中：

```markdown
### fal.ai
FAL_KEY: your-key-here
```

您可以在以下链接获取 API 密钥：https://fal.ai/dashboard/keys

脚本会按顺序检查以下内容：`FAL_KEY` 环境变量 → `TOOLS.md` 文件

## 支持的模型

### fal-ai/nano-banana-pro (文本 → 图像)
使用 Google 的 Gemini 3 Pro 进行文本到图像的转换。

```python
input_data = {
    "prompt": "A cat astronaut on the moon",      # required
    "aspect_ratio": "1:1",                        # auto|21:9|16:9|3:2|4:3|5:4|1:1|4:5|3:4|2:3|9:16
    "resolution": "1K",                           # 1K|2K|4K
    "output_format": "png",                       # jpeg|png|webp
    "safety_tolerance": "4"                       # 1 (strict) to 6 (permissive)
}
```

### fal-ai/nano-banana-pro/edit (图像 → 图像)
使用 Gemini 3 Pro 进行图像编辑。处理速度较慢（约 20 秒），但能很好地处理复杂的编辑操作。

```python
input_data = {
    "prompt": "Transform into anime style",       # required
    "image_urls": [image_data_uri],               # required - array of URLs or base64 data URIs
    "aspect_ratio": "auto",
    "resolution": "1K",
    "output_format": "png"
}
```

### fal-ai/flux/dev/image-to-image (图像 → 图像)
使用 FLUX.1 开发模型。转换速度较快（约 2-3 秒），适用于风格转换。

```python
input_data = {
    "prompt": "Anime style portrait",             # required
    "image_url": image_data_uri,                  # required - single URL or base64 data URI
    "strength": 0.85,                             # 0-1, higher = more change
    "num_inference_steps": 40,
    "guidance_scale": 7.5,
    "output_format": "png"
}
```

### fal-ai/kling-video/o3/pro/video-to-video/edit (视频 → 视频)
使用 Kling O3 Pro 进行带有 AI 效果的视频转换。

**限制：**
- 格式：仅支持 `.mp4` 和 `.mov` 格式
- 时长：3-10 秒
- 分辨率：720-2160px
- 最大文件大小：200MB
- 最多元素数量：4 个（包括元素和参考图片）

```python
input_data = {
    # Required
    "prompt": "Change environment to be fully snow as @Image1. Replace animal with @Element1",
    "video_url": "https://example.com/video.mp4",    # .mp4/.mov, 3-10s, 720-2160px, max 200MB
    
    # Optional
    "image_urls": [                                  # style/appearance references
        "https://example.com/snow_ref.jpg"           # use as @Image1, @Image2 in prompt
    ],
    "keep_audio": True,                              # keep original audio (default: true)
    "elements": [                                    # characters/objects to inject
        {
            "reference_image_urls": [                # reference images for the element
                "https://example.com/element_ref1.png"
            ],
            "frontal_image_url": "https://example.com/element_front.png"  # frontal view (better results)
        }
    ],                                               # use as @Element1, @Element2 in prompt
    "shot_type": "customize"                         # multi-shot type (default: customize)
}
```

**提示参考：**
- `@Video1` — 输入视频
- `@Image1`, `@Image2` — 用于风格/外观参考的图片
- `@Element1`, `@Element2` — 需要插入的元素（角色/对象）

## 输入验证

该技能会在提交前验证输入内容。对于支持多输入的模型，请确保提供了所有必需的字段：

```bash
# Check what a model needs
python3 scripts/fal_client.py model-info "fal-ai/kling-video/o3/standard/video-to-video/edit"

# List all models with their requirements
python3 scripts/fal_client.py models
```

**提交前请确认：**
- ✅ 所有必需的字段都已填写且不为空
- ✅ 文件字段（如 `image_url`, `video_url` 等）是有效的 URL 或 Base64 数据 URI
- ✅ 数组（如 `image_urls`）至少包含一个元素
- ✅ 视频文件符合大小（200MB）和分辨率（720-2160px）的限制

**示例验证输出：**
```
⚠️  Note: Reference video in prompt as @Video1
⚠️  Note: Max 4 total elements (video + images combined)
❌ Validation failed:
   - Missing required field: video_url
```

## 使用方法

### 命令行接口（CLI）命令

```bash
# Check API key
python3 scripts/fal_client.py check-key

# Submit a request
python3 scripts/fal_client.py submit "fal-ai/nano-banana-pro" '{"prompt": "A sunset over mountains"}'

# Check status
python3 scripts/fal_client.py status "fal-ai/nano-banana-pro" "<request_id>"

# Get result
python3 scripts/fal_client.py result "fal-ai/nano-banana-pro" "<request_id>"

# Poll all pending requests
python3 scripts/fal_client.py poll

# List pending requests
python3 scripts/fal_client.py list

# Convert local image to base64 data URI
python3 scripts/fal_client.py to-data-uri /path/to/image.jpg

# Convert local video to base64 data URI (with validation)
python3 scripts/fal_client.py video-to-uri /path/to/video.mp4
```

### Python 使用方法

```python
import sys
sys.path.insert(0, 'scripts')
from fal_client import submit, check_status, get_result, image_to_data_uri, poll_pending

# Text to image
result = submit('fal-ai/nano-banana-pro', {
    'prompt': 'A futuristic city at night'
})
print(result['request_id'])

# Image to image (with local file)
img_uri = image_to_data_uri('/path/to/photo.jpg')
result = submit('fal-ai/nano-banana-pro/edit', {
    'prompt': 'Transform into watercolor painting',
    'image_urls': [img_uri]
})

# Poll until complete
completed = poll_pending()
for req in completed:
    if 'result' in req:
        print(req['result']['images'][0]['url'])
```

## 队列系统

fal.ai 使用异步队列。请求会经历以下状态：
- `IN_QUEUE` — 等待中
- `IN_PROGRESS` — 生成中
- `COMPLETED` — 完成，可以获取结果
- `FAILED` — 发生错误

待处理的请求会被保存在 `~/.openclaw/workspace/fal-pending.json` 文件中，重启后请求会继续处理。

### 轮询策略

**手动轮询：** 定期运行 `python3 scripts/fal_client.py poll` 命令。

**心跳检测：** 在 `HEARTBEAT.md` 文件中配置心跳检测机制：

```markdown
- Poll fal.ai pending requests if any exist
```

**定时任务：** 使用 Cron 任务每隔几分钟自动执行一次轮询。

## 添加新模型

1. 在 fal.ai 上找到所需模型，并查看其 `/api` 页面。
2. 在 `references/models.json` 文件中添加该模型的信息（包括输入/输出格式）。
3. 用简单的请求测试该模型。

**注意：** 队列请求的 URL 应使用模型的基础路径（例如 `fal-ai/flux`，而不是 `fal-ai/flux/dev/image-to-image`）。脚本会自动处理路径匹配问题。

## 相关文件

```
skills/fal-ai/
├── SKILL.md                    ← This file
├── scripts/
│   └── fal_client.py           ← CLI + Python library
└── references/
    └── models.json             ← Model schemas
```

## 故障排除

- **“未找到 FAL_KEY”**：请将 API 密钥添加到 `TOOLS.md` 文件中，或设置 `FAL_KEY` 环境变量。
- **405 方法不允许**：可能是 URL 路由问题，请确保使用正确的模型路径来获取状态或结果。
- **请求卡住**：检查 `fal-pending.json` 文件，可能需要手动清理队列中的待处理请求。