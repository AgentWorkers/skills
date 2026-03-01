---
name: audio-speaker-tools
description: "**扬声器分离、语音比对及音频处理工具**  
适用于处理多扬声器音频数据、语音克隆或扬声器身份验证等任务，具体功能包括：  
(1) 通过 Demucs 和 pyannote 工具从音频文件中分离出不同扬声器的语音信号；  
(2) 使用 Resemblyzer 对语音样本进行比对，以验证扬声器身份或评估语音克隆的质量；  
(3) 提取音频片段；  
(4) 为 ElevenLabs 的语音克隆服务准备所需样本；  
(5) 验证语音分离结果的准确性。"
---
# 音频处理工具

这些工具用于分离不同说话者的声音、进行语音比对以及使用 Demucs、pyannote 和 Resemblyzer 进行音频处理。

## 概述

本技能提供了三种主要的工作流程：

1. **说话者分离**：从多说话者的录音中提取每个说话者的音频。
2. **语音比对**：测量两个音频文件中说话者的相似度。
3. **音频处理**：对音频进行分割和语音提取。

## 先决条件

### 设置虚拟环境

运行一次命令以创建虚拟环境（venv）并安装所需依赖项：

```bash
bash scripts/setup_venv.sh
```

默认的虚拟环境位置：`./.venv`

**要求：**
- Python 3.9 或更高版本
- ffmpeg（通过 `brew install ffmpeg` 安装）
- HuggingFace 令牌（设置为环境变量 `HF_TOKEN`）

## 脚本

### 1. 说话者分离：`diarize_and_slice_mps.py`

从多说话者的音频中分离出各个说话者的声音：

```bash
# Basic usage
HF_TOKEN=<your-hf-token> \
  /path/to/venv/bin/python scripts/diarize_and_slice_mps.py \
  --input audio.mp3 \
  --outdir /path/to/output \
  --prefix MyShow

# With speaker constraints
HF_TOKEN=$TOKEN python scripts/diarize_and_slice_mps.py \
  --input audio.mp3 \
  --outdir ./out \
  --min-speakers 2 \
  --max-speakers 5 \
  --pad-ms 100
```

**处理流程：**
1. 将输入音频转换为 16kHz 单声道 WAV 格式。
2. 运行 Demucs 进行人声与背景的分离（可选，以获得更清晰的音频）。
3. 使用 pyannote 进行人声分割（通过 MPS 加速）。
4. 提取每个说话者的音频文件。

**输出结果：**
- `<prefix>_speaker1.wav`、`<prefix>_speaker2.wav` 等（每个检测到的说话者对应一个文件）
- `diarization.rttm`（带有时间戳的说话者音频片段）
- `segments.jsonl`（音频片段的元数据）
- `meta.json`（处理流程信息和说话者索引）

**重要提示：**
- **务必通过环境变量 `HF_TOKEN` 传递 HuggingFace 令牌**，切勿以命令行参数传递。
- **优先使用 Metal GPU 加速，如果 GPU 不可用则使用 CPU**。
- 默认输出目录：`./separated/`

### 2. 语音比对：`compare_voices.py`

使用 Resemblyzer 测量两个语音样本的相似度：

```bash
# Basic comparison
python scripts/compare_voices.py \
  --audio1 sample1.wav \
  --audio2 sample2.wav

# JSON output
python scripts/compare_voices.py \
  --audio1 reference.wav \
  --audio2 clone.wav \
  --threshold 0.85 \
  --json

# Exit code = 0 if pass, 1 if fail
```

**相似度评分标准：**
- `< 0.75` = 不同的说话者
- `0.75-0.84` = 很可能是同一说话者
- `0.85+` = 非常匹配（适用于语音克隆验证）

**使用场景：**
- 语音克隆质量评估（比较克隆语音与原始语音）
- 说话者身份验证
- 确认分离出的说话者是否确实不同

**参考文档：**`references/scoring-guide.md` 以获取详细的评分解释

### 3. 音频剪辑

直接使用 `ffmpeg` 进行音频片段提取：

