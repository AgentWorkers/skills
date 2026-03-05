---
name: livekit-voice
description: LiveKit real-time voice and video infrastructure — create rooms, generate JWT access tokens, manage participants, and record sessions. Open source WebRTC for voice AI agents and real-time communication. Use for building voice agents, video rooms, or real-time audio.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, LiveKit Cloud or self-hosted
metadata: {"openclaw": {"emoji": "\ud83c\udfa7", "requires": {"env": ["LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]}, "primaryEnv": "LIVEKIT_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 🎧 LiveKit 语音服务

LiveKit 是为 OpenClaw 代理提供的实时语音/视频基础设施，支持创建房间、生成访问令牌、管理参与者以及与语音 AI 平台集成。

## 什么是 LiveKit？

[LiveKit](https://livekit.io) 是一个开源的 WebRTC 基础设施平台，用于构建实时音频/视频应用程序。它为语音 AI 代理、视频会议、实时流媒体等功能提供支持。

**自托管 vs 云服务：**
- **LiveKit Cloud**：托管服务，无需维护基础设施
- **自托管**：通过 Docker/Kubernetes 在自己的服务器上部署

## 所需配置项

| 配置项 | 是否必需 | 说明 |
|----------|----------|-------------|
| `LIVEKIT_API_KEY` | ✅ | LiveKit API 密钥 |
| `LIVEKIT_API_SECRET` | ✅ | LiveKit API 密码 |
| `LIVEKIT_URL` | ✅ | LiveKit 服务器地址（例如：`wss://your-project.livekit.cloud`） |

## 快速入门

```bash
# Create a room
python3 {baseDir}/scripts/livekit_api.py create-room my-room

# Create room with options
python3 {baseDir}/scripts/livekit_api.py create-room my-room --max-participants 10 --empty-timeout 300

# Generate access token for a participant
python3 {baseDir}/scripts/livekit_api.py token my-room --identity user123 --name "John"

# Generate token with specific grants
python3 {baseDir}/scripts/livekit_api.py token my-room --identity agent --can-publish --can-subscribe

# List active rooms
python3 {baseDir}/scripts/livekit_api.py list-rooms

# List participants in a room
python3 {baseDir}/scripts/livekit_api.py participants my-room

# Delete a room
python3 {baseDir}/scripts/livekit_api.py delete-room my-room

# Start recording (Egress)
python3 {baseDir}/scripts/livekit_api.py record my-room --output s3://bucket/recording.mp4
```

## 命令示例

### `create-room <房间名称>`
创建一个新的 LiveKit 房间。
- `--max-participants N`：限制参与者数量
- `--empty-timeout N`：房间空置后自动关闭的时间（默认为 300 秒）

### `token <房间名称>`
为参与者生成 JWT 访问令牌。
- `--identity ID`：参与者身份（必填）
- `--name NAME`：显示名称
- `--can-publish`：允许发布音频/视频
- `--can-subscribe`：允许订阅其他参与者的内容
- `--ttl N`：令牌的有效时间（以秒为单位，默认为 3600 秒）

### `list-rooms`
列出所有活跃的房间及其参与者数量。

### `participants <房间名称>`
列出房间中的参与者及其连接状态。

### `delete-room <房间名称>`
删除/关闭房间并断开所有参与者的连接。

### `record <房间名称>`
开始录制房间内的音频内容。
- `--output URL`：输出路径（S3、GCS 或本地路径）

## 语音 AI 集成

LiveKit 是许多语音 AI 平台的核心组件：
- **Vapi**：利用 LiveKit 实现实时语音 AI 交互
- **ElevenLabs**：将 TTS 音频流传输到 LiveKit 房间
- **OpenAI Realtime**：将 GPT-4o 生成的文本转换为语音并发送给 LiveKit 参与者

### 代理使用流程：
1. 创建一个 LiveKit 房间
2. 为人类参与者和 AI 代理生成访问令牌
3. AI 代理加入房间并订阅人类参与者的音频
4. 处理音频数据 → 转换为文本 → 通过大型语言模型（LLM）生成语音 → 再将语音发送回房间
5. 结果：实现与 AI 的实时语音对话

## 开发者信息
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发
[YouTube 频道](https://youtube.com/@aiwithabidi) | [GitHub 仓库](https://github.com/aiwithabidi)
该功能属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)