---
name: nano-banana-pro
description: 通过 Replicate 上的 Gemini 3 Pro Image 生成或编辑图像
user-invocable: true
metadata: {"openclaw": {"emoji": "🎨", "requires": {"env": ["REPLICATE_API_TOKEN"], "bins": ["uv"]}, "primaryEnv": "REPLICATE_API_TOKEN"}}
---
# Nano Banana Pro 图像生成器

通过 Replicate API 使用 Google 的 Nano Banana Pro 模型生成和编辑图像。

## 使用方法

运行生成脚本：

    uv run --with replicate python {baseDir}/generate.py --prompt "<用户提示>" [--aspect-ratio 1:1] [--output image.png]

## 选项

- `--prompt`：图像描述（必填）
- `--aspect-ratio`：宽高比（例如 1:1、4:3、16:9，默认值为 1:1）
- `--output`：输出文件路径（默认值为 generated_image.png）

## 规则

- 仅使用 `google/nano-banana-pro` 模型，严禁使用其他模型（如 `google/nano-banana` 或其他替代模型）。如果模型不可用或受到使用限制，请向用户报告错误并停止操作。
- 生成图像后，需将图像文件直接发送到聊天中，切勿将其默默地保存在工作区中。

## 提示

- 对于图像中的文本，请明确指定字体、大小和位置。
- 该模型支持的分辨率最高为 2K。
- 安全过滤功能默认处于开启状态。