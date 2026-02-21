---
name: speakturbo-tts
description: 让你的智能助手能够实时与你交流吧！使用Claude，它拥有超快的文本转语音（TTS）技术，语音合成能力以及大约90毫秒的延迟时间，能够实现即时语音响应。Claude内置了8种不同的语音风格，可以满足你的各种需求。如果你需要克隆某个角色的声音，只需使用“speak”技能即可。
---
# speakturbo - 与你的Claude实时对话！

让你的AI助手能够实时与你交流。超快的文本转语音功能，延迟仅约90毫秒，并支持8种内置语音。

## 快速入门

```bash
# Play immediately - you should hear "Hello world" through your speakers
speakturbo "Hello world"
# Output: ⚡ 92ms → ▶ 93ms → ✓ 1245ms

# Verify it's working by saving to file
speakturbo "Hello world" -o test.wav
ls -lh test.wav  # Should show ~50-100KB file
```

**输出说明：** `⚡` = 收到第一个音频信号，`▶` = 开始播放，`✓` = 播放完成

## 首次运行

**首次运行需要2-5秒**，因为后台程序需要启动并将模型加载到内存中。后续调用从接收到信号到开始播放声音的时间约为90毫秒。

```bash
# First run (slow - daemon starting)
speakturbo "Starting up"  # ~2-5 seconds

# Second run (fast - daemon already running)
speakturbo "Now I'm fast"  # ~90ms
```

## 使用方法

```bash
# Basic - plays immediately (default voice: alba)
speakturbo "Hello world"

# Save to file (no audio playback)
speakturbo "Hello" -o output.wav

# Save to specific file
speakturbo "Goodbye" -o goodbye.wav

# Quiet mode (suppress status messages, still plays audio)
speakturbo "Hello" -q

# List available voices
speakturbo --list-voices
```

## 可用语音

| 语音 | 类型 |
|-------|------|
| `alba` | 女性（默认） |
| `marius` | 男性 |
| `javert` | 男性 |
| `jean` | 男性 |
| `fantine` | 女性 |
| `cosette` | 女性 |
| `eponine` | 女性 |
| `azelma` | 女性 |

## 性能

| 指标 | 值 |
|--------|-------|
| 从接收到信号到开始播放声音的时间 | 约90毫秒（后台程序预热完毕） |
| 首次运行时间 | 2-5秒（后台程序启动） |
| 实时性 | 快约4倍 |
| 采样率 | 24kHz单声道 |

## 架构

```
speakturbo (Rust CLI, 2.2MB)
    │
    │ HTTP streaming (port 7125)
    ▼
speakturbo-daemon (Python + pocket-tts)
    │
    │ Model in memory, auto-shutdown after 1hr idle
    ▼
Audio playback (rodio)
```

## 文本输入

- **编码格式：** UTF-8
- **文本中的引号：** 使用转义字符：`speakturbo "She said \"hello\""`
- **长文本：** 支持输入长文本，系统会实时生成音频流

## 输出路径安全

`-o` 标志仅会将输出文件写入允许列表中的目录。默认允许的目录包括：
- `/tmp` 和系统临时文件夹
- 当前工作目录
- `~/.speakturbo/`

如需将输出文件写入其他位置，请使用 `--allow-dir` 参数：

```bash
speakturbo "Hello" -o /custom/path/audio.wav --allow-dir /custom/path
```

若需永久允许某个目录被写入，将其添加到 `~/.speakturbo/config` 文件中：

```bash
mkdir -p ~/.speakturbo && echo "/custom/path" >> ~/.speakturbo/config
```

配置文件中每行对应一个允许的目录。以 `#` 开头的行是注释。

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 成功（音频已播放/保存） |
| 1 | 错误（后台程序连接失败，参数无效） |

## 使用场景

**在以下情况下使用 speakturbo：**
- 需要即时音频反馈（延迟约90毫秒）
- 速度比语音多样性更重要
- 内置语音即可满足需求

**在以下情况下使用 `speak`：**
- 需要自定义语音效果（例如模仿摩根·弗里曼的声音）：
  → `speak "text" --voice ~/.chatter/voices/morgan_freeman.wav`
- 需要添加情感标签（如 `[laugh]`, `[sigh]`）
- 音质和多样性比速度更重要

有关 `speak` 的完整使用方法，请参阅其官方文档。

## 故障排除

**音频无法播放：**
```bash
# Check daemon is running
curl http://127.0.0.1:7125/health
# Expected: {"status":"ready","voices":["alba","marius",...]}

# Verify by saving to file and playing manually
speakturbo "test" -o /tmp/test.wav
afplay /tmp/test.wav  # macOS
aplay /tmp/test.wav   # Linux
```

**后台程序无法启动：**
```bash
# Check port availability
lsof -i :7125

# Manually kill and restart
pkill -f "daemon_streaming"
speakturbo "test"  # Auto-restarts daemon
```

**首次运行速度较慢：**
这是正常现象，因为后台程序需要加载约100MB的模型文件到内存中。后续调用将非常快速（延迟约90毫秒）。

## 后台程序管理

后台程序会在首次使用时自动启动，并在**空闲1小时后自动关闭**。

```bash
# Check status
curl http://127.0.0.1:7125/health

# Manual stop
pkill -f "daemon_streaming"

# View logs
cat /tmp/speakturbo.log
```

## 与 `speak` 的比较

| 功能 | speakturbo | speak |
|---------|------------|-------|
| 从接收到信号到开始播放声音的时间 | 约90毫秒 | 约4-8秒 |
| 自定义语音效果 | 不支持 | 支持 |
| 情感标签 | 不支持 | 支持 |
| 提供的语音数量 | 8种内置语音 | 可自定义WAV文件 |
| 使用的引擎 | pocket-tts | Chatterbox |