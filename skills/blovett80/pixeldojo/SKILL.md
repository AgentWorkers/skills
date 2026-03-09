---
name: pixeldojo
description: 您可以访问 PixelDojo 的 API 来生成 AI 图像和视频。当代理需要创建图像或视频、从 PixelDojo 的在线目录中选择模型、检查异步作业的状态或下载已完成的结果文件时，可以使用该 API。PixelDojo 是一个基于订阅的创意平台，它通过一个统一的 API 提供多种生成模型，包括通用图像处理模型、专注于图像编辑的模型以及视频处理模型。
metadata:
  author: Brian Lovett
  homepage: https://pixeldojo.ai
  source: https://pixeldojo.ai
  openclaw:
    requires:
      env:
        - PIXELDOJO_API_KEY
      bins:
        - curl
        - jq
        - python3
---
# PixelDojo

使用 PixelDojo 的异步 API 生成并下载 AI 图像或视频。

## 设置

运行时要求：
- 环境变量：`PIXELDOJO_API_KEY`
- 必需的 binaries：`curl`, `jq`, `python3`
- 可选配置：`PIXELDOJO_API_BASE`

在运行任何辅助工具之前，请先设置 API 密钥：

```bash
export PIXELDOJO_API_KEY=your_api_key_here
```

可选的本地环境文件：

```bash
cp ~/.openclaw/skills/pixeldojo/.env.example ~/.openclaw/skills/pixeldojo/.env
```

默认的 API 基址：`https://pixeldojo.ai/api/v1`

## 工作流程

1. 首先查看实时模型目录。
2. 选择符合所需工作流程的模型。
3. 使用 `generate.sh` 或 `Nano Banana` 辅助工具提交任务。
4. 监控任务状态，直到任务完成，然后获取下载后的资源路径。

请勿猜测模型 ID。

## 查看实时模型目录

```bash
bash ~/.openclaw/skills/pixeldojo/models.sh
```

有关已知可用模型 ID 及示例选择的详细信息，请参阅：
- `references/model-catalog.md`

## 生成图像

```bash
bash ~/.openclaw/skills/pixeldojo/generate.sh image "editorial product photo of a silver robot" flux-2-pro --aspect-ratio 16:9
```

推荐默认设置：
- 最佳通用图像质量：`flux-2-max`
- 提示遵循性和排版效果：`nano-banana-2`
- 适用于编辑的图像：`flux-kontext-pro`

## 生成视频

```bash
bash ~/.openclaw/skills/pixeldojo/generate.sh video "cinematic ocean waves at sunset" seedance-1.5 --duration 5
```

对于需要将图像转换为视频的模型，请使用 `--image-url` 参数：

```bash
bash ~/.openclaw/skills/pixeldojo/generate.sh video "slow camera push-in" wan-2.6-flash --image-url https://example.com/input.png --duration 5
```

## Nano Banana 辅助工具

当用户特别需要使用 `Nano Banana 2` 或高度遵循提示要求的功能时，请使用此工具：

```bash
python3 ~/.openclaw/skills/pixeldojo/scripts/generate-nano-banana.py "clean ecommerce hero shot of running shoes" --aspect-ratio 16:9 --output ~/Desktop/shoes.png
```

## 查看任务状态

```bash
bash ~/.openclaw/skills/pixeldojo/status.sh job_abc123
```

## 输出路径

默认下载文件夹：
- `~/Pictures/AI Generated/images/`
- `~/Pictures/AI Generated/videos/`

可以通过以下方式自定义下载路径：

```bash
--output /path/to/file.png
```

## 注意事项

- `generate.sh` 支持以下参数：`--aspect-ratio`, `--duration`, `--image-url`, `--output`, `--poll-interval`, `--max-wait`。
- `generate.sh` 遵循基于提示的通用 API 流程。如果请求需要特定模型的编辑功能，请在使用前先查看实时模型目录和 API 的相关说明。
- PixelDojo 对生成的输出内容提供完整的商业使用权，但用户仍需遵守服务条款以及任何第三方模型的使用限制。