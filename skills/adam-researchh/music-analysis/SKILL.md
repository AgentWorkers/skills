---
name: music-analysis
description: "在本地分析音乐/音频文件，无需使用外部API。可以提取音乐的节奏（BPM）、调性估计、段落边界、音量动态、频谱/音色特征，以及音乐的时间情感变化。适用于需要“聆听音乐”、审核音轨、比较混音效果、检查音乐结构，或从音频文件中生成面向制作人的分析报告的场景。"
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

**分析结果包括：** 时长、采样率、节奏（BPM）、音调估计、能量统计（RMS平均值/标准差/p95值）、频谱概要（频谱中心、频谱衰减特性、对比度），以及音频的粗略分段边界。

## 2. 时空聆听 — 以“旅程”的方式体验音频

```bash
python3 skills/music-analysis/scripts/temporal_listen.py /path/to/audio.mp3
python3 skills/music-analysis/scripts/temporal_listen.py track.mp3 --json
```

**分析结果包括：** 通过滑动窗口（每个窗口4秒，跳跃间隔2秒）生成完整的音频时间线：
- 能量水平（相对于整首歌曲的平均值）
- 情绪标签（如“逐渐升温”、“高涨”、“爆发”、“充满力量”、“宁静”、“空灵”等）
- 音频的过渡效果（如突然的节奏变化、音色的转变等）
- 音频的纹理特征（和声与打击乐的比例、声音的起始密度、粗糙度）
- 音乐的紧张度变化模型
- 音乐的叙事结构（如上升、下降、平稳等阶段）
- 最高潮点、最安静的时刻，以及整体情绪变化概览

### 工作原理

该工具完全基于信号处理技术，未使用任何人工智能/机器学习模型，而是通过 `librosa` 库来实现以下功能：
- 计算每个时间窗口内的 **RMS能量值**（相对于全局平均值）
- 分析 **频谱中心**（代表音频的亮度特征）、频谱衰减特性以及音频的平坦度
- 实现 **和声与打击乐成分的分离**
- 检测声音的 **起始时刻**（即节奏活动的开始）
- 计算 **零交叉率**（反映音频的粗糙度）
- 情绪标签是根据这些音频特征通过规则映射得出的

### 情绪分类词汇表

| 情绪 | 特征描述 |
|------|-----------|
| 宁静（submerged） | 能量低，低频成分占主导 |
| 空灵（ethereal） | 能量低，高比例的和声成分 |
| 呼吸般的（breathing） | 能量低，其他音频特征不明显 |
| 逐渐升温（simmering） | 能量中等偏低，温暖的感觉 |
| 不安（restless） | 能量中等偏低，声音起始密度高 |
| 浮动感（floating） | 能量中等偏低，音色明亮 |
| 强劲有力（driving） | 能量中等，以打击乐为主 |
| 高涨（soaring） | 能量中等，以和声为主 |
| 平稳（locked in） | 能量中等，各音频成分平衡 |
| 爆发（erupting） | 能量高，声音起始密度高 |
| 炽热（searing） | 能量高，音色非常明亮 |
| 强烈有力（pounding） | 能量高，以打击乐为主 |
| 充满力量（full force） | 能量高，持续性强 |

## 音频来源

该工具需要本地音频文件。支持以下音频格式：
- 直接文件（mp3、wav、flac、ogg、m4a 等，任何 `ffmpeg/librosa` 能识别的格式）
- 通过 `yt-dlp` 从 YouTube 下载音频：`yt-dlp -x --audio-format mp3 -o "output.mp3" "URL_OR_SEARCH"`
- 也可以从 Spotify、SoundCloud、Bandcamp 等平台下载音频

## 可选功能：歌词转录

如果安装了 `Whisper` CLI 工具，可以单独运行该工具来提取音频文件的歌词：

```bash
whisper track.mp3 --model small --output_format json --output_dir /tmp
```

## 所需依赖库

```
librosa
numpy
```

系统依赖库：`ffmpeg`、`ffprobe`（用于音频解码）

## 开发和使用规范

- 所有实验代码请保存在 `skills/music-analysis/` 目录下
- 音频文件应保存在 `skills/music-analysis/tmp/` 目录中（Git 会忽略该目录）
- 请勿修改交易脚本、网关配置或全局运行环境设置