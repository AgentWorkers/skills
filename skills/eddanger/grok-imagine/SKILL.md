---
name: grok-imagine
description: 通过 xAI 的 Grok Imagine API 生成图像。当用户希望使用 xAI/Grok 创建 AI 生成的图像，或者当 OpenAI 的图像生成功能不可用时，可以使用此方法。
homepage: https://docs.x.ai/docs/api-reference#image-generation
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["node"], "env": ["XAI_API_KEY"] },
        "primaryEnv": "XAI_API_KEY",
      },
  }
---

# Grok Imagine

通过 xAI 的 Grok Imagine API 生成图像。

## 运行方式

```bash
node {baseDir}/scripts/gen.mjs --prompt "your image description"
```

## 示例

```bash
# Basic image generation
node {baseDir}/scripts/gen.mjs --prompt "a cyberpunk city at sunset"

# Multiple images
node {baseDir}/scripts/gen.mjs --prompt "a friendly robot" --count 4

# Custom output directory
node {baseDir}/scripts/gen.mjs --prompt "mountain landscape" --out-dir ./images

# Image editing (provide input image)
node {baseDir}/scripts/gen.mjs --prompt "add a rainbow to the sky" --input /path/to/image.png
```

## 可用模型

- **grok-imagine-image**：文本转图像及图像编辑功能（默认模型）
- **grok-2-image**：旧版本的图像生成模型

## 参数

- `--prompt, -p`：图像描述（必填）
- `--count, -n`：要生成的图像数量（默认值：1）
- `--model, -m`：要使用的模型（默认值：grok-imagine-image）
- `--input, -i`：用于编辑任务的输入图像路径（可选）
- `--out-dir, -o`：输出目录（默认值：./tmp/grok-imagine-<timestamp>）

## 输出结果

- 生成的图像将保存为 PNG 格式的文件
- `prompts.json` 文件：包含提示信息与对应图像的映射关系
- `index.html` 文件：包含图像的缩略图画廊
- `MEDIA:` 文件：用于 OpenClaw 自动加载图像的元数据

## API 密钥

请设置 `XAI_API_KEY` 环境变量，或在 OpenClaw 中进行配置：
- 在 `~/.openclaw/openclaw.json` 文件中的 `skills."grok-imagine".apiKey` 配置项中设置 API 密钥