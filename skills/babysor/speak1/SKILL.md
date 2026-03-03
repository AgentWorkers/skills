---
name: speak
description: 使用 Kokoro 的本地 TTS（文本转语音）功能。当用户需要将文本转换为音频、大声朗读或生成语音时，可以使用该功能。
---
# 语音转换

使用 [Kokoro TTS](https://github.com/nazdridoy/kokoro-tts) 在本地将文本转换为语音。

## 快速入门

```bash
# Text string → audio file
kokoro-tts <(echo "Hello world") hello.wav --voice af_sarah

# Text file → audio
kokoro-tts article.txt out.wav --voice af_heart

# Chinese
kokoro-tts story.txt out.wav --voice zf_xiaoni --lang cmn

# EPUB / PDF → chapter audio files
kokoro-tts book.epub --split-output ./chapters/ --format mp3 --voice bf_emma

# Voice blending (60-40 mix)
kokoro-tts input.txt out.wav --voice "af_sarah:60,am_adam:40"

# Adjust speed
kokoro-tts input.txt out.wav --voice am_adam --speed 1.2

# Stream playback (no file saved)
kokoro-tts input.txt --stream --voice af_nova
```

## 安装

```bash
uv tool install kokoro-tts
```

模型文件（`kokoro-v1.0.onnx` 和 `voices-v1.0.bin`）必须位于工作目录中。只需下载一次：

```bash
wget https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/kokoro-v1.0.onnx
wget https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/voices-v1.0.bin
```

## 语音列表

| 地区 | 女性 | 男性 |
|--------|--------|------|
| 🇺🇸 en-us | af_alloy af_heart af_sarah af_nova ... | am_adam am_echo am_michael ... |
| 🇬🇧 en-gb | bf_alice bf_emma bf_lily ... | bm_daniel bm_george ... |
| 🇨🇳 cmn | zf_xiaoni zf_xiaoxiao zf_xiaoyi ... | zm_yunxi zm_yunyang ... |
| 🇯🇵 ja | jf_alpha jf_nezumi ... | jm_kumo |
| 🇫🇷 fr-fr | ff_siwis | — |
| 🇮🇹 it | if_sara | im_nicola |

有关完整的语音列表、选项和输入格式详情，请参阅 [reference.md](reference.md)。