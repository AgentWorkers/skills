---
name: ai-voice-chat
description: 通过 AirPods 或任何蓝牙耳机实现免提 AI 语音对话。使用本地 Whisper STT 技术以及 Kokoro-ONNX TTS 语音合成引擎，并通过 OpenClaw 代理进行流式处理。当耳机连接时自动启动该功能，支持在对话过程中切换语言（英语、西班牙语、法语、日语、中文）。适用于设置语音聊天、语音助手、语音交互、配置语音循环、音频故障排查，或启用与 AI 代理的免提语音对话。语音处理完全免费，仅需支付 LLM API 令牌费用。
os:
  - darwin
requires:
  bins:
    - whisper
    - python3
    - security
  env:
    - VL_OPENCLAW_API_TOKEN
    - VL_OPENCLAW_SESSION_TO
---
# 语音循环系统

**免提语音对话流程：** 用户说话 → Whisper 将语音转换为文本（本地处理） → OpenClaw 将文本转换为语音流（使用 SSE 协议） → Kokoro 用目标语言逐句播放语音。

## 架构

```
Microphone → Whisper STT (local, ~2s) → OpenClaw API (cloud, ~4-10s) → Kokoro TTS (local, <1s) → Speakers
```

该系统会实时将接收到的文本转换为语音：第一个语音片段会在大约 3 秒内播放完成，而非 13 秒。

## 设置

运行设置脚本以安装依赖项并下载所需模型：

```bash
bash scripts/setup.sh
```

此脚本会创建一个虚拟环境（`.venv`），安装 Python 包（`numpy`、`sounddevice`、`soundfile`、`kokoro-onnx`），并下载 Kokoro 模型（总大小约 136MB）。

### 先决条件

- 需要运行在支持 Apple Silicon（M1–M4）的 macOS 系统上。
- Python 3.11 或更高版本。
- 需要安装 Whisper CLI：`brew install openai-whisper`。
- 确保 OpenClaw 已经启动：`openclaw gateway status` 命令可用于检查 OpenClaw 的运行状态。

### 令牌存储（推荐使用：macOS Keychain）

建议将 OpenClaw 的 API 令牌安全地存储在 macOS Keychain 中，而非以明文形式保存：

```bash
security add-generic-password -a "$USER" -s "voice-loop-openclaw-token" -w "YOUR_TOKEN_HERE" -U
```

系统会自动从 Keychain 中读取令牌。如果需要设置会话目标，也可以通过环境变量来实现：

```bash
security add-generic-password -a "$USER" -s "voice-loop-session-to" -w "+1XXXXXXXXXX" -U
```

另外，也可以通过设置环境变量 `VL_OPENCLAW_API_TOKEN` 和 `VL_OPENCLAW_SESSION_TO` 来配置会话信息。这些环境变量的优先级高于 Keychain 中的配置。

### 环境变量

| 变量 | 是否必需 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `VL_OPENCLAW_API_TOKEN` | 是* | 从 Keychain 中读取的 OpenClaw API 令牌。（若未设置，则从 `keychain voice-loop-openclaw-token` 中获取） |
| `VL_OPENCLAW_SESSION_TO` | 是* | 目标电话号码或用户 ID。（若未设置，则从 Keychain 中读取的 `voice-loop-session-to` 中获取） |
| `VL_OPENCLAW_API_URL` | 否 | `http://127.0.0.1:18789/v1/chat/completions` | OpenClaw API 的本地端点地址（远程端点不可使用） |
| `VL_SILENCE_THRESHOLD` | 否 | 0.015 | 用于检测静音的 RMS 值 |
| `VL_SILENCE_DURATION` | 否 | 1.2 | 静音持续时间（秒） |
| `VL_KOKORO_speed` | 否 | 1.15 | TTS 播放速度（1.0 表示自然语速） |
| `VL_DEFAULTLANG` | 否 | `en` | 默认语言 |
| `VL_DEFAULT_GENDER` | 否 | `female` | 默认语音性别（女性/男性） |
| `VL_WHISPER_MODEL_EN` | 否 | `base.en` | 英语 Whisper 模型 |
| `VL_WHISPER_MODEL_MULTI` | 否 | `small` | 多语言 Whisper 模型 |
| `VL_HEADSET_NAME` | 否 | 要监控的蓝牙设备名称（例如：AirPods） |
| `VL POLL_INTERVAL` | 否 | 5 | 耳机状态检查间隔（秒） |

## 运行方式

### 手动启动

```bash
export VL_OPENCLAW_API_TOKEN="your-token"
export VL_OPENCLAW_SESSION_TO="+1XXXXXXXXXX"
.venv/bin/python scripts/voice_loop.py
```

### 耳机连接时自动启动

```bash
.venv/bin/python scripts/airpods_watcher.py
```

系统会每 5 秒检查一次音频设备。当检测到与 `VL_HEADSET_NAME` 匹配的耳机时，会启动语音循环；设备断开连接时，循环会停止；程序崩溃时会自动重启。

### 启动时自动启动（使用 launchd）

创建 `~/Library/LaunchAgents/com.voice-loop.watcher.plist` 文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.voice-loop.watcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>VENV_PYTHON_PATH</string>
        <string>WATCHER_SCRIPT_PATH</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/voice-loop-watcher.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/voice-loop-watcher.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

