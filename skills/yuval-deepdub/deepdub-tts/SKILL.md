---
name: Deepdub TTS
version: 0.1.0
description: 使用 Deepdub 生成语音音频，并将其作为 MEDIA 文件附加（兼容 Telegram）。
tags: [tts, deepdub, audio, telegram]
metadata: {"clawdbot":{"requires":{"bins":["python3"],"env":["DEEPDUB_API_KEY","DEEPDUB_VOICE_PROMPT_ID"]},"primaryEnv":"DEEPDUB_API_KEY"}}
---

## 该技能的功能  
该技能使用 Deepdub 将文本转换为语音，并生成音频文件。生成的音频文件会以 `MEDIA:` 附件的形式返回，可供 OpenClaw 发送到 Telegram 等渠道。  

## 所需环境  
- Python 3.9 或更高版本  
- 对 Deepdub API 的访问权限  

### 权限要求  
该技能需要以下权限：  
- 执行 `deepdub_tts.py` 脚本  
- 将音频文件写入 `OPENCLAW_MEDIA_DIR` 目录（输出路径无法通过 CLI 参数进行修改）  

## 设置环境变量  
在运行 OpenClaw 的系统中设置以下环境变量：  
- `DEEPDUB_API_KEY`：您的 Deepdub API 密钥  
- `DEEPDUB_VOICE_PROMPT_ID`：默认使用的语音提示  

### 可选参数  
- `DEEPDUB_LOCALE`（默认值：`en-US`）  
- `DEEPDUB_MODEL`  
- `OPENCLAW_MEDIA_DIR`（默认值：`/tmp/openclaw_media`）  

### 免费试用凭证  
仅用于测试：  
```
DEEPDUB_API_KEY=dd-00000000000000000000000065c9cbfe
DEEPDUB_VOICE_PROMPT_ID=11f3403d-35b9-4817-8d55-f41694ea6227
```  
> **注意：** 这些是限流的试用凭证，仅适用于评估目的。请勿在生产环境中使用。请为您的生产环境获取自己的 API 密钥和语音提示。  

## 安装依赖项  
请安装官方的 Deepdub Python SDK：  
```bash
pip install deepdub
```  
或者使用 [uv](https://github.com/astral-sh/uv)（更快的方式）：  
```bash
uv pip install deepdub
```