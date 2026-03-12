---
name: alicloud-ai-image-qwen-image
description: 使用 Model Studio DashScope SDK 和 Qwen 的图像生成模型（qwen-image、qwen-image-plus、qwen-image-max 以及 snapshots）来生成图像。这些模型适用于实现或记录 `image.generate` 请求/响应的处理逻辑，以及配置提示语（prompt/negative_prompt）、图像尺寸（size）、随机种子值（seed）、参考图像（reference_image）等参数的设置。同时，这些模型也非常适合将图像生成功能集成到视频处理流程（video-agent pipeline）中。
version: 1.0.0
---
**类别：提供者（Provider）**

# Model Studio Qwen Image

## 验证（Validation）

```bash
mkdir -p output/alicloud-ai-image-qwen-image
python -m py_compile skills/ai/image/alicloud-ai-image-qwen-image/scripts/generate_image.py && echo "py_compile_ok" > output/alicloud-ai-image-qwen-image/validate.txt
```

**通过标准：**命令执行成功（退出状态码为0），并且生成了 `output/alicloud-ai-image-qwen-image/validate.txt` 文件。

## 输出与证据（Output and Evidence）

- 将生成的图像 URL、提示语（prompt）和元数据（metadata）保存到 `output/alicloud-ai-image-qwen-image/` 目录中。
- 每次运行至少保留一个 JSON 响应示例。

**注意事项：**  
通过标准化 `image.generate` 的输入/输出参数，并使用 DashScope SDK（Python）以及正确的模型名称，确保视频代理（video-agent）流程中的图像生成行为的一致性。

## 先决条件（Prerequisites）

- 安装 DashScope SDK（建议在虚拟环境（venv）中安装，以避免违反 PEP 668 规范）：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 在环境中设置 `DASHSCOPE_API_KEY`，或者将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中（环境变量优先级更高）。

## 关键模型名称（Critical Model Names）

请使用以下模型名称之一：  
- `qwen-image`  
- `qwen-image-plus`  
- `qwen-image-max`  
- `qwen-image-2.0`  
- `qwen-image-2.0-pro`  
- `qwen-image-max-2025-12-30`  
- `qwen-image-plus-2026-01-09`  

## 标准化接口（Normalized Interface）（`image.generate`）

### 请求（Request）

- `prompt`（字符串，必填）：描述场景，而不仅仅是关键词。  
- `negative_prompt`（字符串，可选）：后端可能忽略此参数。  
- `size`（字符串，必填）：图像尺寸，格式为 `WxH`，例如 `1024*1024`、`768*1024`。  
- `style`（字符串，可选）：可选的样式提示。  
- `seed`（整数，可选）：在支持的情况下用于保证结果的一致性。  
- `reference_image`（字符串或字节流，可选）：参考图像的路径或数据。

### 响应（Response）

- `image_url`（字符串）：生成的图像 URL。  
- `width`（整数）：图像宽度。  
- `height`（整数）：图像高度。  
- `seed`（整数）：用于生成图像的随机数。

## 快速入门（标准化请求 + 预览）（Quickstart: Standardized Request + Preview）

**最小化的标准化请求体（Minimalized Request Body）：**  
```json
{
  "prompt": "a cinematic portrait of a cyclist at dusk, soft rim light, shallow depth of field",
  "negative_prompt": "blurry, low quality, watermark",
  "size": "1024*1024",
  "seed": 1234
}
```  

**预览流程（Preview Workflow）：**  
先下载图像，然后打开查看：  
```bash
curl -L -o output/alicloud-ai-image-qwen-image/images/preview.png "<IMAGE_URL_FROM_RESPONSE>" && open output/alicloud-ai-image-qwen-image/images/preview.png
```  

**本地辅助脚本（Local Helper Script）：**  
将 JSON 请求转换为图像文件：  
```bash
python skills/ai/image/alicloud-ai-image-qwen-image/scripts/generate_image.py \\
  --request '{"prompt":"a studio product photo of headphones","size":"1024*1024"}' \\
  --output output/alicloud-ai-image-qwen-image/images/headphones.png \\
  --print-response
```  

