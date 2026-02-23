---
name: ai-voice-chat
description: 通过 AirPods 或任何蓝牙耳机实现免提 AI 语音对话。该系统采用 MLX-Whisper STT 技术（基于 Apple Silicon GPU，响应时间约为 130 毫秒），结合混合式 LLM 路由机制：简单对话在本地 Gemma3 系统中处理，复杂对话则通过云端服务完成；语音合成采用 Kokoro-ONNX TTS 工具，并支持句子的实时流式传输。系统会在耳机连接时自动启动，同时支持对话过程中的语言切换。简单对话完全在本地完成，延迟约为 2.4 秒；复杂查询会路由到云端处理，延迟约为 5 秒。语音处理过程中无需额外费用，仅需要为复杂查询支付云端 LLM API 的使用费用。
os:
  - darwin
requires:
  bins:
    - python3
    - security
  env:
    - VL_OPENCLAW_API_TOKEN
    - VL_OPENCLAW_SESSION_TO
---
# 语音循环系统

**免提语音对话流程：** 用户说话 → MLX-Whisper 进行语音转文字（使用本地 GPU） → 混合式大语言模型（LLM）将转录结果发送到本地或云端 → Kokoro 逐句播放转录后的文本（本地）。

## 系统架构

```
Microphone → MLX-Whisper STT (local GPU, ~130ms) → Router → Kokoro TTS (local, <1s) → Speakers
                                                      ↓
                                          Simple query? → gemma3:1b (local, ~200ms TTFB, free)
                                          Complex query? → OpenClaw API (cloud, ~3s TTFB)
```

当来自混合式大语言模型（LLM）的转录结果到达时，流式文本到语音（STT）引擎会立即将其转换为语音并播放。

### 混合式大语言模型（LLM）路由规则：

- 简单的对话请求（如“你好吗？”、“讲个笑话”、“2+2等于多少？”）会通过 Ollama 路由到本地的 gemma3:1b 模型，**响应时间约 200 毫秒，完全免费**。
- 需要工具、内存、网络搜索、个人数据或智能家居控制功能的复杂请求会通过 OpenClaw 路由到云端（使用 Sonnet/Opus 模型），**响应时间约 3 秒，需要支付 API 许可证费用**。
- 系统会检测请求中是否包含特定关键词（如日历、天气、电子邮件、代码、名称等），并根据请求长度决定是否路由到云端；如果本地模型无法处理请求，系统会自动切换到云端。

### 响应时间对比

| 路由方式 | 静默时间 | 文本转语音（STT） | 大语言模型（LLM） | 语音合成（TTS） | 总响应时间 |
|-------|---------|-----|-----|-----|-------|
| **本地（简单对话）** | 1.0 秒 | 0.13 秒 | 0.3 秒 | 1.0 秒 | **约 2.4 秒** |
| **云端（复杂请求）** | 1.0 秒 | 0.13 秒 | 3.0 秒 | 1.0 秒 | **约 5.1 秒** |

## 安装步骤

运行安装脚本以安装所需依赖库并下载模型：

```bash
bash scripts/setup.sh
```

该脚本会创建一个虚拟环境（.venv），安装 Python 包（`numpy`、`sounddevice`、`soundfile`、`kokoro-onnx`、`mlx-whisper`），并下载 Kokoro 模型（总大小约 136MB）。

### 先决条件：

- 使用 Apple Silicon（M1–M4）架构的 macOS 系统；
- Python 3.11 或更高版本；
- 已安装 Ollama 并拉取了 gemma3:1b 模型（用于本地大语言模型）：`ollama pull gemma3:1b`；
- OpenClaw 已启动并运行：`openclaw gateway status`。

### 推荐的 API 许可证存储方式（macOS Keychain）：

将 OpenClaw 的 API 许可证安全地存储在 macOS 的 Keychain 中，避免以明文形式保存：

```bash
security add-generic-password -a "$USER" -s "voice-loop-openclaw-token" -w "YOUR_TOKEN_HERE" -U
```

系统会自动从 Keychain 中读取 API 许可证。此外，也可以通过设置环境变量（`VL_OPENCLAW_API_TOKEN`、`VL_OPENCLAW_SESSION_TO`）来指定会话目标；如果两者都存在，环境变量的设置优先级高于 Keychain 的设置。

## 运行方式

### 手动启动

```bash
.venv/bin/python scripts/voice_loop.py
```

### 头戴设备连接时自动启动

```bash
.venv/bin/python scripts/airpods_watcher.py
```

