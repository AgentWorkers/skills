# 语音转文本（STT）技能

使用 OpenAI Whisper 将音频文件转换为文本，该工具针对巴西葡萄牙语进行了优化。

## 使用场景

- 将语音消息或音频文件转换为文本
- 转录来自 WhatsApp、Telegram 等平台的音频
- 支持处理以下音频格式：OGG、WAV、MP3、M4A、FLAC、AAC、OPUS
- 生成带有时间戳的转录结果
- 处理巴西葡萄牙语内容

## 工具

- `stt_transcribe`：转录指定的音频文件
- `stt_watch`：持续监控传入的音频文件
- `stt_batch`：一次性处理所有待处理的音频文件

## 设置步骤

1. **安装依赖项：**
```bash
pip install -r requirements.txt
```

2. 安装 FFmpeg（Whisper 需要此工具）：
  - Windows：运行 `install_ffmpeg.cmd` 或使用 Winget 安装 “Gyan.FFmpeg”
  - macOS：使用 `brew install ffmpeg`
  - Linux：使用 `sudo apt install ffmpeg`
3. 创建音频文件输入目录：
```bash
mkdir -p ../../../media/inbound
```

## 使用方法

### 转录指定音频文件
```bash
python stt_processor.py --file /path/to/your/audio.ogg
```

### 一次性转录所有待处理的音频文件
```bash
python stt_processor.py
```