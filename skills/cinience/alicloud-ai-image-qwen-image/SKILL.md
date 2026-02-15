---
name: alicloud-ai-image-qwen-image
description: 使用 Model Studio DashScope SDK 和 Qwen 的图像生成模型（qwen-image-max、qwen-image-plus-2026-01-09）来生成图像。这些模型适用于实现或记录 `image.generate` 请求/响应的功能，以及处理提示词（prompt/negativeprompt）、图像尺寸（size）、随机种子值（seed）和参考图像（reference_image）的映射。同时，这些模型也可用于将图像生成功能集成到视频代理（video-agent）的流程中。
---

**类别：提供者（Provider）**

# Model Studio Qwen Image

通过标准化 `image.generate` 的输入/输出，并使用 DashScope SDK（Python）以及精确的模型名称，为视频代理流程（video-agent pipeline）提供一致的图像生成行为。

## 先决条件

- 安装 SDK（建议在虚拟环境（venv）中安装，以避免违反 PEP 668 的限制）：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

- 在您的环境中设置 `DASHSCOPE_API_KEY`，或将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中（环境变量优先生效）。

## 关键模型名称

使用以下精确的模型名称之一：
- `qwen-image-max`
- `qwen-image-plus-2026-01-09`

## 标准化接口（image.generate）

### 请求参数
- `prompt`（字符串，必填）：描述一个场景，而不仅仅是关键词。
- `negative_prompt`（字符串，可选）：后端可能会忽略此参数。
- `size`（字符串，必填）：例如 `1024*1024`、`768*1024`。
- `style`（字符串，可选）：可选的样式提示。
- `seed`（整数，可选）：在支持的情况下用于保证生成的图像一致性。
- `reference_image`（字符串 | 字节串，可选）：参考图像的路径或数据。

### 响应参数
- `image_url`（字符串）：生成的图像 URL。
- `width`（整数）：图像的宽度。
- `height`（整数）：图像的高度。
- `seed`（整数）：用于生成图像的随机数。

## 快速入门（标准化请求 + 预览）

最小的标准化请求体示例：

```json
{
  "prompt": "a cinematic portrait of a cyclist at dusk, soft rim light, shallow depth of field",
  "negative_prompt": "blurry, low quality, watermark",
  "size": "1024*1024",
  "seed": 1234
}
```

预览流程（下载后打开图像）：

```bash
curl -L -o output/ai-image-qwen-image/images/preview.png "<IMAGE_URL_FROM_RESPONSE>" && open output/ai-image-qwen-image/images/preview.png
```

本地辅助脚本（将 JSON 请求转换为图像文件）：

```bash
python skills/ai/image/alicloud-ai-image-qwen-image/scripts/generate_image.py \\
  --request '{"prompt":"a studio product photo of headphones","size":"1024*1024"}' \\
  --output output/ai-image-qwen-image/images/headphones.png \\
  --print-response
```

## 参数说明

| 参数 | 是否必填 | 备注 |
|------|----------|-------|
| `prompt` | 是 | 请描述一个完整的场景，而不仅仅是关键词。 |
| `negative_prompt` | 否 | 后端可能会忽略此参数。 |
| `size` | 是 | 使用 `WxH` 格式，例如 `1024*1024`、`768*1024`。 |
| `style` | 否 | 可选的样式提示。 |
| `seed` | 否 | 在支持的情况下使用此参数以确保图像生成的一致性。 |
| `reference_image` | 否 | 参考图像的路径、文件或字节数据；具体取决于 SDK 的实现。 |

## 快速入门（Python + DashScope SDK）

使用 DashScope SDK，并将标准化请求转换为 SDK 的调用格式。
注意：对于 `qwen-image-max` 模型，DashScope SDK 目前通过 `ImageGeneration`（基于消息的接口）进行调用，而不是 `ImageSynthesis`。如果您使用的 SDK 版本对参考图像的字段名称有特殊要求，请相应地调整参数映射。

```python
import os
from dashscope.aigc.image_generation import ImageGeneration

# Prefer env var for auth: export DASHSCOPE_API_KEY=...
# Or use ~/.alibabacloud/credentials with dashscope_api_key under [default].


def generate_image(req: dict) -> dict:
    messages = [
        {
            "role": "user",
            "content": [{"text": req["prompt"]}],
        }
    ]

    if req.get("reference_image"):
        # Some SDK versions accept {"image": <url|file|bytes>} in messages content.
        messages[0]["content"].insert(0, {"image": req["reference_image"]})

    response = ImageGeneration.call(
        model=req.get("model", "qwen-image-max"),
        messages=messages,
        size=req.get("size", "1024*1024"),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # Pass through optional parameters if supported by the backend.
        negative_prompt=req.get("negative_prompt"),
        style=req.get("style"),
        seed=req.get("seed"),
    )

    # Response is a generation-style envelope; extract the first image URL.
    content = response.output["choices"][0]["message"]["content"]
    image_url = None
    for item in content:
        if isinstance(item, dict) and item.get("image"):
            image_url = item["image"]
            break
    return {
        "image_url": image_url,
        "width": response.usage.get("width"),
        "height": response.usage.get("height"),
        "seed": req.get("seed"),
    }
```

## 错误处理

| 错误代码 | 可能的原因 | 应对措施 |
|------|--------------|--------|
| 401/403 | `DASHSCOPE_API_KEY` 缺失或无效 | 检查环境变量或 `~/.alibabacloud/credentials` 文件中的设置，并检查访问权限。 |
| 400 | 不支持的尺寸或请求格式错误 | 使用标准的 `WxH` 格式，并验证所有参数。 |
| 429 | 请求频率限制或配额超出 | 采用退避策略重试请求，或减少并发请求的数量。 |
| 5xx | 后端暂时性错误 | 重试一次或两次。

## 输出路径

- 默认输出路径：`output/ai-image-qwen-image/images/`
- 可通过 `OUTPUT_DIR` 变量覆盖默认路径。

## 运营指南

- 将生成的图像存储在对象存储中，并仅将图像的 URL 保存在元数据中。
- 使用 `(prompt, negative_prompt, size, seed, reference_image_hash)` 作为键值对来缓存结果，以避免重复计算成本。
- 对于暂时性的 429/5xx 错误，采用指数级退避策略进行重试。
- 一些后端可能会忽略 `negative_prompt`、`style` 或 `seed` 参数；请将其视为可忽略的输入。
- 如果响应中不包含图像 URL，请显示明确的错误信息，并使用简化的提示再次请求。

## 尺寸说明

- 使用 `WxH` 格式（例如 `1024*1024`、`768*1024`）。
- 建议使用常见的尺寸；不支持的尺寸可能会导致请求失败（返回 400 错误）。

## 避免的错误做法

- 不要自行创建模型名称或别名；仅使用官方提供的模型 ID。
- 不要在数据库行中存储较大的 Base64 编码的图像数据；请使用对象存储。
- 对于耗时较长的图像生成任务，不要省略用户可看到的进度信息。

## 参考资料

- 请参阅 `references/api_reference.md` 以获取更详细的 DashScope SDK 参数映射和响应解析指南。
- 请参阅 `references/prompt-guide.md` 了解提示语的格式和示例。
- 对于编辑流程，请使用 `skills/ai/image/alicloud-ai-image-qwen-image-edit/`。

- 更多资源请参见 `references/sources.md`。