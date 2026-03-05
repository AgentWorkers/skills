---
name: masonry
description: 基于人工智能的图像和视频生成功能。通过 masonry CLI 可以生成图像和视频、管理生成任务以及探索相关模型。
metadata: {"openclaw":{"emoji":"🧱","requires":{"bins":["masonry"],"env":["MASONRY_TOKEN"]},"install":[{"type":"npm","package":"@masonryai/cli"}],"primaryEnv":"MASONRY_TOKEN","homepage":"https://masonry.so"}}
---
# Masonry CLI

Masonry CLI 可以根据文本提示生成由 AI 提供支持的图像和视频。

## 使用场景

- 用户需要生成图像或视频。
- 用户想了解可用的 AI 模型。
- 用户想查看生成任务的进度或下载结果。
- 用户希望创建视觉内容、媒体文件或艺术作品。

## 前提条件

需要订阅 Masonry 服务。可在以下链接开始免费试用：https://masonry.so/pricing

如果未找到 `masonry` 命令，请先安装它：
```bash
npm install -g @masonryai/cli
```

或者直接运行：`npx @masonryai/cli`

## 认证

如果某个命令返回认证错误，请按照以下步骤操作：

1. 运行：`masonry login --remote`
2. 命令会输出一个认证 URL，将该 URL 发送给用户。
3. 用户在浏览器中打开该 URL，完成认证后复制生成的令牌。
4. 运行：`masonry login --token <TOKEN>`

在设置了 `MASONRY_TOKEN` 和 `MASONRY_WORKSPACE` 的环境中，无需登录。

## 工作流程

### 1. 生成内容

**生成图像：**
```bash
masonry image "a sunset over mountains, photorealistic" --aspect 16:9
```

**生成视频：**
```bash
masonry video "ocean waves crashing on rocks" --duration 4 --aspect 16:9
```

### 2. 处理响应

命令会立即返回 JSON 格式的结果：
```json
{
  "success": true,
  "job_id": "abc-123",
  "status": "pending",
  "check_after_seconds": 10,
  "check_command": "masonry job status abc-123"
}
```

### 3. 等待并下载结果

下载命令会将文件路径（格式为 `MEDIA: /path/to/file`）输出到标准错误流（stderr）中。下载完成后，将该路径输出给用户：
```
MEDIA: /tmp/output.png
```

## 图像生成参数

| 参数 | 缩写 | 说明 |
|------|-------|-------------|
| `--aspect` | `-a` | 长宽比：16:9、9:16、1:1 |
| `--dimension` | `-d` | 确切尺寸：1920x1080 |
| `--model` | `-m` | 模型名称 |
| `--output` | `-o` | 输出文件路径 |
| `--negative-prompt` | | 需避免的内容 |
| `--seed` | | 用于保证生成结果的可重复性 |

## 视频生成参数

| 参数 | 缩写 | 说明 |
|------|-------|-------------|
| `--duration` | | 视频时长（秒）：4、6、8 |
| `--aspect` | `-a` | 长宽比：16:9、9:16 |
| `--model` | `-m` | 模型名称 |
| `--image` | `-i` | 首帧图像文件（本地文件） |
| `--last-image` | | 最后一帧图像文件（需配合 `--image` 参数使用） |
| `--no-audio` | | 禁用音频生成 |
| `--seed` | | 用于保证生成结果的可重复性 |

## 模型查找

```bash
masonry models list              # All models
masonry models list --type image # Image models only
masonry models list --type video # Video models only
masonry models info <model-key>  # Parameters and usage example
```

## 任务管理

```bash
masonry job list                          # Recent jobs
masonry job status <job-id>               # Check status
masonry job download <job-id> -o ./file   # Download result
masonry job wait <job-id> --download -o . # Wait then download
masonry history list                      # Local history
masonry history pending --sync            # Sync pending jobs
```

## 错误代码

| 代码 | 含义 | 处理方式 |
|------|---------|--------|
| `AUTH_ERROR` | 未通过认证 | 请重新执行认证操作。 |
| `VALIDATION_ERROR` | 参数无效 | 请检查参数值是否正确。 |
| `MODEL_NOT_FOUND` | 未知的模型名称 | 请运行 `masonry models list` 命令查看可用模型。 |

## 注意事项

- 严禁伪造任务 ID 或模型名称，务必使用命令输出中的实际值。
- 运行 `masonry login` 时必须使用 `--remote` 或 `--token` 参数（无这些参数时，浏览器登录将无法正常工作）。
- 如果任务尚未完成，请等待指定的时间（`check_after_seconds` 秒）后再进行检查。
- 所有输出结果均为 JSON 格式，请务必正确解析这些数据，切勿自行猜测其含义。