## 参数说明（Parameter Description）  

| 参数 | 是否必填 | 备注 |
|------|---------|-------|
| `prompt` | 是 | 需要描述一个具体的场景，而不仅仅是关键词。 |
| `negative_prompt` | 否 | 后端可能会忽略此参数。 |
| `size` | 是 | 图像尺寸，格式为 `WxH`，例如 `1024*1024`、`768*1024`。 |
| `style` | 否 | 可选的样式提示。 |
| `seed` | 否 | 在支持的情况下用于保证结果的一致性。 |
| `reference_image` | 否 | 参考图像的路径、文件或字节流（具体取决于 SDK 的实现）。 |

## 快速入门（Python + DashScope SDK）**

使用 DashScope SDK，并将标准化请求转换为 SDK 调用。  
**注意：**对于 `qwen-image-max` 模型，DashScope SDK 目前使用 `ImageGeneration` 方法（基于消息的接口）而非 `ImageSynthesis` 方法。  
如果所使用的 SDK 版本对参考图像的字段名称有特殊要求，请相应地调整参数映射。  
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

## 错误处理（Error Handling）  

| 错误代码 | 可能原因 | 应对措施 |
|------|--------------|--------|
| 401/403 | `DASHSCOPE_API_KEY` 未设置或无效 | 检查环境变量或 `~/.alibabacloud/credentials` 文件中的配置，以及访问权限。 |
| 400 | 不支持的图像尺寸或请求格式错误 | 使用标准的 `WxH` 格式，并验证所有输入参数。 |
| 429 | 请求次数过多或配额限制 | 采用退避策略重试请求。 |
| 5xx | 后端临时错误 | 重试一次或两次。 |

## 输出路径（Output Location）  

- 默认输出路径：`output/alicloud-ai-image-qwen-image/images/`  
- 可通过 `OUTPUT_DIR` 配置自定义输出目录。  

## 运维指南（Operational Guidelines）  

- 将生成的图像存储在对象存储（object storage）中，并仅将图像 URL 保存在元数据中。  
- 使用 `(prompt, negative_prompt, size, seed, reference_image_hash)` 作为键值对来缓存结果，以避免重复计算成本。  
- 对于因临时错误（如 429/5xx）导致的失败，采用指数级退避策略进行重试。  
- 部分后端可能忽略 `negative_prompt`、`style` 或 `seed` 参数；将其视为可选输入。  
- 如果响应中未包含图像 URL，请显示明确的错误信息，并使用简化的提示语重新尝试请求。  

## 图像尺寸说明（Image Size Notes）  

- 使用 `WxH` 格式（例如 `1024*1024`、`768*1024`）。  
- 建议使用常见的图像尺寸；不支持的尺寸可能会导致请求失败（返回错误代码 400）。  

## 避免的错误做法（Anti-patterns）  

- 不要自行创建模型名称或别名；仅使用官方提供的模型 ID。  
- 不要将大型 Base64 编码的图像数据存储在数据库中；使用对象存储服务。  
- 对于耗时较长的图像生成操作，不要省略用户可看到的进度信息。  

## 工作流程（Workflow）  

1) 确认用户的操作意图、所在区域、使用的模型标识符，以及操作是只读还是修改操作。  
2) 先执行一个最小的只读查询，以验证连接性和权限。  
3) 使用明确的参数和有限的权限范围执行目标操作。  
4) 验证结果并保存输出文件及相关证据。  

## 参考资料（References）  

- 详情请参阅 `references/api_reference.md`，了解 DashScope SDK 的参数映射和响应解析方法。  
- 有关提示语的格式和示例，请参阅 `references/prompt-guide.md`。  
- 如需编辑图像，请参考 `skills/ai/image/alicloud-ai-image-qwen-image-edit/`。  
- 更多资源请查看 `references/sources.md`。