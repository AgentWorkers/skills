---
name: zhipu-asr
description: 使用 Zhipu AI（BigModel）的 GLM-ASR 模型实现自动语音识别（ASR）功能。当您需要将音频文件转录为文本时，可以使用该工具。该服务支持中文音频的转录，并提供上下文提示、自定义关键词以及多种音频格式的支持。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["jq"], "env": ["ZHIPU_API_KEY"] },
      },
  }
---
# Zhipu AI 自动语音识别 (ASR)

使用 Zhipu AI 的 GLM-ASR 模型将中文音频文件转录为文本。

## 设置

**1. 获取您的 API 密钥：**
从 [Zhipu AI 控制台](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) 获取密钥。

**2. 在您的环境中设置密钥：**
```bash
export ZHIPU_API_KEY="your-key-here"
```

## 支持的音频格式

- **WAV** - 推荐格式，音质最佳
- **MP3** - 广泛支持
- **OGG** - 会自动转换为 MP3
- **M4A** - 会自动转换为 MP3
- **AAC** - 会自动转换为 MP3
- **FLAC** - 会自动转换为 MP3
- **WMA** - 会自动转换为 MP3

> **注意：** 脚本会使用 ffmpeg 将不支持的格式自动转换为 MP3。API 只接受 WAV 和 MP3 格式，但您可以使用 ffmpeg 支持的任何格式。

## 文件限制

- **最大文件大小：** 25 MB
- **最大时长：** 30 秒
- **推荐采样率：** 16000 Hz 或更高
- **音频声道：** 单声道或立体声

## 使用方法

### 基本转录

使用默认设置转录音频文件：

```bash
bash scripts/speech_to_text.sh recording.wav
```

### 带上下文的转录

提供之前的转录内容或上下文以提高准确性：

```bash
bash scripts/speech_to_text.sh recording.wav "这是之前的转录内容，有助于提高准确性"
```

### 带热词的转录

使用自定义词汇表来提高对特定术语的识别准确性：

```bash
bash scripts/speech_to_text.sh recording.mp3 "" "人名,地名,专业术语,公司名称"
```

### 全部选项

结合上下文和热词：

```bash
bash scripts/speech_to_text.sh recording.wav "会议记录片段" "张三,李四,项目名称"
```

**参数：**
- `audio_file` (必填)：音频文件的路径（.wav 或 .mp3）
- `prompt` (可选)：之前的转录内容或上下文文本（最多 8000 个字符）
- `hotwords` (可选)：用逗号分隔的特定术语列表（最多 100 个词）

## 功能

### 上下文提示

**为什么使用上下文提示：**
- 提高长对话的准确性
- 有助于处理领域特定的术语
- 保持多个片段之间的一致性

**何时使用：**
- 多部分对话或会议
- 技术或专业内容
- 从之前的转录内容继续

**示例：**
```bash
bash scripts/speech_to_text.sh part2.wav "第一部分的转录内容：讨论了项目进展和下一步计划"
```

### 热词

**什么是热词？**
自定义词汇表，用于提高对特定术语的识别准确性。

**最佳使用场景：**
- 人名、地名
- 领域特定的术语
- 公司名称和产品名称
- 技术术语
- 行业特定的术语

**示例：**
```bash
# Medical transcription
bash scripts/speech_to_text.sh medical.wav "" "患者,症状,诊断,治疗方案"

# Business meeting
bash scripts/speech_to_text.sh meeting.wav "" "张经理,李总,项目代号,预算"

# Tech discussion
bash scripts/speech_to_text.sh tech.wav "" "API,数据库,算法,框架"
```

## 工作流程示例

### 转录会议内容

```bash
# Part 1
bash scripts/speech_to_text.sh meeting_part1.wav

# Part 2 with context
bash scripts/speech_to_text.sh meeting_part2.wav "第一部分讨论了项目进度" "张总,李经理,项目名称"

# Part 3 with context
bash scripts/speech_to_text.sh meeting_part3.wav "前两部分讨论了项目进度和预算" "张总,李经理,项目名称"
```

### 转录讲座内容

```bash
bash scripts/speech_to_text.sh lecture.wav "" "教授,课程名称,专业术语1,专业术语2"
```

### 处理多个文件

```bash
for file in recording_*.wav; do
    bash scripts/speech_to_text.sh "$file"
done
```

## 音频质量建议

**提高转录准确性的最佳实践：**

1. **清晰的音频源**
   - 减少背景噪音
   - 使用质量良好的麦克风
   - 说话清晰且语速适中

2. **最佳音频设置**
   - 采样率：16000 Hz 或更高
   - 位深度：16 位或更高
   - 单声道（mono）即可

3. **文件准备**
   - 删除文件的开头和结尾处的静音
   - 标准化音频音量
   - 确保音量一致

## 输出格式

脚本输出 JSON 格式的数据，包含以下内容：
- `id`：任务 ID
- `created`：请求时间戳（Unix 时间戳）
- `request_id`：唯一请求标识符
- `model`：使用的模型名称
- `text`：转录的文本

示例输出：
```json
{
  "id": "task-12345",
  "created": 1234567890,
  "request_id": "req-abc123",
  "model": "glm-asr-2512",
  "text": "你好，这是转录的文本内容"
}
```

## 故障排除

**文件大小问题：**
- 将大于 25 MB 的音频文件分割
- 降低采样率或位深度
- 对较小的文件使用压缩格式（如 MP3）

**时长问题：**
- 将超过 30 秒的录音分割成多个部分处理
- 分别处理各个片段
- 使用上下文提示以保持连贯性

**识别准确性低：**
- 提高音频质量
- 使用热词来识别特定术语
- 提供上下文提示
- 确保说话清晰且噪音最小

**格式问题：**
- 确保文件格式为 .wav 或 .mp3
- 检查文件是否损坏
- 确保音频可以在标准播放器中播放

## 限制

- 每次请求的最大音频时长：30 秒
- 文件大小限制：25 MB
- 最多热词数量：100 个
- 上下文提示长度限制：8000 个字符
- 对中文音频的性能最佳

## 性能说明

- 通常的转录时间：1-3 秒
- 大多数音频的转录速度可达到实时或更快
- 处理时间取决于音频的质量和长度