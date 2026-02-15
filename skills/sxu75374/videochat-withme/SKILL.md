---
name: videochat-withme
description: |
  Real-time AI video chat that routes through your OpenClaw agent. Uses Groq Whisper (cloud STT),
  edge-tts (cloud TTS via Microsoft), and OpenClaw chatCompletions API for conversation. Your agent
  sees your camera, hears your voice, and responds with its own personality and memory.
  Requires: GROQ_API_KEY for speech recognition. Reads ~/.openclaw/openclaw.json for gateway port and auth token.
  Data flows: audio → Groq cloud (STT), TTS text → Microsoft cloud (edge-tts), camera frames (base64) + text
  → OpenClaw gateway → your configured LLM provider (may be cloud — frames leave the machine if using a cloud LLM).
  Installs a persistent launchd service (optional). Trigger phrases: "video chat", "voice call",
  "call me", "视频一下", "语音", "打电话给我", "我要和你视频", "videochat-withme".
metadata:
  {
    "openclaw":
      {
        "emoji": "🎥",
        "requires":
          {
            "bins": ["python3", "ffmpeg"],
            "env": ["GROQ_API_KEY"],
            "config": ["gateway.http"],
          },
      },
  }
---

# 视频通话功能（videochat-withme）

通过 OpenClaw 代理进行实时视频通话——该代理具备完整的人格表现、记忆功能以及视觉交互能力。

## 首次使用时的设置

新用户在安装该功能后需要运行以下命令一次：

```bash
bash skills/videochat-withme/scripts/setup.sh
```

该命令会处理所有相关设置：依赖项的安装、Groq API 密钥的配置、SSL 证书的生成，以及 launchd 服务的启动。

## 前提条件

- macOS 系统（必须使用 launchd 服务）
- Python 3.10 及更高版本
- OpenClaw 代理已启动，并且启用了 chatCompletions 功能

### Groq API 密钥（用于语音识别）

1. 在以下链接获取免费 API 密钥：https://console.groq.com/keys
2. 将密钥保存到相应的文件中：
   ```bash
   mkdir -p ~/.openclaw/secrets
   echo "your-key-here" > ~/.openclaw/secrets/groq_api_key.txt
   ```
   或者将其设置为环境变量：`export GROQ_API_KEY="your-key-here"`

### 启用 chatCompletions 功能

在 `~/.openclaw/openclaw.json` 文件中添加以下配置：
```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true }
      }
    }
  }
}
```
之后重新启动 OpenClaw 代理。

## 使用方法（代理端操作说明）

当用户请求视频/语音通话时：

**步骤 1：检查服务是否正在运行：**
```bash
curl -sk https://localhost:8766/api/config 2>/dev/null || curl -s http://localhost:8766/api/config 2>/dev/null
```

**步骤 2：如果服务未运行，则需要执行设置操作：**
1. 检查 Groq API 密钥是否已正确配置：
   `cat ~/.openclaw/secrets/groq_api_key.txt 2>/dev/null`
   - 如果密钥缺失，提示用户前往 https://console.groq.com/keys 获取密钥，并将其保存到 `~/.openclaw/secrets/groq_api_key.txt` 文件中。
2. 询问用户：“在视频通话中我应该使用什么名称来称呼您？”
3. 运行设置脚本：
   ```bash
   bash skills/videochat-withme/scripts/setup.sh --auto --agent-name "YourName" --user-name "TheirName"
   ```

**步骤 3：根据用户连接方式选择合适的通话方式：**

根据用户的连接方式（是通过网页聊天、桌面应用还是 Telegram/手机等），选择最合适的通话方式：

1. **用户使用电脑**（收到来自网页聊天或桌面应用的连接请求）：
   ```bash
   bash skills/videochat-withme/scripts/call.sh
   ```
   此时系统会弹出 macOS 的来电通知窗口，用户点击“接受”后，浏览器会自动打开通话页面。

2. **用户使用手机或远程设备**（收到来自 Telegram/手机的连接请求）：
   自动选择合适的通话 URL：
   ```bash
   # Prefer Tailscale IP (works from any network)
   TS_IP=$(tailscale ip -4 2>/dev/null)
   # Fallback to local IP (same WiFi only)
   LOCAL_IP=$(python3 -c "import socket; s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.connect(('8.8.8.8',80)); print(s.getsockname()[0]); s.close()" 2>/dev/null)
   ```
   - 如果使用 Tailscale 服务：发送 `https://<tailscale-ip>:8766`（适用于任何网络环境）
   - 否则：发送 `https://<local-ip>:8766`（仅限于同一 WiFi 网络）
   **注意**：首次使用 Tailscale 服务时，需要先点击“高级设置”→“继续”以接受自签名证书。

## 系统架构

```
🎤 Voice → Groq Whisper (STT)
📷 Camera → base64 frame
    ↓
OpenClaw /v1/chat/completions → Your Agent
    ↓
edge-tts (TTS) → 🔊 Audio playback
```

## 脚本说明

**这些脚本会自动执行：**

| 脚本          | 执行时机                |
|----------------|---------------------|
| `setup.sh --auto`    | 首次使用时（如果服务未运行）       |
| `call.sh`       | 每次收到通话请求时           |

**用户可根据需要手动执行以下脚本：**

| 脚本          | 功能                        |
|----------------|-------------------------|
| `setup.sh`       | 手动执行设置操作             |
| `start.sh`       | 启动 OpenClaw 代理服务           |
| `stop.sh`       | 停止 OpenClaw 代理服务           |

## 配置参数

| 参数            | 默认值                | 说明                          |
|----------------|-----------------------------|
| `GROQ_API_KEY`     | （从 secrets 文件中读取）        | 用于 Whisper STT 语音识别的 Groq API 密钥 |
| `PORT`         | `8766`                | 服务器端监听端口                     |
| `AGENT_NAME`     | `AI Assistant`         | 代理的显示名称                     |
| `USER_NAME`     | `User`                | 用户的显示名称                     |
| `SSL_CERT`      | （自动检测）            | SSL 证书路径                     |
| `SSL_KEY`      | （自动检测）            | SSL 私钥路径                     |