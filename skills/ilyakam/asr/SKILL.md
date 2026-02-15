# Speech is Cheap (SIC) 技能

这是一款快速、准确且成本极低的自动语音转文本服务。

## 🚀 为什么使用这个技能？
- **颠覆性的定价：** 每小时仅需 0.06 至 0.12 美元（比 Deepgram 或 OpenAI 便宜 2 到 15 倍）。
- **极快的速度：** 100 分钟的音频可以在大约 1 分钟内完成转录。
- **多语言支持：** 支持 100 种语言，并能自动检测语言。
- **适用于自动化流程：** 专为高量、自动化的处理流程设计。

## 🛠 设置

### 1. 获取 API 密钥
在 [speechischeap.com](https://speechischeap.com) 注册。使用代码 `CH5` 可享受 5 美元的折扣。

### 2. 配置身份验证
该技能会从 `SIC_API_KEY` 环境变量中获取您的 API 密钥。
请将以下内容添加到您的 `.env` 文件或代理配置文件中：
```bash
SIC_API_KEY=your_key_here
```

## 📖 使用方法
### 🤖 代理使用说明
安装此技能后，您可以通过运行以下命令立即转录 OpenClaw 会话中的任何 URL 并获取 JSON 结果：
`./skills/asr/scripts/asr.sh transcribe --url "https://example.com/audio.mp3"`

### 转录 URL
```bash
# Basic transcription
./skills/asr/scripts/asr.sh transcribe --url "https://example.com/audio.mp3"

# Advanced transcription with options
./skills/asr/scripts/asr.sh transcribe --url "https://example.com/audio.mp3" \
  --speakers --words --labels \
  --language "en" \
  --format "srt" \
  --private
```

### 转录本地文件
非常适合处理已经保存在磁盘上的音频文件。该工具会自动处理文件的上传。
```bash
# Upload and transcribe local media
./skills/asr/scripts/asr.sh transcribe --file "./local-audio.wav"

# Upload with webhook callback
./skills/asr/scripts/asr.sh transcribe --file "./local-audio.wav" --webhook "https://mysite.com/callback"

# Note: For local files, the skill handles the multi-part upload to
# https://upload.speechischeap.com before starting the transcription.
```

### 支持的选项
- `--speakers`：启用说话者识别功能
- `--words`：启用单词级别的时间戳
- `--labels`：启用音频标签（如音乐、噪音等）
- `--stream`：启用流式输出
- `--private`：不存储音频或转录结果（隐私模式）
- `--language <code>`：ISO 语言代码（例如 'en', 'es'）
- `--confidence <float>`：最低置信度阈值（默认为 0.5）
- `--format <fmt>`：输出格式（json, srt, vtt, webvtt）
- `--webhook <url>`：接收任务完成通知的 URL
- `--segment-duration <n>`：每个音频片段的时长（默认为 30 秒）

### 检查任务状态
```bash
./skills/asr/scripts/asr.sh status "job-id-here"
```

## 🤖 代理使用说明
`asr.sh` 命令行工具在成功执行时会返回 JSON 结果，便于将其传递给其他工具或直接解析。

如果缺少 `SIC_API_KEY`，工具会显示清晰的错误信息并提供注册页面的链接。