请替换 `VENV_PYTHON_PATH` 和 `WATCHER_SCRIPT_PATH` 的值。这些路径中的令牌会在运行时从 Keychain 中读取。

## 语言切换

在对话过程中，可以执行以下命令进行语言切换：

- **切换到西班牙语：** `switch to Spanish`、`Spanish mode`、`habla en español`
- **切换到法语：** `switch to French`、`French mode`、`parle en français`
- **切换到日语：** `switch to Japanese`、`Japanese mode`、`speak Mandarin`
- **切换回英语：** `back to English`、`English mode`、`stop Spanish`

切换语言后，Whisper 模型会从 `base.en` 更改为 `small`（多语言模型），Kokoro 的语音和语言也会相应改变，且 LLM 的提示信息会包含当前语言的上下文。系统还会用目标语言播放确认语音。

## 语音选项

- **英语语音：** af_heart ⭐（女性）、am_puck ⭐（男性）、af_bella、af_nova、af_sarah、am_adam、am_eric
- **西班牙语语音：** ef_dora ⭐（女性）、em_alex（男性）
- **法语语音：** ff_siwis
- **日语语音：** jf_alpha（女性）、jm_beta（男性）
- **中文语音：** zf_xiaobei（女性）、zm_yunjian（男性）

若需更改默认语音性别，可以执行：`export VL_DEFAULT_GENDER=male`

## 调优建议

- **加快语音转文字（STT）速度：** 将 `VL_WHISPER_MODEL_EN` 设置为 `tiny.en`（速度约为 1 秒，但准确性可能较低）。
- **提升响应速度：** 将 `VL_SILENCE_DURATION` 设置为 0.8 秒（可减少静音检测的延迟）。
- **加快 LLM 的响应速度：** 将 `VL_SONNET` 作为 LLM 的模型（速度约为 4 秒，相比 `Opus` 模型快）。
- **解决噪音问题：** 提高 `VL_SILENCE_THRESHOLD` 的值（建议尝试 0.02 或 0.03）。
- **调整语速：** 将 `VL_KOKORO_speed` 设置为 1.2 以加快语音播放速度，1.0 表示自然语速。

## 常见问题及解决方法

- **音频设备问题：** 确保耳机已连接并设置为默认输入设备。可在系统设置 > 音频中进行检查。
- **转录结果为空或出现错误：** 可能是由于 Whisper 在背景噪音中生成了错误文本。脚本会自动过滤长度小于 3 个词的输入内容或常见的错误信息。如果问题持续存在，可尝试提高 `VL_SILENCE_THRESHOLD` 的值。
- **流媒体传输错误：** 可能是由于 OpenClaw 未运行或令牌无效。请检查 `openclaw gateway status` 的状态。
- **Kokoro 模型未找到：** 运行 `bash scripts/setup.sh` 命令将模型下载到 `~/.cache/kokoro-onnx/` 目录。
- **多语言转录效果不佳：** 使用 `small` 模型时，如果麦克风输入的音频质量不佳，可能会导致转录结果混乱。建议确保音频质量清晰。

## 成本

语音处理费用为 0 美元。Whisper 和 Kokoro 都在本地运行，唯一费用是 LLM API 令牌的费用（与发送文本消息的费用相同）。

## 延迟情况

| 功能 | 处理时间 | 本地/云端 |
|-----------|------|-------------|
| Whisper 的语音转文字（STT） | 约 2 秒 | 本地处理 |
| LLM（使用 Opus 模型） | 约 8–10 秒 | 云端处理 |
| LLM（使用 Sonnet 模型） | 约 3–5 秒 | 云端处理 |
| Kokoro 的文本转语音（TTS） | 小于 1 秒 | 本地处理 |
| **首次语音传输时间：** 约 3 秒 |

## 安全性措施

- **令牌安全：** 令牌存储在 macOS Keychain 中，不会以明文形式保存在文件或环境变量中。脚本在运行时通过 `security find-generic-password` 从 Keychain 中读取令牌。
- **API 端点限制：** 脚本仅允许连接到本地的 API 端点（`http://127.0.0.1:18789`）。如果 `VL_OPENCLAW_API_URL` 指向远程地址，脚本会立即退出。
- **隔离的子进程环境：** 监控脚本仅将 `VL_*` 环境变量、`PATH` 和 `HOME` 传递给语音循环进程，不会暴露用户的完整环境信息。
- **限制可执行文件路径：** Whisper 和 Python 的路径来自系统的 `PATH` 或虚拟环境（`venv`），无法通过环境变量进行自定义。
- **数据安全：** 所有音频捕获和语音转文字操作都在本地完成，不会将音频数据发送到云端。只有文本转录结果会发送到 LLM。
- **防止数据泄露：** 脚本仅与本地地址进行网络通信，无法访问远程端点。

## 致谢

- [Kokoro-ONNX](https://github.com/thewh1teagle/kokoro-onnx)：本地使用的神经网络语音转文字引擎
- [OpenAI Whisper](https://github.com/openai/whisper)：本地使用的文本转语音工具
- [OpenClaw](https://github.com/openclaw/openclaw)：用于管理 AI 代理的框架