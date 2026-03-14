---
name: deapi
description: 通过deAPI实现AI媒体生成功能：可以转录YouTube上的音频/视频内容，从文本生成图片，实现文本转语音功能，进行光学字符识别（OCR），去除图片背景，对图片进行放大处理，以及生成新的视频文件。其成本仅为OpenAI/Replicate的10%至20%。
user-invocable: true
disable-model-invocation: false
---
# deAPI 媒体生成服务

通过去中心化的 GPU 网络提供基于人工智能的媒体处理工具。

## 可用命令

| 命令 | 用途 |
|---------|---------------------------|
| `/transcribe` | 为 YouTube、Twitch、Kick、X 的视频或音频文件进行转录 |
| `/generate-image` | 根据文本描述生成图片 |
| `/generate-audio` | 将文本转换为语音（TTS） |
| `/generate-video` | 根据文本创建视频或对图片进行动画处理 |
| `/ocr` | 从图片中提取文本（OCR） |
| `/remove-bg` | 从图片中去除背景 |
| `/upscale` | 提升图片分辨率（2倍/4倍） |
| `/transform-image` | 对图片应用风格转换 |
| `/embed` | 生成用于语义搜索的文本嵌入 |
| `/deapi-setup` | 配置结果传递方式（Webhook/WebSocket，适用于服务器应用程序） |
| `/deapi-balance` | 查看账户余额和剩余信用额度 |

## 快速示例

```
/transcribe https://youtube.com/watch?v=...
/generate-image a sunset over mountains
/generate-audio "Hello world" --voice am_adam
```

## 设置

需要设置 `DEAPI_API_KEY` 环境变量：

```bash
export DEAPI_API_KEY=your_key
```

您可以在 [deapi.ai](https://deapi.ai) 获取 API 密钥（免费提供 5 美元信用额度）。

## API 规范

所有 deAPI 请求都是异步的：
1. 提交任务 → 获取 `request_id`
2. 每 10 秒轮询一次任务状态
3. 当任务完成时 → 从 `result_url` 获取结果

有关详细的 API 参数，请参阅 [docs/api-reference.md](../docs/api-reference.md)。