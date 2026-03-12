---
name: alicloud-ai-audio-tts-realtime
description: 实时语音合成功能基于阿里云Model Studio的Qwen TTS实时模型实现。适用于需要低延迟交互式语音的场景，包括由指令控制的实时语音合成。
version: 1.0.0
---
**类别：提供者**  
# Model Studio Qwen TTS 实时模式  

使用实时 TTS 模型实现低延迟的语音流输出。  

## 关键模型名称  
请使用以下模型名称之一：  
- `qwen3-tts-flash-realtime`  
- `qwen3-tts-instruct-flash-realtime`  
- `qwen3-tts-instruct-flash-realtime-2026-01-22`  
- `qwen3-tts-vd-realtime-2026-01-15`  
- `qwen3-tts-vc-realtime-2026-01-15`  

## 先决条件  
- 在虚拟环境中安装 SDK：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 将 `DASHSCOPE_API_KEY` 设置在环境中，或将其添加到 `~/.alibabacloud/credentials` 文件中。  

## 标准化接口（tts.realtime）  
### 请求参数  
- `text`（字符串，必填）  
- `voice`（字符串，必填）  
- `instruction`（字符串，可选）  
- `sample_rate`（整数，可选）  

### 响应参数  
- `audio_base64pcm_chunks`（字符串数组）  
- `sample_rate`（整数）  
- `finish_reason`（字符串）  

## 操作指南  
- 使用 WebSocket 或流式端点实现实时模式。  
- 为降低延迟，请确保每次语音生成的时长较短。  
- 对于指令型模型，务必使指令明确且简洁。  
- 某些 SDK/运行时组合可能不支持通过 `MultiModalConversation` 调用实时模型；请使用下面的测试脚本来验证兼容性。  

## 本地测试脚本  
使用测试脚本来验证当前 SDK/运行时的实时兼容性；如果无法使用实时模式，可回退到非实时模型以立即获取输出：  
```bash
.venv/bin/python skills/ai/audio/alicloud-ai-audio-tts-realtime/scripts/realtime_tts_demo.py \
  --text "This is a realtime speech demo." \
  --fallback \
  --output output/ai-audio-tts-realtime/audio/fallback-demo.wav
```  

**严格模式（用于持续集成/权限控制）**  
```bash
.venv/bin/python skills/ai/audio/alicloud-ai-audio-tts-realtime/scripts/realtime_tts_demo.py \
  --text "realtime health check" \
  --strict
```  

## 输出路径  
- 默认输出路径：`output/ai-audio-tts-realtime/audio/`  
- 可通过 `OUTPUT_DIR` 变量覆盖默认路径。  

## 验证规则  
- 命令执行成功时返回 0，且会生成 `output/alicloud-ai-audio-tts-realtime/validate.txt` 文件。  

## 输出与证据记录  
- 将所有生成的结果、命令输出及 API 响应内容保存到 `output/alicloud-ai-audio-tts-realtime/` 目录下。  
- 确保在证据文件中包含关键参数（区域、资源 ID、时间范围等信息），以便后续复现。  

## 工作流程  
1) 确认用户意图、操作区域、所需资源标识符，以及操作是只读还是可修改的。  
2) 首先运行一个最小的只读查询以验证连接性和权限。  
3) 使用明确的参数和受限的范围执行目标操作。  
4) 验证结果并保存输出文件及证据文件。  

## 参考资料  
- `references/sources.md`