```bash
# Extract 10-second segment starting at 5 seconds
ffmpeg -i input.mp3 -ss 5 -t 10 -c copy output.mp3

# Extract vocals only with Demucs (before diarization)
demucs --two-stems vocals --out ./separated input.mp3
```

## 工作流程

### 工作流程 1：提取用于克隆的清晰语音样本

**目标：** 获取适用于 ElevenLabs 语音克隆的清晰、单声道语音样本

**参考文档：**`references/elevenlabs-cloning.md` 以获取最佳实践

### 工作流程 2：验证语音克隆质量

**目标：** 测量克隆语音与原始语音的匹配程度

**参考文档：**`references/scoring-guide.md` 以解决评分较低的问题

### 工作流程 3：多说话者对话分析

**目标：** 分离并识别对话中的说话者

```bash
# 1. Run diarization
HF_TOKEN=$TOKEN python scripts/diarize_and_slice_mps.py \
  --input meeting.mp3 --outdir ./out --prefix Meeting

# 2. Check detected speakers (meta.json)
cat out/meta.json

# 3. Compare speaker pairs to confirm separation
python scripts/compare_voices.py \
  --audio1 out/Meeting_speaker1.wav \
  --audio2 out/Meeting_speaker2.wav

# Expected: < 0.75 if separation worked correctly
```

## 技术说明

### 设备加速
- **pyannote 语音分割：** 默认使用 Metal GPU 加速，CPU 作为备用方案。
- **Resemblyzer：** 仅支持 CPU 加速（不支持 GPU）。
- **Demucs：** 在支持的情况下默认使用 Metal GPU 加速。

**强制使用 CPU 加速：** 使用 `--device cpu` 参数。

### 音频格式
- **输入格式：** 支持 ffmpeg 的所有格式（wav、mp3、flac、m4a 等）。
- **处理过程：** 内部转换为 16kHz 单声道 WAV 格式。
- **输出格式：** 保持原始音频的 44.1kHz 立体声格式。

### HuggingFace 令牌
- **必需使用：** 用于 pyannote 的语音分割功能。
- **获取方式：** 从 HuggingFace 的 `pyannote/speaker-diarization-3.1` 仓库中获取令牌。
- **存储方式：** 可以使用任何安全的密钥管理工具。
- **使用方法：** 必须通过环境变量 `HF_TOKEN` 传递，切勿以命令行参数传递。

### 样本质量建议
- **样本长度越短越好：** 5-30 秒的清晰样本通常比 60 秒以上的样本得分更高。
- **清除背景噪音：** 使用 Demucs 的 `--two-stems vocals` 选项去除背景噪音。
- **确保是单个说话者的声音：** 避免混合了多个说话者的声音。
- **高质量录音：** 使用专业录音麦克风比手机麦克风能获得更准确的语音对比结果。

## 参考文档

- **elevenlabs-cloning.md**：ElevenLabs 语音克隆的最佳实践（模型设置、样本选择、验证配置）。
- **scoring-guide.md**：如何解读 Resemblyzer 的相似度评分（评分标准、使用场景、故障排除方法）。

## 常见问题

### “缺少 HuggingFace 令牌”的错误
- 在运行脚本前先导出令牌：`export HF_TOKEN=<your-token>`
- 或者在脚本中直接传递令牌：`HF_TOKEN=<your-token> python script.py ...`

### 同一说话者的语音比对得分较低
- 尝试使用更短、更清晰的样本（5-30 秒）。
- 使用 Demucs 进行人声分离：`demucs --two-stems vocals input.mp3`。
- 确保录音质量一致（使用相同的麦克风和录制环境）。
- 参考 `references/scoring-guide.md` 中的故障排除方法。

### 语音分割未检测到所有说话者
- 调整 `--min-speakers` 和 `--max-speakers` 参数。
- 检查音频质量（语音清晰、无重叠）。
- 尝试使用更长的音频片段（30 秒以上）以获得更准确的说话者识别结果。

### MPS/Metal 加速无法使用
- 确保使用的 PyTorch 版本支持 MPS 加速：`python -c "import torch; print(torch.backends.mps.is_available())`。
- 如果无法使用 GPU 加速，切换到 CPU：`--device cpu`。
- 重新运行 `setup_venv.sh` 以重新安装 PyTorch。