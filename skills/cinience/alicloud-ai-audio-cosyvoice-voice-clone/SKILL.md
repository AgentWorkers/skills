---
name: alicloud-ai-audio-cosyvoice-voice-clone
description: >
  **使用说明：**  
  在使用 Alibaba Cloud Model Studio 的 CosyVoice 定制模型（尤其是 cosyvoice-v3.5-plus 或 cosyvoice-v3.5-flash）创建克隆语音时，请从参考音频文件中生成新的语音数据，并将返回的 `voice_id` 保存下来。之后，在后续的文本转语音（TTS）调用中，可以直接使用该 `voice_id` 来识别并播放该克隆语音。
version: 1.0.0
---
**类别：提供者**  
**# Model Studio CosyVoice 语音克隆**  

使用 CosyVoice 语音注册 API 从公共参考音频创建克隆语音。  

## 关键模型名称  
使用 `model="voice-enrollment"` 以及以下 `target_model` 值之一：  
- `cosyvoice-v3.5-plus`  
- `cosyvoice-v3.5-flash`  
- `cosyvoice-v3-plus`  
- `cosyvoice-v3-flash`  
- `cosyvoice-v2`  

**本仓库推荐的默认值：**  
`target_model="cosyvoice-v3.5-plus"`  

## 地区与兼容性  
- `cosyvoice-v3.5-plus` 和 `cosyvoice-v3-flash` 仅在中国大陆部署模式下可用（北京端点）。  
- 在国际部署模式下（新加坡端点），`cosyvoice-v3-plus` 和 `cosyvoice-v3-flash` 不支持语音克隆/设计功能。  
- 注册过程中使用的 `target_model` 必须与后续语音合成中使用的模型相匹配，否则合成会失败。  

## 端点  
- 国内：`https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization`  
- 国际：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`  

## 先决条件  
- 在您的环境中设置 `DASHSCOPE_API_KEY`，或将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中。  
- 提供用于注册的公共音频 URL。  

## 标准化接口（`cosyvoice.voice_clone`）  

### 请求  
- `model`（字符串，可选）：固定为 `voice-enrollment`  
- `target_model`（字符串，可选）：默认值为 `cosyvoice-v3.5-plus`  
- `prefix`（字符串，必填）：仅包含字母和数字，最多 10 个字符  
- `voice_sample_url`（字符串，必填）：公共音频 URL  
- `language_hints`（字符串数组，可选）：仅使用第一个元素  
- `maxprompt_audio_length`（浮点数，可选）：仅适用于 `cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-flash`  
- `enable_preprocess`（布尔值，可选）：仅适用于 `cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-flash`  

### 响应  
- `voice_id`（字符串）：在后续的 TTS 调用中用作 `voice` 参数  
- `request_id`（字符串）  
- `usage.count`（数字，可选）  

## 操作指南  
- 对于中文方言参考音频，将 `language_hints` 设置为 `["zh"]`；后续可以通过文本或 `instruct` 参数来控制方言风格。  
- 对于 `cosyvoice-v3.5-plus`，支持的 `language_hints` 包括 `zh`、`en`、`fr`、`de`、`ja`、`ko`、`ru`、`pt`、`th`、`id`、`vi`。  
- 避免频繁进行注册操作；每次调用都会创建一个新的自定义语音并消耗配额。  

## 本地辅助脚本  
准备一个标准化的请求 JSON 数据：  
```bash
python skills/ai/audio/alicloud-ai-audio-cosyvoice-voice-clone/scripts/prepare_cosyvoice_clone_request.py \
  --target-model cosyvoice-v3.5-plus \
  --prefix myvoice \
  --voice-sample-url https://example.com/voice.wav \
  --language-hint zh
```  

## 验证  
```bash
mkdir -p output/alicloud-ai-audio-cosyvoice-voice-clone
for f in skills/ai/audio/alicloud-ai-audio-cosyvoice-voice-clone/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/alicloud-ai-audio-cosyvoice-voice-clone/validate.txt
```  
验证通过的条件：命令返回 0，并生成 `output/alicloud-ai-audio-cosyvoice-voice-clone/validate.txt` 文件。  

## 输出与证据  
- 将生成的结果、命令输出以及 API 响应摘要保存在 `output/alicloud-ai-audio-cosyvoice-voice-clone/` 目录下。  
- 在证据文件中包含 `target_model`、`prefix` 和样本音频 URL。  

## 参考资料  
- `references/api_reference.md`  
- `references/sources.md`