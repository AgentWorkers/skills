---
name: gemini-image-simple
version: 1.1.0
description: 使用纯 Python 标准库通过 Gemini API 生成和编辑图像。完全不需要任何第三方依赖，因此可以在无法使用 pip 或 uv 的受限环境中正常运行。
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      env: ["GEMINI_API_KEY"]
---

# Gemini Image Simple

使用 Google 的 **Nano Banana Pro**（Gemini 3 Pro Image）生成和编辑图像——这是目前最高质量的图像生成模型。

## 为什么选择这个技能

| 特点 | 本技能 | 其他技能（如 nano-banana-pro 等） |
|---------|------------|-------------------------------|
| **依赖项** | 无（仅需要 stdlib） | google-genai、pillow 等 |
| **是否需要 pip/uv** | ❌ 不需要 | ✅ 需要 |
| **是否可以在 Fly.io 上免费使用** | ✅ 可以 | ❌ 无法使用 |
| **是否支持在容器中运行** | ✅ 可以 | ❌ 经常无法使用 |
| **图像生成** | ✅ 支持 | ✅ 支持 |
| **图像编辑** | ✅ 支持 | ✅ 支持 |
| **设置复杂度** | 只需设置 API 密钥 | 需要先安装相关包 |

**总结：** 只要安装了 Python 3，就可以在任何地方使用这个技能。无需额外的包管理器或虚拟环境，也不存在权限问题。

## 快速入门

```bash
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

设置 `GEMINI_API_KEY` 环境变量。可以在 [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey) 获取 API 密钥。

## 工作原理

该技能使用 Google 的 **Nano Banana Pro**（又名 Gemini 3 Pro Image）进行图像生成和编辑：
- 使用纯 `urllib.request` 处理 HTTP 请求（无需额外的请求库）；
- 使用纯 `json` 进行数据解析（依赖 stdlib）；
- 使用纯 `base64` 对数据进行编码（依赖 stdlib）。

仅此而已，无需任何外部包。适用于所有 Python 3.10 及更高版本的版本。

## 模型

目前使用的模型是：`nano-banana-pro-preview`（也称为 Gemini 3 Pro Image）。

其他可用模型（可根据需要修改 `generate.py` 文件）：
- `gemini-3-pro-image-preview` — 与 Nano Banana Pro 功能相同；
- `imagen-4.0-ultra-generate-001` — Imagen 4.0 Ultra 模型；
- `imagen-4.0-generate-001` — Imagen 4.0 模型；
- `gemini-2.5-flash-image` — Gemini 2.5 Flash 模型（包含图像生成功能）。

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