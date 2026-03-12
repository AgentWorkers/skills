---
name: alicloud-ai-audio-tts
description: 使用 Model Studio DashScope 的 Qwen TTS 模型（qwen3-tts-flash、qwen3-tts-instruct-flash）生成类似人类的语音音频。这些模型适用于将文本转换为语音、为短剧或新闻视频制作旁白，以及为 DashScope 文档记录语音转文本（TTS）请求/响应的相关信息。
version: 1.0.0
---
**类别：提供者（Provider）**

# Model Studio Qwen TTS

## 验证（Validation）

```bash
mkdir -p output/alicloud-ai-audio-tts
python -m py_compile skills/ai/audio/alicloud-ai-audio-tts/scripts/generate_tts.py && echo "py_compile_ok" > output/alicloud-ai-audio-tts/validate.txt
```

**通过标准（Pass criteria）：** 命令以 0 的状态退出，并且生成了 `output/alicloud-ai-audio-tts/validate.txt` 文件。

## 输出与证据（Output and Evidence）

- 将生成的音频链接、样本音频文件以及请求数据保存到 `output/alicloud-ai-audio-tts/` 目录中。
- 每次执行操作都会生成一个验证日志。

## 关键模型名称（Critical model names）

建议使用以下模型之一：
- `qwen3-tts-flash`
- `qwen3-tts-instruct-flash`
- `qwen3-tts-instruct-flash-2026-01-26`

## 先决条件（Prerequisites）

- 安装 SDK（建议在虚拟环境（venv）中安装，以避免违反 PEP 668 规范）：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

- 在您的环境中设置 `DASHSCOPE_API_KEY`，或者将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中（环境变量优先级更高）。

## 标准化接口（Normalized interface: tts.generate）

### 请求（Request）

- `text`（字符串，必填）
- `voice`（字符串，必填）
- `language_type`（字符串，可选；默认值为 `Auto`）
- `instruction`（字符串，可选；对于指令模型推荐使用）
- `stream`（布尔值，可选；默认值为 `false`）

### 响应（Response）

- `audio_url`（字符串，当 `stream` 为 `false` 时）
- `audio_base64 pcm`（字符串，当 `stream` 为 `true` 时）
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

## 流式传输说明（Streaming notes）

- 当 `stream` 设置为 `true` 时，会返回 24kHz 频率的 Base64 编码 PCM 数据块。
- 解码这些数据块后可以播放它们，或者将它们合并到一个 PCM 缓冲区中。
- 当流式传输结束时，响应中会包含 `finish_reason == "stop"` 的信息。

## 操作指南（Operational guidance）

- 保持请求简洁；如果遇到大小限制或超时错误，可以将长文本拆分成多个请求进行发送。
- 使用与文本匹配的 `language_type` 以获得更好的发音效果。
- 仅在需要明确控制语音风格/语气时使用 `instruction` 参数。
- 通过 `(text, voice, language_type)` 的组合来缓存结果，以避免重复请求的开销。

## 输出位置（Output location）

- 默认输出路径：`output/alicloud-ai-audio-tts/audio/`
- 可以使用 `OUTPUT_DIR` 变量覆盖默认输出目录。

## 工作流程（Workflow）

1) 确认用户的意图、地区、标识符，以及操作是只读还是可修改的。
2) 首先运行一个最小的只读查询，以验证连接性和权限。
3) 使用明确的参数和有限的权限范围执行目标操作。
4) 验证结果并保存输出文件和证据文件。

## 参考资料（References）

- 请参阅 `references/api_reference.md` 以了解参数映射和流式传输的示例。
- 实时模式由 `skills/ai/audio/alicloud-ai-audio-tts-realtime/` 提供。
- 语音克隆/设计功能由 `skills/ai/audio/alicloud-ai-audio-tts-voice-clone/` 和 `skills/ai/audio/alicloud-ai-audio-tts-voice-design/` 提供。
- 源代码列表：`references/sources.md`