---
name: alicloud-ai-audio-tts
description: 使用 Model Studio DashScope 的 Qwen TTS 模型（qwen3-tts-flash、qwen3-tts-instruct-flash）生成类似人类的语音音频。这些模型适用于将文本转换为语音、为短剧或新闻视频制作语音台词，以及为 DashScope 记录 TTS 请求/响应字段。
---

**类别：提供者**  
# Model Studio Qwen TTS  

## 关键模型名称  
建议使用以下模型之一：  
- `qwen3-tts-flash`  
- `qwen3-tts-instruct-flash`  
- `qwen3-tts-instruct-flash-2026-01-26`  

## 先决条件  
- 安装 SDK（建议在虚拟环境中安装，以避免违反 PEP 668 规范）：  

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 在您的环境中设置 `DASHSCOPE_API_KEY`，或将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中（环境变量优先级更高）。  

## 标准化接口（`tts.generate`）  
### 请求参数  
- `text`（字符串，必填）  
- `voice`（字符串，必填）  
- `language_type`（字符串，可选；默认值为 `Auto`）  
- `instruction`（字符串，可选；建议用于指令模型）  
- `stream`（布尔值，可选；默认值为 `False`）  

### 响应参数  
- `audio_url`（字符串，当 `stream` 为 `False` 时）  
- `audio_base64 pcm`（字符串，当 `stream` 为 `True` 时）  
- `sample_rate`（整数，24000）  
- `format`（字符串，根据模式为 `wav` 或 `pcm`）  

## 快速入门（Python + DashScope SDK）  
```python
import os
import dashscope

# Prefer env var for auth: export DASHSCOPE_API_KEY=...
# Or use ~/.alibabacloud/credentials with dashscope_api_key under [default].
# Beijing region; for Singapore use: https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

text = "Hello, this is a short voice line."
response = dashscope.MultiModalConversation.call(
    model="qwen3-tts-instruct-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text=text,
    voice="Cherry",
    language_type="English",
    instruction="Warm and calm tone, slightly slower pace.",
    stream=False,
)

audio_url = response.output.audio.url
print(audio_url)
```  

## 流式传输说明  
- 当 `stream` 设置为 `True` 时，会返回以 24kHz 速率编码的 PCM 数据块。  
- 解码这些数据块后可以播放，或将其合并到 PCM 缓冲区中。  
- 当流式传输结束时，响应中会包含 `finish_reason == "stop"`。  

## 运维指南  
- 保持请求简洁；如果遇到长度限制或超时错误，请将长文本拆分为多个请求。  
- 使用与文本匹配的 `language_type` 以改善发音效果。  
- 仅在需要明确控制语音风格/语气时使用 `instruction` 参数。  
- 通过 `(text, voice, language_type)` 的键值对进行缓存，以避免重复请求带来的开销。  

## 输出路径  
- 默认输出路径：`output/ai-audio-tts/audio/`  
- 可通过 `OUTPUT_DIR` 变量覆盖默认路径。  

## 参考资料  
- `references/api_reference.md`：参数映射和流式传输示例。  
- 实时模式的相关功能位于 `skills/ai/audio/alicloud-ai-audio-tts-realtime/`。  
- 语音克隆/设计相关功能位于 `skills/ai/audio/alicloud-ai-audio-tts-voice-clone/` 和 `skills/ai/audio/alicloud-ai-audio-tts-voice-design/`。  
- 源代码列表：`references/sources.md`