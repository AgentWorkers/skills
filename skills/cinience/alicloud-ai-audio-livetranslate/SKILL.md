---
name: alicloud-ai-audio-livetranslate
description: >
  **使用场景：**  
  当需要使用 Alibaba Cloud Model Studio 的 Qwen LiveTranslate 模型进行实时语音翻译时，该功能适用于双语会议、实时口译以及语音转语音或语音转文本的翻译场景。
version: 1.0.0
---
**类别：提供商**  
# Model Studio Qwen LiveTranslate  

## 验证  
```bash
mkdir -p output/alicloud-ai-audio-livetranslate
python -m py_compile skills/ai/audio/alicloud-ai-audio-livetranslate/scripts/prepare_livetranslate_request.py && echo "py_compile_ok" > output/alicloud-ai-audio-livetranslate/validate.txt
```  

**通过标准：**  
命令执行成功（返回代码为0），并且文件 `output/alicloud-ai-audio-livetranslate/validate.txt` 被生成。  

## 输出与证据  
- 将翻译会话的数据及响应摘要保存在目录 `output/alicloud-ai-audio-livetranslate/` 下。  

## 关键模型名称  
使用以下模型名称之一：  
- `qwen3-livetranslate-flash`  
- `qwen3-livetranslate-flash-realtime`  

## 常见用途  
- 中英会议口译  
- 实时生成其他语言的字幕  
- 电话客服人员使用翻译后的字幕辅助沟通  

## 标准化接口（audio.livetranslate）  
### 请求参数  
- `model`（字符串，可选）：默认值为 `qwen3-livetranslate-flash`  
- `source_language`（字符串，必填）  
- `target_language`（字符串，必填）  
- `audio_format`（字符串，可选）：例如 `pcm`  
- `sample_rate`（整数，可选）：例如 `16000`  

### 响应参数  
- `translated_text`（字符串）  
- `source_text`（字符串，可选）  
- `audio_url` 或 `audio_chunk`（可选，具体取决于所使用的模型）  

## 快速入门  
```bash
python skills/ai/audio/alicloud-ai-audio-livetranslate/scripts/prepare_livetranslate_request.py \
  --source-language zh \
  --target-language en \
  --output output/alicloud-ai-audio-livetranslate/request.json
```  

## 注意事项  
- 对于连续的流媒体会议，建议使用实时翻译模型（`qwen3-livetranslate-flash-realtime`）。  
- 对于集成要求较低、客户端实现较为简单的场景，建议使用非实时翻译模型（`qwen3-livetranslate-flash`）。  

## 参考资料  
- `references/sources.md`