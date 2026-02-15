---
name: alicloud-ai-audio-tts-voice-design
description: 使用 Alibaba Cloud Model Studio 的 Qwen TTS VD 模型进行语音设计工作流程。该流程适用于从文本描述创建自定义合成语音，并将这些语音用于语音合成任务。
---

**类别：provider**

# Model Studio Qwen TTS 语音设计

使用语音设计模型，根据自然语言描述生成可控的合成语音。

## 关键模型名称

请使用以下模型字符串之一：
- `qwen3-tts-vd-2026-01-26`
- `qwen3-tts-vd-realtime-2025-12-16`

## 先决条件

- 在虚拟环境中安装 SDK：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

- 在您的环境中设置 `DASHSCOPE_API_KEY`，或将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中。

## 标准化接口（tts.voice_design）

### 请求
- `voice_prompt`（字符串，必填）：目标语音描述
- `text`（字符串，必填）
- `stream`（布尔值，可选）

### 响应
- `audio_url`（字符串）：音频文件链接
- `voice_id`（字符串）
- `request_id`（字符串）

## 操作指南

- 在编写语音提示时，需考虑语调、语速、情感和音色等因素。
- 为确保产品一致性，可以构建一个可重用的语音提示库。
- 在使用长脚本之前，先通过简短的语句验证生成的语音效果。

## 本地辅助脚本

准备一个标准化的请求 JSON 数据，并验证响应格式：

```bash
.venv/bin/python skills/ai/audio/alicloud-ai-audio-tts-voice-design/scripts/prepare_voice_design_request.py \
  --voice-prompt "A warm female host voice, clear articulation, medium pace" \
  --text "这是音色设计演示"
```

## 输出位置

- 默认输出路径：`output/ai-audio-tts-voice-design/audio/`
- 可通过 `OUTPUT_DIR` 变量覆盖默认输出目录。

## 参考资料

- `references/sources.md`