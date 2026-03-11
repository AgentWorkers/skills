---
name: Showmeai
description: 通过 Showmeai 的 OpenAI 兼容图像 API 生成图像。该 API 支持 nano-banana 和 gpt-image 模型系列，默认使用的模型为 nano-banana-pro。默认情况下，生成的图像不会被保存在本地（仅提供 URL 链接）；如果用户希望保存图像，请使用 `--save` 标志。
homepage: https://api.showmeai.art
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["python3"], "env": ["Showmeai_API_KEY", "Showmeai_BASE_URL"] },
        "primaryEnv": "Showmeai_API_KEY",
      },
  }
---
# Showmeai 图像生成

通过 Showmeai 的 OpenAI 兼容图像 API（`/images/generations`）生成图像。

## 基本用法

```bash
python3 {baseDir}/scripts/gen.py --prompt "your prompt here"
```

## 选项

```bash
# Specify model (default: nano-banana-pro)
python3 {baseDir}/scripts/gen.py --prompt "..." --model nano-banana-pro

# Higher resolution (append -2k or -4k to model name)
python3 {baseDir}/scripts/gen.py --prompt "..." --model nano-banana-pro-2k

# Save image locally (default: NO save, URL only)
python3 {baseDir}/scripts/gen.py --prompt "..." --save

# Save to OSS directory (~/.openclaw/oss/)
python3 {baseDir}/scripts/gen.py --prompt "..." --oss

# Save to custom directory
python3 {baseDir}/scripts/gen.py --prompt "..." --save --out-dir /path/to/dir

# Aspect ratio
python3 {baseDir}/scripts/gen.py --prompt "..." --aspect-ratio 16:9

# Image count
python3 {baseDir}/scripts/gen.py --prompt "..." --count 2
```

## 支持的模型

**nano-banana 系列**（返回图像 URL，速度较快）：
- nano-banana
- nano-banana-pro  ← 默认值
- nano-banana-2
- nano-banana-pro-2k / nano-banana-pro-4k （高分辨率）

**gpt-image 系列**（返回 Base64 编码的图像数据，会自动保存）：
- gpt-image-1
- gpt-image-1.5

## 配置

配置信息请设置在 `.env` 或 `~/.openclaw/openclaw.json` 文件中：
- `Showmeai_API_KEY` — 你的 Showmeai API 密钥 **（必需）**
- `Showmeai_BASE_URL` — 带有 `/v1` 后缀的基地址 **（必需）**；如果未设置，默认为 `https://api.showmeai.art/v1`

## 保存行为

- 默认：不生成本地文件，直接输出 `MEDIA:<url>`
- `--save`：将生成的图像保存到 `~/.openclaw/media/`
- `--oss`：将图像保存到 `~/.openclaw/oss/`
- gpt-image 模型生成的图像始终保存到 `media/` 目录（因为 API 返回的是 Base64 编码的数据）