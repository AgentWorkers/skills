---
name: voice-log
description: >
  **使用 Soniox 实时语音转文字（STT）功能为 OpenClaw 实现背景语音记录**  
  该功能需要使用 **SONIOX_API_KEY**。您可以在 [https://soniox.com/speech-to-text](https://soniox.com/speech-to-text) 上获取或创建您的 Soniox API 密钥。  
  **使用场景：**  
  - 当用户请求开始或停止语音记录时（例如：“开始语音记录”、“结束语音记录”等命令）；  
  - 当用户请求获取过去 N 分钟对话的摘要或文字记录时。
metadata: {"openclaw":{"requires":{"bins":["node","arecord|rec|ffmpeg"],"env":{"SONIOX_API_KEY":"required - Soniox API key"},"note":"Captures microphone audio locally and streams audio to Soniox realtime STT only while journal is running."}}}
---
# 语音日志

这是一个使用 Soniox 的实时语音转文本（STT）功能来记录对话的日志系统。该系统在后台以守护进程的形式运行，具备以下功能：
- 持续捕获麦克风输入的音频数据。
- 生成仅包含文本的日志文件，将实时对话内容按分钟为单位进行分组存储。
- 目前仅保留最近 60 分钟的对话记录。

## 命令操作

请从该技能目录中运行以下命令：

```bash
npm install
node scripts/voice_journal_ctl.js start
node scripts/voice_journal_ctl.js end
node scripts/voice_journal_ctl.js status
node scripts/voice_journal_ctl.js last 10
```

## OpenClaw 触发处理

当用户执行以下命令时：
- `start voice journal`：执行 `node scripts/voice_journal_ctl.js start`。
- `start voice log`：执行 `node scripts/voice_journal_ctl.js start`。
- `start voice log ["en","de"]`：执行 `node scripts/voice_journal_ctl.js start '["en","de"]'`。
- `end voice journal`：执行 `node scripts/voice_journal_ctl.js end`。
- `summarize what we talked about for last 10 minutes`：执行 `node scripts/voice_journal_ctl.js last 10`，然后输出过去 10 分钟的对话摘要。

**注意事项：**
- 始终仅用一句话回复用户的请求结果。
- 除非用户明确要求，否则不要粘贴原始命令输出或对话记录的文本片段。
- 如果指定时间范围内的对话记录不存在，应明确告知用户。
- 绝不允许伪造对话记录的文本内容。

## 必需的环境变量

请设置以下环境变量：
- `SONIOX_API_KEY`（必需）：请访问 https://soniox.com/speech-to-text 获取或创建该密钥。

**可选设置：**
- 无。除 `start` 命令中传递的语言参数外，其他运行时配置均为硬编码。

**默认值：**
- 数据存储目录：当前技能目录下的 `./.data`。
- Soniox 的 WebSocket 端点：使用 SDK 的默认值（`SONIOX_API_WS_URL`）。
- 使用的语音转文本模型：`stt-rt-v4`。
- 每条日志的最大字符数：默认为 1800 个字符，可通过 `--max-chars` 参数进行修改。
- 守护进程的环境变量：仅传递 `SONIOX_API_KEY`（以及可选的语言参数）；其他与主机环境相关的配置不会被继承。

**音频捕获的默认设置：**
- 系统会自动选择适用于当前平台的音频捕获命令。推荐设置如下：
- Linux：`arecord -q -f S16_LE -r 16000 -c 1 -t raw`
- macOS：`sox -q -d -t raw -b 16 -e signed-integer -r 16000 -c 1 -`