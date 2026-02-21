---
name: cheapest-image-generation
description: 这可能是最便宜的AI图像生成服务了（每张图片的成本约为0.0036美元）。通过EvoLink API实现文本到图像的转换。
homepage: https://evolink.ai
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"env": ["EVOLINK_API_KEY"]}, "primaryEnv": "EVOLINK_API_KEY"}}
---
# EvoLink 最便宜的图像生成服务

通过 EvoLink 的 z-image-turbo API 生成图像。

## API 端点

- 基础地址：`https://api.evolink.ai/v1`
- 提交请求：`POST /images/generations`
- 查看任务进度：`GET /tasks/{id}`

## 第一步 — 提交生成任务

```json
{
  "model": "z-image-turbo",
  "prompt": "<USER_PROMPT>",
  "size": "<SIZE>",
  "nsfw_check": <true|false>
}
```

可选字段：`"seed": <INT>`

| 参数 | 可能的值 |
|---|---|
| size | 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9, 1:2, 2:1 |
| nsfw_check | `true` / `false`（默认值：`false`） |
| seed | 任意整数（可选，用于保证生成结果的一致性） |

## 第二步 — 查看任务进度

使用 `GET /tasks/{id}` 命令，每 10 秒查询一次任务进度，最多尝试 72 次（约 12 分钟）。

等待任务状态变为 `completed` 或 `failed`。

## 第三步 — 下载并输出结果

从 `results[0]` 中获取图像的 URL，并自动检测图像格式（webp、png 或 jpg）。将图像保存为 `evolink-<TIMESTAMP>.<ext>`。

输出 `MEDIA:<absolute_path>` 以便在 OpenClaw 中自动插入图像。

## 参考实现方式

| 平台 | 文件路径 |
|---|---|
| Python（支持所有平台，无需额外依赖） | `{baseDir}/references/python.md` |
| PowerShell 5.1+（Windows） | `{baseDir}/references/powershell.md` |
| curl + bash（Unix/macOS） | `{baseDir}/references/curl_heredoc.md` |

## API 密钥

- 需要设置环境变量 `EVOLINK_API_KEY` 来访问 API。
- 获取 API 密钥：https://evolink.ai

## 使用指令

- 中文指令：`生图：xxx` / `出图：xxx` / `生成图片：xxx`
- 英文指令：`generate image: xxx` / `generate a picture: xxx`

冒号后的内容作为 `prompt` 参数使用，默认图像尺寸为 `1:1`，命令会立即执行图像生成。

## 注意事项

- 脚本会输出 `MEDIA:<path>`，以便在 OpenClaw 中自动插入图像；无需额外的传输逻辑。
- 图像会保存在本地，格式由 URL 自动检测；URL 的有效期约为 24 小时，但本地文件会长期保存。