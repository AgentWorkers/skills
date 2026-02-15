---
name: assemblyai-transcribe
description: 使用 AssemblyAI 转录音频/视频（支持本地上传或使用 URL），同时支持生成字幕以及导出段落/句子内容。
homepage: https://www.assemblyai.com/docs
user-invocable: true
metadata: {"clawdbot":{"skillKey":"assemblyai","emoji":"🎙️","requires":{"bins":["node"],"env":["ASSEMBLYAI_API_KEY"]},"primaryEnv":"ASSEMBLYAI_API_KEY"}}
---

# AssemblyAI转录 + 导出功能

当您需要使用AssemblyAI对音频/视频进行转录，或导出可读格式的内容（如字幕、段落、句子）时，请使用此功能。

该辅助脚本实现了基本的REST接口流程：

1. 通过`POST /v2/upload`上传本地文件。
2. 通过`POST /v2/transcript`创建转录任务。
3. 定期查询`GET /v2/transcript/:id`，直到转录任务的`status`状态变为`completed`（或`error`）。

## 设置要求

使用此功能需要满足以下条件：

- 系统路径中包含`node`（推荐使用Node.js 18及以上版本；脚本使用了内置的`fetch`函数）。
- 环境变量中设置`ASSEMBLYAI_API_KEY`。

推荐的Clawdbot配置文件（位于`~/.clawdbot/clawdbot.json`）：

```js
{
  skills: {
    entries: {
      // This skill declares metadata.clawdbot.skillKey = "assemblyai"
      assemblyai: {
        enabled: true,
        // Because this skill declares primaryEnv = ASSEMBLYAI_API_KEY,
        // you can use apiKey as a convenience:
        apiKey: "YOUR_ASSEMBLYAI_KEY",
        env: {
          ASSEMBLYAI_API_KEY: "YOUR_ASSEMBLYAI_KEY",

          // Optional: use EU async endpoint
          // ASSEMBLYAI_BASE_URL: "https://api.eu.assemblyai.com"
        }
      }
    }
  }
}
```

## 使用方法

请通过Exec工具运行以下命令：

### 转录（本地文件或公共URL）

将转录文本输出到标准输出（stdout）：

```bash
node {baseDir}/assemblyai.mjs transcribe "./path/to/audio.mp3"
node {baseDir}/assemblyai.mjs transcribe "https://example.com/audio.mp3"
```

将转录结果写入文件（适用于较长的音频文件）：

```bash
node {baseDir}/assemblyai.mjs transcribe "./path/to/audio.mp3" --out ./transcript.txt
```

### 传递高级转录参数

可以通过`--config`参数传递`POST /v2/transcript`支持的所有参数：

```bash
node {baseDir}/assemblyai.mjs transcribe "./path/to/audio.mp3" \
  --config '{"speaker_labels":true,"summarization":true,"summary_model":"informative","summary_type":"bullets"}' \
  --export json \
  --out ./transcript.json
```

### 导出字幕（SRT/VTT格式）

完成转录后立即导出字幕：

```bash
node {baseDir}/assemblyai.mjs transcribe "./path/to/video.mp4" --export srt --out ./subtitles.srt
node {baseDir}/assemblyai.mjs transcribe "./path/to/video.mp4" --export vtt --out ./subtitles.vtt
```

或根据现有的转录ID导出字幕：

```bash
node {baseDir}/assemblyai.mjs subtitles <transcript_id> srt --out ./subtitles.srt
```

### 导出段落/句子

```bash
node {baseDir}/assemblyai.mjs paragraphs <transcript_id> --out ./paragraphs.txt
node {baseDir}/assemblyai.mjs sentences <transcript_id> --out ./sentences.txt
```

### 获取现有转录结果

```bash
node {baseDir}/assemblyai.mjs get <transcript_id> --format json
node {baseDir}/assemblyai.mjs get <transcript_id> --wait --format text
```

## 使用提示：

- 如果输出文件较大，建议使用`--out <文件路径>`选项。
- 请不要将API密钥记录在日志或聊天记录中，应通过环境变量进行传递。
- 如果用户要求数据在欧盟地区进行处理或存储，请将`ASSEMBLYAI_BASE_URL`设置为欧盟地区的服务器地址。
- AssemblyAI要求上传文件和后续的转录请求必须使用同一项目的API密钥；否则会收到403错误（“无法访问上传的文件”）。