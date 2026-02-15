---
name: qwen-image-plus-sophnet
description: 通过 Sophnet Qwen-Image-Plus 生成图像，并监控任务的完成情况。当用户请求 Sophnet 图像生成、使用 Qwen-Image-Plus 或从 Sophnet API 请求图像时，请使用此方法。
---

# Qwen-Image-Plus（Sophnet）图像生成

使用 Sophnet 图像生成 API 创建一个图像生成任务，持续轮询直到任务完成，然后返回生成的图像 URL。

## 快速入门

设置 API 密钥（推荐使用）：
```bash
export SOPHNET_API_KEY="YOUR_API_KEY"
```

使用绝对路径运行脚本（切勿进入技能目录）：
```bash
bash /home/shutongshan/.openclaw/workspace/skills/qwen-image-plus-sophnet/scripts/generate_image.sh --prompt "your prompt"
```

## 脚本参数

- `--prompt`（必需）：用户提示语
- `--negative-prompt`（可选）
- `--size`（可选，默认值：1024*1024）
- `--n`（可选，默认值：1）
- `--watermark`（可选，默认值：false）
- `--prompt-extend`（可选，默认值：true）
- `--api-key`（可选，会覆盖 `SOPHNET_API_KEY` 的设置）
- `--poll-interval`（可选，默认值：2）
- `--max-wait`（可选，默认值：300）

## 输出格式

脚本会输出以下内容：
- `TASK_ID=...`
- `STATUS=succeeded`（任务成功）
- `IMAGE_URL=...`（生成的图像 URL）

使用 `IMAGE_URL` 值来响应用户。

## 工作流程

1. 发送 POST 请求，请求内容包含 `model=Qwen-Image-Plus` 和用户提示语
2. 持续轮询 GET 请求以获取任务状态，直到状态变为 `SUCCEEDED`
3. 提取生成的图像 URL 并返回给用户

## 实际示例（运行结果）

提示语：
```text
A scenic mountain landscape in ink wash style
```

命令：
```bash
bash /home/shutongshan/.openclaw/workspace/skills/qwen-image-plus-sophnet/scripts/generate_image.sh \
  --prompt "A scenic mountain landscape in ink wash style" \
  --negative-prompt "blurry, low quality" \
  --size "1024*1024" \
  --n 1 \
  --watermark false \
  --prompt-extend true
```

输出结果：
```text
TASK_ID=7BWFICt0zgLvuaTKg8ZoDg
STATUS=succeeded
IMAGE_URL=https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/7d/d5/20260203/cfc32567/f0e3ac18-31f6-4a1a-b680-a71d3e6bcbe03032414431.png?Expires=1770714400&OSSAccessKeyId=LTAI5tKPD3TMqf2Lna1fASuh&Signature=fF12GZ7RgGsC7OpEkGCapkBUXws%3D
```

## 常见错误

- `Error: No API key provided.`（错误：未提供 API 密钥。）→ 请设置 `SOPHNET_API_KEY` 或使用 `--api-key` 参数。
- `STATUS=failed`（错误：任务失败。）→ 检查 API 密钥权限或参数设置。
- `Error: url not found in response`（错误：响应中未找到图像 URL。）→ 请手动检查 API 响应内容。