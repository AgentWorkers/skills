---
name: voice-log
description: 使用 Soniox 的实时语音转文字（STT）功能，为 OpenClaw 实现背景语音日志记录功能。当用户请求开始或停止被动语音记录时（例如输入“start voice journal”、“start voice log”或“end voice journal”等命令），或者请求获取过去 N 分钟对话的摘要/文字记录时，该功能可发挥作用。
---
# 语音日志（Soniox）

使用 Soniox 的实时语音转文字（STT）功能，在后台守护进程中实现以下功能：
- 持续捕获麦克风音频。
- 每 15 分钟重新连接 Soniox 服务器。
- 仅存储文本数据（不存储任何令牌对象），并按分钟进行分组。
- 仅保留最近 60 分钟的音频记录。

## 命令

从该技能目录运行以下命令：

```bash
npm install
node scripts/voice_journal_ctl.js start
node scripts/voice_journal_ctl.js end
node scripts/voice_journal_ctl.js status
node scripts/voice_journal_ctl.js last 10
```

## OpenClaw 触发处理

当用户执行以下命令时：
- `start voice journal`：运行 `node scripts/voice_journal_ctl.js start`。
- `start voice log`：运行 `node scripts/voice_journal_ctl.js start`。
- `start voice log ["en","si"]`：运行 `node scripts/voice_journal_ctl.js start '["en","si"]'`。
- `end voice journal`：运行 `node scripts/voice_journal_ctl.js end`。
- `summarize what we talked about for last 10 minutes`：运行 `node scripts/voice_journal_ctl.js last 10`，然后输出总结结果。

**注意事项：**
- 始终仅用一句话回复用户请求的结果。
- 除非用户明确要求提供原始命令输出或转录内容，否则不要粘贴任何命令输出或转录片段。
- 如果指定时间范围内没有音频数据，必须明确告知用户。
- 绝不允许伪造转录文本。

## 必需的环境变量

设置以下环境变量：
- `SONIOX_API_KEY`（必需）

可选环境变量：
- `VOICE_JOURNAL_DATA_DIR`（默认值为 `./.data`）
- `VOICE_JOURNAL_AUDIO_CMD`（自定义麦克风捕获命令；该命令必须将 16kHz 单声道 PCM 数据输出到标准输出）
- `VOICE_JOURNAL LANGUAGE_HINTS`（JSON 数组，例如 `["en","si"]`；通常通过启动命令的参数进行设置）

## 音频捕获默认设置

系统会自动选择适合当前平台的命令。推荐命令如下：
- Linux：`arecord -q -f S16_LE -r 16000 -c 1 -t raw`
- macOS：`sox -q -d -t raw -b 16 -e signed-integer -r 16000 -c 1 -`

如果自动检测失败，请手动设置 `VOICE_JOURNAL_AUDIO_CMD`。