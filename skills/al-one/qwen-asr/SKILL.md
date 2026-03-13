---
name: qwen-asr
description: 使用 Qwen ASR（千问STT）来转录音频文件。当用户发送语音消息并希望将其转换为文本时，可以使用此功能。
homepage: https://github.com/aahl/qwen-asr2api
metadata:
  {
    "openclaw":
      {
        "emoji": "🎤",
        "requires": { "bins": ["uv"] },
        "install":
          [
            {"id": "uv-brew", "kind": "brew", "formula": "uv", "bins": ["uv"], "label": "Install uv (brew)"},
            {"id": "uv-pip", "kind": "pip", "formula": "uv", "bins": ["uv"], "label": "Install uv (pip)"},
            {"id": "pip-aiohttp", "kind": "pip", "formula": "aiohttp", "label": "Install aiohttp (pip)"},
            {"id": "pip-argparse", "kind": "pip", "formula": "argparse", "label": "Install argparse (pip)"},
            {"id": "pip-gradio", "kind": "pip", "formula": "gradio_client", "label": "Install gradio (pip)"},
          ],
      },
  }
---
# Qwen ASR  
使用 Qwen ASR 将音频文件（格式为 wav/mp3/ogg 等）转录为文本。无需进行任何配置或提供 API 密钥。  

## 使用方法  
```shell
uv run scripts/main.py -f audio.wav
cat audio.wav | uv run scripts/main.py > transcript.txt
```  

## 关于 Qwen ASR  
Qwen ASR 是一个免费且开源的语音转文本工具。  
它基于从互联网上收集的大量音频数据集进行训练，支持多种语言。  
该功能基于 Qwen ASR 的演示服务（qwen-qwen3-asr-demo.ms.show）实现。