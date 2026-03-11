---
name: alicloud-ai-audio-asr
description: 使用阿里云模型工作室（Alibaba Cloud Model Studio）的Qwen ASR模型（`qwen3-asr-flash`、`qwen-audio-asr`、`qwen3-asr-flash-filetrans`）来转录非实时语音。这些模型适用于将录制的音频文件转换为文本、生成带有时间戳的文本记录，以及记录与DashScope/OpenAI兼容的ASR请求和响应字段。
version: 1.0.0
---
**类别：提供者**  
# Model Studio Qwen ASR（非实时）  

## 验证  
```bash
mkdir -p output/alicloud-ai-audio-asr
python -m py_compile skills/ai/audio/alicloud-ai-audio-asr/scripts/transcribe_audio.py && echo "py_compile_ok" > output/alicloud-ai-audio-asr/validate.txt
```  

**通过标准：**  
命令执行成功（返回代码0），并且生成了 `output/alicloud-ai-audio-asr/validate.txt` 文件。  

## 输出与证据  
- 将转录结果和API响应保存在 `output/alicloud-ai-audio-asr/` 目录下。  
- 每次运行后保留一条命令日志或一个样本响应。  

**使用说明：**  
使用 Qwen ASR 对录制的音频进行转录（非实时处理），支持短音频同步请求和长音频异步任务。  

## 关键模型名称  
请使用以下模型名称之一：  
- `qwen3-asr-flash`  
- `qwen-audio-asr`  
- `qwen3-asr-flash-filetrans`  

**选择指南：**  
- 对于短音频或普通音频转录（同步请求），使用 `qwen3-asr-flash` 或 `qwen-audio-asr`。  
- 对于长文件转录（异步任务），使用 `qwen3-asr-flash-filetrans`。  

## 先决条件**  
- 安装SDK相关依赖项（该脚本仅使用Python标准库）。  
```bash
python3 -m venv .venv
. .venv/bin/activate
```  

- 将 `DASHSCOPE_API_KEY` 设置在环境变量中，或将其添加到 `~/.alibabacloud/credentials` 文件中。  

## 标准化接口（`asr.transcribe`）  
### 请求参数  
- `audio`（字符串，必填）：音频文件的公共URL或本地文件路径。  
- `model`（字符串，可选）：默认值为 `qwen3-asr-flash`。  
- `language_hints`（字符串数组，可选）：例如 `zh`、`en`。  
- `sample_rate`（数字，可选）  
- `vocabulary_id`（字符串，可选）  
- `disfluency_removal_enabled`（布尔值，可选）  
- `timestamp_granularities`（字符串数组，可选）：例如 `sentence`。  
- `async`（布尔值，可选）：同步模型默认为 `false`；`qwen3-asr-flash-filetrans` 为 `true`。  

### 响应参数  
- `text`（字符串）：标准化的转录文本。  
- `task_id`（字符串，可选）：异步请求时返回的任务ID。  
- `status`（字符串）：操作状态（例如 `SUCCEEDED`）。  
- `raw`（对象）：原始的API响应数据。  

## 快速入门（官方HTTP API）  
- **同步转录（兼容OpenAI协议）：**  
```bash
curl -sS --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "qwen3-asr-flash",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
            }
          }
        ]
      }
    ],
    "stream": false,
    "asr_options": {
      "enable_itn": false
    }
  }'
```  
- **异步长文件转录（DashScope协议）：**  
```bash
curl -sS --location 'https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'X-DashScope-Async: enable' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "qwen3-asr-flash-filetrans",
    "input": {
      "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
    }
  }'
```  
- **查询任务结果：**  
```bash
curl -sS --location "https://dashscope.aliyuncs.com/api/v1/tasks/<task_id>" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```  

## 本地辅助脚本  
使用提供的脚本进行URL或本地文件的输入处理，并支持可选的异步结果查询：  
```bash
python skills/ai/audio/alicloud-ai-audio-asr/scripts/transcribe_audio.py \
  --audio "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3" \
  --model qwen3-asr-flash \
  --language-hints zh,en \
  --print-response
```  

**长文件模式：**  
```bash
python skills/ai/audio/alicloud-ai-audio-asr/scripts/transcribe_audio.py \
  --audio "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3" \
  --model qwen3-asr-flash-filetrans \
  --async \
  --wait
```  

## 操作指南：**  
- 如果无法使用公共URL，请使用 `input_audio.data`（数据URI）来指定本地文件路径。  
- 尽量减少 `language_hints` 的使用，以避免识别歧义。  
- 对于异步任务，建议使用5-20秒的轮询间隔，并设置最大重试次数。  
- 将标准化后的转录结果保存在 `output/alicloud-ai-audio-asr/transcripts/` 目录下。  

## 输出路径  
- 默认输出路径：`output/alicloud-ai-audio-asr/transcripts/`  
- 可通过 `OUTPUT_DIR` 变量覆盖默认路径。  

**工作流程：**  
1. 确认用户意图、所在地区、相关标识信息，以及操作是只读还是可修改的。  
2. 首先执行一个最小的只读查询以验证连接性和权限。  
3. 使用明确的参数和受限的范围执行目标操作。  
4. 验证结果并保存输出文件及相关证据。  

**参考文档：**  
- `references/api_reference.md`  
- `references/sources.md`  
- 实时音频合成功能请参考 `skills/ai/audio/alicloud-ai-audio-tts-realtime/`。