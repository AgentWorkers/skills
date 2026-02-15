---
name: alicloud-ai-audio-tts-voice-clone
description: 使用阿里云模型工作室（Alibaba Cloud Model Studio）中的 Qwen TTS VC 模型进行语音克隆的工作流程。适用于从样本音频创建克隆语音，以及使用克隆后的音色合成文本的场景。
---

**类别：提供者**  
# Model Studio Qwen TTS 语音克隆  

使用语音克隆模型来复制来自注册音频样本的音色。  

## 关键模型名称  
使用以下模型名称之一：  
- `qwen3-tts-vc-2026-01-22`  
- `qwen3-tts-vc-realtime-2026-01-15`  

## 先决条件  
- 在虚拟环境中安装 SDK：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 将 `DASHSCOPE_API_KEY` 设置在您的环境中，或将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中。  

## 标准化接口（tts.voice_clone）  

### 请求  
- `text`（字符串，必填）  
- `voice_sample`（字符串 | 字节，必填）：注册音频样本  
- `voice_name`（字符串，可选）  
- `stream`（布尔值，可选）  

### 响应  
- `audio_url`（字符串）或流式 PCM 数据块  
- `voice_id`（字符串）  
- `request_id`（字符串）  

## 操作指南  
- 使用背景噪声较低的清晰语音样本。  
- 遵守关于克隆语音的同意和政策要求。  
- 保存生成的 `voice_id` 并在未来的合成请求中重复使用。  

## 本地辅助脚本  
准备一个标准化的请求 JSON 数据，并验证响应格式：  
```bash
.venv/bin/python skills/ai/audio/alicloud-ai-audio-tts-voice-clone/scripts/prepare_voice_clone_request.py \
  --text "欢迎来到语音复刻演示" \
  --voice-sample "https://example.com/voice-sample.wav"
```  

## 输出位置  
- 默认输出路径：`output/ai-audio-tts-voice-clone/audio/`  
- 可以使用 `OUTPUT_DIR` 变量覆盖默认输出目录。  

## 参考资料  
- `references/sources.md`