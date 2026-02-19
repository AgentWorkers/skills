---
name: whisnap
description: macOS 命令行工具（CLI），用于使用本地的 Whisper 模型或 Whisnap Cloud 对音频和视频文件进行转录。
homepage: https://whisnap.com
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["whisnap"]},"install":[{"id":"app","kind":"manual","label":"Install via Whisnap app Settings → Advanced → Enable CLI"}]}}
---
# whisnap

使用 `whisnap` 从终端转录音频/视频文件。需要安装 Whisnap macOS 应用程序，并至少下载一个转录模型。

**设置（只需一次）：**
- 打开 Whisnap 应用程序 → 设置 → 高级 → 启用 CLI（系统会在 `/usr/local/bin/` 目录下创建 `whisnap` 符链接）
- 在应用程序中下载至少一个转录模型。

**常用命令：**
- 转录音频：`whisnap recording.wav`
- 转录视频：`whisnap meeting.mp4`
- 云转录：`whisnap recording.wav --cloud`
- 生成包含时间戳的 JSON 输出：`whisnap lecture.m4a --json`
- 指定转录模型：`whisnap interview.wav -m small-q5_1`
- 云转录 + JSON 输出：`whisnap recording.wav --cloud --json`
- 列出已下载的模型：`whisnap --list-models`
- 显示详细诊断信息：`whisnap recording.wav -v`

**支持的格式：**
- 音频：WAV, MP3, FLAC, M4A, OGG
- 视频：MP4, MOV, MKV, WebM

**参数说明：**
- `-c, --cloud` — 使用 Whisnap 云服务进行转录（需要登录）
- `-m, --model <ID>` — 指定转录模型（例如 `small-q5_1`）。默认使用应用程序选择的模型。
- `-j, --json` — 生成包含文本、转录片段和时间戳的 JSON 输出文件
- `-v, --verbose` — 将进度和诊断信息输出到标准错误流（stderr）
- `--list-models` — 列出所有可用模型后退出

**JSON 输出格式：**
```json
{
  "text": "transcribed text",
  "segments": [{ "start_ms": 0, "end_ms": 1000, "text": "segment" }],
  "model": "small-q5_1",
  "backend": "whisper",
  "processing_time_ms": 5000
}
```

**注意事项：**
- CLI 会使用 Whisnap 应用程序中的模型和设置（路径：`~/Library/Application Support/com.whisnap.desktop/`）。
- 云转录模式需要登录。
- 在脚本中使用 `--json` 参数，并将输出重定向到标准输出（stdout）；诊断信息会显示在标准错误流（stderr）中。
- 成功返回代码为 `0`，失败返回代码为 `1`。
- CLI 模式仅支持 Whisnap 转录模型（不支持 Parakeet 模型）。
- 在转录前请确认文件路径存在；CLI 会验证文件路径，但不会自动搜索文件。