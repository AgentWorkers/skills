---
name: best-image-generation
description: 最高质量的AI图像生成服务（每张图像的成本约为0.12-0.20美元）。支持文本到图像、图像到图像的转换，以及通过EvoLink API进行图像编辑。
homepage: https://evolink.ai
metadata: {"openclaw": {"emoji": "🎨", "requires": {"env": ["EVOLINK_API_KEY"]}, "primaryEnv": "EVOLINK_API_KEY"}}
---
# EvoLink 最佳图像生成服务

通过 EvoLink Nano Banana Pro (gemini-3-pro-image-preview) API 生成和编辑图像。

## API 端点

- 基本地址：`https://api.evolink.ai/v1`
- 提交请求：`POST /images/generations`
- 查询结果：`GET /tasks/{id}`

## 第一步 — 提交任务

### 文本转图像

```json
{
  "model": "gemini-3-pro-image-preview",
  "prompt": "<USER_PROMPT>",
  "size": "<SIZE>",
  "quality": "<QUALITY>"
}
```

### 图像转图像 / 编辑

```json
{
  "model": "gemini-3-pro-image-preview",
  "prompt": "<USER_PROMPT>",
  "size": "<SIZE>",
  "quality": "<QUALITY>",
  "image_urls": ["<URL1>", "<URL2>"]
}
```

| 参数 | 可选值 |
|---|---|
| size | auto, 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |
| quality | 1K, 2K（默认），4K（额外费用） |
| image_urls | 最多 10 个图像链接（每个链接大小不超过 10MB，支持格式：jpeg/jpg/png/webp） |

## 第二步 — 查询结果

使用 `GET /tasks/{id}` 每 10 秒查询一次任务状态，最多尝试 72 次（约 12 分钟）。

等待任务状态变为 `completed` 或 `failed`。

## 第三步 — 下载并输出结果

从 `results[0]` 中下载图像链接。系统会自动检测图像格式（png/jpg/webp），并将文件保存为 `evolink-<TIMESTAMP>.<ext>`。

**重要安全提示：** 在将 `<OUTPUT_FILE>` 传递给 shell 命令之前，请进行以下处理：
- 去除所有 shell 特殊字符：`tr -cd 'A-Za-z0-9._-'`
- 确保文件扩展名为 `.png`、`.jpg`、`.jpeg` 或 `.webp`
- 如果结果为空，则默认保存为 `evolink-<timestamp>.png`

为了在 OC（Online Catalog）中自动关联图像，需要输出 `MEDIA:<absolute_path>`。

## 参考实现

| 平台 | 文档文件 |
|---|---|
| Python（所有平台，无依赖） | `{baseDir}/references/python.md` |
| PowerShell 5.1+（Windows） | `{baseDir}/references/powershell.md` |
| curl + bash（Unix/macOS） | `{baseDir}/references/curl_heredoc.md` |

## API 密钥

- 需要设置环境变量 `EVOLINK_API_KEY`，可在 [https://evolink.ai] 获取密钥。

## 触发命令

- 中文：`高质量生图：xxx` / `编辑图片：xxx`
- 英文：`best image: xxx` / `edit image: xxx`

冒号后的文本被视为用户输入的提示。默认使用 `auto` 大小和 `2K` 质量进行生成。

对于图像转图像或编辑操作，用户需要提供图像链接作为参数。

## 注意事项

- 为了在 OC 中自动关联图像，只需输出 `MEDIA:<path>`，无需额外处理逻辑。
- 图像会保存在本地，格式由系统自动检测（支持 png/jpg/webp）。
- 使用 `quality: 4K` 会产生额外费用。
- `image_urls` 参数最多支持 10 个链接，每个链接大小不超过 10MB，支持格式：jpeg/jpg/png/webp。