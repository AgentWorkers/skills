---
name: whisper-mlx-local
description: "使用 Apple Silicon 上的 MLX Whisper，为 Telegram 和 WhatsApp 提供免费的本地语音转文本功能。该服务是私密的，且无需支付任何 API 费用。"
metadata:
  openclaw:
    emoji: "🎤"
    version: "1.5.0"
    author: "Community"
    repo: "https://github.com/ImpKind/local-whisper"
    requires:
      os: ["darwin"]
      arch: ["arm64"]
      bins: ["python3"]
    install:
      - id: "deps"
        kind: "manual"
        label: "Install dependencies"
        instructions: "pip3 install -r requirements.txt"
---

# 本地语音转录工具

**在 Telegram 和 WhatsApp 上免费转录语音消息。** 无需 API 密钥，完全免费，可在您的 Mac 上运行。

## 问题

语音转录 API 需要付费：
- OpenAI Whisper：**每分钟 0.006 美元**
- Groq：**每分钟 0.001 美元**
- AssemblyAI：**每分钟 0.01 美元**

如果您需要转录大量的 Telegram 语音消息，费用会相当可观。

## 解决方案

该工具在您的 Mac 上本地运行 Whisper 服务，质量相同，且完全免费。

- ✅ 永久免费
- ✅ 保密性高（音频数据不会离开您的 Mac）
- ✅ 转录速度快（每条消息约 1 秒）
- ✅ 支持离线模式

## ⚠️ 重要说明

- **首次运行时会下载约 1.5GB 的模型文件** — 请耐心等待，此过程仅发生一次
- **首次转录速度较慢** — 模型加载到内存中需要约 10-30 秒，之后转录速度会很快
- **如果您已经在使用 OpenAI API 进行语音转录**，请将 `tools.media.audio` 的配置文件替换为以下内容

## 快速入门

### 1. 安装依赖项
```bash
pip3 install -r requirements.txt
```

### 2. 启动守护进程
```bash
python3 scripts/daemon.py
```
首次运行时会下载 Whisper 模型（约 1.5GB）。等待“Ready”提示即可。

### 3. 添加到 OpenClaw 配置文件中

将以下配置添加到您的 `~/.openclaw/openclaw.json` 文件中：
```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "models": [
          {
            "type": "cli",
            "command": "~/.openclaw/workspace/skills/local-whisper/scripts/transcribe.sh",
            "args": ["{{MediaPath}}"],
            "timeoutSeconds": 60
          }
        ]
      }
    }
  }
}
```

### 4. 重启 OpenClaw 服务
```bash
openclaw gateway restart
```

现在，来自 Telegram、WhatsApp 等应用的语音消息将可以在本地免费转录！

### 手动测试
```bash
./scripts/transcribe.sh voice_message.ogg
```

## 使用场景：Telegram 语音消息

无需支付 OpenAI API 的费用，只需将 OpenClaw 指向这个本地守护进程即可实现免费转录。

## 登录时自动启动
```bash
cp com.local-whisper.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.local-whisper.plist
```

## API 信息

守护进程运行在 `localhost:8787` 端口：
```bash
curl -X POST http://localhost:8787/transcribe -F "file=@audio.ogg"
# {"text": "Hello world", "language": "en"}
```

## 语言支持

支持任意语言到英语的转录：

```bash
./scripts/transcribe.sh spanish_audio.ogg --translate
```

## 系统要求

- 需要安装支持 Apple Silicon（M1/M2/M3/M4）的 macOS 系统
- Python 3.9 或更高版本

## 许可证

MIT 许可证