系统会每隔 5 秒检查一次音频设备。当检测到与 `VL_HEADSET_NAME` 匹配的设备时，会启动语音循环；设备断开连接时，系统会停止语音循环；系统崩溃时，会自动重启语音循环。

### 启动时自动启动（使用 launchd）

创建 `~/Library/LaunchAgents/com_voice-loop.watcher.plist` 文件：

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

请替换文件中的 `VENV_PYTHON_PATH` 和 `WATCHER_SCRIPT_PATH`；这些路径中的 API 许可证信息会在运行时从 Keychain 中读取。

## 配置选项

| 配置项 | 默认值 | 说明 |
|----------|---------|-------------|
| `STT_engine` | `mlx-whisper` | 语音转文字引擎（使用本地 GPU，速度较快）或 `whisper-cli`（旧版本） |
| `MLX_WHISPER_MODEL` | `mlx-community/whisper-base.en-mlx` | 用于 MLX-Whisper 的 HuggingFace 模型 |
| `LOCAL_LLM_ENABLED` | `True` | 启用本地/云端混合路由功能 |
| `LOCAL_LLM_MODEL` | `gemma3:1b` | 用于处理简单请求的 Ollama 模型 |
| `SILENCE_THRESHOLD` | `0.015` | 静默检测的 RMS 阈值（单位：分贝） |
| `SILENCE_DURATION` | `1.0` | 静默持续时间（单位：秒） |
| `KOKORO_SPEED` | `1.15` | 语音播放速度 |

这些配置项可以直接在 `voice_loop.py` 文件中修改，或通过设置相应的环境变量 `VL_*` 来调整。

## 语言切换

在对话过程中，用户可以随时说出以下指令进行语言切换：

- **切换到西班牙语**：`switch to Spanish`、`Spanish mode`、`habla en español`
- **切换回英语**：`back to English`、`English mode`

语言切换后，语音合成引擎和 Kokoro 的语音会相应改变，大语言模型的提示信息也会包含新的语言信息。

## 语音合成选项：

- **英语**：`af_heart ⭐`（女性音色）、`am_puck ⭐`（男性音色）
- **西班牙语**：`ef_dora ⭐`（女性音色）、`em_alex`（男性音色）

如需更改默认语音性别，可以在 `voice_loop.py` 文件中设置 `CURRENT_GENDER = "male"`。

## 优化建议：

- **提高转录速度**：尝试使用 `mlx-community/distil-whisper-small.en` 模型以获得更快的转录速度。
- **禁用本地大语言模型**：将 `LOCAL_LLM_ENABLED` 设置为 `False`，以便所有请求都通过云端处理。
- **选择不同的语音模型**：`qwen3:4b` 提供更好的音质（但响应速度较慢）；`gemma3:1b` 速度更快。
- **优化响应速度**：将 `SILENCE_DURATION` 设置为 `0.8` 可以减少暂停时间。
- **解决噪音问题**：适当提高 `SILENCE_THRESHOLD`（例如设置为 `0.02` 或 `0.03` 可以减少误判）。

## 常见问题及解决方法：

- **音频设备问题**：确保耳机已正确连接或设置为默认输入设备。
- **转录结果为空或出现错误**：可能是 Whisper 在背景噪音中生成了错误文本；请提高 `SILENCE_THRESHOLD` 的值。
- **流式转录失败**：检查 OpenClaw 是否正在运行以及 API 许可证是否有效。
- **本地大语言模型不可用**：可能是 Ollama 未启动或 gemma3:1b 模型未成功下载；请运行 `ollama pull gemma3:1b`。
- **Kokoro 模型未找到**：运行 `bash scripts/setup.sh` 以下载模型。

## 成本说明：

简单对话的费用为 0 美元（所有处理步骤（文本转语音、本地大语言模型、语音合成）都在本地完成）；仅复杂请求需要支付云端大语言模型的 API 许可证费用。

## 安全性措施：

- API 许可证存储在 macOS Keychain 中，运行时自动读取。
- API 请求仅允许发送到本地主机（localhost）。
- 所有的音频捕获和语音合成操作都在本地完成，只有文本数据会被发送到云端的大语言模型。

## 致谢：

- [MLX-Whisper](https://github.com/ml-explore/mlx-examples)：用于 Apple Silicon GPU 的语音转文字技术。
- [Kokoro-ONNX](https://github.com/thewh1teagle/kokoro-onnx)：本地语音合成引擎。
- [Ollama](https://ollama.ai)：用于本地大语言模型推理的框架。
- [OpenClaw](https://github.com/openclaw/openclaw)：用于管理 AI 代理的框架。