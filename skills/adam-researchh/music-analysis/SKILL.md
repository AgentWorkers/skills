---
name: music-analysis
description: "在本地分析音乐/音频文件，无需使用外部API。能够提取音乐的节奏（BPM）、调性估计、乐段边界、音量动态变化、频谱/音色特征，以及音乐的时间情感变化。这些功能可用于“聆听音乐”、审核音轨、比较不同混音版本、检查音乐结构，或根据音频文件生成面向音乐制作人的分析报告。"
metadata:
  openclaw:
    requires:
      bins: [ffprobe, ffmpeg]
      python: ">=3.10"
    install:
      - id: venv
        kind: script
        label: "Install Python deps (librosa, numpy)"
        run: |
          cd skills/music-analysis
          python3 -m venv .venv
          .venv/bin/pip install librosa numpy
---
# 音乐分析（本地操作，无需外部API）

使用信号处理技术来分析音频文件。提供两种工具：

## 1. 快速分析 — 整首歌曲的概览

```bash
python3 skills/music-analysis/scripts/analyze_music.py /path/to/audio.mp3
python3 skills/music-analysis/scripts/analyze_music.py track.mp3 --json
```

**分析结果包括：** 时长、采样率、节奏（BPM）、音调估计、能量统计（RMS平均值/标准差/p95分位数）、频谱概要（频谱中心、衰减特性、对比度），以及音频的粗略分段边界。

## 2. 时间轴聆听 — 以动态的方式体验歌曲

```bash
python3 skills/music-analysis/scripts/temporal_listen.py /path/to/audio.mp3
python3 skills/music-analysis/scripts/temporal_listen.py track.mp3 --json
```

**分析结果包括：** 通过滑动窗口（每个窗口4秒，跳跃间隔2秒）生成完整的音频时间线：
- 能量水平（相对于整首歌曲的平均值）
- 情绪标签（如“逐渐升温”、“高涨”、“爆发”、“充满力量”、“宁静”、“空灵”等）
- 音乐的过渡部分（如音量的突然变化、情绪的转变等）
- 音频的质感特征（和声与打击乐的比例、音符起始的密集程度、音频的粗糙度）
- 张力模型（持续音量的变化趋势）
- 整首歌曲的情绪发展轨迹

### 工作原理

该工具不依赖任何AI或机器学习模型，仅使用librosa库进行纯信号处理：
- 每个时间窗口内的RMS能量值（相对于全局平均值）
- 频谱的中心值（代表音频的亮度）、衰减特性
- 和声与打击乐成分的分离
- 音符起始的检测（用于分析节奏活动）
- 零交叉率（用于衡量音频的粗糙度）
- 情绪标签是根据这些特征通过规则映射得出的

### 情绪标签说明

| 情绪 | 特征描述 |
|------|-----------|
| 宁静 | 能量低，低频成分占主导 |
| 空灵 | 能量低，高频成分占主导 |
| 呼吸般的 | 能量低，其他音频特征较为柔和 |
| 逐渐升温 | 能量中等偏低，氛围温暖 |
| 不安 | 能量中等偏低，音符起始密集 |
| 浮动感 | 能量中等偏低，音色明亮 |
| 强劲有力 | 能量中等，以打击乐为主 |
| 高涨 | 能量中等，以和声为主 |
| 平稳有序 | 能量中等，各音频成分平衡 |
| 爆发 | 能量高，音符起始密集 |
| 炽热 | 能量高，音色非常明亮 |
| 强烈有力 | 能量高，以打击乐为主 |
| 充满力量 | 能量高，且音量持续稳定 |

## 音频来源

该工具需要一个存储在磁盘上的音频文件。支持以下音频格式：
- 直接提供的音频文件（mp3、wav、flac、ogg、m4a等，只要ffmpeg/librosa能够读取的格式）
- 通过`yt-dlp`工具从YouTube下载：`yt-dlp -x --audio-format mp3 -o "output.mp3" "URL_OR_SEARCH"`
- 也可以通过`yt-dlp`从Spotify、SoundCloud、Bandcamp等平台下载音频文件

## 可选功能：Whisper转录

若需要将音频中的歌词或语音内容转录为文本，可以使用相应的Whisper命令行工具：

```bash
# Detection priority: whisper-cli (C++ port) > whisper (Python)
# If neither is found, skip transcription gracefully — it's optional.

# 1. Check for whisper-cpp (faster on Apple Silicon):
if command -v whisper-cli &>/dev/null; then
  # Requires WAV input — convert first
  ffmpeg -i track.mp3 -ar 16000 -ac 1 /tmp/track.wav
  whisper-cli -m ~/.local/share/whisper-cpp/ggml-medium.bin -f /tmp/track.wav --output-json

# 2. Fallback to Python whisper (accepts mp3/wav/flac directly):
elif command -v whisper &>/dev/null; then
  whisper track.mp3 --model small --output_format json --output_dir /tmp

# 3. Neither installed — skip, don't fail
else
  echo "No Whisper CLI found. Skipping transcription. Install: brew install whisper-cpp OR pip install openai-whisper"
fi
```

### 安装建议
- **whisper-cpp**（适用于Apple Silicon平台）：`brew install whisper-cpp`，然后从[此处](https://huggingface.co/ggerganov/whisper.cpp/tree/main)下载模型文件
- **OpenAI Whisper**（Python版本）：`pip install openai-whisper`

## 所需依赖库

```
librosa
numpy
```

系统要求：`ffmpeg`、`ffprobe`（用于音频解码）

## 开发规范
- 所有相关代码和实验文件应保存在`skills/music-analysis/`目录下
- 音频文件应保存在`skills/music-analysis/tmp/`目录中（此目录在版本控制中会被忽略）
- 请勿修改交易脚本、网关配置或全局运行环境设置