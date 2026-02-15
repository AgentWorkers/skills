---
name: seedream-image-gen
description: 通过 Seedream API（doubao-seedream 模型）生成图像。支持同步生成。
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["python3"],"env":["SEEDREAM_API_KEY"]},"primaryEnv":"SEEDREAM_API_KEY"}}
---

# Seedream 图像生成

使用 Seedream API 生成图像（同步模式，无需轮询）。

## 生成图像

```bash
python3 {baseDir}/scripts/generate_image.py --prompt "your description" --filename "output.png"
```

可选参数：
- `--size`：图像尺寸，可选值为 `2K`、`4K` 或具体的像素数（例如 `2048x2048`）
- `--input-image`：用于图像转换或编辑的源图像 URL

## API 密钥

`SEEDREAM_API_KEY` 会自动从 `clawdbot.json` 文件中的 `skills.entries.seedream-image-gen.apiKey` 中获取，无需手动输入。

## 注意事项：
- 同步 API：图像生成完成后会立即返回结果（无需进行轮询）
- 生成的图像 URL 在 24 小时内有效
- 脚本会输出 `MEDIA:` 行以便自动附加图像文件
- 文件名中会包含日期时间戳，以便区分不同的图像
- 4.5/4.0 版本的模型支持批量图像生成（每次请求可生成多张图像）