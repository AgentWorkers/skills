---
name: alicloud-ai-audio-asr-realtime
description: >
  **使用场景：**  
  当需要使用阿里云 Model Studio 的 Qwen ASR 实时语音识别模型来实现低延迟的实时语音识别功能时，该方案非常适用。具体应用场景包括：流式麦克风输入、实时字幕生成，或双向语音交互系统（如语音助手）。
version: 1.0.0
---
**类别：提供者**  
# Model Studio Qwen ASR 实时服务  

## 验证  

```bash
mkdir -p output/alicloud-ai-audio-asr-realtime
python -m py_compile skills/ai/audio/alicloud-ai-audio-asr-realtime/scripts/prepare_realtime_asr_request.py && echo "py_compile_ok" > output/alicloud-ai-audio-asr-realtime/validate.txt
```  

**通过标准**：命令执行成功（返回代码为 0），并且文件 `output/alicloud-ai-audio-asr-realtime/validate.txt` 被生成。  

## 输出与证据**  
- 将会话数据及响应样本保存在 `output/alicloud-ai-audio-asr-realtime/` 目录下。  

## 关键模型名称**  
使用以下模型名称之一：  
- `qwen3-asr-flash-realtime`  
- `qwen3-asr-flash-realtime-2026-02-10`  

## 使用场景**  
- 实时字幕生成  
- 语音代理的双向通信  
- 浏览器或终端客户端中的语音转文本功能  

## 先决条件**  
- 在您的环境中设置 `DASHSCOPE_API_KEY`，或将其添加到 `~/.alibabacloud/credentials` 文件中。  
- 实时会话通常需要在客户端端实现 WebSocket 或流式会话处理功能。  

## 标准化接口（asr.realtime）  

### 请求**  
- `model`（字符串，可选）：默认值为 `qwen3-asr-flash-realtime`  
- `language_hints`（字符串数组，可选）  
- `format`（字符串，可选）：例如 `pcm`、`wav`  
- `sample_rate`（整数，可选）：例如 `16000`  
- `chunk_ms`（整数，可选）：帧大小（以毫秒为单位）  

### 响应**  
- `text`（字符串）：识别出的文本片段  
- `is_final`（布尔值）：表示是否为最终结果  
- `usage`（对象，可选）：使用情况相关信息  

## 快速入门**  
生成一个请求模板：  
```bash
python skills/ai/audio/alicloud-ai-audio-asr-realtime/scripts/prepare_realtime_asr_request.py \
  --output output/alicloud-ai-audio-asr-realtime/request.json
```  

## 运维指南**  
- 除非客户端需要其他格式，否则建议使用 16kHz 单声道 PCM 格式。  
- 保持数据块的大小适中，以便能够快速获取部分识别结果。  
- 如果您只有已录制的音频文件，可以使用 `skills/ai/audio/alicloud-ai-audio-asr/` 服务。  

## 参考资料**  
- `references/sources.md`