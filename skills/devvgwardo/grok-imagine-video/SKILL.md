---
name: grok-imagine-video
description: xAI Grok Imagine API 提供了图像生成、文本转视频、图像转视频以及基于自然语言的图像编辑等功能。当您需要根据文本提示生成图像或视频、编辑现有图像、将静态图像转换为视频，或使用自然语言指令编辑现有视频时，可以使用该 API。该 API 支持在消息传递平台之间进行交互式生成，支持异步轮询、进度更新以及自动交付结果。
metadata: {"openclaw": {"requires": {"env": ["XAI_API_KEY"]}, "primaryEnv": "XAI_API_KEY"}}
---

# Grok Imagine Video

您可以通过消息界面直接使用 xAI 的 Grok Imagine API 生成视频。

## 设置

**重要提示：** 您需要自己的 xAI API 密钥。请从 https://console.x.ai/ 获取密钥。

有关完整的安装说明，请参阅 [README.md](README.md)。

快速设置：
```bash
# Set your xAI API key (YOUR key, not pre-configured)
export XAI_API_KEY="your-api-key-here"
```

## 功能

- **文本转图像**：根据文本描述生成图像（最多可生成 10 个版本）
- **图像编辑**：使用自然语言修改图像
- **文本转视频**：根据文本描述创建视频
- **图像转视频**：将静态图像制作成动画
- **视频编辑**：使用自然语言修改视频
- **异步生成**：通过轮询处理耗时较长的视频任务
- **自动交付**：通过聊天功能下载并发送图像/视频

## 工作流程

### 1. 图像生成

用户输入：**“生成一幅夜景下的赛博朋克城市景观图像”**

```bash
python3 - << 'EOF'
import os
import sys
sys.path.insert(0, 'scripts')
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(os.getenv("XAI_API_KEY"))
result = client.generate_image("A cyberpunk cityscape at night, neon lights reflecting on wet streets")
print(f"Image URL: {result}")
EOF
```

图像会立即生成（无需轮询）。请注意，生成的 URL 是临时的，需尽快下载。

### 1b. 图像编辑

用户输入：**“将这幅图像编辑成水彩画风格”**

```bash
python3 - << 'EOF'
import os
import sys
sys.path.insert(0, 'scripts')
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(os.getenv("XAI_API_KEY"))
result = client.edit_image(
    image_url="https://example.com/photo.jpg",
    prompt="Make it look like a watercolor painting"
)
print(f"Edited image: {result}")
EOF
```

### 2. 文本转视频

用户输入：**“生成一幅海洋日落的视频”**

```bash
# Use the Python client
python3 - << 'EOF'
import os
import sys
sys.path.insert(0, 'scripts')
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(os.getenv("XAI_API_KEY"))
result = client.text_to_video("A beautiful sunset over the ocean", duration=10)
print(f"Job started: {result['job_id']}")
EOF
```

### 3. 等待视频完成

视频生成需要 1-3 分钟。您可以通过轮询来查看生成进度：

```bash
python3 - << 'EOF'
import os
import sys
sys.path.insert(0, 'scripts')
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(os.getenv("XAI_API_KEY"))

def progress(response):
    print(f"Polling... {'Done!' if 'video' in response else 'Pending'}")

final = client.wait_for_completion("request-id-here", progress_callback=progress)
print(f"Video ready: {final['video']['url']}")
EOF
```

### 4. 下载并发送

将完成的视频下载到工作区：

```bash
python3 - << 'EOF'
import os
import sys
sys.path.insert(0, 'scripts')
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(os.getenv("XAI_API_KEY"))
output = "/data/workspace/videos/sunset.mp4"
client.download_video(final, output)  # pass the full response dict
print(f"Downloaded: {output}")
EOF
```

## 图像转视频

将静态图像制作成动画：

```python
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(api_key)
result = client.image_to_video(
    image_url="https://example.com/photo.jpg",
    prompt="Make the clouds move slowly",
    duration=10
)
```

## 视频编辑

编辑现有的视频：

```python
result = client.edit_video(
    video_url="https://example.com/source.mp4",
    edit_prompt="Add a warm sunset filter and slow down to 50% speed"
)
```

## 配置

**重要提示：** 请从 https://console.x.ai/ 获取自己的 API 密钥——切勿使用预配置的密钥。

```bash
export XAI_API_KEY="sk-..."
```

如需将此功能与 OpenClaw 集成，请将其添加到工作区的 `.env` 文件中，或通过网关配置进行管理。

有关完整的设置说明，请参阅 [README.md](README.md)。

## 错误处理

常见错误及相应的处理方式：

- **未经授权 / 未设置 API 密钥**：请从 https://console.x.ai/ 获取密钥，并设置 `export XAI_API_KEY="your-key"`——详情请参阅 README.md
- **请求速率限制**：“请求过多” → 等待片刻后重试
- **内容政策违规**：提示语句违反了内容政策 → 重新表述提示语句
- **超时**：任务耗时过长 → 减少任务时长或复杂性

请始终使用 `try/except` 语句来封装 API 调用，并向用户提供友好的错误信息。

## 最佳实践

**提示语句编写（图像）：**
- 表达要清晰：例如：“以模板艺术风格绘制伦敦地标拼贴画”
- 指定风格：例如：“黎明时分山间湖泊的水彩画”
- 使用多个版本（`n=4`）以获取不同的生成结果

**提示语句编写（视频）：**
- 表达要具体：例如：“一只金毛猎犬在阳光明媚的草地上奔跑”
- 包含拍摄动作：例如：“从左向右缓慢平移镜头”
- 指定光照效果：例如：“使用温暖的黄金时段光线”

**性能提示：**
- 图像会立即生成——无需轮询
- 选择 480p 分辨率以加快视频生成速度，720p 分辨率可获得更高画质
- 除非必要，否则视频时长应控制在 10 秒以内
- 先尝试文本转视频，如有需要再进行编辑

**用户体验：**
- 图像生成完成后会立即发送
- 视频生成过程中会提供进度更新（例如：“视频生成中……已完成 45%”）
- 提供视频生成时间预估（例如：“预计需要 2-3 分钟”
- 完成后确认发送结果（例如：“这是您的图像/视频！”）

## 限制

- 每次请求最多生成 1-10 张图像
- 视频时长限制为 1-15 秒
- 视频分辨率为 480p（默认）或 720p
- 每分钟请求次数限制为 60 次
- 同时处理的任务数量最多为 15 个

有关完整的 API 文档，请参阅 [references/api_reference.md](references/api_reference.md)。

## 与其他功能的集成

- 与 `ffmpeg-video-editor` 结合使用进行后期处理（裁剪、合并、添加滤镜）
- 使用 `fal-ai` 添加额外的视频效果
- 与 `image-generation` 功能结合使用以获取源图像

## 故障排除

- 如果任务状态停留在“待处理”：检查 API 密钥和请求配额
- 如果视频生成速度较慢：尝试使用 720p 分辨率而非 1080p
- 如果任务失败：查看响应中的错误代码（详见 API 文档）
- 如果下载失败：确认视频 URL 是否可访问且未过期