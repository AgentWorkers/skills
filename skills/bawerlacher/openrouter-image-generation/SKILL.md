---
name: openrouter-image-generation
description: 通过 OpenRouter 的多模态图像生成端点（`/api/v1/chat/completions`）使用与 OpenRouter 兼容的图像模型来生成或编辑图像。适用于文本到图像（text-to-image）或图像到图像（image-to-image）的请求场景，特别是在用户需要使用 OpenRouter、`OPENROUTER_API_KEY`、模型覆盖（model overrides）或提供商特定的 `image_config` 选项时。
---
# OpenRouter 图像生成与编辑

通过 Chat Completions API，使用支持图像处理的 OpenRouter 模型来生成新图像或编辑现有图像。

## 使用方法

使用绝对路径运行脚本（请勿先进入 skill 目录）：

**生成新图像：**
```bash
# Ensure outbound directory exists first
mkdir -p ~/.openclaw/media/outbound

uv run ~/.openclaw/workspace/skills/openrouter-image-generation/scripts/generate_image.py \
  --prompt "your image description" \
  --filename "~/.openclaw/media/outbound/output-name.png" \
  --model google/gemini-2.5-flash-image \
  [--aspect-ratio 16:9] \
  [--image-size 2K]
```

**编辑现有图像（图像到图像的转换）：**
```bash
# Ensure outbound directory exists first
mkdir -p ~/.openclaw/media/outbound

uv run ~/.openclaw/workspace/skills/openrouter-image-generation/scripts/generate_image.py \
  --prompt "editing instructions" \
  --filename "~/.openclaw/media/outbound/output-name.png" \
  --input-image "path/to/input.png" \
  --model google/gemini-2.5-flash-image
```

**重要提示：** OpenClaw 的默认输出路径为 `~/.openclaw/media/outbound/`。请将生成的图像保存在此路径下，以便其他 OpenClaw 流程能够轻松获取它们。

## API 密钥

脚本会按以下顺序检查 API 密钥：
1. `--api-key` 参数
2. `OPENROUTER_API_KEY` 环境变量

可选的 OpenRouter 信息头部参数：
- `--site-url` 或 `OPENROUTER_SITE_URL`
- `--app-name` 或 `OPENROUTER_APP_NAME`

## 模型与图像配置

- 必须指定 `--model <openrouter-model-id>`（脚本默认值为空）
- 示例模型：`google/gemini-2.5-flash-image`
- 使用 `--aspect-ratio` 设置 `image_config.aspect_ratio`（例如 `1:1`、`16:9`）
- 使用 `--image-size` 设置 `image_config.image_size`（`1K`、`2K`、`4K`）
- 使用 `--image-config-json '{"key":"value"}'` 添加高级配置或特定于提供商的额外参数（这些参数会合并到 `image_config` 中）

注意：OpenRouter 的文档中提到 `aspect_ratio` 和 `image_size` 是图像生成的常用配置字段。某些特定提供商/模型可能还支持其他配置参数（例如 Sourceful 功能）。如果请求失败，请移除不支持的选项或更换模型。

**注意：** 该脚本始终会发送 `modalities: ["image", "text"]`。仅支持图像输出的模型（某些 FLUX 变体）可能会拒绝此请求；如果使用非 Gemini 模型时出现意外错误，这可能是原因之一。目前 CLI 参数中尚无解决方法。

## 默认工作流程（草图 → 迭代 → 最终版本）

目标：在花费时间调整高级设置之前，先快速进行多次迭代。

- **草图阶段**：使用较小的图像尺寸和较快的模型
  - `--image-size 1K`
- **迭代阶段**：逐步调整图像内容，并每次运行时生成新的文件名
- **最终版本**：如果所选模型支持，使用较大的图像尺寸或更高的图像质量
  - 例如：`--image-size 4K --aspect-ratio 16:9`

## 预检查 + 常见错误

- **预检查步骤**：
  - `command -v uv`
  - `test -n "$OPENROUTER_API_KEY"`（或直接传递 `--api-key`)
  - `test -d ~/.openclaw/media/outbound || mkdir -p ~/.openclaw/media/outbound`
  - 如果正在编辑图像：`test -f "path/to/input.png"`
- **常见错误**：
  - `Error: No API key provided.` -> 请设置 `OPENROUTER_API_KEY` 或传递 `--api-key`
  - `Error loading input image:` -> 文件路径错误或文件无法读取
  - `HTTP 400`：模型或图像配置错误
  - `HTTP 401/403`：API 密钥无效、无法访问模型或超出配额/信用限制
  - `No image found in response`：模型可能不支持图像输出或请求格式不被接受

## 文件名生成

文件名遵循以下格式：`~/.openclaw/media/outbound/yyyy-mm-dd-hh-mm-ss-name.png`

示例：
- `~/.openclaw/media/outbound/2026-02-26-14-23-05-product-shot.png`
- `~/.openclaw/media/outbound/2026-02-26-14-25-30-sky-edit.png`

## 提示处理

- **生成新图像时**：直接传递用户的描述，除非描述过于模糊而无法执行操作。
- **编辑图像时**：明确用户请求的修改内容，并保持其他设置不变。

**精确编辑的提示模板：**
- **仅更改：<修改内容>。保持以下内容不变：主题、构图/裁剪、姿势、光线、色彩调色板、背景、文本和整体风格。不要添加新的对象。**

## 输出结果

- 默认情况下，将生成的第一个图像保存到 `~/.openclaw/media/outbound/output-name.png`（可以通过 `--filename` 参数指定完整路径）
- 支持 OpenRouter 的 Base64 数据 URL 格式的图像输出（`message.images[0].image_url.url`）
- 会打印保存的文件路径
- 除非用户要求，否则不会读取图像内容

## 示例

**生成新图像：**
```bash
mkdir -p ~/.openclaw/media/outbound

uv run ~/.openclaw/workspace/skills/openrouter-image-generation/scripts/generate_image.py \
  --prompt "A cinematic product photo of a matte black mechanical keyboard on a wooden desk, warm window light" \
  --filename "~/.openclaw/media/outbound/2026-02-26-14-23-05-keyboard-product-shot.png" \
  --model google/gemini-2.5-flash-image \
  --aspect-ratio 16:9 \
  --image-size 2K
```

**编辑现有图像：**
```bash
mkdir -p ~/.openclaw/media/outbound

uv run ~/.openclaw/workspace/skills/openrouter-image-generation/scripts/generate_image.py \
  --prompt "Change ONLY: make the sky dramatic with orange sunset clouds. Keep identical: subject, composition, lighting on foreground, and overall style." \
  --filename "~/.openclaw/media/outbound/2026-02-26-14-25-30-sunset-sky-edit.png" \
  --model google/gemini-2.5-flash-image \
  --input-image "original-photo.jpg"
```

## 参考资料**

- OpenRouter 文档：https://openrouter.ai/docs/guides/overview/multimodal/image-generation