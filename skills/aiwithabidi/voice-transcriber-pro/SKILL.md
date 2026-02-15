---
name: voice-transcriber
description: Voice note transcription and archival for OpenClaw agents. Powered by Deepgram Nova-3. Transcribes audio messages, saves both audio files and text transcripts. Perfect for voice-first AI workflows, founder journaling, and meeting notes.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: curl, jq, Deepgram API key
metadata: {"openclaw": {"emoji": "\ud83c\udf99\ufe0f", "requires": {"env": ["DEEPGRAM_API_KEY"], "bins": ["curl", "jq"]}, "primaryEnv": "DEEPGRAM_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 语音转录器 🎙️  
通过 Whisper 实现音频转录，并支持语音笔记的记录功能。  

## 使用场景  
- 转录语音消息或音频文件  
- 保存带有完整文字记录的语音笔记  
- 将任何音频格式的语音内容转换为文本  

## 使用方法  

### 转录音频  
```bash
bash {baseDir}/scripts/transcribe.sh /path/to/audio.ogg
bash {baseDir}/scripts/transcribe.sh /path/to/audio.ogg --out /path/to/output.txt
```  

### 保存带有文字记录的语音笔记  
```bash
python3 {baseDir}/scripts/save_voice_note.py /path/to/audio.ogg "Optional context"
```  

## 支持的音频格式  
OGG、MP3、WAV、M4A、FLAC、WEBM  

## 致谢  
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
该工具是 OpenClaw 代理软件 **AgxntSix Skill Suite** 的组成部分。  

📅 **需要帮助为您的企业设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)