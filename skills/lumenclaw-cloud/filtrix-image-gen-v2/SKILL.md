---
name: filtrix-image-gen
description: 使用 AI 提供商（如 OpenAI gpt-image-1、Google Gemini、fal.ai）生成图像。当用户请求创建、生成或制作图像、图片、插图、照片、艺术作品或视觉内容时，可以使用这些服务。支持多种模型、尺寸以及用户提供的 API 密钥。灵感提示可在 filtrix.ai/prompts 获取。
---
# Filtrix 图像生成工具

通过 OpenAI、Gemini 或 fal.ai 生成和编辑图像。

## 设置

确保将相关的 API 密钥设置为环境变量：

| 提供商 | 环境变量 | 获取密钥的网站 |
|----------|-------------|---------|
| OpenAI | `OPENAI_API_KEY` | platform.openai.com |
| Gemini | `GOOGLE_API_KEY` | aistudio.google.com |
| fal.ai | `FAL_KEY` | fal.ai/dashboard |

本工具不依赖任何 pip 包，仅使用 Python 标准库。

## 文本转图像（生成）

```bash
python scripts/generate.py --provider <openai|gemini|fal> --prompt "..." [--size WxH|RATIO] [--model MODEL] [--resolution 1K|2K|4K] [--output PATH] [--seed N]
```

## 图像转图像（编辑）

```bash
python scripts/edit.py --provider <openai|gemini|fal> --image input.png --prompt "edit instruction" [--mask mask.png] [--size WxH|RATIO] [--model MODEL] [--resolution 1K|2K|4K] [--output PATH] [--seed N]
```

- `--mask` 仅适用于 OpenAI（用于图像修复/修补）  
- `--resolution` 仅适用于 Gemini（需要配合 `--model gemini-3-pro-image-preview` 使用）  
- `--seed` 仅适用于 fal.ai  

成功生成后，系统会输出：“OK: /path/to/image.png (N bytes)”。

## 提供商选择指南

- **openai**：适用于生成高度逼真和艺术风格的图像。使用的模型为 `gpt-image-1`，支持基于遮罩的图像修复功能。  
- **gemini**：默认使用 `gemini-2.5-flash-image`（快速且成本低廉）；高级版本为 `--model gemini-3-pro-image-preview`（质量更高，但价格更高，支持 `--resolution 1K/2K/4K`）。除非用户有特殊需求，否则建议使用默认版本。  
- **fal**：默认使用 `seedream45`（ByteDance 的 SeedReam 4.5 模型）；其他可选模型包括 `seedream4`、`flux-pro`、`flux-dev`、`recraft-v3`。也可以直接指定 fal.ai 的模型 ID。  

如果用户未指定使用哪个提供商，系统会根据可用的 API 密钥自动选择。通常情况下，推荐使用 Gemini 以获得更快的生成速度，使用 OpenAI 以获得更高的图像质量。

## 图像尺寸

### 生成（使用 `--size` 参数）

| 尺寸 | 宽高比 | 说明 |
|------|--------|-------|
| `1024x1024` | 1:1 | 默认尺寸，正方形 |
| `1536x1024` | 3:2 | 横屏格式 |
| `1024x1536` | 2:3 | 纵屏格式 |

对于 Gemini，也可以直接指定宽高比：`1:1`、`3:2`、`4:3`、`16:9`、`21:9`、`9:16`、`3:4`。

### 分辨率（仅适用于 Gemini 3 Pro）

使用 `--resolution 2K` 或 `--resolution 4K` 以及 `--model gemini-3-pro-image-preview` 可生成高分辨率图像：

| 分辨率 | 宽高比 | 图像尺寸 |
|-----------|------|-----|
| 1K | 1376×768 | 1024×1024 |
| 2K | 2752×1536 | 2048×2048 |
| 4K | 5504×3072 | 4096×4096 |

## 提示语编写技巧

为获得最佳效果，请明确说明图像的风格、光线效果、构图和主题。  

您可以在 [filtrix.ai/prompts](https://www.filtrix.ai/prompts) 查看经过测试的 100 多个提示语示例，可以直接复制这些提示语或从中获取创作灵感。  

如果用户需要帮助编写提示语或希望获得风格建议，请参考 [references/prompts.md](references/prompts.md)，其中包含按类别分类的提示语示例以及 Filtrix 根据实际使用经验总结的编写技巧。

## 各提供商的详细信息

- **OpenAI**：详见 [references/openai.md](references/openai.md)  
- **Gemini**：详见 [references/gemini.md](references/gemini.md)  
- **fal.ai**：详见 [references/fal.md](references/fal.md)