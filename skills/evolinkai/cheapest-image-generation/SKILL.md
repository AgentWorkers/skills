---
name: cheapest-image-generation
description: 这可能是最便宜的AI图像生成服务了（每张图片的成本约为0.0036美元）。通过EvoLink API实现文本到图像的转换。
homepage: https://evolink.ai
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"env": ["EVOLINK_API_KEY"]}, "primaryEnv": "EVOLINK_API_KEY"}}
---
# EvoLink 最便宜的图像生成服务

通过 EvoLink 的 `z-image-turbo` API 生成图像。

## API 端点

- 基本地址：`https://api.evolink.ai/v1`
- 提交请求：`POST /images/generations`
- 查询结果：`GET /tasks/{id}`

## 第一步 — 提交任务

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

## 第二步 — 查询任务结果

使用 `GET /tasks/{id}` 请求，每 10 秒查询一次任务状态，最多尝试 72 次（约 12 分钟）。

等待任务状态变为 `completed` 或 `failed`。

## 第三步 — 下载并输出结果

从 `results[0]` 中获取图像的 URL，并自动检测图像格式（webp、png 或 jpg），然后将其保存为 `evolink-<TIMESTAMP>.<ext>`。

**重要安全提示：** 在将 `<OUTPUT_FILE>` 传递给 shell 命令之前，必须对其进行安全处理：
- 去除所有 shell 元字符：`tr -cd 'A-Za-z0-9._-'`
- 确保文件扩展名有效（`.webp`、`.png`、`.jpg` 或 `.jpeg`）
- 如果 `results[0]` 为空，则默认保存为 `evolink-<TIMESTAMP>.webp`

将生成的图像路径（`MEDIA:<absolute_path>`）打印出来，以便在 OC（OpenClaw）中自动插入图像。

## 参考实现方式

| 平台 | 文件路径 |
|---|---|
| Python（所有平台，无依赖） | `{baseDir}/references/python.md` |
| PowerShell 5.1+（Windows） | `{baseDir}/references/powershell.md` |
| curl + bash（Unix/macOS） | `{baseDir}/references/curl_heredoc.md` |

## API 密钥

- 需要设置环境变量 `EVOLINK_API_KEY` 来获取 API 密钥
- 获取密钥的地址：https://evolink.ai

## 使用触发命令

- 中文：`生图：xxx` / `出图：xxx` / `生成图片：xxx`
- 英文：`generate image: xxx` / `generate a picture: xxx`

冒号后面的文本被视为命令提示；默认使用尺寸比例 `1:1`，并立即开始生成图像。

## 注意事项

- 生成的图像会自动保存在本地（格式由 URL 自动检测），保存的文件会持续存在。
- 无需额外的传输逻辑，因为 OC 会自动处理图像的插入。