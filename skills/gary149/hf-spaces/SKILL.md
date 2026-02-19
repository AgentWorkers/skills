---
name: hf-spaces
description: 使用 HuggingFace Spaces 和推理提供者（Inference Providers）可以直接生成图片、视频、音频等媒体文件。支持批量生成（例如：“生成 10 张图片”），也可以链接多个 HuggingFace Spaces 来完成不同的任务。适用于以下场景：生成图片、创建视频、文本转语音、批量生成内容、使用 Gradio Space、调用 HuggingFace 的模型，以及任何不需要构建复杂数据流（dag）的 AI 生成任务。相关触发命令包括：“generate images”（生成图片）、”create a video”（创建视频）、”text to speech”（文本转语音）、”use this Space”（使用该 HuggingFace Space）、”batch generate”（批量生成）、”generate 10 images”（生成 10 张图片）、”image generation”（图片生成）、”video generation”（视频生成）。
---
# hf-spaces

您可以使用 HuggingFace Spaces 和推理提供者（Inference Providers），通过 `gradio_client` 或 MCP 工具直接生成 AI 内容（图片、视频、音频、文本）。

## 当 MCP 工具可用时

检查是否存在相关的 MCP 工具（例如，用于生成图片的 `mcp__claude_ai_HF__gr1_z_image_turbo_generate`，用于生成视频的 `mcp__claude_ai_HF__gr2_ltx_2_turbo_generate`）。如果存在，请直接使用这些工具——无需编写脚本。

**使用 MCP 工具批量生成：** 可以多次调用该工具（顺序调用或并行调用）来生成多个输出。

## 编写脚本时

使用 `gradio_client` 来操作 HuggingFace Spaces，使用 `huggingface_hub` 来操作推理提供者。

### 设置

```bash
uv init && uv add gradio_client huggingface_hub
```

### 使用 Gradio Space

```python
from gradio_client import Client

client = Client("owner/space-name")
result = client.predict(param1="value", param2="value", api_name="/endpoint")
```

### 使用 HuggingFace 推理提供者

```python
from huggingface_hub import InferenceClient

client = InferenceClient(provider="fal-ai")  # or replicate, together, etc.
image = client.text_to_image("a cat in space", model="black-forest-labs/FLUX.1-schnell")
image.save("output.png")
```

### 批量生成

```python
from gradio_client import Client

client = Client("Tongyi-MAI/Z-Image-Turbo")
prompts = [f"A cute cat in style {i}" for i in range(10)]

for i, prompt in enumerate(prompts):
    result = client.predict(
        prompt=prompt,
        resolution="1024x1024 ( 1:1 )",
        random_seed=True,
        api_name="/generate",
    )
    images, seed_str, seed_int = result
    print(f"Generated image {i}: {images[0]['image']}")
```

### 链接多个 HuggingFace Spaces

```python
from gradio_client import Client

img_client = Client("Tongyi-MAI/Z-Image-Turbo")
vid_client = Client("alexnasa/ltx-2-TURBO")

result = img_client.predict(prompt="a sunset", resolution="1024x1024 ( 1:1 )", random_seed=True, api_name="/generate")
image_path = result[0][0]["image"]

video = vid_client.predict(first_frame=image_path, prompt="cinematic motion", duration=5, api_name="/generate_video")
print(f"Video: {video[0]}")
```

## 查找 HuggingFace Spaces

- **语义搜索：** 输入您需要的内容：
  `https://huggingface.co/api/spaces/semantic-search?q=generate+music+for+a+video&sdk=gradio&includeNonRunning=false`
- **按类别搜索：**
  `https://huggingface.co/api/spaces/semantic-search?category=image-generation&sdk=gradio&includeNonRunning=false`
  可用的类别包括：图片生成（image-generation）、视频生成（video-generation）、文本生成（text-generation）、语音合成（speech-synthesis）、音乐生成（music-generation）、声音克隆（voice-cloning）、图片编辑（image-editing）、背景去除（background-removal）、图片缩放（image-upscaling）、光学字符识别（ocr）、风格转换（style-transfer）、图片加标题（image-captioning）。
  如果可用，还可以使用 `mcp__claude_ai_HF__space_search` 工具进行搜索。

## 查找模型（推理提供者）

`https://huggingface.co/api/models?inference_provider=all&pipeline_tag=text-to-image`
  可用的管道标签（Pipeline Tags）包括：文本转图片（text-to-image）、图片转图片（image-to-image）、图片转文本（image-to-text）、图片转视频（image-to-video）、文本转视频（text-to-video）、文本转语音（text-to-speech）、自动语音识别（automatic-speech-recognition）。
  VLM/LLM 模型：`https://router.huggingface.co/v1/models`

## 检查 HuggingFace Space 的 API

```bash
curl -s "https://<space-subdomain>.hf.space/gradio_api/openapi.json"
```

请将 `<space-subdomain>` 替换为连字符分隔的小写形式（例如，`Tongyi-MAI/Z-Image-Turbo` 应替换为 `tongyi-mai-z-image-turbo`）。HuggingFace Spaces 的页脚中通常会有“通过 API 使用”（Use via API）的链接。

## 处理生成的文件

Gradio 会返回文件字典（file dictionaries）：
```python
path = file.get("path") if isinstance(file, dict) else file
```

## 认证

对于需要 ZeroGPU 功能的 HuggingFace Spaces 和推理提供者，认证是必需的。在进行任何需要认证的调用之前，请先检查是否有有效的令牌：
```bash
python3 -c "from huggingface_hub import get_token; t = get_token(); print('HF token found' if t else 'NO TOKEN')"
```

如果未找到令牌，请让用户访问以下链接创建令牌：
`https://huggingface.co/settings/tokens/new?ownUserPermissions=inference.serverless.write&tokenType=fineGrained`
然后让用户运行 `hf auth login`，或在他们的环境中设置 `HF_TOKEN`。

## 常用的 HuggingFace Spaces

```python
# Image Generation
Client("Tongyi-MAI/Z-Image-Turbo").predict(prompt="...", resolution="1024x1024 ( 1:1 )", random_seed=True, api_name="/generate")

# Text-to-Speech
Client("Qwen/Qwen3-TTS").predict(text="...", language="English", voice_description="...", api_name="/generate_voice_design")

# Image-to-Video
Client("alexnasa/ltx-2-TURBO").predict(first_frame="path.png", prompt="...", duration=5, api_name="/generate_video")
```