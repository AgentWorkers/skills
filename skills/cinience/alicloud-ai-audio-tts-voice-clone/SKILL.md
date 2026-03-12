---
name: alicloud-ai-audio-tts-voice-clone
description: 使用阿里巴巴云模型工作室（Alibaba Cloud Model Studio）中的 Qwen TTS VC 模型进行语音克隆的工作流程。适用于从样本音频中创建克隆语音，以及使用克隆后的音色合成文本的场景。
version: 1.0.0
---
**类别：提供者**  
# Model Studio Qwen TTS 语音克隆功能  

该功能利用语音克隆模型，从用户提供的音频样本中复制出相应的语音特征。  

## 关键模型名称  
请使用以下模型名称之一：  
- `qwen3-tts-vc-2026-01-22`  
- `qwen3-tts-vc-realtime-2026-01-15`  

## 先决条件  
- 在虚拟环境中安装 SDK：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 将 `DASHSCOPE_API_KEY` 设置在环境变量中，或将其添加到 `~/.alibabacloud/credentials` 文件中。  

## 标准化接口（`tts.voice_clone`）  

### 请求参数  
- `text`（字符串，必填）：需要转换的文本内容  
- `voice_sample`（字符串或字节数据，必填）：用于生成语音的音频样本  
- `voice_name`（字符串，可选）：生成语音的名称  
- `stream`（布尔值，可选）：是否需要实时流式输出  

### 响应参数  
- `audio_url`（字符串）：生成的音频文件路径  
- `voice_id`（字符串）：生成的音频的唯一标识符  
- `request_id`（字符串）：请求的唯一标识符  

## 操作指南  
- 请使用背景噪声较低的清晰语音样本。  
- 遵守相关法律法规及政策要求，确保对克隆语音的使用符合规定。  
- 保存生成的 `voice_id`，以便后续重复使用。  

## 本地辅助脚本  
准备一个符合规范的请求 JSON 数据，并验证响应格式：  
```bash
.venv/bin/python skills/ai/audio/alicloud-ai-audio-tts-voice-clone/scripts/prepare_voice_clone_request.py \
  --text "Welcome to this voice-clone demo" \
  --voice-sample "https://example.com/voice-sample.wav"
```  

## 输出路径  
- 默认输出路径：`output/ai-audio-tts-voice-clone/audio/`  
- 可通过设置 `OUTPUT_DIR` 变量来更改输出路径。  

## 验证机制  
- 确保命令执行成功（返回代码为 0），并且生成 `output/alicloud-ai-audio-tts-voice-clone/validate.txt` 文件。  

## 输出结果与证据保存  
- 将所有生成的结果文件、命令输出以及 API 响应内容保存在 `output/alicloud-ai-audio-tts-voice-clone/` 目录下。  
- 在证据文件中记录关键参数（如区域、资源 ID、时间范围等），以便后续复现操作。  

## 工作流程  
1. 确认用户操作意图、所选区域、相关标识符，以及操作类型（仅读取数据还是修改数据）。  
2. 先运行一个最小的仅读取数据的查询，以验证网络连接和权限。  
3. 使用正确的参数和限定范围执行目标操作。  
4. 验证操作结果，并保存相应的输出文件和证据文件。  

## 参考资料  
- `references/sources.md`