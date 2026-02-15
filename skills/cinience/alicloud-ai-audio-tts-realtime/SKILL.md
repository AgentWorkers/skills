---
name: alicloud-ai-audio-tts-realtime
description: 实时语音合成功能支持使用阿里巴巴云模型工作室（Alibaba Cloud Model Studio）的 Qwen TTS 实时模型。当需要低延迟的交互式语音服务时，该功能非常实用，例如在需要根据用户指令进行实时语音合成的场景中。
---

**类别：提供者**  
# Model Studio Qwen TTS 实时版  

使用实时 TTS 模型实现低延迟的语音流输出。  

## 关键模型名称  
请使用以下模型名称之一：  
- `qwen3-tts-flash-realtime`  
- `qwen3-tts-instruct-flash-realtime`  
- `qwen3-tts-instruct-flash-realtime-2026-01-22`  

## 先决条件  
- 在虚拟环境中安装 SDK：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 将 `DASHSCOPE_API_KEY` 设置在您的环境中，或将其添加到 `~/.alibabacloud/credentials` 文件中。  

## 标准化接口（tts.realtime）  

### 请求  
- `text`（字符串，必填）  
- `voice`（字符串，必填）  
- `instruction`（字符串，可选）  
- `sample_rate`（整数，可选）  

### 响应  
- `audio_base64pcm_chunks`（字符串数组）  
- `sample_rate`（整数）  
- `finish_reason`（字符串）  

## 操作指南  
- 使用 WebSocket 或流式接口实现实时模式。  
- 为降低延迟，请确保每次语音生成的时长较短。  
- 对于指令型模型，务必使指令明确且简洁。  
- 某些 SDK/运行时组合可能不支持通过 `MultiModalConversation` 调用实时模型；请使用下面的测试脚本来验证兼容性。  

## 本地演示脚本  
使用测试脚本来验证当前 SDK/运行时的实时兼容性；如果需要，可回退到非实时模型以立即获得输出：  
```bash
.venv/bin/python skills/ai/audio/alicloud-ai-audio-tts-realtime/scripts/realtime_tts_demo.py \
  --text "这是一个 realtime 语音演示。" \
  --fallback \
  --output output/ai-audio-tts-realtime/audio/fallback-demo.wav
```  

**严格模式（用于持续集成/权限控制）：**  
```bash
.venv/bin/python skills/ai/audio/alicloud-ai-audio-tts-realtime/scripts/realtime_tts_demo.py \
  --text "realtime health check" \
  --strict
```  

## 输出路径  
- 默认输出路径：`output/ai-audio-tts-realtime/audio/`  
- 可通过 `OUTPUT_DIR` 变量覆盖默认路径。  

## 参考资料  
- `references/sources.md`