---
name: openai-image-cli
version: 1.0.0
description: 通过 OpenAI 的 GPT Image 和 DALL-E 模型生成、编辑和管理图像。
metadata:
  {
    "openclaw": { "emoji": "🎨", "requires": { "bins": ["openai-image"], "envs": ["OPENAI_API_KEY"] } },
  }
---

# OpenAI Image CLI

使用 OpenAI 的最新模型生成、编辑和创建图像的变体。

## 安装

```bash
npm install -g @versatly/openai-image-cli
```

## 认证

```bash
# Via environment variable
export OPENAI_API_KEY=sk-...

# Or via config
openai-image config set api-key sk-...
```

## 快速入门

```bash
# Generate an image
openai-image generate "A futuristic city at sunset"

# High quality landscape
openai-image generate "Mountain panorama" -s 1536x1024 -q high

# Multiple images with transparency
openai-image generate "Logo design" -n 4 -b transparent

# Edit an existing image
openai-image edit photo.png "Add sunglasses to the person"

# Create variations (DALL-E 2)
openai-image vary original.png -n 3
```

## 可用模型

| 模型 | 描述 | 备注 |
|-------|-------------|-------|
| `gpt-image-1.5` | 最新的 GPT Image 模型（默认） | 图像质量最佳，推荐使用 |
| `gpt-image-1` | GPT Image 模型 | 图像质量与性能平衡良好 |
| `gpt-image-1-mini` | GPT Image Mini 模型 | 性能优越但成本较低 |
| `dall-e-3` | DALL-E 3 模型 | 于 2026 年 5 月停止支持 |
| `dall-e-2` | DALL-E 2 模型 | 于 2026 年 5 月停止支持，但仍支持图像变体功能 |

## 命令

### generate

根据文本提示生成图像。

```bash
openai-image generate "prompt" [options]

Options:
  -m, --model <model>        Model (default: gpt-image-1.5)
  -s, --size <size>          Size: 1024x1024, 1536x1024, 1024x1536, auto
  -q, --quality <quality>    Quality: auto, high, medium, low
  -n, --count <n>            Number of images (1-10)
  -f, --format <format>      Format: png, jpeg, webp
  -o, --output <path>        Output file/directory
  -b, --background <bg>      Background: auto, transparent, opaque
  --compression <0-100>      Compression level for jpeg/webp
  --moderation <level>       Content moderation: auto, low
  --stream                   Enable streaming with partial images
  --partial-images <0-3>     Partial images during streaming
  --json                     Output JSON response
  --dry-run                  Show request without executing
```

### edit

根据提示编辑现有图像。

```bash
openai-image edit <image> "instructions" [options]

Options:
  --mask <path>              Mask image for inpainting
  --images <paths...>        Additional reference images (up to 16)
  -s, --size <size>          Output size
  -q, --quality <quality>    Quality level
  -n, --count <n>            Number of variations
  -f, --format <format>      Output format
  -o, --output <path>        Output path
```

**示例：**
```bash
# Simple edit
openai-image edit photo.png "Add sunglasses"

# Inpainting with mask
openai-image edit room.png "Add a plant" --mask mask.png

# Multi-image composite
openai-image edit base.png "Create gift basket" --images item1.png item2.png
```

### vary

创建图像的变体（仅适用于 DALL-E 2 模型）。

```bash
openai-image vary <image> [options]

Options:
  -n, --count <n>            Number of variations (1-10)
  -s, --size <size>          Size: 256x256, 512x512, 1024x1024
  -o, --output <path>        Output path/directory
```

### batch

从文件或标准输入（stdin）生成多张图像。

```bash
openai-image batch [options]

Options:
  -i, --input <file>         Input file (text or JSONL)
  --stdin                    Read from stdin
  -m, --model <model>        Model for all generations
  -o, --output-dir <dir>     Output directory
  --parallel <n>             Concurrent requests (default: 3)
  --delay <ms>               Delay between requests (default: 100)
```

**JSONL 格式：**
```json
{"prompt": "A red car", "size": "1024x1024", "quality": "high"}
{"prompt": "A blue boat", "size": "1536x1024"}
```

### config

管理 CLI 的配置参数。

```bash
openai-image config set <key> <value>
openai-image config get <key>
openai-image config list
openai-image config reset
openai-image config path
```

**配置参数：`api-key`、`default-model`、`default-size`、`default-quality`、`default-format`、`output-dir`

### models

列出所有可用的模型。

```bash
openai-image models [--json]
```

### history

查看本地生成的图像历史记录。

```bash
openai-image history [-n <limit>] [--json] [--clear]
```

## 输出格式

### 默认格式（人类可读）

```
✓ Generated image saved to ./generated-1707500000.png
  Model: gpt-image-1.5
  Size: 1024x1024
  Quality: high
  Tokens: 150 (text: 10, image: 140)
```

### JSON 格式（`--json`）

```json
{
  "success": true,
  "file": "./generated-1707500000.png",
  "model": "gpt-image-1.5",
  "size": "1024x1024",
  "quality": "high",
  "usage": {
    "total_tokens": 150,
    "input_tokens": 50,
    "output_tokens": 100
  }
}
```

## 图像尺寸选项

| 模型 | 可选尺寸 |
|-------|-------|
| GPT Image | 1024x1024、1536x1024（横向）、1024x1536（纵向）、自动调整 |
| DALL-E 3 | 1024x1024、1792x1024、1024x1792 |
| DALL-E 2 | 256x256、512x512、1024x1024 |

## 提示：

1. **透明背景**：使用 `-b transparent -f png` 选项生成带有透明背景的图像（适用于徽标）。
2. **批量处理**：使用 JSONL 格式为每张图像指定自定义参数。
3. **成本控制**：对于草图需求，建议使用 `gpt-image-1-mini` 模型。
4. **历史记录**：功能默认启用，可通过 `openai-image history` 命令查看生成历史记录。

## 链接：

- npm：https://www.npmjs.com/package/@versatly/openai-image-cli
- GitHub：https://github.com/Versatly/openai-image-cli