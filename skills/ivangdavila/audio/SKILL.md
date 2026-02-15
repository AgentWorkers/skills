---
name: Audio
slug: audio
version: 1.0.1
description: 处理、增强并转换音频文件，包括去除噪音、进行音量标准化、格式转换、文字转录以及实现播客相关工作流程。
changelog: Declare required binaries (ffmpeg, ffprobe), add requirements section with optional deps, add explicit scope
metadata: {"clawdbot":{"emoji":"🔊","requires":{"bins":["ffmpeg","ffprobe"]},"os":["linux","darwin","win32"]}}
---
## 要求

**必备工具：**
- `ffmpeg` / `ffprobe` — 核心音频处理工具

**可选工具（用于高级功能）：**
- `sox` — 用于进一步降噪
- `whisper` — 用于文本转录（或使用相关 API）
- `demucs` — 用于分离音频轨道（人声、鼓声、贝斯等）

## 快速参考

| 情况 | 所需操作 |
|-----------|------|
| 根据任务使用 FFmpeg 命令 | 查看 `commands.md` |
| 不同平台的音量标准 | 查看 `loudness.md` |
| 播客制作流程 | 查看 `podcast.md` |
| 文本转录流程 | 查看 `transcription.md` |

## 核心功能

| 功能 | 实现方法 |
|------|--------|
| 转换音频格式 | 使用 FFmpeg 的 `-acodec` 参数 |
| 降噪 | 使用 FFmpeg 的滤镜或 SoX 工具 |
| 标准化音量 | 使用 `ffmpeg-normalize` 命令或 `-af loudnorm` 参数 |
| 文本转录 | 使用 `whisper` 工具将音频转换为文本、SRT 或 VTT 格式 |
| 分离音频轨道 | 使用 `demucs` 工具分离人声、鼓声、贝斯等音轨 |

## 执行流程

1. **明确目标**：需要转换成什么格式？音量应设置为多少？在哪个平台上使用？
2. **分析音频文件**：使用 `ffprobe` 查看音频文件的编码格式、采样率、声道数和时长等信息。
3. **进行处理**：使用 FFmpeg 或 SoX 对音频文件进行转换或处理。
4. **验证结果**：检查处理后的音频文件是否能正常播放，是否符合要求，音质是否合格。
5. **交付结果**：将处理后的音频文件提供给用户。

## 常见请求与对应操作

| 用户需求 | 代理操作 |
|-----------|------------|
| “将音频转换为 MP3 格式” | 使用 `-acodec libmp3lame -q:a 2` 命令 |
| “去除背景噪音” | 应用高通滤波器或专用降噪工具 |
| “为播客调整音量” | 使用 `-af loudnorm=I=-16:TP=-1.5:LRA=11` 命令 |
| “将音频转录为文本” | 使用 `whisper` 将音频转换为 SRT/VTT/TXT 格式 |
| “从视频中提取音频” | 使用 `-vn -acodec copy` 命令提取音频 |
| “减小文件大小” | 降低比特率（例如：`-b:a 128k` 或 `-b:a 96k`） |
| “加快音频播放速度” | 使用 `-af atempo=1.5` 命令 |

## 音频格式简介

| 格式 | 适用场景 | 音质 |
|--------|----------|---------|
| WAV | 音频母带文件、编辑用途 | 无损压缩格式 |
| FLAC | 音频存档、音频爱好者使用 | 无损压缩格式 |
| MP3 | 通用分享格式 | 有损压缩格式，比特率通常为 128-320 kbps |
| AAC/M4A | Apple 设备、播客使用 | 有损压缩格式，压缩效率高 |
| OGG/Opus | WhatsApp、Discord 等平台使用 | 有损压缩格式，压缩效率极高 |

## 音质默认设置

- **播客音量标准：** -16 LUFS（Spotify），-19 LUFS（Apple）
- **音乐音量标准：** -14 LUFS（Spotify），-16 LUFS（Apple Music）
- **MP3 音质设置：** 可变比特率（VBR）`-q:a 2`（约 190 kbps）或固定比特率（CBR）`-b:a 192k`
- **采样率：** 音乐文件通常为 44.1kHz，视频同步时使用 48kHz

## 功能范围

- 该工具仅处理用户提供的音频文件。
- 仅根据用户请求执行 FFmpeg 命令。
- 未经用户许可，不会访问任何云服务。
- 不会永久存储用户的音频文件（用户自行管理音频文件）。