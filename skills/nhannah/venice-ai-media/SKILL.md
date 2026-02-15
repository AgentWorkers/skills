---
name: venice-ai-media
description: 通过 Venice AI，您可以生成、编辑和放大图像；还可以将图像转换为视频。该工具支持文本转图像、图像转视频（Sora、WAN）的功能，同时具备图像放大和人工智能编辑能力。
homepage: https://venice.ai
metadata:
  {
    "clawdbot":
      {
        "emoji": "🎨",
        "requires": { "bins": ["python3"], "env": ["VENICE_API_KEY"] },
        "primaryEnv": "VENICE_API_KEY",
        "notes": "Requires Python 3.10+",
        "install":
          [
            {
              "id": "python-brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python (brew)",
            },
          ],
      },
  }
---

# Venice AI Media

使用 Venice AI API 生成图片和视频。Venice 是一个无审查限制的 AI 平台，价格具有竞争力。

## 先决条件

- **Python 3.10+**（使用 `brew install python` 或系统自带的 Python 安装）
- **Venice API 密钥**（提供免费 tier）
- **requests** 库（如果未安装，脚本会自动安装）

## 设置

### 1. 获取 API 密钥

1. 在 [venice.ai](https://venice.ai) 注册账户
2. 访问 [venice.ai/settings/api](https://venice.ai/settings/api)
3. 点击 “Create API Key”
4. 复制密钥（密钥以 `vn_...` 开头）

### 2. 配置密钥

**选项 A：环境变量**

```bash
export VENICE_API_KEY="vn_your_key_here"
```

**选项 B：Clawdbot 配置**（推荐使用——配置会在会话间保持）

将以下内容添加到 `~/.clawdbot/clawdbot.json` 文件中：

```json5
{
  skills: {
    entries: {
      "venice-ai-media": {
        env: {
          VENICE_API_KEY: "vn_your_key_here",
        },
      },
    },
  },
}
```

### 3. 验证设置

```bash
python3 {baseDir}/scripts/venice-image.py --list-models
```

如果看到模型列表，说明设置完成！

## 价格概述

| 功能                | 费用                              |
| ---------------- | --------------------------------- |
| 图像生成            | 每张图片约 $0.01-0.03                         |
| 图像放大            | 每张图片约 $0.02-0.04                         |
| 图像编辑            | $0.04                              |
| 视频（WAN）           | 根据时长不同，价格在 $0.10-0.50 之间                 |
| 视频（Sora）           | 根据时长不同，价格在 $0.50-2.00 之间                 |

使用 `--quote` 参数在生成视频前查看价格。

## 快速入门

```bash
# Generate an image
python3 {baseDir}/scripts/venice-image.py --prompt "a serene canal in Venice at sunset"

# Upscale an image
python3 {baseDir}/scripts/venice-upscale.py photo.jpg --scale 2

# Edit an image with AI
python3 {baseDir}/scripts/venice-edit.py photo.jpg --prompt "add sunglasses"

# Create a video from an image
python3 {baseDir}/scripts/venice-video.py --image photo.jpg --prompt "gentle camera pan" --duration 5s
```

---

## 图像生成

```bash
python3 {baseDir}/scripts/venice-image.py --prompt "a serene canal in Venice at sunset"
python3 {baseDir}/scripts/venice-image.py --prompt "cyberpunk city" --count 4
python3 {baseDir}/scripts/venice-image.py --prompt "portrait" --width 768 --height 1024
python3 {baseDir}/scripts/venice-image.py --prompt "abstract art" --out-dir /tmp/venice
python3 {baseDir}/scripts/venice-image.py --list-models
python3 {baseDir}/scripts/venice-image.py --list-styles
python3 {baseDir}/scripts/venice-image.py --prompt "fantasy" --model flux-2-pro --no-validate
python3 {baseDir}/scripts/venice-image.py --prompt "photo" --style-preset "Cinematic" --embed-exif
```

**关键参数：** `--prompt`（提示语），`--model`（默认：flux-2-max），`--count`（使用高效批量 API 处理相同提示语），`--width`（宽度），`--height`（高度），`--format`（webp/png/jpeg），`--resolution`（1K/2K/4K），`--aspect-ratio`（宽高比），`--negative-prompt`（负向提示语），`--style-preset`（使用 `--list-styles` 查看样式选项），`--cfg-scale`（提示语与图像的匹配度，0-20，默认 7.5），`--seed`（用于生成可重复的结果），`--safe-mode`（默认关闭，适用于无审查内容），`--hide-watermark`（仅在使用时启用——Venice 支持水印），`--embed-exif`（将提示语嵌入图像元数据），`--lora-strength`（0-100，适用于特定模型），`--steps`（推理步骤，取决于模型），`--enable-web-search`（启用网络搜索），`--no-validate`（跳过新模型或测试模型的验证）

## 图像放大

```bash
python3 {baseDir}/scripts/venice-upscale.py photo.jpg --scale 2
python3 {baseDir}/scripts/venice-upscale.py photo.jpg --scale 4 --enhance
python3 {baseDir}/scripts/venice-upscale.py photo.jpg --enhance --enhance-prompt "sharpen details"
python3 {baseDir}/scripts/venice-upscale.py --url "https://example.com/image.jpg" --scale 2
```

**关键参数：** `--scale`（放大倍数，1-4，默认 2），`--enhance`（图像增强），`--enhance-prompt`（增强提示语效果），`--enhance-creativity`（创意增强程度，0.0-1.0），`--replication`（保留图像线条/减少噪声，0.0-1.0，默认 0.35），`--url`（使用 URL 而非本地文件），`--output`（输出文件路径），`--out-dir`（输出目录）

## 图像编辑

```bash
python3 {baseDir}/scripts/venice-edit.py photo.jpg --prompt "add sunglasses"
python3 {baseDir}/scripts/venice-edit.py photo.jpg --prompt "change the sky to sunset"
python3 {baseDir}/scripts/venice-edit.py photo.jpg --prompt "remove the person in background"
python3 {baseDir}/scripts/venice-edit.py --url "https://example.com/image.jpg" --prompt "colorize"
```

**关键参数：** `--prompt`（必需——AI 会根据提示语进行编辑），`--url`（使用 URL 而非本地文件），`--output`（输出文件路径），`--out-dir`（输出目录）

**注意：** 图像编辑端点使用 Qwen-Image 模型，该模型对内容有一定的限制（与其他 Venice 端点不同）。

## 视频生成

```bash
# Get price quote first (no generation)
python3 {baseDir}/scripts/venice-video.py --quote --model wan-2.6-image-to-video --duration 10s --resolution 720p

# Image-to-video (WAN 2.6 - default)
python3 {baseDir}/scripts/venice-video.py --image photo.jpg --prompt "camera pans slowly" --duration 10s

# Image-to-video (Sora)
python3 {baseDir}/scripts/venice-video.py --image photo.jpg --prompt "cinematic" \
  --model sora-2-image-to-video --duration 8s --aspect-ratio 16:9 --skip-audio-param

# List models (shows available durations per model)
python3 {baseDir}/scripts/venice-video.py --list-models

# Clean up a video downloaded with --no-delete
python3 {baseDir}/scripts/venice-video.py --complete <queue_id> --model <model>
```

**关键参数：** `--image`（生成视频所需的输入图像），`--prompt`（生成视频所需的提示语），`--model`（默认：wan-2.6-image-to-video），`--duration`（时长，取决于模型，详见 `--list-models`），`--resolution`（分辨率，480p/720p/1080p），`--aspect-ratio`（宽高比），`--audio`/`--no-audio`（是否包含音频），`--skip-audio-param`（是否忽略音频参数），`--quote`（价格估算），`--timeout`（生成时间限制），`--poll-interval`（请求间隔），`--no-delete`（是否保留服务器上的媒体文件），`--complete`（清理已下载的视频文件），`--no-validate`（跳过模型验证）

**进度显示：** 生成过程中，脚本会根据 Venice 的平均执行时间显示进度。

## 模型说明

使用 `--list-models` 查看当前可用的模型及其状态。模型会频繁更新。

**图像模型：** 默认模型为 `flux-2-max`。常见模型还包括 flux、gpt-image 和 nano-banana。

**视频模型：**

- **WAN** 模型：支持将图像转换为视频，可配置音频，时长可选（5秒至21秒）。
- **Sora** 模型：需要使用 `--aspect-ratio` 参数，并且必须使用 `--skip-audio-param` 选项。

**提示：**

- 对于尚未列出在新模型列表中的新模型或测试模型，使用 `--no-validate` 选项。
- 在生成视频前，使用 `--quote` 参数查看价格。
- Venice 是一个无审查限制的 API，因此默认关闭了安全模式。

## 输出

脚本会输出 `MEDIA: /path/to/file` 的信息，以便 Clawdbot 自动处理文件。

**提示：** 在生成媒体文件时，使用 `--out-dir /tmp/venice-$(date +%s)` 可确保文件在不同用户账户间共享。

## 故障排除

**“VENICE_API_KEY 未设置”**

- 检查 `~/.clawdbot/clawdbot.json` 文件中的配置。
- 或者通过环境变量设置：`export VENICE_API_KEY="vn_..."`

**“API 密钥无效”**

- 在 [venice.ai/settings/api](https://venice.ai/settings/api) 验证密钥的有效性。
- 密钥必须以 `vn_` 开头。

**“模型未找到”**

- 运行 `--list-models` 查看可用模型。
- 对于新模型或测试模型，使用 `--no-validate` 选项。

**视频生成失败/超时**

- 视频生成可能需要 1-5 分钟，具体取决于模型和时长。
- 对于较长的视频，使用 `--timeout 600` 设置超时时间。
- 可以在 [venice.ai](https://venice.ai) 查看平台的运行状态。

**“requests” 模块未找到**

- 使用 `pip3 install requests` 安装该模块。