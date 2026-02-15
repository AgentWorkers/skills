---
name: masonry
description: 使用 Masonry CLI 进行基于 AI 的图像和视频生成。可以生成图像和视频，查看作业状态，并管理媒体资产。
metadata:
  author: masonry-ai
  version: "1.0"
compatibility: Requires masonry CLI installed (curl -sSL https://media.masonry.so/cli/install.sh | sh)
allowed-tools: Bash(masonry:*)
---

# Masonry CLI

`masonry` CLI 提供了基于人工智能的图像和视频生成功能。

## 适用场景

当用户需要执行以下操作时，可以使用此 CLI：
- 根据文本提示生成图像
- 根据文本提示生成视频
- 查看生成作业的状态
- 下载生成的媒体文件
- 列出可用的 AI 模型
- 查看生成历史记录

## 安装

如果 `masonry` 命令不可用，请先进行安装：

```bash
curl -sSL https://media.masonry.so/cli/install.sh | sh
```

## 常用命令

```bash
# Generate image
masonry image "your prompt here" --aspect 16:9

# Generate video
masonry video "your prompt here" --duration 4

# Check job status
masonry job status <job-id>

# Download result
masonry job download <job-id> -o ./output.png

# List available models
masonry models list --type image
masonry models list --type video
```

## 详细工作流程

### 图像生成
```bash
# Basic generation
masonry image "a sunset over mountains, photorealistic"

# With options
masonry image "cyberpunk cityscape" --aspect 16:9 --model imagen-3.0-generate-002

# Available flags
#   --aspect, -a     Aspect ratio (16:9, 9:16, 1:1)
#   --dimension, -d  Exact size (1920x1080)
#   --model, -m      Model key
#   --output, -o     Output path
#   --negative-prompt What to avoid
#   --seed           Reproducibility seed
```

### 视频生成
```bash
# Basic generation
masonry video "ocean waves crashing on rocks"

# With options
masonry video "drone shot of forest" --duration 6 --aspect 16:9

# Available flags
#   --duration       Length in seconds (4, 6, 8)
#   --aspect, -a     Aspect ratio (16:9, 9:16)
#   --model, -m      Model key
#   --image, -i      First frame image
#   --no-audio       Disable audio generation
```

### 作业管理
```bash
# List recent jobs
masonry job list

# Check specific job
masonry job status <job-id>

# Wait for completion and download
masonry job wait <job-id> --download -o ./result.png

# View local history
masonry history list
masonry history pending --sync
```

### 模型探索
```bash
# List all models
masonry models list

# Filter by type
masonry models list --type video

# Get model parameters
masonry models params veo-3.1-fast-generate-preview
```

## 命令返回格式

所有命令的返回结果均为 JSON 格式：

```json
{
  "success": true,
  "job_id": "abc-123",
  "status": "pending",
  "check_after_seconds": 10,
  "check_command": "masonry job status abc-123"
}
```

## 认证

如果命令执行过程中出现认证错误，请参考以下说明：

```bash
masonry login
```

## 高级项目技能

对于具有详细工作流程的项目特定技能，可以运行以下命令来安装相应的工具：
- `masonry-generate`：用于图像生成的详细工作流程
- `masonry-models`：用于探索 AI 模型
- `masonry-jobs`：用于管理生成作业

这些工具会安装到 `.claude/skills/` 目录中：