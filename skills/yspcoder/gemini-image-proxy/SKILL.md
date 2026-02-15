---
name: gemini-image-proxy
version: 1.0.0
description: 使用 OpenAI Python SDK 和 Gemini API 生成和编辑图像。
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      env: ["GOOGLE_PROXY_API_KEY", "GOOGLE_PROXY_BASE_URL"]
---

# Gemini Image Simple

通过 OpenAI Python SDK 和兼容 OpenAI 的 API 端点，使用 **Gemini 3 Pro Image** 生成和编辑图像。

## 为什么选择这个技能

| 功能                        | 这个技能                | 其他技能（如 nano-banana-pro 等）       |
| ---------------------------- | ------------------------- | ----------------------------- |
| **依赖库**                     | openai (SDK)              | google-genai, pillow 等           |
| **是否需要 pip/uv**                | ✅ 是                    | ✅ 是                         |
| **是否支持 Fly.io 免费使用**           | ✅ 是（需要安装 pip）          | ❌ 不支持                     |
| **是否支持在容器中运行**           | ✅ 是（需要安装 pip）          | ❌ 经常无法运行                   |
| **是否支持图像生成**                 | ✅ 完整支持               | ✅ 完整支持                     |
| **是否支持图像编辑**                 | ✅ 支持                   | ✅ 支持                         |
| **设置难度**                     | 安装 SDK 并设置 API 密钥       | 首先需要安装相关包                   |

**总结：** 该技能使用 OpenAI SDK，因此您需要使用 pip 安装 `openai`。

## 安装

```bash
python3 -m pip install openai
```

## 快速入门

```bash
# Set env
export GOOGLE_PROXY_API_KEY="your_api_key"
export GOOGLE_PROXY_BASE_URL="https://example.com/v1"

# Generate
python3 /data/clawd/skills/gemini-image-simple/scripts/generate.py "A cat wearing a tiny hat" cat.png

# Edit existing image
python3 /data/clawd/skills/gemini-image-simple/scripts/generate.py "Make it sunset lighting" edited.png --input original.png
```

## 使用方法

### 生成新图像

```bash
python3 {baseDir}/scripts/generate.py "your prompt" output.png
```

### 编辑现有图像

```bash
python3 {baseDir}/scripts/generate.py "edit instructions" output.png --input source.png
```

支持的输入格式：PNG、JPG、JPEG、GIF、WEBP

## 环境配置

设置以下环境变量：

- `GOOGLE_PROXY_API_KEY`（您的 API 密钥）
- `GOOGLE_PROXY_BASE_URL`（兼容 OpenAI 的基础 URL，例如：https://example.com/v1）

## 工作原理

通过 OpenAI Python SDK 使用 **Gemini 3 Pro Image**（`gemini-3-pro-image`）：

- `client.images.generate(...)` 用于生成新图像
- `client.images.edits(...)` 用于编辑图像
- 需要 `openai` 包的支持

只需按照上述步骤操作，即可在任何安装了 Python 3.10 及以上版本并安装了 `openai` 的环境中使用该技能。

## 模型

当前使用的模型：`gemini-3-pro-image`

其他可用模型（可根据需要在 generate.py 文件中更改）：

- `gemini-3-pro-image-preview` - 预览版本
- `imagen-4.0-ultra-generate-001` - Imagen 4.0 Ultra 模型
- `imagen-4.0-generate-001` - Imagen 4.0 模型
- `gemini-2.5-flash-image` - Gemini 2.5 Flash 模型（包含图像生成功能）

## 示例

```bash
# Landscape
python3 {baseDir}/scripts/generate.py "Misty mountains at sunrise, photorealistic" mountains.png

# Product shot
python3 {baseDir}/scripts/generate.py "Minimalist product photo of a coffee cup, white background" coffee.png

# Edit: change style
python3 {baseDir}/scripts/generate.py "Convert to watercolor painting style" watercolor.png --input photo.jpg

# Edit: add element
python3 {baseDir}/scripts/generate.py "Add a rainbow in the sky" rainbow.png --input landscape.png
```