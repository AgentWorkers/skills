---
name: pronunciation-coach
description: 使用 Azure Speech Services 进行发音辅导，通过真实语音分析来评估音频文件在音素级别上的准确性、流利度、韵律和语调。
env:
  AZURE_SPEECH_KEY: Azure Speech Service API Key
  AZURE_SPEECH_REGION: Azure Speech Service Region (e.g., southeastasia)
---
# 发音教练

使用 Azure Speech Services 分析英语口语发音，并提供可操作的发音指导反馈。

**隐私声明**：该功能会读取本地语音文件（位于 `~/.openclaw/media/inbound/`），并将其传输到 Microsoft Azure Speech Services 进行处理。

## 先决条件

- **Azure Speech API 密钥**：设置环境变量 `AZURE_SPEECH_KEY`
- **Azure Speech 地区**：设置环境变量 `AZURE_SPEECH_REGION`（例如：`southeastasia`）
- **ffmpeg**：用于音频格式转换（必须位于系统路径中）
- **Node.js**：用于生成报告

## 工作流程

### 1. 接收音频

来自 Telegram 的语音消息存储在 `~/.openclaw/media/inbound/` 目录下。找到与消息时间戳匹配的最新 `.ogg` 文件。

```bash
ls -lt ~/.openclaw/media/inbound/*.ogg | head -5
```

### 2. 进行评估

```bash
scripts/pronunciation-assess.sh <audio_file> "<reference_text>"
```

- `audio_file`：语音文件的路径（格式为 `.ogg`、`wav`、`mp3` 或 `m4a`）
- `reference_text`：说话者实际想要表达的内容（来自转录文本）
- 脚本会自动将音频文件转换为 16kHz 单声道 WAV 格式

### 3. 生成报告

将 JSON 格式的评估结果传递给报告生成工具：

```bash
scripts/pronunciation-assess.sh audio.ogg "reference text" | node scripts/pronunciation-report.js
```

报告内容包括：
- 总体评分（发音、准确性、流畅度、韵律、完整性）
- 每个单词的详细评分（按音素划分）
- 需改进的发音问题
- 以及具体的改进建议

### 4. 提供发音指导

生成报告后，执行以下步骤：
1. **将报告文本** 发送给用户（包括评分和单词详细分析）
2. **识别出发音问题最严重的 3 个音素**
3. **解释每个问题**：说明正确的发音方式以及如何发出该音素
   - 请参考 `references/phoneme-guide.md` 以获取音素描述和修正方法
4. **通过 TTS（文本转语音）** 演示正确发音
5. **布置练习**：为用户提供需要重新录制的特定句子，重点练习有问题的发音

### 发音指导建议

- 评分 ≥ 90：表现优秀，只需稍作改进
- 评分 70-89：表现良好，需要针对性练习
- 评分 < 70：需要重点练习某个特定音素
- “遗漏”错误表示语音未被识别——可能是说话者声音太小或含糊不清
- 韵律评分低于 85 表示发音过于单调——需指导语调的升降
- 通过多次录音对比评分，以跟踪发音进步情况